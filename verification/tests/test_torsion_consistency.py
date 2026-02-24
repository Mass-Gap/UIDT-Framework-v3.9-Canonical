"""
UIDT VERIFICATION: Torsion Consistency Test
===========================================
Version: 3.9 (Canonical Verification)
Context: Torsion Lattice & Vacuum Frequency

Verifies the mathematical consistency of the Torsion Lattice module,
specifically the Torsion Energy (E_T) and Vacuum Frequency calculations.

Precision: 80 digits (mpmath)
"""

import sys
import os
import unittest
from mpmath import mp, mpf

# Add repository root to sys.path to allow module imports
# Assumes structure: root/verification/tests/this_file.py
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

class TestTorsionConsistency(unittest.TestCase):
    def setUp(self):
        # 1. PRECISION ENFORCEMENT (Anti-Tampering Rule #2)
        mp.dps = 80

        self.op = GeometricOperator()
        self.lattice = TorsionLattice(self.op)

        # Canonical Constants (Category C)
        self.E_T_TARGET = mpf('0.00244')  # 2.44 MeV = 0.00244 GeV

    def test_torsion_energy_constant(self):
        """
        Verify that the Torsion Binding Energy matches the canonical value.
        Category C: E_T = 2.44 MeV
        """
        mp.dps = 80
        e_t_actual = self.lattice.TORSION_ENERGY_GEV
        residual = abs(e_t_actual - self.E_T_TARGET)

        # Strict equality check for defined constants
        self.assertTrue(residual < 1e-14, f"E_T mismatch: {e_t_actual} != {self.E_T_TARGET} (Res: {residual})")

    def test_vacuum_frequency_derivation(self):
        """
        Verify the derivation of the 'Baddewithana Frequency'.
        Formula: f_vac = (Delta / gamma) + E_torsion
        Target: ~107.1 MeV
        """
        mp.dps = 80

        # Calculate expected frequency manually
        delta = self.op.DELTA_GAP
        gamma = self.op.GAMMA
        e_t = self.E_T_TARGET

        f_expected = (delta / gamma) + e_t
        f_actual = self.lattice.calculate_vacuum_frequency()

        residual = abs(f_actual - f_expected)

        self.assertTrue(residual < 1e-14, f"Vacuum Frequency mismatch. Res: {residual}")

        # Verify it is approximately 107.1 MeV
        f_mev = f_actual * 1000
        # 1.710035... / 16.339 + 0.00244 = 0.104659... + 0.00244 = 0.107099... -> 107.1 MeV
        self.assertTrue(107.0 < f_mev < 107.2, f"Frequency out of range: {f_mev} MeV")

    def test_lattice_folding_factor(self):
        """
        Verify the Lattice Folding Factor calculation.
        Factor = 2^(34.58)
        """
        mp.dps = 80
        expected_factor = mpf('2') ** mpf('34.58')
        actual_factor = self.lattice.FOLDING_FACTOR

        residual = abs(actual_factor - expected_factor)
        self.assertTrue(residual < 1e-14, f"Folding Factor mismatch. Res: {residual}")

if __name__ == '__main__':
    unittest.main()
