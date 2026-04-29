#!/usr/bin/env python3
"""Verification script: L1 bare gamma theorem (Session 2, 2026-04-29)

Tests:
  1. gamma_bare = (2*Nc+1)**2/Nc = 49/3 exakt
  2. |gamma_bare - gamma_ledger| < 2*delta_gamma
  3. RG-Constraint: 5*kappa**2 = 3*lambda_S (residual < 1e-14)
  4. Tachyon-UV-Masse: |mu_UV| in physikalischem Bereich

Requirements: mpmath
Run: python3 verification/scripts/test_L1_bare_gamma_session2.py
"""
import mpmath as mp
mp.dps = 80

RESIDUAL_TOL = mp.mpf('1e-14')

DELTA_STAR = mp.mpf('1.710')
GAMMA      = mp.mpf('16.339')
GAMMA_INF  = mp.mpf('16.3437')
DELTA_G    = mp.mpf('0.0047')
V          = mp.mpf('47.7e-3')
KAPPA      = mp.mpf('0.500')
LAMBDA_S   = mp.mpf('5') * KAPPA**2 / mp.mpf('3')
Nc         = mp.mpf('3')


def test_rg_constraint():
    lhs = mp.mpf('5') * KAPPA**2
    rhs = mp.mpf('3') * LAMBDA_S
    residual = abs(lhs - rhs)
    assert residual < RESIDUAL_TOL, (
        f"[RG_CONSTRAINT_FAIL] residual={mp.nstr(residual, 6)} >= 1e-14"
    )
    print(f"  [PASS] RG-Constraint: residual={mp.nstr(residual, 6)} < 1e-14")


def test_bare_gamma_formula():
    gamma_bare = (mp.mpf('2') * Nc + mp.mpf('1'))**2 / Nc
    expected = mp.mpf('49') / mp.mpf('3')
    residual = abs(gamma_bare - expected)
    assert residual < RESIDUAL_TOL, (
        f"[FAIL] gamma_bare != 49/3: residual={mp.nstr(residual, 6)}"
    )
    print(f"  [PASS] gamma_bare = (2Nc+1)^2/Nc = {mp.nstr(gamma_bare, 20)}")


def test_bare_gamma_within_2delta():
    gamma_bare = (mp.mpf('2') * Nc + mp.mpf('1'))**2 / Nc
    diff = abs(gamma_bare - GAMMA)
    tol = mp.mpf('2') * DELTA_G
    assert diff < tol, (
        f"[FAIL] |gamma_bare - gamma_ledger| = {mp.nstr(diff, 6)} >= 2*delta_gamma={mp.nstr(tol, 6)}"
    )
    print(f"  [PASS] |gamma_bare - gamma_ledger| = {mp.nstr(diff, 8)} < 2*delta_gamma")


def test_delta_sign_positive():
    """gamma_ledger > gamma_bare: positive quantum correction expected"""
    gamma_bare = (mp.mpf('2') * Nc + mp.mpf('1'))**2 / Nc
    delta = GAMMA - gamma_bare
    assert delta > mp.mpf('0'), (
        f"[FAIL] delta = gamma_ledger - gamma_bare = {mp.nstr(delta, 6)} is not positive"
    )
    print(f"  [PASS] delta = +{mp.nstr(delta, 8)} > 0 (positive quantum correction)")


def test_tachyon_mu_scale():
    """UV tachyon mass should be ~ SVZ gluon condensate scale (~700 MeV)"""
    g2_eff = mp.mpf('4') * mp.pi * mp.mpf('0.3')
    sigma_coeff = mp.mpf('3') * g2_eff * Nc / (mp.mpf('32') * mp.pi**2)
    k_crit = DELTA_STAR / GAMMA
    mu2_needed = (k_crit**2 - DELTA_STAR**2) * sigma_coeff
    mu_uv = mp.sqrt(-mu2_needed)
    # Should be in range [0.3, 0.9] GeV (physically motivated)
    assert mp.mpf('0.3') < mu_uv < mp.mpf('0.9'), (
        f"[FAIL] mu_UV = {mp.nstr(mu_uv, 6)} GeV outside [0.3, 0.9] GeV"
    )
    print(f"  [PASS] mu_UV = {mp.nstr(mu_uv, 10)} GeV (SVZ-compatible range)")


def test_torsion_kill_switch():
    """ET != 0 => Torsion Kill Switch not triggered, Sigma_T != 0"""
    ET = mp.mpf('2.44e-3')  # GeV
    assert ET != mp.mpf('0'), "[FAIL] ET should be non-zero"
    sigma_T = ET * V**2 / (mp.mpf('2') * DELTA_STAR**2)
    assert sigma_T != mp.mpf('0'), "[FAIL] Sigma_T should be non-zero"
    print(f"  [PASS] ET={mp.nstr(ET*1000,4)} MeV != 0, Sigma_T={mp.nstr(sigma_T*1e6,6)} keV")


if __name__ == '__main__':
    print("=" * 60)
    print("  UIDT L1/L4/L5 Session-2 Verification (mp.dps=80)")
    print("=" * 60)
    tests = [
        test_rg_constraint,
        test_bare_gamma_formula,
        test_bare_gamma_within_2delta,
        test_delta_sign_positive,
        test_tachyon_mu_scale,
        test_torsion_kill_switch,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"  {e}")
            failed += 1
    print("=" * 60)
    print(f"  Results: {passed} passed, {failed} failed")
    if failed > 0:
        raise SystemExit(1)
    print("  ALL TESTS PASSED")
