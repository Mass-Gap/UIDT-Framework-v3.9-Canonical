import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    falsification_path = os.path.join(repo_root, "LEDGER", "FALSIFICATION.md")
    if not os.path.exists(falsification_path):
        return status, messages

    try:
        with open(falsification_path, 'r', encoding='utf-8') as f:
            content = f.read()

        REQUIRED_FALSIFICATION_STRUCTURE = {
            "prediction_value": r"\d+\.?\d*\s*(?:GeV|MeV|nm|%|km/s/Mpc)",
            "falsification_condition": r"(?i)Falsification Condition",
            "sigma_threshold": r"\d+[\.\d]*[σs]",
            "experimental_channel": r"(?i)(?:Lattice|AFM|LHC|DESI|CMB|Casimir)",
        }

        # Split into active tests
        tests = re.split(r'### F\d+:', content)[1:] # Skip preamble

        for i, test in enumerate(tests, 1):
            if not re.search(REQUIRED_FALSIFICATION_STRUCTURE["prediction_value"], test):
                messages.append(f"FAIL: Prediction F{i} missing numerical threshold in FALSIFICATION.md")
                status = "FAIL"
            if not re.search(REQUIRED_FALSIFICATION_STRUCTURE["falsification_condition"], test):
                messages.append(f"FAIL: Prediction F{i} missing 'Falsification Condition' in FALSIFICATION.md")
                status = "FAIL"
            if not re.search(REQUIRED_FALSIFICATION_STRUCTURE["experimental_channel"], test):
                messages.append(f"FAIL: Prediction F{i} missing experimental channel in FALSIFICATION.md")
                status = "FAIL"

    except Exception as e:
        messages.append(f"FAIL: Error parsing FALSIFICATION.md: {str(e)}")
        status = "FAIL"

    return status, messages
