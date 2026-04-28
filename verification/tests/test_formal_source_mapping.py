"""
[UIDT-v3.9] Verification tests — Step 4e: formal Lagrangian closure
====================================================================

Purpose:
  Verify that the explicit source term h*phi reproduces the Step-4c
  stationary equation exactly and that the formal Stratum-III mapping is
  internally consistent.

Constitution rules:
  - mp.dps = 80 local
  - no float(), no mocks
  - algebraic residuals < 1e-14
  - ledger constants unchanged
  - evidence never overstated to [A]
"""

import mpmath as mp

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.formal_source_mapping import (
    symmetric_potential,
    effective_potential,
    effective_potential_derivative,
    effective_potential_second_derivative,
    identify_effective_source_from_gmor,
    identify_effective_source_crosscheck,
    derive_stationary_equation_from_lagrangian,
    derive_lambda3_from_shift,
    formal_mapping_report,
)


def _prec():
    mp.dps = 80


class TestPotentialAlgebra:

    def test_symmetric_potential_formula(self):
        _prec()
        phi = mp.mpf("0.7")
        m_sq = mp.mpf("1.2")
        lam = mp.mpf("0.4")
        expected = mp.mpf("0.5") * m_sq * phi**2 + mp.mpf("0.25") * lam * phi**4
        actual = symmetric_potential(phi, m_sq, lam)
        assert abs(actual - expected) < mp.mpf("1e-14")

    def test_effective_potential_adds_linear_source(self):
        _prec()
        phi = mp.mpf("0.7")
        m_sq = mp.mpf("1.2")
        lam = mp.mpf("0.4")
        h = mp.mpf("0.03")
        expected = symmetric_potential(phi, m_sq, lam) - h * phi
        actual = effective_potential(phi, m_sq, lam, h)
        assert abs(actual - expected) < mp.mpf("1e-14")

    def test_first_derivative_formula(self):
        _prec()
        phi = mp.mpf("0.7")
        m_sq = mp.mpf("1.2")
        lam = mp.mpf("0.4")
        h = mp.mpf("0.03")
        expected = m_sq * phi + lam * phi**3 - h
        actual = effective_potential_derivative(phi, m_sq, lam, h)
        assert abs(actual - expected) < mp.mpf("1e-14")

    def test_second_derivative_formula(self):
        _prec()
        phi = mp.mpf("0.7")
        m_sq = mp.mpf("1.2")
        lam = mp.mpf("0.4")
        expected = m_sq + mp.mpf("3") * lam * phi**2
        actual = effective_potential_second_derivative(phi, m_sq, lam)
        assert abs(actual - expected) < mp.mpf("1e-14")


class TestSourceIdentification:

    def test_gmor_source_has_expected_metadata(self):
        _prec()
        src = identify_effective_source_from_gmor()
        assert src["source_name"] == "h_eff"
        assert src["stratum"] == "III"
        assert src["evidence"] == "[B]"
        assert src["value"] > mp.mpf("0")

    def test_wv_source_has_expected_metadata(self):
        _prec()
        src = identify_effective_source_crosscheck()
        assert src["source_name"] == "h_eff_crosscheck"
        assert src["stratum"] == "III"
        assert src["evidence"] == "[B]"
        assert src["value"] > mp.mpf("0")

    def test_no_direct_A_claim(self):
        _prec()
        src1 = identify_effective_source_from_gmor()
        src2 = identify_effective_source_crosscheck()
        assert src1["evidence"] != "[A]"
        assert src2["evidence"] != "[A]"


class TestForwardClosure:

    def test_stationary_derivation_note_mentions_euler_lagrange(self):
        note = derive_stationary_equation_from_lagrangian()
        assert "Euler-Lagrange" in note
        assert "m^2 phi + lambda_4 phi^3 - h = 0" in note

    def test_lambda3_from_shift_formula(self):
        _prec()
        phi0 = mp.mpf("0.125")
        lam4 = mp.mpf("0.321")
        expected = mp.mpf("3") * lam4 * phi0
        actual = derive_lambda3_from_shift(phi0, lam4)
        assert abs(actual - expected) < mp.mpf("1e-14")

    def test_stationary_equation_has_positive_curvature_example(self):
        _prec()
        phi0 = mp.mpf("0.2")
        m_sq = mp.mpf("1.1")
        lam4 = mp.mpf("0.3")
        curv = effective_potential_second_derivative(phi0, m_sq, lam4)
        assert curv > mp.mpf("0")


class TestConstitutionStep4e:

    def test_rg_constraint_maintained(self):
        _prec()
        _, status = verify_rg_constraint()
        assert status == "PASS"

    def test_ledger_immutable(self):
        _prec()
        before = get_ledger()
        formal_mapping_report()
        after = get_ledger()
        for key in before:
            assert before[key] == after[key], f"Ledger mutated: {key}"

    def test_report_contains_required_sections(self):
        _prec()
        report = formal_mapping_report()
        assert "FORMAL EFFECTIVE POTENTIAL" in report
        assert "SOURCE IDENTIFICATION" in report
        assert "EPISTEMIC NOTE" in report

    def test_report_mentions_limitation(self):
        _prec()
        report = formal_mapping_report()
        assert "does not yet constitute a first-principles bosonization proof" in report
