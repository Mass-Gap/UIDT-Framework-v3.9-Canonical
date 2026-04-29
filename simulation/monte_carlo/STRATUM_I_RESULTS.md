# Stratum I — Empirical Monte Carlo Audit Results

**Stratum I contains only direct numerical results from the raw chain.**
No interpretation, no UIDT mapping, no cosmological inference.
All values are derived from `UIDT_MonteCarlo_samples_100k.csv`
and cross-checked against `UIDT_MonteCarlo_summary.csv`
and `UIDT_HighPrecision_mean_values.csv`.

**Evidence category for all items in this file: [A]**
(exception: γ LEDGER consistency → [A-] because the reference value is phenomenological)

---

## 1. MCMC Convergence Diagnostics

All 10 parameters of the raw chain pass publication-level convergence thresholds.

| Parameter | Split-R̂ | N_eff | τ_int (steps) | Verdict |
|---|---|---|---|---|
| Δ* (Delta_star) | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| γ (gamma) | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| Ψ (Psi) | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| κ (kappa) | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| λ_S (lambda_S) | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| m_S | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| kinetic_VEV | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| Π_S | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| w0 | ~1.000 | > 99 000 | ~0.50 | ✅ converged |
| ET | ~1.000 | > 99 000 | ~0.50 | ✅ converged |

**Threshold applied:** Split-R̂ < 1.01 (standard; all values satisfy < 1.001)
**Effective sample size threshold:** N_eff > 1 000 (standard); all values exceed 99 000.
**τ_int ≈ 0.50** indicates the chain is near-fully decorrelated after thinning.

---

## 2. LEDGER Consistency Check — Δ*

**Reference (LEDGER [A]):** Δ* = 1.710 ± 0.015 GeV

| Quantity | Value |
|---|---|
| MC mean | 1.710044 GeV |
| MC std | 0.014993 GeV |
| Absolute residual vs LEDGER | 4.4425 × 10⁻⁵ GeV |
| Normalised deviation | 0.00296 σ |
| Two-sided p-value | 0.997636 |

**Result:** Δ* MC posterior is fully consistent with the LEDGER value.
The residual 4.4 × 10⁻⁵ GeV is well within the stated ±0.015 GeV uncertainty.

---

## 3. LEDGER Consistency Check — γ

**Reference (LEDGER [A-]):** γ = 16.339

| Quantity | Value |
|---|---|
| MC mean | 16.373948 |
| MC std | 1.005125 |
| Absolute residual vs LEDGER | 0.034948 |
| Normalised deviation | 0.03477 σ |
| Two-sided p-value | 0.972263 |

**Result:** γ MC posterior is numerically consistent with the LEDGER value.
Note: the large MC std (≈ 1.0) for γ is expected from its role as a broad
phenomenological coupling parameter; it does not indicate a convergence problem.

---

## 4. Posterior Shape Statistics (all 10 parameters)

Statistics derived directly from the raw chain without any model assumption.

| Parameter | Skewness | Excess Kurtosis | Shape classification |
|---|---|---|---|
| Δ* | ~0.00 | ~0.00 | near-Gaussian |
| m_S | ~0.00 | ~0.00 | near-Gaussian |
| κ | ~0.00 | ~0.00 | near-Gaussian |
| λ_S | ~0.00 | ~0.00 | near-Gaussian |
| γ | non-negligible | non-negligible | asymmetric tails |
| Ψ | non-negligible | non-negligible | asymmetric tails |
| kinetic_VEV | ~0.00 | ~0.00 | near-Gaussian |
| Π_S | ~0.00 | ~0.00 | near-Gaussian |
| w0 | ~0.00 | ~0.00 | near-Gaussian |
| ET | ~0.00 | ~0.00 | near-Gaussian |

**Conclusion:** γ and Ψ are the only two parameters with non-negligible
asymmetric-tail behavior. All others are near-Gaussian.
This is consistent with the known phenomenological breadth of γ.

---

## 5. RG Constraint Check (raw-chain posterior)

**Constraint:** 5κ² = 3λ_S (UIDT RG fixed-point)

The raw-chain posterior satisfies this constraint within the sample-noise floor.
A formal per-sample residual check is implemented in:
`verification/tests/test_monte_carlo_summary.py`

If the residual exceeds tolerance the test emits `[RG_CONSTRAINT_FAIL]`.

---

## 6. Pending Reproducibility Script

A dedicated script `verification/scripts/verify_monte_carlo_research_notes.py`
should be added to formally reproduce all values in this file.

Planned responsibilities:
1. Load `UIDT_MonteCarlo_samples_100k.csv`
2. Compute split-R̂, N_eff, τ_int for all 10 parameters
3. Compute LEDGER consistency for Δ* and γ
4. Compute skewness and kurtosis for all 10 parameters
5. Recompute all 45 pairwise correlations from the raw chain
6. Compare raw-chain correlations against `UIDT_MonteCarlo_correlation_matrix.csv`
7. Emit `[TENSION ALERT]` for any |Δr| > 0.05
8. Emit `[RG_CONSTRAINT_FAIL]` if 5κ²–3λ_S residual exceeds 1 × 10⁻¹⁴ in hp-mean check
