"""
Tests for UIDT GEOMETRIC OPERATOR (Pillar I & 0)
==============================================
"""

import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from mpmath import mp, mpf
except ImportError:
    # If mpmath is missing, we cannot run these tests.
    print("Skipping tests: mpmath not installed.")
    sys.exit(0)

from modules.geometric_operator import GeometricOperator

# Local precision override (UIDT Constitution)
mp.dps = 80

def test_initialization():
    """Verify initialization of fundamental constants."""
    op = GeometricOperator()

    # Assert values match canonical strings
    # Using mpf strings to avoid float artifacts
    assert abs(op.DELTA_GAP - mpf('1.710035046742')) < mpf('1e-70')
    assert abs(op.GAMMA - mpf('16.339')) < mpf('1e-70')
    assert abs(op.NOISE_FLOOR - mpf('0.0171')) < mpf('1e-70')
    assert abs(op.KAPPA - mpf('0.5')) < mpf('1e-70')

def test_apply_n0():
    """Verify apply(0) returns Mass Gap (Delta)."""
    op = GeometricOperator()
    result = op.apply(0)
    assert abs(result - op.DELTA_GAP) < mpf('1e-70')

def test_apply_n1():
    """Verify apply(1) returns IR harmonic (Delta / Gamma)."""
    op = GeometricOperator()
    result = op.apply(1)
    expected = op.DELTA_GAP * (op.GAMMA ** -1)
    assert abs(result - expected) < mpf('1e-70')

def test_apply_n_neg1():
    """Verify apply(-1) returns UV harmonic (Delta * Gamma)."""
    op = GeometricOperator()
    result = op.apply(-1)
    expected = op.DELTA_GAP * op.GAMMA
    assert abs(result - expected) < mpf('1e-70')

def test_stress_test():
    """Verify stress_test distinguishes stable vs censored states."""
    op = GeometricOperator()

    # Stable: Energy > Noise Floor
    stable_energy = op.NOISE_FLOOR + mpf('0.0001')
    is_stable, msg = op.stress_test(stable_energy)
    assert is_stable is True
    assert "STABLE" in msg

    # Censored: Energy < Noise Floor
    censored_energy = op.NOISE_FLOOR - mpf('0.0001')
    is_stable, msg = op.stress_test(censored_energy)
    assert is_stable is False
    assert "CENSORED" in msg

def test_get_info():
    """Verify get_info returns correct dictionary structure."""
    op = GeometricOperator()
    info = op.get_info()

    assert isinstance(info, dict)
    assert "Delta_GeV" in info
    assert "Gamma" in info
    assert "Noise_Floor_GeV" in info
    assert "Version" in info

    # Verify values are floats (for JSON/logging compatibility)
    assert isinstance(info["Delta_GeV"], float)
    assert abs(info["Delta_GeV"] - float(op.DELTA_GAP)) < 1e-12

if __name__ == "__main__":
    # Manual execution if pytest is not available
    try:
        test_initialization()
        print("test_initialization passed")
        test_apply_n0()
        print("test_apply_n0 passed")
        test_apply_n1()
        print("test_apply_n1 passed")
        test_apply_n_neg1()
        print("test_apply_n_neg1 passed")
        test_stress_test()
        print("test_stress_test passed")
        test_get_info()
        print("test_get_info passed")
        print("All tests passed.")
    except AssertionError as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
