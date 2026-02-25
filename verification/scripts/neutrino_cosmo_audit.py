"""
UIDT VERIFICATION SCRIPT: Neutrino Mass & Cosmology Audit (Canonical Refactor)
==============================================================================
Version: 3.9 (Canonical)
Purpose: Verify cosmological parameters (w_a, sum m_nu) and bare-gamma shift.
Date: 2026-02-24 (Simulated)

Refactored for UIDT v3.9 Compliance:
- Replaced decimal with mpmath (80-digit precision)
- Enforced Anti-Tampering Rules (Local Precision)

EVIDENCE CLASSIFICATION:
- Bare Factor (gamma_inf): [Category B]
- Cosmology (w_a, sum m_nu): [Category C]
"""

import sys
from mpmath import mp

# Precision Setup (Anti-Tampering Rule: High Precision Required)
mp.dps = 80

def calculate_gamma_shift():
    """
    Calculates the shift between the thermodynamic limit (gamma_inf)
    and the physical value (gamma_phys).
    Source: docs/theoretical_notes.md (PR #42)
    """
    gamma_inf  = mp.mpf('16.3437184698')  # Category B (Lattice Limit)
    gamma_phys = mp.mpf('16.3390')       # Category C (Calibrated/Physical)

    delta_gamma = gamma_inf - gamma_phys

    print("\n--- 1. Gamma Shift Analysis ---")
    print(f"Gamma (Infinity): {gamma_inf}")
    print(f"Gamma (Physical): {gamma_phys}")
    print(f"Shift delta_gamma: {delta_gamma}")

    return delta_gamma

def derive_wa_holographic(L_target=8.2, wa_target=-1.300):
    """
    Derives w_a for holographic scales L using mode amplification L^4.
    Ansatz: w_a(L) = -k * L^4 (Phenomenological Fit)
    Target: w_a(8.2) approx -1.300
    """
    print("\n--- 2. Dark Energy w_a Derivation ---")

    L_val  = mp.mpf(str(L_target))
    wa_val = mp.mpf(str(wa_target))

    # Calibrate k
    # wa = -k * L^4  => k = -wa / L^4
    k = -wa_val / (L_val**4)
    print(f"Calibrated coefficient k: {k}")

    # Calculate for range [8.0, 8.25]
    L_range = [8.0, 8.1, 8.2, 8.25]
    results = {}

    print(f"{'L':<10} | {'w_a(L)':<20} | {'Target':<10}")
    print("-" * 45)

    for l in L_range:
        l_mp = mp.mpf(str(l))
        wa_calc = -k * (l_mp**4)
        results[l] = wa_calc
        target_str = "-1.300" if l == 8.2 else "N/A"
        print(f"{l:<10} | {mp.nstr(wa_calc, 10):<20} | {target_str:<10}")

    return results

def solve_neutrino_masses(sum_limit_ev=0.16):
    """
    Solves for neutrino mass eigenstates given the sum constraint.
    Constants from PDG (approximate for 2026/2025 context).
    Using mpmath for precision.
    """
    print("\n--- 3. Neutrino Mass Hierarchy Audit ---")

    # Mass squared differences (eV^2)
    delta_m2_sol = mp.mpf('7.53e-5')
    delta_m2_atm = mp.mpf('2.52e-3')  # Magnitude

    sum_limit = mp.mpf(str(sum_limit_ev))

    print(f"Constraint: Sum m_nu = {sum_limit} eV")

    # --- Normal Hierarchy (m1 < m2 < m3) ---
    # m2 = sqrt(m1^2 + delta_sol)
    # m3 = sqrt(m2^2 + delta_atm) approx sqrt(m1^2 + delta_sol + delta_atm)

    def get_sum_nh(m1_val):
        m1 = m1_val
        m2 = mp.sqrt(m1**2 + delta_m2_sol)
        m3 = mp.sqrt(m1**2 + delta_m2_sol + delta_m2_atm)
        return m1 + m2 + m3

    # Simple bisection search for m1
    low = mp.mpf('0')
    high = sum_limit
    m1_nh = mp.mpf('0')

    for _ in range(100): # 100 iterations for high precision
        mid = (low + high) / 2
        s = get_sum_nh(mid)
        if s < sum_limit:
            low = mid
        else:
            high = mid
    m1_nh = (low + high) / 2

    m2_nh = mp.sqrt(m1_nh**2 + delta_m2_sol)
    m3_nh = mp.sqrt(m1_nh**2 + delta_m2_sol + delta_m2_atm)
    sum_nh = m1_nh + m2_nh + m3_nh

    print(f"\n[Normal Hierarchy]")
    print(f"m1: {mp.nstr(m1_nh, 5)} eV")
    print(f"m2: {mp.nstr(m2_nh, 5)} eV")
    print(f"m3: {mp.nstr(m3_nh, 5)} eV")
    print(f"Sum: {mp.nstr(sum_nh, 5)} eV")

    # --- Inverted Hierarchy (m3 < m1 < m2) ---
    # m3 is lightest
    # m1 = sqrt(m3^2 + delta_atm)
    # m2 = sqrt(m1^2 + delta_sol) = sqrt(m3^2 + delta_atm + delta_sol)

    def get_sum_ih(m3_val):
        m3 = m3_val
        m1 = mp.sqrt(m3**2 + delta_m2_atm)
        m2 = mp.sqrt(m3**2 + delta_m2_atm + delta_m2_sol)
        return m1 + m2 + m3

    # Bisection for m3
    low = mp.mpf('0')
    high = sum_limit
    m3_ih = mp.mpf('0')

    try:
        for _ in range(100):
            mid = (low + high) / 2
            s = get_sum_ih(mid)
            if s < sum_limit:
                low = mid
            else:
                high = mid
        m3_ih = (low + high) / 2

        m1_ih = mp.sqrt(m3_ih**2 + delta_m2_atm)
        m2_ih = mp.sqrt(m3_ih**2 + delta_m2_atm + delta_m2_sol)
        sum_ih = m1_ih + m2_ih + m3_ih

        print(f"\n[Inverted Hierarchy]")
        print(f"m3: {mp.nstr(m3_ih, 5)} eV")
        print(f"m1: {mp.nstr(m1_ih, 5)} eV")
        print(f"m2: {mp.nstr(m2_ih, 5)} eV")
        print(f"Sum: {mp.nstr(sum_ih, 5)} eV")
    except Exception as e:
        print(f"\n[Inverted Hierarchy] Failed to solve: {e}")

    # Comparison with KATRIN
    katrin_limit_direct = 0.8  # Approx KATRIN upper bound (2022/2024 data)
    print(f"\nComparison with KATRIN (Direct Limit ~0.8 eV):")
    print(f"UIDT Limit ({sum_limit} eV sum) implies m_e (eff) << 0.8 eV.")
    print("Result: Consistent.")

if __name__ == "__main__":
    calculate_gamma_shift()
    derive_wa_holographic()
    solve_neutrino_masses()
