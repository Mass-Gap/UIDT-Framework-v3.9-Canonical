# GitHub Release Assets — Monte Carlo Plots

**Target release:** `v3.9-mc-validation` (to be created after PR #366 merges)
**Target PR context:** #366

The three plot JPGs listed below are too large and binary to commit directly
to the repository. They are attached as **GitHub Release Assets** to
`v3.9-mc-validation`.

---

## Asset Registry

| Filename | Type | Size (approx.) | Description |
|---|---|---|---|
| `UIDT_MC_hexbin_Delta_gamma.jpg` | JPG | ~300 KB | Hexbin density: Δ* vs γ posterior |
| `UIDT_MC_histograms_5params.jpg` | JPG | ~350 KB | Marginal histograms, 5 parameters |
| `UIDT_MC_scatter_kappa_lambdaS.jpg` | JPG | ~280 KB | Scatter: κ vs λ_S, RG track visible |

---

## Reproducibility

All three plots can be regenerated locally from the raw CSV:

```bash
# 1. Download raw CSV from Zenodo (19 MB)
curl -L -o simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv \
  "https://zenodo.org/records/17554179/files/UIDT_MonteCarlo_samples_100k.csv"

# 2. Generate all three plots
python simulation/monte_carlo/generate_mc_plots.py \
  --raw    simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv \
  --outdir simulation/monte_carlo/plots/
```

Outputs:
```
simulation/monte_carlo/plots/UIDT_MC_hexbin_Delta_gamma.jpg
simulation/monte_carlo/plots/UIDT_MC_histograms_5params.jpg
simulation/monte_carlo/plots/UIDT_MC_scatter_kappa_lambdaS.jpg
```

---

## Upload Procedure (manual, after PR #366 merges)

1. Go to: https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/releases/new
2. **Tag:** `v3.9-mc-validation`
3. **Target:** `main` (after merge)
4. **Title:** `UIDT v3.9 — Monte Carlo Validation Plots`
5. **Body:** paste content from `PLOTS_REGISTRY.md`
6. **Assets:** drag and drop the three JPG files
7. Publish release

Alternatively via GitHub CLI:

```bash
gh release create v3.9-mc-validation \
  --title "UIDT v3.9 — Monte Carlo Validation Plots" \
  --notes-file simulation/monte_carlo/PLOTS_REGISTRY.md \
  --target main \
  simulation/monte_carlo/plots/UIDT_MC_hexbin_Delta_gamma.jpg \
  simulation/monte_carlo/plots/UIDT_MC_histograms_5params.jpg \
  simulation/monte_carlo/plots/UIDT_MC_scatter_kappa_lambdaS.jpg
```

---

## LEDGER Values Used in Plots

All reference lines in the plots use immutable LEDGER constants:

| Constant | Value | Category |
|---|---|---|
| Δ* | 1.710 ± 0.015 GeV | [A] |
| γ | 16.339 | [A-] |
| γ∞ | 16.3437 | [A-] |
| RG track | 5κ² = 3λ_S | [A] |

Caption note (mandatory in all figures):
> "Dashed/dotted reference lines indicate UIDT LEDGER values
> (category [A]/[A-]); they are not external experimental measurements."

---

## Evidence Categories of Plots

| Plot | Content category | Interpretation layer |
|---|---|---|
| Hexbin Δ* vs γ | [A] (raw posterior) | Stratum I |
| Histograms 5 params | [A] (raw posterior) | Stratum I |
| Scatter κ vs λ_S | [A] (RG track) | Stratum I / II |
