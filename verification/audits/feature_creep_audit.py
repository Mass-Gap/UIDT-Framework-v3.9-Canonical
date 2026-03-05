#!/usr/bin/env python3
"""
UIDT Feature Creep Audit

Monitors module count and structural complexity growth to detect
architectural inflation without theoretical gain.

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
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = repo_root / "verification" / "results" / "audits"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"feature_creep_{timestamp}.json"
    
    # Count modules and scripts
    core_dir = repo_root / "core"
    modules_dir = repo_root / "modules"
    scripts_dir = repo_root / "verification" / "scripts"
    
    results = {
        "timestamp": timestamp,
        "module_counts": {},
        "script_counts": {},
        "complexity_metrics": {},
        "creep_detected": False
    }
    
    if core_dir.exists():
        core_files = list(core_dir.glob("*.py"))
        results["module_counts"]["core"] = len(core_files)
    
    if modules_dir.exists():
        module_files = list(modules_dir.glob("*.py"))
        results["module_counts"]["modules"] = len(module_files)
    
    if scripts_dir.exists():
        script_files = list(scripts_dir.glob("*.py"))
        results["script_counts"]["verification"] = len(script_files)
    
    # Simple complexity heuristic
    total_modules = sum(results["module_counts"].values())
    total_scripts = sum(results["script_counts"].values())
    
    results["complexity_metrics"]["total_modules"] = total_modules
    results["complexity_metrics"]["total_scripts"] = total_scripts
    results["complexity_metrics"]["module_to_script_ratio"] = (
        total_modules / total_scripts if total_scripts > 0 else 0
    )
    
    # Detect creep if module count exceeds reasonable threshold
    if total_modules > 50:
        results["creep_detected"] = True
        results["creep_reason"] = f"Module count ({total_modules}) exceeds threshold (50)"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Total modules: {total_modules}")
    print(f"Feature creep: {'YES' if results['creep_detected'] else 'NO'}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
