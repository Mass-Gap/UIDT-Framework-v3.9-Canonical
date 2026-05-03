# Research Note: Israel–Darmois Matching Analysis for UIDT Black Hole Interior

**Date:** 2026-05-03  
**Author:** P. Rietz  
**Session:** UIDT BH Phase Transition — Parameter Anchoring Audit  
**Status:** Research note — Evidence [D], pending numerical GR verification  
**Related:** PR #412 (mS dependency fix), Issue #413 (C-007 correction), Claim C-070 (this note)  
**DOI:** 10.5281/zenodo.17835200

---

## 1. Motivation

The UIDT black hole interior scenario previously postulated a FRW metric inside
the critical radius $r_c$ via a redefined proper time $d\tau \propto |S|^2 dt$.
This Research Note replaces that postulate with a systematic derivation from
the UIDT Lagrangian via Israel–Darmois junction conditions and perturbative
analysis of the modified Einstein Field Equations (EFE).

**Core question:** Does the UIDT scalar condensate $S(r)$ generate a FRW-like
geometry inside $r_c$ when the EFE are solved self-consistently?

**Result:** No. FRW is doubly excluded. The consistent geometry is Gravastar-type
with a radially varying effective cosmological constant $\Lambda_{\rm eff}(r) \propto r^{-8}$.

---

## 2. Setup

### 2.1 Geometry

Hypersurface: $\Sigma = \{r = r_c\}$ (spherical, timelike).

| Region | Label | Metric | S-field |
|--------|-------|--------|---------|
| $r > r_c$ | $\mathcal{M}^+$ | Schwarzschild | $S = v$ (VEV) |
| $r < r_c$ | $\mathcal{M}^-$ | Unknown, to be derived | $S = S_0(r)$ (condensed) |

Israel–Darmois conditions (no surface layer, $S_{ab} = 0$):
$$[q_{ab}] = 0 \qquad [K_{ab}] = 0$$

### 2.2 Condensed Field Profile

From $\partial V_{\rm eff}/\partial S = 0$ at the off-symmetric minimum:
$$S_0^2(r) = v^2 + \frac{\xi_S\, \mathcal{R}(r)}{\lambda_S}$$

with $\mathcal{R}(r) = 48G^2M^2/r^6$ (Kretschner scalar, Schwarzschild background),
$\xi_S = 1/6$ [Stratum II], $\lambda_S = 5/12$ [A], $v = 47.7$ MeV [A].

In units $\rho = r/r_c$:
$$S_0^2(\rho) = v^2 + \frac{m_S^2}{2\lambda_S \rho^6}$$

The field diverges as $\rho \to 0$ — the condensate strengthens toward the center.

### 2.3 Stress-Energy Tensor

For static $S = S_0(r)$:
$$T^{S}_{tt} = e^{2\alpha}\rho_S(r), \quad
T^{S}_{rr} = e^{2\beta}p_r(r), \quad
T^{S}_{\theta\theta} = R^2 p_\perp(r)$$

where:
$$\rho_S = \tfrac{1}{2}e^{-2\beta}(S_0')^2 + V_{\rm eff}(S_0)$$
$$p_r = \tfrac{1}{2}e^{-2\beta}(S_0')^2 - V_{\rm eff}(S_0)$$
$$p_\perp = -V_{\rm eff}(S_0)$$

At the condensed minimum:
$$V_{\rm eff}(S_0) = -\frac{\xi_S^2 \mathcal{R}^2}{4\lambda_S} - \frac{\xi_S v^2 \mathcal{R}}{2} < 0$$

---

## 3. Matching Conditions

### 3.1 First Fundamental Form $[q_{ab}] = 0$

Exterior (Schwarzschild): $f_+(r_c) = 1 - r_S/r_c$.

Conditions:
- **(MB-I-1):** $A^2(r_c)(d\tau/dt)^{-2} = f_+(r_c)$
- **(MB-I-2):** $R(r_c, t) = r_c = {\rm const}$, hence $\dot{R}(r_c) = 0$

### 3.2 Second Fundamental Form $[K_{ab}] = 0$

Exterior extrinsic curvature components:
$$K^+_{\theta\theta} = r_c\sqrt{f_+(r_c)}, \qquad
K^+_{\tau\tau} = -\frac{r_S}{2r_c^2\sqrt{f_+(r_c)}}$$

Interior (general metric $ds^2_- = -e^{2\alpha}dt^2 + e^{2\beta}dr^2 + R^2 d\Omega^2$):
$$K^-_{\theta\theta} = \frac{R'(r_c)}{e^{\beta(r_c)}}$$

Matching $[K_{\theta\theta}] = 0$:
$$\boxed{\frac{R'(r_c)}{e^{\beta(r_c)}} = r_c\sqrt{f_+(r_c)}}\tag{MB-II-1}$$

Matching $[K_{\tau\tau}] = 0$:
$$\boxed{\alpha'(r_c)e^{-\beta(r_c)} = \frac{r_S}{2r_c^2 f_+(r_c)}}\tag{MB-II-2}$$

This system of four equations (MB-I-1, MB-I-2, MB-II-1, MB-II-2) is
well-posed and constrains the interior metric at $r_c$.

---

## 4. FRW Exclusion

### 4.1 Static Boundary Case

FRW ansatz: $ds^2_- = -d\tau^2 + a^2(\tau)[d\chi^2 + f_k(\chi)^2 d\Omega^2]$,
areal radius $R(\chi, \tau) = a(\tau)\chi$.

Condition MB-I-2 requires $R(\chi_c, \tau) = r_c = {\rm const}$, hence:
$$\dot{a}(\tau) \cdot \chi_c = 0 \implies \dot{a} = 0 \text{ (static universe)}$$

**Static FRW $\neq$ expanding FRW. Excluded.**

### 4.2 Dynamic Boundary Case

If $r_c = r_c(t)$ (moving shell), then $K^-_{\theta\theta}$ acquires a velocity term:
$$K^-_{\theta\theta} = \frac{r_c}{\sqrt{1 - \dot{r}_c^2/f_+(r_c)}}$$

Setting $[K_{\theta\theta}] = 0$:
$$\frac{r_c}{\sqrt{1 - \dot{r}_c^2/f_+}} = r_c\sqrt{f_+(r_c)}
\implies \dot{r}_c^2 = f_+ - 1 = -\frac{r_S}{r_c} < 0$$

**$\dot{r}_c^2 < 0$ has no real solution. Dynamical FRW also excluded.**

---

## 5. Consistent Interior: Gravastar-Type Geometry

### 5.1 Dominant Regime

Numerical comparison of potential vs. kinetic terms at Ledger values
($\xi_S = 1/6$, $\lambda_S = 5/12$, $m_S = 1.710$ GeV, $v = 47.7$ MeV,
mpmath at mp.dps = 80):

| $\rho = r/r_c$ | $|V_{\rm eff}|/({m_S^4}/{4\lambda_S})$ | $\frac{1}{2}(S_0')^2 r_c^2$ (same units) | Pot/Kin |
|---|---|---|---|
| 0.1 | $2.5 \times 10^{11}$ | $3.1 \times 10^8$ | 812 |
| 0.3 | $4.7 \times 10^5$ | $4.7 \times 10^4$ | 10 |
| 0.5 | $1024$ | $788$ | 1.3 |
| 0.7 | $18$ | $53$ | 0.34 |
| 0.9 | $0.89$ | $7.1$ | 0.12 |

For $\rho < 0.5$: potential dominates.

### 5.2 Effective Cosmological Constant

In the potential-dominated regime:
$$T^S_{\mu\nu} \approx V_{\rm eff}(r)\, g_{\mu\nu}
= -|V_{\rm eff}(r)|\, g_{\mu\nu}$$

This acts as a position-dependent effective cosmological constant:
$$\Lambda_{\rm eff}(r) = 8\pi G\, |V_{\rm eff}(r)|
\approx \frac{2\pi G\,\xi_S^2\,(48)^2\, G^4 M^4}{\lambda_S\, r^8}
\propto r^{-8}$$

The interior EFE reduce to:
$$G_{\mu\nu} = -\Lambda_{\rm eff}(r)\, g_{\mu\nu}$$

This is a **generalised Gravastar** (cf. Mazur & Mottola 2001,
Proc. Natl. Acad. Sci. 98, 9236–9241) with radially varying $\Lambda$.

### 5.3 Energy Condition Analysis

| Condition | Expression | Status |
|-----------|------------|--------|
| NEC ($\rho + p_r \geq 0$) | $e^{-2\beta}(S_0')^2 \geq 0$ | **Satisfied** |
| NEC ($\rho + p_\perp \geq 0$) | $\frac{1}{2}e^{-2\beta}(S_0')^2 \geq 0$ | **Satisfied** |
| SEC ($\rho + p_r + 2p_\perp \geq 0$) | $e^{-2\beta}(S_0')^2 - 2V_{\rm eff} \geq 0$ | **Violated** (when $V_{\rm eff} < 0$, potential-dom.) |
| WEC ($\rho \geq 0$) | $\frac{1}{2}e^{-2\beta}(S_0')^2 + V_{\rm eff}$ | **Violated** near center |

SEC violation is the physical mechanism enabling de-Sitter-type repulsion
inside $r_c$ — consistent with the Gravastar scenario.

### 5.4 Open Questions from This Analysis

| ID | Question | Evidence |
|----|----------|----------|
| OQ-BH-001 | Does $\Lambda_{\rm eff}(r) \propto r^{-8}$ regularise the central singularity? | E |
| OQ-BH-002 | Full nonlinear fixpoint system: $G^{(-)}_{{\mu\nu}} = 8\pi G\, T^S_{{\mu\nu}}(S_0(\mathcal{R}[g]))$ | E |
| OQ-BH-003 | Does the $r_c \gg r_S$ structural problem imply condensation is extragalactic, not BH-internal? | D |
| OQ-BH-004 | Israel–Darmois matching with surface layer $S_{ab} \neq 0$ (domain wall scenario)? | E |

---

## 6. Epistemic Classification

**Stratum I** (empirical): None invoked.

**Stratum II** (consensus): Israel–Darmois junction conditions (Misner–Thorne–Wheeler §21.13;
Israel 1966, Nuovo Cim. B 44, 1); FRW metric criteria; SEC/NEC standard definitions;
Gravastar existence (Mazur & Mottola 2001).

**Stratum III** (UIDT): S-field condensation as interior source [D];
$r_c$ via $\xi_S$-coupling [D]; Gravastar identification [D, this note];
$\Lambda_{\rm eff}(r) \propto r^{-8}$ [D, this note].

---

## 7. Pre-Flight Check

- [x] No `float()` usage
- [x] `mp.dps = 80` local in all calculations
- [x] RG constraint $5\kappa^2 = 3\lambda_S$ maintained (residual = 0)
- [x] No modification of Ledger constants
- [x] No deletion in `/core` or `/modules`
- [x] No claims upgraded without evidence

---

*P. Rietz — ORCID 0009-0007-4307-1609 — DOI: 10.5281/zenodo.17835200*
