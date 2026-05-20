# L5 Audit: N=99, N=94.05, and SU(4) N-Definition Tension

> **UIDT Framework:** v3.9 Canonical  
> **Cleanup date:** 2026-05-20  
> **Status:** L5 limitation stub with Phase-8 tension update. No evidence-category promotion.

---

## 1. Current L5 Status

L5 remains open. No first-principles derivation of `N = 99` exists in the current canonical state.

| Candidate | Status | Evidence |
|---|---|---|
| `N = 99` | used in production / canonical family | [D] |
| `N = 94.05` | legacy or PR-87 candidate, not implemented | [E]/legacy |
| SU(4) `N = 176` | fixed-`b0=11` extrapolation | [D]/convention |
| SU(4) `N = 704/3` | pure-YM `b0(N_c)=11N_c/3` extrapolation | Stratum II tension context |

---

## 2. Existing Tension: N=99 vs N=94.05

Original tension:

```text
N = 99     : used in production / canonical family
N = 94.05  : suggested by legacy PR path, not implemented
```

Resolution status: unresolved.

Required action:

1. Identify every code/document path using `N=99`.
2. Identify every code/document path using or implying `N=94.05`.
3. Compare observables under both definitions.
4. Keep cosmology claims capped at [C].
5. Do not promote either value to [A] without derivation and ledger review.

---

## 3. New Phase-8 Tension: SU(4) N Definition

The Phase-8 SU(4) cross-check introduces a separate definition tension.

### Fixed-b0 convention

If one keeps the SU(3)-style factor `b0 = 11` fixed, then:

```text
N_SU4 = N_c^2 * 11 = 16 * 11 = 176
```

### Pure-YM beta coefficient convention

In standard pure Yang-Mills:

```text
b0(N_c) = 11*N_c/3
```

For SU(4):

```text
b0(4) = 44/3
N_SU4 = 16 * 44/3 = 704/3 = 234.666666...
```

Relative difference:

```text
(704/3 - 176)/176 = 1/3
```

This is a 33.333...% convention-level discrepancy.

---

## 4. Consequence for L5

`N=99` can be motivated in SU(3) by:

```text
N = N_c^2 * b0 = 9 * 11 = 99
```

However, this identity is ambiguous under SU(N) generalization:

| Rule | SU(3) | SU(4) | Comment |
|---|---:|---:|---|
| fixed `b0 = 11` | 99 | 176 | UIDT-internal convention candidate |
| pure-YM `b0(N_c)=11N_c/3` | 99 | 704/3 | standard Stratum II scaling |

Both agree at SU(3) and diverge at SU(4). Therefore SU(3) alone cannot decide the rule.

---

## 5. Required Resolution Plan

| Step | Task | Output |
|---:|---|---|
| 1 | Decide whether UIDT `N` uses fixed SU(3)-quenched `b0=11` or standard pure-YM `b0(N_c)=11N_c/3`. | short theory note |
| 2 | Test SU(4) consequences under both definitions. | numerical comparison table |
| 3 | Extract SU(4) lattice observables from primary SU(N) references. | DOI/arXiv-backed table |
| 4 | Decide whether `N=99` remains SU(3)-specific or generalizes. | evidence-tagged claim proposal |
| 5 | Only after review, update `LEDGER/CLAIMS.json` if warranted. | Guardian-gated PR |

---

## 6. Evidence Status

| Statement | Evidence | Status |
|---|---|---|
| `N=99` is used in the canonical SU(3) family. | [D] | retained |
| `N=94.05` is a legacy unresolved candidate. | [E] | unresolved |
| fixed-b0 SU(4) gives `176`. | [D]/convention | unresolved |
| pure-YM SU(4) gives `704/3`. | Stratum II context | tension source |
| L5 is solved. | not supported | false |

---

## 7. Acceptance Status

`L5 OPEN / SU4 N-DEFINITION TENSION ACTIVE`

No evidence-category promotion is justified. The next L5 task is to resolve the definition of `N` under SU(N) generalization before using SU(4) as a falsification or validation channel.
