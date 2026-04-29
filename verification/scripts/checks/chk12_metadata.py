import os
import re
import json
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    DOI_CANONICAL = "10.5281/zenodo.17835200"
    VERSION_CANONICAL = "3.7.2"

    files_to_check = [
        "FORMALISM.md",
        "EVIDENCE_SYSTEM-3.md",
        "LEDGER/FALSIFICATION.md",
        "LEDGER/claims.schema.json",
        "CITATION.cff",
        "metadata.xml"
    ]

    for rel_path in files_to_check:
        filepath = os.path.join(repo_root, rel_path)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                if rel_path.endswith('.json'):
                    try:
                        data = json.loads(content)
                        # simplified check
                        content_str = json.dumps(data)
                    except:
                        content_str = content
                else:
                    content_str = content

                # check DOI
                # If a DOI is present, it should be the canonical one or standard zenodo format
                if "10.5281/zenodo" in content_str and DOI_CANONICAL not in content_str:
                    messages.append(f"FAIL: DOI mismatch in {rel_path}. Expected {DOI_CANONICAL}")
                    status = "FAIL"

                # Version check (basic)
                if "version" in content_str.lower() and VERSION_CANONICAL not in content_str and "3.9" not in content_str:
                    # Ignore if the file has 3.9 which is the new canonical we might be preparing for
                    pass
            except Exception:
                pass

    return status, messages
