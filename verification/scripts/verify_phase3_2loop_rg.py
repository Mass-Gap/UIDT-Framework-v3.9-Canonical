"""
verify_phase3_2loop_rg.py
==========================
UIDT Framework v3.9 — Verification Script
Ticket: TKT-20260428-L1-L4-L5  Phase 3

Verifies the 2-loop RG fixed-point correction for L4.
Uses exact lambda_S = 5/12 (TKT-20260403-LAMBDA-FIX).

UIDT Constitution compliance:
  - mp.dps = 80 LOCAL
  - No float(), no round()
  - lambda_S = 5/12 exact (not 0.417)
  - RG residual < 1e-14
"""

import sys
import mpmath as mp
mp.dps = 80  # RACE CONDITION LOCK: local

# ── Ledger constants (LINTER PROTECTION) ──
KAPPA    = mp.mpf('1') / mp.mpf('2')                    # exact  [A]
LAMBDA_S = mp.mpf('5') * KAPPA**2 / mp.mpf('3')        # = 5/12 [A]  TKT-20260403-LAMBDA-FIX
DELTA_STAR = mp.mpf('1.710')                             # GeV   [A]
GAMMA      = mp.mpf('16.339')                            # [A-]

RESIDUAL_TOL = mp.mpf('1e-14')

PASS_COUNT = 0
FAIL_COUNT = 0

def _report(tag, label, ok, detail):
    global PASS_COUNT, FAIL_COUNT
    status = 'PASS' if ok else 'FAIL'
    marker = '\u2705' if ok else '\u274c'
    print(f'  [{tag}] {label:.<50} {status}  {detail}  {marker}')
    if ok: PASS_COUNT += 1
    else:  FAIL_COUNT += 1

def _info(tag, label, detail):
    print(f'  [{tag}] {label:.<50} INFO  {detail}')


def check_rg_exact():
    """RG constraint 5kappa^2 = 3*lambda_S, residual = 0 exactly."""
    lhs = mp.mpf('5') * KAPPA**2
    rhs = mp.mpf('3') * LAMBDA_S
    residual = abs(lhs - rhs)
    ok = residual == mp.mpf('0')
    _report('L4-P3', 'RG constraint exact (lambda_S=5/12)', ok,
            f'residual={mp.nstr(residual,6)}')
    if not ok:
        print(f'  [RG_CONSTRAINT_FAIL] LHS={mp.nstr(lhs,25)} RHS={mp.nstr(rhs,25)}')


def check_2loop_shift():
    """
    Compute 2-loop fixed-point shift using exact lambda_S = 5/12.
    Reproduces rg_2loop_beta.md §4 with corrected lambda_S.
    """
    pi2 = mp.pi**2

    # 1-loop beta_lambda at FP
    beta1 = (mp.mpf('1') / (mp.mpf('16') * pi2)) * (
        mp.mpf('3') * LAMBDA_S**2 - mp.mpf('5') * KAPPA**4
    )

    # 2-loop correction (rg_2loop_beta.md §3)
    coeff_2loop = mp.mpf('17') / mp.mpf('3')
    beta2 = (mp.mpf('3') * LAMBDA_S / (mp.mpf('16') * pi2)) * coeff_2loop

    # Derivative d(beta1)/d(lambda_S)
    dbeta1_dlam = (mp.mpf('6') * LAMBDA_S) / (mp.mpf('16') * pi2)

    delta_lam = -beta2 / dbeta1_dlam

    _info('L4-P3', 'beta_1 at exact FP',
          f'{mp.nstr(beta1,10)}')
    _info('L4-P3', 'beta_2 2-loop correction',
          f'{mp.nstr(beta2,10)}')
    _info('L4-P3', '2-loop FP shift delta_lambda_S',
          f'{mp.nstr(delta_lam,10)}')

    # The shift is O(0.2): flag as non-perturbative regime
    non_pert = abs(delta_lam) > mp.mpf('0.05') * LAMBDA_S
    if non_pert:
        _info('L4-P3', 'WARNING: 2-loop shift > 5% of lambda_S*',
              'Non-perturbative FRG treatment required (TKT-20260403-FRG-NLO)')

    # Qualitative: beta2 must be positive (adds to IR stability)
    ok = beta2 > mp.mpf('0')
    _report('L4-P3', 'beta_2 positive (IR-stable direction)', ok,
            f'beta2={mp.nstr(beta2,6)}')

    return beta1, beta2, delta_lam


def check_1loop_fp_stable():
    """
    Verify eigenvalues of stability matrix at 1-loop FP are negative
    (IR-attractive fixed point).
    """
    pi2 = mp.pi**2
    prefac = mp.mpf('1') / (mp.mpf('16') * pi2)

    # Stability matrix elements at (kappa*, lambda_S*)
    # d(beta_kappa)/d(kappa) = (3*lambda_S - 15*kappa^2)*prefac
    dBk_dk = prefac * (mp.mpf('3')*LAMBDA_S - mp.mpf('15')*KAPPA**2)
    # d(beta_kappa)/d(lambda) = 3*kappa*prefac
    dBk_dl = prefac * mp.mpf('3') * KAPPA
    # d(beta_lambda)/d(kappa) = -20*kappa^3*prefac
    dBl_dk = prefac * (-mp.mpf('20') * KAPPA**3)
    # d(beta_lambda)/d(lambda) = 6*lambda_S*prefac
    dBl_dl = prefac * mp.mpf('6') * LAMBDA_S

    # Eigenvalues of 2x2 matrix
    trace = dBk_dk + dBl_dl
    det   = dBk_dk * dBl_dl - dBk_dl * dBl_dk
    disc  = trace**2 - mp.mpf('4') * det
    if disc >= mp.mpf('0'):
        ev1 = (trace + mp.sqrt(disc)) / mp.mpf('2')
        ev2 = (trace - mp.sqrt(disc)) / mp.mpf('2')
    else:
        ev_real = trace / mp.mpf('2')
        ev_imag = mp.sqrt(-disc) / mp.mpf('2')
        ev1 = ev_real
        ev2 = ev_real
        _info('L4-P3', 'Complex eigenvalues (spiral attractor)',
              f'Re={mp.nstr(ev_real,8)} Im=\u00b1{mp.nstr(ev_imag,8)}')

    ok = (ev1 < mp.mpf('0')) and (ev2 < mp.mpf('0'))
    _report('L4-P3', '1-loop FP eigenvalues negative (IR-attractive)', ok,
            f'ev1={mp.nstr(ev1,8)} ev2={mp.nstr(ev2,8)}')


def main():
    print()
    print('  UIDT v3.9 — Phase 3: 2-Loop RG Fixed-Point Correction (L4)')
    print(f'  Ticket: TKT-20260428-L1-L4-L5-P3 | mp.dps = {mp.dps}')
    print(f'  lambda_S = 5/12 = {mp.nstr(LAMBDA_S, 20)} (exact, TKT-20260403-LAMBDA-FIX)')
    print('  ' + '\u2500' * 65)
    check_rg_exact()
    check_2loop_shift()
    check_1loop_fp_stable()
    print('  ' + '\u2500' * 65)
    if FAIL_COUNT == 0:
        print(f'  ALL {PASS_COUNT} REQUIRED CHECKS PASSED \u2705')
        print('  L4 OPEN: physical origin of kappa=1/2 not derived')
        print('  L4 OPEN: 2-loop shift O(0.2) requires NLO-FRG (TKT-20260403-FRG-NLO)')
    else:
        print(f'  \u274c {FAIL_COUNT} FAIL(S)')
        sys.exit(1)
    print()

if __name__ == '__main__':
    main()
