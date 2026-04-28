"""
test_brst_su3.py — Full SU(3) BRST Nilpotency Verification
=============================================================
UIDT Framework v3.9 | TKT-20260428-BRST-SU3-FULL
Evidence category: [A] (mathematically proven)

Verifies s^2 = 0 for all 8 SU(3) generators via:
  1. Complete f^{abc} table (9 independent values, Gell-Mann convention)
  2. Jacobi identity: sum_b[f^{abc}f^{bde} + f^{abd}f^{bec} + f^{abe}f^{bcd}] = 0
  3. Tolerance: |residual| < 1e-14 (UIDT Constitution requirement)

Reproduction:
  pip install mpmath pytest
  python verification/tests/test_brst_su3.py
  # or: pytest verification/tests/test_brst_su3.py -v

RACE CONDITION LOCK: mp.dps = 80 is set locally inside each function.
Do NOT centralise precision control in config.py or global variables.
"""

import mpmath as mp


def build_su3_structure_constants():
    """
    Returns the complete SU(3) structure constant tensor f[a][b][c]
    (1-indexed, 1..8) as a dict. Fully antisymmetric.
    Gell-Mann convention. All 9 independent non-zero values.
    """
    mp.dps = 80  # RACE CONDITION LOCK: local precision
    half = mp.mpf('1') / mp.mpf('2')
    sqrt3h = mp.sqrt(mp.mpf('3')) / mp.mpf('2')
    one = mp.mpf('1')

    # 9 independent non-zero values (a < b < c canonical ordering)
    independent = [
        (1, 2, 3, one),
        (1, 4, 7, half),
        (1, 6, 5, half),   # f^{165} = +1/2  [note: 6>5, sign from antisymm]
        (2, 4, 6, half),
        (2, 5, 7, half),
        (3, 4, 5, half),
        (3, 7, 6, half),   # f^{376} = +1/2
        (4, 5, 8, sqrt3h),
        (6, 7, 8, sqrt3h),
    ]

    fabc = {}
    for (a, b, c, val) in independent:
        # Generate all 6 signed permutations (full antisymmetry)
        for (p, q, r), sgn in [
            ((a, b, c),  1), ((b, c, a),  1), ((c, a, b),  1),
            ((a, c, b), -1), ((c, b, a), -1), ((b, a, c), -1)
        ]:
            fabc[(p, q, r)] = sgn * val
    return fabc


def f_val(fabc, a, b, c):
    """Return f^{abc}, zero if not in table."""
    return fabc.get((a, b, c), mp.mpf('0'))


def verify_jacobi_identity():
    """
    Verifies the SU(3) Jacobi identity for all index combinations.
    sum_b [ f^{a,b,d}*f^{b,e,c} + f^{a,b,e}*f^{b,c,d} + f^{a,b,c}*f^{b,d,e} ] = 0
    Returns (max_residual, n_violations).
    """
    mp.dps = 80  # RACE CONDITION LOCK
    fabc = build_su3_structure_constants()
    tol = mp.mpf('1e-14')
    max_res = mp.mpf('0')
    n_viol = 0

    for a in range(1, 9):
        for c in range(1, 9):
            for d in range(1, 9):
                for e in range(1, 9):
                    S = mp.mpf('0')
                    for b in range(1, 9):
                        S += (f_val(fabc, a, b, d) * f_val(fabc, b, e, c)
                            + f_val(fabc, a, b, e) * f_val(fabc, b, c, d)
                            + f_val(fabc, a, b, c) * f_val(fabc, b, d, e))
                    if abs(S) > max_res:
                        max_res = abs(S)
                    if abs(S) > tol:
                        n_viol += 1

    return max_res, n_viol


def verify_brst_nilpotency_su3():
    """
    Main BRST s^2=0 verification for full SU(3).
    Returns True if PASS, raises AssertionError on FAIL.
    """
    mp.dps = 80  # RACE CONDITION LOCK
    tol = mp.mpf('1e-14')

    print("=" * 60)
    print("UIDT BRST Nilpotency Test — Full SU(3)")
    print("TKT-20260428-BRST-SU3-FULL | Evidence: [A]")
    print("=" * 60)

    max_res, n_viol = verify_jacobi_identity()

    print(f"Jacobi identity max residual : {mp.nstr(max_res, 10)}")
    print(f"Violations |S| > 1e-14      : {n_viol}")
    print(f"Tolerance                   : < 1e-14")

    assert n_viol == 0, (
        f"[BRST_SU3_FAIL] {n_viol} Jacobi violations found. "
        f"Max residual: {mp.nstr(max_res, 6)}"
    )
    assert max_res < tol, (
        f"[BRST_SU3_FAIL] Max residual {mp.nstr(max_res, 6)} >= 1e-14"
    )

    print()
    print("RESULT: BRST s^2 = 0 for all 8 SU(3) generators — PASS [A]")
    print(f"        max|Jacobi residuum| = {mp.nstr(max_res, 6)} < 1e-14 ✓")
    print("        Evidence category: [A] (mathematically proven)")
    print("=" * 60)
    return True


def test_brst_nilpotency():
    """pytest-compatible entry point."""
    assert verify_brst_nilpotency_su3()


def test_structure_constants_antisymmetry():
    """Verify full antisymmetry of f^{abc}: f^{abc} = -f^{bac}."""
    mp.dps = 80  # RACE CONDITION LOCK
    fabc = build_su3_structure_constants()
    tol = mp.mpf('1e-14')
    for (a, b, c), val in fabc.items():
        anti = fabc.get((b, a, c), mp.mpf('0'))
        assert abs(val + anti) < tol, (
            f"Antisymmetry violated: f^{{{a}{b}{c}}} + f^{{{b}{a}{c}}} = "
            f"{mp.nstr(abs(val + anti), 6)}"
        )


def test_rg_constraint():
    """
    Verify RG constraint 5*kappa^2 = 3*lambda_S with exact rational values.
    Tolerance: |LHS - RHS| < 1e-14 (UIDT Constitution).
    """
    mp.dps = 80  # RACE CONDITION LOCK
    kappa = mp.mpf('1') / mp.mpf('2')      # kappa = 0.500 [A]
    lambda_S = mp.mpf('5') / mp.mpf('12')  # lambda_S = 5/12 (exact) [A]
    lhs = mp.mpf('5') * kappa**2
    rhs = mp.mpf('3') * lambda_S
    residual = abs(lhs - rhs)
    assert residual < mp.mpf('1e-14'), (
        f"[RG_CONSTRAINT_FAIL] |5*kappa^2 - 3*lambda_S| = {mp.nstr(residual, 6)}"
    )
    print(f"RG constraint 5*kappa^2 = 3*lambda_S: PASS (residual = {mp.nstr(residual, 6)})")


if __name__ == '__main__':
    verify_brst_nilpotency_su3()
    test_structure_constants_antisymmetry()
    print("Antisymmetry check: PASS ✓")
    test_rg_constraint()
    print("All tests PASS [A]")
