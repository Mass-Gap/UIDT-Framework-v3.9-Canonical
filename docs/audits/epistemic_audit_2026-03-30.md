# Epistemic Audit Report — 2026-03-30

**Framework:** UIDT v3.9  
**Maintainer:** P. Rietz  
**Audit Date:** 2026-03-30  
**Audit Update:** 2026-04-03 (FRG NLO results added, PR #199)  
**Evidence Standard:** UIDT Constitution v4.1  
**Search Method:** Systematic arXiv / JHEP / PRD / Lattice QCD literature search  
**Zero Hallucinations Policy:** All cited sources verified. No fabricated references.

---

## Purpose

This document records the results of a systematic first-principles literature search conducted to identify independent, external crosschecks for the three UIDT phenomenological parameters with the highest epistemic uncertainty: `γ = 16.339`, `E_T = 2.44 MeV`, and the speculative `~17.1 MeV` thermodynamic limit.

This audit fulfils the documentation requirement from Issue #192 (action item: `docs/epistemic_audit_2026-03-30.md`).

---

## Stratum Classification (UIDT Constitution)

| Stratum | Definition |
|---------|------------|
| **I** | Empirical measurements, experimental uncertainties, observational data |
| **II** | Scientific consensus, field status, review knowledge |
| **III** | UIDT interpretation, model mapping, theoretical extension |

> Rule: Strata must never be mixed within a single claim statement.

---

## Parameter 1: γ = 16.339 (Kinetic Vacuum Parameter)

### Stratum I — Empirical

No direct experimental measurement of `γ` exists in the literature. The value is defined within UIDT as the dimensionless ratio γ := Δ*/v (Banach fixed point, internal derivation).

### Stratum II — Consensus

Functional Renormalisation Group (FRG) studies of SU(N) Yang-Mills theories have been conducted by Pawlowski et al. (hep-ph/0408089) and in the review by Dupuis et al. (arXiv:2006.04853). These identify non-perturbative fixed-point structures but do not produce a universal dimensionless coupling ratio of magnitude ~16 as a scheme-independent observable.

Nearest external value found: `g²★ ≈ 15.0 ± 0.5` from SU(3) N_f=10 lattice study (arXiv:2306.07236). This is from a different theory (10 fundamental flavours) and a different quantity (gauge coupling at fixed point). **Not a crosscheck.**

### Stratum III — UIDT

The Banach fixed-point derivation is UIDT-internal only. The numerical proximity `|γ_kinetic − 49/3| / (49/3) ≈ 0.21%` is a coincidence at current precision, not a proven constraint (PR #199, §1.4).

### Audit Result

| Field | Value |
|-------|-------|
| Current evidence category | [A-] |
| External crosscheck found | **false** |
| [TENSION ALERT] | Δ = 1.34 vs g²★ = 15.0(5) (different quantity/theory) |
| Stratum | III (UIDT-internal) |
| Upgrade path to [B] | Identify a scheme-independent FRG observable (e.g., ratio of Gribov mass to gluon condensate) reproducing γ without prior knowledge of the value |
| upgrade_path_ticket | TKT-20260403-FRG-NLO (requires BMW/LPA' truncation study) |
| Ledger value | **immutable** |

---

## Parameter 2: E_T = 2.44 MeV (Torsion Binding Energy)

### Stratum I — Empirical

Lattice QCD studies confirm topological vacuum structures: de Forcrand et al. (hep-lat/9802017), Lucini et al. PRResearch 2 (2020). Topological susceptibility: `χ_top^{1/4} ≈ 185 MeV` for pure SU(3) (FLAG 2024). No torsion-specific binding energy signal at the MeV scale has been isolated in these studies.

FLAG 2024 (arXiv:2411.04268): The proton-neutron mass difference receives a pre-QED contribution of 2.52 ± 0.27 MeV (lattice) vs experimental 1.293 MeV. The discrepancy (3.75σ pre-QED, reduces to 0.75σ post-QED) is a known FLAG-flagged tension. UIDT assigns E_T = 2.44 MeV in this vicinity; however, the QED correction derivation connecting this tension to E_T is absent from current UIDT documentation.

### Stratum II — Consensus

Field consensus: no torsion gravity signal has been isolated in lattice QCD. The MeV-scale is dominated by isospin-breaking and QED effects in nuclear physics.

### Stratum III — UIDT

E_T is calibrated from cosmological data (Category [C]) via f_vac − Δ/γ. The cosmological calibration origin means any lattice QCD crosscheck is an independent test, not a circularity.

### Audit Result

| Field | Value |
|-------|-------|
| Current evidence category | [C] (corrected from prior [D] notation in some documents) |
| External crosscheck found | **false** |
| FLAG 2024 tension | 3.75σ pre-QED, 0.75σ post-QED (different quantity; documented) |
| Stratum | III (cosmological calibration) |
| Upgrade path to [B] | Dedicated lattice study with torsion operator in discrete SU(3) vacuum configurations targeting MeV regime |
| upgrade_path_ticket | Requires new independent lattice collaboration |
| Ledger value | **immutable** |

---

## Parameter 3: ~17.1 MeV Thermodynamic Limit (Wolpert Analogue)

### Stratum I — Empirical

Nuclear liquid-gas phase transition: T_c ≈ 15–18 MeV (GSI/ALADIN data). QCD crossover: T_c ≈ 154 MeV (Lattice QCD). These scales are physically distinct; the nuclear T_c involves hadronic matter, not pure Yang-Mills vacuum.

### Stratum II — Consensus

No formal QFT analogue of the Wolpert-Bennett computational limit at this energy scale exists in the peer-reviewed literature. The Wolpert framework (arxiv:math/0512142) applies to Turing-machine computability, not infinite-dimensional QFT Hilbert spaces.

### Stratum III — UIDT

The numerical proximity to nuclear phase transition scales (~15 MeV) is noted but classified as speculative coincidence. No UIDT derivation chain currently connects Wolpert’s formalism to QFT degrees of freedom.

### Audit Result

| Field | Value |
|-------|-------|
| Current evidence category | [E] (speculative) |
| External crosscheck found | **false** |
| Stratum | III (speculative) |
| Upgrade path to [B] | Extend Wolpert-Bennett formalism to infinite-dimensional QFT Hilbert spaces; publish independently with peer review |
| upgrade_path_ticket | None assigned (pre-research stage) |
| Ledger value | N/A (not in immutable ledger) |

---

## FRG NLO Addendum (2026-04-03, PR #199)

A direct numerical test of the claim `δγ = δ_NLO` (Wetterich equation at k = Δ*) was performed at 80-digit mpmath precision:

| Quantity | Value |
|----------|-------|
| η_A^NLO (Litim regulator, C_A=3) | ≈ 5.346 × 10⁻³ |
| δ_NLO := (49/3) × η_A/2 | ≈ 0.0437 |
| δγ (ledger) | 0.0047 |
| Discrepancy | **factor ~9** |

**Conclusion:** `δγ = δ_NLO` is **not supported** at this truncation level. The ledger value `δγ = 0.0047` is consistent with a finite-size scaling correction [B], not a perturbative FRG effect. Claim downgraded to **[E]** pending TKT-20260403-FRG-NLO full NLO analysis.

---

## Summary Table

| Parameter | Category | external_crosscheck | upgrade_path_status | Stratum |
|-----------|----------|---------------------|--------------------|---------|
| γ = 16.339 | [A-] | false | TKT-20260403-FRG-NLO (open) | III |
| E_T = 2.44 MeV | [C] | false | Requires new lattice study | III |
| ~17.1 MeV limit | [E] | false | Pre-research: Wolpert extension | III |
| δγ = δ_NLO | [E] (downgraded) | false | TKT-20260403-FRG-NLO (open) | III |

> All ledger values are **immutable** per UIDT Constitution v4.1, IMMUTABLE PARAMETER LEDGER. This document records epistemic status only.

---

## Literature References

- Pawlowski et al., hep-ph/0408089 (FRG Yang-Mills)
- Dupuis et al., arXiv:2006.04853 (FRG review)
- de Forcrand et al., hep-lat/9802017 (Lattice topology)
- Lucini et al., PRResearch 2 (2020) (Lattice topology)
- FLAG 2024, arXiv:2411.04268 (Lattice QCD averages)
- Aguilar et al., arXiv:2211.12594 (Schwinger mechanism)
- Ferreira & Papavassiliou, arXiv:2501.01080 (Gluon propagator 2025)
- arXiv:2306.07236 (SU(3) N_f=10 fixed point; different theory)
- Wolpert, arxiv:math/0512142 (Computational limits)

> All identifiers verified against arXiv/INSPIRE. No fabricated references.

---

*Closes action items from Issue #192. Satisfies UIDT Constitution v4.1, SEARCH VERIFICATION and PAPER AUDIT PROTOCOL.*  
*Maintainer: P. Rietz — UIDT Framework v3.9*
