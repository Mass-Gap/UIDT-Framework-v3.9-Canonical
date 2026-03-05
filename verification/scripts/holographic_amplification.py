#!/usr/bin/env python3
"""
holographic_amplification.py
============================
UIDT Framework v3.9 — L⁴ Holographic Amplification Table for L = 8.15–8.25

Generates a detailed table of the holographic amplification mechanism:

    δ_eff = δ × L⁴
    w_a   = -δ_eff

where δ = 0.00028757 is the relative vacuum friction shift and L is the
holographic scale parameter. The table spans L = 8.15 to 8.25 in steps
of 0.01, highlighting the central prediction at L = 8.20.

Compares the UIDT prediction against DESI-DR2 (Union3) constraints:
    w_a(Union3) ≈ -1.27 to -1.33

Evidence category: [C]
Author: P. Rietz (ORCID: 0009-0007-4307-1609)
Framework: UIDT v3.9 Canonical
"""

import sys
import mpmath

mpmath.mp.dps = 80

# ── Canonical constants (declared locally, immutable) ─────────────────────
delta_rel    = mpmath.mpf('0.00028757')   # relative shift δ = δγ/γ_∞ [B]
L_target     = mpmath.mpf('8.2')          # holographic scale (central) [C]
Delta        = mpmath.mpf('1.710')        # spectral gap Δ (GeV) [A]
gamma_inf    = mpmath.mpf('16.3437')      # bare γ_∞ [B]
gamma_phys   = mpmath.mpf('16.339')       # dressed γ [A-]
delta_gamma  = mpmath.mpf('0.0047')       # vacuum friction δγ [B/D]
kappa        = mpmath.mpf('0.500')        # κ [A]
lambda_S     = mpmath.mpf('0.417')        # λ_S [A]
H0           = mpmath.mpf('70.4')         # H₀ (km/s/Mpc) [C]
wa_target    = mpmath.mpf('-1.300')       # DESI-DR2 prediction [C]

# DESI-DR2 bounds (Union3 + BAO + CMB)
wa_desi_lo   = mpmath.mpf('-1.33')        # lower bound (more negative)
wa_desi_hi   = mpmath.mpf('-1.27')        # upper bound (less negative)

# Planck 2018 + lensing reference
wa_planck    = mpmath.mpf('-0.58')        # Planck 2018+lensing central (wider uncertainty)
sigma_wa_planck = mpmath.mpf('0.34')      # Planck uncertainty

# ── Generate L range ──────────────────────────────────────────────────────
L_start = mpmath.mpf('8.15')
L_end   = mpmath.mpf('8.25')
L_step  = mpmath.mpf('0.01')

L_values = []
L_cur = L_start
while L_cur <= L_end + L_step / 2:
    L_values.append(L_cur)
    L_cur += L_step

# ── Compute amplification table ──────────────────────────────────────────
table_rows = []
for L in L_values:
    L4      = L**4
    d_eff   = delta_rel * L4
    w_a     = -d_eff
    is_central = (abs(L - L_target) < mpmath.mpf('0.001'))
    in_desi    = (wa_desi_lo <= w_a <= wa_desi_hi)
    table_rows.append((L, L4, d_eff, w_a, is_central, in_desi))

# ── Identify central prediction ──────────────────────────────────────────
central_row = None
for row in table_rows:
    if row[4]:  # is_central
        central_row = row
        break

# ── DESI pass/fail ────────────────────────────────────────────────────────
wa_central = central_row[3] if central_row else None
pass_desi = (wa_central is not None and
             wa_desi_lo <= wa_central <= wa_desi_hi)

# ══════════════════════════════════════════════════════════════════════════
#  OUTPUT
# ══════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("  UIDT Framework v3.9 — L⁴ Holographic Amplification Table")
print("  Author: P. Rietz (ORCID: 0009-0007-4307-1609)")
print("=" * 78)
print()

print("[+] Amplification mechanism:")
print(f"    δ (relative vacuum shift) = {mpmath.nstr(delta_rel, 10)}  [B]")
print(f"    δ_eff = δ × L⁴")
print(f"    w_a   = -δ_eff")
print()

print(f"[+] DESI-DR2 (Union3) bounds: w_a ∈ [{mpmath.nstr(wa_desi_lo, 5)}, {mpmath.nstr(wa_desi_hi, 5)}]")
print(f"[+] Planck 2018+lensing: w_a = {mpmath.nstr(wa_planck, 5)} ± {mpmath.nstr(sigma_wa_planck, 4)}")
print()

# Table header
hdr = f"    {'L':>6s}  {'L⁴':>14s}  {'δ_eff':>14s}  {'w_a':>14s}  {'DESI?':>6s}"
sep = "    " + "-" * 66
print("[+] Holographic amplification table (L = 8.15 – 8.25, step 0.01):")
print(sep)
print(hdr)
print(sep)

for L, L4, d_eff, w_a, is_central, in_desi in table_rows:
    marker = " ◄" if is_central else ""
    desi_flag = "YES" if in_desi else "no"
    line = (f"    {mpmath.nstr(L, 4):>6s}  "
            f"{mpmath.nstr(L4, 10):>14s}  "
            f"{mpmath.nstr(d_eff, 10):>14s}  "
            f"{mpmath.nstr(w_a, 10):>14s}  "
            f"{desi_flag:>6s}{marker}")
    print(line)

print(sep)
print()

if central_row:
    L_c, L4_c, d_eff_c, w_a_c, _, _ = central_row
    print(f"[+] Central prediction (L = {mpmath.nstr(L_c, 4)}):")
    print(f"    L⁴     = {mpmath.nstr(L4_c, 12)}")
    print(f"    δ_eff  = {mpmath.nstr(d_eff_c, 12)}")
    print(f"    w_a    = {mpmath.nstr(w_a_c, 12)}")
    print()

print("[+] Comparison with observational constraints:")
print(f"    DESI-DR2 (Union3+BAO):  w_a ∈ [{mpmath.nstr(wa_desi_lo, 5)}, {mpmath.nstr(wa_desi_hi, 5)}]")
print(f"    Planck 2018+lensing:    w_a = {mpmath.nstr(wa_planck, 5)} ± {mpmath.nstr(sigma_wa_planck, 4)}")
print(f"    UIDT (L = 8.20):        w_a = {mpmath.nstr(wa_central, 10) if wa_central else 'N/A'}")
print()

if pass_desi:
    print(f"    [+] PASS — UIDT prediction w_a = {mpmath.nstr(wa_central, 8)} lies within DESI-DR2 bounds")
else:
    print(f"    [-] FAIL — UIDT prediction w_a = {mpmath.nstr(wa_central, 8) if wa_central else 'N/A'} outside DESI-DR2 bounds")

# Check Planck consistency (wider window)
if wa_central is not None:
    planck_lo = wa_planck - 2 * sigma_wa_planck
    planck_hi = wa_planck + 2 * sigma_wa_planck
    pass_planck = (planck_lo <= wa_central <= planck_hi)
    if pass_planck:
        print(f"    [+] Consistent with Planck 2018+lensing at 2σ")
    else:
        print(f"    [!] Tension with Planck 2018+lensing at 2σ (expected for evolving DE)")
print()

# Count how many table entries fall in DESI range
n_in_desi = sum(1 for row in table_rows if row[5])
print(f"[+] {n_in_desi} of {len(table_rows)} table entries within DESI-DR2 bounds")
print()

print("=" * 78)
if pass_desi:
    print("  RESULT: PASS — Holographic amplification verified against DESI-DR2  [C]")
else:
    print("  RESULT: FAIL — Holographic amplification outside DESI-DR2 bounds")
print("=" * 78)

sys.exit(0 if pass_desi else 1)
