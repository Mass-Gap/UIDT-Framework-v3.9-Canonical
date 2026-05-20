# S4-P1: Torsion-Threshold Onset in the YM+Scalar FRG System

> **Original date:** 2026-04-29  
> **Cleanup erratum:** 2026-05-20  
> **Original branch:** `TKT-20260429-S4P1-tachyon-threshold-frg`  
> **Status:** Research note with erratum. Evidence [D]. No evidence-category promotion.

---

## 0. Cleanup Erratum — 2026-05-20

This file is retained as a historical S4-P1 onset analysis. It must be read through the Phase-8 cleanup policy.

Mandatory corrections:

1. Replace the ambiguous legacy symbol `k_crit` with `k_T` when referring to the S4-P1 torsion-threshold scale.
2. Use the corrected canonical value:

```text
k_T = 4*pi*E_T = 30.661944299036382... MeV
```

for `E_T = 2.44 MeV` [C].

3. The historical `30.707 MeV` and `30.790 MeV` values remain historical numerical-context values only. They are not exact consequences of `E_T = 2.44 MeV`.
4. Regulator independence is not proven. It remains a required test.
5. No upgrade to [C] is made by this note.

---

## 1. Research Goal

The original S4-P1 goal was to test whether the torsion-threshold scale in the coupled YM+Scalar FRG system can be approximated by:

```text
k_T = E_T * (N_c^2 - 1) * pi/2
```

For `N_c = 3`, this becomes:

```text
k_T = 4*pi*E_T
```

The corrected question is not whether this is already exact, but whether it can be derived from the Wetterich trace and shown to be regulator-independent.

---

## 2. Setup

| Quantity | Value | Evidence |
|---|---:|---|
| `Delta*` | `1710 MeV` | [A] |
| `E_T` | `2.44 MeV` | [C] |
| `v` | `47.7 MeV` | [A] |
| `kappa` | `1/2` | [A] |
| `lambda_S` | `5/12` | [A] |

The exact RG relation gives:

```text
sqrt(2*kappa/lambda_S) = sqrt(12/5)
```

---

## 3. Corrected S4-P1 Chain

Using canonical `E_T = 2.44 MeV`:

```text
k_T = 4*pi*E_T
    = 30.6619442990363820073953994208079481497643733379010328127154592209242881253534 MeV
```

Then:

```text
v_S4P1 = sqrt(12/5) * k_T
        = 47.501279853002942... MeV
```

and:

```text
Delta_gamma_NP = (N_c^2 - 1)/(4*pi^2) * v_S4P1/Delta*
               = 0.005629106314891450...
```

Therefore:

```text
gamma_pred = 49/3 + Delta_gamma_NP
           = 16.338962439648224...
```

Residual:

```text
|gamma_pred - 16.339| = 3.7560e-5
```

Status: partial numerical hit [D], not [A].

---

## 4. Wetterich-Trace Context

The relevant formal object is:

```text
partial_t Gamma_k = 1/2 Tr[(Gamma_k^(2) + R_k)^(-1) partial_t R_k]
```

The original note explored whether threshold factors in a Litim-type regulator could generate the `4*pi` structure. This remains a conjectural interpretation.

The LO approximation with constant `alpha_s` is insufficient. The deep-IR threshold is non-perturbative and cannot be closed by a one-loop constant-coupling analysis.

---

## 5. Regulator-Independence Status

Earlier text described regulator independence as confirmed. Under the current evidence rules this is too strong.

Correct status:

```text
Regulator independence: OPEN
Evidence: [D]
Required: explicit multi-regulator comparison with residual table
```

Required regulators:

| Regulator | Required output |
|---|---|
| Litim | baseline threshold and residual |
| smooth exponential | threshold and residual |
| sharp cutoff | threshold and residual |
| Polchinski-type | threshold and residual |

No [C] upgrade is possible before this is done and externally reviewed.

---

## 6. Relation to D2 Gamma-Emergent Scale

Do not conflate:

| Symbol | Scale | Meaning |
|---|---:|---|
| `k_T` | `30.661944... MeV` | S4-P1 torsion threshold `4*pi*E_T`. |
| `k_gamma` | `~104.66 MeV` | D2 gamma-emergent inverse scale near `Delta*/gamma`. |

Both are [D] research quantities. Neither derives `gamma = 16.339` [A-].

---

## 7. Claims Table

| ID | Claim | Evidence | Status |
|---|---|---|---|
| C-S4P1-01 | A torsion-threshold scale `k_T = 4*pi*E_T` is numerically suggestive for S4-P1. | [D] | open |
| C-S4P1-02 | Corrected `k_T` for `E_T=2.44 MeV` is `30.6619442990... MeV`. | [D] | arithmetic chain, no promotion |
| C-S4P1-03 | The corrected S4-P1 gamma chain gives `gamma_pred=16.338962439648224...`. | [D] | partial hit |
| C-S4P1-04 | Regulator independence is established. | not supported | open |
| C-S4P1-05 | S4-P1 derives `gamma=16.339`. | not supported | false |

---

## 8. Required Next Steps

1. Re-run S4-P1 using corrected `k_T` nomenclature.
2. Perform multi-regulator threshold comparison.
3. Quantify NLO and nonlinear flow corrections.
4. Keep S4-P1 at [D] unless the regulator and derivation gates pass.

---

## 9. Reproduction Snippet

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

## Acceptance Status

`S4-P1 RETAINED AS [D] RESEARCH VECTOR / NO CANONICAL PROMOTION`

This file does not close L4 and does not authorize a claim upgrade.
