"""
UIDT v3.6.1 Proof Engine Test Suite
-----------------------------------
This test file verifies the core mathematical engine of the UIDT framework.
It adheres strictly to the canonical constants and precision requirements.

Directives:
1. NO MOCKING: Tests execute the actual deterministic mathematical logic.
2. PRECISION: mp.dps = 80 is set locally.
3. STRING INSTANTIATION: Tolerances are passed as strings to prevent float degradation.
4. SCENARIOS: Covers both convergence (happy path) and interrupted execution (edge case).

Author: Verification Engineer (AI)
"""

import sys
import os
import pytest
from mpmath import mp

# Add repo root to sys.path to allow importing core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from core.uidt_proof_engine import UIDT_Prover
except ImportError:
    # Fallback for when running from repo root
    sys.path.append(os.getcwd())
    from core.uidt_proof_engine import UIDT_Prover

# CRITICAL: Set local precision to 80 digits
mp.dps = 80

class TestUIDTProver:
    """
    Test Suite for UIDT_Prover (v3.6.1 Clean State)
    """

    def setup_method(self):
        """Initialize the prover before each test."""
        self.prover = UIDT_Prover()

    def test_initialization_constants(self):
        """
        Verify that the prover initializes with the correct canonical constants (Category A/C).
        Uses relative error for all floating-point comparisons to handle vastly different magnitudes.
        """
        # Expected values from v3.6.1 Canonical
        expected_Lambda = mp.mpf('1.000')
        expected_C = mp.mpf('0.277')
        expected_Kappa = mp.mpf('0.500')
        expected_m_S = mp.mpf('1.705')
        expected_rho_obs = mp.mpf('2.53e-47')
        expected_v_EW = mp.mpf('246.22')
        expected_M_Pl = mp.mpf('2.435e18')

        # Relative error tolerance
        rel_tol = mp.mpf('1e-14')

        # Assertions with relative error check: abs((actual - expected) / expected) < rel_tol
        assert abs((self.prover.Lambda - expected_Lambda) / expected_Lambda) < rel_tol
        assert abs((self.prover.C - expected_C) / expected_C) < rel_tol
        assert abs((self.prover.Kappa - expected_Kappa) / expected_Kappa) < rel_tol
        assert abs((self.prover.m_S - expected_m_S) / expected_m_S) < rel_tol
        assert abs((self.prover.rho_obs - expected_rho_obs) / expected_rho_obs) < rel_tol
        assert abs((self.prover.v_EW - expected_v_EW) / expected_v_EW) < rel_tol
        assert abs((self.prover.M_Pl - expected_M_Pl) / expected_M_Pl) < rel_tol

    def test_contraction_map_determinism(self):
        """
        Verify that the contraction map T(Delta) produces deterministic output.
        """
        # Test with a known input (e.g., m_S)
        input_val = self.prover.m_S
        output_val = self.prover._map_T(input_val)

        # Re-run to ensure determinism
        output_val_2 = self.prover._map_T(input_val)

        # Assert exact equality
        assert output_val == output_val_2

        # Sanity check: Output should be positive and greater than input (since alpha > 0)
        assert output_val > input_val

    def test_mass_gap_convergence(self):
        """
        Verify the convergence of the mass gap proof (Theorem 3.4).
        """
        # Execute proof with strict tolerance
        delta_star, L = self.prover.prove_mass_gap(max_iter=100, tol=mp.mpf('1e-60'))

        # Expected Mass Gap (approx 1.710 GeV)
        expected_delta = mp.mpf('1.710')

        # Assert close agreement (within tolerance for a proof)
        # Note: The exact value depends on the iteration, but should be close to 1.710
        assert abs(delta_star - expected_delta) < 0.01

        # Assert Lipschitz Constant < 1 (Contraction Condition)
        assert L < 1

    def test_interrupted_convergence(self):
        """
        Verify behavior when max_iter is reached before full convergence.
        """
        # Execute with only 1 iteration
        delta_star, L = self.prover.prove_mass_gap(max_iter=1, tol=mp.mpf('1e-60'))

        # Result should still be valid (float-like), just not fully converged
        assert delta_star > 0
        assert L > 0  # Lipschitz calculation still happens

    def test_vacuum_energy_validation(self):
        """
        Verify the vacuum energy calculation (Theorem 6.1).
        """
        # Use a fixed delta for this test to isolate the logic
        fixed_delta = mp.mpf('1.710')

        rho_phys, ratio = self.prover.prove_dark_energy(fixed_delta)

        # Expected ratio range (0.9 - 1.1) as defined in the prover
        assert 0.9 < ratio < 1.1

        # Verify rho_phys is positive
        assert rho_phys > 0

if __name__ == "__main__":
    # Allow running directly
    pytest.main([__file__])
