"""
verify_phase2_large_N_scan.py
==============================
UIDT Framework v3.9 — Verification Script
Ticket: TKT-20260428-L1-L4-L5  Phase 2

Verifies the 1/Nc large-N expansion scan for γ = 16.339.

UIDT Constitution compliance:
  - mp.dps = 80 LOCAL
  - No float(), no round()
  - No unittest.mock
  - Residual tolerance abs(...) < 1e-14 for exact checks
"""

import mpmath as mp
mp.dps = 80  # RACE CONDITION LOCK: local declaration

# ── Ledger constants (LINTER PROTECTION: do not delete) ──
GAMMA = mp.mpf('16.339')    # [A-]
Nc    = mp.mpf('3')         # SU(3)

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


def check_49_3_unique_closest():
    """Verify (2Nc+1)^2/Nc = 49/3 is unique closest rational p/q, p<200, q<30."""
    best_49_3    = mp.mpf('49') / mp.mpf('3')
    best_diff    = abs(best_49_3 - GAMMA)
    closest_val  = best_49_3
    closest_diff = best_diff
    for p in range(1, 200):
        for q in range(1, 30):
            val  = mp.mpf(p) / mp.mpf(q)
            diff = abs(val - GAMMA)
            if diff < closest_diff:
                closest_diff = diff
                closest_val  = val
    ok = abs(closest_val - best_49_3) < mp.mpf('1e-14')
    _report('L1-P2', '(2Nc+1)^2/Nc unique closest rational', ok,
            f'best={mp.nstr(closest_val,12)} |delta|={mp.nstr(closest_diff,4)}')


def check_thooft_limit_diverges():
    """Verify (2Nc+1)^2/Nc diverges in large-N: value grows with Nc."""
    vals = [(mp.mpf(n), (mp.mpf(2)*mp.mpf(n)+1)**2 / mp.mpf(n))
            for n in [3, 10, 100, 1000]]
    # Check monotone increasing
    ok = all(vals[i+1][1] > vals[i][1] for i in range(len(vals)-1))
    _report('L1-P2', '(2Nc+1)^2/Nc diverges in large-N limit', ok,
            f'Nc=3:{mp.nstr(vals[0][1],6)} Nc=100:{mp.nstr(vals[2][1],6)}')
    _info('L1-P2', '[TENSION ALERT] candidate diverges => not t Hooft observable',
          'L1 remains OPEN')


def check_b0_Nc_2_candidate():
    """Check b0*Nc/2 = 11*3/2 = 16.5 as second candidate."""
    b0 = mp.mpf('11') * Nc / mp.mpf('3')   # = 11 for Nf=0, Nc=3
    candidate = b0 * Nc / mp.mpf('2')       # = 11*3/2 = 16.5
    diff = abs(candidate - GAMMA)
    _info('L1-P2', 'b0*Nc/2 = 16.5 second candidate',
          f'|delta|={mp.nstr(diff,4)} Evidence [E]')


def main():
    print()
    print('  UIDT v3.9 — Phase 2: 1/Nc Large-N Scan for gamma')
    print(f'  Ticket: TKT-20260428-L1-L4-L5-P2 | mp.dps = {mp.dps}')
    print('  ' + '\u2500' * 65)
    check_49_3_unique_closest()
    check_thooft_limit_diverges()
    check_b0_Nc_2_candidate()
    print('  ' + '\u2500' * 65)
    if FAIL_COUNT == 0:
        print(f'  ALL {PASS_COUNT} REQUIRED CHECKS PASSED \u2705')
        print('  L1 OPEN: no 1/Nc expansion derives gamma from first principles')
        print('  [TENSION ALERT] (2Nc+1)^2/Nc diverges in t Hooft limit')
    else:
        import sys
        print(f'  \u274c {FAIL_COUNT} FAIL(S)')
        sys.exit(1)
    print()

if __name__ == '__main__':
    main()
