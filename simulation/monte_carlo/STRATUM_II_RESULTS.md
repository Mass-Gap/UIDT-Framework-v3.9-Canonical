# Stratum II — Physical Interpretation Layer

**Stratum II interprets the Stratum I numerical results in the context of
established physics and UIDT framework concepts.**
All claims carry explicit evidence-category labels.
No cosmological conclusions are drawn in this file — see Stratum III.

**Version:** 2026-04-29 (precision update)

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
| γ∞(MC-propagated) | 16.36925 ± 1.00513 | [B] |
| 68 % CI | [15.364, 17.374] | [B] |
| p-value vs canonical γ∞ = 16.3437 | 0.9797 | [A] |

**Interpretation [B]:** The MC posterior is consistent with the canonical bare-gamma
extrapolation. The canonical finite-size-scaling uncertainty (±10⁻⁴) and the MC
uncertainty (±1.005) describe complementary aspects of the same physical quantity
and must **not** be added in quadrature.

---

## 2. Kinetic-VEV Anti-Correlation

**Source:** `UIDT_MonteCarlo_correlation_matrix.csv`

| Correlation | Value | Category |
|---|---|---|
| r(γ, kinetic_VEV) | −0.982130546 | [B] |

**Interpretation [B]:** The strong anti-correlation r ≈ −0.982 between γ and
the kinetic vacuum expectation value is consistent with the anti-proportional
coupling and with the 2.3-damping mapping documented in Appendix III of the
manuscript (`clay_appendix_mc_evidence.tex` Section 5).
This supports — but does not prove — the holographic damping picture.

---

## 3. [TENSION ALERT] — r(Δ*, Π_S)

> **[TENSION ALERT]**
>
> | Source | Value |
> |---|---|
> | Stored correlation matrix | r(Δ*, Π_S) = +0.720284420 |
> | Raw-chain audit (MC session) | **not reproduced** |
> | Δ | unresolved |
>
> **Hard conflict:** The stored `UIDT_MonteCarlo_correlation_matrix.csv` reports
> r(Δ*, Π_S) = +0.720, but the raw-chain audit appendix explicitly states
> that this value does not appear in the dataset under audit.
>
> **Consequence:** This correlation must **not** be used as an evidence-upgrade
> argument (A− → A) until a dedicated script recomputes r(Δ*, Π_S) directly
> from `UIDT_MonteCarlo_samples_100k.csv` and resolves the provenance conflict
> between the raw CSV, the summary file, and the stored correlation matrix.

---

## 4. κ–λ_S Correlation (RG Fixed-Point)

**Source:** `UIDT_MonteCarlo_correlation_matrix.csv`

| Correlation | Value | Category |
|---|---|---|
| r(κ, λ_S) | ~+0.99 | [A] |

**Interpretation [A]:** The near-unity correlation is the direct algebraic consequence
of the RG fixed-point 5κ² = 3λ_S. Parameters linked by an exact constraint must
have r → 1 in a converged chain. This is a mathematical consistency check.

> **Note:** The soft `[RG_CONSTRAINT_FAIL]` flagged in Stratum I § 5 applies to the
> hp-mean residual, not to the posterior correlation. Both must be reported
> transparently; neither may be suppressed.

---

## 5. Non-Gaussian Parameters (γ and Ψ)

**Evidence category: [A-] for γ, [B] for Ψ**

γ shows asymmetric tails consistent with its phenomenological coupling role [A-].
Ψ shows asymmetric tails whose physical origin is not yet analytically characterized.
This is identified as a topic for the planned NLO extension work and must not be
used as evidence for any current parameter-upgrade claim.
