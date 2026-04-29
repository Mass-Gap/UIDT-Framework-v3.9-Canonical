# Monte Carlo Plot Registry

All three publication-quality diagnostic plots for the UIDT v3.9 MC validation.

**Dataset:** `UIDT_MonteCarlo_samples_100k.csv`
Zenodo: [10.5281/zenodo.17554179](https://doi.org/10.5281/zenodo.17554179)
(N = 100 000 thinned samples, 10 parameters)

**Status:** JPG files are tracked as GitHub Release Assets
→ Release tag: `v3.9-mc-plots` (see PR FU-2)

---

## Plot 1 — Joint Density: Δ* vs γ (Hexbin)

**File:** `UIDT_joint_Delta_gamma_hexbin.jpg` (366 KB)
**Type:** Hexbin density plot

| Axis | Parameter | Unit |
|---|---|---|
| x | Δ* (Delta_star / Delta) | GeV |
| y | γ (gamma) | dimensionless |

**Key values visible:**
- LEDGER Δ* = 1.710 GeV (reference line)
- LEDGER γ = 16.339 (reference line)
- r(Δ*, γ) = +0.138 (Stratum I; near-independent)

**Evidence category:** [A] (direct raw-chain density)

**Reproduction:**
```python
import mpmath as mp
mp.dps = 80
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv')
fig, ax = plt.subplots(figsize=(8, 6))
hb = ax.hexbin(df['Delta'], df['gamma'], gridsize=60, cmap='viridis', mincnt=1)
plt.colorbar(hb, ax=ax, label='counts')
ax.axvline(1.710, color='white', lw=1.2, ls='--', label='LEDGER Δ*')
ax.axhline(16.339, color='white', lw=1.2, ls=':', label='LEDGER γ')
ax.set_xlabel('Δ* [GeV]')
ax.set_ylabel('γ')
ax.set_title('Joint posterior Δ* vs γ (N=100 000)')
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig('UIDT_joint_Delta_gamma_hexbin.jpg', dpi=150)
```

---

## Plot 2 — Marginal Histograms: Δ*, γ, Ψ

**File:** `UIDT_histograms_Delta_gamma_Psi.jpg` (202 KB)
**Type:** 3-panel histogram (100 bins each)

| Panel | Parameter | Shape |
|---|---|---|
| Left | Δ* | near-Gaussian |
| Centre | γ | asymmetric tails |
| Right | Ψ | asymmetric tails |

**Key values:**
- Δ*: mean = 1.710044 GeV, σ = 0.014993 GeV
- γ: mean = 16.37395, σ = 1.00513
- Ψ: asymmetric posterior, non-Gaussian

**Evidence category:** [A]

**Reproduction:**
```python
import mpmath as mp
mp.dps = 80
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv')
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, col, xlabel in zip(axes,
        ['Delta', 'gamma', 'Psi'],
        ['Δ* [GeV]', 'γ', 'Ψ']):
    ax.hist(df[col], bins=100, color='steelblue', edgecolor='none', alpha=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('counts')
plt.suptitle('Marginal posteriors: Δ*, γ, Ψ  (N=100 000)', y=1.01)
plt.tight_layout()
plt.savefig('UIDT_histograms_Delta_gamma_Psi.jpg', dpi=150)
```

---

## Plot 3 — Scatter: γ vs Ψ

**File:** `UIDT_gamma_vs_Psi_scatter.jpg` (87 KB)
**Type:** 2D scatter (alpha-blended, random subsample N=5 000)

| Axis | Parameter | Unit |
|---|---|---|
| x | γ (gamma) | dimensionless |
| y | Ψ (Psi) | dimensionless |

**Key value:**
- r(γ, Ψ) = +0.999523 (Stratum I; near-degenerate axis)

**Evidence category:** [A]

**Reproduction:**
```python
import mpmath as mp
mp.dps = 80
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv')
sub = df.sample(5000, random_state=42)
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(sub['gamma'], sub['Psi'], alpha=0.15, s=4, color='teal')
ax.set_xlabel('γ')
ax.set_ylabel('Ψ')
ax.set_title(f'γ vs Ψ  r = {df[["gamma","Psi"]].corr().loc["gamma","Psi"]:.6f}')
plt.tight_layout()
plt.savefig('UIDT_gamma_vs_Psi_scatter.jpg', dpi=150)
```

---

## Upload Checklist (FU-2 PR)

- [ ] `UIDT_joint_Delta_gamma_hexbin.jpg` uploaded as Release Asset
- [ ] `UIDT_histograms_Delta_gamma_Psi.jpg` uploaded as Release Asset
- [ ] `UIDT_gamma_vs_Psi_scatter.jpg` uploaded as Release Asset
- [ ] Release tag `v3.9-mc-plots` created and linked in `DATA_NOTE.md`
