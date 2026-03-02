import os
import re


def test_theoretical_notes_desi_reference_is_correct():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    path = os.path.join(repo_root, "docs", "theoretical_notes.md")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "arXiv:2404.03047" not in content
    assert re.search(r"arXiv:2404\.03002", content) is not None

