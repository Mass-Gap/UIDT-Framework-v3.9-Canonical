import unittest
import sys
import os
import mpmath
from mpmath import mp

# Add script directory to path to import the function
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "scripts"))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

if SCRIPTS_PATH not in sys.path:
    sys.path.insert(0, SCRIPTS_PATH)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from UIDT_Master_Verification import solve_exact_cubic_v, C_GLUON_FLOAT, LAMBDA_FLOAT

class TestSolveExactCubicV(unittest.TestCase):
    def setUp(self):
        # Set high precision for mpmath checks
        mp.dps = 80

    def test_happy_path(self):
        """Test with canonical parameters (m_S=1.705, kappa=0.500, lambda_S=0.417)"""
        m_S = 1.705
        kappa = 0.500
        lambda_S = 0.417

        v = solve_exact_cubic_v(m_S, lambda_S, kappa)

        # Verify it's a root of the equation using mpmath for high-precision residual
        # m_S^2 * v + lambda_S * v^3 / 6 - kappa * C / Lambda = 0
        v_mp = mp.mpf(v)
        m_S_mp = mp.mpf(m_S)
        lambda_S_mp = mp.mpf(lambda_S)
        kappa_mp = mp.mpf(kappa)
        C_mp = mp.mpf(C_GLUON_FLOAT)
        L_mp = mp.mpf(LAMBDA_FLOAT)

        residual = m_S_mp**2 * v_mp + (lambda_S_mp * v_mp**3)/6 - (kappa_mp * C_mp)/L_mp

        # Ensure mathematical exactness up to floating constraints
        self.assertLess(abs(residual), mp.mpf('1e-14'), f"Residual too high: {residual}")

        # Check against canonical VEV (~47.7 MeV)
        self.assertLess(abs(v_mp * mp.mpf('1000') - mp.mpf('47.7')), mp.mpf('0.5'), 
                        f"Expected approx 47.7 MeV, got {v*1000}")

    def test_lambda_zero(self):
        """Test edge case lambda_S = 0 (Linear equation)"""
        m_S = 1.705
        kappa = 0.500
        lambda_S = 0.0

        # Mathematical expectation: v = (kappa * C) / (Lambda * m_S**2)
        expected_v = (kappa * C_GLUON_FLOAT) / (LAMBDA_FLOAT * m_S**2)
        v = solve_exact_cubic_v(m_S, lambda_S, kappa)
        
        expected_v_mp = mp.mpf(expected_v)
        v_mp = mp.mpf(v)

        self.assertLess(abs(v_mp - expected_v_mp), mp.mpf('1e-14'),
                        msg=f"Expected {expected_v}, got {v}. Linear solution failed.")

    def test_kappa_zero(self):
        """Test edge case kappa = 0 (No gluon coupling)"""
        # If kappa is 0, v=0 should be a root
        v = solve_exact_cubic_v(1.705, 0.417, 0.0)
        self.assertLess(abs(mp.mpf(v)), mp.mpf('1e-14'))

    def test_numerical_stability_small_lambda(self):
        """Test numerical stability with very small lambda_S"""
        m_S = 1.705
        kappa = 0.500
        lambda_S = 1e-10

        v = solve_exact_cubic_v(m_S, lambda_S, kappa)

        v_mp = mp.mpf(v)
        m_S_mp = mp.mpf(m_S)
        lambda_S_mp = mp.mpf(lambda_S)
        kappa_mp = mp.mpf(kappa)
        C_mp = mp.mpf(C_GLUON_FLOAT)
        L_mp = mp.mpf(LAMBDA_FLOAT)

        residual = m_S_mp**2 * v_mp + (lambda_S_mp * v_mp**3)/6 - (kappa_mp * C_mp)/L_mp
        self.assertLess(abs(residual), mp.mpf('1e-14'))

if __name__ == '__main__':
    unittest.main()
