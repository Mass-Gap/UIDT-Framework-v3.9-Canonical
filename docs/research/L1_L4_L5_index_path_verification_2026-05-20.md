# L1/L4/L5 Index Path Verification Audit

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-20  
> **Branch:** `TKT-2026-05-20-l1-l4-l5-docs-cleanup`  
> **Stacked on:** PR #467 → PR #461 → PR #460 → PR #459  
> **DOI:** `10.5281/zenodo.17835200`  
> **Status:** Path-verification audit. No evidence-category promotion.

---

## Purpose

This audit verifies the remaining `NEEDS REVIEW`, `MISSING / UNVERIFIED`, and loose `research/` entries referenced by the cleaned `docs/research/INDEX.md`.

This is a documentation-governance audit only. It does not resolve L1, L4, or L5 and does not update `LEDGER/CLAIMS.json`.

---

## Summary Verdict

`REVIEW-REQUIRED`

Several files exist but require errata or evidence-language cleanup before they can be treated as current research references. Several earlier frontier entries remain path-missing and should not be cited as current evidence. Loose `research/` notes exist, but should not be moved into `docs/research/` without evidence-language cleanup.

---

## 1. Previously MISSING / UNVERIFIED Frontier Entries

GitHub search found these terms only through `docs/research/INDEX.md` during this audit, not as independent files on the checked repository state.

| File | Verification result | Action |
|---|---|---|
| `L4_delta_gamma_1loop_vacuum_correction.md` | `MISSING` | Keep out of Current Frontier. If recovered, require full review before indexing. |
| `L4_L1_L5_computational_verification_sprint_2026-05-08.md` | `MISSING` | Keep out of Current Frontier. If recovered, require full review before indexing. |
| `L4_lattice_gamma_bare_survey.md` | `MISSING` | Do not use for [B] or lattice claims until file and DOI/arXiv sources are verified. |
| `L1_geometric_factor_10_10_analysis.md` | `MISSING` | Do not cite as active L1 analysis until file is located. |
| `L4_three_gluon_vertex_planar_degeneracy.md` | `MISSING` | Do not cite until file and external source chain are verified. |

---

## 2. Existing `NEEDS REVIEW` Entries

### 2.1 `docs/research/L4-Q1-algebraic-path-b-derivation-2026-04-28.md`

**Path status:** `EXISTS`  
**Recommended index status:** `EXISTS / NEEDS ERRATUM`

Key concern: the file describes the algebraic `N_c=3` identity around `gamma_bare = 49/3` and contains stronger language such as `Evidence B` for parts of the construction. Under the Phase-8 cleanup policy, the arithmetic identity is exact, but the physical UIDT identification must remain [D], Stratum III.

Required cleanup:

- Add erratum: physical `gamma_bare = 49/3` remains [D].
- Remove or qualify `Evidence B` wording unless a verified external lattice source is cited.
- Ensure no text implies `gamma = 16.339` is derived.

### 2.2 `docs/research/l5_n99_audit.md`

**Path status:** `EXISTS`  
**Recommended index status:** `EXISTS / CURRENT LIMITATION STUB`

The file correctly states that `N=99` vs `N=94.05` remains unresolved. It is short but conservative.

Required cleanup:

- Add the new SU(4) N-definition tension: `176` vs `704/3`.
- Keep L5 OPEN.
- Do not promote `N=99` beyond [D].

### 2.3 `docs/research/S4-P1_tachyon_onset_full_derivation.md`

**Path status:** `EXISTS`  
**Recommended index status:** `EXISTS / NEEDS k_T ERRATUM`

The file still uses `k_crit` and contains older `k_crit = E_T*(N_c^2-1)*pi/2` notation. It also labels the result [D*] and discusses an upgrade path.

Required cleanup:

- Rename S4-P1 torsion-threshold symbol to `k_T`.
- Add the corrected canonical value `k_T = 30.6619442990... MeV` for `E_T=2.44 MeV`.
- Retain [D] / research-note status unless regulator-independence is demonstrated.

### 2.4 `docs/research/S4-P4-P5-P6-torsion-ir-stabilization.md`

**Path status:** `MISSING` via direct path fetch.  
**Recommended index status:** `MISSING / UNVERIFIED`

Action: keep out of active current list until located.

### 2.5 `docs/research/S4-P7-gribov-torsion-kcrit-derivation.md`

**Path status:** `MISSING` via direct path fetch.  
**Recommended index status:** `MISSING / UNVERIFIED`

Action: keep out of active current list until located. If recovered, it must be audited for `k_crit` ambiguity.

### 2.6 `docs/research/S4-P7a-brst-cohomology-torsion.md`

**Path status:** `MISSING` via direct path fetch.  
**Recommended index status:** `MISSING / UNVERIFIED`

Action: keep out of active current list until located.

---

## 3. Loose `research/` Notes

### 3.1 `research/TKT-FRG-TACHYON-S2-gamma-emergent-findings.md`

**Path status:** `EXISTS outside docs/research`  
**Recommended index status:** `VERIFIED OUTSIDE DOCS / NEEDS EVIDENCE-LANGUAGE CLEANUP`

Important content:

- D2 gamma-emergent scale line with `k_crit = 104.718 MeV` and `gamma_emergent = 16.3296` [D].
- This is the `k_gamma` line, not the S4-P1 torsion threshold `k_T`.
- It contains language implying possible future upgrade toward [C] or [A]. This must be constrained by current evidence rules.

Required cleanup before migration:

- Rename ambiguous `k_crit` to `k_gamma` for this D2 context.
- Explicitly state `gamma = 16.339` remains [A-].
- Remove or qualify any implication that [A] promotion is near; residual and scheme-independence are not satisfied.
- Verify SVZ / lattice references before any [B] statement is retained.

### 3.2 `research/TKT-FRG-TACHYON-S2a-findings.md`

**Path status:** `EXISTS outside docs/research`  
**Recommended index status:** `VERIFIED OUTSIDE DOCS / METHOD NOTE`

Important content:

- Documents that S2-a v1 had a methodological bug: the UV initial mass was already tachyonic, so no sign-change detection was possible.
- Defines S2-a v2 with positive UV mass and tighter tolerances, but result remains outstanding.

Required cleanup before migration:

- Preserve as method-correction note.
- Keep evidence at [D] / method status.
- Do not imply [C] upgrade until the v2 run exists and external validation is available.

---

## 4. Updated Index Recommendations

| Entry | New recommended status |
|---|---|
| `L4_delta_gamma_1loop_vacuum_correction.md` | `MISSING / UNVERIFIED` |
| `L4_L1_L5_computational_verification_sprint_2026-05-08.md` | `MISSING / UNVERIFIED` |
| `L4_lattice_gamma_bare_survey.md` | `MISSING / UNVERIFIED` |
| `L1_geometric_factor_10_10_analysis.md` | `MISSING / UNVERIFIED` |
| `L4_three_gluon_vertex_planar_degeneracy.md` | `MISSING / UNVERIFIED` |
| `L4-Q1-algebraic-path-b-derivation-2026-04-28.md` | `EXISTS / NEEDS ERRATUM` |
| `l5_n99_audit.md` | `EXISTS / CURRENT LIMITATION STUB` |
| `S4-P1_tachyon_onset_full_derivation.md` | `EXISTS / NEEDS k_T ERRATUM` |
| `S4-P4-P5-P6-torsion-ir-stabilization.md` | `MISSING / UNVERIFIED` |
| `S4-P7-gribov-torsion-kcrit-derivation.md` | `MISSING / UNVERIFIED` |
| `S4-P7a-brst-cohomology-torsion.md` | `MISSING / UNVERIFIED` |
| `research/TKT-FRG-TACHYON-S2-gamma-emergent-findings.md` | `VERIFIED OUTSIDE DOCS / NEEDS EVIDENCE-LANGUAGE CLEANUP` |
| `research/TKT-FRG-TACHYON-S2a-findings.md` | `VERIFIED OUTSIDE DOCS / METHOD NOTE` |

---

## 5. Next Cleanup Actions

1. Add erratum to `L4-Q1-algebraic-path-b-derivation-2026-04-28.md`.
2. Add SU(4) `N` tension to `l5_n99_audit.md`.
3. Add `k_T` erratum to `S4-P1_tachyon_onset_full_derivation.md`.
4. Decide whether to migrate the loose `research/TKT-FRG-TACHYON-*` files into `docs/research/` or keep them in `research/` with explicit links and warning labels.
5. Do not begin new physics derivation until the high-risk evidence-language cleanup is complete.

---

## Acceptance Status

`PATH VERIFICATION COMPLETE / CLEANUP STILL REQUIRED`

The index is now auditable, but some existing files still require errata before they can be treated as current research references.
