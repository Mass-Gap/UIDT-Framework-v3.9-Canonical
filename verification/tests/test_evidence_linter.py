"""
test_evidence_linter.py

Unit tests for evidence_linter.py rules.
All tests use synthetic in-memory content — no repository files read here.
No float(), no mocks, no MagicMock.
Framework: pytest
"""

import sys
import os
import pytest

# Make scripts importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from evidence_linter import lint_file, FORBIDDEN_LANGUAGE, INVALID_CATEGORY


def lines(text):
    return [l + "\n" for l in text.splitlines()]


# ---------------------------------------------------------------------------
# RULE-EL-01 tests
# ---------------------------------------------------------------------------
def test_el01_catches_solved():
    content = lines("The mass gap solved by UIDT. Spectral gap [A].")
    viol = lint_file("test.md", content)
    assert any(v[2] == "RULE-EL-01" for v in viol), "Should flag 'solved'"


def test_el01_allows_resolved_in_changelog():
    content = lines("RESOLVED: S1-04 w0 triple inconsistency. Decision D-002. [C]")
    viol = lint_file("test.md", content)
    assert not any(v[2] == "RULE-EL-01" for v in viol), (
        "RESOLVED inside changelog context should not trigger EL-01"
    )


def test_el01_clean_passes():
    content = lines("The spectral gap Delta* = 1.710 GeV is consistent with lattice QCD. [A]")
    viol = lint_file("test.md", content)
    assert not any(v[2] == "RULE-EL-01" for v in viol)


# ---------------------------------------------------------------------------
# RULE-EL-02 tests
# ---------------------------------------------------------------------------
def test_el02_catches_cosmo_with_evidence_A():
    content = lines("Hubble constant H_0 = 70.4 km/s/Mpc [A] from UIDT prediction.")
    viol = lint_file("test.md", content)
    assert any(v[2] == "RULE-EL-02" for v in viol), (
        "Cosmological claim with [A] should trigger EL-02"
    )


def test_el02_allows_cosmo_with_evidence_C():
    content = lines("Hubble constant H_0 = 70.4 km/s/Mpc [C] calibrated from DESI DR2.")
    viol = lint_file("test.md", content)
    assert not any(v[2] == "RULE-EL-02" for v in viol)


# ---------------------------------------------------------------------------
# RULE-EL-03 tests
# ---------------------------------------------------------------------------
def test_el03_catches_E_without_context_word():
    content = lines("Old torsion model. [E] Previous approach.")
    viol = lint_file("test.md", content)
    assert any(v[2] == "RULE-EL-03" for v in viol)


def test_el03_passes_with_withdrawn_nearby():
    content = lines("Old torsion model — withdrawn [E] in v3.3 due to formatting errors.")
    viol = lint_file("test.md", content)
    assert not any(v[2] == "RULE-EL-03" for v in viol)


# ---------------------------------------------------------------------------
# RULE-EL-04 tests
# ---------------------------------------------------------------------------
def test_el04_catches_invalid_category_Bplus():
    content = lines("Gamma = 16.339 [B+] highly verified.")
    viol = lint_file("test.md", content)
    assert any(v[2] == "RULE-EL-04" for v in viol), "[B+] is non-existent category"


def test_el04_allows_valid_categories():
    for cat in ["A", "A-", "B", "C", "D", "E"]:
        content = lines(f"Parameter value 1.23 [{cat}] as expected.")
        viol = lint_file("test.md", content)
        assert not any(v[2] == "RULE-EL-04" for v in viol), (
            f"Valid category [{cat}] should not trigger EL-04"
        )
