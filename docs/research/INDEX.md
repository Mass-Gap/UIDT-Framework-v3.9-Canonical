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
| Current cleanup branch | Status/index/roadmap/errata/symbol cleanup | docs-only, no evidence promotion |

---

## Active Documents

| Document | Role | Evidence Status | Notes |
|---|---|---|---|
| [`L1_L4_L5_roadmap_2026-05-08.md`](./L1_L4_L5_roadmap_2026-05-08.md) | Active roadmap, updated by cleanup branch | [A-]/[D]/[E] separated | No canonical promotion. |
| [`L1_L4_L5_research_reconciliation_audit_2026-05-17.md`](./L1_L4_L5_research_reconciliation_audit_2026-05-17.md) | Research-state reconciliation audit | no promotion | Tension register T-001 through T-009. |
| [`L1_L4_L5_precision_context_addendum_2026-05-20.md`](./L1_L4_L5_precision_context_addendum_2026-05-20.md) | Precision addendum | no promotion | T-010: real `mpmath` context requirement. |
| [`phase8_delta_gamma_su4_audit_2026-05-17.md`](./phase8_delta_gamma_su4_audit_2026-05-17.md) | Phase-8 delta-gamma/SU(4) audit | [D], [E]/TENSION | Staged in PR #460; S4-P1 remains partial [D]. |
| [`TKT-20260429-FRG-STEP5-lambda3-flow.md`](./TKT-20260429-FRG-STEP5-lambda3-flow.md) | LPA' NLO Step-5 no-go | [D] | Physical `lambda3` path does not derive `gamma`. |
| [`S4-P1_tachyon_threshold_frg.md`](./S4-P1_tachyon_threshold_frg.md) | S4-P1 torsion-threshold chain | [D] | Requires 2026-05-20 erratum: use `k_T`, not ambiguous `k_crit`. |
| [`TKT-20260428-L4-FRG-gamma-derivation.md`](./TKT-20260428-L4-FRG-gamma-derivation.md) | Older L4 FRG plan | historical / [D] | Must be read through Step-5 no-go and Phase-8 corrections. |
| [`L1_L4_L5_nogo_analysis_2026-04-28.md`](./L1_L4_L5_nogo_analysis_2026-04-28.md) | April no-go baseline | historical / [D]/[E] | Baseline, not current terminal state. |
| [`L1_L4_L5_research_summary_2026-04-28.md`](./L1_L4_L5_research_summary_2026-04-28.md) | April summary | historical | Keep for chronology. |

---

## Topic Index

### L1 — Geometric Factor and Bare-Gamma Research

| Document | Status | Notes |
|---|---|---|
| [`L1_L4_L5_roadmap_2026-05-08.md`](./L1_L4_L5_roadmap_2026-05-08.md) | CURRENT | Active ordering for L1/L4/L5. |
| [`L1_L4_L5_nogo_analysis_2026-04-28.md`](./L1_L4_L5_nogo_analysis_2026-04-28.md) | BASELINE | No-go baseline; Session-2 refines but does not prove. |
| [`L1_L4_L5_research_summary_2026-04-28.md`](./L1_L4_L5_research_summary_2026-04-28.md) | HISTORICAL | Older summary. |
| [`../theory/L1_L4_L5_session2_derivation_2026-04-29.md`](../theory/L1_L4_L5_session2_derivation_2026-04-29.md) | ACTIVE WITH ERRATUM | `gamma_bare=49/3` [D]; `k_T` erratum required. |

### L4 — Gamma, FRG, and Delta-Gamma

| Document | Status | Notes |
|---|---|---|
| [`phase8_delta_gamma_su4_audit_2026-05-17.md`](./phase8_delta_gamma_su4_audit_2026-05-17.md) | STAGED CURRENT | Uses corrected assumptions from PR #459. |
| [`TKT-20260429-FRG-STEP5-lambda3-flow.md`](./TKT-20260429-FRG-STEP5-lambda3-flow.md) | CURRENT NO-GO | LPA' NLO physical lambda3 path is insufficient. |
| [`TKT-20260428-L4-FRG-gamma-derivation.md`](./TKT-20260428-L4-FRG-gamma-derivation.md) | HISTORICAL PLAN | Must not be used as proof of gamma derivation. |
| [`L4-Q1-algebraic-path-b-derivation-2026-04-28.md`](./L4-Q1-algebraic-path-b-derivation-2026-04-28.md) | NEEDS REVIEW | Check against Phase-8 and Step-5 before use. |

### L5 — N=99 and SU(4) Consistency

| Document | Status | Notes |
|---|---|---|
| [`l5_n99_audit.md`](./l5_n99_audit.md) | NEEDS REVIEW | Must be reconciled with SU(4) `N=176` vs `704/3` tension. |
| [`phase8_delta_gamma_su4_audit_2026-05-17.md`](./phase8_delta_gamma_su4_audit_2026-05-17.md) | STAGED CURRENT | Registers SU(4) N-definition tension. |

### S4 / FRG Tachyon Research

| Document | Status | Notes |
|---|---|---|
| [`S4-P1_tachyon_threshold_frg.md`](./S4-P1_tachyon_threshold_frg.md) | ACTIVE WITH ERRATUM | Replace ambiguous `k_crit` with `k_T` for torsion threshold. |
| [`S4-P1_tachyon_onset_full_derivation.md`](./S4-P1_tachyon_onset_full_derivation.md) | NEEDS REVIEW | Must be checked against `k_T` convention. |
| [`S4-P4-P5-P6-torsion-ir-stabilization.md`](./S4-P4-P5-P6-torsion-ir-stabilization.md) | NEEDS REVIEW | Torsion-sector follow-up. |
| [`S4-P7-gribov-torsion-kcrit-derivation.md`](./S4-P7-gribov-torsion-kcrit-derivation.md) | NEEDS REVIEW | `k_crit` naming likely requires disambiguation. |
| [`S4-P7a-brst-cohomology-torsion.md`](./S4-P7a-brst-cohomology-torsion.md) | NEEDS REVIEW | BRST/torsion context. |

### Loose Research Notes Requiring Migration or Explicit Indexing

These files are known from the reconciliation audit but may exist outside `docs/research/` on some branches. Treat as indexed dependencies only after path verification.

| Document | Current known location | Status |
|---|---|---|
| `TKT-FRG-TACHYON-S2-gamma-emergent-findings.md` | `research/` in main audit context | NEEDS MIGRATION OR LINKING |
| `TKT-FRG-TACHYON-S2a-findings.md` | `research/` in main audit context | NEEDS MIGRATION OR LINKING |

---

## Missing or Unverified Entries from the Previous Index

The previous index listed several files as current-frontier items even though they were not retrievable during the reconciliation audit. They must not be treated as current evidence until confirmed.

| Previously indexed item | Current status | Required action |
|---|---|---|
| `L4_delta_gamma_1loop_vacuum_correction.md` | MISSING / UNVERIFIED | Locate file or remove from current-frontier set. |
| `L4_L1_L5_computational_verification_sprint_2026-05-08.md` | MISSING / UNVERIFIED | Locate file or remove from current-frontier set. |
| `L4_lattice_gamma_bare_survey.md` | UNVERIFIED | Verify path and DOI/arXiv references before use. |
| `L1_geometric_factor_10_10_analysis.md` | UNVERIFIED | Verify path before use. |
| `L4_three_gluon_vertex_planar_degeneracy.md` | UNVERIFIED | Verify path and external sources before use. |

---

## Symbol Discipline

| Symbol | Meaning | Use |
|---|---|---|
| `k_T` | Torsion-threshold scale `4πE_T ≈ 30.661944 MeV` for `E_T=2.44 MeV` [C]. | S4-P1 torsion-threshold chain. |
| `k_γ` | Gamma-emergent scale near `Δ*/γ ≈ 104.66 MeV`. | D2 inverse gamma-emergent threshold. |
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

1. Verify all `NEEDS REVIEW` and `UNVERIFIED` paths.
2. Move or index loose `research/TKT-FRG-TACHYON-*` notes consistently.
3. Add errata to Session-2 and S4-P1 documents.
4. Only after cleanup, begin the explicit scalar self-energy calculation `Π_S(p²)` at `p=Δ*`.
