# ⚛️ UIDT Ω Monte Carlo Validation Data (v3.3)

**Author:** Philipp Rietz  
**License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)  
**Canonical DOI (v3.2/v3.3):** [10.5281/zenodo.17554179](https://doi.org/10.5281/zenodo.17554179)  
**Status:** Validation Data (Technically Closed)

---

## 1. Overview

This directory contains the complete dataset from the final **Monte Carlo (MC) validation run** for the Unified Information-Density Theory (UIDT) Ω framework. This data serves as the non-perturbative statistical validation of the canonical parameters (Δ, γ, κ, m_S, λ_S) derived from the analytical 3-equation system.

The dataset includes the raw MC chain samples, high-precision mean values, parameter correlation matrices, and the final summary tables and plots used in the UIDT v3.3 publication.

### Key Data Artifacts

- **Raw Data:** 100,000 high-thinning samples (`UIDT_MonteCarlo_samples_100k.csv`) — primary artifact
- **High-Precision Means:** Final derived parameter values with mpmath 80-digit precision (`UIDT_HighPrecision_mean_values.csv`)
- **Correlation Analysis:** Full Pearson-r matrix (`UIDT_MonteCarlo_correlation_matrix.csv`)
- **Summary Tables:** CSV and LaTeX publication tables
- **Plots:** Hexbin density, histograms, γ vs Ψ scatter (JPG)

---

## 2. File Manifest

### 2.1 Raw Simulation Data

| File | Description |
|:---|:---|
| `UIDT_MonteCarlo_samples_100k.csv` | Raw MC chain, 100k thinned samples (primary artifact) |
| `UIDT_HighPrecision_mean_values.csv` | mpmath 80-digit precision parameter means |

### 2.2 Summary Statistics & Tables

| File | Description |
|:---|:---|
| `UIDT_MonteCarlo_summary.csv` | Mean, std, 2.5%, 97.5% CI for Δ, γ, Ψ |
| `UIDT_MonteCarlo_summary_table_short.csv` | Abbreviated summary for quick reference |
| `UIDT_MonteCarlo_correlation_matrix.csv` | 8×8 Pearson-r matrix (m_S, κ, λ_S, C, α_s, Δ, γ, Ψ) |
| `UIDT_MonteCarlo_summary_table.tex` | Publication-ready LaTeX table |

### 2.3 Plots

| File | Description |
|:---|:---|
| `UIDT_joint_Delta_gamma_hexbin.jpg` | Hexbin density: Δ vs γ (100k samples) |
| `UIDT_histograms_Delta_gamma_Psi.jpg` | 1D marginal distributions for Δ, γ, Ψ |
| `UIDT_gamma_vs_Psi_scatter.jpg` | γ vs Ψ scatter (2000 random points) — confirms near-perfect linear correlation r=0.9995 |

---

## 3. Key Numerical Results

| Parameter | Mean | Std | 2.5% CI | 97.5% CI | Evidence |
|:---|:---|:---|:---|:---|:---|
| Δ* (GeV) | 1.7100444 | 0.0149928 | 1.6806964 | 1.7393990 | [A] |
| γ | 16.373948 | 1.005125 | 14.752242 | 18.275849 | [A-] |
| Ψ | 1291.759 | 159.125 | 1044.618 | 1603.232 | [A-] |

**Notable correlations (from correlation matrix):**
- r(m_S, Δ) ≈ 0.9999 — strong positive coupling
- r(γ, Ψ) ≈ 0.9995 — near-perfect linear dependence
- r(α_s, γ) ≈ −0.9499 — strong anti-correlation

**LEDGER cross-check:**
- Δ* = 1.710 ± 0.015 GeV [A] ✓ consistent with MC mean 1.7100 ± 0.0150
- γ = 16.339 [A-] ← MC mean 16.374 (δ = 0.035, within 1σ)
- γ∞ = 16.3437 [A-] ← HP mean 16.2887 (δ = 0.055, within 1σ)

---

## 4. Reproducibility

```bash
# One-command verification
python verification/tests/test_monte_carlo_summary.py
```

```python
import pandas as pd
samples = pd.read_csv('simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv')
print(samples[['Delta','gamma','Psi']].describe())
```

---

## 5. Citation

> Rietz, P. (2025). *Unified Information-Density Theory (UIDT) v3.2: Canonical Formulation,
> Mathematical Consistency, and Empirical Testability*. Zenodo.
> https://doi.org/10.5281/zenodo.17554179
