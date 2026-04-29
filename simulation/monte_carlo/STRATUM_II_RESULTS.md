# Stratum II — Physical Interpretation Layer

**Stratum II interprets the Stratum I numerical results in the context of
established physics and UIDT framework concepts.**
All claims here carry explicit evidence-category labels.
No cosmological conclusions are drawn in this file — see Stratum III.

---

## 1. Bare-Gamma Posterior Propagation

**Source:** finite-size scaling extrapolation documented in
`docs/bare_gamma_theorem.md` (DOI: [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200))

Canonical bare-gamma values:

| Quantity | Value | Category |
|---|---|---|
| γ_phys (dressed) | 16.339 | [A-] |
| γ∞ (bare, extrapolated) | 16.3437 ± 1 × 10⁻⁴ | [B] |
| δγ | 0.0047 | [B/D] |

From the MC γ-posterior (Stratum I):

| Quantity | Value | Category |
|---|---|---|
| γ∞(MC-propagated) | 16.369248 ± 1.005125 | [B] |
| 68% CI | [15.274248, 17.523387] | [B] |
| p-value vs canonical γ∞ | 0.979722 | [A] |

**Interpretation [B]:** The MC posterior is consistent with the canonical bare-gamma
extrapolation. The MC-derived uncertainty (±1.005) is wide compared to the fit
uncertainty (±1 × 10⁻⁴) because the MC chain naturally samples the full
phenomenological spread of γ, whereas the finite-size scaling fit is a
numerical extrapolation with a much narrower formal error.
These two uncertainties are complementary and must not be added in quadrature.

---

## 2. Kinetic-VEV Anti-Correlation

**Source:** `UIDT_MonteCarlo_correlation_matrix.csv`

| Correlation | Value | Category |
|---|---|---|
| r(γ, kinetic_VEV) | −0.982130546 | [B] |

**Interpretation [B]:** The strong anti-correlation r ≈ −0.98 between γ and
the kinetic vacuum expectation value is consistent with the existing holographic
damping interpretation in the UIDT framework (damping factor ~2.3 documented
in the bare-gamma theorem). This supports — but does not prove — the
anti-proportional coupling picture. The magnitude is fully reproducible from
the stored correlation matrix.

---

## 3. [TENSION ALERT] — r(Δ*, Π_S)

> **[TENSION ALERT]**
>
> | Quantity | Value | Source |
> |---|---|---|
> | r(Δ*, Π_S) stored | +0.720284420 | `UIDT_MonteCarlo_correlation_matrix.csv` |
> | r(Δ*, Π_S) from raw-chain audit | not independently reproduced | raw-chain analysis |
> | Difference | unresolved | — |
>
> **Action required:** A dedicated reproducibility script must recompute r(Δ*, Π_S)
> directly from `UIDT_MonteCarlo_samples_100k.csv` and compare against the stored matrix.
> Until this is done, r(Δ*, Π_S) = +0.720 must **not** be used as an evidence-upgrade argument.

---

## 4. κ–λ_S Strong Correlation (RG Fixed-Point)

**Source:** `UIDT_MonteCarlo_correlation_matrix.csv` + Stratum I RG check

| Correlation | Value | Category |
|---|---|---|
| r(κ, λ_S) | ~+0.99 | [A] |

**Interpretation [A]:** The near-unity correlation r(κ, λ_S) ≈ +0.99 is the
expected direct consequence of the RG fixed-point constraint 5κ² = 3λ_S.
Parameters linked by an exact algebraic constraint must have correlation → 1
in any correctly converged MC chain. This is a mathematical consistency check,
not a new physical result.

---

## 5. Non-Gaussian Parameters (γ and Ψ)

**Evidence category: [A-] for γ, [B] for Ψ**

Both γ and Ψ show the strongest asymmetric-tail behavior in their marginalized
posteriors. For γ this is expected: it is a phenomenological coupling parameter [A-]
whose posterior naturally reflects the width of the phenomenological fit.
For Ψ the non-Gaussianity indicates parameter degeneracies or non-linear
couplings that are present in the MC chain but not yet analytically characterized.
This is flagged as a topic for the planned NLO extension work.
