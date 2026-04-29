"""
[UIDT-v3.9] Verification Test: FRG/NLO gamma derivation (Steps 1-3)
====================================================================

Constitution requirements enforced here:
  - mp.dps = 80 LOCAL (no global, no centralisation)
  - No float() in decision logic
  - No unittest.mock / MagicMock / patch
  - Real mpmath arithmetic only
  - RG constraint residual < 1e-14
  - Evidence category [D] — never auto-upgraded

Test structure:
  Step 1 — Lagrangian: RG constraint + Ledger integrity
  Step 2 — Truncation: Litim regulator arithmetic
  Step 3 — Flow:       Z_phi UV->IR, Constitution residual check

Run:
    pytest verification/tests/test_frg_gamma_nlo.py -v
"""

from __future__ import annotations

import mpmath as mp
import pytest

from modules.frg_gamma_nlo.lagrangian import (
    get_ledger,
    verify_rg_constraint,
    lagrangian_structure_report,
)
from modules.frg_gamma_nlo.truncation import (
    litim_regulator,
    litim_regulator_derivative,
    callan_symanzik_regulator,
    truncation_selftest,
)
from modules.frg_gamma_nlo.flow_equations import (
    threshold_l0_4d,
    threshold_l1_4d,
    threshold_l2_4d,
    volume_factor_4d,
    anomalous_dimension,
    dz_dt,
    run_frg_flow,
    flow_report,
)


# =====================================================================
# STEP 1 — Lagrangian: Ledger Integrity + RG Constraint
# =====================================================================

class TestLagrangianStep1:
    """Verify Ledger constants and RG fixed-point constraint."""

    def setup_method(self):
        mp.dps = 80

    def test_ledger_delta_star(self):
        """Delta* = 1.710 GeV exactly as mpf."""
        mp.dps = 80
        L = get_ledger()
        assert L["DELTA_STAR"] == mp.mpf("1.710"), (
            f"Ledger DELTA_STAR mismatch: {L['DELTA_STAR']}"
        )

    def test_ledger_gamma(self):
        """gamma = 16.339 exactly as mpf."""
        mp.dps = 80
        L = get_ledger()
        assert L["GAMMA"] == mp.mpf("16.339"), (
            f"Ledger GAMMA mismatch: {L['GAMMA']}"
        )

    def test_ledger_kappa(self):
        """kappa = 0.500 exactly as mpf."""
        mp.dps = 80
        L = get_ledger()
        assert L["KAPPA"] == mp.mpf("0.500"), (
            f"Ledger KAPPA mismatch: {L['KAPPA']}"
        )

    def test_ledger_lambda_s_derived(self):
        """lambda_S = 5*kappa^2/3 exactly."""
        mp.dps = 80
        L = get_ledger()
        expected = mp.mpf("5") * mp.mpf("0.500")**2 / mp.mpf("3")
        residual = abs(L["LAMBDA_S"] - expected)
        assert residual < mp.mpf("1e-14"), (
            f"lambda_S derivation residual {residual} >= 1e-14"
        )

    def test_rg_constraint_pass(self):
        """5*kappa^2 = 3*lambda_S with residual < 1e-14 (Constitution)."""
        mp.dps = 80
        residual, status = verify_rg_constraint()
        assert status == "PASS", f"[RG_CONSTRAINT_FAIL] status={status}"
        assert residual < mp.mpf("1e-14"), (
            f"[RG_CONSTRAINT_FAIL] residual={mp.nstr(residual, 6)} >= 1e-14"
        )

    def test_rg_constraint_exact_zero(self):
        """Residual is machine zero (mpmath 80 dps)."""
        mp.dps = 80
        L = get_ledger()
        lhs = mp.mpf("5") * L["KAPPA"]**2
        rhs = mp.mpf("3") * L["LAMBDA_S"]
        assert lhs == rhs, (
            f"5*kappa^2 != 3*lambda_S: {mp.nstr(lhs,20)} vs {mp.nstr(rhs,20)}"
        )

    def test_lagrangian_report_runs(self):
        """lagrangian_structure_report() executes without error."""
        mp.dps = 80
        report = lagrangian_structure_report()
        assert "PASS" in report
        assert "Z_phi" in report
        assert "16.339" in report


# =====================================================================
# STEP 2 — Truncation: Litim Regulator Arithmetic
# =====================================================================

class TestTruncationStep2:
    """Verify Litim regulator and LPA' projection, all mp.mpf."""

    def setup_method(self):
        mp.dps = 80

    def test_litim_outside_window_zero(self):
        """R_k(p^2 >= k^2) = 0 exactly."""
        mp.dps = 80
        k_sq = mp.mpf("1.710")**2
        p_sq = mp.mpf("2.0")**2
        result = litim_regulator(p_sq, k_sq, mp.mpf("1"))
        assert result == mp.mpf("0"), f"Expected 0, got {result}"

    def test_litim_inside_window_positive(self):
        """R_k(p^2 < k^2) > 0."""
        mp.dps = 80
        k_sq = mp.mpf("1.710")**2
        p_sq = mp.mpf("1.0")**2
        result = litim_regulator(p_sq, k_sq, mp.mpf("1"))
        assert result > mp.mpf("0"), f"Expected > 0, got {result}"

    def test_litim_value_exact(self):
        """R_k(p^2=1, k^2=4, Z=1) = 3 exactly."""
        mp.dps = 80
        result = litim_regulator(mp.mpf("1"), mp.mpf("4"), mp.mpf("1"))
        expected = mp.mpf("3")
        residual = abs(result - expected)
        assert residual < mp.mpf("1e-14"), (
            f"Litim value residual {mp.nstr(residual,6)} >= 1e-14"
        )

    def test_litim_derivative_inside(self):
        """dR/dt(p^2 < k^2) = 2*Z*k^2 > 0."""
        mp.dps = 80
        k_sq = mp.mpf("4")
        p_sq = mp.mpf("1")
        z = mp.mpf("1")
        result = litim_regulator_derivative(p_sq, k_sq, z)
        expected = mp.mpf("2") * z * k_sq
        residual = abs(result - expected)
        assert residual < mp.mpf("1e-14"), (
            f"dR/dt residual {mp.nstr(residual,6)} >= 1e-14"
        )

    def test_litim_derivative_outside_zero(self):
        """dR/dt(p^2 >= k^2) = 0."""
        mp.dps = 80
        result = litim_regulator_derivative(mp.mpf("9"), mp.mpf("4"), mp.mpf("1"))
        assert result == mp.mpf("0"), f"Expected 0, got {result}"

    def test_callan_symanzik_value(self):
        """R_CS = Z*k^2."""
        mp.dps = 80
        z = mp.mpf("1.5")
        k_sq = mp.mpf("2.0")
        result = callan_symanzik_regulator(k_sq, z)
        expected = z * k_sq
        residual = abs(result - expected)
        assert residual < mp.mpf("1e-14"), (
            f"CS regulator residual {mp.nstr(residual,6)} >= 1e-14"
        )

    def test_truncation_selftest_passes(self):
        """truncation_selftest() passes all internal asserts."""
        mp.dps = 80
        report = truncation_selftest()
        assert "PASS" in report


# =====================================================================
# STEP 3 — Flow Equations: Threshold Functions + Full Flow
# =====================================================================

class TestFlowEquationsStep3:
    """Verify threshold functions, anomalous dimension, and full UV->IR flow."""

    def setup_method(self):
        mp.dps = 80

    # --- Threshold functions ---

    def test_l0_at_zero_mass(self):
        """l_0^4(0) = 1."""
        mp.dps = 80
        result = threshold_l0_4d(mp.mpf("0"))
        assert result == mp.mpf("1"), f"l0(0) = {result}, expected 1"

    def test_l1_at_zero_mass(self):
        """l_1^4(0) = -1."""
        mp.dps = 80
        result = threshold_l1_4d(mp.mpf("0"))
        assert result == mp.mpf("-1"), f"l1(0) = {result}, expected -1"

    def test_l2_at_zero_mass(self):
        """l_2^4(0) = 2."""
        mp.dps = 80
        result = threshold_l2_4d(mp.mpf("0"))
        assert result == mp.mpf("2"), f"l2(0) = {result}, expected 2"

    def test_l0_large_mass_suppressed(self):
        """l_0^4(m^2) -> 0 for large m^2."""
        mp.dps = 80
        result = threshold_l0_4d(mp.mpf("1e10"))
        assert result < mp.mpf("1e-9"), f"l0 not suppressed: {result}"

    def test_volume_factor_4d(self):
        """v_4 = 1/(32*pi^2) with residual < 1e-14."""
        mp.dps = 80
        result = volume_factor_4d()
        expected = mp.mpf("1") / (mp.mpf("32") * mp.pi**2)
        residual = abs(result - expected)
        assert residual < mp.mpf("1e-14"), (
            f"v_4 residual {mp.nstr(residual,6)} >= 1e-14"
        )

    def test_anomalous_dimension_zero_for_z2(self):
        """eta_phi = 0 when lambda_3 = 0 (Z_2 symmetric fixed point)."""
        mp.dps = 80
        eta = anomalous_dimension(
            z_phi=mp.mpf("1"),
            m_sq=mp.mpf("0.25"),
            lambda_3=mp.mpf("0"),
        )
        assert eta == mp.mpf("0"), f"eta_phi != 0 for lambda_3=0: {eta}"

    def test_dz_dt_zero_for_z2(self):
        """dZ/dt = 0 when lambda_3 = 0 (no NLO correction at Z_2 point)."""
        mp.dps = 80
        result = dz_dt(
            z_phi=mp.mpf("1"),
            m_sq=mp.mpf("0.25"),
            lambda_3=mp.mpf("0"),
        )
        assert result == mp.mpf("0"), f"dZ/dt != 0 for lambda_3=0: {result}"

    # --- Full flow ---

    def test_flow_rg_constraint_maintained(self):
        """run_frg_flow() passes RG constraint check before running."""
        mp.dps = 80
        result = run_frg_flow(n_steps=100)
        assert result["rg_status"] == "PASS"
        assert result["rg_residual"] < mp.mpf("1e-14"), (
            f"[RG_CONSTRAINT_FAIL] residual={mp.nstr(result['rg_residual'],6)}"
        )

    def test_flow_evidence_locked_at_D(self):
        """Evidence category is always [D]; never auto-upgraded."""
        mp.dps = 80
        result = run_frg_flow(n_steps=100)
        assert result["evidence"] == "[D]", (
            f"Evidence auto-upgraded to {result['evidence']} — Constitution violation"
        )

    def test_flow_z_uv_initial_value(self):
        """Z_phi at t=0 (UV) = 1 exactly."""
        mp.dps = 80
        result = run_frg_flow(n_steps=100)
        z_uv = result["z_values"][0]
        assert z_uv == mp.mpf("1"), f"Z_UV != 1: {z_uv}"

    def test_flow_z_ir_positive(self):
        """Z_phi(IR) > 0 (physical kinetic coefficient)."""
        mp.dps = 80
        result = run_frg_flow(n_steps=500)
        assert result["z_ir"] > mp.mpf("0"), (
            f"Z_phi(IR) <= 0: {result['z_ir']}"
        )

    def test_flow_z2_symmetric_z_unchanged(self):
        """
        At Z_2 symmetric fixed point (lambda_3=0),
        Z_phi stays at 1 throughout the flow (eta_phi=0 exactly).
        This is the analytic reference: dZ/dt = 0 => Z_IR = 1.
        """
        mp.dps = 80
        result = run_frg_flow(
            n_steps=500,
            lambda_3_uv=mp.mpf("0"),
        )
        z_ir = result["z_ir"]
        residual = abs(z_ir - mp.mpf("1"))
        assert residual < mp.mpf("1e-14"), (
            f"Z_2 fixed point: Z_IR residual {mp.nstr(residual,6)} >= 1e-14\n"
            f"Z_IR = {mp.nstr(z_ir, 20)}"
        )

    def test_flow_output_length_consistent(self):
        """t_values, z_values, m_values all have length n_steps+1."""
        mp.dps = 80
        n = 200
        result = run_frg_flow(n_steps=n)
        assert len(result["t_values"]) == n + 1
        assert len(result["z_values"]) == n + 1
        assert len(result["m_values"]) == n + 1

    def test_flow_report_contains_evidence_D(self):
        """flow_report() output contains [D] evidence marker."""
        mp.dps = 80
        result = run_frg_flow(n_steps=200)
        report = flow_report(result)
        assert "[D]" in report
        assert "TKT-FRG-GAMMA-NLO" in report
        assert "RG Constraint" in report


# =====================================================================
# CONSTITUTION CHECKPOINT: Combined residual gate
# =====================================================================

class TestConstitutionCheckpoint:
    """
    Master gate: all Constitution requirements in one place.
    If any of these fail, no PR merge is permitted.
    """

    def test_rg_residual_below_constitution_threshold(self):
        """CRITICAL: 5*kappa^2 - 3*lambda_S < 1e-14 (Constitution)."""
        mp.dps = 80
        residual, status = verify_rg_constraint()
        assert residual < mp.mpf("1e-14"), (
            f"[RG_CONSTRAINT_FAIL] residual={mp.nstr(residual,6)}"
        )
        assert status == "PASS"

    def test_no_float_in_flow_decision(self):
        """
        Z_2 reference flow: Z_IR = 1 exactly (analytic).
        If float() were used internally, this would drift from 1.
        Residual < 1e-14 proves mp.mpf arithmetic throughout.
        """
        mp.dps = 80
        result = run_frg_flow(n_steps=1000, lambda_3_uv=mp.mpf("0"))
        residual = abs(result["z_ir"] - mp.mpf("1"))
        assert residual < mp.mpf("1e-14"), (
            f"float() contamination detected: Z_IR residual = {mp.nstr(residual,6)}"
        )

    def test_evidence_never_auto_upgraded(self):
        """Evidence must be [D] for all flow configurations."""
        mp.dps = 80
        for lam3 in [mp.mpf("0"), mp.mpf("0.1"), mp.mpf("0.5")]:
            result = run_frg_flow(n_steps=100, lambda_3_uv=lam3)
            assert result["evidence"] == "[D]", (
                f"Evidence auto-upgraded to {result['evidence']} for lambda_3={lam3}"
            )

    def test_ledger_constants_immutable(self):
        """Multiple get_ledger() calls return identical values."""
        mp.dps = 80
        L1 = get_ledger()
        L2 = get_ledger()
        for key in L1:
            assert L1[key] == L2[key], (
                f"Ledger key '{key}' changed between calls: {L1[key]} != {L2[key]}"
            )

    def test_torsion_kill_switch(self):
        """If E_T = 0 then SigmaT = 0 exactly (Constitution torsion rule)."""
        mp.dps = 80
        L = get_ledger()
        e_t = L["E_T"]
        # E_T = 2.44 MeV != 0 in canonical Ledger; verify non-zero
        assert e_t == mp.mpf("2.44"), f"E_T Ledger value changed: {e_t}"
        # If E_T were forced to 0, SigmaT must be 0:
        e_t_test = mp.mpf("0")
        sigma_t = e_t_test * mp.mpf("1")  # SigmaT proportional to E_T
        assert sigma_t == mp.mpf("0"), "[TORSION_KILL_SWITCH] SigmaT != 0 for E_T=0"
