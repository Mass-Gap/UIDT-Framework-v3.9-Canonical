# Stratum I — Empirical Monte Carlo Audit Results

**Stratum I contains only direct numerical results from the raw chain.**
No interpretation, no UIDT mapping, no cosmological inference.
All values are derived from `UIDT_MonteCarlo_samples_100k.csv`
and cross-checked against `UIDT_MonteCarlo_summary.csv`
and `UIDT_HighPrecision_mean_values.csv`.

**Evidence category for all items in this file: [A]**
(exception: γ LEDGER consistency → [A-] because the reference value is phenomenological)

**Version:** 2026-04-29 (precision update — canonical audit values from MC session)

---

## 1. MCMC Convergence Diagnostics

All 10 parameters of the raw chain pass publication-level convergence thresholds.

| Parameter | Split-R̂ | N_eff | τ_int (steps) | Verdict |
|---|---|---|---|---|
| Δ* | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| γ | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| Ψ | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| κ | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| λ_S | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| m_S | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| kinetic_VEV | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| Π_S | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| w0 | ~1.000 | > 96 000 | ~0.50 | ✅ converged |
| ET | ~1.000 | > 96 000 | ~0.50 | ✅ converged |

**Threshold applied:** Split-R̂ < 1.01 (standard); all values satisfy < 1.001.
**N_eff threshold:** > 1 000 (standard); all values exceed 96 000.
**τ_int ≈ 0.50:** near-fully decorrelated after thinning; practical upper bound τ_int ≪ 1.

---

## 2. LEDGER Consistency Check — Δ*

**Reference (LEDGER [A]):** Δ* = 1.710 ± 0.015 GeV

| Quantity | Value |
|---|---|
| MC mean | 1.710044 GeV |
| MC std | 0.014993 GeV |
| Absolute residual vs LEDGER | 4.44 × 10⁻⁵ GeV |
| z-score (MC units) | 0.00296 |
| Two-sided p-value | 0.997636 |

**Result:** Δ* MC posterior is fully consistent with the LEDGER value.
The residual 4.44 × 10⁻⁵ GeV is three orders of magnitude smaller than the
stated ±0.015 GeV uncertainty.

---

## 3. LEDGER Consistency Check — γ

**Reference (LEDGER [A-]):** γ = 16.339

| Quantity | Value |
|---|---|
| MC mean | 16.37395 |
| MC std | 1.00513 |
| Absolute residual vs LEDGER | 0.03495 |
| z-score | −0.0348 |
| Two-sided p-value | 0.9723 |

**Result:** γ MC posterior is numerically consistent with the LEDGER value.
The large MC std (≈ 1.005) reflects the phenomenological breadth of γ as a
coupling parameter; it does not indicate a convergence problem.
The negative z-score (−0.0348) indicates the MC mean sits marginally below the
LEDGER reference, well within statistical noise.

---

## 4. Posterior Shape Statistics (all 10 parameters)

Statistics derived directly from the raw chain without any model assumption.

| Parameter | Shape classification |
|---|---|
| Δ* | near-Gaussian |
| m_S | near-Gaussian |
| κ | near-Gaussian |
| λ_S | near-Gaussian |
| kinetic_VEV | near-Gaussian |
| Π_S | near-Gaussian |
| w0 | near-Gaussian |
| ET | near-Gaussian |
| **γ** | **asymmetric tails (non-negligible skewness and kurtosis)** |
| **Ψ** | **asymmetric tails (non-negligible skewness and kurtosis)** |

**Textually established conclusion:** Δ*, m_S, κ, λ_S, kinetic_VEV, Π_S, w0,
and ET behave near-Gaussian. γ and Ψ show the most relevant deviations from
a simple Gaussian approximation.

---

## 5. RG Constraint Check

**Constraint:** 5κ² = 3λ_S (UIDT RG fixed-point [A])

The hp-mean file reports a soft RG residual that was flagged as
`[RG_CONSTRAINT_FAIL]` in the raw-chain audit appendix.

> ⚠️ **[RG_CONSTRAINT_FAIL] — open item**
>
> The residual |5κ² − 3λ_S| at the hp-mean values exceeds the
> formal tolerance 1 × 10⁻¹⁴ set in the verification suite.
> This flag was explicitly noted in the audit appendix and must
> **not** be silently smoothed over.
>
> **Required action before merge of any claim that depends on the
> RG constraint being exactly satisfied:** re-run
> `verification/tests/test_monte_carlo_summary.py` with the current
> hp-mean values and document the residual numerically.
> The test will emit `[RG_CONSTRAINT_FAIL]` if the threshold is exceeded.

---

## 6. Pending Reproducibility Script

`verification/scripts/verify_monte_carlo_research_notes.py` — to be added in a follow-up PR.

Planned responsibilities:
1. Load `UIDT_MonteCarlo_samples_100k.csv`
2. Compute split-R̂, N_eff, τ_int for all 10 parameters
3. Compute LEDGER consistency for Δ* and γ (reproduce z-scores and p-values above)
4. Compute skewness and kurtosis for all 10 parameters
5. Recompute all 45 pairwise correlations from the raw chain
6. Compare raw-chain correlations against `UIDT_MonteCarlo_correlation_matrix.csv`
7. Emit `[TENSION ALERT]` for any |Δr| > 0.05
8. Recompute 5κ² − 3λ_S from hp-mean values using `mpmath` (mp.dps=80)
9. Emit `[RG_CONSTRAINT_FAIL]` if residual exceeds 1 × 10⁻¹⁴
