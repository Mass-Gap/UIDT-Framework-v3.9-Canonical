
import unittest
import sys
from unittest.mock import MagicMock, patch

# Mock mpmath BEFORE importing anything else
# This is crucial because modules import mpmath at module level
mock_mp = MagicMock()
mock_mp.dps = 80
mock_mpf = MagicMock(side_effect=lambda x: float(x) if isinstance(x, (int, float, str)) else x)
mock_pi = 3.141592653589793

modules_mock = {
    'mpmath': MagicMock(mp=mock_mp, mpf=mock_mpf, pi=mock_pi),
    'mpmath.mp': mock_mp,
    'mpmath.mpf': mock_mpf,
}

# Apply the mock to sys.modules
with patch.dict(sys.modules, modules_mock):
    # Now we can import the modules
    # Assuming running from repo root
    sys.path.append('.')
    try:
        from modules.geometric_operator import GeometricOperator
        from modules.lattice_topology import TorsionLattice
    except ImportError:
        # Fallback if running from tests/ directory
        sys.path.append('..')
        from modules.geometric_operator import GeometricOperator
        from modules.lattice_topology import TorsionLattice

class TestTorsionConsistency(unittest.TestCase):
    def setUp(self):
        self.op = GeometricOperator()
        self.lattice = TorsionLattice(self.op)

    def test_torsion_energy_constant(self):
        """
        Verify that Torsion Energy E_T is strictly 2.44 MeV.
        Boundary: Do NOT alter Category A or C constants.
        """
        # E_T = 2.44 MeV = 0.00244 GeV
        expected_et_mev = 2.44
        expected_et_gev = 0.00244

        # Convert to float because it's a mocked mpf
        actual_et_gev = float(self.lattice.TORSION_ENERGY_GEV)

        self.assertAlmostEqual(actual_et_gev, expected_et_gev, places=5,
                               msg=f"Torsion energy E_T must be {expected_et_gev} GeV (2.44 MeV)")

    def test_vacuum_frequency_correction(self):
        """
        Verify f_vac calculation logic: f_vac = (Delta / gamma) + E_torsion
        """
        # Values from code (float approximation)
        delta = 1.710035046742
        gamma = 16.339
        torsion_gev = 0.00244

        base_freq = delta / gamma
        expected_freq = base_freq + torsion_gev

        # Calculate using the class method
        actual_freq = float(self.lattice.get_corrected_vacuum_frequency())

        self.assertAlmostEqual(actual_freq, expected_freq, places=5,
                               msg="Corrected vacuum frequency logic mismatch")

    def test_overlap_shift(self):
        """
        Verify Overlap Shift constant 1/2.302
        """
        expected_shift = 1.0 / 2.302
        actual_shift = float(self.lattice.OVERLAP_SHIFT)
        self.assertAlmostEqual(actual_shift, expected_shift, places=5,
                               msg="Overlap shift constant mismatch")

    def test_holographic_folding_factor(self):
        """
        Verify Folding Factor 2^34.58
        """
        expected_folding = 2 ** 34.58
        actual_folding = float(self.lattice.FOLDING_FACTOR)
        self.assertAlmostEqual(actual_folding, expected_folding, places=2,
                               msg="Folding factor logic mismatch")

if __name__ == '__main__':
    unittest.main()
