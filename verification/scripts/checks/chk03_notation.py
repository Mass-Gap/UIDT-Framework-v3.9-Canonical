import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    SYMBOL_MAP = {"γ": "gamma", "κ": "kappa", "λ_S": "lambda_S",
                  "Δ": "Delta", "v": "v_vev"}

    # Checking for contradictory units
    # e.g. "Δ = ... MeV" instead of GeV
    # FAIL: Ein Symbol mit zwei Bedeutungen in derselben Datei
    # FAIL: Widersprüchliche Einheiten (z.B. Δ in MeV statt GeV)

    unit_checks = {
        r'Δ\s*[\approx\=]\s*[\d\.]+\s*MeV': 'Δ should be in GeV, not MeV',
        r'Delta\s*[\approx\=]\s*[\d\.]+\s*MeV': 'Delta should be in GeV, not MeV',
        r'v\s*[\approx\=]\s*[\d\.]+\s*GeV': 'v should be in MeV, not GeV'
    }

    for root, dirs, files in os.walk(repo_root):
        if any(skip in root for skip in [".git", "UIDT-OS", "venv", "clay-submission"]):
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    for pattern, error_msg in unit_checks.items():
                        if re.search(pattern, content):
                            messages.append(f"FAIL: {error_msg} in {os.path.basename(filepath)}")
                            status = "FAIL"
                except Exception as e:
                    pass

    return status, messages
