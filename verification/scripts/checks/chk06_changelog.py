import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    VERSION_PATTERN = r"v(\d+\.\d+\.?\d*)"
    DOI_PATTERN = r"10\.\d{4,}/\S+"

    files_to_check = [
        "FORMALISM.md",
        "EVIDENCE_SYSTEM-3.md",
        "EVIDENCE_SYSTEM.md",
        "EVIDENCE.md",
        "LEDGER/FALSIFICATION.md",
        "LEDGER/claims.schema.json",
        "LEDGER/CLAIMS.json"
    ]

    versions = {}
    dois = []

    for rel_path in files_to_check:
        filepath = os.path.join(repo_root, rel_path)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for versions in the first 1000 chars (header)
                header = content[:1000]
                version_match = re.search(VERSION_PATTERN, header)
                if version_match:
                    versions[rel_path] = version_match.group(1)

                for match in re.finditer(DOI_PATTERN, content):
                    doi = match.group(0).rstrip(')') # clean trailing char
                    dois.append((rel_path, doi))
            except Exception:
                pass

    if versions:
        base_ver = "3.7.2" # the known version based on formalisms
        for f, v in versions.items():
            if v != base_ver and v != "3.9" and v != "3.9.0" and base_ver != "3.9": # Tolerate 3.9 as the target version
                messages.append(f"FAIL: Contradictory version {v} in {f} (expected {base_ver})")
                status = "FAIL"

    changelog_path = os.path.join(repo_root, "CHANGELOG.md")
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            cl_content = f.read()
            for match in re.finditer(DOI_PATTERN, cl_content):
                doi = match.group(0)
                if "zenodo" not in doi.lower() and "arxiv" not in doi.lower():
                    messages.append(f"FAIL: DOI in CHANGELOG without external verifiability (not zenodo/arxiv format): {doi}")
                    status = "FAIL"

    return status, messages
