# Experimental Validation Roadmap — UIDT v3.9

> **Author:** P. Rietz  
> **Date:** 2026-05-10  
> **Status:** ACTIVE  
> **DOI:** 10.5281/zenodo.17835200  
> **Follows from:** PR #443 (Ontology Manuscript finalisation)

---

## Preamble

The philosophical and mathematical foundation of UIDT v3.9 is now closed (see
`manuscript/UIDT_Ontology_v3.9.tex`, PR #443). What follows is the confrontation
with physical evidence. This document defines the strategic research programme
across two tracks:

1. Strategic analysis and reframing of the 7.96σ H₀ tension
2. Experimental validation pathway for Pillars III and IV

Every action item is classified by its evidence category and carry-over impact
on the kill-switch architecture.

---

## Track 1 — H₀ Tension (7.96σ)

### Current Status

| Quantity | Value | Source | Category |
|----------|-------|--------|----------|
| UIDT canonical H₀ | 70.4 ± 0.16 km/s/Mpc | DESI DR2 calibration | [C] |
| DESI+CMB H₀ | 68.17 ± 0.28 km/s/Mpc | DESI DR2 Results II | Stratum I |
| Planck 2018 H₀ | 67.4 ± 0.5 km/s/Mpc | Planck Collab. 2018 | Stratum I |
| Tension (UIDT vs DESI+CMB) | **7.96σ** | PR #443 disclosure box | — |
| Tension (UIDT vs Planck) | **~6σ** | estimated | — |

### Three-Interpretation Framework

#### Interpretation 1 — Calibration Artefact [C]

UIDT H₀ = 70.4 was calibrated to DESI late-time BAO data. Planck H₀ is
reconstructed from early-time CMB photons under the assumption w = −1
(ΛCDM). These two measurements probe fundamentally different cosmic epochs
under different model assumptions. The tension between them is a **pre-existing
cosmological problem** (the Hubble Tension), not a UIDT failure. UIDT
reproduces a tension already present in the observational landscape.

**Evidence tag:** [C] — calibrated to external data.  
**Action:** Reformulate disclosure box to make the epoch-dependence explicit.

#### Interpretation 2 — Feature, Not Bug [D]

UIDT predicts dynamical dark energy w(z) ≠ −1. The Planck H₀ reconstruction
assumes a static cosmological constant w = −1 throughout cosmic history. If
UIDT is correct, the Hubble Tension is a **signature of dynamical dark energy**
— evidence *for* the framework, not against it. The tension reveals the
inadequacy of ΛCDM as the reference model, not of UIDT as a theory.

**Evidence tag:** [D] — prediction, not yet verified.  
**Action:** Draft explicit subsection in `cosmological_implications_v3.9.md`
arguing that DESI Y1/Y2 hints at dynamic w(z) support this interpretation.

#### Interpretation 3 — Open Research Problem [A-adjacent]

Until H₀ is derived from UIDT first principles without calibration input,
all calibrated values are provisional. This is a Limitation L5-adjacent
condition and must be declared as such in all public-facing documents.

**Evidence tag:** [A-adjacent] — structural constraint.  
**Action:** Add explicit open-question box to ontology manuscript.

### Recommended Disclosure-Box Update

The existing disclosure box in `manuscript/UIDT_Ontology_v3.9.tex` must be
updated to:

- [ ] Distinguish **model-vs-model tension** from **theory-vs-experiment failure**
- [ ] State clearly: Planck H₀ is a ΛCDM-derived parameter under w = −1;
      UIDT H₀ is derived under w(z) variable
- [ ] Retain `[TENSION ALERT]` classification
- [ ] Add three-interpretation block with evidence tags
- [ ] Note: formal recalibration requires PI authorisation (Decision D-002)

---

## Track 2 — Pillar III: Laboratory Verification

### III.a — Casimir Anomaly at λ = 0.66 nm

**Prediction:** Measurable deviation ΔF/F from the standard Casimir force at
plate separation d = 0.660 ± 0.005 nm, arising from coupling of S(x) to the
vacuum field configuration.

**Evidence category:** [D] — prediction, unverified.  
**Kill-switch:** F2 (Torsion Binding Energy / Casimir scale) — currently pending.

**Technology assessment:**
AFM-Casimir experiments currently operate reliably at d > 10 nm. Sub-nm
measurements are at the experimental frontier (Cannex collaboration, Lamoreaux
group). The 0.66 nm scale corresponds to the UIDT holographic vacuum wavelength
(calibrated, [C]).

**Action items:**

- [ ] **III.a-1:** Draft technical dossier specifying ΔF/F(d) with full error
      propagation from UIDT parameters. Minimum required force resolution must
      be stated explicitly.
- [ ] **III.a-2:** Define kill-switch F2 precisely:
      *If at d = 0.660 nm ± 0.005 nm the force anomaly ΔF/F is excluded at*
      *> 3σ confidence, F2 is triggered and Pillar III.a is refuted.*
- [ ] **III.a-3:** Contact Cannex collaboration with technical dossier.
      Offer integration of UIDT prediction into their data analysis pipeline.
- [ ] **III.a-4:** File as Issue referencing this roadmap.

**Target evidence upgrade:** [D] → [C] (if consistent) or [F] (if excluded).

---

### III.b — Glueball Resonance m_S = 1.705 GeV

**Prediction:** Scalar glueball / UIDT scalar excitation at
m_S = 1.705 ± 0.015 GeV [D], coupling to the scalar 0⁺⁺ channel.
Lattice QCD range for lightest scalar glueball: 1.5–1.7 GeV.

**Evidence category:** [D] — prediction.  
**Kill-switch:** F1 (Lattice QCD continuum limit, existing) — theory-killing.
Current status: z = 0.37σ (passed).

**Action items:**

- [ ] **III.b-1:** Draft technical paper comparing UIDT m_S prediction with
      available BESIII and Belle II scalar-channel data.
- [ ] **III.b-2:** Derive explicit decay channel predictions:
      - f₀(1710) → 2π
      - f₀(1710) → 4π
      - f₀(1710) → KK̄
      These must follow from the UIDT coupling κ and the scalar VEV v = 47.7 MeV [A].
- [ ] **III.b-3:** Contact BESIII collaboration. Offer UIDT parameter set for
      inclusion in scalar-channel analysis.
- [ ] **III.b-4:** Kill-switch F1 is already the dominant test. Ensure
      `falsification-criteria.md` reflects the 1.5–1.7 GeV lattice window.

**Target evidence upgrade:** [D] → [B] (lattice consistent) or [F] (excluded).

---

### III.c — Fundamental Scalar Field Parametrisation

**Prediction:** A fundamental scalar S(x) coupled to the Yang-Mills sector at
coupling κ = 0.500 ± 0.008 [A].

**Status:** Currently underspecified for experimental targeting. Without
explicit mass and coupling-strength predictions at collider energies, a
dedicated experimental search is not yet feasible.

**Action items:**

- [ ] **III.c-1:** Derive the scalar propagator mass m_S and production
      cross-section at LHC Run 4 energies from the fixed-point equations.
      This is prerequisite to kill-switch F5.
- [ ] **III.c-2:** Specify the S(x)-gluon vertex in terms of κ and lattice
      input. Deliverable: one-page technical summary.
- [ ] **III.c-3:** Kill-switch F5 (LHC scalar resonance): if > 5σ exclusion
      of any 0⁺⁺ resonance in 1.5–1.9 GeV window at Run 4, Pillar III.c refuted.

**Target evidence upgrade:** [D] → [D/B] depending on derivation completeness.

---

## Track 3 — Pillar IV: Photonic Isomorphism

**Prediction:** Critical refractive index n_crit = γ = 16.339 ± 0.1 [D] in
nonlocal metamaterials, exhibiting a phase transition analogous to the vacuum
information density phase transition.

**Evidence category:** [D] — prediction, unverified.  
**Kill-switch:** F4 (Photonic Isomorphism).

**Technology assessment:**
Song et al. (2025, *Nature Communications* 16: 8915,
DOI: 10.1038/s41467-025-63981-3) demonstrated photonic analogies for parallel
spaces and wormholes in nonlocal artificial media. n = 16.339 is far beyond
standard dielectrics (typical n < 4); metamaterial engineering is required.

**Action items:**

- [ ] **IV-1:** Derive the observable signature at n = n_crit:
      - Transmission anomaly T(n)?
      - Reflection peak R(n)?
      - Nonlinear group velocity threshold?
      Without this specification, F4 is not operationally testable.
- [ ] **IV-2:** Contact Song et al. group or equivalent photonic metamaterial
      group. Inquire whether a material or effective-medium structure achieving
      n_eff ≈ 16.339 is within reach.
- [ ] **IV-3:** Define kill-switch F4 operationally:
      *If at n = 16.339 ± 0.1 no anomalous transmission or phase transition is*
      *observed at > 3σ in a verified metamaterial platform, F4 is triggered.*
- [ ] **IV-4:** Document the S(x) ↔ metamaterial refractive index mapping
      rigorously. The isomorphism must be derivable, not merely analogical.

**Target evidence upgrade:** [D] → [C] (if consistent) or [F] (if excluded).

---

## Meta-Strategy: Experimental Pitch Document

A single "Experimental Pitch" document targeting experimentalists must be
created with the following structure:

```
For each Pillar:
- One-page summary
- Prediction (yes/no falsifiable statement)
- Required instrument and sensitivity
- Kill-switch threshold
- Contact offer
```

**Action items:**

- [ ] **Meta-1:** Draft `docs/outreach/experimental_pitch_v1.0.md` (one page
      per pillar: Casimir, Glueball, Scalar, Photonic).
- [ ] **Meta-2:** Register UIDT v3.9 on arXiv as a formal preprint address.
      GitHub alone is not sufficient for experimental community outreach.
- [ ] **Meta-3:** Identify one experimental contact per pillar:
      - III.a → Cannex collaboration
      - III.b → BESIII / Belle II
      - IV  → Song et al. / photonic metamaterial groups

---

## Validation Roadmap Summary

| Pillar | Prediction | Category | Kill-Switch | Next Deliverable |
|--------|-----------|----------|-------------|------------------|
| III.a | Casimir anomaly at 0.660 nm | [D] | F2 | Technical dossier ΔF/F(d) |
| III.b | Glueball m_S = 1.705 GeV | [D] | F1 (active) | Technical paper + BESIII contact |
| III.c | Fundamental scalar S(x) | [D] | F5 | Fixed-point mass derivation |
| IV | Photonic n_crit = 16.339 | [D] | F4 | Effect specification |
| Meta | H₀ tension 7.96σ | [C]/open | — | Disclosure-box update |

---

## Pre-Flight Check

- [x] No `float()` introduced
- [x] `mp.dps = 80` precision not modified
- [x] RG constraint 5κ² = 3λ_S not touched
- [x] No deletion > 10 lines in /core or /modules
- [x] Ledger constants unchanged:
  - Δ* = 1.710 ± 0.015 GeV [A]
  - γ = 16.339 [A-]
  - v = 47.7 MeV [A]
  - w₀ = −0.99 [C]
  - E_T = 2.44 MeV [C]

---

*P. Rietz — ORCID 0009-0007-4307-1609 — DOI: 10.5281/zenodo.17835200*
