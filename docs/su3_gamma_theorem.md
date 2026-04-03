# The SU(3) Gamma Conjecture

**Version:** TKT-20260403-gamma-epistemic-audit  
**Evidence Category:** [A-] (Numerical match with algebraic candidate — conjecture only)  
**Status for L4:** `OPEN — no formal proof from Gap/VEV equations`

## Conjecture Statement

The universal gamma invariant $\gamma$ observed phenomenologically in the UIDT vacuum energy density aligns numerically with the algebraic representation of the $SU(N_c)$ color constraint, specifically at $N_c = 3$:

$$
\gamma_{\text{SU(3)}} = \frac{(2N_c + 1)^2}{N_c}\bigg|_{N_c=3} = \frac{49}{3} = 16.\overline{3}
$$

## Epistemic Status — Explicit Limitation

> **[A-] CONJECTURE — NOT A FORMAL PROOF**
>
> The relation $\gamma = 49/3$ is a **numerical coincidence** at the 0.037% level.  
> A formal algebraic derivation from the Banach fixed-point Gap equation and the UIDT
> VEV equation (Def. 2.6) does **not** reproduce $49/3$.
>
> Derivation attempt (TKT-20260403, mp.dps=80, residual verified):
> $$\gamma^3 = \frac{6\Delta^{*3}\,\lambda_S}{13\,\kappa\,\mathcal{C}} \approx 1.91^3 \neq (49/3)^3$$
> To obtain $\gamma = 49/3$ from the Gap equation requires $\Delta^* \approx 14.6\,\text{GeV}$,
> which is inconsistent with the Banach fixed-point result $\Delta^* = 1.710 \pm 0.015\,\text{GeV}$.

## Algebraic Motivation (Structural Analogy Only)

The term $(2N_c + 1)$ correlates structurally with the dimensionality of the extended adjoint representation space plus the singlet, where the color Casimir invariant $C_2(A) = N_c$ dictates the normalization. The squared numerator is consistent with a composite color-singlet interaction in the kinetic VEV sector. This structural analogy motivates the conjecture but does not constitute a derivation.

## Numerical Comparison

| Source | Value | Deviation | Status |
|--------|-------|-----------|--------|
| $\gamma_{\text{kinetic}}$ (VEV Calibration) | 16.339 | — | Ledger [A-] |
| $\gamma_{\text{SU(3)}} = 49/3$ | 16.3333... | 0.037% | **Conjecture [A-]** |
| $\gamma_{\text{MC}}$ (100k Samples) | 16.374 ± 1.005 | within 1σ | [A-] |
| $\gamma_{\text{RG, pert.}}$ (1-loop naive) | ≈ 55.8 | ❌ Factor 3.4 | [E] |
| $\gamma_{\text{Gap eq. closed form}}$ | ≈ 1.91 | ❌ Factor 8.6 | — |

## FRG-NLO Route — Refuted (TKT-20260403)

The hypothesis $\delta\gamma = \delta_{\text{NLO}}^{\text{FRG}}$ was tested analytically using the  
Wetterich equation at $k = \Delta^*$ with the Litim optimised regulator:

$$
\delta_{\text{NLO}} = \frac{49}{3}\cdot\frac{\eta_A^{\text{NLO}}}{2} \approx 0.044
$$

This exceeds the ledger value $\delta\gamma = 0.0047$ by a **factor of ~9**. The FRG-NLO route  
is therefore **not** the origin of $\delta\gamma$.

**Conclusion:** $\delta\gamma = 0.0047$ retains evidence category **[B]** as a finite-size  
scaling (FSS) artefact from thermodynamic extrapolation. It is not a perturbative correction.

## Open Tasks

- [ ] L4: Derive $(2N_c+1)^2/N_c$ from functional determinant of UIDT Lagrangian (formal proof)
- [ ] Verify whether holographic/AdS-QCD arguments can elevate to [A] (TKT-2026-03-09-005)
- [ ] Cross-check with KS-MC-FSS data on $\gamma_{\infty}$ extrapolation (TKT-2026-03-09-013)
