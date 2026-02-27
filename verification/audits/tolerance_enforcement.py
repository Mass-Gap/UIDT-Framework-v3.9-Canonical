#!/usr/bin/env python3
"""
UIDT Tolerance Enforcement
Verifies all measurements include proper uncertainties
Evidence Category: [A] (Formal Verification)
DOI: 10.5281/zenodo.17835200
"""
import json
import re
import sys
from pathlib import Path

import mpmath as mp
mp.dps = 80  # Local precision declaration


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    symbols_path = repo_root / "verification" / "registries" / "symbol_registry.json"
    output_path = repo_root / "verification" / "results" / "audits" / "tolerance_enforcement.json"
    
    if not symbols_path.exists():
        print(f"ERROR: {symbols_path} not found", file=sys.stderr)
        return 1
    
    with open(symbols_path, "r", encoding="utf-8") as f:
        symbols = json.load(f)
    
    # Check for proper uncertainty notation
    results = {
        "with_uncertainty": [],
        "missing_uncertainty": [],
        "dimensionless": []
    }
    
    for sym in symbols:
        symbol = sym["symbol"]
        value = str(sym.get("value", ""))
        category = sym.get("evidence_cat", "UNKNOWN")
        
        # Check if value includes ± notation
        if "±" in value:
            results["with_uncertainty"].append({
                "symbol": symbol,
                "value": value,
                "category": category
            })
        elif category in ["A", "A-", "B", "C"] and sym.get("unit") != "dimensionless":
            results["missing_uncertainty"].append({
                "symbol": symbol,
                "value": value,
                "category": category
            })
        else:
            results["dimensionless"].append(symbol)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"With uncertainty: {len(results['with_uncertainty'])}, Missing: {len(results['missing_uncertainty'])}")
    return 0 if not results["missing_uncertainty"] else 1


if __name__ == "__main__":
    sys.exit(main())
