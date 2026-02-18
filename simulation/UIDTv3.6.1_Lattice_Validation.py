#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.6.1 VALIDATION SUITE: MACHINE PRECISION
===============================================
Status: Canonical / Clean State / Final Fix
Description: Validates the Matrix Exponential using High-Order (8th)
             Scaling & Squaring. Achieves ~1e-15 accuracy.
"""

import numpy as np
from scipy.linalg import expm
import time

# =============================================================================
# 1. GPU/CPU CONFIGURATION
# =============================================================================
try:
    import cupy as cp
    from cupyx.scipy.linalg import expm as cupy_expm
    USE_CUPY = True
    print("✅ GPU Acceleration: ENABLED (CuPy detected)")
except ImportError:
    cp = None
    cupy_expm = None
    USE_CUPY = False
    print("⚠️ GPU Acceleration: DISABLED (Running on CPU)")

xp = cp if USE_CUPY else np
linalg_expm = cupy_expm if USE_CUPY else expm

def to_gpu(arr):
    return cp.asarray(arr) if USE_CUPY else arr

def to_cpu(arr):
    return arr.get() if USE_CUPY and hasattr(arr, 'get') else arr

# =============================================================================
# 2. HIGH-PRECISION ALGORITHM (Order 8 Taylor)
# =============================================================================
def su3_expm_scaled_taylor(A, xp_local=xp):
    """
    High-Precision SU(3) Exponential.
    Uses Scaling & Squaring with an 8th-order Taylor expansion base.
    This replaces the unstable trigonometric Cayley-Hamilton form for small norms.
    """
    # --- 1. Aggressive Scaling ---
    # Target norm < 0.05 with Order 8 implies error ~ 1e-18
    norms = xp_local.linalg.norm(A, axis=(-2,-1))
    max_norm = xp_local.max(norms)
    
    # Calculate required scaling steps s
    # 2^s > max_norm / 0.05
    s = 0
    target_norm = 0.05 
    if max_norm > target_norm:
        s = int(xp_local.ceil(xp_local.log2(max_norm / target_norm)))
    
    scale_factor = 2.0**s
    A_scaled = A / scale_factor

    # --- 2. 8th Order Taylor Expansion (Horner Scheme) ---
    # E = I + A + A^2/2! + ... + A^8/8!
    # Evaluated efficiently to minimize matrix multiplications.
    
    # Pre-compute powers
    A2 = xp_local.matmul(A_scaled, A_scaled)
    A4 = xp_local.matmul(A2, A2)
    
    # Constants
    c0 = 1.0
    c1 = 1.0
    c2 = 0.5
    c3 = 1.0/6.0
    c4 = 1.0/24.0
    c5 = 1.0/120.0
    c6 = 1.0/720.0
    c7 = 1.0/5040.0
    c8 = 1.0/40320.0
    
    I = xp_local.eye(3, dtype=complex)
    if A.ndim > 2:
        I = xp_local.broadcast_to(I, A.shape)

    # Horner-like Grouping for 8th Order:
    # E = (c0*I + c1*A + c2*A2 + c3*A3) + A4(c4*I + c5*A + c6*A2 + c7*A3 + c8*A4)
    # This reduces MatMuls compared to naive sum.
    
    # Odd terms help
    A3 = xp_local.matmul(A2, A_scaled)
    
    # Low part: I + A + A^2/2 + A^3/6
    Low = (c0 * I) + (c1 * A_scaled) + (c2 * A2) + (c3 * A3)
    
    # High part terms
    # Term 8: c8 * A4
    # Term 4..7 grouped
    
    # Optimized Summation:
    # High = c4*I + c5*A + c6*A2 + c7*A3 + c8*A4
    High = (c4 * I) + (c5 * A_scaled) + (c6 * A2) + (c7 * A3) + (c8 * A4)
    
    # Combine: E = Low + A4 * High
    E = Low + xp_local.matmul(A4, High)

    # --- 3. Squaring Step ---
    # Square result s times to reverse scaling
    for _ in range(s):
        E = xp_local.matmul(E, E)
        
    return E

# =============================================================================
# 3. VALIDATION CLASS
# =============================================================================

class UIDTValidator:
    def __init__(self):
        self.xp = xp
        
    def validate_cayley_hamiltonian(self, n_tests=1000):
        print(f"\n🔍 Validating Optimized Exponential (Order 8) vs Scipy (N={n_tests})")
        print("=" * 60)
        
        max_error = 0.0
        avg_error = 0.0
        
        t_custom_total = 0
        t_std_total = 0
        
        for i in range(n_tests):
            # 1. Random Anti-Hermitian Matrix
            A_real = np.random.randn(3, 3)
            A_imag = np.random.randn(3, 3)
            A_herm = (A_real + 1j*A_imag + (A_real - 1j*A_imag).T) / 2
            A_herm -= np.trace(A_herm) / 3 * np.eye(3)
            A_antiherm = 1j * A_herm 
            
            # Test with LARGE norm to force scaling loop to work hard
            scale = 5.0 # Norm ~ 15.0 -> requires ~9 squarings
            A_antiherm *= scale
            
            A_dev = to_gpu(A_antiherm)
            
            # 2. Benchmark Custom
            start = time.time()
            exp_custom = su3_expm_scaled_taylor(A_dev, xp_local=self.xp)
            if USE_CUPY: cp.cuda.Stream.null.synchronize()
            t_custom_total += time.time() - start
            
            # 3. Benchmark Standard
            start = time.time()
            exp_std = linalg_expm(A_dev)
            if USE_CUPY: cp.cuda.Stream.null.synchronize()
            t_std_total += time.time() - start
            
            # 4. Error Calc
            res_custom = to_cpu(exp_custom)
            res_std = to_cpu(exp_std)
            
            error = np.max(np.abs(res_custom - res_std))
            max_error = max(max_error, error)
            avg_error += error
        
        avg_error /= n_tests
        
        print(f"✅ Maximum Error: {max_error:.2e}")
        print(f"✅ Average Error: {avg_error:.2e}")
        print("-" * 60)
        print(f"⏱️  Time Custom Solver: {t_custom_total*1000:.2f} ms")
        print(f"⏱️  Time Standard expm: {t_std_total*1000:.2f} ms")
        
        if t_custom_total > 0:
            speedup = t_std_total / t_custom_total
            print(f"🚀 Speedup Factor:     {speedup:.2f}x (CPU/GPU dependent)")
        
        print("-" * 60)
        
        if max_error < 1e-14:
            print("🎉 PRECISION: PERFECT (Machine Epsilon).")
            print("   The algorithm is ready for high-precision production runs.")
        elif max_error < 1e-10:
            print("✅ PRECISION: EXCELLENT (< 1e-10).")
        else:
            print("⚠️  Warning: Precision drift detected.")

if __name__ == "__main__":
    validator = UIDTValidator()
    validator.validate_cayley_hamiltonian(n_tests=1000)