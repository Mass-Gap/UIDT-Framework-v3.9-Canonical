#!/usr/bin/env python3
"""
UIDT Formal Dependency Graph Generator
Generates formal_graph.json from axioms_registry.json
Evidence Category: [A] (Structural Analysis)
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
    output_path = repo_root / "verification" / "results" / "audits" / "formal_graph.json"
    
    if not axioms_path.exists():
        print(f"ERROR: {axioms_path} not found", file=sys.stderr)
        return 1
    
    with open(axioms_path, "r", encoding="utf-8") as f:
        axioms = json.load(f)
    
    # Build dependency graph
    graph = {
        "nodes": [],
        "edges": []
    }
    
    for axiom in axioms:
        graph["nodes"].append({
            "id": axiom["id"],
            "statement": axiom["statement"],
            "category": axiom.get("category", "UNKNOWN")
        })
        
        for dep in axiom.get("deps", []):
            graph["edges"].append({
                "from": dep,
                "to": axiom["id"],
                "type": "depends_on"
            })
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Nodes: {len(graph['nodes'])}, Edges: {len(graph['edges'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
