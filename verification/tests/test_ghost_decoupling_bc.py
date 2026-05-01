# verification/tests/test_ghost_decoupling_bc.py
#
# UIDT Constitution compliance:
#   - No unittest.mock, MagicMock, patch, or test doubles  (§TESTING LAWS)
#   - Real mpmath instantiation, mp.dps = 80 LOCAL          (§NUMERICAL DETERMINISM)
#   - Residual checks: abs(expected - actual) < 1e-14       (§TESTING LAWS)
#   - No float()                                            (§NUMERICAL DETERMINISM)
#
# Run: python -m pytest verification/tests/test_ghost_decoupling_bc.py -v

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import mpmath as mp
from bmw_frg_ghost_decoupling import (
    litim_threshold_ghost,
    ghost_anomalous_dimension,
    ghost_ode_rhs,
    run_ghost_flow,
    decoupling_bc_check,
)


def test_litim_threshold_exact():
    """
    Litim threshold p_c must equal 1/4 exactly [Evidence A].
    Residual tolerance: < 1e-14 (Constitution §TESTING LAWS).
    """
    mp.dps = 80  # LOCAL
    p_c      = litim_threshold_ghost()
    expected = mp.mpf("1") / mp.mpf("4")
    residual = abs(p_c - expected)
    assert residual < mp.mpf("1e-14"), (
        f"[RG_CONSTRAINT_FAIL] p_c residual = {residual}, expected < 1e-14"
    )


def test_ghost_anomalous_dimension_sign():
    """
    eta_c must be negative (ghost field is screened in decoupling scenario).
    Inputs: Z_c = 1, Z_A = 1, g^2 = 1 (dimensionless units).
    Evidence: [D]
    """
    mp.dps = 80  # LOCAL
    eta_c = ghost_anomalous_dimension(
        mp.mpf("1"),  # Z_c
        mp.mpf("1"),  # Z_A
        mp.mpf("1"),  # g^2
    )
    assert eta_c < mp.mpf("0"), (
        f"[GHOST_SECTOR_FAIL] eta_c = {eta_c} should be negative"
    )


def test_ghost_ode_rhs_zero_when_Z_c_large():
    """
    In the deep IR, if g^2 -> 0, the RHS -> 0 (frozen coupling limit).
    Test: g^2 = 0 => dZ_c/dt = 0 exactly.
    Residual: < 1e-14.
    Evidence: [A] (algebraic consequence)
    """
    mp.dps = 80  # LOCAL
    rhs = ghost_ode_rhs(
        mp.mpf("0"),   # t
        mp.mpf("1"),   # Z_c
        mp.mpf("1"),   # Z_A
        mp.mpf("0"),   # g^2 = 0
    )
    assert abs(rhs) < mp.mpf("1e-14"), (
        f"[GHOST_SECTOR_FAIL] RHS with g^2=0 should be 0, got {rhs}"
    )


def test_decoupling_bc_positive_IR():
    """
    Full ODE integration: Z_c(IR) must be positive [Evidence B, D].
    Simplified setup: Z_A = const = 1, g^2 = const = 0.5.
    Flows from t_UV=0 to t_IR=-5 (conservative range for test speed).
    """
    mp.dps = 80  # LOCAL
    Z_A_const = lambda t: mp.mpf("1")
    g2_const  = lambda t: mp.mpf("1") / mp.mpf("2")

    Z_c_IR, Z_c_sol = run_ghost_flow(
        Z_c_UV=mp.mpf("1"),
        Z_A_flow=Z_A_const,
        g2_flow=g2_const,
        t_UV=mp.mpf("0"),
        t_IR=mp.mpf("-5"),
        tol=mp.mpf("1e-20"),
    )
    assert Z_c_IR > mp.mpf("0"), (
        f"[DECOUPLING_BC_FAIL] Z_c(IR) = {Z_c_IR} must be > 0"
    )


def test_decoupling_bc_check_raises_on_zero():
    """
    decoupling_bc_check() must raise AssertionError when Z_c_IR = 0.
    Evidence: [A] (contract enforcement)
    """
    mp.dps = 80  # LOCAL
    raised = False
    try:
        decoupling_bc_check(mp.mpf("0"))
    except AssertionError:
        raised = True
    assert raised, "[DECOUPLING_BC_FAIL] Expected AssertionError for Z_c_IR=0"


def test_decoupling_bc_check_raises_on_negative():
    """
    decoupling_bc_check() must raise AssertionError when Z_c_IR < 0.
    Evidence: [A]
    """
    mp.dps = 80  # LOCAL
    raised = False
    try:
        decoupling_bc_check(mp.mpf("-0.1"))
    except AssertionError:
        raised = True
    assert raised, "[DECOUPLING_BC_FAIL] Expected AssertionError for Z_c_IR<0"


def test_rg_constraint_consistency():
    """
    Consistency check: Z_c must remain > 0 throughout the flow
    (monotone decrease toward positive IR value in Decoupling scenario).

    Samples Z_c_sol at 5 intermediate points and checks positivity.
    Evidence: [D]
    """
    mp.dps = 80  # LOCAL
    Z_A_const = lambda t: mp.mpf("1")
    g2_const  = lambda t: mp.mpf("1") / mp.mpf("2")

    _, Z_c_sol = run_ghost_flow(
        Z_c_UV=mp.mpf("1"),
        Z_A_flow=Z_A_const,
        g2_flow=g2_const,
        t_UV=mp.mpf("0"),
        t_IR=mp.mpf("-5"),
        tol=mp.mpf("1e-20"),
    )
    for i in range(1, 6):
        t_sample = mp.mpf(str(-i))
        Z_c_val  = Z_c_sol(t_sample)
        assert Z_c_val > mp.mpf("0"), (
            f"[DECOUPLING_BC_FAIL] Z_c(t={t_sample}) = {Z_c_val} <= 0"
        )
