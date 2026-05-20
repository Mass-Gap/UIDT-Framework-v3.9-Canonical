# TKT-FRG-TACHYON S2 — Gamma-Emergent Findings

> **UIDT Framework:** v3.9 Canonical  
> **Migration date:** 2026-05-20  
> **Source path:** `research/TKT-FRG-TACHYON-S2-gamma-emergent-findings.md`  
> **Target path:** `docs/research/TKT-FRG-TACHYON-S2-gamma-emergent-findings.md`  
> **Status:** Migrated research note with evidence-language cleanup. No evidence-category promotion.  
> **DOI:** `10.5281/zenodo.17835200`

---

## 0. Migration Erratum — 2026-05-20

This file is a cleaned migration of a loose `research/` note into `docs/research/`. It preserves the methodically relevant S2 observation while removing or constraining evidence-upgrade language.

Mandatory interpretation rules:

1. This note concerns the D2 gamma-emergent scale line, not the S4-P1 torsion threshold.
2. Use `k_gamma` for the D2 gamma-emergent inverse scale near `Delta*/gamma`, not `k_crit`.
3. `gamma = 16.339` remains [A-], calibrated, not derived.
4. `gamma_emergent = 16.3296` remains [D], not [A], [B], or [C].
5. No upgrade path to [C] or [A] is active without independent validation and a regulator-independent derivation.

---

## 1. Scope

The original S2 note investigated a tachyonic FRG-flow line in which a gamma-like scale emerges from an inverse relation near:

```text
k_gamma ~ Delta*/gamma
```

This scale is approximately:

```text
Delta*/gamma = 1710 MeV / 16.339 ≈ 104.66 MeV
```

It is distinct from the S4-P1 torsion threshold:

```text
k_T = 4*pi*E_T = 30.6619442990... MeV
```

---

## 2. Recorded S2 Result

The original S2 finding reported a value near:

```text
gamma_emergent ≈ 16.3296
```

with a residual to the calibrated ledger value:

```text
|gamma_emergent - 16.339| ≈ 0.0094
```

This is approximately twice the canonical finite-size shift scale `delta_gamma = 0.0047` [A- context].

Current evidence status: [D].

---

## 3. Methodological Interpretation

The S2 result is useful as a diagnostic of a D2-style inverse gamma scale. It is not a derivation of `gamma = 16.339`.

The original note included language suggesting possible evidence upgrade paths. Under the current UIDT v3.9 evidence discipline, those statements are constrained:

| Earlier implication | Current status |
|---|---|
| `gamma_emergent` may support upgrade toward [C] | not active without independent validation |
| residual close to `delta_gamma` may imply NLO closure | conjectural [D] only |
| D2 flow derives gamma | not supported |

---

## 4. Required Follow-Up

| Step | Task | Output |
|---:|---|---|
| 1 | Re-run the D2 flow with corrected UV initial conditions from S2-a v2. | numerical log |
| 2 | Use real `mpmath` context: `from mpmath import mp`; local `mp.dps = 80`. | reproducible script |
| 3 | Separate `k_gamma` from `k_T` in all outputs. | symbol-clean report |
| 4 | Test regulator dependence. | residual table |
| 5 | Keep evidence at [D] unless external validation exists. | quality-gate note |

---

## 5. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Status | Falsification Exposure |
|---|---|---:|---|---|---|---|
| S2-D2-001 | D2 gamma-emergent scale lies near `Delta*/gamma`. | `~104.66 MeV` | [D] | III | retained | Fails if corrected flow does not produce a stable sign-change scale. |
| S2-D2-002 | Original S2 run produced `gamma_emergent≈16.3296`. | `16.3296` | [D] | III | retained as historical diagnostic | Fails as derivation because residual is too large and scheme is not regulator-independent. |
| S2-D2-003 | D2 derives `gamma=16.339`. | — | not supported | III | rejected | No first-principles closure exists. |

---

## 6. Reproduction Note

The original note referenced branch-local scripts. This migrated document does not introduce a new reproduction command. Before using this as active evidence, create or verify a current script under `verification/scripts/` with:

```bash
python verification/scripts/<d2_gamma_emergent_verifier>.py
```

Required numerical policy:

```python
from mpmath import mp
mp.dps = 80
```

No `float()`, no `round()`, no mocks.

---

## 7. Acceptance Status

`MIGRATED / METHODICALLY USEFUL / EVIDENCE [D] ONLY`

This note is now indexed as a cleaned research reference. It is not a canonical claim and does not authorize evidence promotion.
