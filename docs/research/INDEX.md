# Research Notes — Navigation Index

> **Last Updated:** 2026-05-20  
> **Purpose:** conservative navigation index for UIDT v3.9 L1/L4/L5 research.  
> **Evidence policy:** this index does not promote claims. Evidence tags describe the linked document's current role, not an upgrade in `LEDGER/CLAIMS.json`.

---

## Current Status

The active L1/L4/L5 research state is staged across PR #459 → PR #460 → PR #461 and the current cleanup branch.

| Layer | Role | Status |
|---|---|---|
| PR #459 | Session-2 Phase-8 ledger sync corrections | `TECHNICAL PASS / GUARDIAN REQUIRED` |
| PR #460 | Phase-8 delta-gamma and SU(4) audit | `TECHNICAL PASS / STACKED DEPENDENCY REQUIRED` |
| PR #461 | L1/L4/L5 reconciliation audit | `RECONCILIATION PASS / CLEANUP REQUIRED` |
| PR #467 | Documentation cleanup and path verification | `DOCS CLEANUP / REVIEW REQUIRED` |

---

## Active Documents

| Document | Role | Evidence Status | Notes |
|---|---|---|---|
| [`L1_L4_L5_roadmap_2026-05-08.md`](./L1_L4_L5_roadmap_2026-05-08.md) | Active roadmap, updated by cleanup branch | [A-]/[D]/[E] separated | No canonical promotion. |
| [`L1_L4_L5_research_reconciliation_audit_2026-05-17.md`](./L1_L4_L5_research_reconciliation_audit_2026-05-17.md) | Research-state reconciliation audit | no promotion | Tension register. |
| [`L1_L4_L5_precision_context_addendum_2026-05-20.md`](./L1_L4_L5_precision_context_addendum_2026-05-20.md) | Precision addendum | no promotion | T-010: real `mpmath` context requirement. |
| [`L1_L4_L5_index_path_verification_2026-05-20.md`](./L1_L4_L5_index_path_verification_2026-05-20.md) | Path-verification audit | no promotion | Verifies missing/existing research-note paths. |
| [`phase8_delta_gamma_su4_audit_2026-05-17.md`](./phase8_delta_gamma_su4_audit_2026-05-17.md) | Phase-8 delta-gamma/SU(4) audit | [D], [E]/TENSION | Staged in PR #460; S4-P1 remains partial [D]. |
| [`TKT-20260429-FRG-STEP5-lambda3-flow.md`](./TKT-20260429-FRG-STEP5-lambda3-flow.md) | LPA' NLO Step-5 no-go | [D] | Physical `lambda3` path does not derive `gamma`. |
| [`S4-P1_tachyon_threshold_frg.md`](./S4-P1_tachyon_threshold_frg.md) | S4-P1 torsion-threshold chain | [D] | Erratum applied: use `k_T`, not ambiguous `k_crit`. |
| [`S4-P1_tachyon_onset_full_derivation.md`](./S4-P1_tachyon_onset_full_derivation.md) | S4-P1 onset analysis | [D] | Erratum applied: `k_T` nomenclature and no [C] upgrade. |
| [`L4-Q1-algebraic-path-b-derivation-2026-04-28.md`](./L4-Q1-algebraic-path-b-derivation-2026-04-28.md) | Historical algebraic bare-gamma path | [D]/historical | Erratum applied: active SU(4) scaling is `81/4`, old `169/4` path is superseded. |
| [`l5_n99_audit.md`](./l5_n99_audit.md) | L5 N-definition audit | [D]/TENSION | Updated with SU(4) `176` vs `704/3` tension. |
| [`TKT-20260428-L4-FRG-gamma-derivation.md`](./TKT-20260428-L4-FRG-gamma-derivation.md) | Older L4 FRG plan | historical / [D] | Must be read through Step-5 no-go and Phase-8 corrections. |
| [`L1_L4_L5_nogo_analysis_2026-04-28.md`](./L1_L4_L5_nogo_analysis_2026-04-28.md) | April no-go baseline | historical / [D]/[E] | Baseline, not current terminal state. |
| [`L1_L4_L5_research_summary_2026-04-28.md`](./L1_L4_L5_research_summary_2026-04-28.md) | April summary | historical | Keep for chronology. |

---

## Topic Index

### L1 — Geometric Factor and Bare-Gamma Research

| Document | Status | Notes |
|---|---|---|
| [`L1_L4_L5_roadmap_2026-05-08.md`](./L1_L4_L5_roadmap_2026-05-08.md) | CURRENT | Active ordering for L1/L4/L5. |
| [`../theory/L1_L4_L5_session2_derivation_2026-04-29.md`](../theory/L1_L4_L5_session2_derivation_2026-04-29.md) | ERRATUM APPLIED | `gamma_bare=49/3` [D]; `k_T/k_gamma` split applied. |
| [`L4-Q1-algebraic-path-b-derivation-2026-04-28.md`](./L4-Q1-algebraic-path-b-derivation-2026-04-28.md) | ERRATUM APPLIED | Historical algebraic path; no [A]/[B] promotion. |
| [`L1_L4_L5_nogo_analysis_2026-04-28.md`](./L1_L4_L5_nogo_analysis_2026-04-28.md) | BASELINE | No-go baseline; Session-2 refines but does not prove. |
| [`L1_L4_L5_research_summary_2026-04-28.md`](./L1_L4_L5_research_summary_2026-04-28.md) | HISTORICAL | Older summary. |

### L4 — Gamma, FRG, and Delta-Gamma

| Document | Status | Notes |
|---|---|---|
| [`phase8_delta_gamma_su4_audit_2026-05-17.md`](./phase8_delta_gamma_su4_audit_2026-05-17.md) | STAGED CURRENT | Uses corrected assumptions from PR #459. |
| [`TKT-20260429-FRG-STEP5-lambda3-flow.md`](./TKT-20260429-FRG-STEP5-lambda3-flow.md) | CURRENT NO-GO | LPA' NLO physical lambda3 path is insufficient. |
| [`TKT-20260428-L4-FRG-gamma-derivation.md`](./TKT-20260428-L4-FRG-gamma-derivation.md) | HISTORICAL PLAN | Must not be used as proof of gamma derivation. |

### L5 — N=99 and SU(4) Consistency

| Document | Status | Notes |
|---|---|---|
| [`l5_n99_audit.md`](./l5_n99_audit.md) | ERRATUM APPLIED / OPEN | Includes `N=99`, `N=94.05`, and SU(4) `176` vs `704/3` tension. |
| [`phase8_delta_gamma_su4_audit_2026-05-17.md`](./phase8_delta_gamma_su4_audit_2026-05-17.md) | STAGED CURRENT | Registers SU(4) N-definition tension. |

### S4 / FRG Tachyon Research

| Document | Status | Notes |
|---|---|---|
| [`S4-P1_tachyon_threshold_frg.md`](./S4-P1_tachyon_threshold_frg.md) | ERRATUM APPLIED | Uses `k_T` for torsion threshold. |
| [`S4-P1_tachyon_onset_full_derivation.md`](./S4-P1_tachyon_onset_full_derivation.md) | ERRATUM APPLIED | Regulator independence remains open; no [C] upgrade. |
| `S4-P4-P5-P6-torsion-ir-stabilization.md` | MISSING / UNVERIFIED | Direct path fetch returned 404. |
| `S4-P7-gribov-torsion-kcrit-derivation.md` | MISSING / UNVERIFIED | Direct path fetch returned 404. |
| `S4-P7a-brst-cohomology-torsion.md` | MISSING / UNVERIFIED | Direct path fetch returned 404. |

### Loose Research Notes

| Document | Location | Status |
|---|---|---|
| `TKT-FRG-TACHYON-S2-gamma-emergent-findings.md` | `research/` | VERIFIED OUTSIDE DOCS / NEEDS EVIDENCE-LANGUAGE CLEANUP |
| `TKT-FRG-TACHYON-S2a-findings.md` | `research/` | VERIFIED OUTSIDE DOCS / METHOD NOTE |

---

## Missing or Unverified Entries from the Previous Index

These files were previously listed as current-frontier items but were not found as independent files during path verification. They must not be used as active evidence until recovered and reviewed.

| Previously indexed item | Current status | Required action |
|---|---|---|
| `L4_delta_gamma_1loop_vacuum_correction.md` | MISSING / UNVERIFIED | Locate file or remove from current-frontier set. |
| `L4_L1_L5_computational_verification_sprint_2026-05-08.md` | MISSING / UNVERIFIED | Locate file or remove from current-frontier set. |
| `L4_lattice_gamma_bare_survey.md` | MISSING / UNVERIFIED | Verify path and DOI/arXiv references before use. |
| `L1_geometric_factor_10_10_analysis.md` | MISSING / UNVERIFIED | Verify path before use. |
| `L4_three_gluon_vertex_planar_degeneracy.md` | MISSING / UNVERIFIED | Verify path and external sources before use. |

---

## Symbol Discipline

| Symbol | Meaning | Use |
|---|---|---|
| `k_T` | Torsion-threshold scale `4πE_T ≈ 30.661944 MeV` for `E_T=2.44 MeV` [C]. | S4-P1 torsion-threshold chain. |
| `k_gamma` | Gamma-emergent scale near `Delta*/gamma ≈ 104.66 MeV`. | D2 inverse gamma-emergent threshold. |
| `k_crit` | Legacy ambiguous symbol. | Avoid unless context is explicitly stated. |

---

## Quality Gate Notes

- `gamma = 16.339` remains calibrated [A-].
- `gamma_bare = 49/3` remains [D], Stratum III, as a physical UIDT identification.
- `gamma_pred = 16.338962439648224...` remains [D].
- No cosmology claim is promoted beyond [C].
- No claim in this index is promoted in `LEDGER/CLAIMS.json`.

---

## Next Required Cleanup

1. Decide whether loose `research/TKT-FRG-TACHYON-*` notes should be migrated into `docs/research/` after evidence-language cleanup.
2. Locate or intentionally retire the remaining `MISSING / UNVERIFIED` frontier entries.
3. Only after cleanup, begin the explicit scalar self-energy calculation `Pi_S(p^2)` at `p=Delta*`.
