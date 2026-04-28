# First-Principles Evidence Audit
**Date:** 2026-03-30 | **Updated:** 2026-04-26 (TKT-20260425-L1-L4-L5-first-principles)  
**Status:** DRAFT — Research Branch  
**Linked Issue:** #192  
**Author:** P. Rietz (UIDT Framework)

---

## Scope

This document records a systematic literature search (arXiv, PRD, JHEP, Lattice QCD review series) aimed at locating **independent, first-principles verifications** for three core UIDT parameters currently classified as Category A-, C, or D. The goal is to identify upgrade paths toward Category B (lattice-compatible) or Category A (rigorously proven).

All cited sources have been verified for real existence (DOI or arXiv identifier). No fabricated references.

---

## Search Protocol

- Sources: arXiv (hep-ph, hep-lat, hep-th), PRD, JHEP, Semantic Scholar, INSPIRE-HEP
- Date range: 1995–2026
- Methodology: keyword search + abstract verification + compatibility analysis
- Stratum separation: I (empirical) / II (consensus) / III (UIDT-internal) applied throughout
- Forbidden language: "solved", "ultimate", "definitive", "holy grail"

---

## Parameter 1: γ = 16.339 and γ∞ = 16.3437 (Kinetic Vacuum Parameter)

### Evidence Classification (Updated 2026-04-26)

| Quantity | Value | Evidence Category | Derivation Type | External Verification |
|---|---|---|---|---|
| γ (dressed) | 16.339 | **[A-]** | Phenomenological fit to hadronic/vacuum data | None — UIDT-internal |
| γ∞ (bare, FSS) | 16.3437 ± 10⁻⁴ | **[B]** | Finite-size scaling extrapolation (1/L²+1/L⁴ ansatz) | None — UIDT-internal |
| δγ = γ∞ − γ | 0.0047 | **[B/D]** | Numerically derived difference | None — interpretation model-dependent |

**γ must not be upgraded from [A-] to [A].** The FSS extrapolation in `docs/bare_gamma_theorem.md` is UIDT-internal and does not constitute external first-principles proof. See L4 below.

### What is being sought
An independent FRG or lattice derivation of a universal dimensionless ratio of comparable magnitude (~16) linking the non-perturbative spectral gap to kinetic vacuum expectation — *without prior knowledge of the UIDT value*.

### Relevant Literature Found

| Authors / Year | Paper | arXiv / DOI | Core Result | Stratum | Compatibility |
|---|---|---|---|---|---|
| Pawlowski et al. (2004) | Renormalization flow of Yang-Mills propagators | hep-ph/0408089 | Non-perturbative FRG vertex expansion for YM; scheme-dependent IR fixed point | II | Scaling ratios are truncation-dependent; no universal ~16 factor emerges scheme-independently |
| Dupuis et al. (2021) | The nonperturbative functional renormalization group and its applications | arXiv:2006.04853 | Comprehensive review of FRG fixed points and universality classes | II | Universal dimensionless ratios appear in O(N) models (~1–6 range); no YM ratio of magnitude ~16 identified |
| Litim & Pawlowski (2002) | Completeness and consistency of renormalisation group flows | hep-th/0110026 | Exact RG flows for gauge theories; fixed-point structure | II | Fixed-point couplings are scheme-dependent observables, not universal numbers |
| Ferreira & Papavassiliou (2025) | Gluon mass gap: origin and implications for QCD observables | Prog.Part.Nucl.Phys. 144, 104186 | Schwinger mechanism derivation of dynamical gluon mass gap from first principles | I–II | Mass gap derived without free parameter; ratio m_gluon/Λ_QCD ~ O(1–3), not ~16 |
| Hasenfratz & Peterson (2024) | Infrared fixed point in the massless 12-flavor SU(3) gauge-fermion system | arXiv:2402.18038, PRD 109, 114507 | Lattice IRFP at g²_GF★ = 6.60(62); critical exponent γ_g★ = 0.199(32) | B | Dimensionless coupling at fixed point is g² ~ 6.6, not ~16; different physical quantity |
| Chiu (2017–2018) | β-function SU(3) N_f=10 domain-wall fermions | PRD 99 (2019) | IRFP at g²★ ≈ 7.55(36) in GF scheme | B | Confirms scheme-dependent IRFP values in range 5–15; none correspond to γ_UIDT |

### Assessment

**Stratum I/II finding:** The FRG and lattice programs produce scheme-dependent IR coupling values. For near-conformal SU(3) theories (N_f = 10–12), these range from g²★ ~ 5.5–15.0 depending on scheme and fermion content (arXiv:2306.07236; PRD 109, 114507). Pure Yang-Mills (N_f = 0) is confining — no IRFP exists; instead, the running coupling diverges in the IR.

**Stratum III (UIDT):** γ = 16.339 is derived internally via a Banach fixed-point argument on the UIDT field equations. It does not correspond to any directly measurable scheme-independent lattice coupling.

**[TENSION ALERT]** Numerical proximity (g²=15.0 vs γ=16.339) is noted. Difference: Δ = 1.34. No physical identification is justified without independent derivation.

**L4 Blocking Point (open):** γ is phenomenologically calibrated, not RG-derived. Until an independent derivation exists, γ stays [A-] and all derived quantities are capped accordingly.

**Upgrade path to Category B:**
- Compute the ratio Δ★/v (UIDT spectral gap / vacuum scale) via independent lattice simulation of pure SU(3) Yang-Mills using gradient flow renormalization
- Identify whether any scheme-independent combination of gluon propagator parameters reproduces γ without input
- Candidate observable: ratio of Gribov mass parameter γ_GZ to dynamical gluon mass m_gl in the Refined Gribov-Zwanziger framework (see arXiv:2402.17534)

---

## Parameter 2: E_T = 2.44 MeV (Torsion Binding Energy, Category C)

### What is being sought
A lattice QCD study or topological QFT analysis producing a torsion-related binding energy or entropic stabilization increment in discrete vacuum configurations at the MeV scale.

### Relevant Literature Found

| Authors / Year | Paper | arXiv / DOI | Core Result | Stratum | Compatibility |
|---|---|---|---|---|---|
| de Forcrand et al. (1998) | Topological Properties of the QCD Vacuum at T=0 and T~T_c | hep-lat/9802017 | Topological susceptibility χ^(1/4) ≈ 185 MeV for SU(3); instanton size 0.5–0.6 fm | B | Energy scale is ~(185 MeV)⁴; no MeV-scale torsion signal isolated |
| Alexandrou et al. (2005) | The Reality of the Fundamental Topological Structure in the QCD Vacuum | hep-lat/0506018 | Long-range topological charge density confirmed in quenched QCD | B | Confirms topological reality; no MeV-scale binding energy measurable |
| Lucini et al. (2020) | Higher topological charge and the QCD vacuum | PRResearch 2, 033359 | Higher-charge topological sectors modify vacuum structure in SU(N) | B | Topology affects vacuum energy at Λ_QCD scale (~200 MeV), not MeV scale |
| Gogokhia (2006) | Mass gap in QCD | hep-th/0604095 | Dynamical mass gap generated by nonlinear gluon self-interaction; gap ~ Λ_QCD | II | MeV-scale gap not produced; all gaps are at Λ_QCD ~ 200–300 MeV |

### Assessment

**Stratum I finding:** Lattice QCD establishes that topological vacuum structures are real. However, all measured energy scales are at or above Λ_QCD (~200 MeV). No dedicated MeV-scale torsion study exists.

**Stratum III (UIDT):** E_T = 2.44 MeV is calibrated from cosmological constraints (Category C), not derived from Yang-Mills axioms.

**L5 Blocking Point (open):** The cascade step count N=99 used in vacuum energy calculations has no first-principles derivation. Downstream quantities using N=99 are capped at [D] evidence until a derivation from YM axioms is provided.

**Upgrade path to Category B:**
- Design a dedicated SU(3) lattice simulation targeting discrete torsion operators (analogous to the center vortex operator but tracking holonomy twists)
- Measure the free energy difference between topologically twisted and untwisted sectors in the MeV regime
- Reference methodology: 't Hooft twisted boundary conditions on small lattices (see Lucini et al. 2020 for technique)

---

## Parameter 3: ~17.1 MeV Thermodynamic Limit (Wolpert Analogue, Category D)

### Assessment

**No Wolpert-limit analogue in QFT at the MeV scale has been found in the literature.** This remains Category D.

**Upgrade path to Category D→B:** Requires formal extension of Wolpert's stochastic thermodynamics framework to infinite-dimensional QFT Hilbert spaces — an open mathematical problem not yet addressed in the literature.

---

## Summary Table (Updated 2026-04-26)

| Parameter | UIDT Category | Evidence Found | Nearest External Result | Δ (numerical) | L-Deficiency | Upgrade Feasibility |
|---|---|---|---|---|---|---|
| γ = 16.339 | A- | No direct crosscheck | g²★=15.0(5), SU(3) N_f=10 (arXiv:2306.07236) | 1.34 (different quantity) | **L4** (no RG derivation) | Low |
| γ∞ = 16.3437 | B | UIDT-internal FSS only | — | — | **L1** (L⁴ factor unexplained), **L4** | B confirmed internally only |
| E_T = 2.44 MeV | C/D | No lattice MeV signal | Nuclear T_c ≈ 15 MeV (different physics) | ~12 MeV gap | **L5** (N=99 unjustified) | Hard |
| ~17.1 MeV limit | D | No QFT analogue | Nuclear T_c ≈ 15 MeV | ~2 MeV proximity | — | Very hard |

---

## Open Limitations Register (L1 / L4 / L5)

These three deficiencies are formally registered as blocking points for evidence upgrades:

| ID | Description | Affected Parameters | Evidence Cap | Status |
|---|---|---|---|---|
| **L1** | Holographic amplification factor L⁴ (~4521–10¹⁰) has no first-principles derivation | γ∞, δγ, w_a, all cosmological quantities | [C] max | Open |
| **L4** | γ = 16.339 is phenomenologically calibrated, not derived from RG flow from first principles | γ, all quantities derived from γ | [A-] max (blocked from [A]) | Open |
| **L5** | Cascade step count N=99 is empirically chosen; no derivation from YM axioms | E_T, vacuum energy cascade quantities | [D] max | Open |

All three deficiencies must be formally resolved (with independent derivation + Reproduction Note) before affected quantities can receive evidence upgrades.

---

## Constraints (UIDT Constitution)

- Parameter values in IMMUTABLE PARAMETER LEDGER are **unchanged** by this audit
- This document is Stratum III documentation only — no physics code is modified
- All citations verified: DOI/arXiv IDs confirmed real
- mp.dps = 80 local precision requirement untouched
- RG constraint 5κ² = 3λ_S: unchanged; λ_S = 5/12 (exact) per TKT-20260403-LAMBDA-FIX

---

## Next Steps (Checklist)

- [ ] Update `LEDGER/` entries for γ, E_T, 17.1 MeV with `external_crosscheck: false` and `upgrade_path` field
- [ ] Update `FORMALISM.md` with explicit Stratum I/II/III table for each mechanism
- [ ] Add this document link to `CHANGELOG.md` under `[3.9.1] - 2026-03-30`
- [ ] Track upgrade path for γ (L4): commission pure SU(3) YM gradient-flow ratio study
- [ ] Track upgrade path for E_T (L5): design dedicated twisted-boundary lattice simulation + derive N=99 from YM axioms
- [ ] Track upgrade path for L1: derive holographic L⁴ factor from first principles

---

*Original audit date: 2026-03-30. Updated: 2026-04-26 (TKT-20260425-L1-L4-L5-first-principles).*  
*Audit policy: zero hallucinations. All sources verified against arXiv/DOI. No fabricated papers.*
