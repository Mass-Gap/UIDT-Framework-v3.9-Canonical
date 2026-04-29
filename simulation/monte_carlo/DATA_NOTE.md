# Data Note — Monte Carlo Simulation Files

## Summary

This directory contains **aggregated outputs** of the UIDT v3.9 Monte Carlo
validation (N = 100 000 thinned samples). The full raw chain lives on Zenodo.

---

## Files Present (tracked in Git)

| File | Size | Description |
|---|---|---|
| `UIDT_MonteCarlo_summary.csv` | 263 B | 5-number summary per parameter |
| `UIDT_MonteCarlo_summary_table_short.csv` | 263 B | Short-form table for LaTeX |
| `UIDT_MonteCarlo_summary_table.tex` | 444 B | Full LaTeX tabular |
| `UIDT_MonteCarlo_correlation_matrix.csv` | 1.3 KB | 8×8 Pearson correlation matrix |
| `UIDT_HighPrecision_mean_values.csv` | 696 B | hp-precision mean values |
| `PLOTS_REGISTRY.md` | — | Axis specs + reproduction code for all 3 JPGs |
| `STRATUM_II_RESULTS.md` | — | Physical interpretation layer |

---

## Files NOT in Git (too large / binary)

### 19 MB Raw-Chain CSV (`samples_100k`)

| Property | Value |
|---|---|
| **Filename** | `UIDT_MonteCarlo_samples_100k.csv` |
| **Size** | ~19 MB |
| **DOI (Zenodo)** | [10.5281/zenodo.17554179](https://doi.org/10.5281/zenodo.17554179) |
| **N** | 100 000 |
| **Columns** | Delta, gamma, Psi, kappa, lambda_S, kinetic_VEV, Pi_S, sigma_8_pred, H0_pred, rho_vac_pred |

Download:
```bash
wget "https://zenodo.org/records/17554179/files/UIDT_MonteCarlo_samples_100k.csv"
mv UIDT_MonteCarlo_samples_100k.csv simulation/monte_carlo/
```

Verify (SHA-256):
```bash
sha256sum simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv
```

### 3 Diagnostic Plot JPGs

| File | Size | Content |
|---|---|---|
| `UIDT_joint_Delta_gamma_hexbin.jpg` | 366 KB | Hexbin joint posterior Δ* vs γ |
| `UIDT_histograms_Delta_gamma_Psi.jpg` | 202 KB | Marginal histograms Δ*, γ, Ψ |
| `UIDT_gamma_vs_Psi_scatter.jpg` | 87 KB | Scatter γ vs Ψ (N=5 000 subsample) |

All three are available as **GitHub Release Assets** under tag `v3.9-mc-plots`.
See `docs/RELEASE_ASSET_GUIDE.md` for upload instructions.

Reproduce from raw CSV:
```bash
# ensure samples_100k.csv is present (see above)
python verification/scripts/verify_monte_carlo_research_notes.py \\
    --csv simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv \\
    --stored-corr simulation/monte_carlo/UIDT_MonteCarlo_correlation_matrix.csv \\
    --hp-mean simulation/monte_carlo/UIDT_HighPrecision_mean_values.csv
```

See `PLOTS_REGISTRY.md` for exact matplotlib reproduction code.

---

## Rationale for Hybrid Storage

| Artefact | Where | Why |
|---|---|---|
| Summary CSVs, LaTeX | Git | Version-controlled, diff-able, ≤10 KB |
| Raw 19 MB CSV | Zenodo | Permanent DOI, large binary, not diff-able |
| Plot JPGs | GitHub Release | Binary, project-scoped, easy download; not commit noise |

Git LFS is available as a fallback (`.gitattributes` track `*.jpg *.csv`) but
not required for current file sizes.
