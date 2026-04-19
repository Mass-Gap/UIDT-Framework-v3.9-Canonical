"""
Verification tests for Step 4b: derive phi* from U_k(phi).
"""

import mpmath as mp

from modules.frg_gamma_nlo.lagrangian import get_ledger
from modules.frg_gamma_nlo.potential_vacuum import (
    potential_u,
    dpotential_u,
    ddpotential_u,
    broken_vacuum_discriminant,
    derive_phi_star_from_potential,
    infer_lambda3_for_target_phi,
    compare_with_legacy_phi_mapping,
    potential_report,
)


def _prec():
    mp.dps = 80


class TestPotentialVacuumBasics:
    def test_discriminant_mpf(self):
        _prec()
        disc = broken_vacuum_discriminant(mp.mpf("0.25"), mp.mpf("4.0"), mp.mpf("0.41666666666666666667"))
        assert isinstance(disc, mp.mpf)

    def test_infer_lambda3_nonzero_for_nonzero_target_phi(self):
        _prec()
        lam3 = infer_lambda3_for_target_phi(mp.mpf("0.02789473684210526316"))
        assert lam3 != mp.mpf("0")

    def test_stationary_condition_residual_below_threshold(self):
        _prec()
        phi_target = mp.mpf("0.02789473684210526316")
        lam3 = infer_lambda3_for_target_phi(phi_target)
        result = derive_phi_star_from_potential(lam3)
        L = get_ledger()
        residual = abs(dpotential_u(result["phi_star"], L["KAPPA"]**2, lam3, L["LAMBDA_S"]))
        assert residual < mp.mpf("1e-14")

    def test_stability_positive_second_derivative(self):
        _prec()
        phi_target = mp.mpf("0.02789473684210526316")
        lam3 = infer_lambda3_for_target_phi(phi_target)
        result = derive_phi_star_from_potential(lam3)
        L = get_ledger()
        curvature = ddpotential_u(result["phi_star"], L["KAPPA"]**2, lam3, L["LAMBDA_S"])
        assert curvature > mp.mpf("0")

    def test_report_runs(self):
        _prec()
        report = potential_report()
        assert "phi*" in report or "phi" in report


class TestPotentialVacuumComparison:
    def test_compare_with_legacy_returns_dict(self):
        _prec()
        cmp = compare_with_legacy_phi_mapping(mp.mpf("0.02789473684210526316"))
        assert isinstance(cmp, dict)

    def test_relative_difference_zero_for_legacy_value(self):
        _prec()
        phi = mp.mpf("47.7") / mp.mpf("1710")
        cmp = compare_with_legacy_phi_mapping(phi)
        assert cmp["relative_difference"] < mp.mpf("1e-14")

    def test_derived_phi_matches_target_when_lambda3_inferred(self):
        _prec()
        phi_target = mp.mpf("47.7") / mp.mpf("1710")
        lam3 = infer_lambda3_for_target_phi(phi_target)
        result = derive_phi_star_from_potential(lam3)
        residual = abs(result["phi_star"] - phi_target)
        assert residual < mp.mpf("1e-14")

    def test_positive_root_exists(self):
        _prec()
        phi_target = mp.mpf("47.7") / mp.mpf("1710")
        lam3 = infer_lambda3_for_target_phi(phi_target)
        result = derive_phi_star_from_potential(lam3)
        assert result["phi_star"] > mp.mpf("0")

    def test_evidence_stays_D(self):
        _prec()
        phi_target = mp.mpf("47.7") / mp.mpf("1710")
        lam3 = infer_lambda3_for_target_phi(phi_target)
        result = derive_phi_star_from_potential(lam3)
        assert result["evidence"] == "[D]"
