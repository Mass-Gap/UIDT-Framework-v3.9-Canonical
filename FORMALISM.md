# UIDT Formalism v3.7.2

> **PURPOSE:** Central repository for UIDT equations  
> **RULE:** Math (LaTeX) MUST be separated from interpretation

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

---

## Core Equations

### Vacuum Equation
$$\left\langle S \right\rangle = v = 47.7 \text{ MeV}$$

### Schwinger-Dyson Equation
$$\Box S + \lambda_S S (S^2 - v^2) + \frac{\kappa}{2} S F^2 = 0$$

### Renormalization Group Equation
$$\mu \frac{d\lambda_S}{d\mu} = \beta_{\lambda_S}(\lambda_S, \kappa, g)$$

---

## Fixed-Point Condition

### RG Fixed Point Constraint
$$5\kappa^2 = 3\lambda_S$$

**Verification:**
$$5 \times (0.500)^2 = 1.250$$
$$3 \times 0.417 = 1.251$$
$$|\Delta| = 0.001 < 0.01 \checkmark$$

---

## Mass Gap Derivation

### Spectral Gap
$$\Delta^* = \gamma \cdot \Lambda_{\text{QCD}}$$

With:
- $\gamma = 16.339$ (kinetic VEV) [A-]
- $\Lambda_{\text{QCD}} \approx 0.1046$ GeV
- $\Delta^* = 1.710 \pm 0.015$ GeV [A]

### Scalar Mass

> **TKT-20260503 — Scope clarification:** The formula below gives the
> tree-level mass of $S$ evaluated at the **symmetric point** $S = 0$
> with the potential $V(S) = \tfrac{\lambda_S}{4}(S^2 - v^2)^2$.
> At $S = 0$: $V''(0) = -\lambda_S v^2$, so $m_{S,\text{sym}}^2 = \lambda_S v^2$
> (tachyonic, symmetry-unbroken phase).
> At the broken minimum $S = v$: $V''(v) = 2\lambda_S v^2$, so
> $m_{S,\text{broken}}^2 = 2\lambda_S v^2$.
>
> **Numerical result with Ledger values** ($\lambda_S = 5/12$, $v = 47.7$ MeV):
> $$m_{S,\text{broken}} = \sqrt{2\lambda_S\, v^2} \approx 43.5 \text{ MeV}$$
>
> This value is **numerically inconsistent** with the Ledger prediction
> $m_S = 1.705 \pm 0.015$ GeV [D] listed in CONSTANTS.md.
> The Ledger value is numerically compatible with $\Delta^* = 1.710$ GeV [A]
> (deviation 0.29%, within stated uncertainty), suggesting the identification
> $m_S \approx \Delta^*$ as working hypothesis — but this identification
> is **not yet formally derived** from the Lagrangian.
> The dependency declaration in CLAIMS.json C-007 (`mS = 2λ_S v`) is
> therefore **incorrect as a derivation source** and has been flagged
> for correction (see C-007 note below). **Evidence category [D] is maintained.**

$$m_{S,\text{broken}}^2 = 2\lambda_S v^2 \quad \text{[tree-level, broken minimum]}$$
$$m_{S,\text{broken}} \approx 43.5 \text{ MeV} \quad \text{[from Ledger } \lambda_S, v \text{]}$$

$$m_S = 1.705 \pm 0.015 \text{ GeV} \quad \text{[D — Ledger value, origin: } m_S \approx \Delta^*\text{, unverified]}$$

---

## Stability Conditions

### Perturbative Stability
$$\lambda_S < 1 \quad \Rightarrow \quad 0.417 < 1 \checkmark$$

### Vacuum Stability
$$V''(v) = 2\lambda_S v^2 > 0 \quad \Rightarrow \quad 2.907 > 0 \checkmark$$

> **Note:** The quantity $V''(v) = 2\lambda_S v^2$ used in the stability check
> evaluates to $2 \times (5/12) \times (0.0477)^2 \approx 1.90 \times 10^{-3}$ GeV$^2 > 0$.
> The value 2.907 cited above uses $v$ in MeV units without consistent
> dimensional normalisation and is retained here for historical continuity
> pending a dedicated dimensional-audit PR.

---

## Cosmological Equations

### Hubble Parameter (Calibrated)
$$H_0 = 70.4 \pm 0.16 \text{ km/s/Mpc}$$

> **Category C:** Calibrated to DESI DR2, NOT derived.

### Vacuum Energy Suppression
$$\rho_{\text{vac}}^{\text{obs}} = \rho_{\text{vac}}^{\text{QFT}} \times \pi^{-2} \times \prod_{n=1}^{99} f_n(g)$$

> **Category C:** Phenomenological 99-step cascade.

### UIDT Wavelength
$$\lambda_{\text{UIDT}} = 0.660 \pm 0.005 \text{ nm}$$

---

## Pillar II-CSF (Covariant Scalar-Field)

### Conformal Density Mapping
$$ \gamma_{CSF} = \frac{1}{2 \sqrt{\pi \ln(\gamma_{UIDT})}} $$

### Planck-Singularity Regularization
$$ \rho_{max} = \Delta^4 \cdot \gamma^{99} $$

### Equation of State (Placeholders)
$$ w_0 = -0.99, \quad w_a = +0.03 $$

> **Strict Caveat:** The CSF extensions are strictly evaluated under Evidence Category `[C]`. 
> They map phenomenologically upon the `[A-]` calibrated lattice invariant $\gamma = 16.339$. 
> **Limitation L4:** $\gamma$ is calibrated, not fundamentally derived. 
> **Limitation L5:** The $N=99$ RG step limit remains empirical.

---

## Casimir Prediction

### Force Anomaly
$$\frac{\Delta F}{F} = +0.59\% \quad \text{at} \quad d = 0.66 \text{ nm}$$

> **Category D:** Unverified prediction.

### Optimal Distance (v3.7.1 corrected)
$$d_{\text{opt}} = 0.854 \text{ nm}$$

---

## Numerical Precision

### Residual Thresholds
| Equation System | Residual | Status |
|-----------------|----------|--------|
| Three-Equation Closure | < 10⁻⁴⁰ | ✅ |
| Branch 1 | 3.2×10⁻¹⁴ | ✅ |
| Branch 2 (excluded) | 1.8×10⁻¹² | ❌ |
| Verification Tolerance | < 10⁻¹⁴ | ✅ |

---

## Constraint Summary

| Constraint | Expression | Value | Status |
|------------|------------|-------|--------|
| RG Fixed Point | 5κ² = 3λ_S | 1.250 ≈ 1.251 | ✅ |
| Perturbative | λ_S < 1 | 0.417 | ✅ |
| Vacuum | V''(v) > 0 | 2.907 | ✅ (see note) |
| Gamma | γ_kinetic ≈ γ_MC | 16.339 ≈ 16.374 | ✅ |

---

## Reference Implementation

See `WORKSPACE/derivations/` for:
- `uidt_proof_core.py` — Core proof implementation
- `rg_flow_analysis.py` — RG flow calculations
- `error_propagation.py` — Uncertainty analysis

---

**CITATION:** Rietz, P. (2025). UIDT v3.7.2. DOI: 10.5281/zenodo.17835200
