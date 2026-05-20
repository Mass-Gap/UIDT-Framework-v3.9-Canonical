# L1/L4/L5 Research Reconciliation Audit

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-17  
> **Branch:** `TKT-2026-05-17-l1-l4-l5-research-reconciliation`  
> **Stacked on:** PR #460, which is stacked on PR #459  
> **DOI:** `10.5281/zenodo.17835200`  
> **Status:** Repository-state reconciliation audit. No evidence-category promotion.  

---

## 0. Executive Finding

The L1/L4/L5 research state is not blocked by lack of ideas; it is blocked by **state disorder**:

1. Root files, `CANONICAL/`, `docs/research/`, `docs/theory/`, and loose `research/` notes do not present the same current state.
2. `docs/research/INDEX.md` lists several current-frontier documents that are not retrievable from current `main`.
3. Several older documents use evidence language that is now too strong or stale relative to PR #459/#460 corrections.
4. The corrected Phase-8 state is:
   - `gamma_bare(Nc) = (2Nc+1)^2/Nc` [D]
   - `gamma_bare(3) = 49/3` [D]
   - `Delta_gamma_required = 17/3000` [D]
   - `k_crit = 4*pi*E_T = 30.6619442990... MeV` for `E_T = 2.44 MeV` [D]
   - `gamma_pred = 16.338962439648224...` [D]
   - SU(4): `gamma_bare(4)=81/4=20.25` [D]
   - SU(4) N-definition has `[TENSION ALERT]`: `176` vs `704/3`.
5. The Phase-8 verification scripts must use explicit residual checks for decimal/rational mixed quantities; exact `mpmath.mpf` equality is too brittle for ledger-decimal comparisons.

Therefore the next logical action is not another speculative derivation. The next action is a **Research State Consolidation PR** that makes the repository navigable and eliminates stale/contradictory roadmaps.

---

## 1. Audit Scope

This audit reviewed the L1/L4/L5/FRG/gamma/N=99 state across the following repository areas:

| Area | Documents sampled/read | Role |
|---|---|---|
| Root | `README.md`, `STATUS.md` | Public-facing state summary |
| Canonical | `CANONICAL/LIMITATIONS.md`, `CANONICAL/CONSTANTS.md` via PR #459 context | Canonical constraints and limitation definitions |
| Research index | `docs/research/INDEX.md` | Navigation / discoverability |
| April L1/L4/L5 docs | `L1_L4_L5_research_summary_2026-04-28.md`, `L1_L4_L5_nogo_analysis_2026-04-28.md`, `TKT-20260428-L4-FRG-gamma-derivation.md` | Older no-go baseline |
| Session 2 | `docs/theory/L1_L4_L5_session2_derivation_2026-04-29.md` | gamma_bare / S4 chain origin |
| FRG Step 5 | `docs/research/TKT-20260429-FRG-STEP5-lambda3-flow.md` | LPA' NLO no-go |
| S4-P1 | `docs/research/S4-P1_tachyon_threshold_frg.md` | tachyon-threshold chain |
| Loose research notes | `research/TKT-FRG-TACHYON-S2-gamma-emergent-findings.md`, `research/TKT-FRG-TACHYON-S2a-findings.md` | later D2 tachyon-flow attempts |
| Current open PRs | PR #459, PR #460 | corrected Phase-8 assumptions and first audit |

This audit is not a full literal parse of every file in the repository. It is a targeted content audit of the active L1/L4/L5 research surface and its immediate dependency documents.

---

## 2. Current State by Source Group

### 2.1 Root README.md

Root README presents UIDT as an active research framework and correctly warns that Category A designations refer to internal mathematical consistency, not external validation. It also states gamma as [A-] and preserves H0 as calibrated [C], not a solved tension. However, it contains public-facing language such as “Central Result” and broad physical significance statements that should be periodically rechecked against current evidence tags.

**Audit status:** usable but needs alignment with PR #459/#460 after merge.

### 2.2 Root STATUS.md

`STATUS.md` currently says the latest research includes “Color Algebra Identity [A]: gamma_bare=(2Nc+1)^2/Nc=49/3 proven at 80-digit precision.” This conflicts with the stricter Phase-8 state. The arithmetic identity is exact, but the physical identification of gamma_bare with the UIDT gamma sector remains [D]/Stratum III unless a complete first-principles derivation and ledger entry exist.

**Required fix:** downgrade STATUS wording from “Color Algebra Identity [A]” to “Arithmetic identity [A] / physical gamma_bare conjecture [D]”.

### 2.3 CANONICAL/LIMITATIONS.md

`CANONICAL/LIMITATIONS.md` is conservative and still states L4 correctly: gamma is phenomenologically determined and not derived from RG flow. It also permits gamma derivation exploration in research mode with [E] tag. This is broadly compatible with PR #459/#460, but it is versioned as `v3.7.2`, stale relative to v3.9.

**Required fix:** update version header and add Phase-8 TENSION entries without changing canonical values.

### 2.4 docs/research/INDEX.md

`docs/research/INDEX.md` is the most important discoverability surface and currently contains stale references.

Examples:

| Indexed file | Audit result |
|---|---|
| `L4_delta_gamma_1loop_vacuum_correction.md` | listed but not retrievable from current main |
| `L4_L1_L5_computational_verification_sprint_2026-05-08.md` | listed but not retrievable from current main |
| `L4_lattice_gamma_bare_survey.md` | listed; retrieval not yet verified in this pass |
| `L1_L4_L5_roadmap_2026-05-08.md` | retrievable, but too skeletal and stale relative to #459/#460 |

**Required fix:** rebuild index from actual tree, classify documents as CURRENT / SUPERSEDED / MISSING / STAGED-IN-PR.

### 2.5 April 28 No-Go Baseline

The April 28 no-go documents are still important. They establish that L1/L4/L5 remain open and that many derivation paths fail. However, some details are now superseded:

- The April no-go state treated `49/3` as outside the tight ledger band and speculative [E].
- Session 2 and PR #459/#460 refine this into: `49/3` is a valid bare-gamma conjecture [D], but the correction `17/3000` remains uncomputed.
- The core epistemic result remains unchanged: no [A] derivation exists.

**Required fix:** mark April 28 as baseline/no-go, not current terminal state.

### 2.6 Session 2 Derivation

Session 2 is the origin of the `49/3` and S4-P1 chain. It is valuable but contains stale details relative to PR #459/#460:

- Good: `gamma_bare=(2Nc+1)^2/Nc=49/3`.
- Good: required positive correction `Delta_gamma=+0.00567`.
- Stale: `k_crit` historical value around `30.707 MeV` must be replaced or annotated with `30.661944... MeV` for `E_T=2.44 MeV`.
- Risk: “Evidenzklasse [D] unless marked otherwise” is correct, but public summaries elsewhere inflated some arithmetic identities to [A].

**Required fix:** add erratum note pointing to PR #459.

### 2.7 FRG Step 5

FRG Step 5 remains a strong no-go:

- Physical `lambda3(UV)=0.034823...` gives `Z_phi(IR)=1.0000019`, not gamma.
- Shooting solution requires `lambda3*=99.638`, about `2857x` physical lambda3.
- Therefore LPA' NLO cannot derive gamma from the physical lambda3 path.

**Required fix:** no physics change; make this a hard blocker in the roadmap so old plans do not retry LPA' as if untested.

### 2.8 S4-P1 Tachyon Threshold

S4-P1 is still the strongest numerical [D] vector, but it must be corrected:

- Historical: `k_crit ≈ E_T*4pi ≈ 30.707 MeV`.
- Correct for `E_T=2.44 MeV`: `k_crit=30.6619442990... MeV`.
- Corrected `gamma_pred=16.338962439648224...` remains a partial numerical hit [D].
- Residual is `3.756e-5`, not [A].

**Required fix:** after #459 merge, all S4-P1 docs should carry an erratum block.

### 2.9 D2 Tachyon-Flow Loose Research Notes

The loose `research/TKT-FRG-TACHYON-S2...` notes are important but not integrated into `docs/research`.

They show a separate D2 line:

- `gamma_emergent=16.3296` with residual about `0.0094`, roughly `2*delta_gamma`.
- `k_crit=104.718 MeV`, conceptually different from the S4-P1 `k_crit≈30.66 MeV` chain.
- S2-a v1 found `k_crit NOT REACHED` due to a bad tachyonic UV initial condition.
- S2-a v2 is defined but result is outstanding.

**Critical reconciliation issue:** The repository currently has at least two different “tachyon threshold” k_crit meanings:

| Symbol use | Scale | Context |
|---|---:|---|
| `k_crit≈30.66 MeV` | S4-P1 torsion threshold, `4*pi*E_T` | S4-P1 gamma_pred chain |
| `k_crit≈104.718 MeV` | D2 gamma-emergent RG scale, `Delta*/gamma` region | FRG-TACHYON-S2 |

These must be renamed or disambiguated before any further derivation.

### 2.10 Verification Script Robustness

PR #459 and PR #460 initially used exact `mpmath.mpf` equality for decimal/rational mixed comparisons such as:

```python
assert delta_gamma_required == mp.mpf(17) / mp.mpf(3000)
```

This is brittle because `gamma_ledger = mp.mpf("16.339")` and `17/3000` are created through different high-precision decimal/rational paths. The mathematical residual is approximately `1.72e-80`, which is far below the [A] threshold of `1e-14`, but exact equality can still fail.

**Required fix:** use explicit residual gates, e.g.

```python
expected_delta = mp.mpf(17) / mp.mpf(3000)
delta_residual = abs(delta_gamma_required - expected_delta)
assert delta_residual < mp.mpf("1e-70"), mp.nstr(delta_residual, 80)
```

**Audit status:** fixed on the PR #459 and PR #460 branches after the second Gate Review.

---

## 3. Tension Register

| ID | Tension | Severity | Required Action |
|---|---|---:|---|
| T-001 | `STATUS.md` says gamma_bare color identity [A]; physical gamma_bare remains [D] | Critical | Rewrite status wording |
| T-002 | `docs/research/INDEX.md` lists files missing from main | Critical | Rebuild index from actual tree |
| T-003 | S4-P1 historical `30.707 MeV` conflicts with `E_T=2.44 MeV` exact product | Critical | PR #459 erratum across docs |
| T-004 | Two different `k_crit` meanings: 30.66 MeV vs 104.718 MeV | Critical | Rename symbols: e.g. `k_T` and `k_gamma` |
| T-005 | SU(4) N-definition: `176` vs `704/3` | Major | Decide fixed-b0 convention vs pure-YM b0(Nc) |
| T-006 | LPA' NLO path already no-go, but older roadmaps still point to generic LPA'/BMW without hard exclusion | Major | Roadmap consolidation |
| T-007 | Evidence distribution in STATUS.md differs from CLAIMS.json recovery state and open PR staged claims | Major | Recompute statistics after merge |
| T-008 | Loose `research/` notes are not in `docs/research/INDEX.md` | Major | Move or index them explicitly |
| T-009 | Verification scripts used brittle exact `mpmath.mpf` equality for decimal/rational mixed comparisons | Critical | Replace exact equality with explicit residual gates; fixed in #459/#460 branches after Gate Review v2 |

---

## 4. Logical Next Steps

### Step 1 — Merge / review PR #459

Purpose: establish corrected assumptions.

Required before any further physics:

- `gamma_bare(Nc)=(2Nc+1)^2/Nc`
- `k_crit=30.6619442990... MeV` for `E_T=2.44 MeV`
- no evidence promotion
- verification script must pass residual-gate checks rather than brittle exact equality
- Guardian / SSOT gate must be documented before any migration into `LEDGER/CLAIMS.json`

### Step 2 — Merge / review PR #460

Purpose: record the first corrected Phase-8 research pass.

Key outcomes:

- `Delta_gamma_required=17/3000`
- coefficient-scale audit gives `C≈0.2184` for `alpha_s/(4pi)` ansatz
- S4-P1 partial hit remains [D]
- SU(4) `N` tension registered

### Step 3 — Research-state cleanup PR

This audit recommends a dedicated cleanup PR that only edits navigation / errata docs:

- `STATUS.md`
- `docs/research/INDEX.md`
- `docs/research/L1_L4_L5_roadmap_2026-05-08.md`
- erratum blocks in Session 2 and S4-P1 documents
- optional move/index of loose `research/TKT-FRG-TACHYON-*` notes

No physics constants should change.

### Step 4 — Symbol disambiguation

Before further computation, define:

| Proposed symbol | Meaning |
|---|---|
| `k_T` | torsion-threshold scale `4*pi*E_T ≈ 30.661944 MeV` |
| `k_gamma` | D2 gamma-emergent threshold near `Delta*/gamma ≈ 104.66 MeV` |
| `k_crit` | deprecated ambiguous symbol unless context is explicit |

### Step 5 — Actual next physics calculation

Only after cleanup:

1. Explicit scalar self-energy `Pi_S(p^2)` at `p=Delta*`.
2. Use corrected target `Delta_gamma_required=17/3000`.
3. Fail-fast criteria:
   - if correction < 0: reject L1 bare-gamma ansatz
   - if correction > 0.012: reject L1 bare-gamma ansatz
   - if no diagrammatic coefficient emerges: remain [D]/[E]
4. In parallel, resolve SU(4) N convention before using SU(4) for claim promotion.

---

## 5. Proposed Roadmap Replacement

The repository should converge on the following active roadmap:

| Priority | Task | Reason | Output |
|---:|---|---|---|
| 0 | Reconcile docs/index/status | current state inconsistent | cleanup PR |
| 1 | Merge corrected assumptions (#459) | prevents wrong formulas | constants/ledger staging |
| 2 | Keep Phase-8 audit (#460) | records true partial/no-go state | research report + script |
| 3 | Rename `k_crit` usages | removes symbol collision | errata + roadmap |
| 4 | Compute `Pi_S(p^2)` explicitly | only direct P1 path | verification script |
| 5 | Resolve SU(4) N convention | blocks SU(4) falsification | short theory note |
| 6 | Extract SU(4) lattice data | external [B] test | data table + DOI/arXiv |
| 7 | Regulator-independence S4-P1 | tests [D] robustness | multi-regulator script |
| 8 | Full BMW/Dyson FRG | only after above cleanup | long-running solver |

---

## 6. Acceptance Status

`[RECONCILIATION REQUIRED BEFORE NEW CLAIMS]`

The repository contains enough research to proceed, but the current documentation graph is inconsistent. Further derivation work without cleanup risks duplicating no-go paths or mixing the two tachyon-threshold scales.

No [A] or [C] evidence-category promotion is justified at this time.

---

## 7. Reproduction / Verification Commands

After PR #459 and PR #460 are locally available:

```bash
python verification/scripts/verify_session2_phase8_sync.py
python verification/scripts/verify_phase8_delta_gamma_su4_audit.py
python verification/scripts/research/verify_frg_step5_lambda3_flow.py
```

Expected classification:

```text
PR #459: corrected arithmetic PASS with explicit residual gates
PR #460: partial numerical hit / SU4 tension PASS with explicit residual gates
FRG Step 5: NO-GO confirmed
```

---

## 8. Final Audit Verdict

The logical next step is **not** to declare Phase 8 successful. The logical next step is:

1. merge/review #459,
2. merge/review #460,
3. execute a cleanup PR from this reconciliation audit,
4. then calculate the explicit one-loop scalar self-energy.

This preserves the correct scientific order: repository truth first, then numerics, then evidence review.
