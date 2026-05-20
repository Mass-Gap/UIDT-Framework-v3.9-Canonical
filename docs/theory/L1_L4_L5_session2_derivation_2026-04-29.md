# L1/L4/L5 — Session 2: First-Principles Derivation Results

> **Original date:** 2026-04-29  
> **Cleanup erratum:** 2026-05-20  
> **Branch:** TKT-20260429-L1-L4-L5-first-principles-session2  
> **Precision policy:** native `mpmath`, active local `mp.dps = 80`, no `float()`, no `round()`  
> **Status:** Research note with erratum. No canonical evidence promotion.

---

## 0. Cleanup Erratum — 2026-05-20

This document is retained as the Session-2 research source, but the following corrections are mandatory for all later use:

1. **Bare-gamma formula:**

```text
gamma_bare(N_c) = (2*N_c + 1)^2 / N_c
```

At `N_c = 3`, this gives `49/3`. The expression with denominator `N_c^2` gives `49/9` and is rejected for the Session-2 conjecture.

2. **Evidence status:**

The arithmetic identity at fixed `N_c=3` is exact, but the physical UIDT identification `gamma_bare = 49/3` remains [D], Stratum III. It is not an [A] derivation of `gamma = 16.339` [A-].

3. **Torsion-threshold notation:**

The legacy symbol `k_crit` is ambiguous. Use:

| Symbol | Meaning |
|---|---|
| `k_T` | S4-P1 torsion-threshold scale `4*pi*E_T = 30.6619442990... MeV` for `E_T = 2.44 MeV` [C]. |
| `k_gamma` | D2 gamma-emergent scale near `Delta*/gamma ≈ 104.66 MeV` [D]. |
| `k_crit` | Deprecated unless context is explicitly stated. |

The historical `30.707 MeV` value is not exact for `E_T = 2.44 MeV`; it implies an effective `E_T ≈ 2.443585 MeV`.

4. **mpmath import discipline:**

Use `from mpmath import mp` followed by local `mp.dps = 80`, or explicitly set `mp.mp.dps = 80` when importing the module. Do not rely on `import mpmath as mp; mp.dps = 80`.

---

## Stratum Separation

### Stratum I — Empirical / Canonical Inputs

- `Delta* = 1.710 ± 0.015 GeV` [A]
- `gamma = 16.339` [A-]
- `gamma_infinity = 16.3437` [A-]
- `delta_gamma = 0.0047` [A-]
- `v = 47.7 MeV` [A]
- `E_T = 2.44 MeV` [C]
- `kappa = 0.500` [A]
- `lambda_S = 5*kappa^2/3 = 5/12` [A]

### Stratum II — External Physics Context

- `alpha_s(Delta*) ≈ 0.3` [B-context]
- SVZ gluon condensate scale around the sub-GeV regime [B-context]
- SU(3): `C_F = 4/3`, `C_A = 3`, `b_0 = 11`, `d_A = 8`

### Stratum III — UIDT Theoretical Extension

All L1/L4/L5 results below are [D] unless explicitly stated otherwise. They are research candidates, not ledger promotions.

---

## RG-Constraint Verification

```text
5*kappa^2 = 1.25000000000000000000...
3*lambda_S = 1.25000000000000000000...
Residual = 0.0
```

Evidence: [A], conditional on `lambda_S = 5*kappa^2/3` and residual `< 1e-14`.

---

## L1 — gamma_bare from SU(3) Casimir-Combinatorics

### Core Result

A systematic scan over combinations of `{N_c, C_F, C_A, d_A, b_0}` identified the Session-2 candidate:

```text
gamma_bare(N_c) = (2*N_c + 1)^2 / N_c
gamma_bare(3)  = 49/3 = 16.333333...
```

### Interpretation

```text
gamma_phys = gamma_bare + Delta_gamma_correction + O(g^4)
```

with the required correction:

```text
Delta_gamma_required = gamma - 49/3 = 17/3000 = 0.005666666...
```

Status: [D], Stratum III. The correction has not been derived from a first-principles self-energy or regulator-independent FRG calculation.

### Next Required Step

Compute the scalar self-energy `Pi_S(p^2)` at `p = Delta*` and extract the sign/magnitude of the correction. Fail-fast criteria:

| Result | Consequence |
|---|---|
| `Delta_gamma < 0` | reject the L1 bare-gamma ansatz |
| `Delta_gamma > 0.012` | reject the L1 bare-gamma ansatz |
| `0 < Delta_gamma <= 0.012` | retain at [D]/[D*], no promotion |
| explicit derivation with residual `< 1e-14` | only then discuss [A]-level promotion |

---

## L4 — D2 Vector: gamma as a Scale Ratio

The D2 line explored a gamma-emergent scale near:

```text
k_gamma ≈ Delta*/gamma ≈ 104.66 MeV
```

This is distinct from the S4-P1 torsion-threshold scale:

```text
k_T = 4*pi*E_T = 30.6619442990... MeV
```

The two scales must not be conflated.

### Session-2 D2 Observation

The inverse problem indicated a tachyonic UV mass scale in the sub-GeV regime. This is a [D] observation and not a prediction. The perturbative FRG flow was not closed at the required accuracy.

### Limitation

The 1-loop FRG scheme is not sufficient to derive `gamma = 16.339` [A-]. A full regulator-independent flow or a controlled BMW/Dyson-resummed calculation would be required.

---

## L5 — Torsion Term Sigma_T from E_T Coupling

The torsion-kill-switch condition remains:

```text
E_T = 0  =>  Sigma_T = 0
```

For canonical `E_T = 2.44 MeV` [C], the kill-switch is not triggered. A dimensional ansatz gives a sub-keV scale, but this is not a geometric derivation.

Status: [D].

---

## Consolidated Session-2 Balance

| Limitation | Session-2 result | Evidence | Current status |
|---|---|---|---|
| L1 | `gamma_bare = 49/3`; required correction `17/3000` | [D] | open |
| L4 | D2 scale-ratio path near `k_gamma` | [D] | perturbatively insufficient |
| L5 | torsion self-energy ansatz | [D] | dimensional only |
| RG | `5*kappa^2 = 3*lambda_S` | [A] | closed |

---

## Reproduction Snippet

```python
from mpmath import mp
mp.dps = 80
N_c = mp.mpf(3)
gamma = mp.mpf("16.339")
gamma_bare = (2*N_c + 1)**2 / N_c
delta_gamma_required = gamma - gamma_bare
print(mp.nstr(gamma_bare, 80))
print(mp.nstr(delta_gamma_required, 80))
```

Expected classification:

```text
gamma_bare = 49/3 exactly at N_c=3 [arithmetic]
Delta_gamma_required = 17/3000 within residual-gate tolerance [D]
No evidence promotion.
```

---

## Mandatory Limitations

1. L1 is not solved: `gamma_bare = 49/3` lacks a first-principles correction to `gamma = 16.339` [A-].
2. L4 is not solved: the D2/FRG line is perturbatively insufficient.
3. L5 is not solved: the torsion self-energy remains ansatz-level.
4. Stratum III statements remain UIDT-internal until externally validated.

---

*Maintainer: P. Rietz | UIDT Framework v3.9 | DOI: 10.5281/zenodo.17835200*
