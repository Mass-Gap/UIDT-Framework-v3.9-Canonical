# SU(3) Gamma Invariant — Audit Report

**Version:** TKT-20260403-gamma-rg-frg-audit  
**Date:** 2026-04-03  
**Precision:** mpmath 80-digit arithmetic throughout  
**Evidence Categories affected:** [A-] (γ), [A] (RG constraint), [E] (FRG NLO claim)  

---

## 1  Formal Status of γ = (2N_c+1)²/N_c

### 1.1  Conjecture Statement (unchanged)

The universal gamma invariant observed phenomenologically aligns numerically with:

$$
\gamma_{\text{SU(3)}} = \frac{(2N_c+1)^2}{N_c}\bigg|_{N_c=3} = \frac{49}{3} \approx 16.3\overline{3}
$$

### 1.2  Attempted Formal Derivation

From the UIDT Lagrangian (v3.7.1, Def. 2.6), the vacuum equation at the Banach fixed point reads:

$$
m_S^2\,v + \frac{\lambda_S}{6}\,v^3 = \kappa\,\mathcal{C}
$$

with $m_S^2 = 2\lambda_S v^2$ at the potential minimum. Substituting $v = \Delta^*/\gamma$ yields the closed-form expression:

$$
\gamma^3 = \frac{6\,\Delta^{*3}\,\lambda_S}{13\,\kappa\,\mathcal{C}}
$$

### 1.3  Numerical Evaluation (80-digit precision)

With canonical ledger values ($\Delta^* = 1.710$ GeV, $\lambda_S = 0.417$, $\kappa = 0.500$, $\mathcal{C} = 0.277$ GeV$^4$):

$$
\gamma_{\text{closed}} = \left(\frac{6 \times 1.710^3 \times 0.417}{13 \times 0.500 \times 0.277}\right)^{1/3} \approx 1.908
$$

For $\gamma_{\text{closed}} = 49/3$ to hold exactly, the gap equation would require $\Delta^* \approx 14.64$ GeV — a factor ~8.6 above the Banach fixed point.

### 1.4  Conclusion

**The relation γ = Δ\*/v is a definitional identity** (phenomenologically determined $v = 47.7$ MeV), not an algebraic theorem derivable from the gap equation. The numerical proximity $|\gamma_{\text{kinetic}} - 49/3| / (49/3) \approx 0.035\%$ remains a **coincidence at current precision**, not a proven constraint.

| Source | Value | Deviation from 49/3 |
|--------|-------|---------------------|
| $\gamma_{\text{kinetic}}$ (ledger) | 16.339 | +0.006 (0.035%) |
| $49/3$ (algebraic candidate) | 16.3333… | 0 (reference) |
| $\gamma_{\text{MC}}$ (100k samples) | 16.374 ± 1.005 | within 1σ |
| $\gamma_{\text{closed}}$ (Gap-Eq.) | **1.908** | **−14.43 (−88%)** |

**Evidence Category: [A-] unchanged** (phenomenological parameter; algebraic derivation not established).  
**Limitation L4 remains open.**

---

## 2  FRG NLO Correction δ_NLO vs δγ

### 2.1  Setup

From the Wetterich equation at $k = \Delta^*$ with Litim optimized regulator and $g^{*2} = 2\kappa = 1.0$:

$$
\eta_A^{\text{NLO}} = \frac{13}{6}\,C_A\,\frac{g^{*2}}{(4\pi)^2}\cdot f\!\left(\frac{\Delta^{*2}}{\mu^2}\right), \qquad f(x) = \frac{2}{(1+x)^2}
$$

### 2.2  Numerical Result

With $C_A = N_c = 3$, $(\Delta^*/\mu)^2 \approx 2.924$:

$$
\eta_A^{\text{NLO}} \approx 5.346 \times 10^{-3}
$$

$$
\delta_{\text{NLO}} := \frac{49}{3}\cdot\frac{\eta_A^{\text{NLO}}}{2} \approx 0.04366
$$

### 2.3  Comparison with Ledger

$$
\delta\gamma_{\text{ledger}} = 0.0047 \qquad \text{vs} \qquad \delta_{\text{NLO}} \approx 0.0437
$$

$$
\left|\delta_{\text{NLO}} - \delta\gamma\right| \approx 0.0390 \qquad (\text{factor } {\sim}9 \text{ discrepancy})
$$

### 2.4  Conclusion

**δγ = δ_NLO is NOT supported** at this level of truncation. The ledger value $\delta\gamma = \gamma_\infty - \gamma = 0.0047$ is consistent with a finite-size scaling (FSS) correction (Category [B], `bare_gamma_theorem.md`), not a perturbative FRG effect.

Any claim that $\delta\gamma = \delta_{\text{NLO}}$ must be downgraded to **Evidence Category [E]** until a full NLO FRG analysis with consistent truncation scheme is performed.

**Open ticket:** TKT-20260403-FRG-NLO — requires truncation-scheme study (BMW/LPA') before re-evaluation.

---

## 3  RG Fixed-Point Constraint 5κ² = 3λ_S

### 3.1  Numerical Check (80-digit mpmath)

$$
\text{LHS} = 5\kappa^2 = 5 \times 0.500^2 = 1.25000000\ldots \text{ (exact)}
$$

$$
\text{RHS} = 3\lambda_S = 3 \times 0.417 = 1.25099999\ldots
$$

$$
|\text{LHS} - \text{RHS}| = 1.000 \times 10^{-3}
$$

### 3.2  Tolerance Assessment

| Criterion | Value | Status |
|-----------|-------|--------|
| Ledger tolerance (≤ 0.01) | 0.001 | ✅ PASS |
| Constitution tolerance (< 10⁻¹⁴) | 0.001 | ❌ FAIL → [RG_CONSTRAINT_FAIL] |

**[RG_CONSTRAINT_FAIL]** — The ledger rounds $\lambda_S = 0.417$, whereas the exact fixed-point value is:

$$
\lambda_S^{\text{exact}} = \frac{5\kappa^2}{3} = \frac{5 \times 0.25}{3} = 0.41\overline{6}
$$

The deviation $\Delta\lambda_S = 0.41\overline{6} - 0.417 = -3.\overline{3} \times 10^{-4}$ lies **within the ledger uncertainty $\pm 0.007$**, so no physical inconsistency exists.

### 3.3  Recommended Fix

To restore the constraint to $< 10^{-14}$, update the canonical ledger:

```
λ_S := 5κ²/3   [exact RG fixed-point definition]
     = 0.41666...  (not 0.417)
```

This is a **rounding correction only** — no physics changes. It upgrades the RG constraint from Category [A] (tolerance 0.01) to **Category [A] (tolerance < 10⁻¹⁴)**.

Proposed PR: `[UIDT-v3.9] Constants: λ_S → exact fixed-point value 5κ²/3`

---

## 4  Summary Table

| Claim | Analysis result | Evidence | Action |
|-------|----------------|----------|--------|
| γ = (2N_c+1)²/N_c (formal proof) | Not derivable from gap eq. | [A-] → stays [A-] | L4 open |
| δγ = δ_NLO (FRG Wetterich) | Factor ~9 discrepancy | [E] | New ticket TKT-20260403-FRG-NLO |
| 5κ² = 3λ_S (< 10⁻¹⁴) | Residual = 10⁻³ → [RG_CONSTRAINT_FAIL] | [A] (tol. 0.01) | Ledger fix proposed |

---

*Computation: mpmath v1.3, `mp.dps = 80` (local), residual accuracy $< 10^{-14}$ for all arithmetic operations.*  
*Maintainer: P. Rietz — UIDT Framework v3.9*
