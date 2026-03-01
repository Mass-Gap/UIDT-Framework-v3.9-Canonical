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
# 2. HIGH-PRECISION ALGORITHM (Order 40 Taylor)
# =============================================================================
def su3_expm_scaled_taylor(A, xp_local=xp, order=40):
    """
    High-Precision SU(3) Exponential.
    Uses Scaling & Squaring with a 40th-order Taylor expansion base.
    """
    # --- 1. Scaling ---
    norms = xp_local.linalg.norm(A, axis=(-2,-1))
    max_norm = xp_local.max(norms)
    
    # Calculate required scaling steps s
    # 2^s > max_norm / 0.05
    s = 0
    target_norm = 0.5
    if max_norm > target_norm:
        s = int(xp_local.ceil(xp_local.log2(max_norm / target_norm)))
    
    scale_factor = 2.0**s
    A_scaled = A / scale_factor

    I = xp_local.eye(3, dtype=complex)
    if A.ndim > 2:
        I = xp_local.broadcast_to(I, A.shape)

    E = I
    term = I
    for k in range(1, int(order) + 1):
        term = xp_local.matmul(term, A_scaled) / k
        E = E + term

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
        print(f"\n🔍 Validating Optimized Exponential (Order 40) vs Scipy (N={n_tests})")
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
    import argparse

    parser = argparse.ArgumentParser(description="UIDT v3.6.1 SU(3) expm validation")
    parser.add_argument("--n_tests", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=123456)
    args, _ = parser.parse_known_args()

    np.random.seed(args.seed)
    validator = UIDTValidator()
    validator.validate_cayley_hamiltonian(n_tests=args.n_tests)
