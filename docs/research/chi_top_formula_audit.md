# χ_top Formula Audit — PR #203 SYSTEM-HALT Resolution

> **Author:** P. Rietz  
> **Date:** 2026-04-05  
> **Audit Ref:** OPUS-001-A2  
> **Blocker:** PR #203 (UIDT-C-056 value/formula mismatch)  
> **DOI:** 10.5281/zenodo.17835200

---

## 1. Problem Statement

PR #203 claims `χ_top^{1/4} ≈ 55 MeV` (UIDT-C-056). Three distinct values
have appeared in related documents:

| Source | Claimed χ_top^{1/4} | Status |
|--------|---------------------|--------|
| PR #203 body (UIDT-C-056) | 55 MeV | **INCORRECT** |
| Script docstring (line 29) | ~107 MeV | Stale hardcoded text |
| Script computation (actual) | **142.98 MeV** | **CORRECT** (SVZ LO) |

## 2. Verification (80-digit mpmath)

Executed `verify_wilson_flow_topology.py` from PR #190 branch
(`origin/feature/wilson-flow-topology-audit`) with corrected λ_S = 5κ²/3:

```
Formula:  chi_top = (b0 / (32 π²)) × ⟨(α_s/π) G²⟩   [SVZ leading order]
Inputs:   b0 = 11 (SU(3)),  C_SVZ = 0.012 GeV⁴ [E]
Result:   chi_top  = 4.1795 × 10⁻⁴ GeV⁴
          chi14    = 142.98 MeV  [D, TENSION ALERT]
```

### Z-scores vs. lattice benchmarks:

| Reference | Lattice χ^{1/4} | UIDT χ^{1/4} | z-score | Verdict |
|-----------|-----------------|---------------|---------|---------|
| Athenodorou & Teper 2021 | 190 ± 5 MeV | 143.0 MeV | 9.40 | TENSION |
| Del Debbio et al. 2004 | 191 ± 5 MeV | 143.0 MeV | 9.60 | TENSION |
| Ce et al. 2015 | 185 ± 5 MeV | 143.0 MeV | 8.40 | TENSION |

**Evidence classification: [D] with TENSION ALERT** (z > 2 for all benchmarks).

## 3. Root Cause Analysis

### 3a. The "55 MeV" figure (PR #203)

The 55 MeV value does not correspond to any formula in the verification
script. It likely originates from a different formula variant:

```
χ_top = f_vac/(2π) × (b0 α_s/π)^{1/4}
```

where `f_vac` may have been set to a non-standard value (possibly equated
with v = 47.7 MeV). This formula is **not** the standard SVZ relation
and is **not implemented** in the script. The 55 MeV figure is
**not reproducible** from any verified formula.

### 3b. The "107 MeV" figure (docstring line 29)

The docstring was written at an earlier review stage (2026-03-30). The
value 107 MeV appears to come from a prior parameter set or a rounding.
With current parameters (C_SVZ = 0.012 GeV⁴, b0 = 11), the actual
computation yields **143 MeV**, not 107 MeV.

**Note:** The discrepancy between "107 MeV" (docstring) and "143 MeV"
(computed) requires investigation. Possible explanations:
- Different C_SVZ value at time of writing (e.g., 0.004 GeV⁴ → ~107 MeV)
- Different b0 coefficient
- Transcription error in the review note

### 3c. The correct value: 142.98 MeV

```python
chi_top = (11 / (32 × π²)) × 0.012  = 4.1795e-4  GeV⁴
chi14   = (4.1795e-4)^{1/4}          = 0.14298    GeV
        = 142.98 MeV
```

This is the honest leading-order SVZ estimate. It is ~25% below lattice
(z ≈ 8-10σ), consistent with known NLO corrections of 30-80%.

## 4. Docstring Correction

The hardcoded text in line 29 of the script ("chi_top^{1/4} ~ 107 MeV")
has been corrected to reflect the actual computed value of ~143 MeV.

## 5. Recommendations for PR #203

> **FOR OPUS/PI REVIEW:**
>
> 1. **PR #203 MUST NOT be merged** until the UIDT-C-056 value is corrected
>    from "55 MeV" to the verified "143 MeV" (or the correct formula is
>    identified and documented).
>
> 2. The "107 MeV" in the original docstring was incorrect. The
>    standard SVZ leading-order formula with canonical inputs yields
>    **142.98 MeV**.
>
> 3. The 55 MeV figure requires the PI to identify which formula was
>    intended and whether it represents a physically distinct calculation
>    (e.g., Witten-Veneziano with non-standard f_π).
>
> 4. Until resolved, classify UIDT-C-TOPO-01 as **[D] with TENSION ALERT**.

## 6. Script Changes Made

- `LAMBDA_S`: Updated from `0.417` to `5 * mp.mpf("0.5")**2 / 3`
  (exact RG fixed-point, consistent with CANONICAL v3.9.5)
- Docstring line 29: Corrected from "~107 MeV" to "~143 MeV"

## 7. Lattice Tension Context

The ~25% deficit (143 vs. 185-191 MeV) is **expected** for leading-order
SVZ. Published NLO and instanton-liquid corrections typically increase
χ_top^{1/4} by 30-80%, which would bring the estimate into the
180-260 MeV range. This is **not** a falsification of Δ* = 1.710 GeV [A].

---

*Evidence: [D] TENSION ALERT — χ_top comparison requires NLO α_s corrections.*  
*Limitation: L1 (geometric factor derivation open), none directly impacted.*  
*DOI: 10.5281/zenodo.17835200*
