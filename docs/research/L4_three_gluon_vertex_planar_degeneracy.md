# Three-Gluon Vertex Planar Degeneracy and Gluon Anomalous Dimension η_A(k²)

**UIDT Framework v3.9** | Evidence Category: B (lattice input), D (SDE structure)
**Research Note Classification:** L4 — Active Research
**Author:** P. Rietz | **Date:** 2026-05-08
**DOI:** 10.5281/zenodo.17835200

---

## Abstract

This research note documents the functional structure of the transversely
projected three-gluon vertex as established by Pinto-Gómez, Aguilar, De Soto,
Ferreira, and Papavassiliou in their lattice study of extended kinematics
(arXiv:2208.01020), and develops the schematic Schwinger–Dyson equation (SDE)
for the gluon anomalous dimension η_A(k²) with explicit three-gluon, ghost,
and four-gluon contributions. The planar degeneracy result — that the leading
transverse form factors depend predominantly on the single Bose-symmetric
variable s² = ½(q² + r² + p²) — provides a crucial simplification for
non-perturbative vertex input in SDE studies.

**Scope limitation:** No explicit numerical fit parameters are given in the
source publication. This note restricts itself to functional relationships and
qualitative behavior that can be faithfully reconstructed from the published
text and figures. Any parametric fit would require access to raw lattice data
or digitized plots, which lies outside the scope of this document.

---

## 1. Scope and Evidence Layers

| Stratum | Content | Evidence | Source |
|---------|---------|----------|--------|
| **I — Lattice Input** | Planar degeneracy of transverse form factors Γ₁, Γ₂, Γ₃ in bisectoral kinematics | B | Pinto-Gómez et al., arXiv:2208.01020 |
| **II — Continuum SDE/FRG** | Schematic SDE for η_A(k²) with dressed 3-gluon vertex input | B–D | Aguilar et al., arXiv:2201.08496; Huber, arXiv:2004.00415 |
| **III — UIDT Mapping** | Constraints on γ-scaling and non-perturbative fixed points from η_A behavior | D–E | UIDT Framework v3.9 (this note) |

---

## 2. Planar Degeneracy and Transverse Form Factors

### 2.1 Bose-Symmetric Transverse Basis

The transversely projected three-gluon vertex in Landau gauge is decomposed in
a fully transverse, Bose-symmetric basis {λ̃ᵢᵅᵘᵛ} with form factors
Γ̂ᵢ(q², r², p²):

$$\Gamma_{\alpha\mu\nu}^{\perp}(q,r,p) = \sum_{i} \widehat{\Gamma}_i(q^2, r^2, p^2) \, \tilde{\lambda}_i^{\alpha\mu\nu}(q,r,p)$$

For bisectoral kinematics q² = r², the vertex reduces to **three** independent
scalar form factors Γ₁, Γ₂, Γ₃(q², q², p²), which are specific linear
combinations of the Γ̂ᵢ.

### 2.2 Planar Degeneracy

Lattice data demonstrate that the form factors depend, to excellent
approximation, only on the Bose-symmetric scalar variable:

$$s^2 = \frac{1}{2}(q^2 + r^2 + p^2)$$

This means that all kinematic configurations sharing the same value of s² — a
plane in the (q², r², p²) parameter space — yield essentially identical form
factor values. This constitutes the **planar degeneracy** property.

**Evidence tag:** [B] — Direct lattice QCD measurement (quenched SU(3),
Landau gauge, multiple lattice volumes and spacings).

### 2.3 Hierarchy of Form Factors

| Form Factor | Magnitude Relative to Γ₁ | s²-Dependence | Status |
|-------------|--------------------------|---------------|--------|
| Γ₁(q², q², p²) | **Dominant** (tree-level tensor) | Pure s²-dependence to high accuracy | Confirmed [B] |
| Γ₂(q², q², p²) | O(0.1 × Γ₁) | Approximately s²-dependent | Confirmed [B] |
| Γ₃(q², q², p²) | Compatible with zero | — | Confirmed [B] |

### 2.4 Planar Degeneracy Approximation

The dominant approximation expresses the full vertex through the **soft-gluon
form factor** Γₛᵍ(s²):

$$\Gamma_{\alpha\mu\nu}(q,r,p) \approx \Gamma_{\text{sg}}(s^2) \, \tilde{\lambda}_1^{\alpha\mu\nu}(q,r,p)$$

A refined version incorporates the symmetric form factor Γ₂ˢʸᵐ:

$$\Gamma_{\alpha\mu\nu}(q,r,p) = \Gamma_{\text{sg}}(s^2) \, \tilde{\lambda}_1^{\alpha\mu\nu} + \Gamma_2^{\text{sym}}\!\left(\frac{2s^2}{3}\right) \tilde{\lambda}_2^{\alpha\mu\nu}$$

The soft-gluon form factor is defined as:

$$\Gamma_{\text{sg}}(q^2) = \lim_{p^2 \to 0} \left[ \Gamma_1(q^2, q^2, p^2) + \frac{3}{2} \, \Gamma_3(q^2, q^2, p^2) \right]$$

---

## 3. Functional Profile of the Soft-Gluon Form Factor Γₛᵍ(s²)

The source publication provides **no explicit closed-form fit** of the type
F₁(s²) = f(s²; {aᵢ}) with tabulated parameters. The following functional
behavior is reconstructed from the published text, figures, and analytical
arguments:

| Momentum Regime | Behavior of F₁(s²) ≃ Γₛᵍ(s²) | Physical Origin |
|-----------------|-------------------------------|-----------------|
| **UV** (s ≫ 3–4 GeV) | Perturbative logarithmic running: F₁ → 1 + O(αₛ ln s²) | Asymptotic freedom; one-loop running | 
| **Intermediate** (s ~ 1–3 GeV) | Smooth interpolation; no zero-crossing; moderate deviation from one-loop | Onset of non-perturbative dressing |
| **IR** (s ≲ 1 GeV) | Strong suppression; onset of non-perturbative structure | Dynamical gluon mass generation, ghost-loop effects |
| **Deep IR** (s → 0) | Logarithmic singularity through ghost loops; zero-crossing of the tree-level form factor | Ghost dominance in the SDE; see also SU(2) 3D studies |

**Evidence tags:**
- UV behavior: [B] (perturbation theory + lattice confirmation)
- IR suppression: [B] (lattice data, multiple groups)
- Zero-crossing: [B–C] (confirmed in SU(2) 3D and certain SU(3) kinematic limits; full SU(3) 4D position not precisely determined)

### 3.1 Important Limitation

> **No numerical fit parameters are available from the source publication.**
> Any parametric ansatz of the form Γₛᵍ(s²) = a₀ + a₁/(s² + m²) + ...
> would require either (a) access to the raw lattice data, or (b) digitization
> of the published plots. Neither has been performed here. Fabricating fit
> parameters would violate the UIDT anti-hallucination protocol.

---

## 4. One-Loop Analysis with Effective Gluon Mass

The source publication performs a perturbative one-loop analysis of the
three-gluon vertex with and without an effective gluon mass parameter m:

- **Massless case (m = 0):** Standard one-loop running of the three-gluon
  vertex, recovering the expected UV logarithm. The IR behavior is
  qualitatively incorrect (no suppression, no zero-crossing).

- **Massive case (m ≠ 0):** Introducing the Schwinger-mechanism gluon mass
  into the one-loop integrands produces IR suppression and, depending on the
  kinematic limit, a zero-crossing. This one-loop massive analysis captures
  the qualitative lattice behavior but does not reproduce it quantitatively.

**Evidence tag:** [C] — One-loop calculation with phenomenological mass
parameter; not self-consistent (mass not dynamically generated within the
same truncation).

---

## 5. Schematic SDE for η_A(k²) with Three-Gluon, Ghost, and Four-Gluon Contributions

### 5.1 Definitions

Working in Landau gauge with the gluon propagator:

$$D_{\mu\nu}(k) = P_{\mu\nu}(k) \, \Delta(k^2), \qquad P_{\mu\nu}(k) = g_{\mu\nu} - \frac{k_\mu k_\nu}{k^2}$$

The gluon anomalous dimension is defined as:

$$\eta_A(k^2) = -\frac{\partial \ln Z_A(k^2)}{\partial \ln k^2}, \qquad Z_A(k^2) = k^2 \, \Delta(k^2)$$

equivalently:

$$\eta_A(k^2) = \frac{\partial}{\partial \ln k^2} \ln\!\left[k^2 \Delta(k^2)\right]$$

### 5.2 Truncated SDE for the Gluon Propagator

The inverse gluon propagator satisfies (schematically):

$$\Delta^{-1}(k^2) = Z_3 \, k^2 + \Pi_{\text{gh}}(k^2) + \Pi_{3g}(k^2) + \Pi_{4g}(k^2)$$

where Z₃ is the gluon wave-function renormalization constant, and the
self-energy contributions are:

#### Ghost Loop Π_gh

$$\Pi_{\text{gh}}^{\mu\nu}(k) = -g^2 N_c \int \frac{d^4q}{(2\pi)^4} \, q_\mu (q+k)_\nu \, D_G(q) \, D_G(q+k) \, \mathcal{F}_{\text{gh}}(q,k)$$

where D_G denotes the full ghost propagator and F_gh encodes the
ghost-gluon vertex dressing. In Landau gauge, the ghost-gluon vertex is
known to remain close to its tree-level form (Taylor's theorem).

**Evidence tag:** [B] — Structure well-established; ghost-gluon vertex
dressing near unity confirmed on the lattice (Cucchieri et al., Ilgenfritz
et al.).

#### Three-Gluon Loop Π_3g

$$\Pi_{3g}^{\mu\nu}(k) = \frac{g^2}{2} N_c \int \frac{d^4q}{(2\pi)^4} \, \Gamma^{(0)\,\mu\alpha\beta}(k,q,-q-k) \, \Delta(q^2) \, \Delta((q+k)^2) \, \Gamma^{\nu}{}_{\alpha\beta}(k,q,-q-k)$$

Here Γ^(0) is the bare three-gluon vertex and Γ^ν_{αβ} the fully dressed
transverse vertex. Inserting the planar degeneracy approximation:

$$\Gamma_{\alpha\mu\nu}(k,q,-q-k) \approx \Gamma_{\text{sg}}(s^2) \, \tilde{\lambda}_{\alpha\mu\nu}^{(1)}(k,q,-q-k)$$

yields:

$$\Pi_{3g}(k^2) \sim g^2 N_c \int \frac{d^4q}{(2\pi)^4} \, \Delta(q^2) \, \Delta((q+k)^2) \, \Gamma_{\text{sg}}^2(s^2) \, \mathcal{K}_{3g}(k,q)$$

where K_3g is a purely kinematic kernel arising from the contraction of the
Lorentz-color tensor structures, and s² = ½(k² + q² + (k+q)²).

**Evidence tag:** [B–D] — Integral structure is standard (B); quantitative
evaluation requires numerical implementation with lattice-calibrated
Γₛᵍ input (D).

#### Four-Gluon Loop Π_4g

$$\Pi_{4g}^{\mu\nu}(k) = \frac{g^2}{2} N_c \int \frac{d^4q}{(2\pi)^4} \, \Delta(q^2) \, \Gamma_{4g}^{\mu\nu\alpha\beta}(k,-k,q,-q)$$

The full four-gluon vertex Γ₄g is the least well-known ingredient. In
most SDE truncations it is approximated by its tree-level form or by an
effective constant. Recent lattice studies (Athenodorou et al.) have begun
to constrain its non-perturbative structure.

**Evidence tag:** [D] — Tree-level approximation common but uncontrolled;
lattice data scarce.

### 5.3 Decomposition of η_A(k²)

Taking the logarithmic derivative of the SDE yields:

$$\eta_A(k^2) = \eta_A^{(\text{gh})}(k^2) + \eta_A^{(3g)}(k^2) + \eta_A^{(4g)}(k^2) + \ldots$$

with:

$$\eta_A^{(3g)}(k^2) \sim -\frac{\partial}{\partial \ln k^2} \int \frac{d^4q}{(2\pi)^4} \, \Delta(q^2) \, \Delta((q+k)^2) \, \Gamma_{\text{sg}}^2(s^2) \, \mathcal{K}_{3g}(k,q)$$

### 5.4 Qualitative Behavior of η_A(k²)

| Regime | η_A^(gh) | η_A^(3g) | η_A^(4g) | Net η_A |
|--------|----------|----------|----------|---------|
| **UV** (k² ≫ Λ²_QCD) | Perturbative (positive, subdominant) | Perturbative (dominant, positive) | Subdominant | Positive; drives asymptotic freedom |
| **IR** (k² ~ Λ²_QCD) | Enhanced by ghost dressing | Suppressed by Γₛᵍ IR behavior | Model-dependent | Sign change possible; non-perturbative fixed point candidate |
| **Deep IR** (k² → 0) | Log-enhanced | Damped or sign-flipped (zero-crossing of Γₛᵍ) | Poorly constrained | Depends critically on relative magnitudes |

**Key finding for UIDT:** The IR suppression and potential zero-crossing of
Γₛᵍ(s²) — established from lattice data [B] — is the only known
gauge-invariant mechanism capable of inducing a sign change in η_A^(3g) in the
deep infrared. This is relevant for:

- **L4 (γ not derived from RG first principles):** A non-perturbative β-function
  fixed point at g*² = 8π²/ln(γ) would require specific magnitudes of η_A(k²)
  in the infrared. The three-gluon vertex provides the dominant channel for
  generating such behavior.

- **L1 (10¹⁰ geometric factor):** The interplay between ghost and three-gluon
  contributions to η_A may constrain the accessible range of geometric
  enhancement factors.

**Evidence tag:** [D] — Qualitative behavior well-motivated; quantitative
matching to UIDT parameters not yet achieved.

---

## 6. Relevance for UIDT γ-Scaling

The universal scaling parameter γ = 16.339 [A-] is phenomenologically
calibrated. A first-principles derivation would require establishing a
non-perturbative infrared fixed point of the pure Yang-Mills β-function.

The three-gluon vertex enters this program as follows:

1. The perturbative two-loop β-function yields γ* ≈ 55.8, a factor 3.4
   above the calibrated value. This discrepancy is documented as **L4**.

2. Non-perturbative corrections to the β-function arise primarily through
   the gluon anomalous dimension η_A(k²), which receives its dominant
   contribution from the three-gluon loop Π_3g.

3. The planar degeneracy result reduces the three-gluon vertex input to a
   single function Γₛᵍ(s²), dramatically simplifying the SDE analysis.

4. The lattice-confirmed IR suppression and zero-crossing of Γₛᵍ suggest
   that η_A^(3g) is significantly smaller in the IR than perturbation theory
   predicts, potentially bringing the fixed-point value closer to γ = 16.339.

5. **Gap to be bridged:** A quantitative SDE evaluation with realistic
   Γₛᵍ(s²) input is needed to determine whether the three-gluon vertex
   alone can close the factor-3.4 discrepancy, or whether additional
   non-perturbative effects (e.g., Gribov copies, four-gluon vertex
   corrections) are required.

**Evidence tag:** [D–E] — Program outlined; no quantitative result achieved.
Documented as L4 active research.

---

## 7. Claims Table

| Claim ID | Statement | Category | Source | Status |
|----------|-----------|----------|--------|--------|
| L4-3GV-001 | Transverse form factors of the three-gluon vertex exhibit planar degeneracy in s² = ½(q² + r² + p²) | B | arXiv:2208.01020 (Lattice, quenched SU(3)) | Active |
| L4-3GV-002 | The leading form factor Γ₁ dominates; Γ₂ ≈ O(0.1 Γ₁); Γ₃ ≈ 0 | B | arXiv:2208.01020 | Active |
| L4-3GV-003 | Planar degeneracy approximation: Γ_αμν ≈ Γₛᵍ(s²) λ̃₁^αμν | B | arXiv:2208.01020 | Active |
| L4-3GV-004 | Γₛᵍ(s²) exhibits IR suppression and log-singularity from ghost loops | B | arXiv:2208.01020; earlier soft-gluon studies | Active |
| L4-3GV-005 | Zero-crossing of the tree-level form factor occurs at very small s | B–C | arXiv:2208.01020; SU(2) 3D confirmation | Active |
| L4-3GV-006 | Schematic SDE: η_A = η_A^(gh) + η_A^(3g) + η_A^(4g) with Γₛᵍ input for Π_3g | D | Standard SDE framework; this note | Active |
| L4-3GV-007 | Quantitative β-function fixed point matching to γ = 16.339 requires full SDE evaluation with lattice-calibrated Γₛᵍ | D | UIDT L4 research program | Open |

---

## 8. Open Tasks

- [ ] Obtain or digitize Γₛᵍ(s²) data from lattice publications for
      quantitative SDE input (requires raw data access or plot digitization)
- [ ] Implement numerical evaluation of η_A^(3g)(k²) with planar degeneracy
      ansatz using mpmath (80-digit precision for UIDT compatibility)
- [ ] Compare quantitative η_A^(3g) with perturbative prediction to assess
      magnitude of non-perturbative suppression
- [ ] Evaluate whether ghost + four-gluon contributions can compensate or
      reinforce the three-gluon IR suppression
- [ ] Determine if the lattice-calibrated SDE yields a non-perturbative
      fixed point compatible with γ = 16.339 [A-]
- [ ] Cross-reference with Huber (arXiv:2004.00415) for state-of-the-art
      SDE truncation schemes including the four-gluon vertex
- [ ] Update L4 limitation status upon completion of quantitative evaluation

---

## 9. Affected Canonical Parameters

> **No ledger constants are modified by this note.**

| Parameter | Canonical Value | Category | Impact of This Note |
|-----------|----------------|----------|---------------------|
| γ | 16.339 | A- | None; documents pathway toward first-principles derivation (L4) |
| Δ* | 1.710 ± 0.015 GeV | A | None; spectral gap not directly coupled to η_A structure |
| κ | 0.500 ± 0.008 | A | None |
| λ_S | 5κ²/3 | A | None |

---

## 10. References

1. F. Pinto-Gómez, F. De Soto, M. N. Ferreira, A. C. Aguilar, J. Papavassiliou,
   *Lattice three-gluon vertex in extended kinematics: Planar degeneracy*,
   Phys. Lett. B 838 (2023) 137737.
   arXiv:2208.01020 | DOI: 10.1016/j.physletb.2023.137737

2. A. C. Aguilar, M. N. Ferreira, B. M. Oliveira, J. Papavassiliou,
   *Schwinger mechanism for gluons from lattice QCD*,
   Phys. Lett. B 838 (2023) 137737.
   arXiv:2201.08496

3. M. Q. Huber,
   *Correlation functions of Landau gauge Yang-Mills theory*,
   Phys. Rev. D 101 (2020) 114009.
   arXiv:2004.00415 | DOI: 10.1103/PhysRevD.101.114009

4. A. C. Aguilar, D. Binosi, J. Papavassiliou,
   *Gluon and ghost propagators in the Landau gauge: Deriving lattice
   results from Schwinger-Dyson equations*,
   Phys. Rev. D 78 (2008) 025010.
   arXiv:0802.1870

5. A. Athenodorou et al.,
   *On the zero crossing of the three-gluon vertex*,
   Phys. Lett. B 761 (2016) 444–449.
   arXiv:1607.01991

6. P. Boucaud, J. P. Leroy, A. Le Yaouanc, J. Micheli, O. Pène, J. Rodríguez-Quintero,
   *The infrared behaviour of the pure Yang-Mills Green functions*,
   Few-Body Syst. 53 (2012) 387–436.
   arXiv:1109.1936

---

**Cross-references within UIDT:**
- [Schwinger–Dyson Propagator Documentation](../schwinger_dyson_propagator.md)
- [RG β-Function Derivation for γ](../rg_beta_derivation_gamma.md)
- [Known Limitations (L1–L6)](../limitations.md)
- [Evidence Classification System](../evidence-classification.md)
- [Schwinger Mechanism Deep Research](../schwinger_mechanism_deep_research_2026-03-30.md)

---

*P. Rietz — DOI: 10.5281/zenodo.17835200 — UIDT Framework v3.9*
