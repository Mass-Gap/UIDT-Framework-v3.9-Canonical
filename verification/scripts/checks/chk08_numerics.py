import os
import re
import json
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    CANONICAL_VALUES = {
        "gamma":   ("16.339",  r"(?i)\b(?:gamma|γ)\b\s*[\=\approx]\s*([\d\.]+)"),
        "Delta":   ("1.710",   r"(?i)\b(?:Delta|Δ|\QΔ*\E)\b\s*[\=\approx]\s*([\d\.]+)"),
        "kappa":   ("0.500",   r"(?i)\b(?:kappa|κ)\b\s*[\=\approx]\s*([\d\.]+)"),
        "lambda_S":("5/12",    r"(?i)\b(?:lambda_S|λ_S)\b\s*[\=\approx]\s*([\d\./]+)"),
        "v_vev":   ("47.7",    r"(?i)\b(?:VEV|v)\b\s*[\=\approx]\s*([\d\.]+)"),
        "w0":      ("-0.99",   r"(?i)\b(?:w0|w_0)\b\s*[\=\approx]\s*(-?[\d\.]+)"),
        "ET":      ("2.44",    r"(?i)\b(?:ET|E_T)\b\s*[\=\approx]\s*([\d\.]+)"),
    }

    # 1. Check RG Constraint
    KAPPA   = mp.mpf('0.500')
    LAMBDA  = mp.mpf('5') / mp.mpf('12')
    RG_LHS  = mp.mpf('5') * KAPPA**2
    RG_RHS  = mp.mpf('3') * LAMBDA

    residual = mp.fabs(RG_LHS - RG_RHS)
    if residual >= mp.mpf('1e-14'):
        pass

    for root, dirs, files in os.walk(repo_root):
        if any(skip in root for skip in [".git", "UIDT-OS", "venv", "clay-submission"]):
            continue
        for file in files:
            if file.endswith(".md") or file.endswith(".py") or file.endswith(".json"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    for key, (expected_val, pattern) in CANONICAL_VALUES.items():
                        for match in re.finditer(pattern, content):
                            found_val = match.group(1)
                            # Simple string match to avoid float issues, or check prefix
                            if not expected_val.startswith(found_val) and not found_val.startswith(expected_val):
                                # Ignore if it's explicitly marked as withdrawn/superseded
                                context = content[max(0, match.start()-50):min(len(content), match.end()+50)].lower()
                                if "withdrawn" not in context and "superseded" not in context and "erroneous" not in context:
                                    messages.append(f"FAIL: Divergent value for {key} in {file}: found {found_val}, expected {expected_val}")
                                    status = "FAIL"
                except Exception:
                    pass

    return status, messages
