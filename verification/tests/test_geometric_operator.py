"""
Test Suite for GeometricOperator (modules/geometric_operator.py)
Tests initialization, apply methods, and stress test logic.
Ensures high precision (80 dps) and correct constant values.
"""
import pytest
from mpmath import mp, mpf
from modules.geometric_operator import GeometricOperator

# Local Precision - REQUIRED
mp.dps = 80

class TestGeometricOperator:

    def setup_method(self):
        self.op = GeometricOperator()

    def test_initialization(self):
        """Verify constants are initialized correctly with high precision."""
        expected_delta = mpf('1.710035046742')
        expected_gamma = mpf('16.339')
        expected_noise = mpf('0.0171')
        expected_kappa = mpf('0.5')

        # Since implementation uses string instantiation, exact equality should hold
        assert self.op.DELTA_GAP == expected_delta
        assert self.op.GAMMA == expected_gamma
        assert self.op.NOISE_FLOOR == expected_noise
        assert self.op.KAPPA == expected_kappa

    def test_apply_n0(self):
        """Verify apply(0) returns the base Mass Gap (Delta)."""
        result = self.op.apply(0)
        assert result == self.op.DELTA_GAP

    def test_apply_n1(self):
        """Verify apply(1) returns the first harmonic (Delta / Gamma)."""
        expected = self.op.DELTA_GAP / self.op.GAMMA
        result = self.op.apply(1)
        # Check within a very small tolerance appropriate for 80 dps
        assert abs(result - expected) < mpf('1e-75')

    def test_apply_n_negative(self):
        """Verify apply(-1) returns the UV state (Delta * Gamma)."""
        expected = self.op.DELTA_GAP * self.op.GAMMA
        result = self.op.apply(-1)
        assert abs(result - expected) < mpf('1e-75')

    def test_stress_test_stable(self):
        """Verify energy above Noise Floor is considered Stable."""
        energy = self.op.NOISE_FLOOR + mpf('0.0001')
        is_stable, message = self.op.stress_test(energy)
        assert is_stable is True
        assert "STABLE" in message

    def test_stress_test_censored(self):
        """Verify energy below Noise Floor is considered Censored."""
        energy = self.op.NOISE_FLOOR - mpf('0.0001')
        is_stable, message = self.op.stress_test(energy)
        assert is_stable is False
        assert "CENSORED" in message

    def test_get_info(self):
        """Verify get_info returns correct dictionary structure."""
        info = self.op.get_info()
        assert "Delta_GeV" in info
        assert "Gamma" in info
        assert "Noise_Floor_GeV" in info
        assert "Version" in info

        # Check values match float conversion (within float precision)
        assert info["Delta_GeV"] == float(self.op.DELTA_GAP)
        assert info["Gamma"] == float(self.op.GAMMA)
