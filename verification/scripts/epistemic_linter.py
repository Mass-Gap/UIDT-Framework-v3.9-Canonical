#!/usr/bin/env python3
# ============================================================================
# UIDT v3.9 Canonical — Epistemic Linter
# Vacuum Information Density as the Fundamental Geometric Scalar
# DOI: 10.5281/zenodo.17835200
# Author: P. Rietz (ORCID: 0009-0007-4307-1609)
# ============================================================================
# This script scans modified Markdown files for forbidden language regarding
# cosmological and phenomenological claims.
# E.g., preventing "γ is derived" or "H₀ is proven".
# ============================================================================

import sys
import re
from pathlib import Path

# Fix unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Phrases that imply Category A/A- certainty
FORBIDDEN_PHRASES = [
    re.compile(r'\b(proven|solved|derived|exact proof)\b', re.IGNORECASE)
]

# Claims that must NOT be associated with the forbidden phrases
RESTRICTED_ENTITIES = [
    r'γ', r'gamma',
    r'H₀', r'Hubble',
    r'w₀', r'Dark Energy',
    r'm_S', r'Scalar Mass',
    r'Cosmology'
]

def scan_file(file_path):
    path = Path(file_path)
    if not path.exists():
        return 0
        
    content = path.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    # Phrases that negate the certainty
    NEGATIONS = [re.compile(r'\b(not|never|incorrect|false)\b', re.IGNORECASE)]
    
    errors = 0
    for i, line in enumerate(lines):
        has_restricted = any(re.search(entity, line, re.IGNORECASE) for entity in RESTRICTED_ENTITIES)
        if has_restricted:
            # Check if there is a negation near the forbidden phrase
            has_negation = any(neg.search(line) for neg in NEGATIONS)
            if has_negation:
                continue
                
            for phrase in FORBIDDEN_PHRASES:
                match = phrase.search(line)
                if match:
                    print(f"::error file={file_path},line={i+1}::Epistemic Violation: Found '{match.group(1)}' near restricted entity in '{line.strip()}'")
                    errors += 1
                    
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: epistemic_linter.py <file1.md> <file2.md> ...")
        sys.exit(0)
        
    total_errors = 0
    for arg in sys.argv[1:]:
        if arg.endswith('.md'):
            total_errors += scan_file(arg)
            
    if total_errors > 0:
        print(f"FAILED: Found {total_errors} epistemic violations. See errors above.")
        sys.exit(1)
    else:
        print("PASSED: Epistemic language is compliant.")
        sys.exit(0)

if __name__ == "__main__":
    main()
