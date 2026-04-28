"""
[UIDT-v3.9] Verification Tests — Step 4: Fixed-Point Potential + Pipeline
==========================================================================

Tests 26-51 of the UIDT FRG/NLO verification suite.

CONSTITUTION RULES ENFORCED:
  - All numerical operations use real mpmath (mp.dps=80), no float()
  - No unittest.mock, MagicMock, or patch
  - Residual < 1e-14 for [A] claims
  - Evidence '[D]' hardcoded; never auto-upgraded
  - Ledger constants immutable
  - RG constraint checked before any flow

RUN:
  pytest verification/tests/test_fixedpoint_potential.py -v
"""

import mpmath as mp
import pytest

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.fixedpoint_potential import (
    compute_phi_vev,
    fixed_point_mass,
    fixed_point_derivative_relation,
    derive_uv_couplings,
    lpa_fixedpoint_rhs,
    verify_fixedpoint_consistency,
    fixedpoint_report,
)
from modules.frg_gamma_nlo.gamma_pipeline import run_gamma_pipeline, pipeline_report
from modules.frg_gamma_nlo.flow_equations import volume_factor_4d


# =====================================================================
# Precision helper
# =====================================================================

def _prec():
    mp.dps = 80


# =====================================================================
# Class A: VEV identification (Stratum III, [D])
# =====================================================================

class TestVEVIdentification:
    """Tests for phi* = V_vac / Delta*."""

    def test_phi_star_is_mpf(self):
        _prec()
        phi = compute_phi_vev()
        assert isinstance(phi, mp.mpf)

    def test_phi_star_positive(self):
        _prec()
        phi = compute_phi_vev()
        assert phi > mp.mpf("0")

    def test_phi_star_less_than_one(self):
        """Dimensionless phi* << 1 (V_vac << Delta*)."""
        _prec()
        phi = compute_phi_vev()
        assert phi < mp.mpf("1")

    def test_phi_star_value_exact(self):
        """
        phi* = 47.7 / 1710 = 0.027894736842...
        Residual < 1e-14 (mpf arithmetic).
        """
        _prec()
        phi = compute_phi_vev()
        expected = mp.mpf("47.7") / mp.mpf("1710")
        residual = abs(phi - expected)
        assert residual < mp.mpf("1e-14"), f"phi* residual = {residual}"

    def test_phi_star_not_zero(self):
        """phi* != 0 confirms Z_2 breaking."""
        _prec()
        phi = compute_phi_vev()
        assert phi != mp.mpf("0")


# =====================================================================
# Class B: Fixed-point mass (UV couplings, [A])
# =====================================================================

class TestFixedPointMass:

    def test_m_sq_equals_kappa_squared(self):
        _prec()
        L = get_ledger()
        phi_star = compute_phi_vev()
        m_sq = fixed_point_mass(phi_star, L["KAPPA"])
        expected = L["KAPPA"]**2
        residual = abs(m_sq - expected)
        assert residual < mp.mpf("1e-14"), f"m^2 residual = {residual}"

    def test_m_sq_is_mpf(self):
        _prec()
        L = get_ledger()
        phi_star = compute_phi_vev()
        m_sq = fixed_point_mass(phi_star, L["KAPPA"])
        assert isinstance(m_sq, mp.mpf)

    def test_m_sq_positive(self):
        _prec()
        L = get_ledger()
        phi_star = compute_phi_vev()
        m_sq = fixed_point_mass(phi_star, L["KAPPA"])
        assert m_sq > mp.mpf("0")

    def test_m_sq_from_kappa_half(self):
        """kappa = 0.500 -> m^2 = 0.250."""
        _prec()
        L = get_ledger()
        phi_star = compute_phi_vev()
        m_sq = fixed_point_mass(phi_star, L["KAPPA"])
        expected = mp.mpf("0.25")
        residual = abs(m_sq - expected)
        assert residual < mp.mpf("1e-14"), f"m^2 = {m_sq}, expected 0.25"


# =====================================================================
# Class C: lambda_3 derivation ([D])
# =====================================================================

class TestLambda3Derivation:

    def test_lambda3_is_mpf(self):
        _prec()
        L = get_ledger()
        phi_star = compute_phi_vev()
        m_sq = fixed_point_mass(phi_star, L["KAPPA"])
        lam3 = fixed_point_derivative_relation(phi_star, m_sq, L["LAMBDA_S"])
        assert isinstance(lam3, mp.mpf)

    def test_lambda3_positive(self):
        """lambda_3 > 0 for phi* > 0 and m^2 > 0."""
        _prec()
        L = get_ledger()
        phi_star = compute_phi_vev()
        m_sq = fixed_point_mass(phi_star, L["KAPPA"])
        lam3 = fixed_point_derivative_relation(phi_star, m_sq, L["LAMBDA_S"])
        assert lam3 > mp.mpf("0")

    def test_lambda3_not_zero(self):
        """Non-zero lambda_3 is the source of Z_2 breaking in the flow."""
        _prec()
        L = get_ledger()
        phi_star = compute_phi_vev()
        m_sq = fixed_point_mass(phi_star, L["KAPPA"])
        lam3 = fixed_point_derivative_relation(phi_star, m_sq, L["LAMBDA_S"])
        assert lam3 != mp.mpf("0")

    def test_lambda3_formula_exact(self):
        """
        Verify formula:
          lambda_3 = phi* * m^2 * (1+m^2)^2 / (3 * v_4)
        independently.
        """
        _prec()
        L = get_ledger()
        phi_star = compute_phi_vev()
        m_sq = L["KAPPA"]**2
        v4 = volume_factor_4d()
        expected = phi_star * m_sq * (mp.mpf("1") + m_sq)**2 / (mp.mpf("3") * v4)
        lam3 = fixed_point_derivative_relation(phi_star, m_sq, L["LAMBDA_S"])
        residual = abs(lam3 - expected)
        assert residual < mp.mpf("1e-14"), f"lambda_3 formula residual = {residual}"

    def test_lambda3_scales_linearly_with_phi_star(self):
        """lambda_3 ~ phi*: doubling phi* doubles lambda_3 (at leading order)."""
        _prec()
        L = get_ledger()
        m_sq = L["KAPPA"]**2
        phi1 = mp.mpf("0.01")
        phi2 = mp.mpf("0.02")
        l1 = fixed_point_derivative_relation(phi1, m_sq, L["LAMBDA_S"])
        l2 = fixed_point_derivative_relation(phi2, m_sq, L["LAMBDA_S"])
        ratio = l2 / l1
        assert abs(ratio - mp.mpf("2")) < mp.mpf("1e-14"), f"ratio = {ratio}"

    def test_lambda3_at_zero_phi_is_zero(self):
        """Z_2 symmetric case: phi* = 0 => lambda_3 = 0."""
        _prec()
        L = get_ledger()
        m_sq = L["KAPPA"]**2
        lam3 = fixed_point_derivative_relation(mp.mpf("0"), m_sq, L["LAMBDA_S"])
        assert lam3 == mp.mpf("0")


# =====================================================================
# Class D: Full UV couplings dict
# =====================================================================

class TestUVCouplingsDict:

    def test_derive_uv_couplings_runs(self):
        _prec()
        couplings = derive_uv_couplings()
        assert isinstance(couplings, dict)

    def test_rg_status_pass(self):
        _prec()
        couplings = derive_uv_couplings()
        assert couplings["rg_status"] == "PASS"

    def test_evidence_locked_at_D(self):
        _prec()
        couplings = derive_uv_couplings()
        assert couplings["evidence"] == "[D]"

    def test_rg_residual_below_threshold(self):
        _prec()
        couplings = derive_uv_couplings()
        assert abs(couplings["rg_residual"]) < mp.mpf("1e-14")

    def test_lambda4_equals_lambda_s(self):
        _prec()
        L = get_ledger()
        couplings = derive_uv_couplings()
        residual = abs(couplings["lambda_4"] - L["LAMBDA_S"])
        assert residual < mp.mpf("1e-14")

    def test_m_sq_equals_kappa_sq(self):
        _prec()
        L = get_ledger()
        couplings = derive_uv_couplings()
        residual = abs(couplings["m_sq_uv"] - L["KAPPA"]**2)
        assert residual < mp.mpf("1e-14")


# =====================================================================
# Class E: LPA fixed-point equation consistency
# =====================================================================

class TestLPAFixedPointConsistency:

    def test_consistency_check_runs(self):
        _prec()
        couplings = derive_uv_couplings()
        rel_res, status = verify_fixedpoint_consistency(couplings)
        assert isinstance(rel_res, mp.mpf)
        assert status in ("CONSISTENT", "LARGE_RESIDUAL")

    def test_consistency_relative_residual_positive(self):
        _prec()
        couplings = derive_uv_couplings()
        rel_res, _ = verify_fixedpoint_consistency(couplings)
        assert rel_res >= mp.mpf("0")

    def test_lpa_rhs_at_zero_field(self):
        """
        At phi=0, u_val=0, u_pp=m^2:
          F = v_4 / (1 + m^2)  (since U*'=0, first two terms vanish)
        """
        _prec()
        L = get_ledger()
        m_sq = L["KAPPA"]**2
        v4 = volume_factor_4d()
        f_val = lpa_fixedpoint_rhs(mp.mpf("0"), mp.mpf("0"), m_sq)
        expected = v4 / (mp.mpf("1") + m_sq)
        residual = abs(f_val - expected)
        assert residual < mp.mpf("1e-14"), f"LPA RHS residual = {residual}"


# =====================================================================
# Class F: Full gamma pipeline
# =====================================================================

class TestGammaPipeline:

    def test_pipeline_runs_with_100_steps(self):
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        assert isinstance(result, dict)

    def test_pipeline_rg_status_pass(self):
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        assert result["rg_status"] == "PASS"

    def test_pipeline_evidence_locked_at_D(self):
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        assert result["evidence"] == "[D]"

    def test_pipeline_z_ir_is_mpf(self):
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        assert isinstance(result["z_ir"], mp.mpf)

    def test_pipeline_z_ir_positive(self):
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        assert result["z_ir"] > mp.mpf("0")

    def test_pipeline_lambda3_nonzero(self):
        """Non-zero lambda_3 is the Z_2-breaking source; must be non-zero."""
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        assert result["lambda_3"] != mp.mpf("0")

    def test_pipeline_deviation_is_mpf(self):
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        assert isinstance(result["deviation"], mp.mpf)

    def test_pipeline_report_runs(self):
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        report = pipeline_report(result)
        assert "gamma" in report.lower() or "GAMMA" in report
        assert "[D]" in report

    def test_pipeline_gamma_target_matches_ledger(self):
        _prec()
        L = get_ledger()
        result = run_gamma_pipeline(n_steps=100)
        residual = abs(result["gamma_target"] - L["GAMMA"])
        assert residual < mp.mpf("1e-14")

    def test_pipeline_no_float_contamination(self):
        """
        Constitution test: all pipeline outputs are mp.mpf instances.
        Confirms no float() was silently introduced.
        """
        _prec()
        result = run_gamma_pipeline(n_steps=100)
        for key in ["phi_star", "lambda_3", "z_ir", "gamma_target", "deviation", "delta_gamma"]:
            assert isinstance(result[key], mp.mpf), (
                f"Float contamination detected in key '{key}': "
                f"type={type(result[key])}"
            )


# =====================================================================
# Class G: Constitution checkpoint (Step 4)
# =====================================================================

class TestConstitutionCheckpointStep4:

    def test_ledger_immutable_across_pipeline(self):
        """Ledger returns identical values before and after pipeline run."""
        _prec()
        L_before = get_ledger()
        _ = run_gamma_pipeline(n_steps=50)
        L_after = get_ledger()
        for key in L_before:
            assert L_before[key] == L_after[key], (
                f"Ledger mutation detected for key '{key}'"
            )

    def test_rg_residual_maintained_through_pipeline(self):
        _prec()
        result = run_gamma_pipeline(n_steps=50)
        rg_res = result["uv_couplings"]["rg_residual"]
        assert abs(rg_res) < mp.mpf("1e-14")

    def test_evidence_never_upgraded_in_pipeline(self):
        """Evidence must stay '[D]' even when within_delta is True."""
        _prec()
        result = run_gamma_pipeline(n_steps=50)
        assert result["evidence"] == "[D]"
        assert result["uv_couplings"]["evidence"] == "[D]"
        assert result["flow_result"]["evidence"] == "[D]"

    def test_torsion_kill_switch_in_pipeline(self):
        """
        E_T = 2.44 MeV in Ledger.
        Verify ledger E_T != 0, so kill switch is NOT triggered.
        (Kill switch: E_T = 0 => Sigma_T = 0 exactly.)
        """
        _prec()
        L = get_ledger()
        assert L["E_T"] != mp.mpf("0"), "E_T should be 2.44 MeV per Ledger"

    def test_phi_star_consistent_with_ledger_ratio(self):
        """
        phi* = V_vac / Delta* must match Ledger [A] values.
        """
        _prec()
        L = get_ledger()
        phi_expected = L["V_VAC"] / (L["DELTA_STAR"] * mp.mpf("1000"))
        phi_actual = compute_phi_vev()
        residual = abs(phi_actual - phi_expected)
        assert residual < mp.mpf("1e-14")
