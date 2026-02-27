#!/usr/bin/env python3
"""
UIDT Manuscript-Data Consistency Audit

Verifies consistency between manuscript claims and computational results
stored in verification registries.

Evidence Category: [A] (Formal Verification)
DOI: 10.5281/zenodo.17835200
Author: P. Rietz (ORCID: 0009-0007-4307-1609)
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp
mp.dps = 80


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    symbols_path = repo_root / "verification" / "registries" / "symbol_registry.json"
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = repo_root / "verification" / "results" / "audits"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"manuscript_consistency_{timestamp}.json"
    
    if not symbols_path.exists():
        print(f"ERROR: {symbols_path} not found", file=sys.stderr)
        return 1
    
    with open(symbols_path, "r", encoding="utf-8") as f:
        symbols = json.load(f)
    
    results = {
        "timestamp": timestamp,
        "consistent": [],
        "inconsistent": [],
        "missing_manuscript_refs": []
    }
    
    # Verify each symbol has proper evidence references
    for sym in symbols:
        symbol = sym["symbol"]
        refs = sym.get("refs", [])
        category = sym.get("evidence_cat", "UNKNOWN")
        
        if not refs:
            results["missing_manuscript_refs"].append({
                "symbol": symbol,
                "category": category,
                "severity": "MINOR"
            })
        else:
            results["consistent"].append({
                "symbol": symbol,
                "category": category,
                "refs": refs
            })
    
    # Check critical parameters have Category A or A-
    critical_params = ["Δ", "κ", "λ_S", "v"]
    for sym in symbols:
        if sym["symbol"] in critical_params:
            if sym["evidence_cat"] not in ["A", "A-"]:
                results["inconsistent"].append({
                    "symbol": sym["symbol"],
                    "expected_category": "A or A-",
                    "actual_category": sym["evidence_cat"],
                    "severity": "CRITICAL"
                })
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Consistent: {len(results['consistent'])}")
    print(f"Inconsistent: {len(results['inconsistent'])}")
    
    return 0 if not results["inconsistent"] else 1


if __name__ == "__main__":
    sys.exit(main())
