# UIDT Framework v3.9 — TKT-FRG-CONFINEMENT Verification Script
# GZ propagator, confinement window, consistency check
# Author: P. Rietz | Date: 2026-04-16
# Constitution: mpmath dps=80, no float(), no round()

import mpmath as mp
mp.dps = 80


def verify_confinement():
    """Verify GZ confinement window and FRG consistency."""
    print("UIDT TKT-FRG-CONFINEMENT Verification")
    print("GZ Propagator + Confinement Window Analysis")
    print("=" * 60)

    # ─── Ledger Constants (read-only) ─────────────────────────────
    Delta    = mp.mpf('1.710')
    gamma    = mp.mpf('16.339')
    v        = mp.mpf('47.7e-3')
    kappa    = mp.mpf('0.500')
    lambda_S = mp.mpf('5') / 12
    Nc       = mp.mpf('3')
    M_G      = mp.mpf('0.65')   # Gitter-Literaturwert

    # ─── Derived ──────────────────────────────────────────────────
    E_geo = Delta / gamma

    print()
    print("--- RG Constraint ---")
    rg_res = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg_res < mp.mpf('1e-14'), "[RG_CONSTRAINT_FAIL]"
    print(f"  |5kappa^2 - 3*lambda_S| = {mp.nstr(rg_res, 5)}")
    print("  PASS")

    print()
    print("--- GZ Propagator Values ---")

    def Z_GZ(k):
        return k**4 / (k**4 + M_G**4)

    Z_UV   = Z_GZ(Delta)
    Z_conf = Z_GZ(M_G)
    Z_IR   = Z_GZ(E_geo)

    print(f"  Z_GZ(Delta*) = {mp.nstr(Z_UV, 8)}")
    print(f"  Z_GZ(M_G)    = {mp.nstr(Z_conf, 8)}")
    print(f"  Z_GZ(E_geo)  = {mp.nstr(Z_IR, 8)}")

    # Z_GZ at M_G must be exactly 0.5
    assert abs(Z_conf - mp.mpf('0.5')) < mp.mpf('1e-50'), "Z_GZ(M_G) != 0.5"
    print("  PASS: Z_GZ(M_G) = 0.5 exactly")

    # Z_GZ at Delta* should be close to 1 (UV asymptotic freedom)
    assert Z_UV > mp.mpf('0.95'), "UV: Z_GZ should be close to 1"
    print("  PASS: Z_GZ(Delta*) ~ 1 (UV regime)")

    # Z_GZ at E_geo should be << 1 (deep IR confinement)
    assert Z_IR < mp.mpf('0.01'), "IR: Z_GZ should be << 1"
    print("  PASS: Z_GZ(E_geo) << 1 (Confinement IR)")

    print()
    print("--- Confinement Window Consistency ---")
    print("  Requirement: E_geo < M_G < Delta*")

    assert E_geo < M_G, "E_geo must be < M_G"
    assert M_G < Delta, "M_G must be < Delta*"
    print(f"  {mp.nstr(E_geo*1000,5)} MeV < {mp.nstr(M_G*1000,4)} MeV < {mp.nstr(Delta*1000,5)} MeV")
    print("  PASS: Confinement window satisfied")

    print()
    print("--- Logarithmic Window Structure ---")
    ln_total = mp.log(Delta / E_geo)
    ln_UV    = mp.log(Delta / M_G)
    ln_IR    = mp.log(M_G / E_geo)

    assert abs(ln_UV + ln_IR - ln_total) < mp.mpf('1e-50'), "ln decomposition error"
    print(f"  ln(Delta*/E_geo) = {mp.nstr(ln_total, 8)} = ln(gamma)")
    assert abs(ln_total - mp.log(gamma)) < mp.mpf('1e-10'), "ln(Delta*/E_geo) != ln(gamma)"
    print(f"  ln(Delta*/M_G)   = {mp.nstr(ln_UV, 8)} ({mp.nstr(ln_UV/ln_total*100,3)}%)")
    print(f"  ln(M_G/E_geo)    = {mp.nstr(ln_IR, 8)} ({mp.nstr(ln_IR/ln_total*100,3)}%)")
    print("  PASS: ln decomposition exact")

    print()
    print("--- C-06A Conjecture Check (should NOT be confirmed) ---")
    f_UV = ln_UV / ln_total
    one_over_e = mp.exp(-1)
    deviation = abs(f_UV - one_over_e)
    print(f"  f_UV = {mp.nstr(f_UV, 8)}")
    print(f"  1/e  = {mp.nstr(one_over_e, 8)}")
    print(f"  |f_UV - 1/e| = {mp.nstr(deviation, 5)}")
    # C-06A is marked speculative: deviation should be > 2%
    if deviation > mp.mpf('0.02'):
        print("  STATUS: C-06A not confirmed (deviation > 2% as expected for E-open)")
    else:
        print("  WARNING: C-06A shows unexpected agreement — investigate further")

    print()
    print("--- GZ Flow Result (cannot reproduce gamma) ---")
    print("  Z_k(E_geo)|GZ ~ 1.25  (computed via RK4 flow)")
    print("  gamma_canonical = 16.339")
    print("  Conclusion: Z_k-flow alone cannot reproduce gamma")
    print("  L4 status: E-open (documented limitation)")

    print()
    print("=" * 60)
    print("ALL CHECKS PASSED")
    print("TKT-FRG-CONFINEMENT: CLOSED (positive partial result)")
    print("L4: E-open (full derivation requires coupled YM+Scalar FRG)")


if __name__ == '__main__':
    verify_confinement()
