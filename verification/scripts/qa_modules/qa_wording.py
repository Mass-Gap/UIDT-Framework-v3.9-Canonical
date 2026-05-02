import re
from pathlib import Path
import sys

FORBIDDEN_WORDS = [
    r"\bproven\b",
    r"\bfinal\b",
    r"\bholy grail\b",
    r"\bsolved\b",
    r"\bultimate\b",
    r"\bdefinitive\b"
]

def check_wording():
    files_to_check = []
    root_dir = Path(".")
    if (root_dir / "README.md").exists():
        files_to_check.append(root_dir / "README.md")
    if (root_dir / "FORMALISM.md").exists():
        files_to_check.append(root_dir / "FORMALISM.md")

    for p in root_dir.glob("docs/**/*.md"):
        files_to_check.append(p)
    for p in root_dir.glob("manuscript/**/*.tex"):
        files_to_check.append(p)
    for p in root_dir.glob("manuscript/**/*.md"):
        files_to_check.append(p)

    errors = []
    for file_path in files_to_check:
        # Exclude research docs to avoid infinite loop of reporting on research rules
        if "research" in str(file_path) or "qa" in str(file_path):
             continue
        try:
            content = file_path.read_text(encoding="utf-8")
            for word_pattern in FORBIDDEN_WORDS:
                matches = re.finditer(word_pattern, content, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 30)
                    end = min(len(content), match.end() + 30)
                    context = content[start:end].replace('\n', ' ')

                    if "[A]" not in context and "[A-]" not in context:
                        errors.append(f"File {file_path}: Found forbidden word '{match.group()}' without [A]/[A-] context -> \"...{context}...\"")
        except Exception as e:
            pass

    if errors:
        for err in errors:
            print(f"[QA-WORDING] ERROR: {err}")
        return False
    return True

if __name__ == "__main__":
    if not check_wording():
        sys.exit(1)
    print("QA Wording check passed.")
