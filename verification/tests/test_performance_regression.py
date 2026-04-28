import sys
import os
import time
import pytest
from mpmath import mp, mpf

# Ensure UTF-8 output on Windows terminals
if sys.platform == "win32":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Path Resolution for UIDT-OS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.covariant_unification import CovariantUnification
from core.uidt_proof_engine import UIDT_Prover

def test_banach_convergence_performance():
    """
    Elite Tier Requirement: Banach convergence MUST be < 2.5s.
    This ensures the stability and efficiency of the core mathematical engine.
    """
    mp.dps = 80
    engine = UIDT_Prover()
    
    start_time = time.time()
    # Run the fixed-point iteration
    delta_star, L = engine.prove_mass_gap()
    end_time = time.time()
    
    duration = end_time - start_time
    print(f"\n[PERFORMANCE] Banach Convergence Time: {duration:.4f}s")
    print(f"[PERFORMANCE] Delta*: {float(delta_star):.6f} GeV")
    print(f"[PERFORMANCE] Lipschitz L: {float(L):.6e}")
    
    assert duration < 2.5, f"Performance regression detected! Convergence took {duration:.4f}s (limit: 2.5s)"
    assert delta_star > 0, "Non-physical delta_star detected."

def test_nlo_polarization_scaling():
    """
    Verifies the NLO polarization-corrected scaling logic.
    Reconciles S1-02: LO (N=99) vs NLO (N=94.05).
    """
    mp.dps = 80
    cu = CovariantUnification()
    
    rho_lo = cu.check_information_saturation_bound(mode='LO')
    rho_nlo = cu.check_information_saturation_bound(mode='NLO')
    
    ratio = rho_nlo / rho_lo
    expected_ratio = cu.GAMMA_UIDT ** (cu.NLO_STEPS - cu.RG_STEPS) # gamma^(94.05-99)
    
    print(f"\n[PHYSICS] LO Rho_max:  {float(rho_lo):.2e}")
    print(f"[PHYSICS] NLO Rho_max: {float(rho_nlo):.2e}")
    print(f"[PHYSICS] NLO/LO Ratio: {float(ratio):.6f}")
    
    # Residual check
    residual = abs(ratio - expected_ratio)
    assert residual < 1e-14, f"NLO scaling logic inconsistency. Residual: {residual}"

if __name__ == "__main__":
    # Allow manual execution
    import sys
    pytest.main([__file__])
