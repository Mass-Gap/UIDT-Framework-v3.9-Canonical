# Monte Carlo Research Results — Audit Index

**UIDT Framework v3.9** | Maintainer: P. Rietz
**Canonical DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)
**Dataset DOI:** [10.5281/zenodo.17554179](https://doi.org/10.5281/zenodo.17554179)
**Date:** 2026-04-29

---

This index document provides navigation into the stratified Monte Carlo audit results.
All files in this directory follow the UIDT Evidence PR Rules:
explicit Stratum I / II / III separation, a Claims Table, a Reproduction Note,
and DOI/arXiv traceability for every external numeric value.

---

## Directory Contents

| File | Stratum | Purpose |
|---|---|---|
| `STRATUM_I_RESULTS.md` | I | Direct numerical audit from raw chain — no interpretation |
| `STRATUM_II_RESULTS.md` | II | Physical interpretation layer with evidence caps |
| `STRATUM_III_RESULTS.md` | III | UIDT mapping, lattice comparison, publication positioning |
| `PR_CLAIMS_TABLE.md` | — | Pull-request claim registry for this integration |
| `PLOTS_REGISTRY.md` | — | Catalog of all three diagnostic plots (Hexbin, Histogramm, Scatter) |
| `DATA_NOTE.md` | — | Data provenance and Zenodo reference |

---

## Critical Status Flags

> **[TENSION ALERT]**
> `r(Δ*, Π_S) = +0.720284420` appears in the stored correlation matrix
> but is **not** reproduced by the raw-chain audit.
> This claim must remain flagged until the stored matrix and raw CSV
> are cross-verified in a dedicated reproducibility script.

> **Cosmological claims are capped at Category [C] maximum.**
> Any Ψ → w_a mapping derived from the MC posterior must be labelled [D] (prediction).
> The canonical cosmology path remains the bare-gamma holographic dressing route.

---

## Reproduction Note (one command)

```bash
pytest verification/tests/test_monte_carlo_summary.py -v
```

A full raw-chain reproducibility script is pending:
`verification/scripts/verify_monte_carlo_research_notes.py`
See `STRATUM_I_RESULTS.md` Section 6 for the planned script responsibilities.
