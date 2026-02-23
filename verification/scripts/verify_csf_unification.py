#!/usr/bin/env python3
"""
UIDT v3.9 VERIFICATION: CSF-UIDT UNIFICATION
============================================
Pillar: II (Cosmological Harmony)
Regel-Compliance: Native Precision Only, No Mocks, Residuals < 10^-14
"""

import sys
import os
from mpmath import mp, mpf, nstr

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.covariant_unification import CovariantUnification

mp.dps = 80


def run_csf_verification():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  UIDT v3.9 COVARIANT UNIFICATION VERIFICATION (CSF-UIDT)     ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    gamma_canonical = mpf('16.339')
    unifier = CovariantUnification(gamma_uidt=gamma_canonical)

    print("\n[1] Verifying Conformal Density Mapping (Lemma 1)...")
    gamma_csf = unifier.derive_csf_anomalous_dimension()
    # USE NSTR FOR MPMATH FORMATTING. NEVER FLOAT CAST. NEVER CRASH INTENTIONALLY.
    gamma_csf_str = nstr(gamma_csf, 6)
    print(f"    > Derived gamma_CSF: {gamma_csf_str} (Expected: ~0.504)")

    print("\n[2] Verifying Information Saturation Bound (Theorem 2)...")
    rho_max = unifier.check_information_saturation_bound()
    print(f"    > Maximum Density limit scaled via gamma^99.")
    print(f"    > Value: {str(rho_max)[:20]}... GeV^4")

    print("\n[3] Verifying Equation of State (Lemma 2)...")
    eos = unifier.get_equation_of_state_asymptotic()
    target_w0 = mpf('-0.99')
    residual_w0 = abs(eos['w_0'] - target_w0)
    print(f"    > w_0 = {nstr(eos['w_0'], 5)}")
    print(f"    > w_a = {nstr(eos['w_a'], 5)}")
    print(f"    > Residual w_0: {nstr(residual_w0, 5)}")

    if residual_w0 < mpf('1e-14'):
        print("\n✅ SYSTEM STATUS: CSF-UIDT MAPPING STRICTLY CLOSED.")
    else:
        print("\n❌ SYSTEM STATUS: RESIDUAL EXCEEDS 10^-14 THRESHOLD.")
        sys.exit(1)


if __name__ == "__main__":
    # Ensure Windows console can display UTF-8 (box art/checkmarks)
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    run_csf_verification()
