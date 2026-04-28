#!/usr/bin/env python3
# ============================================================================
# UIDT v3.9 Canonical — Global SSoT Ledger Sync
# Vacuum Information Density as the Fundamental Geometric Scalar
# DOI: 10.5281/zenodo.17835200
# Author: P. Rietz (ORCID: 0009-0007-4307-1609)
# ============================================================================
# This script reads the LEDGER/CLAIMS.json Single Source of Truth and
# updates parameters and evidence tags across all canonical Markdown files.
# It ensures epistemic integrity and prevents documentation drift.
# ============================================================================

import json
import re
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Mapping from Claim ID to canonical symbol and regex patterns for tables
PARAM_MAP = {
    "UIDT-C-030": {"symbol": "Δ*", "regex_name": r"Spectral Gap|Δ\*"},
    "UIDT-C-031": {"symbol": "γ", "regex_name": r"Gamma Invariant|γ(?!\S)"},
    "UIDT-C-032": {"symbol": "γ_MC", "regex_name": r"Gamma MC Mean|γ_MC"},
    "UIDT-C-043": {"symbol": "γ_∞", "regex_name": r"Bare Gamma|γ_∞"},
    "UIDT-C-033": {"symbol": "κ", "regex_name": r"Coupling|κ(?!\S)"},
    "UIDT-C-034": {"symbol": "λ_S", "regex_name": r"Self-Coupling|λ_S"},
    "UIDT-C-036": {"symbol": "v", "regex_name": r"VEV|v(?!\S)"},
    "UIDT-C-035": {"symbol": "m_S", "regex_name": r"Scalar Mass|m_S"},
    "UIDT-C-044": {"symbol": "E_T", "regex_name": r"Torsion (Energy|Basis Energy)|E_T"},
    "UIDT-C-048": {"symbol": "f_vac", "regex_name": r"Vacuum Frequency|f_vac"},
    "UIDT-C-029": {"symbol": "H₀", "regex_name": r"Hubble Constant|H₀"},
    "UIDT-C-037": {"symbol": "w₀", "regex_name": r"Dark Energy EOS|w₀"},
    "UIDT-C-045": {"symbol": "w_a", "regex_name": r"DE Evolution|w_a"},
    "UIDT-C-047": {"symbol": "Σmν", "regex_name": r"Neutrino Sum|Σmν"},
    "UIDT-C-019": {"symbol": "λ_UIDT", "regex_name": r"UIDT Wavelength|λ_UIDT"},
    "UIDT-C-020": {"symbol": "S₈", "regex_name": r"S8 Parameter|S₈"},
    "UIDT-C-021": {"symbol": "d_opt", "regex_name": r"Casimir Distance|d_opt"}
}

def load_claims():
    ledger_path = Path("LEDGER/CLAIMS.json")
    if not ledger_path.exists():
        logging.error("CLAIMS.json not found.")
        sys.exit(1)
    with open(ledger_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_evidence(claims_data):
    """
    Extract evidence categories for each parameter from CLAIMS.json
    """
    evidence_map = {}
    for claim in claims_data.get("claims", []):
        cid = claim["id"]
        if cid in PARAM_MAP:
            ev = claim.get("evidence", "E")
            if "pi_override" in claim and "evidence_override" in claim["pi_override"]:
                ev = claim["pi_override"]["evidence_override"]
            
            evidence_map[cid] = {
                "symbol": PARAM_MAP[cid]["symbol"],
                "regex_name": PARAM_MAP[cid]["regex_name"],
                "evidence": ev
            }
    return evidence_map

def sync_markdown_table(content, evidence_map):
    """
    Updates ONLY the Category column in markdown tables.
    Format typically: | **Name** | Symbol | Value | Uncertainty | Category | Notes |
    """
    updated = content
    for cid, data in evidence_map.items():
        # Match: | **Name** | Symbol | Value | Unc | [A-E-] | Notes |
        row_regex = re.compile(
            r'(\|\s*\*\*.*?' + data["regex_name"] + r'.*?\*\*\s*\|\s*' + 
            re.escape(data["symbol"]) + r'\s*\|[^\|]+\|[^\|]+\|\s*)([A-E]\-?)(\s*\|.*)',
            re.MULTILINE
        )
        
        def repl(match):
            prefix = match.group(1)
            suffix = match.group(3)
            return f"{prefix}{data['evidence']}{suffix}"
            
        updated = row_regex.sub(repl, updated)
    return updated

def sync_quick_copy_block(content, evidence_map):
    """
    Updates ONLY the [Category] brackets in the quick copy block.
    Format: Δ* = 1.710 ± 0.015 GeV   [A]  Spectral gap
    """
    updated = content
    for cid, data in evidence_map.items():
        row_regex = re.compile(
            r'^(' + re.escape(data["symbol"]) + r'\s*=[^\[]+)\[([A-E]\-?)\](.*)',
            re.MULTILINE
        )
        
        def repl(match):
            prefix = match.group(1)
            suffix = match.group(3)
            return f"{prefix}[{data['evidence']}]{suffix}"
            
        updated = row_regex.sub(repl, updated)
    return updated

def process_file(file_path, evidence_map):
    path = Path(file_path)
    if not path.exists():
        return False
        
    orig_content = path.read_text(encoding="utf-8")
    content = orig_content
    
    content = sync_markdown_table(content, evidence_map)
    content = sync_quick_copy_block(content, evidence_map)
    
    if content != orig_content:
        path.write_text(content, encoding="utf-8")
        logging.info(f"Updated {file_path}")
        return True
    return False

def main():
    logging.info("Starting Global SSoT Sync (Evidence-Only Mode)...")
    claims_data = load_claims()
    evidence_map = extract_evidence(claims_data)
    
    docs_to_scan = [
        "CANONICAL/CONSTANTS.md",
        "CANONICAL/LIMITATIONS.md",
        "CANONICAL/FALSIFICATION.md",
        "CANONICAL/EVIDENCE.md"
    ]
    
    changes = 0
    for doc in docs_to_scan:
        if process_file(doc, evidence_map):
            changes += 1
            
    logging.info(f"Sync complete. Files updated: {changes}")
    sys.exit(0)

if __name__ == "__main__":
    main()
