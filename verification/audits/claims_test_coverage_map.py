#!/usr/bin/env python3
"""
UIDT Claims Test Coverage Mapping

Maps theoretical claims to verification scripts and identifies
untested assertions requiring experimental validation.

Evidence Category: [A] (Structural Analysis)
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
    axioms_path = repo_root / "verification" / "registries" / "axioms_registry.json"
    scripts_dir = repo_root / "verification" / "scripts"
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = repo_root / "verification" / "results" / "audits"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"coverage_{timestamp}.json"
    
    if not axioms_path.exists():
        print(f"ERROR: {axioms_path} not found", file=sys.stderr)
        return 1
    
    with open(axioms_path, "r", encoding="utf-8") as f:
        axioms = json.load(f)
    
    # Count verification scripts
    test_scripts = []
    if scripts_dir.exists():
        test_scripts = [
            p.name for p in scripts_dir.glob("verify_*.py")
        ]
    
    coverage = {
        "timestamp": timestamp,
        "total_axioms": len(axioms),
        "total_test_scripts": len(test_scripts),
        "tested_axioms": [],
        "untested_axioms": [],
        "test_scripts": test_scripts
    }
    
    # Map axioms to tests (simplified heuristic)
    tested_ids = set()
    for script in test_scripts:
        if "rg_fixed_point" in script:
            tested_ids.add("AX-005")
        if "geometric_operator" in script:
            tested_ids.add("AX-008")
        if "light_quark" in script or "heavy_quark" in script:
            tested_ids.add("AX-010")
    
    for axiom in axioms:
        ax_id = axiom["id"]
        if ax_id in tested_ids:
            coverage["tested_axioms"].append({
                "id": ax_id,
                "statement": axiom["statement"][:80] + "...",
                "category": axiom.get("category", "UNKNOWN")
            })
        else:
            coverage["untested_axioms"].append({
                "id": ax_id,
                "statement": axiom["statement"][:80] + "...",
                "category": axiom.get("category", "UNKNOWN")
            })
    
    coverage["coverage_ratio"] = len(coverage["tested_axioms"]) / len(axioms) if axioms else 0
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Coverage: {coverage['coverage_ratio']:.1%}")
    print(f"Tested: {len(coverage['tested_axioms'])}/{len(axioms)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
