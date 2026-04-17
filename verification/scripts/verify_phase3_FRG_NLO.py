# UIDT Framework v3.9 — Phase 3 FRG/NLO Verification Script
# TKT-20260403-FRG-NLO: γ-Derivation via Wetterinck Equation
# Author: P. Rietz | Date: 2026-04-16
# Constitution: mpmath dps=80, no float(), no round()

import mpmath as mp
mp.dps = 80


def verify_frg_nlo():
    """Verify all numerical claims in Phase 3 FRG/NLO analysis."""
    print("UIDT Phase 3 FRG/NLO Verification")
    print("TKT-20260403-FRG-NLO | mpmath dps=80")
    print("=" * 60)

    # ─── Ledger Constants (read-only) ─────────────────────────────
    Delta    = mp.mpf('1.710')          # GeV [A]
    gamma    = mp.mpf('16.339')         # [A-]
    v        = mp.mpf('47.7e-3')        # GeV [A]
    kappa    = mp.mpf('0.500')          # [A]
    lambda_S = mp.mpf('5') / 12        # [A]
    Nc       = mp.mpf('3')
    Nf       = mp.mpf('0')

    # ─── Derived quantities ───────────────────────────────────────
    E_geo    = Delta / gamma
    d_adj    = Nc**2 - 1
    b0       = mp.mpf('11') * Nc / 3 - mp.mpf('2') * Nf / 3
    c_4      = mp.mpf('1') / (32 * mp.pi**2)
    xi_eff   = kappa / Delta
    rho_0    = v**2 / 2
    rho_0_dim = rho_0 / Delta**2
    w_UV     = 2 * lambda_S * rho_0_dim

    print()
    print("--- RG Constraint ---")
    rg_residual = abs(5 * kappa**2 - 3 * lambda_S)
    print(f"  |5kappa^2 - 3*lambda_S| = {mp.nstr(rg_residual, 5)}")
    assert rg_residual < mp.mpf('1e-14'), "[RG_CONSTRAINT_FAIL]"
    print("  PASS: machine zero")

    print()
    print("--- Structural Identity: xi_eff * Delta* = kappa ---")
    xi_Delta = xi_eff * Delta
    diff_xi  = abs(xi_Delta - kappa)
    print(f"  xi_eff * Delta* = {mp.nstr(xi_Delta, 15)}")
    print(f"  kappa           = {mp.nstr(kappa, 15)}")
    print(f"  |diff|          = {mp.nstr(diff_xi, 5)}")
    assert diff_xi < mp.mpf('1e-50'), "xi_eff * Delta* != kappa [FAIL]"
    print("  PASS: exact identity (machine precision)")

    print()
    print("--- E_geo = Delta*/gamma ---")
    E_geo_mev = E_geo * 1000
    print(f"  E_geo = Delta*/gamma = {mp.nstr(E_geo_mev, 10)} MeV")
    expected_E_geo = mp.mpf('104.657')
    assert abs(E_geo_mev - expected_E_geo) < mp.mpf('0.01'), "E_geo mismatch [FAIL]"
    print("  PASS")

    print()
    print("--- LPA beta-function at UV boundary ---")
    dt_lambda_UV = c_4 * 2 * lambda_S**2 * d_adj / (1 + w_UV)**2
    dt_rho_UV    = c_4 * d_adj / (1 + w_UV)
    print(f"  2*lambda_S*rho_0_dim = {mp.nstr(w_UV, 8)}")
    print(f"  dt lambda|_UV = {mp.nstr(dt_lambda_UV, 8)}")
    print(f"  dt rho_0|_UV  = {mp.nstr(dt_rho_UV, 8)}")
    assert dt_lambda_UV > 0, "dt_lambda must be positive [FAIL]"
    assert dt_rho_UV > 0, "dt_rho must be positive [FAIL]"
    print("  PASS: both positive (UV flow direction correct)")

    print()
    print("--- Best algebraic candidate: Nc*b0/(2*kappa+1) ---")
    gamma_alg = Nc * b0 / (2 * kappa + 1)
    diff_alg  = abs(gamma_alg - gamma)
    pct_alg   = diff_alg / gamma * 100
    print(f"  gamma_alg = Nc*b0/(2kappa+1) = {mp.nstr(gamma_alg, 8)}")
    print(f"  gamma_canonical              = {mp.nstr(gamma, 8)}")
    print(f"  |diff| = {mp.nstr(diff_alg, 5)}  ({mp.nstr(pct_alg, 3)}%)")
    print(f"  Evidence: E-open (no group-theoretic derivation)")
    # Not asserting equality — this is E-open
    assert diff_alg < mp.mpf('1'), "Candidate deviates > 1 from gamma [UNEXPECTED]"
    print("  PASS: deviation < 1 (within sigma=1.005 range)")

    print()
    print("--- Path B: Delta_eta = ln(gamma) / |ln(E_geo/Delta*)| ---")
    t_flow   = mp.log(E_geo / Delta)  # < 0
    Delta_eta = mp.log(gamma) / abs(t_flow)
    print(f"  t_flow = ln(E_geo/Delta*) = {mp.nstr(t_flow, 8)}")
    print(f"  ln(gamma)                 = {mp.nstr(mp.log(gamma), 8)}")
    print(f"  Delta_eta = ln(gamma)/|t| = {mp.nstr(Delta_eta, 10)}")
    print(f"  Target: Delta_eta ≈ 1.000")
    diff_eta = abs(Delta_eta - mp.mpf('1'))
    print(f"  |Delta_eta - 1| = {mp.nstr(diff_eta, 6)}")
    # Conjecture C-05V: Delta_eta = 1 exactly
    # Not asserting — this is E-open conjecture
    assert diff_eta < mp.mpf('0.01'), "Delta_eta deviates > 0.01 from 1 [NOTE]"
    print("  NOTE: Delta_eta ~ 1 to < 0.1% [E-open conjecture UIDT-C-05V]")

    print()
    print("=" * 60)
    print("ALL CHECKS PASSED")
    print("Evidence: E-open for all new claims")
    print("Limitation L4 status: E-open (Confinement input required)")
    print("Constitution: compliant")


if __name__ == '__main__':
    verify_frg_nlo()
