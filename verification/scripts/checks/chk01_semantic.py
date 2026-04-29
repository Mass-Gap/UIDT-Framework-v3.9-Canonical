import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    TERM_VARIANTS = {
        "spectral_gap":  ["Lattice Torsion Binding Energy", "Torsion Energy",
                          "mass gap", "spectral gap", "Yang-Mills gap"],
        "gamma":         ["kinetic VEV", "gamma invariant", "γ"],
        "rg_constraint": ["RG fixed point", "renormalization group constraint",
                          "5κ²=3λ_S", "fixed-point condition"],
    }

    forbidden_pattern = re.compile(r'(?i)(particle\s+mass|Teilchenmasse)')
    allowed_pattern = re.compile(r'(?i)(NOT\s+particle\s+mass|keine\s+Teilchenmasse)')

    def check_file(filepath):
        nonlocal status
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            for concept, variants in TERM_VARIANTS.items():
                found_variants = []
                for variant in variants:
                    if variant.lower() in content.lower():
                        found_variants.append(variant)
                if len(found_variants) > 1:
                    messages.append(f"WARN: Multiple terms for {concept} in {os.path.basename(filepath)}: {found_variants}")
                    if status == "PASS":
                        status = "WARN"

            if 'Δ' in content or 'Delta' in content:
                for match in forbidden_pattern.finditer(content):
                    start = max(0, match.start() - 30)
                    end = min(len(content), match.end() + 30)
                    context = content[start:end]
                    if not allowed_pattern.search(context):
                        messages.append(f"FAIL: Forbidden association of Δ with 'particle mass' in {os.path.basename(filepath)}")
                        status = "FAIL"
        except Exception as e:
            pass

    for root, dirs, files in os.walk(repo_root):
        if any(skip in root for skip in [".git", "UIDT-OS", "venv", "clay-submission"]):
            continue
        for file in files:
            if file.endswith(".md"):
                check_file(os.path.join(root, file))

    return status, messages
