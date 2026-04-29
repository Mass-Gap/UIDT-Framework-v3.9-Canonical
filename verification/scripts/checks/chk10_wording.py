import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    FORBIDDEN_WORDS = {
        "FAIL": [
            (r"\bsolved\b", "Constitution: verboten ohne Beweis"),
            (r"\bdefinitive\b", "Prestige language forbidden"),
            (r"\bultimate\b", "Prestige language forbidden"),
            (r"\bholy grail\b", "Prestige language forbidden"),
            (r"A\+\+?", "Nicht-existente Evidenzkategorie"),
            (r"(?i)UIDT\s+(?:solves|proves)\s+Yang.?Mills", "Muss 'attempt' sein"),
            (r"(?i)(?:solves|resolves)\s+(?:the\s+)?(?:Hubble|S8)\s+tension", "[TENSION ALERT] + FAIL")
        ],
        "WARN": [
            (r"\bfinal proof\b", "Prestige language"),
            (r"\bcomplete proof\b", "Prestige language"),
            (r"\bproven beyond\b", "Prestige language"),
            (r"100%\s+agree", "Prestige language"),
            (r"\bsettles\s+the\b", "Prestige language"),
            (r"\bresolved\b", "Gilt für H₀-/S₈-Tension")
        ]
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

                    for level, patterns in FORBIDDEN_WORDS.items():
                        for pattern, reason in patterns:
                            if re.search(pattern, content):
                                messages.append(f"{level}: Wording issue in {os.path.basename(filepath)} - '{pattern}': {reason}")
                                if level == "FAIL":
                                    status = "FAIL"
                                elif status == "PASS" and level == "WARN":
                                    status = "WARN"
                except Exception:
                    pass

    return status, messages
