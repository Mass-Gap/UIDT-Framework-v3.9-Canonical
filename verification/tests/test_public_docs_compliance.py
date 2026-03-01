import os
import re


def test_readme_has_no_invalid_evidence_tags():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    forbidden = [
        r"\[A\+\]",
        r"\[B-\]",
        r"\[C\+\]",
        r"\[D\+\]",
        r"Category\s*A\+",
        r"Category\s*D\+",
    ]
    for pattern in forbidden:
        assert re.search(pattern, content, flags=re.IGNORECASE) is None


def test_readme_has_no_cosmology_closure_language():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    forbidden = [
        r"\bsolves?\b",
        r"\bresolved?\b",
        r"\bdefinitive\b",
        r"\bscientifically\s+closed\b",
        r"\bsolves\s+hubble\b",
        r"\bhubble\s+tension\s+resolution\b",
    ]
    for pattern in forbidden:
        assert re.search(pattern, content, flags=re.IGNORECASE) is None


def test_readme_delta_is_marked_as_spectral_gap():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert re.search(r"spectral\s+gap", content, flags=re.IGNORECASE) is not None

