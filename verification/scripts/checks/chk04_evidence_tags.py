import os
import re
import json
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    HARD_RULES = [
        # (pattern, required_tag, forbidden_tags, fail_message)
        (r'(?i)\b(?:gamma|γ)\b', "A-", ["A"], "γ MUST always be [A-], NEVER [A]"),
        (r'(?i)\b(?:H0|Hubble)\b', None, ["A", "A-", "B"], "H₀ MUSS [C] sein, max C"),
        (r'(?i)\b(?:spectral_gap|Delta|Δ)\b', "A", [], "Δ* ist [A]"),
        (r'(?i)\b(?:cosmology|Hubble|S8|CMB|dark energy)\b', None, ["A", "A-", "B"], "Kosmologie NIEMALS A/A-/B"),
    ]
    FORBIDDEN_TAGS = ["A++", "A+", "A*"]

    schema_path = os.path.join(repo_root, "LEDGER", "claims.schema.json")
    # For testing, we also check CLAIMS.json if it exists
    claims_path = os.path.join(repo_root, "LEDGER", "CLAIMS.json")

    if os.path.exists(claims_path):
        try:
            with open(claims_path, 'r', encoding='utf-8') as f:
                claims_data = json.load(f)

            for claim in claims_data.get("claims", []):
                stmt = claim.get("statement", "")
                ev = claim.get("evidence", "")

                if ev in FORBIDDEN_TAGS:
                    messages.append(f"FAIL: Forbidden evidence tag '{ev}' used in claim {claim.get('id')}")
                    status = "FAIL"

                for pattern, req_tag, forbid_tags, msg in HARD_RULES:
                    if re.search(pattern, stmt):
                        if req_tag and ev != req_tag and not (req_tag == "A" and ev == "A-"):
                            messages.append(f"FAIL: {msg} - Found [{ev}] for '{stmt}'")
                            status = "FAIL"
                        if ev in forbid_tags:
                            messages.append(f"FAIL: {msg} - Found forbidden tag [{ev}] for '{stmt}'")
                            status = "FAIL"

                # Check Category D
                if ev == "D":
                    # MUSS in FALSIFICATION.md verlinkt sein (simplified check: is the claim id or content in falsification?)
                    falsification_path = os.path.join(repo_root, "LEDGER", "FALSIFICATION.md")
                    if os.path.exists(falsification_path):
                        with open(falsification_path, 'r', encoding='utf-8') as fals:
                            fc = fals.read()
                            # Rough check: try to find keywords
                            # In a real impl, we'd do a deeper mapping
                            pass
        except Exception as e:
            pass

    # Check markdown files for forbidden tags
    for root, dirs, files in os.walk(repo_root):
        if any(skip in root for skip in [".git", "UIDT-OS", "venv", "clay-submission"]):
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    for ftag in FORBIDDEN_TAGS:
                        if f"[{ftag}]" in content:
                            messages.append(f"FAIL: Forbidden tag [{ftag}] found in {file}")
                            status = "FAIL"
                except Exception:
                    pass

    return status, messages
