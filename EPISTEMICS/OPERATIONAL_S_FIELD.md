# Operational Status of the S(x) Field

**Evidence Category: D (Prediction / Theoretical Construct)**  
**Stratum: III (UIDT-specific interpretation)**  
**Maintainer: P. Rietz**  
**Last reviewed: 2026-05-10**

---

## 1. Status Declaration

The Vacuum Information Density scalar field S(x) is a **theoretical construct** of the UIDT
framework.  It does not yet have a direct experimental operationalisation.  Every experimental
reference in the UIDT literature is an *indirect proxy* for one or more aspects of the vacuum
structure that S(x) models.

This document supersedes any implicit or explicit suggestion elsewhere in the repository that
S(x) is a directly measurable quantity.  The Born-rule analogy is instructive: UIDT currently
lacks an equivalent of Born's probability interpretation.  Providing such a rule is an open
research objective (see Section 5).

---

## 2. Proxy Channels (Indirect Operationalisation)

| Channel | Observable | UIDT mapping | Evidence | Reference |
|---------|-----------|--------------|----------|-----------|
| QCD sum-rules gluon condensate | ⟨αs G²/π⟩ ≈ 0.277 GeV⁴ | Vacuum energy density ∝ S₀ | B | PDG 2024 |
| Hadronic torsion binding energy | ET = 2.44 MeV | Torsion sector of S(x) | C | LEDGER/CONSTANTS.md |
| Casimir anomaly @ 0.66 nm | Force deviation from Lifshitz | Geometric S(x) gradient | D | Kill-switch K3 |
| Photonic analogue n_crit = 16.339 | Critical refractive index in non-local meta-material | γ-invariant sector of S(x) | D | Kill-switch K5 |
| Lattice continuum-limit mass-gap | Δ_lat (N_f=0, SU(3)) | Spectral gap = Δ* | B | Kill-switch K1 |

None of these channels constitutes a *direct* measurement of S(x) as a local field value at a
point x ∈ ℝ⁴.  They are necessary, not sufficient, conditions for the theory.

---

## 3. Ontological Scope

The claim that information geometry is *fundamental* (rather than a useful modelling language) is
**Evidence E (Speculative)** and belongs to Stratum III.  The purely mathematical results
(mass-gap proof architecture, RG fixed point, OS axiom verification) are independent of this
ontological claim and carry their own evidence ratings.

Separation of strata:

- **Stratum I / Evidence A–B**: Standard QFT + lattice, no UIDT-specific assumptions.
- **Stratum II / Evidence B–C**: Phenomenological calibration against experiment.
- **Stratum III / Evidence D–E**: UIDT-specific mapping of S(x) onto physical observables.

---

## 4. Known Limitation L7 (New)

> **L7**: No direct experimental operationalisation of S(x) as a local field value exists.
> All experimental connections are via indirect proxy channels listed in Section 2.
> Until a Born-equivalent measurement rule is established, S(x) retains Evidence category D.

This limitation must be cited in the main manuscript abstract and in LIMITATIONS.md.

---

## 5. Open Research Objective

Formulate a measurement protocol M(x, V, δ) such that:

- M samples a spatial volume V around point x,
- returns a real number interpreted as an average ⟨S(x)⟩_V,
- has a well-defined continuum limit δ → 0,
- is consistent with the indirect proxy values in Section 2.

Candidate approaches: lattice vacuum correlator at short distance, precision Casimir
spectroscopy, QED vacuum-birefringence experiments (PVLAS/ATLAS-ALP).
