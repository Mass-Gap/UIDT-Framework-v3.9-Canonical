"""
UIDT Verification Test: Geometric Operator Stress Test
======================================================
Focus: Boundary Conditions for Noise Floor Censorship
"""

import sys
import os
import pytest
from mpmath import mp, mpf

# Explicit Precision Declaration (Local Scope Rule)
mp.dps = 80

# Add project root to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.geometric_operator import GeometricOperator

class TestGeometricOperatorStress:
    """
    Validates the Physical Stress Test logic (Pillar 0) with high precision.
    Ensures strict adherence to NOISE_FLOOR boundary conditions.
    """

    def setup_method(self):
        self.op = GeometricOperator()
        # Verify precision context is active
        assert mp.dps == 80

    def test_stress_test_censored(self):
        """Test energy strictly below noise floor is censored."""
        # NOISE_FLOOR is 0.0171
        energy = mpf('0.0170')
        result, message = self.op.stress_test(energy)

        assert result is False
        assert "CENSORED" in message
        assert f"{energy} GeV < Noise Floor" in message

    def test_stress_test_boundary(self):
        """Test energy exactly at noise floor is stable."""
        # NOISE_FLOOR is 0.0171
        energy = mpf('0.0171')
        result, message = self.op.stress_test(energy)

        assert result is True
        assert "STABLE" in message

    def test_stress_test_stable(self):
        """Test energy strictly above noise floor is stable."""
        # NOISE_FLOOR is 0.0171
        energy = mpf('0.0172')
        result, message = self.op.stress_test(energy)

        assert result is True
        assert "STABLE" in message

    def test_stress_test_high_precision_boundary(self):
        """Test extremely close values to verify precision handling."""
        noise_floor = self.op.NOISE_FLOOR
        epsilon = mpf('1e-75')

        # Slightly below
        energy_below = noise_floor - epsilon
        result_below, _ = self.op.stress_test(energy_below)
        assert result_below is False, f"Expected Censored for {energy_below}"

        # Slightly above
        energy_above = noise_floor + epsilon
        result_above, _ = self.op.stress_test(energy_above)
        assert result_above is True, f"Expected Stable for {energy_above}"
