# Glossary of Terms — UIDT v3.9

## Mathematical Definitions

### Mass Gap (Δ)
The lowest non-zero eigenvalue of the Hamiltonian operator H on the physical Hilbert space:
$$\Delta := \inf\left(\text{Spec}(H) \setminus \{0\}\right)$$
**UIDT Value:** Δ* = 1.710 ± 0.015 GeV

### Lipschitz Constant (L)
A bound on the rate of change of a mapping T, such that for all x, y in the domain:
$$|T(x) - T(y)| \leq L |x - y|$$
**UIDT Value:** L = 3.749 × 10⁻⁵

### Banach Fixed-Point Theorem
If T: X → X is a contraction mapping (L < 1) on a complete metric space X, then T has a unique fixed point x* = T(x*).

### BRST Charge (Q)
A nilpotent operator (Q² = 0) generating gauge transformations. Physical states satisfy Q|phys⟩ = 0.

### Slavnov-Taylor Identities
Ward identities for non-Abelian gauge theories encoding gauge invariance at the quantum level.

---

## Physical Quantities

### Gluon Condensate (𝒞)
The vacuum expectation value of the gluon field strength squared:
$$\mathcal{C} = \left\langle \frac{\alpha_s}{\pi} G^a_{\mu\nu} G^{a\mu\nu} \right\rangle \approx 0.277 \text{ GeV}^4$$

### Vacuum Expectation Value (VEV)
The expectation value of the scalar field in the vacuum state:
$$v = \langle 0 | S | 0 \rangle = 47.7 \text{ MeV}$$

### Universal Invariant (γ)
The dimensionless scaling parameter appearing in UIDT:
$$\gamma = 16.339$$

### Non-minimal Coupling (κ)
The coupling strength between the scalar field S and the gluon field strength:
$$\mathcal{L}_{\text{int}} = \frac{\kappa}{\Lambda} S \, \text{Tr}(F_{\mu\nu} F^{\mu\nu})$$
**UIDT Value:** κ = 0.500

### Scalar Self-Coupling (λ_S)
The quartic self-interaction of the scalar field:
$$V(S) \supset \frac{\lambda_S}{4!} S^4$$
**UIDT Value:** λ_S = 0.417

---

## Gauge Theory Concepts

### Yang-Mills Field Strength
$$F^a_{\mu\nu} = \partial_\mu A^a_\nu - \partial_\nu A^a_\mu + g f^{abc} A^b_\mu A^c_\nu$$

### Glueball
A bound state of gluons (no valence quarks). The lightest glueball has quantum numbers 0⁺⁺ and mass ≈ 1.7 GeV.

### Confinement
The property that color-charged particles (quarks, gluons) cannot exist as free states.

### Asymptotic Freedom
The property that the strong coupling αₛ decreases at high energies.

---

## Renormalization Group

### Beta Function
The function describing how a coupling constant changes with energy scale:
$$\beta_g = \mu \frac{\partial g}{\partial \mu}$$

### UV Fixed Point
A point in coupling space where all beta functions vanish:
$$\beta_\kappa(\kappa^*, \lambda_S^*) = 0, \quad \beta_{\lambda_S}(\kappa^*, \lambda_S^*) = 0$$

### RG Invariance
Physical observables are independent of the renormalization scale μ.

---

## Axioms

### Osterwalder-Schrader Axioms
Conditions on Euclidean correlation functions ensuring reconstruction of a relativistic QFT:
1. Analyticity
2. Euclidean Covariance
3. Reflection Positivity
4. Cluster Property

### Wightman Axioms
Axiomatic framework for relativistic QFT in Minkowski spacetime.

---

## Acronyms

| Acronym | Meaning |
|---------|---------|
| BRST | Becchi-Rouet-Stora-Tyutin (gauge symmetry) |
| CCR | Canonical Commutation Relations |
| FRG | Functional Renormalization Group |
| GNS | Gelfand-Naimark-Segal (construction) |
| HMC | Hybrid Monte Carlo |
| MCMC | Markov Chain Monte Carlo |
| OS | Osterwalder-Schrader |
| QCD | Quantum Chromodynamics |
| QFT | Quantum Field Theory |
| RG | Renormalization Group |
| SDE | Schwinger-Dyson Equations |
| UIDT | Unified Information-Density Theory |
| UV | Ultraviolet |
| VEV | Vacuum Expectation Value |

---

## Evidence Categories

| Category | Description | Example |
|----------|-------------|---------|
| A+ | Mathematical proof | Banach theorem, L < 1 |
| A | Verified derivation | Gap equation |
| B | Lattice validated | z-score < 2σ |
| C | Calibrated | DESI-fitted parameters |
| D | Predicted | Awaiting experiment |

---

**DOI:** 10.5281/zenodo.17835200  
**Author:** Philipp Rietz (ORCID: 0009-0007-4307-1609)
