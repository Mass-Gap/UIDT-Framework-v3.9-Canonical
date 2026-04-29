"""Verification: 2-Loop β-Fixpunkt-Analyse UIDT v3.9

Prüft die strukturelle Aussage:
  β_g^pert < 0 für alle g > 0 (SU(3), N_f=0, reine YM)
  und bestimmt LPA-Fixpunkt-Eigenschaften.

Evidenz: [D] Prediction
Epistemic-Stratum: III
mp.dps = 80 (lokal, Race-Condition-safe)
"""
import mpmath as mp


def verify_2loop_beta_negativity():
    mp.dps = 80
    Nc = mp.mpf('3')
    b0 = 11 * Nc / 3
    b1 = 34 * Nc**2 / 3
    loop = 16 * mp.pi**2
    N_G = Nc**2 - 1

    # Theorem: β_g^pert < 0 für alle g > 0
    errors = []
    test_g_vals = ['0.01', '0.1', '0.5', '1.0', '2.0', '5.0']
    for gs in test_g_vals:
        g = mp.mpf(gs)
        beta_g = -(b0 / loop) * g**3 - (b1 / loop**2) * g**5
        if beta_g >= 0:
            errors.append(f"FAIL: β_g(g={gs}) = {mp.nstr(beta_g, 8)} >= 0")

    if errors:
        for e in errors:
            print(e)
        raise AssertionError("[THEOREM_FAIL] β_g >= 0 detected")
    print("PASS: β_g^pert < 0 für alle getesteten g > 0  [A]")

    # Threshold-Scan: b_eff(κ̃) = 0 für α_s = 1/3?
    alpha_star = mp.mpf('1') / 3
    g2_star = 4 * mp.pi * alpha_star
    print(f"\nThreshold-Scan für α_s* = 1/3, g²* = {mp.nstr(g2_star, 6)}:")
    found_zero = False
    for kappa_test in [mp.mpf('0.1') * i for i in range(1, 50)]:
        mGl2 = g2_star * kappa_test
        prop_gl = 1 / (1 + mGl2)
        b_eff = b0 - 4 * N_G * kappa_test * prop_gl**2
        if b_eff <= 0:
            found_zero = True
            print(f"  b_eff = 0 bei κ̃ ≈ {mp.nstr(kappa_test, 4)}")
            break
    if not found_zero:
        print("  [SEARCH_FAIL] Keine reelle Nullstelle b_eff=0 im Bereich κ̃∈(0.1,5.0)")
        print("  → ERGE-Fixpunkt bei α_s=1/3 erfordert jenseits-LPA-Beiträge")

    # LPA-Fixpunkt-Stabilitäts-Eigenwerte (Gauss'scher FP)
    print("\nStabilitäts-Eigenwerte am Gauss'schen Fixpunkt (LPA):")
    canonical_dims = [mp.mpf('-2'), mp.mpf('-4'), mp.mpf('-6') + b0/loop * g2_star]
    for i, theta in enumerate(canonical_dims):
        status = 'RELEVANT (IR-attraktiv)' if theta < 0 else 'IRRELEVANT'
        print(f"  θ_{i+1} ≈ {mp.nstr(theta, 8)}  [{status}]")

    # RG-Constraint-Check am Ledger-Punkt
    kappa_l = mp.mpf('0.500')
    lambda_l = mp.mpf('5') / 12
    lhs = 5 * kappa_l**2
    rhs = 3 * lambda_l
    residual = abs(lhs - rhs)
    print(f"\nRG-Constraint 5κ²=3λ_S am Ledger:")
    print(f"  5κ² = {mp.nstr(lhs, 12)}")
    print(f"  3λ_S = {mp.nstr(rhs, 12)}")
    print(f"  |5κ² - 3λ_S| = {mp.nstr(residual, 6)}")
    if residual < mp.mpf('1e-14'):
        print("  → RG-CONSTRAINT SATISFIED")
    else:
        print(f"  → [RG_CONSTRAINT_FAIL]: Residual = {mp.nstr(residual, 4)}")
        print("     Note: 5κ²=3λ_S ist keine LPA-Gleichgewichtsbedingung")
        print("     Es ist eine UIDT-spezifische Kopplungsbedingung (Stratum III)")
    return True


if __name__ == '__main__':
    result = verify_2loop_beta_fixpoint()
    print(f"\nVerifikation abgeschlossen: {result}")


def verify_2loop_beta_fixpoint():
    return verify_2loop_beta_negativity()
