"""
UIDT VERIFICATION: Lattice Topology Test
=========================================
Version: 3.9 (Canonical Verification)
Context: Torsion Lattice & Vacuum Energy

Verifies the mathematical consistency of the Torsion Lattice module,
specifically the Vacuum Energy calculation and edge cases.

Precision: 80 digits (mpmath)
"""

import sys
import os
import unittest
from mpmath import mp, mpf

# Add repository root to sys.path to allow module imports
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if root_path not in sys.path:
    sys.path.append(root_path)

try:
    from modules.geometric_operator import GeometricOperator
    from modules.lattice_topology import TorsionLattice
except ImportError:
    # Fallback if modules not found as package
    sys.path.append(os.path.join(root_path, 'modules'))
    from geometric_operator import GeometricOperator
    from lattice_topology import TorsionLattice

mp.dps = 80

class TestLatticeTopology(unittest.TestCase):
    def setUp(self):
        # 1. PRECISION ENFORCEMENT (Anti-Tampering Rule #2)
        mp.dps = 80

        self.op = GeometricOperator()
        self.lattice = TorsionLattice(self.op)

    def test_calculate_vacuum_energy_zero_planck_mass(self):
        """
        Test that calculating vacuum energy with m_planck = 0 raises ZeroDivisionError.
        """
        v_ew = mpf('246.0')
        m_planck = mpf('0.0')

        with self.assertRaises(ZeroDivisionError):
            self.lattice.calculate_vacuum_energy(v_ew, m_planck)

if __name__ == '__main__':
    unittest.main()
