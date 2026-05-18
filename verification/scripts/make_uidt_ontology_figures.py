"""Generate audit figures for the UIDT Ontology v3.9 manuscript.

The figures are intentionally non-decorative: they visualise dimensional
bookkeeping, external cosmology tension, and falsification exposure only.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "verification" / "data" / "visualizations"
OUT = ROOT / "manuscript" / "figures"


UIDT_BLACK = "#1f2933"
UIDT_GRAY = "#667085"
UIDT_LIGHT = "#e5e7eb"
UIDT_BLUE = "#2563eb"
UIDT_RED = "#b42318"
UIDT_GREEN = "#15803d"
UIDT_MUTED_BLUE = "#dbeafe"
UIDT_MUTED_RED = "#fee2e2"
UIDT_MUTED_GREEN = "#dcfce7"
UIDT_ROW = "#f8fafc"


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Palatino Linotype", "DejaVu Serif", "Times New Roman"],
        "font.size": 8.0,
        "axes.titlesize": 9.0,
        "axes.labelsize": 7.6,
        "xtick.labelsize": 7.0,
        "ytick.labelsize": 7.0,
        "figure.dpi": 180,
        "savefig.dpi": 600,
    }
)


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save(fig: plt.Figure, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


def figure_eft_dimensions() -> None:
    rows = read_csv("eft_operator_dimensions.csv")
    terms = [
        r"$F_{\mu\nu}F^{\mu\nu}$",
        r"$(D_\mu S)(D^\mu S)$",
        r"$\mu^2 S^2$",
        r"$\lambda_S S^4$",
        r"$(\bar{\kappa}/\Lambda_{\rm UIDT})SF^2$",
    ]
    statuses = [
        "renormalisable",
        "kinetic",
        "relevant",
        "renormalisable",
        "EFT-only",
    ]
    dims = [float(row["operator_dimension"]) for row in rows]

    fig, ax = plt.subplots(figsize=(6.7, 2.35), constrained_layout=True)
    ypos = list(range(len(rows)))
    colors = [UIDT_RED if dim > 4 else UIDT_BLACK for dim in dims]

    for y in ypos:
        if y % 2 == 0:
            ax.axhspan(y - 0.42, y + 0.42, color=UIDT_ROW, zorder=0)

    ax.hlines(ypos, xmin=0, xmax=dims, color="#cbd5e1", linewidth=1.25)
    ax.scatter(dims, ypos, s=34, color=colors, zorder=3)
    ax.axvline(4, color=UIDT_GRAY, linewidth=0.9, linestyle=(0, (3, 3)))
    ax.text(4.04, -0.62, r"$d=4$ boundary", fontsize=7.2, color=UIDT_GRAY, va="top")

    for y, dim, status in zip(ypos, dims, statuses):
        ax.text(5.18, y, f"d={dim:g}, {status}", va="center", fontsize=7.2, color=UIDT_GRAY)

    ax.set_yticks(ypos)
    ax.set_yticklabels(terms)
    ax.set_xlabel("canonical operator mass dimension")
    ax.set_xlim(0, 5.92)
    ax.set_ylim(-0.55, len(rows) - 0.45)
    ax.invert_yaxis()
    ax.grid(axis="x", color=UIDT_LIGHT, linewidth=0.55)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#94a3b8")
    ax.tick_params(axis="y", length=0)
    ax.set_title("EFT operator dimensions", loc="left", fontweight="bold", pad=5)
    save(fig, "fig_eft_operator_dimensions")


def figure_desi_tension() -> None:
    rows = read_csv("desi_uidt_tension.csv")
    h0 = [row for row in rows if row["observable"] == "H0"]
    w0 = [row for row in rows if row["observable"] == "w0"]

    fig, axes = plt.subplots(1, 2, figsize=(6.7, 2.35), constrained_layout=True)
    panels = [
        (axes[0], h0, r"$H_0$  [km s$^{-1}$ Mpc$^{-1}$]", 67.75, 70.75, "7.96 sigma / 6.91 sigma"),
        (axes[1], w0, r"$w_0$", -1.04, -0.78, "2.76 sigma"),
    ]

    for ax, panel_rows, xlabel, xmin, xmax, note in panels:
        labels = [row["source"] for row in panel_rows]
        values = [float(row["value"]) for row in panel_rows]
        errs = [float(row["uncertainty"]) for row in panel_rows]
        ypos = list(range(len(panel_rows)))
        colors = [UIDT_BLACK if "UIDT" in label else UIDT_RED for label in labels]

        ax.axhspan(-0.42, 0.42, color=UIDT_ROW, zorder=0)

        ax.errorbar(values, ypos, xerr=errs, fmt="o", color=UIDT_BLACK,
                    ecolor=UIDT_GRAY, elinewidth=0.9, capsize=2.5, markersize=0)
        ax.scatter(values, ypos, s=36, color=colors, zorder=3)
        ax.plot(values, ypos, color="#94a3b8", linewidth=0.75, zorder=1)
        for value, y in zip(values, ypos):
            ax.text(value, y + 0.24, f"{value:g}", ha="center", va="bottom",
                    fontsize=6.8, color=UIDT_GRAY)

        ax.set_yticks(ypos)
        ax.set_yticklabels(["UIDT", "DESI DR2"])
        ax.set_xlabel(xlabel)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(-0.55, len(panel_rows) - 0.45)
        ax.invert_yaxis()
        ax.grid(axis="x", color=UIDT_LIGHT, linewidth=0.55)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.spines["bottom"].set_color("#94a3b8")
        ax.tick_params(axis="y", length=0)
        ax.text(0.02, 0.95, note, transform=ax.transAxes, ha="left", va="top",
                fontsize=6.8, color=UIDT_GRAY)

    axes[0].set_title("DESI/UIDT stress-test", loc="left", fontweight="bold", pad=5)
    save(fig, "fig_desi_uidt_tension")


def figure_falsification_exposure() -> None:
    rows = read_csv("falsification_exposure.csv")
    level_style = {
        "theory-level": (UIDT_RED, UIDT_MUTED_RED, "theory"),
        "pillar-level": (UIDT_BLUE, UIDT_MUTED_BLUE, "pillar"),
        "prediction-level": (UIDT_GREEN, UIDT_MUTED_GREEN, "prediction"),
    }
    short_threshold = {
        "F1": r"lattice excludes $\Delta$ at $>3\sigma$",
        "F2": r"$E_T\!\to0 \Rightarrow \Sigma_T=0$",
        "F3": r"$w=-1.000\pm0.005$ or $w_0>-0.90$",
        "F4": r"$n_{\rm crit}\ne\gamma$",
        "F5": r"no $0^{++}$ signal in 1.5--1.9 GeV",
        "F6": r"anchor ratio deviates at $>3\sigma$",
    }

    fig, ax = plt.subplots(figsize=(6.7, 2.75), constrained_layout=True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.0, 0.985, "Falsification exposure", ha="left", va="top",
            fontsize=9.0, fontweight="bold", color=UIDT_BLACK)

    header_y = 0.885
    ax.text(0.02, header_y, "ID", fontsize=6.8, fontweight="bold", color=UIDT_GRAY)
    ax.text(0.12, header_y, "target", fontsize=6.8, fontweight="bold", color=UIDT_GRAY)
    ax.text(0.39, header_y, "tag", fontsize=6.8, fontweight="bold", color=UIDT_GRAY)
    ax.text(0.50, header_y, "level", fontsize=6.8, fontweight="bold", color=UIDT_GRAY)
    ax.text(0.68, header_y, "threshold", fontsize=6.8, fontweight="bold", color=UIDT_GRAY)

    y0 = 0.81
    row_h = 0.118
    for idx, row in enumerate(rows):
        y = y0 - idx * row_h
        if idx % 2 == 0:
            ax.add_patch(Rectangle((0.0, y - 0.073), 1.0, 0.097, facecolor=UIDT_ROW,
                                   edgecolor="none", zorder=0))
        fg, bg, level_label = level_style[row["level"]]
        ax.text(0.02, y - 0.025, row["kill_switch"], fontsize=7.5, fontweight="bold",
                color=UIDT_BLACK, va="center")
        ax.text(0.12, y - 0.025, row["target"], fontsize=7.2, color=UIDT_BLACK, va="center")
        ax.text(0.39, y - 0.025, row["evidence_tag"], fontsize=7.0, color=UIDT_GRAY, va="center")
        ax.add_patch(Rectangle((0.50, y - 0.053), 0.125, 0.052, facecolor=bg,
                               edgecolor=fg, linewidth=0.55))
        ax.text(0.562, y - 0.027, level_label, fontsize=6.6, color=fg,
                ha="center", va="center")
        ax.text(0.68, y - 0.025, short_threshold[row["kill_switch"]],
                fontsize=6.85, color=UIDT_GRAY, va="center")

    save(fig, "fig_falsification_exposure")


def main() -> None:
    figure_eft_dimensions()
    figure_desi_tension()
    figure_falsification_exposure()


if __name__ == "__main__":
    main()
