#!/usr/bin/env python3
"""
UIDT VERIFICATION SCRIPT: Geometric Operator Stresstest (PR #51)
================================================================
Version: 3.9 (Canonical)
Purpose: Stress test the Geometric Operator under extreme boundary conditions.
Evidence: Category B (Numerical Stability / Thermodynamic Limit)

Logic:
- Apply Operator G for N -> 10000 iterations (Thermodynamic Limit).
- Verify numerical precision (Float Degradation Check).
- Ensure Scaling Ratio is invariant: E(n)/E(n-1) == 1/gamma.

Precision: 80 digits (mpmath)
"""

import sys
import os

# Ensure modules are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from mpmath import mp
from modules.geometric_operator import GeometricOperator

# --- Anti-Tampering Rule: Local Precision ---
mp.dps = 80

def run_stresstest():
    print("=== PR #51: Geometric Operator Stresstest (Thermodynamic Limit N=10000) ===")
    print(f"Precision: {mp.dps} digits")

    op = GeometricOperator()
    gamma = op.GAMMA
    inv_gamma = 1 / gamma

    print(f"Gamma: {gamma}")
    print(f"Target Ratio (1/gamma): {inv_gamma}")
    print("-" * 60)

    limit_n = 10000
    checkpoints = [10, 100, 1000, 5000, 10000]

    prev_E = op.apply(0)
    max_drift = mp.mpf('0.0')

    print("Iterating...")

    for n in range(1, limit_n + 1):
        E_n = op.apply(n)

        # Calculate Ratio
        ratio = E_n / prev_E

        # Check Drift
        drift = abs(ratio - inv_gamma)
        if drift > max_drift:
            max_drift = drift

        # Update
        prev_E = E_n

        # Checkpoint Reporting
        if n in checkpoints:
            print(f"n={n:<5} | E_n = {mp.nstr(E_n, 10):<20} | Max Drift = {mp.nstr(max_drift, 20)}")

        # Check for Numerical Collapse (Underflow to strict zero)
        if E_n == 0:
            print(f"❌ FAILURE: Numerical Underflow at n={n}. Precision insufficient.")
            return False

    print("-" * 60)
    print(f"Final Max Drift: {max_drift}")

    # Strict tolerance check (should be near machine epsilon for 80 dps)
    tolerance = mp.mpf('1e-75')

    if max_drift < tolerance:
        print("✅ SUCCESS: Geometric Operator stable in Thermodynamic Limit.")
        print("   No Float Degradation detected.")
        return True
    else:
        print(f"❌ FAILURE: Float Degradation detected (Drift > {tolerance}).")
        return False

if __name__ == "__main__":
    success = run_stresstest()
    sys.exit(0 if success else 1)
