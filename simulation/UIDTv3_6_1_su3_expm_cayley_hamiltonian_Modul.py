#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.6.1 MODULE: SU(3) EXPONENTIAL SOLVER
============================================
Status: Canonical / Clean State
Description: Optimized matrix exponential for SU(3) via Cayley-Hamilton theorem.
             Includes Performance Benchmark.
"""

import numpy as np
from scipy.linalg import expm
import time

# Versuch, CuPy für GPU-Beschleunigung zu laden
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

# GPU/CPU Handling
xp = cp if USE_CUPY else np
linalg_expm = cupy_expm if USE_CUPY else expm

def su3_expm_cayley_hamiltonian(A, xp_local=xp):
    """
    GPU-optimierte SU(3) Exponentialfunktion via Cayley-Hamilton Theorem.
    """
    # Koeffizienten des charakteristischen Polynoms
    A2 = xp_local.matmul(A, A)
    tr_A2 = xp_local.trace(A2, axis1=-2, axis2=-1)
    
    c0 = xp_local.linalg.det(A)
    c1 = -0.5 * tr_A2
    
    # Norm & Winkel
    q = xp_local.sqrt(-c1 / 3.0 + 1e-15)
    q = q[..., xp_local.newaxis, xp_local.newaxis]
    c0 = c0[..., xp_local.newaxis, xp_local.newaxis]
    
    q3 = q**3
    arg = c0 / (2.0 * q3 + 1e-15)
    arg = xp_local.clip(arg, -1.0, 1.0)
    theta = xp_local.arccos(arg)
    
    # Analytische Koeffizienten
    theta_third = theta / 3.0
    cos_t3 = xp_local.cos(theta_third)
    sin_t3 = xp_local.sin(theta_third)
    sqrt3 = xp_local.sqrt(3.0)

    u0 = xp_local.exp(-2j * q * cos_t3)
    exp_plus = xp_local.exp(1j * q * (cos_t3 + sqrt3 * sin_t3))
    exp_minus = xp_local.exp(1j * q * (cos_t3 - sqrt3 * sin_t3))
    
    denom = 3 * q**2 + 1e-15
    u1 = (exp_plus + exp_minus - 2 * u0) / denom
    u2 = (exp_plus + exp_minus - u0) / denom

    # Identitätsmatrix
    I = xp_local.eye(3, dtype=complex)
    if A.ndim > 2:
        target_shape = A.shape
        I = xp_local.broadcast_to(I, target_shape)

    return u0 * I + u1 * A + u2 * A2

def su3_expm_hybrid(A, xp_local=xp):
    """Fallback-Wrapper"""
    try:
        return su3_expm_cayley_hamiltonian(A, xp_local)
    except Exception:
        if USE_CUPY and xp_local == cp:
            return cupy_expm(A)
        return expm(A)

# =============================================================================
# BENCHMARK TEST (Läuft nur bei direktem Start)
# =============================================================================
if __name__ == "__main__":
    print("\n🚀 CAYLEY-HAMILTON PERFORMANCE TEST")
    print("===================================")
    
    # 1. Testdaten generieren (10.000 Matrizen)
    N = 10000
    print(f"Generating {N} random anti-hermitian matrices...", end="")
    
    shape = (N, 3, 3)
    # Zufällige Anti-Hermitesche Matrizen (Generatoren von SU(3))
    R = xp.random.normal(0, 1, shape) + 1j * xp.random.normal(0, 1, shape)
    A = R - R.conj().swapaxes(-1, -2) # Anti-Hermitesch machen
    A = A - xp.trace(A, axis1=-2, axis2=-1)[..., None, None]/3 * xp.eye(3) # Spurlos machen
    print(" Done.")

    # 2. Benchmark Standard (Scipy/CuPy expm)
    print("\n1. Standard linalg.expm()...", end="")
    start = time.time()
    # Scipy expm ist oft nicht vektorisiert, wir loopen für fairen CPU Vergleich
    # oder nutzen cupy_expm wenn verfügbar
    if USE_CUPY:
        res_std = cupy_expm(A) # CuPy ist vektorisiert
    else:
        # Auf CPU müssen wir oft loopen, da scipy.linalg.expm nicht voll vektorisiert ist für (N,3,3)
        # Wir simulieren den Batch
        res_std = np.array([expm(m) for m in A])
        
    t_std = time.time() - start
    print(f" {t_std:.4f} sec")

    # 3. Benchmark Cayley-Hamilton
    print("2. UIDT Cayley-Hamilton...", end="")
    start = time.time()
    res_ch = su3_expm_cayley_hamiltonian(A)
    t_ch = time.time() - start
    print(f"   {t_ch:.4f} sec")
    
    # 4. Auswertung
    speedup = t_std / t_ch
    print(f"\n⚡ SPEEDUP: {speedup:.1f}x schneller")
    
    # Genauigkeits-Check
    diff = xp.mean(xp.abs(res_std - res_ch))
    print(f"🎯 Accuracy Error: {diff:.2e} (sollte sehr klein sein)")
    
    if diff < 1e-5:
        print("\n✅ TEST BESTANDEN: Algorithmus ist präzise und schnell.")
    else:
        print("\n⚠️ WARNUNG: Abweichung zu hoch!")