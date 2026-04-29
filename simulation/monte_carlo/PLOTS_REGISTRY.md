# Monte Carlo Plots Registry

This file documents the five diagnostic plots for the UIDT Monte Carlo validation run (v3.3).
All plots were generated from `UIDT_MonteCarlo_samples_100k.csv` (N=100,000).

## Canonical Source

All artifacts are archived at Zenodo and the official repository:

> **DOI:** https://doi.org/10.5281/zenodo.17554179  
> **Dataset:** UIDT Ω Monte Carlo Validation Data (v3.3)

---

## Plot Manifest

### 1. `plots/UIDT_joint_Delta_gamma_hexbin.jpg` (~358 KB)
**Title:** Hexbin density: Delta vs gamma (100k)  
**Type:** 2D hexbin density map  
**Axes:** x = Delta (GeV) [1.64–1.78], y = gamma [14–19]  
**Evidence:** [A] for Δ*, [A-] for γ

### 2. `plots/UIDT_histograms_Delta_gamma_Psi.jpg` (~197 KB)
**Title:** Delta distribution | gamma distribution | Psi distribution  
**Type:** 1D marginal histograms (3-panel)  
**Evidence:** [A] for Δ*, [A-] for γ, [A-] for Ψ

### 3. `plots/UIDT_gamma_vs_Psi_scatter.jpg` (~85 KB)
**Title:** gamma vs Psi (2000 random points)  
**Type:** Scatter plot  
**Axes:** x = gamma [14–19], y = Psi [980–1750]  
**Evidence:** [A-] (derived linear relationship)

### 4. `plots/corner_plot_uidt_v33.png` (~940 KB)
**Title:** UIDT v3.3 Corner Plot (N=100,000)  
**Type:** Full covariance matrix visualization  
**Key features:**
- Shows posterior distributions for all parameters (Δ, γ, Ψ, κ, λ_S)
- Confirms alignment with LEDGER values (white lines)
- Demonstrates statistical convergence and marginal independence of core parameters.

### 5. `plots/convergence_diagnostics_uidt_v33.png` (~347 KB)
**Title:** UIDT v3.3 MCMC Convergence Diagnostics  
**Type:** Trace plots, autocorrelation (ACF), and Gelman-Rubin R  
**Key features:**
- **Gelman-Rubin R < 1.01**: Confirms chain convergence.
- **Effective Sample Size N_eff > 99,000**: Indicates extremely efficient sampling.
- **τ_int ≈ 0.5**: Confirms near-zero autocorrelation (ideal thinning).

---

## Reproduction

```python
# Full visualization suite available in verification/scripts/visualize_mc_results.py
# Requires matplotlib, seaborn, corner
```
