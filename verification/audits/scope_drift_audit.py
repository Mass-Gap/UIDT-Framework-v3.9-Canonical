#!/usr/bin/env python3
"""
UIDT Scope Drift Audit

Analyzes framework evolution to detect scope expansion beyond
core Yang-Mills mass gap problem.

Evidence Category: [A] (Strategic Analysis)
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
    output_path = output_dir / f"scope_drift_{timestamp}.json"
    
    if not symbols_path.exists():
        print(f"ERROR: {symbols_path} not found", file=sys.stderr)
        return 1
    
    with open(symbols_path, "r", encoding="utf-8") as f:
        symbols = json.load(f)
    
    # Define core scope: Yang-Mills mass gap
    core_symbols = {"Δ", "κ", "λ_S", "v", "Λ_QCD"}
    cosmology_symbols = {"H₀", "S₈", "λ_UIDT"}
    
    results = {
        "timestamp": timestamp,
        "core_problem": "Yang-Mills mass gap (Clay Millennium Problem)",
        "core_parameters": [],
        "extended_parameters": [],
        "scope_drift_detected": False
    }
    
    for sym in symbols:
        symbol = sym["symbol"]
        category = sym.get("evidence_cat", "UNKNOWN")
        
        if symbol in core_symbols:
            results["core_parameters"].append({
                "symbol": symbol,
                "category": category,
                "scope": "core"
            })
        elif symbol in cosmology_symbols:
            results["extended_parameters"].append({
                "symbol": symbol,
                "category": category,
                "scope": "cosmology",
                "note": "Extension beyond core problem"
            })
            if category in ["A", "B"]:
                results["scope_drift_detected"] = True
        else:
            results["extended_parameters"].append({
                "symbol": symbol,
                "category": category,
                "scope": "extended"
            })
    
    results["core_ratio"] = len(results["core_parameters"]) / len(symbols) if symbols else 0
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Core parameters: {len(results['core_parameters'])}")
    print(f"Extended parameters: {len(results['extended_parameters'])}")
    print(f"Scope drift: {'YES' if results['scope_drift_detected'] else 'NO'}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
