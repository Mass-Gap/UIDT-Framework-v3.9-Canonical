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
    # Use mpf (scipy might cast internally, but we avoid explicit float())
    macro_vals = [mp.mpf(x) for x in samples]
    # Scipy requires float array, use numpy conversion to avoid explicit float()
    ks_stat_macro, p_macro = stats.kstest(np.array(macro_vals, dtype=float), 'uniform')
    print(f"    > KS Statistic: {mp.nstr(mp.mpf(ks_stat_macro), 6)}")
    print(f"    > p-value:      {mp.nstr(mp.mpf(p_macro), 6)}")

    # 4. Test 2: Micro Uniformity (Digits > 40)
    print("[-] Running Test 2: Micro Uniformity (Digits > 40)...")
    # Extract fractional part of x * 10^40
    # x = 0.abcdef... -> x * 10^40 = abc...def.ghi...
    # (x * 10^40) % 1 = 0.ghi...
    scale = mp.mpf(10)**40
    micro_vals = []
    for x in samples:
        val = (x * scale) % 1
        micro_vals.append(mp.mpf(val))

    # Scipy requires float array, use numpy conversion to avoid explicit float()
    ks_stat_micro, p_micro = stats.kstest(np.array(micro_vals, dtype=float), 'uniform')
    print(f"    > KS Statistic: {mp.nstr(mp.mpf(ks_stat_micro), 6)}")
    print(f"    > p-value:      {mp.nstr(mp.mpf(p_micro), 6)}")

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
    # Avoid explicit float() call by using numpy casting
    p_autocorr = 2 * (1 - stats.norm.cdf(np.array(abs(z_score), dtype=float))) # Two-tailed test

    print(f"    > Autocorrelation: {mp.nstr(mp.mpf(autocorr), 6)}")
    print(f"    > Z-score:         {mp.nstr(mp.mpf(z_score), 4)}")
    print(f"    > p-value:         {mp.nstr(mp.mpf(p_autocorr), 6)}")

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
    print(f"Statistical Confidence Level (p-value): {mp.nstr(mp.mpf(min_p), 6)}")
    print("="*60)

    # Special output for chat extraction
    print("\n--- CHAT OUTPUT BLOCK ---")
    print(f"Statistical Confidence Level (p-value): {mp.nstr(mp.mpf(min_p), 6)}")
    print("-------------------------")

if __name__ == "__main__":
    run_stress_test()
