# UIDT v3.9 — Phase 8 P1/P5 Research Note

> **Ticket:** TKT-2026-05-17-phase8-p1-p5-research  
> **Date:** 2026-05-17  
> **DOI:** 10.5281/zenodo.17835200  
> **Status:** Research note; no canonical evidence-category promotion.  
> **Dependency:** PR #459 assumptions: corrected `gamma_bare(Nc)=(2Nc+1)^2/Nc`, corrected `k_crit=4πE_T` for `E_T=2.44 MeV`.

---

## Kurzstatus

Phase 8 can be executed before PR #459 is merged only if the research branch is based on the PR #459 head. This note follows that condition.

The work here executes two bounded tasks:

1. **P1:** quantify the minimal positive correction envelope required for `gamma_bare = 49/3` to reach `gamma = 16.339 [A-]`.
2. **P5:** establish the corrected SU(4) falsification target for the bare-gamma ansatz.

No claim is promoted to [A], [B], or [C].

---

## Stratum I — External / empirical anchor

| Quantity / source | Value / scope | Evidence role | Status |
|---|---:|---|---|
| Athenodorou & Teper, JHEP 12 (2021) 082 | SU(N), N≤12, 3+1D glueball spectrum, string tensions, topology | external lattice anchor for SU(N) context | verified DOI |
| DOI | `10.1007/JHEP12(2021)082` | reference check | resolved |
| arXiv | `2106.00364` | preprint identifier | resolved |

The paper is used only as a lattice-context anchor for SU(N) availability. It does not provide a UIDT gamma observable and therefore cannot validate `gamma_bare(SU4)=20.25` as [B].

---

## Stratum II — Standard theory context

- Pure Yang-Mills SU(N) lattice spectra can be compared across several N values when observables are dimensionless, e.g. ratios to string tension.
- A UIDT-specific `gamma_bare(Nc)` observable is not part of standard lattice Yang-Mills terminology.
- Therefore a SU(4) test must first define a lattice-extractable UIDT observable before any [B] comparison is possible.

---

## Stratum III — UIDT research claims

### P1 — Δγ envelope audit

Corrected Session-2 premise:

```text
gamma_bare(Nc) = (2Nc + 1)^2 / Nc
gamma_bare(3) = 49/3
```

Canonical calibrated target:

```text
gamma = 16.339 [A-]
```

Required correction:

```text
Delta_gamma_required = gamma - 49/3 = 17/3000 = 0.005666666666...
```

Two one-loop scale templates were evaluated as envelopes only:

```text
C_A template:        Nc*kappa^2/(16*pi^2)              = 0.00474943048323458...
adjoint-dof template:(Nc^2-1)*kappa^2/(16*pi^2)        = 0.0126651479552922...
```

The required dimensionless threshold coefficients are:

```text
F_C_A       = 1.19312550982058...
F_adjoint   = 0.447422066182718...
```

Interpretation:

- Both coefficients are positive and O(1).
- This is a **necessary viability condition**, not a derivation.
- P1 is therefore **PARTIAL-PASS [D]**, not [A], [B], or [C].

### P1 relation to corrected S4-P1 chain

With PR #459 assumptions:

```text
E_T          = 2.44 MeV [C]
k_crit       = 4*pi*E_T = 30.661944299036382... MeV
v_S4P1       = sqrt(12/5)*k_crit = 47.50127985300294... MeV
Delta_gamma_NP = (Nc^2-1)/(4*pi^2)*v_S4P1/Delta* = 0.00562910631489145...
gamma_pred   = 16.338962439648224...
```

The ratio to the required correction is:

```text
Delta_gamma_NP / Delta_gamma_required = 1.00667252485103...
```

The residual to the calibrated value is:

```text
|gamma_pred - gamma| = 0.0000375603517752...
```

Interpretation:

- The corrected S4-P1 chain is numerically close.
- The residual is much larger than `1e-14`, so it cannot be classified as [A].
- The result remains **[D] Stratum III**.

---

## P5 — SU(4) falsification target

Corrected formula:

```text
gamma_bare(Nc) = (2Nc + 1)^2 / Nc
```

Then:

```text
gamma_bare(SU3) = 49/3 = 16.333333...
gamma_bare(SU4) = 81/4 = 20.25
N_SU3 = 3^2 * 11 = 99
N_SU4 = 4^2 * 11 = 176
```

Incorrect denominator rejected:

```text
wrong(SU3) = (2*3+1)^2/3^2 = 49/9
wrong(SU4) = (2*4+1)^2/4^2 = 81/16
```

Interpretation:

- SU(4) target is now mathematically clear: `gamma_bare(SU4)=20.25`.
- This is not yet a lattice test, because no UIDT gamma observable has been defined for extraction from SU(4) lattice data.
- P5 status: **falsification-ready [D]**, not [B].

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|---|
| PH8-P1-001 | Required correction from corrected gamma_bare | `Delta_gamma_required=17/3000` | [D] | III | `verify_phase8_delta_gamma_1loop_envelope.py` | partial-pass | Fails if first-principles correction is negative or >0.012. |
| PH8-P1-002 | O(1) one-loop envelope viability | `F_C_A=1.193...`, `F_adj=0.447...` | [D] | III | `verify_phase8_delta_gamma_1loop_envelope.py` | partial-pass | Fails if exact calculation requires non-O(1) coefficient or wrong sign. |
| PH8-P1-003 | Corrected S4-P1 gamma chain remains near target | `gamma_pred=16.338962439648...` | [D] | III | `verify_phase8_delta_gamma_1loop_envelope.py` | partial-pass | Fails under regulator-independence or full Wetterich flow mismatch. |
| PH8-P5-001 | SU(4) target from corrected formula | `gamma_bare(SU4)=81/4=20.25` | [D] | III | `verify_phase8_su4_crosscheck.py` | falsification-ready | Fails if defined SU(4) observable does not scale according to `(2Nc+1)^2/Nc`. |
| PH8-P5-002 | N_SU4 algebraic target | `N_SU4=176` | [D] | III | `verify_phase8_su4_crosscheck.py` | falsification-ready | Fails if N-scaling is not supported by lattice-extractable structure. |

---

## Reproduction Note

Single commands:

```bash
python verification/scripts/verify_phase8_delta_gamma_1loop_envelope.py
python verification/scripts/verify_phase8_su4_crosscheck.py
```

Expected:

```text
ALL PHASE-8 P1 ENVELOPE CHECKS PASSED
ALL PHASE-8 P5 SU(4) CROSS-CHECKS PASSED
```

---

## Verified References

| DOI/arXiv/PR | Status | Used for | Evidence Tag |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | project DOI | UIDT project identity | n/a |
| PR #459 | draft PR | corrected Phase-8 assumptions | [D] context |
| DOI `10.1007/JHEP12(2021)082` | resolved | SU(N) lattice context | Stratum I reference |
| arXiv `2106.00364` | resolved | SU(N) lattice context | Stratum I reference |

No new UIDT claim is promoted using the external SU(N) lattice paper.

---

## Limitations

- P1 is an envelope audit, not a Feynman-rule calculation.
- P5 defines a SU(4) target, not a completed SU(4) lattice comparison.
- No `CLAIMS.json` modification is performed here.
- No core or module numerical behavior is changed.
- `gamma=16.339` remains [A-].
- `gamma_bare=49/3` remains [D].
- `gamma_pred=16.338962...` remains [D].

---

## Next step

Phase 8.3 should implement regulator-dependence tests for S4-P1 using the corrected threshold scale:

```text
k_crit = 4*pi*E_T = 30.661944299036382... MeV
```

The historical value `30.707 MeV` must not be used as exact unless `E_T` is explicitly changed to approximately `2.443585 MeV`.
