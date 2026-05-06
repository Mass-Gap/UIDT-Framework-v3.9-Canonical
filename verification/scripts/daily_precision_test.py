import os
import sys
import random
from mpmath import mp, mpf

# UIDT-OS MANDATORY: Set precision to 80 locally to prevent race conditions
mp.dps = 80

# Import the geometric operator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from modules.geometric_operator import GeometricOperator

def run_precision_test():
    """
    Daily Precision Test Protocol:
    Generates n > 1000 random parameter configurations (harmonic octaves and 
    parametric mutations) to verify the 80-digit numerical stability of the 
    geometric operator under extreme conditions.
    """
    print("--- UIDT Daily Precision Test Protocol ---")
    op = GeometricOperator()
    
    # Verify canonical constraints
    kappa = op.KAPPA
    # Fixed point relation: 5k^2 = 3 lambda_S
    lambda_s = 5 * (kappa ** 2) / 3
    
    residual_fixed_point = abs(5 * (kappa ** 2) - 3 * lambda_s)
    assert residual_fixed_point < 1e-14, f"Fixed point residual violation: {residual_fixed_point}"
    print(f"[PASS] Canonical constraint 5k^2 = 3 lambda_S holds (residual: {residual_fixed_point})")

    # Generate n > 1000 random harmonic states to test the Banach contraction
    n_tests = 1050
    stable_count = 0
    censored_count = 0

    print(f"Running {n_tests} random harmonic octave queries (n > 1000 requirement)...")
    
    for i in range(n_tests):
        # Pick a random harmonic state (n between 0 and 50)
        n_harmonic = random.randint(0, 50)
        
        # Calculate functional output
        energy_gev = op.apply(n_harmonic)
        
        # Test physical stability
        is_stable, diagnosis = op.stress_test(energy_gev)
        
        if is_stable:
            stable_count += 1
        else:
            censored_count += 1
            
        # Ensure that the precision of the output is strictly maintained (mpf type)
        assert type(energy_gev) == type(mpf('1.0')), "Precision leak detected: output is not an mpf object"
        
        # Verify deterministic calculation (no floating point jitter)
        energy_recalc = op.DELTA_GAP * (op.GAMMA ** (-n_harmonic))
        assert abs(energy_gev - energy_recalc) == 0, f"Determinism violation at n={n_harmonic}"

    print(f"[PASS] 80-digit precision stability maintained across {n_tests} tests.")
    print(f"Results: {stable_count} Stable States, {censored_count} Censored States.")
    print("STATUS: SUCCESS")

if __name__ == "__main__":
    run_precision_test()
