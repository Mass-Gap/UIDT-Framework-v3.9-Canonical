"""
[UIDT-v3.9] Verification Tests — Step 4c: lambda_3 from explicit source h*phi
==============================================================================

Constitution rules:
  - All mp.mpf, mp.dps=80 local
  - No float(), no mock
  - phi_residual < 1e-14
  - RG constraint maintained
  - Evidence [D]/[B] never auto-upgraded

RUN:
  pytest verification/tests/test_symmetry_breaking.py -v
"""

import mpmath as mp
import pytest

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.symmetry_breaking import (
    compute_explicit_breaking_source,
    compute_classical_vacuum,
    compute_lambda3_from_vacuum,
    derive_lambda3_from_source,
    consistency_check_against_legacy,
    symmetry_breaking_report,
)


def _prec():
    mp.dps = 80


# =====================================================================
# Class A: Breaking source h
# =====================================================================

class TestBreakingSource:

    def test_h_is_mpf(self):
        _prec()
        h = compute_explicit_breaking_source()
        assert isinstance(h, mp.mpf)

    def test_h_positive(self):
        _prec()
        h = compute_explicit_breaking_source()
        assert h > mp.mpf("0")

    def test_h_formula_exact(self):
        """
        h = m^2 * V_vac/(Delta*[MeV])
        Verify independently.
        """
        _prec()
        L = get_ledger()
        expected = L["KAPPA"]**2 * L["V_VAC"] / (L["DELTA_STAR"] * mp.mpf("1000"))
        h = compute_explicit_breaking_source()
        residual = abs(h - expected)
        assert residual < mp.mpf("1e-14"), f"h residual = {residual}"

    def test_h_much_less_than_m_sq(self):
        """h << m^2 ensures perturbative regime phi_0 ~ h/m^2 is valid."""
        _prec()
        L = get_ledger()
        h = compute_explicit_breaking_source()
        m_sq = L["KAPPA"]**2
        assert h < m_sq


# =====================================================================
# Class B: Classical vacuum phi_0
# =====================================================================

class TestClassicalVacuum:

    def test_phi_0_is_mpf(self):
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        assert isinstance(vac["phi_0"], mp.mpf)

    def test_phi_0_positive(self):
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        assert vac["phi_0"] > mp.mpf("0")

    def test_phi_0_stationary_residual_below_constitution_threshold(self):
        """Core Constitution check: |dU/dphi| < 1e-14 at phi_0."""
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        assert vac["residual"] < mp.mpf("1e-14"), (
            f"Stationary residual {vac['residual']} >= 1e-14"
        )

    def test_phi_0_stable(self):
        """d^2U/dphi^2 > 0 at phi_0."""
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        assert vac["stable"] is True

    def test_phi_0_evidence_locked(self):
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        assert vac["evidence"] == "[D]"

    def test_phi_0_leading_order_agreement(self):
        """
        At leading order phi_0 = h/m^2.
        Newton solution should agree to < 1e-6 relative.
        """
        _prec()
        L = get_ledger()
        h = compute_explicit_breaking_source()
        phi_lo = h / L["KAPPA"]**2
        vac = compute_classical_vacuum(h)
        rel = abs(vac["phi_0"] - phi_lo) / abs(phi_lo)
        assert rel < mp.mpf("1e-6")


# =====================================================================
# Class C: lambda_3 derivation
# =====================================================================

class TestLambda3FromVacuum:

    def test_lambda3_is_mpf(self):
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        l3 = compute_lambda3_from_vacuum(vac["phi_0"])
        assert isinstance(l3["lambda_3"], mp.mpf)

    def test_lambda3_positive(self):
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        l3 = compute_lambda3_from_vacuum(vac["phi_0"])
        assert l3["lambda_3"] > mp.mpf("0")

    def test_lambda3_not_zero(self):
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        l3 = compute_lambda3_from_vacuum(vac["phi_0"])
        assert l3["lambda_3"] != mp.mpf("0")

    def test_lambda3_formula_exact(self):
        """
        lambda_3 = 3 * lambda_S * phi_0
        Verify independently.
        """
        _prec()
        L = get_ledger()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        expected = mp.mpf("3") * L["LAMBDA_S"] * vac["phi_0"]
        l3 = compute_lambda3_from_vacuum(vac["phi_0"])
        residual = abs(l3["lambda_3"] - expected)
        assert residual < mp.mpf("1e-14"), f"lambda_3 formula residual = {residual}"

    def test_lambda3_evidence_locked_D(self):
        _prec()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        l3 = compute_lambda3_from_vacuum(vac["phi_0"])
        assert l3["evidence"] == "[D]"

    def test_m_eff_sq_greater_than_m_sq(self):
        """Effective mass after shift should be larger than bare m^2."""
        _prec()
        L = get_ledger()
        h = compute_explicit_breaking_source()
        vac = compute_classical_vacuum(h)
        l3 = compute_lambda3_from_vacuum(vac["phi_0"])
        assert l3["m_eff_sq"] > L["KAPPA"]**2


# =====================================================================
# Class D: Full pipeline
# =====================================================================

class TestFullPipelineStep4c:

    def test_pipeline_runs(self):
        _prec()
        result = derive_lambda3_from_source()
        assert isinstance(result, dict)

    def test_pipeline_rg_pass(self):
        _prec()
        result = derive_lambda3_from_source()
        assert result["rg_status"] == "PASS"

    def test_pipeline_rg_residual_below_threshold(self):
        _prec()
        result = derive_lambda3_from_source()
        assert abs(result["rg_residual"]) < mp.mpf("1e-14")

    def test_pipeline_phi_residual_below_threshold(self):
        _prec()
        result = derive_lambda3_from_source()
        assert result["phi_residual"] < mp.mpf("1e-14"), (
            f"phi_0 stationary residual = {result['phi_residual']}"
        )

    def test_pipeline_evidence_h_is_B(self):
        _prec()
        result = derive_lambda3_from_source()
        assert result["evidence_h"] == "[B]"

    def test_pipeline_evidence_locked_D(self):
        _prec()
        result = derive_lambda3_from_source()
        assert result["evidence"] == "[D]"

    def test_pipeline_stable_vacuum(self):
        _prec()
        result = derive_lambda3_from_source()
        assert result["stable"] is True

    def test_pipeline_lambda3_positive_and_nonzero(self):
        _prec()
        result = derive_lambda3_from_source()
        assert result["lambda_3"] > mp.mpf("0")
        assert result["lambda_3"] != mp.mpf("0")


# =====================================================================
# Class E: Consistency with legacy mapping
# =====================================================================

class TestConsistencyWithLegacy:

    def test_check_runs(self):
        _prec()
        c = consistency_check_against_legacy()
        assert isinstance(c, dict)

    def test_phi_newton_vs_legacy_relative_diff_small(self):
        """
        phi_0 (Newton) agrees with legacy phi* = V_vac/(Delta*[MeV])
        to within the leading quartic correction ~ O(lambda_4*phi*^2/m^2) ~ 1e-4.
        """
        _prec()
        c = consistency_check_against_legacy()
        assert c["rel_diff"] < mp.mpf("1e-4"), (
            f"Relative diff = {c['rel_diff']} exceeds 1e-4"
        )

    def test_correction_order_is_small(self):
        _prec()
        c = consistency_check_against_legacy()
        assert c["correction_order"] < mp.mpf("1e-3")

    def test_phi_newton_is_mpf(self):
        _prec()
        c = consistency_check_against_legacy()
        assert isinstance(c["phi_newton"], mp.mpf)


# =====================================================================
# Class F: Report and Constitution (Step 4c)
# =====================================================================

class TestConstitutionStep4c:

    def test_report_runs(self):
        _prec()
        report = symmetry_breaking_report()
        assert "lambda_3" in report
        assert "[D]" in report
        assert "[B]" in report

    def test_ledger_immutable_after_pipeline(self):
        _prec()
        L_before = get_ledger()
        _ = derive_lambda3_from_source()
        L_after = get_ledger()
        for k in L_before:
            assert L_before[k] == L_after[k], f"Ledger mutated: {k}"

    def test_no_float_contamination_in_pipeline(self):
        """
        All numerical pipeline outputs must be mp.mpf.
        """
        _prec()
        result = derive_lambda3_from_source()
        for key in ["h", "phi_0", "phi_residual", "lambda_3", "m_eff_sq", "rg_residual"]:
            assert isinstance(result[key], mp.mpf), (
                f"Float contamination in '{key}': type={type(result[key])}"
            )

    def test_rg_constraint_maintained_throughout(self):
        _prec()
        _, status = verify_rg_constraint()
        assert status == "PASS"
