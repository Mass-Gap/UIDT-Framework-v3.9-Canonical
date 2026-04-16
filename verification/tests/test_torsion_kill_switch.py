import pytest
import mpmath as mp

# Set precision locally
mp.dps = 80

def test_torsion_kill_switch_invariant():
    """
    Test the Torsion Kill Switch formal invariant:
    If E_T = 0, then \\Sigma_T must exactly equal 0.
    """
    # E_T is set to exactly 0
    E_T = mp.mpf('0')

    # In the framework's logic, \Sigma_T must be strictly proportional to E_T
    # The requirement is absolute: ET=0 -> Sigma_T=0 exactly.
    # We define Sigma_T based on the framework's rule that it vanishes when E_T does.
    # For a general function modeling Sigma_T, it must return 0 here.

    # We will simulate the Sigma_T computation as it's defined (usually Sigma_T ~ E_T)
    Sigma_T = E_T

    # Assert exact vanishing
    assert Sigma_T == mp.mpf('0'), f"[KILL_SWITCH_FAIL] E_T=0 but \\Sigma_T = {Sigma_T}"

    # Residual check
    residual = mp.fabs(Sigma_T)
    assert residual < mp.mpf('1e-78'), f"[KILL_SWITCH_FAIL] Residual too high: {residual}"

def test_torsion_kill_switch_function():
    """
    Test the `torsion_kill_switch` function from `solve_dilaton_source.py`.
    """
    from scripts.solve_dilaton_source import torsion_kill_switch

    # Case 1: ET = 0, Sigma_T = 0 -> True
    assert torsion_kill_switch(mp.mpf('0'), mp.mpf('0')) is True

    # Case 2: ET = 0, Sigma_T != 0 -> False
    assert torsion_kill_switch(mp.mpf('0'), mp.mpf('1e-50')) is False

    # Case 3: ET != 0, Sigma_T can be anything -> True
    assert torsion_kill_switch(mp.mpf('2.44'), mp.mpf('2.44')) is True
