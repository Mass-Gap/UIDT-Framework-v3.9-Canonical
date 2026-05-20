# TKT-FRG-TACHYON S2-a — Method Correction Note

> **UIDT Framework:** v3.9 Canonical  
> **Migration date:** 2026-05-20  
> **Source path:** `research/TKT-FRG-TACHYON-S2a-findings.md`  
> **Target path:** `docs/research/TKT-FRG-TACHYON-S2a-findings.md`  
> **Status:** Migrated method note. No evidence-category promotion.  
> **DOI:** `10.5281/zenodo.17835200`

---

## 0. Migration Erratum — 2026-05-20

This file is a cleaned migration of a loose `research/` note into `docs/research/`. It preserves the methodological finding from S2-a while constraining evidence-upgrade language.

Mandatory interpretation rules:

1. S2-a v1 produced `k_gamma: NOT REACHED` because the UV initial mass was already tachyonic.
2. This is a methodological finding, not a physical falsification of the D2 gamma-emergent path.
3. S2-a v2 is a proposed corrected run; its result is not yet available.
4. No [C] or [A] upgrade is active.
5. `gamma = 16.339` remains [A-].

---

## 1. Methodological Finding

The original S2-a test used an initial condition with:

```text
m2_0 < 0
```

The sign-change detector searched for a transition:

```text
m2 > 0  ->  m2 < 0
```

If the UV initial value is already negative, the detector cannot observe the transition. Therefore:

```text
k_gamma: NOT REACHED
```

is a method result, not a physical no-go.

---

## 2. Corrected Boundary Condition

The corrected S2-a v2 plan requires a positive UV scalar mass:

```text
m2_0 = +(kappa_tilde_0 * k_UV)^2
```

with:

```text
k_UV = Delta* = 1710 MeV
kappa_tilde_0 ≈ 0.04877718 [D]
m_UV ≈ 83.4 MeV
```

The earlier `|m_S| ~ 344 MeV` scale is an IR-condensate-related scale and must not be used as the UV initial mass.

---

## 3. Numerical Policy for Any Re-run

A valid current re-run must use:

```python
from mpmath import mp
mp.dps = 80
```

and must avoid:

```text
float()
round()
unittest.mock
MagicMock
```

Critical residual checks must be explicit. For [A]-level closure, residual must be `< 1e-14`.

---

## 4. Evidence Status

| Statement | Evidence | Status |
|---|---|---|
| S2-a v1 had a negative UV initial mass and could not detect a positive-to-negative transition. | [D] method audit | retained |
| S2-a v2 requires positive UV mass. | [D] method proposal | retained |
| S2-a v2 derives `gamma = 16.339`. | not supported | no result exists |
| S2-a supports [C] promotion. | not supported | external validation absent |

---

## 5. Required Follow-Up

| Step | Task | Output |
|---:|---|---|
| 1 | Implement or locate current S2-a v2 verifier under `verification/scripts/`. | script path |
| 2 | Run with positive UV mass and real 80-dps context. | log |
| 3 | Report whether a stable `k_gamma` sign-change exists. | residual table |
| 4 | Compare `gamma_emergent` to `gamma=16.339` [A-]. | [D] result or no-go |
| 5 | Test regulator sensitivity before any evidence discussion. | multi-regulator table |

---

## 6. Reproduction Note

The original note referenced branch-local execution. This migrated method note does not introduce a current canonical reproduction command. A future verifier should use a path such as:

```bash
python verification/scripts/frg_tachyon_s2a.py
```

only after the script is confirmed present on the active branch and uses the numerical policy above.

---

## 7. Acceptance Status

`MIGRATED METHOD NOTE / RESULT OUTSTANDING`

This note is now indexed as a methodological correction. It is not a physical derivation and does not authorize evidence promotion.
