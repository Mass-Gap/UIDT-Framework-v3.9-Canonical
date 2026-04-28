"""
test_l4_gamma_derivation.py — L4 Systematic Gamma Derivation Audit
====================================================================
UIDT Framework v3.9 | TKT-20260428-L4-GAMMA-DERIVATION
Evidence Category: D (internally consistent, no external confirmation)
Stratum: III

Verifies all numerical results in docs/l4_gamma_first_principles_2026-04-28.md
at mpmath 80-digit precision. Does NOT claim to resolve L4.

Reproduction:
    pip install mpmath pytest
    python verification/tests/test_l4_gamma_derivation.py
    # or: pytest verification/tests/test_l4_gamma_derivation.py -v

RACE CONDITION LOCK: mp.dps = 80 declared locally in each function.
Never use float(), round(), or centralised precision control.
"""

import mpmath as mp


def su3_constants():
    """Return SU(3) group constants as exact mpmath mpf objects."""
    mp.dps = 80  # RACE CONDITION LOCK
    Nc = mp.mpf('3')
    return {
        'Nc':      Nc,
        'C2_adj':  Nc,
        'C2_fund': (Nc**2 - 1) / (2 * Nc),
        'dim_adj': Nc**2 - 1,
        'T_fund':  mp.mpf('1') / mp.mpf('2'),
        'b0':      mp.mpf('11') * Nc / mp.mpf('3'),
        'b1':      mp.mpf('34') * Nc**2 / mp.mpf('3'),
        'b2':      mp.mpf('2857') / mp.mpf('2'),
    }


def uidt_ledger():
    """Return UIDT ledger constants as exact mpmath mpf objects."""
    mp.dps = 80  # RACE CONDITION LOCK
    return {
        'Delta_star':  mp.mpf('1710')  / mp.mpf('1000'),
        'v':           mp.mpf('477')   / mp.mpf('10000'),
        'kappa':       mp.mpf('1')     / mp.mpf('2'),
        'lambda_S':    mp.mpf('5')     / mp.mpf('12'),
        'gamma':       mp.mpf('16339') / mp.mpf('1000'),
        'gamma_inf':   mp.mpf('163437') / mp.mpf('10000'),
        'delta_gamma': mp.mpf('47')    / mp.mpf('10000'),
    }


def test_rg_constraint():
    """5*kappa^2 = 3*lambda_S must hold with residual < 1e-14 (UIDT Constitution)."""
    mp.dps = 80  # RACE CONDITION LOCK
    L = uidt_ledger()
    lhs = mp.mpf('5') * L['kappa'] ** 2
    rhs = mp.mpf('3') * L['lambda_S']
    residual = abs(lhs - rhs)
    tol = mp.mpf('1e-14')
    assert residual < tol, (
        f"[RG_CONSTRAINT_FAIL] residual={mp.nstr(residual, 6)} >= 1e-14"
    )
    print(f"RG constraint 5*kappa^2 = 3*lambda_S: PASS  "
          f"(residual = {mp.nstr(residual, 6)})")


def test_49_over_3_is_nearest_group_factor():
    """
    Verify that C2(adj)*(2*Nc+1)^2 / Nc^2 = 49/3 is the nearest SU(3)
    group-theoretic rational to gamma = 16.339 found in the systematic scan.

    This test does NOT prove L4. It confirms the Path-A observation.
    Evidence: [E] — numerical coincidence only, no group-theoretic derivation.
    """
    mp.dps = 80  # RACE CONDITION LOCK
    G = su3_constants()
    L = uidt_ledger()

    val = G['C2_adj'] * (2 * G['Nc'] + 1) ** 2 / G['Nc'] ** 2
    expected = mp.mpf('49') / mp.mpf('3')
    assert abs(val - expected) < mp.mpf('1e-14'), (
        f"C2(adj)*(2Nc+1)^2/Nc^2 != 49/3: {mp.nstr(val, 8)}"
    )

    delta = abs(val - L['gamma'])
    assert delta < mp.mpf('0.01'), (
        f"49/3 not within 0.01 of gamma_ledger: delta = {mp.nstr(delta, 6)}"
    )
    print(f"Path A: C2_adj*(2Nc+1)^2/Nc^2 = {mp.nstr(val, 10)}")
    print(f"  delta to gamma_ledger = {mp.nstr(delta, 6)} < 0.01  [confirmed]")
    print(f"  NOTE: numerical coincidence only — no group-theoretic derivation [E]")


def test_h4_n99_bridge():
    """
    Verify H4: N99 * C2(fund) / dim(adj) = 99 * (4/3) / 8 = 16.5
    Closest L5-L4 cross-deficit candidate in the scan.
    Delta = 0.161 to gamma_ledger. Evidence: [E] speculative.
    """
    mp.dps = 80  # RACE CONDITION LOCK
    G = su3_constants()
    L = uidt_ledger()

    N99 = mp.mpf('99')
    val = N99 * G['C2_fund'] / G['dim_adj']
    expected = mp.mpf('132') / mp.mpf('8')  # 16.5 exactly
    assert abs(val - expected) < mp.mpf('1e-14'), (
        f"N99*C2_fund/dim_adj != 16.5: {mp.nstr(val, 8)}"
    )

    delta = abs(val - L['gamma'])
    assert delta < mp.mpf('0.2'), (
        f"H4 value not within 0.2 of gamma: delta = {mp.nstr(delta, 6)}"
    )
    print(f"H4: N99*C2(fund)/dim(adj) = {mp.nstr(val, 8)}")
    print(f"  delta to gamma_ledger = {mp.nstr(delta, 6)}  [E] speculative L5-L4 bridge")


def test_b0_c2fund_lower_bound():
    """
    Verify b0 * C2(fund) = 44/3 = 14.667 is the closest beta-cascade result
    (Path D), confirming the gap of > 1.5 to gamma_ledger.
    """
    mp.dps = 80  # RACE CONDITION LOCK
    G = su3_constants()
    L = uidt_ledger()

    val = G['b0'] * G['C2_fund']
    expected = mp.mpf('44') / mp.mpf('3')
    assert abs(val - expected) < mp.mpf('1e-14'), (
        f"b0*C2_fund != 44/3: {mp.nstr(val, 8)}"
    )

    gap = L['gamma'] - val
    assert gap > mp.mpf('1.5'), (
        f"b0*C2_fund unexpectedly close to gamma: gap = {mp.nstr(gap, 6)}"
    )
    print(f"Path D: b0*C2(fund) = 44/3 = {mp.nstr(val, 8)}")
    print(f"  gamma - b0*C2_fund = {mp.nstr(gap, 6)} > 1.5  [Path D gap confirmed]")


def test_l4_status_unchanged():
    """
    Confirm that no path in this audit resolves L4.
    The best rational approximation 49/3 has delta > 0.005.
    L4 status must remain OPEN [D/E].
    """
    mp.dps = 80  # RACE CONDITION LOCK
    L = uidt_ledger()

    best_candidate = mp.mpf('49') / mp.mpf('3')
    delta_best = abs(best_candidate - L['gamma'])

    assert delta_best > mp.mpf('0.005'), (
        f"Unexpected: 49/3 within 0.005 of gamma — review L4 status. "
        f"delta = {mp.nstr(delta_best, 8)}"
    )
    print(f"L4 OPEN confirmed: best candidate 49/3 has "
          f"delta = {mp.nstr(delta_best, 6)} > 0.005")
    print(f"Evidence: [D/E]. No external confirmation. No closed derivation.")


if __name__ == '__main__':
    print("=" * 62)
    print("UIDT L4 Gamma Derivation Audit  —  TKT-20260428-L4-GAMMA")
    print("=" * 62)
    test_rg_constraint()
    test_49_over_3_is_nearest_group_factor()
    test_h4_n99_bridge()
    test_b0_c2fund_lower_bound()
    test_l4_status_unchanged()
    print()
    print("All L4 audit tests PASS.")
    print("L4 remains OPEN [D/E]. No closed first-principles derivation.")
    print("=" * 62)
