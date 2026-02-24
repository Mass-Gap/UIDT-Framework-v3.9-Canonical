#!/usr/bin/env python3
"""
UIDT v3.9 CSF-UIDT UNIFICATION VERIFICATION (Pillar II-CSF)
=============================================================
Evidence Category: [C] for all CSF outputs.
Limitations: L4 (gamma calibrated, not RG-derived), L5 (N=99 empirical).

Verifies:
  1. Conformal Density Mapping (gamma_CSF derivation)
  2. Information Saturation Bound (rho_max computation)
  3. Equation of State consistency (residual < 1e-14)
"""

import sys
import os
from mpmath import mp, mpf, nstr

# Set precision locally
mp.dps = 80

# Path injection (same pattern as UIDT_Master_Verification.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.covariant_unification import CovariantUnification


def run_csf_verification():
    print("=" * 64)
    print("  UIDT v3.9 CSF-UIDT UNIFICATION VERIFICATION")
    print("  Evidence Category: [C] (Phenomenological)")
    print("=" * 64)

    cu = CovariantUnification(gamma_uidt=mpf('16.339'))
    all_passed = True

    # ------------------------------------------------------------------
    # Check 1: Conformal Density Mapping
    # ------------------------------------------------------------------
    print("\n[Check 1] Conformal Density Mapping (gamma_CSF) [C]...")
    gamma_csf = cu.derive_csf_anomalous_dimension()
    # USE NSTR FOR MPMATH FORMATTING. NEVER FLOAT CAST.
    gamma_csf_str = nstr(gamma_csf, 6)
    print(f"  gamma_CSF = {gamma_csf_str}")
    print(f"  Evidence:   [C] — phenomenological mapping from calibrated [A-] gamma")

    if gamma_csf > 0 and gamma_csf < 1:
        print("  Status:     PASS (0 < gamma_CSF < 1)")
    else:
        print("  Status:     FAIL (gamma_CSF out of expected range)")
        all_passed = False

    # ------------------------------------------------------------------
    # Check 2: Information Saturation Bound
    # ------------------------------------------------------------------
    print("\n[Check 2] Information Saturation Bound (rho_max) [C]...")
    rho_max = cu.check_information_saturation_bound()
    rho_str = str(rho_max)[:20]
    print(f"  rho_max = {rho_str}... GeV^4")
    print(f"  Evidence: [C] — empirical N=99 (Limitation L5)")

    if rho_max > 0:
        print("  Status:   PASS (rho_max > 0)")
    else:
        print("  Status:   FAIL (rho_max <= 0)")
        all_passed = False

    # ------------------------------------------------------------------
    # Check 3: Equation of State (internal consistency)
    # ------------------------------------------------------------------
    print("\n[Check 3] Equation of State (w_0, w_a) [C]...")
    eos = cu.derive_equation_of_state()
    residual_w0 = abs(eos['w_0'] - mpf('-0.99'))
    residual_wa = abs(eos['w_a'] - mpf('+0.03'))
    print(f"  w_0 = {nstr(eos['w_0'], 5)}  (residual: {nstr(residual_w0, 5)})")
    print(f"  w_a = {nstr(eos['w_a'], 5)}  (residual: {nstr(residual_wa, 5)})")
    print(f"  Evidence: [C] — phenomenological placeholder")

    if residual_w0 < mpf('1e-14') and residual_wa < mpf('1e-14'):
        print("  Status:   PASS (residuals < 1e-14, mpmath 80-dps consistency)")
    else:
        print("  Status:   FAIL (residual too large)")
        all_passed = False

    # ------------------------------------------------------------------
    # Final Status
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    if all_passed:
        print("  ✅ SYSTEM STATUS: CSF-UIDT MAPPING STRICTLY CLOSED.")
        print("=" * 64)
        sys.exit(0)
    else:
        print("  ❌ SYSTEM STATUS: CSF-UIDT VERIFICATION FAILED.")
        print("=" * 64)
        sys.exit(1)


if __name__ == "__main__":
    # Ensure Windows console can display UTF-8 (box art/checkmarks)
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    run_csf_verification()
