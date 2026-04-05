"""
UIDT COMPLIANCE TEST: No float() in /modules
=============================================
Directive: UIDT System Directive v4.1 — NUMERICAL DETERMINISM
           "never use float()" — applies to all files in /modules/

This test permanently enforces that no module inside /modules/
uses the forbidden float() or round() builtins on mpmath values.
It will catch any future regression introduced by LLM rewrites,
automatic refactoring, or merge conflicts.
"""

import ast
import os
import pytest

MODULES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../modules")
)

FORBIDDEN_CALLS = {"float", "round"}


def _collect_forbidden_calls(source: str) -> list[tuple[int, str]]:
    """Return list of (lineno, funcname) for forbidden calls found in source."""
    violations = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return violations
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Direct call: float(...) or round(...)
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                violations.append((node.lineno, node.func.id))
    return violations


def _get_module_files() -> list[str]:
    files = []
    for fname in os.listdir(MODULES_DIR):
        if fname.endswith(".py"):
            files.append(os.path.join(MODULES_DIR, fname))
    return files


@pytest.mark.parametrize("filepath", _get_module_files())
def test_no_float_or_round_in_module(filepath):
    """
    UIDT Directive: never use float() or round() in /modules/.
    Use mp.nstr() for string output, mpf() for precision arithmetic.
    Violation of this rule silently destroys 80-digit precision.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    violations = _collect_forbidden_calls(source)

    assert violations == [], (
        f"PRECISION VIOLATION in {os.path.basename(filepath)}:\n"
        + "\n".join(
            f"  Line {ln}: forbidden call to {fn}() "
            "— use mp.nstr() or mpf() instead"
            for ln, fn in violations
        )
    )
