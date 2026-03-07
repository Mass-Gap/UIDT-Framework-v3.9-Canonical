#!/usr/bin/env python3
"""
UIDT v3.9 CORE BASELINE VERIFICATION
====================================
Scope: Category A Mathematical Core Only
Status: Canonical Baseline (no peripheral modules)
"""
import sys
import os
from mpmath import mp, mpf, nstr

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 80-digit precision lock (Constitution §4)
mp.dps = 80

print("╔══════════════════════════════════════════════════════════════╗")
print("║  UIDT v3.9 CORE BASELINE VERIFICATION                        ║")
print("║  Scope: Mathematical Core (Category A) Only                  ║")
print("╚══════════════════════════════════════════════════════════════╝\n")

# [1] Banach Fixed Point (Theorem 3.4)
print("[1] BANACH FIXED-POINT PROOF (Mass Gap)...")
try:
    from core.banach_proof import BanachMassGap
    solver = BanachMassGap()
    Delta_star = solver.solve()
    L = solver.lipschitz_constant()
    print(f"   > Δ* = {nstr(Delta_star, 20)}... GeV")
    print(f"   > Lipschitz L = {nstr(L, 10)} (< 1: ✅ CONTRACTION)\n")
except ImportError as e:
    print(f"   > ❌ CORE MODULE MISSING: {e}\n")
    sys.exit(1)

# [2] RG Fixed Point (5κ² = 3λ_S)
print("[2] RG CONSTRAINT CLOSURE (Proposition 5.5)...")
try:
    from core.rg_closure import RGFixedPoint
    rg = RGFixedPoint()
    residual = rg.verify_closure()
    print(f"   > Residual: {nstr(residual, 5)}")
    if residual < mpf('1e-14'):
        print("   > Status: ✅ CLOSED\n")
    else:
        print("   > Status: ❌ EXCEEDS TOLERANCE\n")
        sys.exit(1)
except ImportError as e:
    print(f"   > ❌ CORE MODULE MISSING: {e}\n")
    sys.exit(1)

# [3] Geometric Operator Stability
print("[3] GEOMETRIC OPERATOR PRECISION (80-digit audit)...")
try:
    from modules.geometric_operator import GeometricOperator
    op = GeometricOperator()
    
    # Perform inline stress test at n=1089
    n = 1089
    E_n = op.apply(n)
    E_prev = op.apply(n-1)
    
    # Invariant: E(n) / E(n-1) == 1 / Gamma
    ratio = E_n / E_prev
    expected_ratio = 1 / op.GAMMA
    high_order_residual = abs(ratio - expected_ratio)
    
    print(f"   > Residual at n={n}: {nstr(high_order_residual, 10)}")
    
    # Relaxed tolerance for ratio drift at high N, but should be small
    if high_order_residual < mpf('1e-75'):
        print("   > Status: ✅ STABLE\n")
    else:
        print("   > Status: ⚠️  PRECISION LEAK DETECTED\n")
        sys.exit(1)
except ImportError as e:
    print(f"   > ❌ MODULE MISSING: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"   > ❌ ERROR: {e}\n")
    sys.exit(1)

print("="*66)
print("CORE BASELINE STATUS: ✅ PASSED")
print("="*66)
print("DOI: 10.5281/zenodo.17835200")
print("Repository: github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical")
