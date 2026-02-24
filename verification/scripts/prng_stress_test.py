#!/usr/bin/env python3
"""
UIDT PRNG Stress Test (mpmath @ 80 dps)
---------------------------------------
Checks for artifacts in the lower precision bits of mpmath random numbers.
Specifically targeted at verifying "noise quality" for HMC Lattice simulations.

Author: Philipp Rietz (via Jules)
Date: 2026-02-14
"""

import mpmath
from mpmath import mp
import numpy as np
from scipy import stats
import sys

def run_stress_test():
    print("="*60)
    print("UIDT PRNG STRESS TEST (mpmath @ 80 dps)")
    print("="*60)

    # 1. Set Precision
    print("[-] Setting mp.dps = 80 (Extreme Precision)...")
    mp.dps = 80

    # 2. Generate Samples
    N = 100000
    print(f"[-] Generating {N} random numbers using mp.rand()...")

    # Pre-allocate (for speed, though list comp is fine)
    samples = [mp.rand() for _ in range(N)]

    # 3. Test 1: Macro Uniformity (Full Range [0, 1))
    print("[-] Running Test 1: Macro Uniformity (KS Test)...")
    # Convert to float (lossy, but checks major structure)
    macro_vals = [float(x) for x in samples]
    ks_stat_macro, p_macro = stats.kstest(macro_vals, 'uniform')
    print(f"    > KS Statistic: {ks_stat_macro:.6f}")
    print(f"    > p-value:      {p_macro:.6e}")

    # 4. Test 2: Micro Uniformity (Digits > 40)
    print("[-] Running Test 2: Micro Uniformity (Digits > 40)...")
    # Extract fractional part of x * 10^40
    # x = 0.abcdef... -> x * 10^40 = abc...def.ghi...
    # (x * 10^40) % 1 = 0.ghi...
    scale = mp.mpf(10)**40
    micro_vals = []
    for x in samples:
        val = (x * scale) % 1
        micro_vals.append(float(val))

    ks_stat_micro, p_micro = stats.kstest(micro_vals, 'uniform')
    print(f"    > KS Statistic: {ks_stat_micro:.6f}")
    print(f"    > p-value:      {p_micro:.6e}")

    # 5. Test 3: Lag-1 Autocorrelation (Lattice Artifact Check)
    print("[-] Running Test 3: Lag-1 Autocorrelation (Micro Scale)...")
    arr_micro = np.array(micro_vals)
    mean = np.mean(arr_micro)
    var = np.var(arr_micro)

    # Calculate Lag-1 Autocorrelation
    # sum((x_i - mu)*(x_{i+1} - mu)) / ((N-1)*var)
    numerator = np.sum((arr_micro[:-1] - mean) * (arr_micro[1:] - mean))
    autocorr = numerator / ((N - 1) * var)

    # Z-score and p-value for autocorrelation (Standard Error ~ 1/sqrt(N))
    sigma = 1 / np.sqrt(N)
    z_score = autocorr / sigma
    p_autocorr = 2 * (1 - stats.norm.cdf(abs(z_score))) # Two-tailed test

    print(f"    > Autocorrelation: {autocorr:.6e}")
    print(f"    > Z-score:         {z_score:.4f}")
    print(f"    > p-value:         {p_autocorr:.6e}")

    # 6. Combined Confidence
    # Conservative approach: Minimum p-value dictates the "weakest link" confidence
    min_p = min(p_macro, p_micro, p_autocorr)

    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)

    status = "✅ PASSED (Noise Integrity Verified)"
    if min_p < 0.01:
        status = "❌ FAILED (Artifacts Detected)"
    elif min_p < 0.05:
        status = "⚠️ WARNING (Marginal Randomness)"

    print(f"Status: {status}")
    print(f"Statistical Confidence Level (p-value): {min_p:.6e}")
    print("="*60)

    # Special output for chat extraction
    print("\n--- CHAT OUTPUT BLOCK ---")
    print(f"Statistical Confidence Level (p-value): {min_p:.6e}")
    print("-------------------------")

if __name__ == "__main__":
    run_stress_test()
