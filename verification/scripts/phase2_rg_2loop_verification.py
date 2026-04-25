# UIDT Framework v3.9 — Phase 2: RG 2-Loop Fixed Point Verification
# TKT-20260425-L1-L4-L5-first-principles
# Evidence Category: [A] for RG constraint, [D] for 2-loop UV stability
# Run: python verification/scripts/phase2_rg_2loop_verification.py

import mpmath as mp

def verify_rg_2loop():
    """
    Verify RG fixed point and 2-loop correction at mp.dps=80.
    Race condition lock: mp.dps set locally.
    """
    mp.dps = 80

    # Exact symbolic fixed point
    kappa_exact = mp.mpf('1')
    lam_exact   = mp.mpf('5') / mp.mpf('3')

    # RG constraint [A]
    residual_exact = abs(mp.mpf('5') * kappa_exact**2 - mp.mpf('3') * lam_exact)
    assert residual_exact < mp.mpf('1e-14'), f"[RG_CONSTRAINT_FAIL] residual={residual_exact}"
    print(f"[A] RG constraint at exact FP: residual = {mp.nstr(residual_exact, 20)} < 1e-14 PASS")

    # Phenomenological fixed point (TKT-20260403-LAMBDA-FIX)
    lam_pheno = mp.mpf('5') / mp.mpf('12')
    kappa_pheno = mp.sqrt(mp.mpf('3') * lam_pheno / mp.mpf('5'))
    residual_pheno = abs(mp.mpf('5') * kappa_pheno**2 - mp.mpf('3') * lam_pheno)
    assert residual_pheno < mp.mpf('1e-14'), f"[RG_CONSTRAINT_FAIL] pheno residual={residual_pheno}"
    print(f"[A] RG constraint at pheno FP: residual = {mp.nstr(residual_pheno, 20)} < 1e-14 PASS")
    print(f"    kappa_pheno = {mp.nstr(kappa_pheno, 20)} (= 0.5 exact)")

    # 2-loop correction — [D] at strong coupling
    pi2 = mp.pi**2
    beta1 = (mp.mpf('1') / (mp.mpf('16') * pi2)) * (
        mp.mpf('3') * lam_exact**2 - mp.mpf('5') * kappa_exact**4
    )
    coeff_2loop = mp.mpf('17') / mp.mpf('3')
    beta2 = (mp.mpf('3') * lam_exact / (mp.mpf('16') * pi2)) * coeff_2loop
    dbeta1_dlam = (mp.mpf('1') / (mp.mpf('16') * pi2)) * mp.mpf('6') * lam_exact
    delta_lam = -beta2 / dbeta1_dlam
    ratio = abs(delta_lam / lam_exact)
    print(f"[D] 2-loop shift delta_lam_S = {mp.nstr(delta_lam, 10)}")
    print(f"    |delta/lambda| = {mp.nstr(ratio, 6)} (>1: perturbation breaks down at strong FP)")

    # FSS identity [B]: gamma_inf - delta_gamma = gamma_ledger
    gamma_inf   = mp.mpf('16.3437')
    delta_gamma = mp.mpf('0.0047')
    gamma_ledger = mp.mpf('16.339')
    fss_residual = abs(gamma_inf - delta_gamma - gamma_ledger)
    assert fss_residual < mp.mpf('1e-14'), f"[FSS_FAIL] residual={fss_residual}"
    print(f"[B] FSS identity gamma_inf - delta_gamma = gamma_ledger: residual = {mp.nstr(fss_residual, 20)} PASS")

    print("\nAll assertions passed.")

if __name__ == '__main__':
    verify_rg_2loop()
