import json
from pathlib import Path
import sys

def check_evidence():
    claims_file = Path("verification/data/CLAIMS_public.json")
    if not claims_file.exists():
        print("[QA-EVIDENCE] ERROR: verification/data/CLAIMS_public.json not found.")
        return False

    try:
        with open(claims_file, 'r', encoding="utf-8") as f:
            claims_data = json.load(f)
    except Exception as e:
        print(f"[QA-EVIDENCE] ERROR reading CLAIMS_public.json: {e}")
        return False

    claims = claims_data.get("claims", [])
    errors = []

    for claim in claims:
        evidence = claim.get("evidence")
        claim_type = claim.get("type")
        status = claim.get("status")

        if claim_type == "cosmology":
            if evidence in ["A", "A-", "B"]:
                errors.append(f"Claim {claim.get('id')}: Cosmology claims MUST NOT be Category {evidence}. Max is C.")

        # Adjusting the prediction rule to allow C for calibrated predictions or E for speculative ones
        if claim_type == "prediction" and evidence not in ["C", "D", "E"]:
            errors.append(f"Claim {claim.get('id')}: Predictions should be C, D or E. Found: {evidence}.")

        if evidence not in ["A", "A-", "B", "C", "D", "E"]:
            errors.append(f"Claim {claim.get('id')}: Invalid evidence tag '{evidence}'. Must be A, A-, B, C, D, or E.")

    files_to_check = []
    root_dir = Path(".")
    if (root_dir / "README.md").exists():
        files_to_check.append(root_dir / "README.md")
    for p in root_dir.glob("docs/**/*.md"):
        files_to_check.append(p)

    for file_path in files_to_check:
        if "research" in str(file_path) or "qa" in str(file_path) or "Protocol" in str(file_path):
             continue
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "[A]" in line or "[B]" in line or "[A-]" in line:
                    if "Cosmology" in line or "Hubble" in line or "H₀" in line:
                        errors.append(f"File {file_path} (line {i+1}): Found Cosmology/Hubble claim with A/B tag. This is forbidden.")
        except Exception:
            pass

    if errors:
        for err in errors:
            print(f"[QA-EVIDENCE] ERROR: {err}")
        return False

    return True

if __name__ == "__main__":
    if not check_evidence():
        sys.exit(1)
    print("QA Evidence check passed.")
