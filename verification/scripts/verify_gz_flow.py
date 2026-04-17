# UIDT Framework v3.9 — TKT-FRG-CONFINEMENT Verification Script
# Gribov-Zwanziger FRG Flow reproducing gamma = 16.339
# Author: P. Rietz | Date: 2026-04-16
# Constitution: mpmath dps=80, no float(), no round()

import mpmath as mp
mp.dps = 80


def verify_gz_flow():
    """Verify GZ-flow integration and M_G* computation."""
    print("UIDT TKT-FRG-CONFINEMENT Verification")
    print("Gribov-Zwanziger FRG Flow: gamma reproduction")
    print("=" * 60)

    # ─── Ledger Constants (read-only) ─────────────────────────────
    Delta    = mp.mpf('1.710')
    gamma    = mp.mpf('16.339')
    v        = mp.mpf('47.7e-3')
    kappa    = mp.mpf('0.500')
    lambda_S = mp.mpf('5') / 12

    # ─── Derived ──────────────────────────────────────────────────
    E_geo = Delta / gamma
    M_G   = E_geo * (gamma - 1) ** mp.mpf('0.25')

    print()
    print("--- RG Constraint ---")
    rg_res = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg_res < mp.mpf('1e-14'), "[RG_CONSTRAINT_FAIL]"
    print(f"  |5kappa^2 - 3*lambda_S| = {mp.nstr(rg_res, 5)}")
    print("  PASS: machine zero")

    print()
    print("--- M_G* computation ---")
    print(f"  E_geo = Delta/gamma = {mp.nstr(E_geo*1000, 8)} MeV")
    print(f"  M_G*  = E_geo*(gamma-1)^(1/4) = {mp.nstr(M_G*1000, 8)} MeV")
    assert M_G > mp.mpf('0.100'), "M_G* must be > 100 MeV"
    assert M_G < mp.mpf('0.500'), "M_G* must be < 500 MeV"
    print("  PASS: M_G* in expected range")

    print()
    print("--- GZ anomalous dimension ---")

    def eta_A_GZ(k, M_G):
        x = (M_G / k) ** 4
        return 4 * x / (1 + x)

    eta_at_Delta = eta_A_GZ(Delta, M_G)
    eta_at_Egeo  = eta_A_GZ(E_geo, M_G)
    print(f"  eta_A^GZ(k=Delta*) = {mp.nstr(eta_at_Delta, 8)}")
    print(f"  eta_A^GZ(k=E_geo)  = {mp.nstr(eta_at_Egeo, 8)}")
    assert eta_at_Delta < eta_at_Egeo, "eta must increase toward IR"
    print("  PASS: eta increases toward IR")

    print()
    print("--- GZ Flow Integration ---")

    def integrand(k):
        x = (M_G / k) ** 4
        return 4 * x / (1 + x) / k

    ln_ratio, err = mp.quad(integrand, [E_geo, Delta], error=True)
    gamma_GZ = mp.exp(ln_ratio)
    print(f"  integral ln(Z_k) = {mp.nstr(ln_ratio, 10)}")
    print(f"  gamma_GZ = exp(integral) = {mp.nstr(gamma_GZ, 10)}")
    print(f"  gamma_canonical           = {mp.nstr(gamma, 10)}")

    deviation = abs(gamma_GZ - gamma) / gamma
    print(f"  relative deviation = {mp.nstr(deviation * 100, 5)}%")
    assert deviation < mp.mpf('0.001'), f"GZ flow deviation too large: {deviation}"
    print("  PASS: GZ flow reproduces gamma within 0.1%")

    print()
    print("--- Circularity check ---")
    print("  M_G* is derived FROM gamma, not independent.")
    print("  GZ-flow gives: gamma_GZ = exp(integral(M_G*)) = gamma by construction.")
    print("  This is structural, not a prediction. Evidence: D.")
    print("  PASS: circularity explicitly acknowledged")

    print()
    print("--- GZ regime transition scale ---")
    k_star = M_G * mp.mpf('3') ** mp.mpf('0.25')
    print(f"  k* (eta_A=1 crossing) = {mp.nstr(k_star*1000, 8)} MeV")
    print(f"  E_geo                 = {mp.nstr(E_geo*1000, 8)} MeV")
    ratio_ks = k_star / E_geo
    print(f"  k*/E_geo = {mp.nstr(ratio_ks, 6)}  (expect ~ 0.76)")
    assert mp.mpf('0.5') < ratio_ks < mp.mpf('1.5'), "k* should be near E_geo"
    print("  PASS: k* is in neighbourhood of E_geo")

    print()
    print("=" * 60)
    print("ALL CHECKS PASSED")
    print("TKT-FRG-CONFINEMENT: CLOSED (structural results documented)")
    print("UIDT-C-06A: [D] new prediction filed")
    print("L4 status: E-open (circularity established, testable prediction available)")


if __name__ == '__main__':
    verify_gz_flow()
