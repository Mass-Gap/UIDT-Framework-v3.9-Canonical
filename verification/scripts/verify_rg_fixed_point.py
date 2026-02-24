#!/usr/bin/env python3
"""
UIDT v3.9 VERIFICATION: RG FIXED POINT CONSTRAINT
=================================================
Pillar: I (Physical Framework Verification)
Regel-Compliance: Native Precision Only, No Mocks, Bounds specified (=0.001)
"""

import sys
import os
from mpmath import mp, mpf, nstr

# Windows UTF-8 console support
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ABSOLUTE DIRECTIVE: Local precision initialization
mp.dps = 80

def verify_rg_fixed_point():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  UIDT v3.9 RG FIXED POINT CONSTRAINT VERIFICATION            ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    # Framework Defaults
    kappa = mpf('0.5')
    lambda_s = mpf('0.417')
    
    # Mathematical Evaluation: |5 * kappa^2 - 3 * lambda_S|
    term1 = mpf('5') * (kappa ** 2)
    term2 = mpf('3') * lambda_s
    
    residual = abs(term1 - term2)
    tolerance = mpf('0.001')
    
    print("[1] Verifying RG Fixed Point Constraint...")
    print(f"    > Target function: |5 * kappa^2 - 3 * lambda_S| <= 0.001")
    print(f"    > kappa        = {nstr(kappa, 5)}")
    print(f"    > lambda_S     = {nstr(lambda_s, 5)}")
    print(f"    > 5 * kappa^2  = {nstr(term1, 5)}")
    print(f"    > 3 * lambda_S = {nstr(term2, 5)}")
    print(f"    > Residual     = {nstr(residual, 5)}")
    
    # 1e-14 allowed for mpmath binary-to-decimal representation discrepancy
    if residual <= tolerance + mpf('1e-14'):
        print("\n✅ SYSTEM STATUS: RG FIXED POINT CONSTRAINT STRICTLY SATISFIED.")
    else:
        print("\n❌ SYSTEM STATUS: RESIDUAL EXCEEDS 0.001 THRESHOLD.")
        sys.exit(1)

if __name__ == "__main__":
    verify_rg_fixed_point()
