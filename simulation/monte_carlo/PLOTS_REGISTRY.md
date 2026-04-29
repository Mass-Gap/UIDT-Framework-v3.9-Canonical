# Monte Carlo Plots Registry

This file documents the three diagnostic plots for the UIDT Monte Carlo validation run (v3.3).
All plots were generated from `UIDT_MonteCarlo_samples_100k.csv` (N=100,000).

## Canonical Source

All three JPG files are archived at Zenodo:

> **DOI:** https://doi.org/10.5281/zenodo.17554179  
> **Dataset:** UIDT Ω Monte Carlo Validation Data (v3.3)

---

## Plot Manifest

### 1. `UIDT_joint_Delta_gamma_hexbin.jpg` (~366 KB)

**Title:** Hexbin density: Delta vs gamma (100k)  
**Type:** 2D hexbin density map  
**Axes:** x = Delta (GeV) [1.64–1.78], y = gamma [14–19]  
**Color scale:** Counts per hexbin (0–25+, viridis)  
**Key features:**
- Peak density at Δ ≈ 1.710 GeV, γ ≈ 15.5–16.0
- Broad γ-axis distribution (std ≈ 1.005) vs. narrow Δ distribution (std ≈ 0.015)
- Confirms marginal independence: r(Δ, γ) ≈ 0.138 (weak positive correlation)

**Evidence:** [A] for Δ*, [A-] for γ

---

### 2. `UIDT_histograms_Delta_gamma_Psi.jpg` (~202 KB)

**Title:** Delta distribution (100k) | gamma distribution (100k) | Psi distribution (100k)  
**Type:** 1D marginal histograms (3-panel)  
**Key features:**
- **Delta:** Near-Gaussian, peak at ≈ 1.710–1.712 GeV, consistent with LEDGER 1.710 ± 0.015 GeV [A]
- **gamma:** Right-skewed distribution, peak at ≈ 15.3–15.5, long tail to ≈ 19
- **Psi:** Right-skewed, peak at ≈ 1100–1200, tail to ≈ 1800; mirrors gamma shape (r=0.9995)

**Evidence:** [A] for Δ*, [A-] for γ, [A-] for Ψ

---

### 3. `UIDT_gamma_vs_Psi_scatter.jpg` (~87 KB)

**Title:** gamma vs Psi (2000 random points)  
**Type:** Scatter plot (random 2000-point subsample)  
**Axes:** x = gamma [14–19], y = Psi (sampled subset) [980–1750]  
**Key features:**
- Near-perfect linear relationship with minimal scatter
- r(γ, Ψ) = 0.9995 confirmed (from correlation matrix)
- Slope ≈ 78.9 (Psi/gamma ratio)
- Confirms Ψ is a near-deterministic function of γ

**Evidence:** [A-] (derived linear relationship)

---

## Reproduction

```python
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Download samples from Zenodo DOI: 10.5281/zenodo.17554179
df = pd.read_csv('UIDT_MonteCarlo_samples_100k.csv')

# Plot 1: Hexbin
fig, ax = plt.subplots(figsize=(8, 8))
ax.hexbin(df['Delta'], df['gamma'], gridsize=50, cmap='inferno')
ax.set_xlabel('Delta (GeV)')
ax.set_ylabel('gamma')
ax.set_title('Hexbin density: Delta vs gamma (100k)')
plt.colorbar(ax.collections[0], ax=ax)
fig.savefig('UIDT_joint_Delta_gamma_hexbin.jpg', dpi=150, bbox_inches='tight')
plt.close()

# Plot 2: Histograms
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col, title in zip(axes,
    ['Delta', 'gamma', 'Psi'],
    ['Delta distribution (100k)', 'gamma distribution (100k)', 'Psi distribution (100k)']):
    ax.hist(df[col], bins=100, density=(col=='Psi'))
    ax.set_title(title)
fig.savefig('UIDT_histograms_Delta_gamma_Psi.jpg', dpi=150, bbox_inches='tight')
plt.close()

# Plot 3: Scatter
sample = df.sample(2000, random_state=42)
fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(sample['gamma'], sample['Psi'], alpha=0.3, s=10)
ax.set_xlabel('gamma (sampled subset)')
ax.set_ylabel('Psi (sampled subset)')
ax.set_title('gamma vs Psi (2000 random points)')
fig.savefig('UIDT_gamma_vs_Psi_scatter.jpg', dpi=150, bbox_inches='tight')
plt.close()
```
