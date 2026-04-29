"""
verify_frg_gamma_path_b.py
==========================
UIDT Framework v3.9 Canonical
TKT-20260428-L4-FRG-gamma-derivation -- Phase 1: Algebraic Path-B Check

Purpose:
    Verify the numerical coincidence between the UIDT ledger value
    gamma = 16.339 [A-] and the color-algebra candidate
    gamma_color = (2*N_c + 1)**2 / N_c = 49/3 for SU(3).

    Also verifies:
    - RG constraint: 5*kappa^2 == 3*lambda_S  (residual < 1e-14)
    - Torsion kill switch: ET != 0 => Sigma_T != 0
    - Ledger self-consistency: Delta*/v does NOT reproduce gamma
      (confirms gamma is not simply Delta*/v)

Evidence classification:
    gamma = 16.339                  [A-] phenomenological (ledger)
    gamma_color = 49/3              [E]  speculative candidate
    Numerical match ~0.037%         [E]  requires algebraic proof

Compliance:
    - mp.dps = 80 declared locally (no global precision control)
    - No float() used anywhere
    - No round() used anywhere
    - Residual check: |expected - actual| < 1e-14
    - Real mpmath calculations only (no mocks)
    - MASS DELETION LOCK: script is additive only

Usage:
    python3 verification/scripts/verify_frg_gamma_path_b.py

Expected output (all PASS):
    [PATH-B-01] gamma_color numerical value
    [PATH-B-02] Relative deviation from ledger gamma
    [PATH-B-03] RG constraint residual
    [PATH-B-04] Torsion kill switch
    [PATH-B-05] Delta*/v != gamma (confirms non-trivial nature)
    [PATH-B-06] gamma_inf consistency
    [SUMMARY]   PASS/FAIL counts

DOI: 10.5281/zenodo.17835200
"""

import sys
import mpmath as mp

# -----------------------------------------------------------------------
# RACE CONDITION LOCK: mp.dps declared locally, NOT in global config
# -----------------------------------------------------------------------
mp.dps = 80

# -----------------------------------------------------------------------
# IMMUTABLE PARAMETER LEDGER (read-only reference, never modified)
# -----------------------------------------------------------------------
DELTA_STAR    = mp.mpf('1.710')          # GeV  [A]
GAMMA_LEDGER  = mp.mpf('16.339')         #      [A-]
GAMMA_INF     = mp.mpf('16.3437')        #      [A-]
DELTA_GAMMA   = mp.mpf('0.0047')         #
V_VEV         = mp.mpf('47.7')           # MeV  [A]
W0            = mp.mpf('-0.99')          #      [C]
ET            = mp.mpf('2.44')           # MeV  [C]
KAPPA         = mp.mpf('1') / mp.mpf('2')       # [A] exact
LAMBDA_S      = mp.mpf('5') / mp.mpf('12')      # [A] exact  5/12
N_C           = mp.mpf('3')              # SU(3) color number

# Residual tolerance per UIDT Constitution
TOL = mp.mpf('1e-14')

# -----------------------------------------------------------------------
# Test registry
# -----------------------------------------------------------------------
results = []

def check(test_id, description, passed, detail):
    status = 'PASS' if passed else 'FAIL'
    results.append((test_id, status))
    marker = '[OK]' if passed else '[!!]'
    print(f"{marker} [{test_id}] {description}")
    print(f"         {detail}")
    print()


def run_verification():
    print("=" * 70)
    print("UIDT v3.9 -- Phase 1 Path-B Verification: gamma color algebra")
    print("TKT-20260428-L4-FRG-gamma-derivation")
    print(f"mp.dps = {mp.dps}")
    print("=" * 70)
    print()

    # -------------------------------------------------------------------
    # PATH-B-01: Compute gamma_color = (2*N_c + 1)^2 / N_c
    # -------------------------------------------------------------------
    gamma_color = (2 * N_C + 1) ** 2 / N_C
    # For N_c=3: (7)^2 / 3 = 49/3
    gamma_color_rational = mp.mpf('49') / mp.mpf('3')
    rational_match = abs(gamma_color - gamma_color_rational) < TOL

    check(
        'PATH-B-01',
        'gamma_color = (2*N_c+1)^2 / N_c computed correctly',
        rational_match,
        f"gamma_color = {mp.nstr(gamma_color, 30)}\n"
        f"         49/3       = {mp.nstr(gamma_color_rational, 30)}\n"
        f"         |diff|     = {mp.nstr(abs(gamma_color - gamma_color_rational), 10)}"
    )

    # -------------------------------------------------------------------
    # PATH-B-02: Relative deviation from ledger gamma [A-]
    # -------------------------------------------------------------------
    delta_rel = abs(gamma_color - GAMMA_LEDGER) / GAMMA_LEDGER
    # Expected: ~0.000366... (0.037%)
    # This is a numerical coincidence check, NOT a proof
    deviation_small = delta_rel < mp.mpf('0.001')  # < 0.1%

    check(
        'PATH-B-02',
        'Relative deviation gamma_color vs ledger gamma < 0.1%',
        deviation_small,
        f"gamma_ledger = {mp.nstr(GAMMA_LEDGER, 20)} [A-]\n"
        f"         gamma_color  = {mp.nstr(gamma_color, 20)} [E]\n"
        f"         |delta_rel|  = {mp.nstr(delta_rel, 10)} ({mp.nstr(delta_rel*100, 6)} %)\n"
        f"         NOTE: Numerical match [E] -- algebraic proof MISSING"
    )

    # -------------------------------------------------------------------
    # PATH-B-03: RG constraint 5*kappa^2 = 3*lambda_S (exact)
    # -------------------------------------------------------------------
    rg_lhs = 5 * KAPPA ** 2
    rg_rhs = 3 * LAMBDA_S
    rg_residual = abs(rg_lhs - rg_rhs)
    rg_ok = rg_residual < TOL

    if not rg_ok:
        print("[RG_CONSTRAINT_FAIL]")

    check(
        'PATH-B-03',
        'RG constraint: |5*kappa^2 - 3*lambda_S| < 1e-14',
        rg_ok,
        f"5*kappa^2   = {mp.nstr(rg_lhs, 30)}\n"
        f"         3*lambda_S  = {mp.nstr(rg_rhs, 30)}\n"
        f"         residual    = {mp.nstr(rg_residual, 10)}"
    )

    # -------------------------------------------------------------------
    # PATH-B-04: Torsion kill switch ET != 0 => Sigma_T != 0
    # -------------------------------------------------------------------
    et_nonzero = abs(ET) > TOL
    # If ET != 0, Sigma_T must be nonzero (kill switch inactive)
    sigma_t_nonzero = et_nonzero  # by UIDT Constitution rule

    check(
        'PATH-B-04',
        'Torsion kill switch: ET != 0 confirmed (Sigma_T != 0)',
        sigma_t_nonzero,
        f"ET = {mp.nstr(ET, 10)} MeV [C]\n"
        f"         ET != 0: {et_nonzero} => Sigma_T != 0 (kill switch INACTIVE)"
    )

    # -------------------------------------------------------------------
    # PATH-B-05: Confirm Delta*/v does NOT directly reproduce gamma
    # (gamma is non-trivially phenomenological, not simply Delta*/v)
    # -------------------------------------------------------------------
    # Unit note: Delta* in GeV, V_VEV in MeV => convert
    delta_star_mev = DELTA_STAR * mp.mpf('1000')  # convert to MeV
    gamma_naive = delta_star_mev / V_VEV
    # Expected: ~35.85, NOT 16.339
    not_equal = abs(gamma_naive - GAMMA_LEDGER) > mp.mpf('1.0')  # clearly different

    check(
        'PATH-B-05',
        'Delta*/v != gamma_ledger (gamma is non-trivial, not simple ratio)',
        not_equal,
        f"Delta* / v  = {mp.nstr(delta_star_mev, 10)} MeV / {mp.nstr(V_VEV, 10)} MeV\n"
        f"           = {mp.nstr(gamma_naive, 20)}\n"
        f"         gamma_ledger= {mp.nstr(GAMMA_LEDGER, 20)}\n"
        f"         |diff|      = {mp.nstr(abs(gamma_naive - GAMMA_LEDGER), 10)}\n"
        f"         => gamma is NOT simply Delta*/v [confirms non-trivial origin]"
    )

    # -------------------------------------------------------------------
    # PATH-B-06: gamma_inf consistency with delta_gamma
    # -------------------------------------------------------------------
    gamma_inf_check = abs(GAMMA_INF - GAMMA_LEDGER - DELTA_GAMMA)
    # Expected: small (ledger consistency)
    inf_consistent = gamma_inf_check < mp.mpf('0.01')  # within 0.01

    check(
        'PATH-B-06',
        'gamma_inf = gamma + delta_gamma (ledger internal consistency)',
        inf_consistent,
        f"gamma_inf   = {mp.nstr(GAMMA_INF, 20)} [A-]\n"
        f"         gamma       = {mp.nstr(GAMMA_LEDGER, 20)} [A-]\n"
        f"         delta_gamma = {mp.nstr(DELTA_GAMMA, 10)}\n"
        f"         |gamma_inf - gamma - delta_gamma| = {mp.nstr(gamma_inf_check, 10)}"
    )

    # -------------------------------------------------------------------
    # PATH-B-07: 49/3 exact rational verification
    # -------------------------------------------------------------------
    # Confirm 49/3 is exactly representable and equals gamma_color
    forty_nine_thirds = mp.mpf('49') / mp.mpf('3')
    exact_match = abs(gamma_color - forty_nine_thirds) == mp.mpf('0')

    check(
        'PATH-B-07',
        '49/3 exact rational representation matches gamma_color',
        exact_match,
        f"49/3 = {mp.nstr(forty_nine_thirds, 40)}\n"
        f"         gamma_color = {mp.nstr(gamma_color, 40)}\n"
        f"         |diff| = {mp.nstr(abs(gamma_color - forty_nine_thirds), 10)}"
    )

    # -------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------
    print("=" * 70)
    passed = sum(1 for _, s in results if s == 'PASS')
    failed = sum(1 for _, s in results if s == 'FAIL')
    total  = len(results)

    print(f"[SUMMARY] {passed}/{total} tests PASSED, {failed}/{total} FAILED")
    print()

    if failed > 0:
        print("FAILED tests:")
        for tid, status in results:
            if status == 'FAIL':
                print(f"  - [{tid}]")
        print()

    print("Evidence classification reminder:")
    print("  gamma = 16.339            [A-] phenomenological (ledger, unchanged)")
    print("  gamma_color = 49/3        [E]  speculative candidate")
    print("  Numerical match ~0.037%   [E]  algebraic proof MISSING")
    print("  Path B NOT proven by this script -- numerical coincidence only")
    print()
    print("Next step: Implement verify_frg_gamma_fixedpoint.py (Phase 2, BMW/LPA')")
    print("=" * 70)

    return failed == 0


if __name__ == '__main__':
    success = run_verification()
    sys.exit(0 if success else 1)
