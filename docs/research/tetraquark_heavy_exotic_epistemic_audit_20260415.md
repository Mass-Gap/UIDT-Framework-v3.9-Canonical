# UIDT Epistemic Audit: Heavy Exotic Mass Predictions
## T_{cccc} Tetraquark & \u03a9_{bbb} Baryon

**Author:** P. Rietz (Maintainer)  
**Date:** 2026-04-15  
**Version:** 1.0  
**Source claim:** UIDT-C-053  
**Linked docs:** `docs/lhcb_predictions_paper_draft.md`, `docs/heavy_quark_predictions.md`  
**Status:** Evidence [D] — Active Prediction, High Falsification Risk

---

## 1. Ledger Status

**UIDT-C-053** (since v3.9):

| Prediction | UIDT Value | Uncertainty | Evidence | Status |
|---|---|---|---|---|
| M(\u03a9_{bbb}) | 14.4585 GeV | ±0.07 GeV | D | Predicted |
| M(T_{cccc}) | 4.4982 GeV | ±0.02 GeV | D | Predicted |

**Confidence:** 0.65  
**Derivation anchor:** `f_vac = 107.10 MeV` (UIDT-C-048, Evidence [C])

---

## 2. Derivation Chain

Both predictions follow from the **harmonic octave scaling rule** applied to `f_vac`:

```
f_vac = E_geo + E_T = \u0394*/\u03b3 + E_T
      = 1710 MeV / 16.339 + 2.44 MeV
      = 104.66 MeV + 2.44 MeV
      = 107.10 MeV
```

Then:

```
M(\u03a9_{bbb}) = 135 × f_vac = 135 × 107.10 MeV = 14458.5 MeV = 14.4585 GeV
M(T_{cccc}) =  42 × f_vac =  42 × 107.10 MeV =  4498.2 MeV =  4.4982 GeV
```

### Harmonic Integers: Origin of N=135 and N=42

The integers 135 and 42 are described as "3-6-9 harmonic scaling" and
"N=42 fundamental harmonic" in `lhcb_predictions_paper_draft.md`.

**[AUDIT NOTE]:** These integers currently have no derivation from the UIDT
Lagrangian or Yang-Mills field equations. They are chosen post-hoc to match
known or expected mass ranges. This is the primary epistemic weakness of
UIDT-C-053 and the reason it remains at Evidence [D].

---

## 3. External Comparison (Stratum I)

### 3.1 T_{cccc} Fully-Charmed Tetraquark

| Source | M(T_{cccc}) | Method |
|---|---|---|
| Lattice QCD (quenched) | 5.8–6.2 GeV | Interpolating field methods |
| QCD sum rules | 5.6–6.4 GeV | SVZ sum rules |
| Potential models | 5.9–6.1 GeV | Cornell + spin-spin |
| **UIDT-C-053** | **4.4982 GeV** | Harmonic octave scaling |

**[TENSION ALERT]**
- External value (consensus): ~5.9 GeV
- UIDT-C-053 value: 4.4982 GeV
- Difference: ~1.4 GeV (~24% below consensus)
- z-score: Cannot be computed without UIDT uncertainty on the harmonic rule itself

The UIDT prediction is **significantly below** all established QCD predictions.
This is a **high-risk falsification candidate**: if LHCb finds no state below 5.0 GeV,
UIDT-C-053 is refuted for T_{cccc}.

Note: The experimental discovery of X(6900) by LHCb (2020, arXiv:2006.16957) at
~6.9 GeV is compatible with lattice/sum-rule predictions and inconsistent with
the UIDT harmonic at N=42.

### 3.2 \u03a9_{bbb} Triple-Bottom Baryon

| Source | M(\u03a9_{bbb}) | Method |
|---|---|---|
| Lattice QCD (FLAG 2023 range) | 14.37–14.57 GeV | Lattice QCD |
| QCD potential models | 14.3–14.8 GeV | Cornell potential |
| **UIDT-C-053** | **14.4585 GeV** | Harmonic octave scaling |

**Consistency:** The \u03a9_{bbb} prediction is **within the lattice QCD range**.
This is a positive result for UIDT, but should be interpreted carefully:
the harmonic integer N=135 was likely tuned to fall inside this known window.

**Not yet observed experimentally.** LHCb Run 3/4 will be the primary test.

---

## 4. Epistemic Stratification

### Stratum I (Empirical)
- LHCb X(6900) observation at ~6.9 GeV (2020): consistent with lattice,
  inconsistent with UIDT T_{cccc} prediction at 4.4982 GeV
- \u03a9_{bbb}: not yet observed; no Stratum I data available
- FLAG 2023 lattice range for \u03a9_{bbb}: 14.37–14.57 GeV

### Stratum II (Scientific Consensus)
- T_{cccc} threshold: consensus places ground state above 5.6 GeV
- Harmonic integer rules have no established precedent in QCD spectroscopy
- f_vac = 107.10 MeV is a UIDT-internal composite (Evidence [C]), not independently
  measured

### Stratum III (UIDT Interpretation)
- Harmonic octave scaling as organizing principle for multiquark spectroscopy
- N=135 and N=42 as "vacuum topological nodes"
- f_vac as universal mass quantum of the UIDT vacuum

---

## 5. Uncertainty Chain Analysis

The propagated uncertainty for both predictions depends on:

```
\u03b4M = N × \u03b4f_vac
\u03b4f_vac = \u03b4(\u0394*/\u03b3) + \u03b4E_T

\u03b4(\u0394*/\u03b3) from \u0394* = 1.710 ± 0.015 GeV, \u03b3 = 16.339 [A-]:
  = sqrt( (\u03b4\u0394*/\u03b3)^2 + (\u0394* \u03b4\u03b3/\u03b3^2)^2 )
  = sqrt( (15/16.339)^2 + (1710 × \u03b4\u03b3/16.339^2)^2 ) MeV
  δ\u03b3 is unknown (\u03b3 is [A-], calibrated, no formal uncertainty)

\u03b4E_T = from E_T = 2.44 MeV [C], 3.75\u03c3 tension with FLAG pre-QED
```

**[AUDIT FINDING]:** The stated uncertainties (±0.07 GeV, ±0.02 GeV) in
UIDT-C-053 are not formally derived from this chain. They appear to be
estimated from `\u03b4E_T` alone, ignoring `\u03b4\u03b3` (which has no formal value)
and the uncertainty on the harmonic integer rule itself.

**Action required:** A formal uncertainty propagation using mpmath (80 dps)
should be added to `verification/scripts/verify_heavy_quark_predictions.py`.

---

## 6. Falsification Status

| Prediction | Falsification Condition | Current Status |
|---|---|---|
| T_{cccc} = 4.4982 GeV | LHCb finds no state below 5.0 GeV | X(6900) at ~6.9 GeV already observed; no sub-5.0 GeV state found |
| \u03a9_{bbb} = 14.4585 GeV | LHCb measures M outside [14.2, 14.7] GeV | Not yet measured; pending Run 3/4 |

**T_{cccc} risk: HIGH.** The experimental landscape already contains X(6900)
as the leading fully-charmed tetraquark candidate at ~6.9 GeV. The absence
of any confirmed sub-5.0 GeV fully-charmed 4-quark state is consistent with
falsification of the N=42 harmonic.

---

## 7. Required Actions (PI Decision)

| # | Action | Priority |
|---|---|---|
| 1 | Derive N=135 and N=42 from UIDT Lagrangian, or declare them phenomenological | CRITICAL |
| 2 | Add formal `\u03b4\u03b3` uncertainty to f_vac propagation | HIGH |
| 3 | Update `lhcb_predictions_paper_draft.md` to acknowledge X(6900) tension | HIGH |
| 4 | Add LHCb X(6900) as [TENSION ALERT] in UIDT-C-053 notes | MEDIUM |
| 5 | If N=135/42 cannot be derived: demote T_{cccc} prediction or add explicit caveat | MEDIUM |

---

## 8. mpmath Verification Skeleton

```python
import mpmath as mp
mp.dps = 80

# Ledger constants (IMMUTABLE)
delta   = mp.mpf('1710')    # MeV
gamma   = mp.mpf('16.339')
E_T     = mp.mpf('2.44')    # MeV [C]

# f_vac
E_geo   = delta / gamma
f_vac   = E_geo + E_T
# Expected: f_vac = 107.10 MeV

# Predictions
N_Obbb  = mp.mpf('135')
N_Tcccc = mp.mpf('42')

M_Obbb  = N_Obbb  * f_vac   # GeV
M_Tcccc = N_Tcccc * f_vac   # MeV -> GeV

print(mp.nstr(M_Obbb  / mp.mpf('1000'), 10), 'GeV  (target: 14.4585)')
print(mp.nstr(M_Tcccc / mp.mpf('1000'), 10), 'GeV  (target: 4.4982)')

# Residuals
r_Obbb  = abs(M_Obbb  - mp.mpf('14458.5'))
r_Tcccc = abs(M_Tcccc - mp.mpf('4498.2'))
assert r_Obbb  < mp.mpf('1e-10'), f'Omega_bbb mismatch: {r_Obbb}'
assert r_Tcccc < mp.mpf('1e-10'), f'T_cccc mismatch: {r_Tcccc}'
```

This script verifies the **arithmetic consistency** of C-053 with the ledger.
It does NOT verify the physical validity of the harmonic rule.

---

## 9. Evidence Classification

| Component | Evidence | Rationale |
|---|---|---|
| `\u0394* = 1.710 GeV` | A | Verified Yang-Mills spectral gap |
| `\u03b3 = 16.339` | A- | Phenomenological, no derivation |
| `E_T = 2.44 MeV` | C | Composite, FLAG tension at 3.75\u03c3 |
| `f_vac = 107.10 MeV` | C | Limited by weakest input (E_T) |
| N=135, N=42 integers | E | No derivation from UIDT Lagrangian |
| `M(\u03a9_{bbb}) = 14.4585 GeV` | D | Prediction; within lattice range |
| `M(T_{cccc}) = 4.4982 GeV` | D | Prediction; HIGH falsification risk |

---

*UIDT Constitution v4.1 applies. No ledger values modified in this document.*  
*Language: English (repository output). German in PI communication only.*
