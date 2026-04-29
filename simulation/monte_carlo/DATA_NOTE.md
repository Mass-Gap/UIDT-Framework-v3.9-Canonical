# Data Note: Large File (UIDT_MonteCarlo_samples_100k.csv)

The primary raw data file `UIDT_MonteCarlo_samples_100k.csv` (~19 MB, 100,000 rows)
cannot be tracked in this repository due to GitHub file-size recommendations
for large tabular data.

## Canonical Source

The full 100k sample chain is archived at Zenodo:

> **DOI:** https://doi.org/10.5281/zenodo.17554179  
> **File:** `UIDT_MonteCarlo_samples_100k.csv`  
> **SHA256:** verify via Zenodo record

## Local Reproduction

The samples can be regenerated from the UIDT simulation pipeline:

```bash
python simulation/UIDTv3_6_1_HMC_Real.py --samples 100000 --thinning 10 \
  --output simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv
```

All derived statistics in `UIDT_MonteCarlo_summary.csv` and
`UIDT_HighPrecision_mean_values.csv` are fully reproducible from this source.

## Evidence Category

- Δ* = 1.710 ± 0.015 GeV → **[A]** (mathematically proven)
- γ = 16.339 / γ∞ = 16.3437 → **[A-]** (phenomenological parameter)
- Ψ ≈ 1291.76 → **[A-]** (derived from γ via near-exact linear relation r=0.9995)
