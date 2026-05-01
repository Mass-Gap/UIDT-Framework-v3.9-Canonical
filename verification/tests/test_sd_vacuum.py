"""
test_sd_vacuum.py  —  UIDT v3.9 Canonical
==========================================
Pytest suite for sd_vacuum_check.py

Constitution compliance
-----------------------
  - Real mpmath instances — zero mocks
  - mp.dps = 80 declared locally
  - abs(expected - actual) < 1e-14 for all residuals
  - RG constraint 5kappa^2 = 3*lambda_S verified as gate
  - No float(), no round(), no numpy scalar arithmetic

Run
---
  pytest verification/tests/test_sd_vacuum.py -v

DOI: 10.5281/zenodo.17835200
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import mpmath as mp
import pytest

from sd_vacuum_check import (
    compute_b0_full,
    verify_rg_constraint,
    sd_vacuum_scan,
    compute_cs_dimensionless,
    bmw_frg_scaffold_info,
)


# ---------------------------------------------------------------------------
# Gate test — must pass before any physics test is meaningful
# ---------------------------------------------------------------------------

class TestRGConstraintGate:
    """5kappa^2 = 3*lambda_S — Evidence A gate."""

    def test_rg_constraint_passes(self):
        mp.dps = 80
        result = verify_rg_constraint()
        assert result["passed"], (
            f"[RG_CONSTRAINT_FAIL]  residual={mp.nstr(result['residual'], 10)}"
        )

    def test_rg_lhs_value(self):
        mp.dps = 80
        result = verify_rg_constraint()
        expected = mp.mpf("5") * (mp.mpf("0.500") ** 2)
        assert abs(result["LHS"] - expected) < mp.mpf("1e-14")

    def test_rg_rhs_value(self):
        mp.dps = 80
        result = verify_rg_constraint()
        expected = mp.mpf("3") * mp.mpf("5") / mp.mpf("12")
        assert abs(result["RHS"] - expected) < mp.mpf("1e-14")

    def test_flag_is_ok(self):
        result = verify_rg_constraint()
        assert result["flag"] == "OK"


# ---------------------------------------------------------------------------
# Module I — b0
# ---------------------------------------------------------------------------

class TestB0GhostCorrected:
    """One-loop b0 with Faddeev-Popov ghosts included — Evidence A."""

    def test_b0_su3_pure_ym(self):
        """b0 = 33/(48*pi^2) for SU(3), Nf=0."""
        mp.dps = 80
        result = compute_b0_full(Nc_str="3", Nf_str="0")
        expected = mp.mpf("33") / (mp.mpf("48") * mp.pi ** 2)
        assert abs(result["b0"] - expected) < mp.mpf("1e-14"), (
            f"b0 mismatch: got {mp.nstr(result['b0'], 20)}, "
            f"expected {mp.nstr(expected, 20)}"
        )

    def test_b0_residual_below_threshold(self):
        mp.dps = 80
        result = compute_b0_full()
        assert result["residual"] < mp.mpf("1e-14"), (
            f"residual too large: {mp.nstr(result['residual'], 10)}"
        )

    def test_b0_passed_flag(self):
        result = compute_b0_full()
        assert result["passed"]

    def test_b0_positive(self):
        """Positive b0 means asymptotic freedom in pure YM."""
        mp.dps = 80
        result = compute_b0_full()
        assert result["b0"] > mp.mpf("0")

    def test_b0_nf6(self):
        """QCD with 6 flavours: b0 = (33-12)/(48*pi^2) = 21/(48*pi^2)."""
        mp.dps = 80
        result = compute_b0_full(Nc_str="3", Nf_str="6")
        expected = mp.mpf("21") / (mp.mpf("48") * mp.pi ** 2)
        assert abs(result["b0"] - expected) < mp.mpf("1e-14")

    def test_b0_nf_above_asymptotic_freedom_threshold(self):
        """For SU(3) Nf>=17: 11*3-2*17=33-34=-1 < 0 => no AF."""
        mp.dps = 80
        result = compute_b0_full(Nc_str="3", Nf_str="17")
        assert result["b0"] < mp.mpf("0")


# ---------------------------------------------------------------------------
# Module II — c_S extraction
# ---------------------------------------------------------------------------

class TestCSDimensionless:
    """Dimensionless scalar damping parameter — Evidence B."""

    def test_cs_uv_limit_equals_kappa_over_2(self):
        mp.dps = 80
        result = compute_cs_dimensionless()
        expected = mp.mpf("0.500") / mp.mpf("2")
        assert abs(result["c_S_UV_limit"] - expected) < mp.mpf("1e-14")

    def test_cs_in_range_zero_to_kappa_over_2(self):
        mp.dps = 80
        result = compute_cs_dimensionless()
        assert mp.mpf("0") < result["c_S"] <= result["c_S_UV_limit"]

    def test_cs_less_than_uv_limit(self):
        """Full c_S < UV limit because m_S^2/Delta^2 > 0."""
        mp.dps = 80
        result = compute_cs_dimensionless()
        assert result["c_S"] < result["c_S_UV_limit"]

    def test_b0_minus_cs_is_negative(self):
        """c_S > b0 => 1-loop AF is broken at k~Delta*. Expected physics."""
        mp.dps = 80
        result = compute_cs_dimensionless()
        assert result["b0_minus_cs"] < mp.mpf("0")
        assert not result["asymptotic_freedom_preserved"]

    def test_ms2_equals_2_lambda_v2(self):
        mp.dps = 80
        result = compute_cs_dimensionless()
        expected = mp.mpf("2") * (mp.mpf("5") / mp.mpf("12")) * mp.mpf("0.0477") ** 2
        assert abs(result["m_S2_GeV2"] - expected) < mp.mpf("1e-14")

    def test_rg_constraint_residual(self):
        mp.dps = 80
        result = compute_cs_dimensionless()
        assert result["passed_rg"], (
            f"RG constraint failed inside cs computation: "
            f"residual={mp.nstr(result['residual_rg_constraint'], 10)}"
        )


# ---------------------------------------------------------------------------
# Module III — SD vacuum scan
# ---------------------------------------------------------------------------

class TestSDVacuumScan:
    """Schwinger-Dyson vacuum stability — Evidence B."""

    def test_small_F2_is_stable(self):
        """Vanishingly small condensate must give stable vacuum."""
        mp.dps = 80
        results = sd_vacuum_scan(F2_values_GeV4=["1e-6"], verbose=False)
        assert len(results) == 1
        assert results[0]["stable"]
        assert results[0]["flag"] == "OK"

    def test_large_F2_is_unstable(self):
        """Very large condensate (>>v^2/coeff) must destabilise vacuum."""
        mp.dps = 80
        results = sd_vacuum_scan(F2_values_GeV4=["100.0"], verbose=False)
        assert len(results) == 1
        assert not results[0]["stable"]
        assert results[0]["flag"] == "[VACUUM_INSTABILITY]"

    def test_sd_residual_below_threshold_when_stable(self):
        """Stable points must satisfy |LHS_SD| < 1e-14."""
        mp.dps = 80
        results = sd_vacuum_scan(F2_values_GeV4=["0.001", "0.01", "0.05"], verbose=False)
        for r in results:
            if r["stable"]:
                assert r["residual"] < mp.mpf("1e-14"), (
                    f"SD residual too large at F2={mp.nstr(r['F2'],8)}: "
                    f"{mp.nstr(r['residual'],10)}"
                )

    def test_critical_F2_boundary(self):
        """
        At F2 exactly equal to F2_crit, <S>^2 should be zero.
        Verify <S>^2 >= 0 for F2 slightly below crit.
        """
        mp.dps = 80
        kappa    = mp.mpf("0.500")
        lambda_S = mp.mpf("5") / mp.mpf("12")
        v        = mp.mpf("0.0477")
        Delta    = mp.mpf("1.710")
        kappa_ph = kappa / Delta ** 2
        coeff_ph = kappa_ph / (mp.mpf("2") * lambda_S)
        F2_crit  = v ** 2 / coeff_ph
        F2_below = mp.nstr(F2_crit * mp.mpf("0.9999"), 20)
        results  = sd_vacuum_scan(F2_values_GeV4=[F2_below], verbose=False)
        assert results[0]["stable"]

    def test_scan_returns_correct_number_of_results(self):
        mp.dps = 80
        F2_list = ["0.001", "0.01", "0.1", "1.0"]
        results = sd_vacuum_scan(F2_values_GeV4=F2_list, verbose=False)
        assert len(results) == 4

    def test_S_vac_decreases_with_increasing_F2(self):
        """Larger condensate => smaller <S> (monotone until instability)."""
        mp.dps = 80
        F2_list = ["0.001", "0.01", "0.05"]
        results = sd_vacuum_scan(F2_values_GeV4=F2_list, verbose=False)
        stable  = [r for r in results if r["stable"]]
        if len(stable) >= 2:
            for i in range(len(stable) - 1):
                assert stable[i]["S_vac"] >= stable[i + 1]["S_vac"]


# ---------------------------------------------------------------------------
# Module V — BMW scaffold metadata
# ---------------------------------------------------------------------------

class TestBMWScaffold:
    """Verify scaffold structure — Evidence E."""

    def test_status_is_scaffold_only(self):
        result = bmw_frg_scaffold_info()
        assert result["status"] == "SCAFFOLD_ONLY"

    def test_evidence_is_E(self):
        result = bmw_frg_scaffold_info()
        assert result["evidence"] == "E"

    def test_required_steps_count(self):
        result = bmw_frg_scaffold_info()
        assert len(result["required_steps"]) == 7

    def test_lattice_inputs_defined(self):
        result = bmw_frg_scaffold_info()
        assert len(result["lattice_inputs_needed"]) >= 3


# ---------------------------------------------------------------------------
# Integration test
# ---------------------------------------------------------------------------

class TestIntegration:
    """End-to-end: RG gate => b0 => c_S => SD scan."""

    def test_full_pipeline_no_exceptions(self):
        mp.dps = 80
        rg  = verify_rg_constraint()
        assert rg["passed"]
        b0  = compute_b0_full()
        assert b0["passed"]
        cs  = compute_cs_dimensionless()
        assert cs["passed_rg"]
        sd  = sd_vacuum_scan(F2_values_GeV4=["0.001", "0.1", "10.0"], verbose=False)
        assert len(sd) == 3

    def test_c_S_consistent_with_b0(self):
        """c_S must be derived from the same kappa as b0 formula."""
        mp.dps = 80
        cs     = compute_cs_dimensionless()
        kappa  = mp.mpf("0.500")
        assert abs(cs["c_S_UV_limit"] - kappa / mp.mpf("2")) < mp.mpf("1e-14")
