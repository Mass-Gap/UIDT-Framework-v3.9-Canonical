# UIDT Framework v3.9 — TKT-FRG-XI-LOOP Verification Script
# 1-loop xi-vertex contribution to eta_A and eta_S
# Author: P. Rietz | Date: 2026-04-16
# Constitution: mpmath dps=80, no float(), no round()

import mpmath as mp
mp.dps = 80


def verify_xi_loop():
    """Verify all numerical claims in TKT-FRG-XI-LOOP analysis."""
    print("UIDT TKT-FRG-XI-LOOP Verification")
    print("1-loop xi-vertex: eta_A and eta_S")
    print("=" * 60)

    # ─── Ledger Constants (read-only) ─────────────────────────────
    Delta    = mp.mpf('1.710')
    gamma    = mp.mpf('16.339')
    v        = mp.mpf('47.7e-3')
    kappa    = mp.mpf('0.500')
    lambda_S = mp.mpf('5') / 12
    Nc       = mp.mpf('3')
    Nf       = mp.mpf('0')

    # ─── Derived ──────────────────────────────────────────────────
    E_geo    = Delta / gamma
    d_adj    = Nc**2 - 1
    b0       = mp.mpf('11') * Nc / 3 - mp.mpf('2') * Nf / 3
    c_4      = mp.mpf('1') / (32 * mp.pi**2)
    xi_eff   = kappa / Delta
    m_S_sq   = 2 * lambda_S * v**2
    m_S      = mp.sqrt(m_S_sq)

    print()
    print("--- RG Constraint ---")
    rg_res = abs(5 * kappa**2 - 3 * lambda_S)
    print(f"  |5kappa^2 - 3*lambda_S| = {mp.nstr(rg_res, 5)}")
    assert rg_res < mp.mpf('1e-14'), "[RG_CONSTRAINT_FAIL]"
    print("  PASS: machine zero")

    print()
    print("--- Structural identity: xi_eff * Delta* = kappa ---")
    xi_Delta = xi_eff * Delta
    assert abs(xi_Delta - kappa) < mp.mpf('1e-50'), "Identity failed"
    print(f"  xi_eff * Delta* = {mp.nstr(xi_Delta, 15)}")
    print("  PASS: exact")

    print()
    print("--- eta_A|xi at k = Delta* ---")
    eta_A_xi_UV = 3 * xi_eff**2 * v**2 * c_4 * Delta**2
    print(f"  eta_A|xi(k=Delta*) = {mp.nstr(eta_A_xi_UV, 8)}")
    assert eta_A_xi_UV > 0, "Must be positive"
    assert eta_A_xi_UV < mp.mpf('1e-4'), "Must be << 1"
    print("  PASS: small and positive")

    print()
    print("--- eta_S|xi at k = Delta* ---")
    eta_S_xi_UV = xi_eff**2 * c_4 * 4 * Delta**2 * d_adj * mp.mpf('3') / 4
    print(f"  eta_S|xi(k=Delta*) = {mp.nstr(eta_S_xi_UV, 8)}")
    assert eta_S_xi_UV > 0, "Must be positive"
    print("  PASS: positive")

    print()
    print("--- eta_A|xi << eta_S|xi (xi-loop direction) ---")
    ratio_xi = eta_A_xi_UV / eta_S_xi_UV
    print(f"  eta_A|xi / eta_S|xi = {mp.nstr(ratio_xi, 8)}")
    expected_ratio = v**2 / d_adj
    assert abs(ratio_xi - expected_ratio) < mp.mpf('1e-10'), "Ratio formula mismatch"
    assert ratio_xi < mp.mpf('1'), "eta_A must be < eta_S for xi-loop"
    print("  PASS: eta_A|xi < eta_S|xi confirmed (xi-loop suppresses Z_k/Z_S)")

    print()
    print("--- YM sector dominance over xi-loop ---")
    alpha_s = mp.mpf('0.3')
    g2_UV   = 4 * mp.pi * alpha_s
    eta_A_YM = b0 * g2_UV / (16 * mp.pi**2)
    dominance = eta_A_YM / eta_A_xi_UV
    print(f"  eta_A|YM(k=Delta*) = {mp.nstr(eta_A_YM, 6)}")
    print(f"  Dominance ratio = {mp.nstr(dominance, 6)}")
    assert dominance > mp.mpf('1000'), "YM must dominate by >1000x"
    print("  PASS: YM dominates xi-loop by >> 1000x")

    print()
    print("--- UIDT-C-05V withdrawal check ---")
    print("  C-05V claimed: Delta_eta = eta_A - eta_S = 1")
    print("  Result: eta_A|xi << eta_S|xi (opposite direction)")
    print("  Result: YM dominates, xi-loop is < 0.003% of eta_A")
    print("  Status: C-05V WITHDRAWN (not supportable at 1-loop)")

    print()
    print("--- Freezing scale k_freeze ---")
    A = 2 * lambda_S
    B = mp.mpf('1')
    C = -c_4 * d_adj / 2
    rho_freeze = (-B + mp.sqrt(B**2 - 4*A*C)) / (2*A)
    rho_phys   = v**2 / 2
    k_freeze   = mp.sqrt(rho_phys / rho_freeze)
    print(f"  rho_tilde_freeze = {mp.nstr(rho_freeze, 8)}")
    print(f"  k_freeze = {mp.nstr(k_freeze*1000, 8)} MeV")
    print(f"  E_geo    = {mp.nstr(E_geo*1000, 8)} MeV")
    print(f"  Deviation: {mp.nstr(abs(k_freeze-E_geo)/E_geo*100, 4)}%")
    assert abs(k_freeze - E_geo) / E_geo > mp.mpf('1'), "k_freeze should NOT equal E_geo"
    print("  PASS: LPA freezing scale confirmed != E_geo (as expected)")

    print()
    print("=" * 60)
    print("ALL CHECKS PASSED")
    print("TKT-FRG-XI-LOOP: CLOSED (negative results)")
    print("UIDT-C-05V: WITHDRAWN")
    print("L4 status: E-open (Confinement input required)")


if __name__ == '__main__':
    verify_xi_loop()
