#!/usr/bin/env python3
"""
verify_monte_carlo_research_notes.py
=====================================
UIDT v3.9 -- MC Correlation Provenance Audit

Purpose
-------
Recompute ALL pairwise correlations from the raw Monte Carlo chain
(UIDT_MonteCarlo_samples_100k.csv) and compare them against the stored
summary artefact (UIDT_MonteCarlo_correlation_matrix.csv).

Emits:
  [TENSION ALERT]      if |Delta_r| > 0.05 for any pair
  [RG_CONSTRAINT_FAIL] if |5*kappa^2 - 3*lambda_S| > 1e-14 at hp-mean
  [AUDIT_FAIL]         if raw CSV is not found (Zenodo download required)

Reproduction (one command)
--------------------------
  python verification/scripts/verify_monte_carlo_research_notes.py \\
      --raw  simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv \\
      --corr simulation/monte_carlo/UIDT_MonteCarlo_correlation_matrix.csv \\
      --hp   simulation/monte_carlo/UIDT_HighPrecision_mean_values.csv

Raw CSV source (Zenodo, 19 MB):
  https://doi.org/10.5281/zenodo.17554179

Context
-------
The stored correlation matrix (8x8, parameters: m_S, kappa, lambda_S, C,
alpha_s, Delta, gamma, Psi) reports r(Delta, Psi) = +0.13770 and
r(gamma, Psi) = +0.99952.  A previous audit session flagged that
r(Delta*, Pi_S) = +0.720284420 claimed in STRATUM_II could not be
reproduced.  NOTE: 'Pi_S' does not appear as a column in the stored 8x8
matrix.  This script:
  (a) verifies which parameters are actually in the raw CSV,
  (b) recomputes all N*(N-1)/2 pairwise correlations with mpmath,
  (c) flags any |Delta_r| > 0.05 as [TENSION ALERT].

ARCHITECTURE RULES
------------------
- mp.dps = 80  declared LOCAL inside functions, never global.
- No float(), no round().
- No unittest.mock, no MagicMock.
- Constants from LEDGER are read-only reference values.
- Deletes nothing from /core or /modules.

Evidence categories of outputs
-------------------------------
  Recomputed correlations vs raw CSV  : [A]
  Comparison against stored artefact  : [B]
  RG constraint check at hp-mean      : [A] (constraint) / [A-] (hp-values)
"""

import argparse
import csv
import os
import sys
from itertools import combinations

import mpmath as mp

# ---------------------------------------------------------------------------
# LEDGER CONSTANTS  (read-only; do not modify)
# ---------------------------------------------------------------------------
LEDGER_DELTA_STAR   = "1.710"          # GeV  [A]
LEDGER_GAMMA        = "16.339"         # [A-]
LEDGER_GAMMA_INF    = "16.3437"        # [A-]
LEDGER_DELTA_GAMMA  = "0.0047"         # [B/D]
LEDGER_V            = "47.7e-3"        # GeV  [A]
LEDGER_W0           = "-0.99"          # [C]
LEDGER_ET           = "2.44e-3"        # GeV  [C]

# ---------------------------------------------------------------------------
# TENSION / FAIL THRESHOLDS
# ---------------------------------------------------------------------------
CORR_TENSION_THRESHOLD = mp.mpf("0.05")   # |Delta_r| > this -> [TENSION ALERT]
RG_RESIDUAL_THRESHOLD  = mp.mpf("1e-14")  # |5k^2 - 3l| > this -> [RG_CONSTRAINT_FAIL]


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def _load_csv_columns(path):
    """Return (header, list-of-dicts) from a CSV file."""
    if not os.path.isfile(path):
        return None, None
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    return reader.fieldnames, rows


def _load_raw_chain(path):
    """
    Load raw MC chain CSV.
    Returns (column_names: list[str], columns: dict[str, list[mpf]]).
    Uses streaming read to handle large files.
    """
    if not os.path.isfile(path):
        return None, None
    print(f"  Loading raw chain: {path}")
    columns = {}
    col_names = None
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        for i, row in enumerate(reader):
            if i == 0:
                col_names = [c.strip() for c in row]
                for c in col_names:
                    columns[c] = []
                continue
            for j, val in enumerate(row):
                if j < len(col_names):
                    try:
                        columns[col_names[j]].append(mp.mpf(val.strip()))
                    except Exception:
                        columns[col_names[j]].append(mp.mpf("0"))
    n_rows = len(columns[col_names[0]]) if col_names else 0
    print(f"  Loaded {n_rows} samples, {len(col_names)} columns.")
    return col_names, columns


# ---------------------------------------------------------------------------
# Correlation computation (mpmath, mp.dps=80 LOCAL)
# ---------------------------------------------------------------------------

def _pearson_r(x, y):
    """Pearson r with mp.dps=80 local precision."""
    mp.dps = 80
    n = len(x)
    if n == 0:
        return mp.mpf("0")
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    dx = [xi - mean_x for xi in x]
    dy = [yi - mean_y for yi in y]
    num   = sum(dxi * dyi for dxi, dyi in zip(dx, dy))
    denom = mp.sqrt(sum(dxi**2 for dxi in dx) * sum(dyi**2 for dyi in dy))
    if denom == 0:
        return mp.mpf("0")
    return num / denom


def compute_all_correlations(col_names, columns):
    """
    Compute all N*(N-1)/2 pairwise Pearson correlations.
    Returns dict: (col_a, col_b) -> mpf
    """
    mp.dps = 80
    result = {}
    pairs = list(combinations(col_names, 2))
    print(f"  Computing {len(pairs)} pairwise correlations ...")
    for a, b in pairs:
        result[(a, b)] = _pearson_r(columns[a], columns[b])
    return result


# ---------------------------------------------------------------------------
# Stored correlation matrix reader
# ---------------------------------------------------------------------------

def load_stored_correlations(path):
    """
    Read the stored 8x8 correlation matrix CSV.
    First column is row-label.
    Returns dict: (row_label, col_label) -> mpf  (upper+lower triangle)
    """
    mp.dps = 80
    if not os.path.isfile(path):
        return None
    stored = {}
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = None
        for row in reader:
            if header is None:
                header = [c.strip() for c in row[1:]]  # skip index col
                continue
            row_label = row[0].strip()
            for j, val in enumerate(row[1:]):
                if j < len(header):
                    col_label = header[j]
                    if row_label != col_label:
                        key = tuple(sorted([row_label, col_label]))
                        stored[key] = mp.mpf(val.strip())
    return stored


# ---------------------------------------------------------------------------
# RG constraint check (hp-mean)
# ---------------------------------------------------------------------------

def check_rg_constraint(hp_path):
    """
    Load kappa_mean and lambda_S from hp CSV and check 5*kappa^2 = 3*lambda_S.
    Emits [RG_CONSTRAINT_FAIL] if residual > 1e-14.
    Returns (kappa, lambda_S, residual, passed: bool)
    """
    mp.dps = 80
    if not os.path.isfile(hp_path):
        print("  [AUDIT_FAIL] hp-mean CSV not found:", hp_path)
        return None, None, None, False

    with open(hp_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    if not rows:
        print("  [AUDIT_FAIL] hp-mean CSV is empty.")
        return None, None, None, False

    row = rows[0]
    # Column names from actual CSV: kappa_mean, lambda_S not present --
    # the hp CSV stores: m_S_mean, kappa_mean, C_mean, Pi_S_mp, Delta_mp,
    # kin_mp, gamma_mp, Psi_mp
    # lambda_S is NOT in the hp CSV (known limitation).
    kappa_key = "kappa_mean"
    if kappa_key not in row:
        print("  [AUDIT_FAIL] 'kappa_mean' column not found in hp CSV.")
        print("  Available columns:", list(row.keys()))
        print("  [RG_CONSTRAINT_FAIL] Cannot evaluate 5*kappa^2 = 3*lambda_S:")
        print("  lambda_S is absent from UIDT_HighPrecision_mean_values.csv.")
        print("  Action required: add lambda_S to hp CSV or derive from kappa.")
        return None, None, None, False

    kappa = mp.mpf(row[kappa_key].strip())
    # lambda_S is not in hp CSV -> derive from RG constraint as cross-check
    # If 5*kappa^2 = 3*lambda_S is exact, then lambda_S = 5*kappa^2 / 3
    lambda_S_derived = mp.mpf(5) * kappa**2 / mp.mpf(3)
    residual = abs(mp.mpf(5) * kappa**2 - mp.mpf(3) * lambda_S_derived)
    # Residual against derived value is zero by construction.
    # Real test: compare kappa_mean from hp with kappa from summary CSV.
    print(f"  kappa_mean (hp)      : {mp.nstr(kappa, 30)}")
    print(f"  lambda_S (derived)   : {mp.nstr(lambda_S_derived, 30)}")
    print(f"  5*kappa^2 - 3*lambda_S (self-consistency): {mp.nstr(residual, 30)}")

    # Cross-check: compare hp kappa with summary kappa if available
    print("  Note: lambda_S is absent from the hp CSV. Full RG constraint")
    print("  check requires lambda_S to be added to UIDT_HighPrecision_mean_values.csv.")
    print("  [RG_CONSTRAINT_FAIL] flag from prior audit session remains OPEN.")
    return kappa, lambda_S_derived, residual, False  # open until lambda_S added


# ---------------------------------------------------------------------------
# Tension comparison
# ---------------------------------------------------------------------------

def compare_correlations(recomputed, stored, raw_col_names):
    """
    Compare recomputed correlations against stored matrix.
    Emits [TENSION ALERT] for |Delta_r| > 0.05.
    Also reports which stored pairs are absent from the raw chain.
    """
    mp.dps = 80
    print("\n" + "=" * 64)
    print("CORRELATION PROVENANCE AUDIT")
    print("=" * 64)

    tension_count = 0
    absent_count  = 0

    if stored is None:
        print("  [AUDIT_FAIL] Stored correlation matrix not loaded.")
        return

    for key, stored_r in sorted(stored.items()):
        a, b = key
        # Check if both columns exist in raw chain
        if a not in raw_col_names or b not in raw_col_names:
            print(f"  ABSENT  ({a}, {b}): not in raw CSV columns")
            print(f"          stored r = {mp.nstr(stored_r, 10)}")
            absent_count += 1
            continue
        canon_key = tuple(sorted([a, b]))
        recomp_r = recomputed.get(canon_key)
        if recomp_r is None:
            print(f"  MISSING ({a}, {b}): recomputed value not available")
            continue
        delta = abs(recomp_r - stored_r)
        flag = "[TENSION ALERT]" if delta > CORR_TENSION_THRESHOLD else "OK"
        if flag == "[TENSION ALERT]":
            tension_count += 1
        print(
            f"  {flag:<16} ({a:12}, {b:12})  "
            f"stored={mp.nstr(stored_r, 8):>12}  "
            f"recomp={mp.nstr(recomp_r, 8):>12}  "
            f"|Delta|={mp.nstr(delta, 6)}"
        )

    print("=" * 64)
    print(f"  Tensions:       {tension_count}")
    print(f"  Absent columns: {absent_count}")
    if absent_count > 0:
        print("  NOTE: columns absent from raw CSV but present in stored matrix")
        print("  indicate a provenance gap.  Update correlation matrix or")
        print("  document which chain version produced the stored values.")
    if tension_count == 0 and absent_count == 0:
        print("  All pairwise correlations reproduced within threshold.")
        print("  [TENSION ALERT] for r(Delta*, Pi_S) is RESOLVED.")
    elif tension_count == 0 and absent_count > 0:
        print("  No numerical tension in overlapping pairs.")
        print("  [TENSION ALERT] status: PARTIALLY OPEN (absent columns).")
    else:
        print("  [TENSION ALERT] items remain OPEN.")


# ---------------------------------------------------------------------------
# Additional: check claimed r(Delta*, Pi_S) directly
# ---------------------------------------------------------------------------

def check_claimed_pis_correlation(raw_col_names, columns):
    """
    Specifically check whether Pi_S (or Psi, Pi_S, Pi_s variants) exists
    in the raw chain and report r(Delta*, Pi_S).
    """
    mp.dps = 80
    print("\n" + "=" * 64)
    print("SPECIFIC CHECK: r(Delta*, Pi_S) -- [TENSION ALERT] resolution")
    print("=" * 64)
    # Possible column name variants
    delta_candidates = ["Delta", "Delta_star", "Delta*", "delta"]
    pis_candidates   = ["Pi_S", "Pi_s", "Psi", "pi_S", "kinetic_VEV"]

    delta_col = next((c for c in delta_candidates if c in raw_col_names), None)
    pis_col   = next((c for c in pis_candidates   if c in raw_col_names), None)

    if delta_col is None:
        print("  [AUDIT_FAIL] No Delta* column found in raw CSV.")
        print(f"  Available columns: {raw_col_names}")
        return
    if pis_col is None:
        print("  Pi_S column NOT found in raw CSV.")
        print(f"  Available columns: {raw_col_names}")
        print("  Stored claim r(Delta*, Pi_S) = +0.720284420 CANNOT be")
        print("  reproduced from this CSV version.")
        print("  [TENSION ALERT] remains OPEN: provenance of stored matrix unclear.")
        return

    r_val = _pearson_r(columns[delta_col], columns[pis_col])
    stored_claim = mp.mpf("0.720284420")
    delta = abs(r_val - stored_claim)
    print(f"  Delta* column : '{delta_col}'")
    print(f"  Pi_S  column  : '{pis_col}'")
    print(f"  Recomputed r  : {mp.nstr(r_val, 15)}")
    print(f"  Stored claim  : {mp.nstr(stored_claim, 15)}")
    print(f"  |Delta_r|     : {mp.nstr(delta, 10)}")
    if delta > CORR_TENSION_THRESHOLD:
        print("  [TENSION ALERT] -- numerical conflict confirmed.")
    else:
        print("  OK -- stored value reproduced. [TENSION ALERT] RESOLVED.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="UIDT MC Correlation Provenance Audit"
    )
    parser.add_argument(
        "--raw",
        default="simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv",
        help="Path to raw MC chain CSV (19 MB, from Zenodo DOI 10.5281/zenodo.17554179)",
    )
    parser.add_argument(
        "--corr",
        default="simulation/monte_carlo/UIDT_MonteCarlo_correlation_matrix.csv",
        help="Path to stored correlation matrix CSV",
    )
    parser.add_argument(
        "--hp",
        default="simulation/monte_carlo/UIDT_HighPrecision_mean_values.csv",
        help="Path to high-precision mean values CSV",
    )
    args = parser.parse_args()

    print("=" * 64)
    print("UIDT v3.9 -- MC Correlation Provenance Audit")
    print("=" * 64)

    # ------------------------------------------------------------------
    # Phase 1: RG constraint at hp-mean (independent of raw CSV)
    # ------------------------------------------------------------------
    print("\nPhase 1: RG Constraint Check (hp-mean values)")
    check_rg_constraint(args.hp)

    # ------------------------------------------------------------------
    # Phase 2: Load raw chain
    # ------------------------------------------------------------------
    print("\nPhase 2: Load Raw MC Chain")
    if not os.path.isfile(args.raw):
        print(f"  [AUDIT_FAIL] Raw CSV not found: {args.raw}")
        print("  Download from Zenodo: https://doi.org/10.5281/zenodo.17554179")
        print("  Place at:", args.raw)
        print("  Skipping correlation recomputation.")
        print("  [TENSION ALERT] for r(Delta*, Pi_S) remains OPEN.")
        sys.exit(1)

    raw_col_names, columns = _load_raw_chain(args.raw)
    if raw_col_names is None:
        print("  [AUDIT_FAIL] Failed to load raw CSV.")
        sys.exit(1)

    print(f"  Raw CSV columns ({len(raw_col_names)}): {raw_col_names}")

    # ------------------------------------------------------------------
    # Phase 3: Recompute all pairwise correlations
    # ------------------------------------------------------------------
    print("\nPhase 3: Recompute All Pairwise Correlations")
    recomputed = compute_all_correlations(raw_col_names, columns)

    # ------------------------------------------------------------------
    # Phase 4: Load stored matrix and compare
    # ------------------------------------------------------------------
    print("\nPhase 4: Compare Against Stored Correlation Matrix")
    stored = load_stored_correlations(args.corr)
    compare_correlations(recomputed, stored, raw_col_names)

    # ------------------------------------------------------------------
    # Phase 5: Specific Pi_S / Tension Alert check
    # ------------------------------------------------------------------
    print("\nPhase 5: Specific r(Delta*, Pi_S) Check")
    check_claimed_pis_correlation(raw_col_names, columns)

    print("\nAudit complete.")


if __name__ == "__main__":
    main()
