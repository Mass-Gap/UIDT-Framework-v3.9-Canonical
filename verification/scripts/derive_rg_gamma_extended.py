#!/usr/bin/env python3
"""
UIDT FRG Extended Fixed-Point Analysis — Structural Audit
==========================================================
Truncation : SF^2 + S^2F^2 (4x4 system)
Regulator  : Litim (optimised)
Group      : SU(3), N_c = 3
Precision  : mp.dps = 80 (local — Race Condition Lock)

Claim      : UIDT-C-070 (Evidence D)
Limitation : L8  (eta_A = 0 throughout)

Audit finding (2026-04-13):
    The original code used  beta_g2 = -b0*g2^2  (pure YM, one-loop).
    This has NO non-trivial zero at g2 != 0, so the Newton solver
    encountered a singular Jacobian and raised ZeroDivisionError.

    Adding the Scalar-Back-Reaction term  C_back*kap2*g2  (from the
    S*F^2 vertex contribution to the gauge running via the Wetterich
    equation) creates a non-trivial zero  g2* = (C_back/b0)*kap2*.
    However, the analytical reduction of the remaining 3D system
    proves that beta_lam = 0 forces kap2* = 0 (Gaussian FP only),
    because the discriminant coefficient equals -1.74e-4 < 0.

    Root cause: eta_A = 0 (Limitation L8) is the fundamental blocker.
    A non-trivial Gauge+Scalar FRG fixed point requires either:
      (a) eta_A != 0  (Gribov-Zwanziger / confinement sector), OR
      (b) Nf > 0 quarks (changes sign structure in beta_g2), OR
      (c) non-perturbative resummation (Pade / BMW).

    This script documents all steps with 80-digit mpmath precision and
    exits with code 0 (structural analysis complete, not a FP solver).

Reproduction:
    python verification/scripts/derive_rg_gamma_extended.py

Expected output:
    Structural analysis of beta-function zero structure.
    blam-coefficient sign reported.
    Confirmation of Limitation L8 as root cause.
"""

import mpmath as mp
import sys

# ── Precision: LOCAL declaration mandatory (Race Condition Lock) ─────────────
mp.dps = 80

# ── SU(3) group factors ──────────────────────────────────────────────────────
Nc   = mp.mpf('3')
dA   = Nc**2 - 1          # 8
CA   = Nc                  # 3

# ── Litim threshold functions (w -> 0 limit) ─────────────────────────────────
l1   = mp.mpf('1') / (mp.mpf('16') * mp.pi**2)
l2   = mp.mpf('1') / (mp.mpf('32') * mp.pi**2)

# ── One-loop coefficient (pure YM) ───────────────────────────────────────────
b0      = mp.mpf('11') * Nc / mp.mpf('3')        # 11.0 for N_c=3

# ── Scalar-Back-Reaction coefficient ─────────────────────────────────────────
# Derived from the S*F^2 vertex contribution to the gauge propagator in the
# Wetterich equation at one loop with Litim regulator:
#   delta_beta_g2 = + d_A * l1 * kap^2 * g^2
# This encodes the back-reaction of the scalar singlet S on the gauge running.
C_back  = dA * l1   # = 8 / (16*pi^2)

# ── Beta-function coefficients (scalar sector) ────────────────────────────────
A_lam   =  mp.mpf('3')  * l1
B_lam   = -mp.mpf('4')  * CA * l2
C_lam   =  CA**2 * l2
A_kap   =  mp.mpf('2')  * l1
B_kap   = -mp.mpf('2')  * CA * l2
C_kap   =  CA**2 * l2
A_sig   =  mp.mpf('4')  * l1
B_sig   =  mp.mpf('2')  * CA * l2
C_sig   = -mp.mpf('2')  * CA * l2
D_sig   =  CA**2 * l2

# ── Full 4x4 beta functions (with Scalar-Back-Reaction) ──────────────────────
def beta(x):
    """
    x = [g2, lam, kap2, sig]
    beta_g2 includes C_back*kap2*g2 (Scalar-Back-Reaction).
    """
    g2, lam, kap2, sig = x
    bg2   = A_g * g2**2 + C_back * kap2 * g2
    blam  = A_lam * lam**2 + B_lam * kap2 * g2 + C_lam * g2**2
    bkap2 = mp.mpf('2') * kap2 * (A_kap * lam + (B_kap + C_kap) * g2)
    bsig  = A_sig * sig * lam + B_sig * kap2 + C_sig * sig * g2 + D_sig * g2**2
    return [bg2, blam, bkap2, bsig]

# A_g coefficient
A_g = -b0

# ── Analytical zero-structure analysis ───────────────────────────────────────

print('=' * 64)
print('UIDT FRG Extended Fixed-Point Analysis — Structural Audit')
print('Truncation: SF^2 + S^2F^2 (4x4) | Regulator: Litim | SU(3)')
print('Claim: UIDT-C-070 | Limitation: L8 | Evidence: D')
print('=' * 64)
print()

# Step 1: g2* from beta_g2 = 0
ratio = C_back / b0
print('Step 1 — Non-trivial zero of beta_g2:')
print(f'  beta_g2 = g2 * (-b0*g2 + C_back*kap2) = 0')
print(f'  => g2* = (C_back / b0) * kap2*')
print(f'     ratio = C_back/b0 = {mp.nstr(ratio, 15)}')
print()

# Step 2: kap2 inner condition from beta_kap2 = 0 (kap2 != 0)
BpC = B_kap + C_kap
lam_coeff = -BpC * ratio / A_kap
print('Step 2 — Non-trivial zero of beta_kap2 (kap2 != 0):')
print(f'  A_kap*lam + (B_kap+C_kap)*g2* = 0')
print(f'  => lam* = {mp.nstr(lam_coeff, 15)} * kap2*')
print()

# Step 3: Substitution into beta_lam
coeff_kap2sq = A_lam * lam_coeff**2 + B_lam * ratio + C_lam * ratio**2
print('Step 3 — Substitution lam*=lam_coeff*kap2*, g2*=ratio*kap2* into beta_lam:')
print(f'  beta_lam = ({mp.nstr(coeff_kap2sq, 10)}) * kap2*^2')
print()

if coeff_kap2sq < 0:
    # Negative coefficient: kap2* from sqrt(-const/coeff) if there were a
    # linear source term. Without one, still implies kap2*=0.
    print(f'  coeff < 0: beta_lam = 0 would require an additional source term.')
    print(f'  In this truncation (no source), kap2* = 0 is the only solution.')
elif coeff_kap2sq > 0:
    print(f'  coeff > 0: beta_lam = 0 implies kap2* = 0 (Gaussian FP only).')
else:
    print(f'  coeff = 0: lam* is a free parameter (line of FPs).')
print()

# Step 4: sigma* from beta_sig = 0 at g2*=0, kap2*=0
# bsig = A_sig*sig*0 + B_sig*0 + C_sig*sig*0 + D_sig*0 = 0 => sigma free at Gaussian FP
print('Step 4 — Gaussian FP (g2*=lam*=kap2*=0): beta_sig = 0 trivially.')
print()

# Step 5: Verify Gaussian FP
x_gauss = [mp.mpf('0'), mp.mpf('0'), mp.mpf('0'), mp.mpf('0')]
bg = beta(x_gauss)
print('Step 5 — Gaussian FP verification:')
print(f'  beta(0,0,0,0) = {[mp.nstr(r,6) for r in bg]}')
all_zero = all(abs(r) < mp.mpf('1e-50') for r in bg)
print(f'  All zero: {all_zero}')
print()

# Step 6: Root cause
print('Step 6 — Root cause analysis:')
print()
print('  The Litim-regulated pure-YM beta_g2 has the form:')
print('    beta_g2 = -b0*g2^2 + C_back*kap2*g2')
print()
print('  This yields g2* = (C_back/b0)*kap2* (non-trivial only if kap2* != 0).')
print('  But the beta_lam equation requires kap2* = 0 in this truncation.')
print()
print('  CONCLUSION: A non-trivial Gauge+Scalar FRG fixed point requires one of:')
print('    (a) eta_A != 0  [Gribov-Zwanziger / confinement sector]')
print('        -> upgrades Limitation L8, requires full gluon Propagator')
print('    (b) Nf > 0 quarks')
print('        -> changes sign structure via -Nf/3 in b0')
print('    (c) Non-perturbative resummation (Pade / BMW approximation)')
print()
print('  Limitation L8 (eta_A = 0) is the fundamental blocker.')
print('  The canonical gamma = 16.339 [A-] is NOT derivable within')
print('  this truncation and remains strictly phenomenological.')
print()

# ── Anomalous dimension at Gaussian FP ───────────────────────────────────────
# At g2*=kap2*=0: eta_* = 0 trivially
eta_at_gauss = mp.mpf('0')
print(f'eta_* at Gaussian FP = {eta_at_gauss}  (trivial)')
print()

# ── Summary ───────────────────────────────────────────────────────────────────
print('=' * 64)
print('STRUCTURAL AUDIT COMPLETE')
print(f'blam-coefficient = {mp.nstr(coeff_kap2sq, 10)}')
print(f'Non-trivial FP exists in this truncation: False')
print(f'Root cause: Limitation L8 (eta_A = 0) confirmed')
print(f'Evidence: D | Limitation: L8')
print('gamma = 16.339 remains [A-] per Ledger (not derivable here)')
print('=' * 64)

sys.exit(0)
