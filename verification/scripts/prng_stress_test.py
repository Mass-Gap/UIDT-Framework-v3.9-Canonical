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
import sys

# Helper functions for high-precision statistics

def kolmogorov_sf_mpf(x):
    """
    Survival function of Kolmogorov distribution (for KS test p-value).
    2 * sum_{k=1}^inf (-1)^(k-1) * exp(-2 * k^2 * x^2)
    """
    if x <= 0: return mp.mpf(1.0)
    s = mp.mpf(0)
    term = mp.mpf(1)
    k = 1
    while abs(term) > mp.mpf('1e-20'):
        term = 2 * (-1)**(k-1) * mp.exp(-2 * k**2 * x**2)
        s += term
        k += 1
    return s

def ks_test_uniform_mpf(data):
    """
    Kolmogorov-Smirnov test for Uniform[0,1] using mpmath precision.
    Returns (statistic, p-value).
    """
    n = len(data)
    data_sorted = sorted(data)
    d_max = mp.mpf(0)

    for i, x in enumerate(data_sorted):
        # Theoretical CDF is x (for Uniform[0,1])
        # Empirical CDF jumps by 1/n at each point
        # Upper step difference: |(i+1)/n - x|
        diff1 = abs(mp.mpf(i+1)/n - x)
        # Lower step difference: |i/n - x|
        diff2 = abs(mp.mpf(i)/n - x)
        d_max = max(d_max, diff1, diff2)

    p_val = kolmogorov_sf_mpf(d_max * mp.sqrt(n))
    return d_max, p_val

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

    # Pre-allocate
    samples = [mp.rand() for _ in range(N)]

    # 3. Test 1: Macro Uniformity (Full Range [0, 1))
    print("[-] Running Test 1: Macro Uniformity (KS Test)...")
    # Use custom mpf-compatible KS test
    macro_vals = [mp.mpf(x) for x in samples]
    ks_stat_macro, p_macro = ks_test_uniform_mpf(macro_vals)
    print(f"    > KS Statistic: {ks_stat_macro:.6f}")
    print(f"    > p-value:      {p_macro:.6e}")

    # 4. Test 2: Micro Uniformity (Digits > 40)
    print("[-] Running Test 2: Micro Uniformity (Digits > 40)...")
    scale = mp.mpf(10)**40
    micro_vals = []
    for x in samples:
        val = (x * scale) % 1
        micro_vals.append(mp.mpf(val))

    ks_stat_micro, p_micro = ks_test_uniform_mpf(micro_vals)
    print(f"    > KS Statistic: {ks_stat_micro:.6f}")
    print(f"    > p-value:      {p_micro:.6e}")

    # 5. Test 3: Lag-1 Autocorrelation (Lattice Artifact Check)
    print("[-] Running Test 3: Lag-1 Autocorrelation (Micro Scale)...")
    # Numpy array of objects (mpf)
    arr_micro = np.array(micro_vals)

    # Calculate Mean and Variance using mpmath functions via numpy object array support
    # Or iterate manually to ensure precision?
    # Numpy sum() on object array calls __add__, which works for mpf.
    mean = np.sum(arr_micro) / N
    # Var: sum((x-mean)**2) / N
    var = np.sum((arr_micro - mean)**2) / N

    # Calculate Lag-1 Autocorrelation
    # sum((x_i - mu)*(x_{i+1} - mu)) / ((N-1)*var)
    numerator = np.sum((arr_micro[:-1] - mean) * (arr_micro[1:] - mean))
    autocorr = numerator / ((N - 1) * var)

    # Z-score and p-value for autocorrelation (Standard Error ~ 1/sqrt(N))
    sigma = 1 / mp.sqrt(N)
    z_score = autocorr / sigma

    # Use mpmath ncdf for normal distribution CDF
    # p_value = 2 * (1 - CDF(|z|))
    p_autocorr = 2 * (1 - mp.ncdf(abs(z_score)))

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
