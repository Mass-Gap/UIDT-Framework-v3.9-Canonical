"""
[UIDT-v3.9] Verification Tests — Step 4d: Lattice QCD anchor for h
====================================================================

Constitution rules:
  - All mp.mpf, mp.dps=80 local
  - No float(), no mock
  - Residual < 1e-14 for [A] arithmetic
  - Evidence [D]/[B] never auto-upgraded
  - Lattice constants [A] must not be modified

RUN:
  pytest verification/tests/test_lattice_anchor.py -v
"""

import mpmath as mp
import pytest

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.lattice_anchor import (
    get_lattice_constants,
    compute_h_gmor,
    compute_h_wv,
    agreement_check,
    validate_uidt_h_against_lattice,
    assess_h_evidence,
    lattice_anchor_report,
)


def _prec():
    mp.dps = 80


# =====================================================================
# A: Lattice constants
# =====================================================================

class TestLatticeConstants:

    def test_all_values_mpf(self):
        _prec()
        LC = get_lattice_constants()
        for key in ["cond_cbrt", "condensate", "chi_fourth", "chi_top",
                    "f_pi", "m_q"]:
            assert isinstance(LC[key], mp.mpf), f"{key} not mpf"

    def test_condensate_cube(self):
        """condensate = cond_cbrt^3 exactly."""
        _prec()
        LC = get_lattice_constants()
        expected = LC["cond_cbrt"]**3
        residual = abs(LC["condensate"] - expected)
        assert residual < mp.mpf("1e-14")

    def test_chi_top_fourth_power(self):
        """chi_top = chi_fourth^4 exactly."""
        _prec()
        LC = get_lattice_constants()
        expected = LC["chi_fourth"]**4
        residual = abs(LC["chi_top"] - expected)
        assert residual < mp.mpf("1e-14")

    def test_condensate_cbrt_value(self):
        """FLAG 2023: |<psi-bar psi>|^{1/3} = 272 MeV."""
        _prec()
        LC = get_lattice_constants()
        assert abs(LC["cond_cbrt"] - mp.mpf("272")) < mp.mpf("1e-14")

    def test_chi_fourth_value(self):
        """Borsanyi 2016: chi_top^{1/4} = 75.5 MeV."""
        _prec()
        LC = get_lattice_constants()
        assert abs(LC["chi_fourth"] - mp.mpf("75.5")) < mp.mpf("1e-14")

    def test_f_pi_value(self):
        """PDG 2024: f_pi = 92.1 MeV."""
        _prec()
        LC = get_lattice_constants()
        assert abs(LC["f_pi"] - mp.mpf("92.1")) < mp.mpf("1e-14")

    def test_evidence_is_A(self):
        _prec()
        LC = get_lattice_constants()
        assert LC["evidence"] == "[A]"

    def test_sources_list_nonempty(self):
        _prec()
        LC = get_lattice_constants()
        assert len(LC["sources"]) >= 2


# =====================================================================
# B: GMOR route
# =====================================================================

class TestHGMOR:

    def test_h_gmor_is_mpf(self):
        _prec()
        r = compute_h_gmor()
        assert isinstance(r["h_dimless"], mp.mpf)

    def test_h_gmor_positive(self):
        _prec()
        r = compute_h_gmor()
        assert r["h_dimless"] > mp.mpf("0")

    def test_sigma_gmor_positive(self):
        _prec()
        r = compute_h_gmor()
        assert r["sigma_h_dimless"] > mp.mpf("0")

    def test_h_gmor_formula_exact(self):
        """
        h_GMOR = m_q * condensate / f_pi^2 / Delta*^2
        Verify independently.
        """
        _prec()
        LC = get_lattice_constants()
        L  = get_ledger()
        delta_mev = L["DELTA_STAR"] * mp.mpf("1000")
        expected  = LC["m_q"] * LC["condensate"] / LC["f_pi"]**2 / delta_mev**2
        r = compute_h_gmor()
        residual = abs(r["h_dimless"] - expected)
        assert residual < mp.mpf("1e-14")

    def test_evidence_lattice_is_A(self):
        _prec()
        r = compute_h_gmor()
        assert r["evidence_lattice"] == "[A]"

    def test_evidence_h_is_B(self):
        _prec()
        r = compute_h_gmor()
        assert r["evidence_h"] == "[B]"


# =====================================================================
# C: Witten-Veneziano route
# =====================================================================

class TestHWV:

    def test_h_wv_is_mpf(self):
        _prec()
        r = compute_h_wv()
        assert isinstance(r["h_wv"], mp.mpf)

    def test_h_wv_positive(self):
        _prec()
        r = compute_h_wv()
        assert r["h_wv"] > mp.mpf("0")

    def test_h_wv_formula_exact(self):
        """
        h_WV = chi_fourth^2 / Delta*^2
        """
        _prec()
        LC = get_lattice_constants()
        L  = get_ledger()
        delta_mev = L["DELTA_STAR"] * mp.mpf("1000")
        expected  = LC["chi_fourth"]**2 / delta_mev**2
        r = compute_h_wv()
        residual = abs(r["h_wv"] - expected)
        assert residual < mp.mpf("1e-14")

    def test_sigma_wv_positive(self):
        _prec()
        r = compute_h_wv()
        assert r["sigma_h_wv"] > mp.mpf("0")

    def test_evidence_lattice_is_A(self):
        _prec()
        r = compute_h_wv()
        assert r["evidence_lattice"] == "[A]"


# =====================================================================
# D: Agreement check
# =====================================================================

class TestAgreementCheck:

    def test_runs(self):
        _prec()
        gmor = compute_h_gmor()
        wv   = compute_h_wv()
        agr  = agreement_check(gmor, wv)
        assert "status" in agr

    def test_status_is_string(self):
        _prec()
        gmor = compute_h_gmor()
        wv   = compute_h_wv()
        agr  = agreement_check(gmor, wv)
        assert isinstance(agr["status"], str)

    def test_relative_diff_positive(self):
        _prec()
        gmor = compute_h_gmor()
        wv   = compute_h_wv()
        agr  = agreement_check(gmor, wv)
        assert agr["relative_diff"] >= mp.mpf("0")

    def test_status_valid_value(self):
        _prec()
        gmor = compute_h_gmor()
        wv   = compute_h_wv()
        agr  = agreement_check(gmor, wv)
        assert agr["status"] in ("CONSISTENT", "[TENSION_ALERT]")


# =====================================================================
# E: UIDT validation against lattice band
# =====================================================================

class TestUIDTValidation:

    def test_runs(self):
        _prec()
        val = validate_uidt_h_against_lattice()
        assert isinstance(val, dict)

    def test_h_uidt_is_mpf(self):
        _prec()
        val = validate_uidt_h_against_lattice()
        assert isinstance(val["h_uidt"], mp.mpf)

    def test_n_sigma_is_mpf(self):
        _prec()
        val = validate_uidt_h_against_lattice()
        assert isinstance(val["n_sigma"], mp.mpf)

    def test_within_3sigma_is_bool(self):
        _prec()
        val = validate_uidt_h_against_lattice()
        assert isinstance(val["within_3sigma"], bool)

    def test_status_valid(self):
        _prec()
        val = validate_uidt_h_against_lattice()
        assert val["status"] in ("PASS", "[TENSION_ALERT]")

    def test_no_float_contamination(self):
        _prec()
        val = validate_uidt_h_against_lattice()
        for key in ["h_uidt", "h_gmor", "sigma_gmor", "abs_diff", "n_sigma"]:
            assert isinstance(val[key], mp.mpf), (
                f"Float contamination: {key} type={type(val[key])}"
            )


# =====================================================================
# F: Evidence assessment
# =====================================================================

class TestEvidenceAssessment:

    def test_runs(self):
        _prec()
        gmor = compute_h_gmor()
        wv   = compute_h_wv()
        agr  = agreement_check(gmor, wv)
        val  = validate_uidt_h_against_lattice()
        evid = assess_h_evidence(val, agr)
        assert isinstance(evid, str)

    def test_never_returns_A_directly(self):
        """Evidence auto-upgrade to [A] is locked."""
        _prec()
        gmor = compute_h_gmor()
        wv   = compute_h_wv()
        agr  = agreement_check(gmor, wv)
        val  = validate_uidt_h_against_lattice()
        evid = assess_h_evidence(val, agr)
        # Must not claim [A] without the PI-sign-off note
        assert "Evidence remains [B]" in evid or "[TENSION_ALERT]" in evid or "[B]" in evid


# =====================================================================
# G: Constitution checkpoint
# =====================================================================

class TestConstitutionStep4d:

    def test_rg_constraint_maintained(self):
        _prec()
        _, status = verify_rg_constraint()
        assert status == "PASS"

    def test_ledger_immutable(self):
        _prec()
        L_before = get_ledger()
        lattice_anchor_report()
        L_after = get_ledger()
        for k in L_before:
            assert L_before[k] == L_after[k], f"Ledger mutated: {k}"

    def test_report_contains_sources(self):
        _prec()
        report = lattice_anchor_report()
        assert "FLAG" in report
        assert "Borsanyi" in report

    def test_report_contains_tension_or_consistent(self):
        _prec()
        report = lattice_anchor_report()
        assert "CONSISTENT" in report or "TENSION_ALERT" in report
