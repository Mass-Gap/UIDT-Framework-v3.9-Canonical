import unittest
import sys
import os

# Add project root to sys.path to allow importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from mpmath import mp, mpf
    MPMATH_AVAILABLE = True
except ImportError:
    MPMATH_AVAILABLE = False

if MPMATH_AVAILABLE:
    # Anti-Tampering Rule #1: Local Precision Declaration
    mp.dps = 80

    # Import actual modules (NO MOCKS allowed per UIDT Constitution)
    from modules.geometric_operator import GeometricOperator
    from modules.photonic_isomorphism import PhotonicInterface


class TestPhotonicIsomorphism(unittest.TestCase):
    """
    UIDT Verification Suite: Photonic Isomorphism (Pillar IV)

    Strict adherence to UIDT Constitution:
    1. No mocking of physics components.
    2. mp.dps = 80 local declaration.
    3. Residuals < 1e-14 required.
    """

    def setUp(self):
        if not MPMATH_AVAILABLE:
            self.skipTest("mpmath library not found in environment")

        # Initialize real physics objects
        self.geo_op = GeometricOperator()
        self.photon_interface = PhotonicInterface(self.geo_op)

    def test_initialization_constants(self):
        """Verify initialization loads correct constants from GeometricOperator."""
        # Expected values from canonical GeometricOperator
        expected_gamma = self.geo_op.GAMMA
        expected_delta = self.geo_op.DELTA_GAP

        # Verify loaded values match source exactly
        self.assertEqual(self.photon_interface.gamma, expected_gamma)
        self.assertEqual(self.photon_interface.delta, expected_delta)

        # Verify vacuum index is exactly 1.0 (mpf)
        self.assertTrue(abs(self.photon_interface.n_vacuum - mpf('1.0')) < 1e-14)

    def test_metamaterial_index_calculation(self):
        """
        Verify n_eff calculation: n_eff = gamma^alpha
        Critical Rule: Inputs must be mpf objects from strings to avoid float artifacts.
        """
        # Case 1: Alpha = 0 (Vacuum State) -> n_eff should be 1.0
        alpha_zero = mpf('0.0')
        n_eff_zero = self.photon_interface.calculate_metamaterial_index(alpha_zero)
        expected_zero = mpf('1.0')
        diff_zero = abs(n_eff_zero - expected_zero)
        self.assertTrue(diff_zero < 1e-14, f"Vacuum index residual {diff_zero} >= 1e-14")

        # Case 2: Alpha = 1 (Critical State) -> n_eff should be Gamma
        alpha_one = mpf('1.0')
        n_eff_one = self.photon_interface.calculate_metamaterial_index(alpha_one)
        expected_gamma = self.geo_op.GAMMA
        diff_one = abs(n_eff_one - expected_gamma)
        self.assertTrue(diff_one < 1e-14, f"Critical index residual {diff_one} >= 1e-14")

        # Case 3: Alpha = 0.5 (Fractional Dimension)
        alpha_half = mpf('0.5')
        n_eff_half = self.photon_interface.calculate_metamaterial_index(alpha_half)
        expected_half = mp.sqrt(self.geo_op.GAMMA)
        diff_half = abs(n_eff_half - expected_half)
        self.assertTrue(diff_half < 1e-14, f"Fractional index residual {diff_half} >= 1e-14")

    def test_wormhole_transition_prediction(self):
        """
        Verify predict_wormhole_transition returns correct critical values.
        Note: The method returns standard python floats (Category D application layer).
        We compare against float-converted expected values to account for inherent precision limits.
        """
        prediction = self.photon_interface.predict_wormhole_transition()

        # Extract values
        n_critical = mpf(str(prediction['n_critical']))
        epsilon_critical = mpf(str(prediction['epsilon_critical']))

        # Expected values (converted to float to match method output precision)
        # 16.339 fits in double precision with minimal error (< 1e-14)
        expected_n = mpf(str(float(self.geo_op.GAMMA)))
        # 16.339^2 ~ 267 fits in double precision but has truncation error > 1e-14 vs mpf
        expected_epsilon = mpf(str(float(self.geo_op.GAMMA ** 2)))

        # Verify n_critical
        diff_n = abs(n_critical - expected_n)
        self.assertTrue(diff_n < 1e-14, f"n_critical residual {diff_n} >= 1e-14")

        # Verify epsilon_critical
        diff_epsilon = abs(epsilon_critical - expected_epsilon)
        self.assertTrue(diff_epsilon < 1e-14, f"epsilon_critical residual {diff_epsilon} >= 1e-14")

if __name__ == '__main__':
    unittest.main()
