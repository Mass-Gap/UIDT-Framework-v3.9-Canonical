# L2: Electron Mass Residual — Structural Analysis and Resolution Pathways

> **Author:** P. Rietz  
> **Date:** 2026-05-10  
> **Status:** RESEARCH — not canonical, not ledger-elevated  
> **Evidence:** [E] speculative / [D] candidate pathways  
> **Follows from:** BETA-W4 (#359), L1/L4/L5 audit (#358)  
> **DOI:** 10.5281/zenodo.17835200

---

## 1. Current Status of L2

**Limitation L2 (Electron Mass Residual):** The electron mass derived via
γ-scaling exhibits a **23% residual** relative to the CODATA measured value.
Status: **Under investigation.** Not resolved. Not ledger-upgraded.

The BETA-W4 research note (PR #359) claims a pathway [III] reducing the
residual to 0.2%. This claim carries **Research status only** and has
not been independently verified or elevated to Evidence [B] or above.
L2 remains formally open.

---

## 2. Why L2 Is a Structural Problem, Not a Numerical One

The γ-scaling mechanism of UIDT operates in the **SU(3) colour sector**:
it couples the vacuum information density S(x) to the Yang–Mills gauge
configuration through the term κ S Tr(F_{μν} F^{μν}). The mass gap
Δ* = 1.710 GeV [A] and the kinetic VEV v = 47.7 MeV [A] are properties
of this colour-charged vacuum.

The **electron**, however, is an SU(3) colour singlet. In the Standard Model,
its mass arises from Yukawa coupling to the Higgs VEV:

    m_e = y_e · v_H / √2,    v_H ≈ 246 GeV

This is a fundamentally different mechanism from QCD-scale dimensional
transmutation. Applying γ-scaling to derive a lepton mass conflates two
ontologically distinct mass-generation channels. The 23% residual is therefore
a **structural signal**: γ-scaling does not natively describe the lepton sector.

**Comparison:** The glueball sector (QCD-charged) is where γ-scaling is
physically motivated. The additional tension UIDT m_G = 3.420 GeV [D] vs.
experimental X(2370) at 2.370 GeV (PR #373, ~45% discrepancy) suggests
that even within QCD, the second-generation glueball prediction faces
serious strain. L2 and the glueball tension are structurally related:
both indicate that γ-scaling is sector-specific and not universal.

---

## 3. Three Resolution Pathways

All three pathways are classified [E] (speculative) unless analytically
closed. None modify the immutable parameter ledger.

---

### Pathway A — Yukawa Coupling to S(x) [E]

**Concept:** Introduce a separate Yukawa-type coupling of the lepton
fields to the vacuum information density S(x):

    L_Yukawa = y_l \bar{\psi}_L S \psi_R + h.c.

where y_l is a dimensionless Yukawa coupling, not derived from γ, but
potentially expressible as a rational function of γ and the SU(3) Casimir
structure.

**Advantage:** This cleanly separates the lepton mass mechanism from the
Yang–Mills sector. S(x) couples to leptons through a distinct channel;
γ-scaling governs the QCD sector only. The 23% residual becomes a
missing-coupling problem, not a scaling failure.

**Open question:** Can y_e be derived from the UIDT fixed-point equations
(κ, λ_S) without introducing a new free parameter? If y_e is simply
fitted, L2 is traded for a new phenomenological parameter.

**Evidence tag:** [E] — speculative until analytic derivation exists.

**Kill-switch:** If y_e cannot be derived without free fitting, Pathway A
reduces to curve-fitting and does not resolve L2 structurally.

---

### Pathway B — Koide Relation [E]

**Concept:** The Koide formula is the empirical lepton mass relation:

    (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3

This relation holds to experimental precision < 10^{-5} and has no
Standard Model derivation. Its value 2/3 is a candidate for an
information-geometric vacuum constraint.

**UIDT relevance:** The UIDT framework posits S(x) as the generator of
geometric structure. A vacuum that generates γ = 16.339 [A-] via SU(3)
Casimir structure might also constrain lepton mass ratios through a
related algebraic mechanism. Specifically:

    Is 2/3 (Koide) derivable from the SU(3) Casimir C_2 = 4/3
    or from the colour factor N_c = 3 in the UIDT algebra?

    Observation: 2/3 = 2/N_c = 1 - 1/N_c (for N_c = 3).
    This is also the ratio appearing in the Gribov no-pole condition
    (alpha_s_Gribov = 1/N_c in 4D convention, see alpha_s_convention.md).

**Open question:** Whether this numerical coincidence reflects a deep
structural connection or is accidental. A derivation would require
showing that the S(x) vacuum configuration, when restricted to the
U(1)_em sector, generates a mass-ratio constraint of the Koide form.

**Evidence tag:** [E] — numerical observation, no derivation.

**Note:** The Koide relation has no established derivation in any
current framework. UIDT would be the first to provide one if this
pathway closes. This is high-risk, high-reward research.

---

### Pathway C — E_T Vielfache + Mixing Angles [E]

**Concept:** The torsion binding energy E_T = 2.44 MeV [C] has been
observed in the repo to coincide with light quark mass scales:

    E_T = 2.44 MeV ≈ m_u    (CODATA: m_u ≈ 2.2 MeV)
    E_{T,iso} = 4.88 MeV ≈ m_d    (CODATA: m_d ≈ 4.7 MeV)

This suggests that the torsion sector — not γ-scaling — may be the
correct energy scale for fermion mass generation in UIDT.

**For leptons:** Rather than applying γ-scaling, one could model the
electron as an excitation in the torsion-lattice sector with a separate
**mixing angle** θ_l:

    m_e = E_T · f(θ_l)

where f(θ_l) is a dimensionless geometric function of the leptonic
mixing angle. This would parallel the quark-sector E_T coincidences
but require a new derivation of θ_l from UIDT geometry.

**Advantage:** E_T = 2.44 MeV [C] is already in the canonical ledger.
No new free parameters are introduced if θ_l can be derived from the
existing fixed-point structure.

**Open question:** Is there a geometric mechanism in the torsion sector
that selects lepton-specific mixing angles? The U(1)_em charge must be
explained within this picture.

**Evidence tag:** [E] — speculative, E_T quark coincidences are [C].

---

## 4. Pre-Flight Check

- [x] No `float()` introduced
- [x] `mp.dps = 80` not modified
- [x] RG constraint 5κ² = 3λ_S not touched
- [x] No deletion > 10 lines in /core or /modules
- [x] Ledger constants unchanged:
  - Δ* = 1.710 ± 0.015 GeV [A]
  - γ = 16.339 [A-]
  - v = 47.7 MeV [A]
  - E_T = 2.44 MeV [C]
  - w₀ = −0.99 [C]

---

## 5. Recommended Next Steps

| ID | Action | Evidence Target |
|----|--------|-----------------|
| L2-A1 | Derive y_e from (κ, λ_S) fixed-point without free parameter | [E] → [D] |
| L2-B1 | Check if Koide 2/3 follows from SU(3) colour algebra (N_c = 3, C_2 = 4/3) | [E] → [D] |
| L2-C1 | Compute m_e from E_T + mixing angle hypothesis; compare to CODATA | [E] → [D] |
| L2-X1 | Formally declare L2 sector boundary: γ-scaling does not apply to leptons | Documentation |
| L2-X2 | Add explicit L2 sector-boundary note to `UIDT_Ontology_v3.9.tex` (PR #443) | Documentation |

---

*P. Rietz — ORCID 0009-0007-4307-1609 — DOI: 10.5281/zenodo.17835200*
