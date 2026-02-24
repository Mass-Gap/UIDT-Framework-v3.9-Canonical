"""
UIDT Verification Tests: Geometric Operator
============================================
Combined: Boundary Conditions + Stress Test (Noise Floor Censorship)
"""

import sys
import os
import pytest

# Inject project root for module resolution
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Core imports
try:
    from mpmath import mp, mpf
    # Set local precision as mandated by Constitution BEFORE importing module logic
    mp.dps = 80
    from modules.geometric_operator import GeometricOperator
except ImportError:
    # Environment missing mpmath - skip tests if run locally without dependencies
    pytest.skip("mpmath or modules not found - skipping verification tests", allow_module_level=True)


class TestGeometricOperator:
    """
    Verification suite for the Geometric Operator G^ in UIDT v3.8.
    Ensures mathematical closure and correct boundary conditions.
    """

    def setup_method(self):
        """Initialize the operator for each test."""
        # Enforce precision again to be safe against side effects
        mp.dps = 80
        self.operator = GeometricOperator()

    def test_apply_zero_mass_gap(self):
        """
        Test G^|0> = Delta (Mass Gap).
        Verifies Category A constant: Delta = 1.710 GeV.
        """
        n = 0
        expected = self.operator.DELTA_GAP
        actual = self.operator.apply(n)

        # Exact equality check for n=0 case
        # Note: apply(0) explicitly returns self.DELTA_GAP in the code
        assert actual == expected, f"G^|0> must return Delta exactly. Got {actual}"

        # Residual check (rigorous)
        residual = abs(expected - actual)
        assert residual < mpf('1e-14'), f"Residual {residual} exceeds 1e-14 tolerance"

    def test_apply_positive_harmonic_ir(self):
        """
        Test G^|n> for n > 0 (IR Harmonics).
        Example: n=1 (Vacuum/Muon scale).
        Formula: E_n = Delta * Gamma^(-n)
        """
        n = 1
        # Manual calculation with high precision
        # E = Delta * (Gamma ^ -1)
        expected = self.operator.DELTA_GAP * (self.operator.GAMMA ** (-n))
        actual = self.operator.apply(n)

        # Verification of decay
        assert actual < self.operator.DELTA_GAP, "IR state must have energy < Delta"

        # Closure check
        residual = abs(expected - actual)
        assert residual < mpf('1e-14'), f"IR Harmonic n={n} residual {residual} too high"

    def test_apply_negative_harmonic_uv(self):
        """
        Test G^|n> for n < 0 (UV States).
        Example: n=-1 (High Energy).
        Formula: E_n = Delta * Gamma^(-n) = Delta * Gamma^|n|
        """
        n = -1
        # Manual calculation with high precision
        # E = Delta * (Gamma ^ 1)
        expected = self.operator.DELTA_GAP * (self.operator.GAMMA ** (-n))
        actual = self.operator.apply(n)

        # Verification of growth
        assert actual > self.operator.DELTA_GAP, "UV state must have energy > Delta"

        # Closure check
        residual = abs(expected - actual)
        assert residual < mpf('1e-14'), f"UV Harmonic n={n} residual {residual} too high"

    def test_constants_integrity(self):
        """
        Verify immutable physical constants.
        Checks against canonical values defined in the Constitution.
        """
        # Category A: Mass Gap (Delta)
        # Value from Constitution/GeometricOperator: 1.710035046742
        canonical_delta = mpf('1.710035046742')
        assert abs(self.operator.DELTA_GAP - canonical_delta) < 1e-12, "Delta Gap integrity violation"

        # Category C: Gamma
        # Value from Constitution: 16.339
        canonical_gamma = mpf('16.339')
        assert abs(self.operator.GAMMA - canonical_gamma) < 1e-12, "Gamma integrity violation"


class TestGeometricOperatorStress:
    """
    Validates the Physical Stress Test logic (Pillar 0) with high precision.
    Ensures strict adherence to NOISE_FLOOR boundary conditions.
    """

    def setup_method(self):
        mp.dps = 80
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
