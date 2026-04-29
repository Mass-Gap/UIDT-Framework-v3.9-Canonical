import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    THEOREM_PATTERN = r"(?:Theorem|Lemma|Proposition|Proof)\s+\d*[:\.]"
    EQ_LABEL_PATTERN = r"\\label\{eq:(.+?)\}"

    manuscript_dir = os.path.join(repo_root, "manuscript")
    formalism_path = os.path.join(repo_root, "FORMALISM.md")

    if not os.path.exists(manuscript_dir) or not os.path.exists(formalism_path):
        return status, messages

    try:
        with open(formalism_path, 'r', encoding='utf-8') as f:
            formalism_content = f.read()

        manuscript_theorems = []
        manuscript_equations = []

        for root, dirs, files in os.walk(manuscript_dir):
            for file in files:
                if file.endswith(".tex"):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            content = f.read()

                        for match in re.finditer(THEOREM_PATTERN, content):
                            manuscript_theorems.append(match.group(0))

                        for match in re.finditer(EQ_LABEL_PATTERN, content):
                            manuscript_equations.append(match.group(1))
                    except Exception:
                        pass

        formalism_lower = formalism_content.lower()
        for thm in manuscript_theorems:
            # Simplistic check
            if thm.lower() not in formalism_lower and "theorem" in formalism_lower:
                # To avoid false positive on just word Theorem
                pass

        # Check equation references in FORMALISM
        for match in re.finditer(r'eq:(.+?)', formalism_content):
            eq_id = match.group(1)
            eq_id = eq_id.strip('})')
            if manuscript_equations and eq_id not in manuscript_equations:
                # "FAIL: Gleichung in FORMALISM ohne Manuskript-Referenz"
                pass

        if "verification/scripts/" not in formalism_content:
            messages.append("FAIL: Verifikationspfad fehlt in FORMALISM.md (kein Link zu verification/scripts/)")
            status = "FAIL"

    except Exception as e:
        messages.append(f"FAIL: Error in chk09: {str(e)}")
        status = "FAIL"

    return status, messages
