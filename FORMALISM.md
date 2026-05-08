# UIDT Formalism v3.9.0

> **PURPOSE:** Central repository for UIDT equations  
> **RULE:** Math (LaTeX) MUST be separated from interpretation  
> **VERSION:** 3.9.0  |  Updated: 2026-05-02  |  Supersedes v3.7.2

---

## Lagrangian

### Full UIDT Lagrangian
$$\mathcal{L}_{\text{UIDT}} = \mathcal{L}_{\text{YM}} + \mathcal{L}_S + \mathcal{L}_{\text{int}}$$

### Yang-Mills Sector
$$\mathcal{L}_{\text{YM}} = -\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}$$

### Scalar Sector
$$\mathcal{L}_S = \frac{1}{2} \partial_\mu S \partial^\mu S - V(S)$$

### Scalar Potential
$$V(S) = \frac{\lambda_S}{4} (S^2 - v^2)^2$$

### Interaction (Non-Minimal Coupling)
$$\mathcal{L}_{\text{int}} = -\frac{\kappa}{4} S^2 F^a_{\mu\nu} F^{a\mu\nu}$$

> **[TENSION ALERT — L-CS-01] Dimensional status of $\kappa$** \[Evidence B\]  
> In natural units ($\hbar = c = 1$), the Lagrangian density carries dimension $[\mathcal{L}] = \text{GeV}^4$.  
> Since $[S] = \text{GeV}^1$ and $[F^2] = \text{GeV}^4$, the interaction term requires:
> $$[\kappa]\cdot[S^2]\cdot[F^2] = [\kappa]\cdot\text{GeV}^2\cdot\text{GeV}^4 \stackrel{!}{=} \text{GeV}^4
>   \quad\Longrightarrow\quad [\kappa] = \text{GeV}^{-2}$$
> **Consequence:** The ledger value $\kappa = 0.500$ is a **dimensionless proxy** for the physical coupling
> $$\kappa_{\mathrm{ph}} = \frac{\kappa}{\Delta^{*2}} = \frac{0.500}{(1.710\,\text{GeV})^2}
>   = 0.17085\,\text{GeV}^{-2} \quad [\text{Evidence B}]$$
> **Scope of kappa = 0.500:** Valid as a dimensionless ratio $\kappa_{\mathrm{ledger}} = \kappa_{\mathrm{ph}}\cdot\Delta^{*2}$
> for use in the RG fixed-point constraint $5\kappa^2 = 3\lambda_S$ and in dimensionless
> ratios only.  All dimensional calculations (SD vacuum, FRG flow) must use $\kappa_{\mathrm{ph}}$.  
> **This tension does not invalidate the ledger** — it clarifies the domain of validity.
> See `docs/cs_derivation_report.md` §Dimensional consistency and Limitation L-CS-01.

---

## Core Equations

### Vacuum Equation
$$\left\langle S \right\rangle = v = 47.7\,\text{MeV} \quad [\text{Evidence A}]$$

### Schwinger-Dyson Equation
$$\Box S + \lambda_S S (S^2 - v^2) + \frac{\kappa_{\mathrm{ph}}}{2} S F^2 = 0$$

> **Note:** $\kappa_{\mathrm{ph}}$ (GeV$^{-2}$) must be used here for dimensional consistency.
> In the original form with dimensionless $\kappa$, the equation is schematic;
> dimensional correctness requires $\kappa \to \kappa/\Delta^{*2}$.

### Renormalization Group Equation
$$\mu \frac{d\lambda_S}{d\mu} = \beta_{\lambda_S}(\lambda_S, \kappa, g)$$

> **Note:** $\kappa$ here is the dimensionless ledger proxy, consistent with the
> RG fixed-point constraint below.

---

## Fixed-Point Condition

### RG Fixed Point Constraint
$$5\kappa^2 = 3\lambda_S \quad [\text{Evidence A}]$$

**Exact values:**
$$\kappa = 0.500, \qquad \lambda_S = \frac{5}{12} \approx 0.41\overline{6}$$

**Verification (80-digit mpmath):**
$$5 \times (0.500)^2 = 1.250000\ldots$$
$$3 \times \frac{5}{12} = 1.250000\ldots$$
$$|\mathrm{LHS} - \mathrm{RHS}| < 10^{-14} \checkmark$$

> **Correction note v3.9.0:** Previous versions stated $\lambda_S \approx 0.417$
> (3 significant figures).  The exact value is $\lambda_S = 5/12$.
> The residual was $0.001$ only due to rounding of $\lambda_S$; the exact
> constraint is satisfied identically.

---

## Mass Gap Derivation

### Spectral Gap
$$\Delta^* = \gamma \cdot \Lambda_{\text{QCD}}$$

With:
- $\gamma = 16.339$ (kinetic VEV parameter) $[\text{A-}]$
- $\Lambda_{\text{QCD}} \approx 0.1046\,\text{GeV}$
- $\Delta^* = 1.710 \pm 0.015\,\text{GeV}$ $[\text{A}]$

> **Interpretation:** $\Delta^*$ is the Yang–Mills spectral gap.
> It is **NOT** a particle mass.

### Scalar Mass
$$m_S^2 = 2\lambda_S\, v^2 = 2 \cdot \frac{5}{12} \cdot (47.7\,\text{MeV})^2
  = 1.897 \times 10^{-3}\,\text{GeV}^2$$
$$m_S = \sqrt{2\lambda_S}\, v \approx 43.56\,\text{MeV} \quad [\text{Evidence A}]$$

> **Correction note v3.9.0:** Previous versions stated $m_S = 1.705 \pm 0.015\,\text{GeV}$.
> This was an error: $m_S = 1.705\,\text{GeV}$ is the **spectral gap** $\Delta^*$, not the scalar mass.
> The S-field mass is determined by $m_S^2 = 2\lambda_S v^2$ with $v = 47.7\,\text{MeV}$,
> giving $m_S \approx 43.56\,\text{MeV}$.  The near-coincidence $\Delta^* \approx m_S^{\text{(wrong)}}$
> was a notational conflation.  Ledger constant $\Delta^* = 1.710\,\text{GeV}$ is unchanged.

---

## Stability Conditions

### Perturbative Stability
$$\lambda_S < 1 \quad \Rightarrow \quad \frac{5}{12} < 1 \checkmark$$

### Vacuum Stability (perturbative)
$$V''(v) = 2\lambda_S v^2 = m_S^2 > 0 \quad \Rightarrow \quad 1.897\times 10^{-3}\,\text{GeV}^2 > 0 \checkmark$$

### Vacuum Stability (non-perturbative, with gluon condensate)

> **[Evidence B]** When the gluon condensate $\langle F^2 \rangle \neq 0$,
> the SD equation shifts the effective vacuum:
>
> $$\langle S\rangle^2 = v^2 - \frac{\kappa_{\mathrm{ph}}}{2\lambda_S}\,\langle F^2\rangle$$
>
> Vacuum stability requires $\langle S\rangle^2 \geq 0$, i.e.,
>
> $$\langle F^2\rangle \leq \langle F^2\rangle_{\mathrm{crit}}
>   = \frac{2\lambda_S\, v^2}{\kappa_{\mathrm{ph}}} \approx 0.0222\,\text{GeV}^4$$
>
> The SVZ/lattice range $\langle F^2\rangle \in [0.02,\,0.5]\,\text{GeV}^4$ (Stratum I, external)
> overlaps with $\langle F^2\rangle_{\mathrm{crit}}$, indicating that a full
> non-perturbative BMW-FRG treatment is required.  
> See `verification/scripts/sd_vacuum_check.py` Module III for the numerical scan.

---

## Scalar Damping Parameter

> **[Evidence B]** Derived in `docs/cs_derivation_report.md` (PR #395, 2026-05-02).

### Dimensionless c_S

$$c_S = \frac{\kappa}{2}\cdot\frac{1}{1 + m_S^2/\Delta^{*2}}$$

| Quantity | Exact form | Numerical value | Evidence |
|----------|-----------|-----------------|----------|
| $\kappa$ | $0.500$ | $0.500$ | A- |
| $\lambda_S$ | $5/12$ | $0.41\overline{6}$ | A |
| $v$ | $47.7\,\text{MeV}$ | $0.0477\,\text{GeV}$ | A |
| $\Delta^*$ | $1.710\,\text{GeV}$ | $1.710\,\text{GeV}$ | A |
| $m_S^2$ | $2\lambda_S v^2$ | $1.897\times10^{-3}\,\text{GeV}^2$ | A |
| $m_S$ | $\sqrt{2\lambda_S}\,v$ | $43.56\,\text{MeV}$ | A |
| $\kappa_{\mathrm{ph}}$ | $\kappa/\Delta^{*2}$ | $0.17085\,\text{GeV}^{-2}$ | B |
| $c_S$ | full expression | $0.24974$ | B |
| $c_S^{\mathrm{UV}}$ | $\kappa/2$ | $0.250$ | B |
| $b_0$ | $33/(48\pi^2)$ | $0.069572$ | A |
| $b_0 - c_S$ | | $-0.18017$ | B |

> **Physics note:** $b_0 - c_S < 0$ at $k \sim \Delta^*$.  This is consistent with
> non-perturbative confinement at IR scales.  UV asymptotic freedom ($k \gg \Delta^*$) is unaffected.

---

## Cosmological Equations

### Hubble Parameter (Calibrated)
$$H_0 = 70.4 \pm 0.16\,\text{km/s/Mpc}$$

> **Category C:** Calibrated to DESI DR2, NOT derived.

### Vacuum Energy Suppression
$$\rho_{\text{vac}}^{\text{obs}} = \rho_{\text{vac}}^{\text{QFT}} \times \pi^{-2} \times \prod_{n=1}^{99} f_n(g)$$

> **Category C:** Phenomenological 99-step cascade.

### UIDT Wavelength
$$\lambda_{\text{UIDT}} = 0.660 \pm 0.005\,\text{nm}$$

---

## Pillar II-CSF (Covariant Scalar-Field)

### Conformal Density Mapping
$$\gamma_{\text{CSF}} = \frac{1}{2\sqrt{\pi\ln(\gamma_{\text{UIDT}})}}$$

### Planck-Singularity Regularization
$$\rho_{\text{max}} = \Delta^{*4} \cdot \gamma^{99}$$

### Equation of State (Placeholders)
$$w_0 = -0.99, \qquad w_a = +0.03$$

> **Strict Caveat:** The CSF extensions are strictly evaluated under Evidence Category `[C]`.  
> They map phenomenologically upon the `[A-]` calibrated lattice invariant $\gamma = 16.339$.  
> **Limitation L4:** $\gamma$ is calibrated, not fundamentally derived.  
> **Limitation L5:** The $N=99$ RG step limit remains empirical.

---

## Casimir Prediction

### Force Anomaly
$$\frac{\Delta F}{F} = +0.59\% \quad \text{at} \quad d = 0.66\,\text{nm}$$

> **Category D:** Unverified prediction.

### Optimal Distance (v3.7.1 corrected)
$$d_{\text{opt}} = 0.854\,\text{nm}$$

---

## Numerical Precision

### Residual Thresholds
| Equation System | Residual | Status |
|-----------------|----------|--------|
| Three-Equation Closure | $< 10^{-40}$ | ✅ |
| Branch 1 | $3.2\times10^{-14}$ | ✅ |
| Branch 2 (excluded) | $1.8\times10^{-12}$ | ❌ |
| Verification Tolerance | $< 10^{-14}$ | ✅ |
| RG Fixed Point (exact) | $< 10^{-14}$ | ✅ |

---

## Constraint Summary

| Constraint | Expression | Exact value | Status |
|------------|------------|-------------|--------|
| RG Fixed Point | $5\kappa^2 = 3\lambda_S$ | $1.250 = 1.250$ | ✅ |
| Perturbative | $\lambda_S < 1$ | $5/12$ | ✅ |
| Vacuum (pert.) | $V''(v) > 0$ | $1.897\times10^{-3}\,\text{GeV}^2$ | ✅ |
| Gamma | $\gamma_{\mathrm{kin}} \approx \gamma_{\mathrm{MC}}$ | $16.339 \approx 16.374$ | ✅ |
| $\kappa$ dimensional | $[\kappa_{\mathrm{ph}}] = \text{GeV}^{-2}$ | $\kappa_{\mathrm{ph}} = 0.17085$ | ⚠️ L-CS-01 |
| Vacuum (non-pert.) | $\langle F^2\rangle < \langle F^2\rangle_{\mathrm{crit}}$ | $0.022\,\text{GeV}^4$ | ⚠️ L-CS-04 |

---

## Known Limitations

| ID | Description | Impact |
|----|-------------|--------|
| L-CS-01 | $\kappa$ listed as dimensionless; physical coupling requires $\kappa_{\mathrm{ph}} = \kappa/\Delta^{*2}$ [GeV$^{-2}$] | Medium — affects SD and FRG calculations |
| L-CS-04 | Vacuum may be unstable for $\langle F^2\rangle > 0.022\,\text{GeV}^4$ | High — motivates BMW-FRG |
| L4 | $\gamma = 16.339$ is calibrated, not fundamentally derived | Medium |
| L5 | $N=99$ RG step limit is empirical | Medium |

Full limitations: see `docs/limitations.md` and `docs/cs_derivation_report.md`.

---

## Reference Implementation

See `WORKSPACE/derivations/` for:
- `uidt_proof_core.py` — Core proof implementation
- `rg_flow_analysis.py` — RG flow calculations
- `error_propagation.py` — Uncertainty analysis

See `verification/scripts/sd_vacuum_check.py` for:
- Module I–II: $b_0$ and RG gate
- Module III: SD vacuum stability scan
- Module IV: dimensionless $c_S$ extraction
- Module V: BMW-FRG scaffold (Evidence E)

---

**CITATION:** Rietz, P. (2025). UIDT Framework v3.9. DOI: 10.5281/zenodo.17835200
