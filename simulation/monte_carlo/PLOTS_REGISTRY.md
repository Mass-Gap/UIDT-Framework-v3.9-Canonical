# Monte Carlo Plots Registry

This file documents the diagnostic plots for the UIDT Monte Carlo validation run (v3.3).
All plots were generated from `UIDT_MonteCarlo_samples_100k.csv` (N=100,000).

## Canonical Source

All artifacts are archived at Zenodo and the official repository:

> **DOI:** https://doi.org/10.5281/zenodo.17554179  
> **Dataset:** UIDT Ω Monte Carlo Validation Data (v3.3)

---

## Plot Manifest (in `figure/` directory)

### 1. `figure/UIDT_joint_Delta_gamma_hexbin.jpg` (~358 KB)
**Title:** Hexbin density: Delta vs gamma (100k)  
**Type:** 2D hexbin density map  
**Evidence:** [A] for Δ*, [A-] for γ

### 2. `figure/UIDT_histograms_Delta_gamma_Psi.jpg` (~197 KB)
**Title:** Delta distribution | gamma distribution | Psi distribution  
**Type:** 1D marginal histograms (3-panel)  
**Evidence:** [A] for Δ*, [A-] for γ, [A-] for Ψ

### 3. `figure/UIDT_gamma_vs_Psi_scatter.jpg` (~85 KB)
**Title:** gamma vs Psi (2000 random points)  
**Type:** Scatter plot  
**Evidence:** [A-] (derived linear relationship)

### 4. `figure/UIDT_v33_Corner_Plot.png` (~490 KB)
**Title:** UIDT v3.3 10x10 Corner Plot (N=100,000)  
**Type:** Full covariance matrix visualization  
**Key features:**
- Shows posterior distributions and correlations for all 10 parameters.
- High-resolution validation of canonical constraints.

### 5. `figure/UIDT_v33_Marginal_Posteriors.png` (~150 KB)
**Title:** UIDT v3.3 Marginal Posteriors (Alle 10 Parameter)  
**Type:** KDE plots with 68/95% CI.
- Confirms statistical stability and Gaussian-like distributions for core constants.

### 6. `figure/UIDT_v33_Stratum_II_Derivations.png` (~195 KB)
**Title:** UIDT v3.3 Stratum II: Physikalische Ableitungen  
**Type:** Analysis of physical derivations (Universal scaling, w_a coupling, holographic damping, Banach fixed point).

---

## Reproduction

```python
# Full visualization suite available in verification/scripts/visualize_mc_results.py
# Requires matplotlib, seaborn, corner
```
