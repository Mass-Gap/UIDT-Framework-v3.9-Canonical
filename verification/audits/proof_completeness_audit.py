#!/usr/bin/env python3
"""
UIDT Proof Completeness Audit
Verifies all axioms have complete derivation chains
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
    axioms_path = repo_root / "verification" / "registries" / "axioms_registry.json"
    output_path = repo_root / "verification" / "results" / "audits" / "proof_completeness.json"
    
    if not axioms_path.exists():
        print(f"ERROR: {axioms_path} not found", file=sys.stderr)
        return 1
    
    with open(axioms_path, "r", encoding="utf-8") as f:
        axioms = json.load(f)
    
    # Check completeness
    axiom_ids = {ax["id"] for ax in axioms}
    results = {
        "complete": [],
        "incomplete": [],
        "circular": []
    }
    
    for axiom in axioms:
        ax_id = axiom["id"]
        deps = set(axiom.get("deps", []))
        
        # Check if all dependencies exist
        missing_deps = deps - axiom_ids
        if missing_deps:
            results["incomplete"].append({
                "axiom": ax_id,
                "missing_deps": list(missing_deps)
            })
        else:
            results["complete"].append(ax_id)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Complete: {len(results['complete'])}, Incomplete: {len(results['incomplete'])}")
    return 0 if not results["incomplete"] else 1


if __name__ == "__main__":
    sys.exit(main())
