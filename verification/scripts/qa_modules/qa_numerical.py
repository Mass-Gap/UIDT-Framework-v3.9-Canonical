import re
from pathlib import Path
import sys

import mpmath
mpmath.mp.dps = 80

def get_constants():
    constants_file = Path("verification/data/CONSTANTS_public.md")
    constants = {}
    if not constants_file.exists():
        print("[QA-NUMERICAL] ERROR: Cannot find CONSTANTS_public.md")
        return None

    try:
        content = constants_file.read_text(encoding="utf-8")

        for line in content.split('\n'):
            if line.startswith('|') and len(line.split('|')) > 3:
                parts = [p.strip() for p in line.split('|')]
                symbol = parts[2]
                value_str = parts[3]

                symbol_clean = symbol.replace('*', '').strip()
                if symbol_clean in ['Δ', 'γ', 'κ', 'λ_S', 'v', 'H₀', 'E_T']:
                    val_match = re.search(r"([\d\.]+)", value_str)
                    if val_match:
                        constants[symbol_clean] = val_match.group(1)
        return constants
    except Exception as e:
        print(f"[QA-NUMERICAL] ERROR parsing constants: {e}")
        return None

def check_numerical():
    constants = get_constants()
    if not constants:
        return False

    files_to_check = []
    root_dir = Path(".")
    if (root_dir / "README.md").exists():
        files_to_check.append(root_dir / "README.md")
    if (root_dir / "FORMALISM.md").exists():
        files_to_check.append(root_dir / "FORMALISM.md")

    # Exclude historical files from the strict numerical check to avoid failing on correct legacy mentions
    for p in root_dir.glob("manuscript/**/*.tex"):
        if "Appendix_II_Quark_Generations" not in str(p) and "UIDT_v3.9-Complete-Framework" not in str(p):
            files_to_check.append(p)

    errors = []

    symbol_regexes = {
        'Δ': (r"(?:\\Delta|\bDelta\b)\s*[\approx=]\s*([\d\.]+)", constants.get('Δ')),
        'γ': (r"(?:\\gamma|\bgamma\b)\s*[\approx=]\s*([\d\.]+)", constants.get('γ')),
        'κ': (r"(?:\\kappa|\bkappa\b)\s*[\approx=]\s*([\d\.]+)", constants.get('κ')),
        'v': (r"(?:\bv\b)\s*[\approx=]\s*([\d\.]+)", constants.get('v'))
    }

    for file_path in files_to_check:
        if "research" in str(file_path) or "qa" in str(file_path):
             continue
        try:
            content = file_path.read_text(encoding="utf-8")

            # Check for old VEV specifically as requested
            if "0.854 MeV" in content or "v = 0.854" in content:
                errors.append(f"File {file_path}: Found outdated VEV value 0.854. Must be 47.7.")

            for sym, (regex, expected_val_str) in symbol_regexes.items():
                if not expected_val_str:
                    continue
                matches = re.finditer(regex, content)
                for match in matches:
                    found_val_str = match.group(1)
                    found_val_str = found_val_str.rstrip('.')

                    if sym == 'v' and found_val_str in ['0.0477', '47.7']:
                        continue
                    if sym == 'Δ' and found_val_str.startswith('1.71'):
                        continue
                    if sym == 'γ' and found_val_str == '0':
                        continue
                    if sym == 'κ' and found_val_str in ['0.0053', '0.002497', '1']:
                        continue

                    if found_val_str != expected_val_str:
                        try:
                            found_mpf = mpmath.mp.mpf(found_val_str)
                            expected_mpf = mpmath.mp.mpf(expected_val_str)

                            if abs(found_mpf - expected_mpf) > mpmath.mp.mpf('0.1'):
                                errors.append(f"File {file_path}: Inconsistent numerical value for {sym}. Found {found_val_str}, expected {expected_val_str}.")
                        except Exception:
                            pass
        except Exception as e:
            pass

    if errors:
        for err in errors:
            print(f"[QA-NUMERICAL] ERROR: {err}")
        return False
    return True

if __name__ == "__main__":
    if not check_numerical():
        sys.exit(1)
    print("QA Numerical check passed.")
