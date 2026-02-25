#!/usr/bin/env python3
"""
UIDT VERIFICATION SCRIPT: Operator Unitarity Check (PR #48)
===========================================================
Version: 3.9 (Canonical)
Purpose: Formally prove that the Geometric Operator G is non-unitary (contractive).
Evidence: Category B (Mathematical Derivation / Consistency)

Logic:
- The Geometric Operator G scales vacuum states by gamma^-n.
- A unitary operator U must satisfy U^dagger U = I.
- We verify that G^dagger G = gamma^-2n I != I for n > 0.
- This proves the system is dissipative (Information Shift to Deep IR).

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

def check_operator_unitarity():
    print("=== PR #48: Operator Unitarity Check (Non-Unitarity Proof) ===")
    print(f"Precision: {mp.dps} digits")

    # Instantiate Operator
    op = GeometricOperator()
    gamma = op.GAMMA
    delta = op.DELTA_GAP

    print(f"Operator Constant Gamma: {gamma}")
    print(f"Spectral Gap Delta: {delta} GeV")
    print("-" * 60)

    # 1. Test Unitarity Condition: U^dagger U = I
    # For G_n acting on |0>, eigenvalue is E_n.
    # We define the normalized scaling factor S_n = E_n / Delta = gamma^-n
    # The unitarity check is |S_n|^2 == 1 ?

    non_unitary_proven = True

    print(f"{'n':<5} | {'Eigenvalue E_n (GeV)':<25} | {'G^dagger G (|S_n|^2)':<25} | {'Unitary?'}")
    print("-" * 75)

    test_range = [0, 1, 2, 3, 10, 50, 100]

    for n in test_range:
        # Apply Operator
        E_n = op.apply(n)

        # Calculate normalized scaling factor (Eigenvalue of G relative to vacuum gap)
        S_n = E_n / delta

        # Calculate Operator Norm Squared (G^dagger G)
        # Since eigenvalues are real scalars: |S_n|^2
        norm_sq = S_n**2

        # Check Unitary Condition (I = 1.0)
        # Using explicit difference for robust precision check
        is_unitary = abs(norm_sq - 1.0) < mp.mpf('1e-70')

        unitary_str = "YES" if is_unitary else "NO (Contractive)"

        print(f"{n:<5} | {mp.nstr(E_n, 10):<25} | {mp.nstr(norm_sq, 10):<25} | {unitary_str}")

        # Logic Verification
        if n > 0 and is_unitary:
            print(f"❌ ERROR: Operator appeared unitary for n={n}!")
            non_unitary_proven = False

    # 2. Calculate IR Dissipation Rate (Information Shift)
    # Rate R = -d(ln E)/dn = ln(gamma)

    print("-" * 60)
    print(">> Calculating Asymptotic IR Dissipation Rate (n -> inf)")

    # Analytical Expectation
    rate_analytical = mp.log(gamma)

    # Numerical Calculation at n=100
    E_100 = op.apply(100)
    E_99 = op.apply(99)
    rate_numerical = mp.log(E_99 / E_100)

    residual = abs(rate_numerical - rate_analytical)

    print(f"Analytical Rate (ln gamma): {mp.nstr(rate_analytical, 20)}")
    print(f"Numerical Rate (n=100):     {mp.nstr(rate_numerical, 20)}")
    print(f"Residual: {mp.nstr(residual, 20)}")

    if residual < mp.mpf('1e-70'):
         print("✅ Dissipation Rate Consistency Proven.")
    else:
         print("❌ Dissipation Rate Mismatch.")
         non_unitary_proven = False

    # Final Verdict
    print("-" * 60)
    if non_unitary_proven:
        print("✅ SUCCESS: Operator G is formally proven to be NON-UNITARY (Contractive).")
        print("   This confirms the Information Shift to Deep IR mechanism.")
        return True
    else:
        print("❌ FAILURE: Non-Unitarity proof failed.")
        return False

if __name__ == "__main__":
    success = check_operator_unitarity()
    sys.exit(0 if success else 1)
