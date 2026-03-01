import os
import re


def test_modules_are_english_only_heuristic():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    modules_dir = os.path.join(repo_root, "modules")
    patterns = [
        r"[äöüß]",
        r"\bDieser\b",
        r"\bDieses\b",
        r"\bBerechnet\b",
        r"\bLeitet\b",
        r"\bInitialisiert\b",
        r"\bBenötigt\b",
        r"\bPrüft\b",
        r"\bQuelle\b",
        r"\bPräzision\b",
        r"\bVakuum\b",
        r"\bFaltung\b",
        r"\bLösung\b",
        r"\bSoll\b",
    ]
    combined = re.compile("|".join(patterns))

    for filename in os.listdir(modules_dir):
        if not filename.endswith(".py"):
            continue
        path = os.path.join(modules_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert combined.search(content) is None

