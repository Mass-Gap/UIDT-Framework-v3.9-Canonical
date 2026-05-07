# c_S Derivation Report — UIDT v3.9

**Date:** 2026-05-02  
**Author:** UIDT Framework (P. Rietz, maintainer)  
**DOI:** 10.5281/zenodo.17835200  
**Addresses:** Claims C-016, C-040  
**Branch:** `feature/sd-vacuum-cs-derivation`

---

## Claims Table

| Claim ID | Statement | Evidence Category | Source |
|----------|-----------|-------------------|--------|
| C-016 | c_S modifies the gluon β-function at k~Δ* | B | This derivation |
| C-040 | Vacuum stability requires non-perturbative treatment for κ=0.500 | B→E | This derivation |
| C-NEW-01 | Ghost-corrected b₀ = 33/(48π²) for SU(3) pure YM | A | Standard QFT [Caswell 1974] |
| C-NEW-02 | Physical κ carries dimension GeV⁻² (dimensional tension) | B | FORMALISM.md audit |
| C-NEW-03 | c_S (dimensionless) = (κ/2)·[1 + m_S²/Δ²]⁻¹ ∈ (0, 0.25] | B | This derivation |
| C-NEW-04 | Vacuum instability onset at ⟨F²⟩_crit = 2λ_S v²/κ_ph | B | SD scan |

---

## Reproduction Note

One-command verification:

```bash
pip install mpmath pytest
python verification/scripts/sd_vacuum_check.py
pytest verification/tests/test_sd_vacuum.py -v
```

All tests run real `mpmath` arithmetic at `mp.dps = 80`.  
No mocks. No float(). No round(). Residual threshold: `|LHS - RHS| < 1e-14`.

---

## Mathematical Derivation

### Stratum I — Input from Standard Physics

The one-loop gauge-coupling β-function coefficient for SU(N_c) with N_f quarks,
including Faddeev-Popov ghost loops, is (Evidence **A**):

$$b_0^\text{full} = \frac{11 N_c - 2 N_f}{48\pi^2}$$

For pure SU(3) Yang-Mills (N_f = 0, vacuum sector):

$$b_0 = \frac{33}{48\pi^2} \approx 0.06957$$

This expression **already includes** the Faddeev-Popov ghost contribution.
The ghost loop contributes −N_c/(48π²), which is absorbed into the coefficient
11 → (12 − 1) = 11 for the gluon sector.

---

### Stratum II — Standard QFT Result

The UIDT interaction Lagrangian (FORMALISM.md) is:

$$\mathcal{L}_\text{int} = -\frac{\kappa}{4}\, S^2\, F^a_{\mu\nu} F^{a\mu\nu}$$

This is a **four-point vertex** (2 scalar legs, 2 gluon legs).  
The 1-loop tadpole contribution to the transverse gluon self-energy is:

$$\Pi^{ab}_{\mu\nu}(k)\big|_\text{UIDT} =
  -\kappa\, \delta^{ab}\,(k^2 g_{\mu\nu} - k_\mu k_\nu)\cdot I_S(k)$$

with the Litim-regulated scalar tadpole:

$$I_S(k) = \frac{k^4}{16\pi^2\,(k^2 + m_S^2)}, \qquad m_S^2 = 2\lambda_S v^2$$

---

### Stratum III — UIDT Model Mapping

#### Dimensional consistency

**⚠️ [TENSION ALERT]**

In FORMALISM.md, κ is listed as dimensionless [A-].  
Dimensional analysis of $\mathcal{L}_\text{int}$:

$$[\kappa]\cdot[S^2]\cdot[F^2] = [\kappa]\cdot\text{GeV}^2\cdot\text{GeV}^4
  \stackrel{!}{=} \text{GeV}^4$$

$$\Rightarrow \quad [\kappa] = \text{GeV}^{-2}$$

The physical coupling is therefore:

$$\kappa_\text{ph} = \frac{\kappa_\text{ledger}}{\Delta^{*2}}
  = \frac{0.500}{(1.710\,\text{GeV})^2}
  = 0.17085\,\text{GeV}^{-2}$$

Externally: κ_ledger = 0.500 [A-] is a dimensionless proxy.  
Physical renormalisability requires κ_ph with units GeV⁻².

#### Dimensionless c_S

The gluon wave-function renormalisation shift from the scalar tadpole:

$$\delta Z_A(k) \propto \kappa \cdot I_S(k) / k^2
  = \frac{\kappa}{16\pi^2}\cdot\frac{k^2}{k^2 + m_S^2}$$

The physically correct, dimensionless damping parameter:

$$\boxed{c_S = \frac{\kappa}{2}\cdot\frac{1}{1 + m_S^2/\Delta^{*2}}}$$

Numerical values with UIDT ledger constants:

| Quantity | Value | Units | Evidence |
|----------|-------|-------|----------|
| κ | 0.500 | 1 (ledger proxy) | A- |
| λ_S | 5/12 | 1 | A |
| v | 47.7 | MeV | A |
| Δ* | 1.710 | GeV | A |
| m_S² = 2λ_S v² | 1.897×10⁻³ | GeV² | A |
| m_S | 43.56 | MeV | A |
| c_S (full) | 0.24974 | 1 | B |
| c_S (UV limit) | 0.250 | 1 | B |
| b₀ | 0.069572 | 1 | A |
| b₀ − c_S | −0.18017 | 1 | B |

#### Physical interpretation

- `b₀ − c_S < 0` indicates that the UIDT scalar feedback **dominates** the
  perturbative gluon loop at k ∼ Δ*.  
- This is **not a contradiction**: at IR scales k ∼ Δ* ∼ 1.7 GeV, QCD is
  non-perturbative. Asymptotic freedom is restored at k ≫ Δ*.  
- Full resolution requires the BMW-FRG flow for Z_A(k) (Evidence E, Module V).

---

### Schwinger-Dyson Vacuum Stability

From the SD equation (FORMALISM.md):

$$\Box S + \lambda_S\, S(S^2 - v^2) + \frac{\kappa}{2}\, S\, F^2 = 0$$

Non-trivial vacuum ⟨S⟩ ≠ 0 requires:

$$\langle S\rangle^2 = v^2 - \frac{\kappa_\text{ph}}{2\lambda_S}\,\langle F^2\rangle$$

Stability criterion:  $\langle S\rangle^2 \geq 0$

Critical condensate:

$$\langle F^2\rangle_\text{crit} = \frac{2\lambda_S\, v^2}{\kappa_\text{ph}}
  = \frac{2 \cdot (5/12) \cdot (0.0477)^2}{0.17085}\,\text{GeV}^4
  \approx 0.02215\,\text{GeV}^4$$

The SVZ/lattice range for the gluon condensate spans
⟨F²⟩ ∈ [0.02, 0.5] GeV⁴ (Stratum I, external input).
**The critical value sits inside this range**, confirming that a full
non-perturbative treatment is mandatory.

---

## BMW-FRG Upgrade Path (Evidence E)

The full non-perturbative c_S is defined by:

$$c_S^\text{phys} = 1 - \frac{Z_A(k\to 0)}{Z_A(k\to\Lambda_\text{UV})}$$

This requires solving the Wetterich equation for the UIDT truncation:

$$\partial_t \Gamma_k^\text{UIDT} = \frac{1}{2}\,
  \text{Tr}\!\left[\left(\Gamma_k^{(2)} + R_k\right)^{-1} \partial_t R_k\right]$$

with coupled flows for {Z_A(k), Z_S(k), κ(k), λ_S(k), U_k(S)}.
See `verification/scripts/sd_vacuum_check.py` → Module V for the required steps.

**Open tasks before BMW-FRG can be executed:**

1. External lattice input: ⟨F²⟩ with uncertainty (Stratum I)
2. Ghost propagator in the Gribov–Zwanziger or Kugo–Ojima scheme
   (see `docs/ghost_sector_lagrangian.md`, `docs/kugo_ojima_criterion.md`)
3. Full propagator matrix in (A_μ, S, c, c̄) space at one-loop order
4. Numerical ODE integration with `mpmath.odefun` at dps = 80

---

## Known Limitations (UIDT Constitution §LIMITATION POLICY)

| ID | Limitation | Impact |
|----|------------|--------|
| L-CS-01 | κ listed as dimensionless in FORMALISM.md but requires GeV⁻² for consistency | Medium — dimensional tension in κ S² F² vertex |
| L-CS-02 | c_S derived at 1-loop only | Medium — non-perturbative BMW-FRG needed |
| L-CS-03 | ⟨F²⟩ not fixed from first principles in UIDT | High — external lattice input mandatory |
| L-CS-04 | Vacuum may be unstable for ⟨F²⟩ > ⟨F²⟩_crit ≈ 0.022 GeV⁴ | High — motivates BMW-FRG |
| L-CS-05 | BMW-FRG scaffold not yet implemented | High — Evidence E only |

---

*Transparency has priority over narrative. — UIDT Constitution*
