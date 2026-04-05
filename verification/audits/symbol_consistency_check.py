#!/usr/bin/env python3
"""
UIDT Symbol Consistency Check
Verifies symbol definitions are consistent across registry
Evidence Category: [A] (Formal Verification)
DOI: 10.5281/zenodo.17835200
"""
import json
import sys
from pathlib import Path

import mpmath as mp
mp.dps = 80  # Local precision declaration


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    symbols_path = repo_root / "verification" / "registries" / "symbol_registry.json"
    output_path = repo_root / "verification" / "results" / "audits" / "symbol_consistency.json"
    
    if not symbols_path.exists():
        print(f"ERROR: {symbols_path} not found", file=sys.stderr)
        return 1
    
    with open(symbols_path, "r", encoding="utf-8") as f:
        symbols = json.load(f)
    
    # Check for duplicates and inconsistencies
    results = {
        "consistent": [],
        "duplicates": [],
        "missing_units": []
    }
    
    seen_symbols = {}
    for sym in symbols:
        symbol = sym["symbol"]
        if symbol in seen_symbols:
            results["duplicates"].append({
                "symbol": symbol,
                "definitions": [seen_symbols[symbol], sym["defn"]]
            })
        else:
            seen_symbols[symbol] = sym["defn"]
            results["consistent"].append(symbol)
        
        if not sym.get("unit"):
            results["missing_units"].append(symbol)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Consistent: {len(results['consistent'])}, Duplicates: {len(results['duplicates'])}")
    return 0 if not results["duplicates"] else 1


if __name__ == "__main__":
    sys.exit(main())
