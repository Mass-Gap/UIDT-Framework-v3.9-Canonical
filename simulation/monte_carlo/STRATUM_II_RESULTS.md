# Stratum II — Physical Interpretation Layer

**Stratum II interprets Stratum I numerical results in the context of
established physics and UIDT framework concepts.**
All claims carry explicit evidence-category labels.
No cosmological conclusions are drawn in this file — see Stratum III.

**Version:** 2026-04-29 — `[TENSION ALERT] r(Δ*,Π_S)` RESOLVED via raw-chain audit.

---

## 1. Bare-Gamma Posterior Propagation

**Source:** finite-size scaling extrapolation in `docs/bare_gamma_theorem.md`
DOI: [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

Canonical repository values:

| Quantity | Value | Category |
|---|---|---|
| γ_phys (dressed) | 16.339 | [A-] |
| γ∞ (bare, extrapolated) | 16.3437 ± 1 × 10⁻⁴ | [B] |
| δγ | 0.0047 | [B/D] |

From MC γ-posterior (Stratum I):

| Quantity | Value | Category |
|---|---|---|
| γ∞ (MC-propagated) | 16.36925 ± 1.00513 | [B] |
| 68 % CI | [15.364, 17.374] | [B] |
| p-value vs canonical γ∞ = 16.3437 | 0.9797 | [A] |

**Interpretation [B]:** The MC posterior is consistent with the canonical bare-gamma
extrapolation. The canonical finite-size-scaling uncertainty (±10⁻⁴) and the MC
uncertainty (±1.005) describe complementary aspects of the same physical quantity
and must **not** be added in quadrature.

---

## 2. Kinetic-VEV Anti-Correlation

**Source:** `UIDT_MonteCarlo_correlation_matrix.csv` + raw-chain recomputation

| Correlation | Stored value | Raw-chain recomputed | Δ | Status |
|---|---|---|---|---|
| r(γ, kinetic_VEV) | −0.982130546 | **−0.985860** | 0.003729 | ✅ OK (< 0.05) |

**Interpretation [B]:** The strong anti-correlation r ≈ −0.983…−0.986 between γ and
the kinetic vacuum expectation value is consistent with anti-proportional coupling
and with the 2.3-damping mapping (Appendix III, `clay_appendix_mc_evidence.tex` §5).
The minor discrepancy between stored and recomputed values (|Δr| = 0.0037) is
within the accepted tolerance and does not constitute a tension.

---

## 3. ~~[TENSION ALERT]~~ r(Δ*, Π_S) — **RESOLVED** ✅

> **RESOLVED 2026-04-29** via `verify_monte_carlo_research_notes.py`
>
> | Source | r(Δ*, Π_S) |
> |---|---|
> | Previously cited value | +0.720284420 |
> | Raw-chain (`UIDT_MonteCarlo_samples_100k.csv`, N=100 000) | **+0.015798** |
> | Δ | 0.704487 |
>
> **Root cause:** The stored `UIDT_MonteCarlo_correlation_matrix.csv` does **not**
> contain a `Pi_S` column. The value +0.720 was cited from an unidentified source and
> erroneously attributed to the correlation matrix. It does not appear in the
> raw chain.
>
> **Consequence:** r(Δ*, Π_S) = **+0.0158** from the raw chain — Δ* and Π_S are
> statistically **uncorrelated**. No evidence-upgrade conflict exists.
> The previously planned A⁻ → A upgrade for this pair is **not warranted** by the data.

---

## 4. Full 28-Pair Stored-Matrix Audit

All 28 overlapping pairs (8-parameter stored matrix vs raw chain):

- **0 TENSION ALERTS** — all pairs within |Δr| < 0.05
- Maximum discrepancy: r(γ, kinetic_VEV), |Δr| = 0.0037

Script: `verification/scripts/verify_monte_carlo_research_notes.py`
Output: `verification_audit_report.json` (generated per run, not tracked in repo)

---

## 5. κ–λ_S Correlation (RG Fixed-Point)

| Correlation | Raw-chain value | Category |
|---|---|---|
| r(κ, λ_S) | **+0.9994** | [A] |

**Interpretation [A]:** Near-unity correlation is the algebraic consequence of
5κ² = 3λ_S. Parameters linked by an exact constraint must have r → 1 in a converged
chain.

> ⚠️ **[RG_CONSTRAINT_FAIL] remains open** (Stratum I §5):
> The hp-mean residual |5κ²(hp) − 3λ_S(MC)| ≈ 9.9 × 10⁻⁴ >> 1 × 10⁻¹⁴.
> This flag does not contradict the posterior correlation but indicates the
> hp-mean file requires an independent λ_S precision determination.

---

## 6. Non-Gaussian Parameters (γ and Ψ)

**Evidence category: [A-] for γ, [B] for Ψ**

γ shows asymmetric tails consistent with its phenomenological coupling role.
Ψ shows asymmetric tails whose physical origin is not yet analytically characterised.
Neither parameter is a candidate for an evidence-category upgrade based on shape
alone. Both must be treated with a non-Gaussian posterior approximation in any
future analytical propagation.
