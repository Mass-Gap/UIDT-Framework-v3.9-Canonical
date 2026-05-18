"""Generate audit figures for the UIDT Ontology v3.9 manuscript.

The figures are intentionally non-decorative: they visualise dimensional
bookkeeping, external cosmology tension, and falsification exposure only.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "verification" / "data" / "visualizations"
OUT = ROOT / "manuscript" / "figures"


UIDT_BLACK = "#1f2933"
UIDT_GRAY = "#667085"
UIDT_LIGHT = "#e5e7eb"
UIDT_BLUE = "#2563eb"
UIDT_RED = "#b42318"
UIDT_GREEN = "#15803d"


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
    terms = [row["term"] for row in rows]
    dims = [float(row["operator_dimension"]) for row in rows]

    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    ypos = list(range(len(rows)))
    colors = [UIDT_RED if dim > 4 else UIDT_BLUE for dim in dims]

    ax.hlines(ypos, xmin=0, xmax=dims, color=UIDT_LIGHT, linewidth=2.2)
    ax.scatter(dims, ypos, s=58, color=colors, zorder=3)
    ax.axvline(4, color=UIDT_BLACK, linewidth=1.1, linestyle="--")
    ax.text(4.05, len(rows) - 0.35, "d = 4 boundary", fontsize=8.5, color=UIDT_BLACK)

    ax.set_yticks(ypos)
    ax.set_yticklabels(terms, fontsize=8.4)
    ax.set_xlabel("canonical operator mass dimension in 3+1 dimensions")
    ax.set_xlim(0, 5.45)
    ax.set_ylim(-0.55, len(rows) - 0.45)
    ax.invert_yaxis()
    ax.grid(axis="x", color=UIDT_LIGHT, linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title("EFT operator dimensions in Axiom 2", loc="left", fontsize=11, pad=8)
    save(fig, "fig_eft_operator_dimensions")


def figure_desi_tension() -> None:
    rows = read_csv("desi_uidt_tension.csv")
    h0 = [row for row in rows if row["observable"] == "H0"]
    w0 = [row for row in rows if row["observable"] == "w0"]

    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.4))
    panels = [
        (axes[0], h0, r"$H_0$ [km s$^{-1}$ Mpc$^{-1}$]", 67.6, 70.9),
        (axes[1], w0, r"$w_0$", -1.04, -0.76),
    ]

    for ax, panel_rows, xlabel, xmin, xmax in panels:
        labels = [row["source"] for row in panel_rows]
        values = [float(row["value"]) for row in panel_rows]
        errs = [float(row["uncertainty"]) for row in panel_rows]
        ypos = list(range(len(panel_rows)))
        colors = [UIDT_BLUE if "UIDT" in label else UIDT_RED for label in labels]

        ax.errorbar(values, ypos, xerr=errs, fmt="o", color=UIDT_BLACK,
                    ecolor=UIDT_GRAY, elinewidth=1.1, capsize=3, markersize=0)
        ax.scatter(values, ypos, s=62, color=colors, zorder=3)
        ax.set_yticks(ypos)
        ax.set_yticklabels(labels, fontsize=8.8)
        ax.set_xlabel(xlabel)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(-0.55, len(panel_rows) - 0.45)
        ax.invert_yaxis()
        ax.grid(axis="x", color=UIDT_LIGHT, linewidth=0.8)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)

    axes[0].set_title("DESI/UIDT cosmology stress-test", loc="left", fontsize=11, pad=8)
    save(fig, "fig_desi_uidt_tension")


def figure_falsification_exposure() -> None:
    rows = read_csv("falsification_exposure.csv")
    level_x = {"theory-level": 3, "pillar-level": 2, "prediction-level": 1}
    level_color = {"theory-level": UIDT_RED, "pillar-level": UIDT_BLUE, "prediction-level": UIDT_GREEN}

    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ypos = list(range(len(rows)))
    xvals = [level_x[row["level"]] for row in rows]
    colors = [level_color[row["level"]] for row in rows]
    labels = [f"{row['kill_switch']}  {row['target']}  {row['evidence_tag']}" for row in rows]

    ax.scatter(xvals, ypos, s=80, color=colors, zorder=3)
    for y, row in zip(ypos, rows):
        ax.text(3.22, y, row["threshold"], va="center", fontsize=8.0, color=UIDT_GRAY)

    ax.set_yticks(ypos)
    ax.set_yticklabels(labels, fontsize=8.4)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["prediction-level", "pillar-level", "theory-level"], fontsize=8.8)
    ax.set_xlim(0.65, 4.55)
    ax.set_ylim(-0.55, len(rows) - 0.45)
    ax.invert_yaxis()
    ax.grid(axis="x", color=UIDT_LIGHT, linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title("Falsification exposure by kill-switch level", loc="left", fontsize=11, pad=8)
    save(fig, "fig_falsification_exposure")


def main() -> None:
    figure_eft_dimensions()
    figure_desi_tension()
    figure_falsification_exposure()


if __name__ == "__main__":
    main()
