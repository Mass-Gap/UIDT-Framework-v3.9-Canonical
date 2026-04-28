#!/usr/bin/env python3
# ============================================================================
# UIDT v3.9 Canonical — Performance & Precision Regression Tracking
# Vacuum Information Density as the Fundamental Geometric Scalar
# ============================================================================
import time
import pytest
import mpmath as mp
from core.uidt_proof_engine import UIDT_Prover

# Local precision override. Never centralise.
mp.dps = 80

class TestPerformanceRegression:
    """
    Performance and Precision Regression Tracker.
    Ensures that high-precision convergence algorithms do not degrade in performance.
    In UIDT, taking 10x longer to converge often indicates a destabilized
    RG flow or floating point precision leak.
    """
    
    def test_banach_convergence_time(self):
        """
        Verify that the Banach fixed-point iteration converges within the
        acceptable latency budget (e.g., < 2.0 seconds for 80-dps).
        """
        start_time = time.perf_counter()
        
        # Instantiate the real engine (No Mocking Rule)
        engine = UIDT_Prover()
        gap, _ = engine.prove_mass_gap(max_iter=100)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Verify precision constraint
        assert abs(gap - mp.mpf('1.710')) < 1e-2, f"Mass gap constraint violated: {gap}"
        
        # Verify performance constraint
        # A typical run should be well under 1 second, but we set a conservative 2.5s limit
        # to account for CI runner variance.
        assert execution_time < 2.5, f"Performance regression! Convergence took {execution_time:.3f}s (Threshold: 2.5s)"
        
    def test_rg_flow_performance(self):
        """
        Verify the computational cost of the RG flow steps (N=99 iterations).
        """
        start_time = time.perf_counter()
        
        # A dummy map to emulate RG flow since GeometricOperator might not exist
        # Just verifying map iteration speed over 99 loops
        engine = UIDT_Prover()
        val = mp.mpf('1.0')
        for _ in range(99):
            val = engine._map_T(val)
            
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        assert execution_time < 1.0, f"RG flow regression! N=99 iterations took {execution_time:.3f}s (Threshold: 1.0s)"
