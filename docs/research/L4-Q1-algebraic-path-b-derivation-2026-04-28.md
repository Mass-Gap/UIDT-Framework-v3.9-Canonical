# L4-Q1: Algebraic Path B — Bare-Gamma Structure Audit

> **Original date:** 2026-04-28  
> **Cleanup erratum:** 2026-05-20  
> **Ticket:** TKT-20260428-L4-FRG-gamma-derivation  
> **Stratum:** III — UIDT-internal research  
> **Status:** Historical research note with erratum. No evidence-category promotion.

---

## 0. Cleanup Erratum — 2026-05-20

This document is retained as a historical algebraic-path audit. It must be read through the Phase-8 cleanup policy.

Mandatory corrections for all later use:

1. The arithmetic identities at fixed `N_c = 3` are exact, but the physical UIDT identification of `gamma_bare = 49/3` remains [D], Stratum III.
2. No statement in this document derives `gamma = 16.339` [A-] from first principles.
3. Earlier wording such as `Evidence B` for the lie-algebraic interpretation is downgraded to `B-context / D-interpretation` unless a verified external source is cited for the specific mapping.
4. The SU(4) extrapolation must use the Phase-8 convention check. The currently active bare-gamma conjecture is:

```text
gamma_bare(N_c) = (2*N_c + 1)^2 / N_c
```

Thus:

```text
gamma_bare(3) = 49/3
gamma_bare(4) = 81/4 = 20.25
```

The older candidate `(N_c^2 - N_c + 1)^2 / N_c` gives `169/4 = 42.25` for SU(4). It is not the current Phase-8 scaling rule and must be treated as a superseded alternative [E/D-historical].

---

## 1. Problem Statement

Earlier L4 work asked whether `49/3` could be obtained from SU(3) algebraic structure rather than inserted as a numerical target.

The corrected current question is narrower:

```text
Can an exact SU(3) arithmetic structure motivate gamma_bare = 49/3 [D],
and can a first-principles correction produce Delta_gamma_required = 17/3000 [D]?
```

This document addresses only the first part. It does not compute the correction.

---

## 2. SU(N_c) Basic Quantities

| Quantity | Formula | SU(3) value | Evidence |
|---|---:|---:|---|
| `dim(adj)` | `N_c^2 - 1` | `8` | [A] arithmetic / standard algebra |
| rank | `N_c - 1` | `2` | [A] arithmetic / standard algebra |
| `C_A` | `N_c` | `3` | [A] arithmetic / standard algebra |
| `C_F` | `(N_c^2 - 1)/(2*N_c)` | `4/3` | [A] arithmetic / standard algebra |
| pure-YM `b_0` | `11*N_c/3` | `11` | Stratum II standard context |
| `kappa` | `1/2` | `1/2` | [A] UIDT ledger |
| `lambda_S` | `5/12` | `5/12` | [A] UIDT ledger |

---

## 3. Algebraic Observations

### 3.1 SU(3)-specific identity

For `N_c = 3`:

```text
2*N_c + 1 = N_c^2 - N_c + 1 = 7
```

because:

```text
(2*N_c + 1) - (N_c^2 - N_c + 1) = N_c*(3 - N_c)
```

This equality is exact only at `N_c = 3`.

Evidence: [A] arithmetic.

### 3.2 Historical alternative structure

The older path considered:

```text
[N_c^2 - N_c + 1]^2 / N_c
```

At `N_c = 3`, this gives:

```text
7^2 / 3 = 49/3
```

However, for `N_c = 4` it gives:

```text
13^2 / 4 = 169/4 = 42.25
```

This conflicts with the current Phase-8 scaling candidate:

```text
(2*N_c + 1)^2 / N_c
```

which gives:

```text
9^2 / 4 = 81/4 = 20.25
```

Therefore the older `N_c^2 - N_c + 1` extrapolation is retained only as a historical SU(3)-coincident path, not as the active SU(N) conjecture.

---

## 4. Current Phase-8 Bare-Gamma Candidate

The current active candidate is:

```text
gamma_bare(N_c) = (2*N_c + 1)^2 / N_c
```

For SU(3):

```text
gamma_bare(3) = 49/3 = 16.333333...
```

The required correction to the calibrated kinetic value is:

```text
Delta_gamma_required = 16.339 - 49/3 = 17/3000 = 0.005666666...
```

Evidence: [D], Stratum III. This is a UIDT research mapping, not a derivation of `gamma = 16.339` [A-].

---

## 5. Gap Register

| Gap ID | Description | Status |
|---|---|---|
| G1 | Tensor-contraction path does not derive `gamma = 16.339`. | OPEN |
| G2 | Older Casimir/Banach path does not close the correction. | OPEN |
| G3 | `49/3` has SU(3)-specific arithmetic motivation, but no first-principles physical derivation. | PARTIAL / [D] |
| G4 | `beta_kappa` / FRG calculation lacks regulator-independent closure. | OPEN |
| G5 | Verification scripts must not insert `49/3` as a proof target. | OPEN / monitored |
| G6 | `49/3` differs from `gamma = 16.339` by `17/3000`. | OPEN |
| G7 | SU(4) extrapolation distinguishes historical `169/4` from active `81/4`. | OPEN / TENSION SURFACE |

---

## 6. Evidence Classification

| Statement | Evidence | Reason |
|---|---|---|
| `N_c*(3-N_c)=0` only at `N_c=3` for the identity above | [A] | arithmetic |
| `dim(adj)-rank+1 = N_c^2-N_c+1` | [A] | algebraic identity |
| physical interpretation of `dim(adj)-rank+1` as mass-carrying channels | [D] | UIDT interpretation, not externally validated |
| historical candidate `(N_c^2-N_c+1)^2/N_c` | [E]/historical | superseded as SU(N) scaling by Phase-8 candidate |
| active candidate `(2*N_c+1)^2/N_c` | [D] | UIDT research mapping |
| `gamma = 16.339` from this path | not derived | remains [A-] calibrated input |

---

## 7. Required Next Step

The necessary calculation is not another algebraic scan. The necessary calculation is the correction term:

```text
Pi_S(p^2) at p = Delta*
```

or an equivalent regulator-independent FRG correction producing:

```text
Delta_gamma_required = 17/3000
```

Fail-fast criteria:

| Result | Consequence |
|---|---|
| `Delta_gamma < 0` | reject active L1 bare-gamma ansatz |
| `Delta_gamma > 0.012` | reject active L1 bare-gamma ansatz |
| `0 < Delta_gamma <= 0.012` | retain at [D]/[D*], no promotion |
| proof-level derivation with residual `< 1e-14` | only then discuss [A]-level claim |

---

## 8. Reproduction Snippet

```python
from mpmath import mp
mp.dps = 80
N_c = mp.mpf(3)
gamma_bare = (2*N_c + 1)**2 / N_c
delta_gamma_required = mp.mpf("16.339") - gamma_bare
print(mp.nstr(gamma_bare, 80))
print(mp.nstr(delta_gamma_required, 80))
```

Expected classification:

```text
gamma_bare(3) = 49/3 [arithmetic]
Delta_gamma_required = 17/3000 [D]
No evidence promotion.
```

---

## 9. Acceptance Status

`HISTORICAL PATH RETAINED / PHASE-8 ERRATUM APPLIED`

The file remains useful as a history of the algebraic search, but it is not a proof and must not be cited as a current [A] or [B] evidence source for `gamma = 16.339`.
