#!/usr/bin/env python3
"""
generate_mc_plots.py
====================
UIDT v3.9 -- Monte Carlo Validation Plot Generator

Generates the three publication-quality JPGs for the GitHub Release
`v3.9-mc-validation` (see RELEASE_ASSETS.md).

Outputs
-------
  <outdir>/UIDT_MC_hexbin_Delta_gamma.jpg
  <outdir>/UIDT_MC_histograms_5params.jpg
  <outdir>/UIDT_MC_scatter_kappa_lambdaS.jpg

Reproduction (one command)
--------------------------
  python simulation/monte_carlo/generate_mc_plots.py \\
      --raw    simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv \\
      --outdir simulation/monte_carlo/plots/

Raw CSV source (Zenodo, 19 MB):
  https://doi.org/10.5281/zenodo.17554179

ARCHITECTURE RULES
------------------
- mp.dps = 80 declared LOCAL (race-condition lock).
- LEDGER constants as string literals -> mp.mpf().
- No float() for physics values; float() allowed ONLY for matplotlib axis
  coordinates after mp.mpf computation is complete.
- No unittest.mock, no MagicMock.
- Deletes nothing from /core or /modules.

Evidence categories
-------------------
  Plot data (raw posterior)     : [A]
  LEDGER reference lines        : [A] / [A-]
  Interpretation annotations    : Stratum I / II
"""

import argparse
import csv
import os
import sys

import mpmath as mp

# ---------------------------------------------------------------------------
# LEDGER CONSTANTS  (read-only; do not modify)
# ---------------------------------------------------------------------------
LEDGER_DELTA_STAR  = mp.mpf("1.710")    # GeV [A]
LEDGER_DELTA_UNC   = mp.mpf("0.015")    # GeV [A]
LEDGER_GAMMA       = mp.mpf("16.339")   # [A-]
LEDGER_GAMMA_INF   = mp.mpf("16.3437")  # [A-]

# RG constraint: 5*kappa^2 = 3*lambda_S -> lambda_S = 5/3 * kappa^2
# Used to draw the RG track in the scatter plot.
RG_KAPPA_MIN = mp.mpf("0.40")
RG_KAPPA_MAX = mp.mpf("0.60")


# ---------------------------------------------------------------------------
# CSV loader (streaming, float conversion only for matplotlib)
# ---------------------------------------------------------------------------

def load_columns(path, needed_cols):
    """
    Load only the requested columns from a large CSV.
    Returns dict: col_name -> list[float]  (float allowed for plot axes only).
    """
    if not os.path.isfile(path):
        return None
    columns = {c: [] for c in needed_cols}
    found = set()
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = None
        for i, row in enumerate(reader):
            if i == 0:
                header = [c.strip() for c in row]
                found = set(needed_cols) & set(header)
                missing = set(needed_cols) - found
                if missing:
                    print(f"  WARNING: columns not found in CSV: {missing}")
                continue
            for col in found:
                idx = header.index(col)
                if idx < len(row):
                    try:
                        # float() is permitted here: only used for matplotlib
                        # after all mpmath computations are complete.
                        columns[col].append(float(row[idx]))
                    except ValueError:
                        pass
    print(f"  Loaded {len(columns[list(found)[0]])} rows for {sorted(found)}.")
    return columns


# ---------------------------------------------------------------------------
# Plot 1: Hexbin Delta* vs gamma
# ---------------------------------------------------------------------------

def plot_hexbin(columns, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    mp.dps = 80

    x = columns.get("Delta", [])
    y = columns.get("gamma", [])
    if not x or not y:
        print("  [SKIP] hexbin: missing Delta or gamma column.")
        return

    fig, ax = plt.subplots(figsize=(7, 6))
    hb = ax.hexbin(x, y, gridsize=80, cmap="plasma", mincnt=1, linewidths=0.1)
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label("Sample count", fontsize=10)

    # LEDGER reference lines [A] / [A-]
    ax.axvline(
        float(LEDGER_DELTA_STAR), color="white", ls=":", lw=1.4,
        label=rf"$\Delta^*_{{\rm LEDGER}}={mp.nstr(LEDGER_DELTA_STAR, 5)}$ GeV [A]"
    )
    ax.axvline(
        float(LEDGER_DELTA_STAR - LEDGER_DELTA_UNC), color="white", ls="--",
        lw=0.8, alpha=0.5
    )
    ax.axvline(
        float(LEDGER_DELTA_STAR + LEDGER_DELTA_UNC), color="white", ls="--",
        lw=0.8, alpha=0.5
    )
    ax.axhline(
        float(LEDGER_GAMMA), color="cyan", ls=":", lw=1.4,
        label=rf"$\gamma_{{\rm LEDGER}}={mp.nstr(LEDGER_GAMMA, 6)}$ [A-]"
    )
    ax.axhline(
        float(LEDGER_GAMMA_INF), color="cyan", ls="--", lw=0.8, alpha=0.6,
        label=rf"$\gamma_\infty={mp.nstr(LEDGER_GAMMA_INF, 7)}$ [A-]"
    )

    ax.set_xlabel(r"$\Delta^*$ (GeV)", fontsize=12)
    ax.set_ylabel(r"$\gamma$", fontsize=12)
    ax.set_title(
        r"UIDT v3.9 MC Posterior: $\Delta^*$ vs $\gamma$" + "\n"
        r"(Hexbin density, $N=100\,000$ samples, Stratum~I [A])",
        fontsize=11
    )
    ax.legend(fontsize=8, loc="upper right")
    fig.text(
        0.01, 0.01,
        "Reference lines: UIDT LEDGER values [A]/[A-], not external measurements.",
        fontsize=7, color="gray"
    )
    fig.tight_layout()

    out = os.path.join(outdir, "UIDT_MC_hexbin_Delta_gamma.jpg")
    fig.savefig(out, dpi=150, format="jpeg", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Plot 2: Marginal histograms (5 parameters)
# ---------------------------------------------------------------------------

def plot_histograms(columns, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    mp.dps = 80

    params = [
        ("Delta",     r"$\Delta^*$ (GeV)",  float(LEDGER_DELTA_STAR),  "[A]"),
        ("gamma",     r"$\gamma$",           float(LEDGER_GAMMA),       "[A-]"),
        ("Psi",       r"$\Psi$",             None,                      None),
        ("kappa",     r"$\kappa$",           None,                      None),
        ("lambda_S",  r"$\lambda_S$",        None,                      None),
    ]

    n_available = sum(1 for p, _, _, _ in params if p in columns and columns[p])
    if n_available == 0:
        print("  [SKIP] histograms: no required columns found.")
        return

    fig, axes = plt.subplots(1, 5, figsize=(18, 4))
    for ax, (col, label, ref, cat) in zip(axes, params):
        data = columns.get(col, [])
        if not data:
            ax.text(0.5, 0.5, f"{col}\nnot in CSV",
                    ha="center", va="center", transform=ax.transAxes, fontsize=9)
            ax.set_title(label, fontsize=10)
            continue
        ax.hist(data, bins=120, color="steelblue", alpha=0.85,
                edgecolor="none", density=True)
        if ref is not None:
            ax.axvline(ref, color="crimson", ls=":", lw=1.6,
                       label=f"LEDGER {cat}")
            ax.legend(fontsize=7)
        ax.set_xlabel(label, fontsize=10)
        ax.set_ylabel("Density" if ax == axes[0] else "", fontsize=9)
        ax.tick_params(labelsize=8)

    fig.suptitle(
        r"UIDT v3.9 MC Posterior: Marginal Histograms ($N=100\,000$, Stratum~I [A])",
        fontsize=12
    )
    fig.text(
        0.01, -0.03,
        "Reference lines: UIDT LEDGER values [A]/[A-], not external measurements.",
        fontsize=7, color="gray"
    )
    fig.tight_layout()

    out = os.path.join(outdir, "UIDT_MC_histograms_5params.jpg")
    fig.savefig(out, dpi=150, format="jpeg", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Plot 3: Scatter kappa vs lambda_S with RG track
# ---------------------------------------------------------------------------

def plot_scatter_rg(columns, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    mp.dps = 80

    x = columns.get("kappa", [])
    y = columns.get("lambda_S", [])
    if not x or not y:
        print("  [SKIP] scatter: missing kappa or lambda_S column.")
        return

    # RG track: lambda_S = 5/3 * kappa^2 (computed in mpmath, converted for plot)
    kappa_track = [float(RG_KAPPA_MIN) + i * (float(RG_KAPPA_MAX) - float(RG_KAPPA_MIN)) / 200
                   for i in range(201)]
    lambda_track = [float(mp.mpf(5) / mp.mpf(3) * mp.mpf(str(k))**2) for k in kappa_track]

    fig, ax = plt.subplots(figsize=(6, 6))

    # Thin scatter (every 20th point for readability)
    ax.scatter(x[::20], y[::20], s=1.5, alpha=0.25, color="steelblue",
               rasterized=True, label=r"MC samples ($\times 1/20$)")

    # RG fixed-point track [A]
    ax.plot(kappa_track, lambda_track, color="crimson", lw=2.0, ls="-",
            label=r"RG track: $5\kappa^2 = 3\lambda_S$ [A]")

    ax.set_xlabel(r"$\kappa$", fontsize=12)
    ax.set_ylabel(r"$\lambda_S$", fontsize=12)
    ax.set_title(
        r"UIDT v3.9: $\kappa$ vs $\lambda_S$ — RG Fixed-Point Track" + "\n"
        r"(Stratum~I/II [A], $N=100\,000$ samples)",
        fontsize=11
    )
    ax.legend(fontsize=9)
    fig.text(
        0.01, 0.01,
        "RG track: exact constraint 5\u03ba\u00b2=3\u03bb_S [A]. "
        "Soft [RG_CONSTRAINT_FAIL] at hp-mean level remains open (see STRATUM_I_RESULTS.md).",
        fontsize=7, color="gray", wrap=True
    )
    fig.tight_layout()

    out = os.path.join(outdir, "UIDT_MC_scatter_kappa_lambdaS.jpg")
    fig.savefig(out, dpi=150, format="jpeg", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="UIDT v3.9 MC Plot Generator"
    )
    parser.add_argument(
        "--raw",
        default="simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv",
        help="Path to raw MC chain CSV (19 MB, Zenodo 10.5281/zenodo.17554179)",
    )
    parser.add_argument(
        "--outdir",
        default="simulation/monte_carlo/plots/",
        help="Output directory for JPG files",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.raw):
        print(f"[AUDIT_FAIL] Raw CSV not found: {args.raw}")
        print("Download: curl -L -o", args.raw,
              "'https://zenodo.org/records/17554179/files/UIDT_MonteCarlo_samples_100k.csv'")
        sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)

    needed = ["Delta", "gamma", "Psi", "kappa", "lambda_S", "alpha_s", "C", "m_S"]
    print("Loading columns:", needed)
    columns = load_columns(args.raw, needed)
    if columns is None:
        print("[AUDIT_FAIL] Could not load CSV.")
        sys.exit(1)

    print("\nPlot 1: Hexbin Delta* vs gamma")
    plot_hexbin(columns, args.outdir)

    print("\nPlot 2: Marginal histograms (5 parameters)")
    plot_histograms(columns, args.outdir)

    print("\nPlot 3: Scatter kappa vs lambda_S + RG track")
    plot_scatter_rg(columns, args.outdir)

    print("\nAll plots generated. Upload to GitHub Release v3.9-mc-validation")
    print("See: simulation/monte_carlo/RELEASE_ASSETS.md")


if __name__ == "__main__":
    main()
