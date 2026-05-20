# S4-P1: Torsion-Threshold Chain in YM+Scalar FRG

> **Original date:** 2026-04-29  
> **Cleanup erratum:** 2026-05-20  
> **Original branch:** TKT-20260429-S4P1-tachyon-threshold-frg  
> **Status:** Research note with erratum. Evidence [D]. No canonical promotion.

---

## 0. Cleanup Erratum — 2026-05-20

The original note used the legacy symbol `k_crit` for the S4-P1 torsion threshold and quoted a historical value near `30.707 MeV`. Later Phase-8 reconciliation requires the following corrections.

### Corrected symbol

Use:

```text
k_T = 4*pi*E_T
```

for the S4-P1 torsion-threshold scale.

Do not use unqualified `k_crit`, because the repository also contains a distinct D2 gamma-emergent scale near `Delta*/gamma ≈ 104.66 MeV`.

### Corrected value for canonical E_T

For canonical `E_T = 2.44 MeV` [C]:

```text
k_T = 4*pi*E_T
    = 30.6619442990363820073953994208079481497643733379010328127154592209242881253534 MeV
```

The historical value `30.707 MeV` is not exact for `E_T = 2.44 MeV`; it implies an effective `E_T ≈ 2.443585 MeV`.

### Evidence status

The S4-P1 chain remains [D]. It is a partial numerical hit, not an [A] derivation.

---

## 1. Research Question

Given the UIDT scalar-sector relation:

```text
v_S4P1 = sqrt(2*kappa/lambda_S) * k_T
```

and the exact RG relation:

```text
lambda_S = 5*kappa^2/3,  kappa = 1/2
```

one obtains:

```text
sqrt(2*kappa/lambda_S) = sqrt(12/5)
```

The research question is whether the torsion threshold:

```text
k_T = 4*pi*E_T
```

can be derived from the Wetterich trace and whether it is regulator-independent.

---

## 2. Corrected Numerical Chain

Using `E_T = 2.44 MeV` [C]:

```text
k_T = 4*pi*E_T = 30.661944299036382... MeV
```

Then:

```text
v_S4P1 = sqrt(12/5) * k_T
        = 47.501279853002942... MeV
```

With `N_c = 3` and `Delta* = 1710 MeV` [A]:

```text
Delta_gamma_NP = (N_c^2 - 1)/(4*pi^2) * v_S4P1/Delta*
               = 0.005629106314891450...
```

Therefore:

```text
gamma_pred = 49/3 + Delta_gamma_NP
           = 16.338962439648224...
```

Residual to the calibrated value `gamma = 16.339` [A-]:

```text
|gamma_pred - gamma| = 0.0000375603517752158...
```

This residual is below `1e-3` but above `1e-14`. Therefore the chain is retained as [D] but cannot be promoted to [A].

---

## 3. FRG Framework

The S4-P1 line is motivated by the Wetterich equation:

```text
partial_t Gamma_k = 1/2 STr[(Gamma_k^(2) + R_k)^(-1) partial_t R_k]
```

with Litim-type threshold structures. The original note argued that the factor `4*pi` may arise from adjoint degeneracy and threshold-integration structure.

This remains a conjectural interpretation [D]. The algebraic equality:

```text
k_T = 4*pi*E_T
```

is not yet proven from the Wetterich trace.

---

## 4. Required Regulator-Independence Tests

To move beyond [D], repeat the threshold calculation under at least:

| Regulator | Required output |
|---|---|
| Litim | baseline S4-P1 chain |
| smooth exponential | threshold shift and residual |
| sharp cutoff | threshold shift and residual |
| Polchinski-type | threshold shift and residual |

If the threshold is regulator-sensitive beyond the accepted uncertainty band, S4-P1 remains [D] or drops toward [E].

---

## 5. Relation to D2 Gamma-Scale Research

Do not conflate:

| Symbol | Scale | Meaning |
|---|---:|---|
| `k_T` | `30.661944... MeV` | S4-P1 torsion threshold `4*pi*E_T`. |
| `k_gamma` | `~104.66 MeV` | D2 gamma-emergent inverse scale near `Delta*/gamma`. |

Both are [D] research quantities. Neither derives `gamma = 16.339` [A-] from first principles.

---

## 6. Reproduction Snippet

```python
from mpmath import mp
mp.dps = 80
N_c = mp.mpf(3)
E_T = mp.mpf("2.44")
Delta_star_mev = mp.mpf("1710")
gamma_bare = mp.mpf(49) / mp.mpf(3)
k_T = 4 * mp.pi * E_T
v_S4P1 = mp.sqrt(mp.mpf(12) / mp.mpf(5)) * k_T
Delta_gamma_NP = (N_c**2 - 1) / (4 * mp.pi**2) * (v_S4P1 / Delta_star_mev)
gamma_pred = gamma_bare + Delta_gamma_NP
print(mp.nstr(k_T, 80))
print(mp.nstr(gamma_pred, 80))
```

Expected classification:

```text
k_T arithmetic chain: reproducible [D]
gamma_pred: partial numerical hit [D]
No evidence promotion.
```

---

## 7. Open Tasks

| Task | Purpose | Status |
|---|---|---|
| S4-P1a | Hard-cutoff test with `k_IR = E_T` | open |
| S4-P1b | Algebraic Wetterich-trace proof of `k_T = 4*pi*E_T` | open |
| S4-P1c | Regulator-independence check | open |
| S4-P1d | Decide whether [D] remains justified after regulator tests | open |

---

## 8. Acceptance Status

`RESEARCH ACTIVE / NO CANONICAL PROMOTION`

S4-P1 remains a structured [D] research vector. It is not a proof, not a claim promotion, and not a closure of L4.
