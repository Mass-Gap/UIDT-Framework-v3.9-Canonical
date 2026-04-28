# TKT-FRG-TACHYON — Numerical Result

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-19  
**Status:** E-open (Stratum III)  
**Script:** `verification/scripts/verify_FRG_tachyon_inversion.py`  
**Constitution:** mp.dps=80 local, no float(), RG-constraint machine zero ✓

---

## Inversion Result

The bisection over the tachyonic UV boundary κ̃₀ converged in **40 iterations**.

### Optimal UV Boundary

```
κ̃₀*  = 0.0487771846469
m²_S(Λ) = -2 λ_S Δ*² κ̃₀* = -0.1188578047 GeV²
|m_S(Λ)|                  =  344.7576 MeV
```

### IR Flow Result

```
κ̃(t_IR) achieved  = 0.103864105968
κ̃_target          = 0.103864105968   [= v²/(2 E_geo²)]
Residual |F|      = 3.33 × 10⁻¹³     [< 1e-12, converged]
```

### γ Derivation

```
γ_FRG      = Δ* / E_geo = 16.339   [= γ_canonical by construction]
γ_canonical = 16.339
Deviation   = 0  (exact match by construction — see epistemic note)
```

### Auxiliary Flow Quantities at k = E_geo

```
Z_A(t_IR) = 1.3602631    [Gluon WFR, B-compatible]
λ̃(t_IR)   = 0.35945986
g̃²(t_IR)  = 14.151494
```

---

## Bracket Scan Summary

| log₁₀(κ̃₀) | κ̃₀ | κ̃(t_IR) | F sign |
|---|---|---|---|
| −4.0 | 1.0×10⁻⁴ | 0.0 | − |
| −3.0 | 1.0×10⁻³ | 0.0 | − |
| −2.0 | 1.0×10⁻² | 0.0 | − |
| **−1.4** | **0.03981** | **0.0** | **−** |
| **−1.3** | **0.05012** | **0.4664** | **+** |
| −1.0 | 0.1 | 13.882 | + |
| 0.0 | 1.0 | 254.6 | + |

Bracket: κ̃₀ ∈ [0.039811, 0.050119] → sign change confirmed.

---

## Physical Scale Analysis [Stratum III, Evidence E]

```
|m_S(Λ)| = 344.758 MeV

Scale ratios:
  |m_S(Λ)| / E_geo  = 3.294
  |m_S(Λ)| / v      = 7.228
  |m_S(Λ)| / m_π    ≈ 2.47   (m_π = 139.57 MeV, PDG)
  |m_S(Λ)| / M_G   ≈ 0.531  (M_G = 0.65 GeV, lattice)
  |m_S(Λ)| / Δ*    ≈ 0.202  (Δ* = 1.71 GeV [A])
```

|m_S(Λ)| ≈ 345 MeV is in the hadronic regime, between m_π and M_G.
No algebraic coincidence with Standard Model parameters identified at this stage.

Confinement window preserved:
```
E_geo = 104.7 MeV  <  M_G = 650 MeV  <  Δ* = 1710 MeV  ✓
```

---

## Epistemic Status — Critical Note

**γ = 16.339 is reproduced by construction**, not by prediction.

The inversion problem is formulated as:
  *Given γ_canonical, find κ̃₀ such that the flow reproduces v at k = E_geo = Δ*/γ.*

This is a **consistency check**, not an independent derivation.

For a genuine first-principles derivation of γ, two additional steps are required:

1. **Physical motivation for m²_S(Λ)**: Show that |m_S(Λ)| = 344.758 MeV follows
   from UIDT dynamics (e.g., from the ξ_eff-coupling to Δ*, a Coleman-Weinberg
   mechanism, or a lattice-calibrated Schwinger-Dyson equation).

2. **Prediction**: Compute γ_FRG without using γ_canonical as input.
   This requires fixing m²_S(Λ) from an independent physical principle.

Until step (2) is achieved, evidence remains **E-open (Stratum III)**.

---

## L4 Status Update

| Sub-task | Status |
|---|---|---|
| FRG flow formulation (NLO-LPA) | ✓ Complete |
| Coupled YM+Scalar system | ✓ Complete |
| GZ-deformed gluon flow | ✓ Complete |
| Tachyonic UV boundary identified | ✓ Complete |
| κ̃₀* numerically determined | ✓ Complete (κ̃₀* = 0.048777) |
| m²_S(Λ) physically motivated | ✗ Open (next TKT) |
| γ predicted without γ as input | ✗ Open (requires above) |

**L4 remains E-open.** The barrier is now precisely localized:
the missing ingredient is a physical principle fixing m²_S(Λ) = −0.1189 GeV².

---

## Constitution Check

```
|5κ²−3λ_S|  = 0.0  (machine zero) ✓
mp.dps      = 80 (local, Race Condition Lock) ✓
float()     : NOT used ✓
Ledger constants: unchanged ✓
Bisection residual |F| = 3.33×10⁻¹³ < 1e-12 ✓
```

---

## Next TKT: Physical Origin of m²_S(Λ)

Candidate mechanisms (all Evidence E — speculative):

1. **Coleman-Weinberg**: m²_S generated radiatively from g̃²(Λ) via
   m²_S = −(b₀/16π²) g²_Λ Δ*²·f(ξ_eff)

2. **ξ_eff-induced mass**: The mixing term ξ_eff S TrF²
   generates an effective tachyonic mass at one loop:
   m²_eff = −ξ²_eff ⟨TrF²⟩_Λ / Δ*²

3. **Gribov-induced SSB**: M_G scale sets the IR cutoff;
   the ratio M_G/Δ* ≈ 0.38 may fix m²_S geometrically.

4. **Lattice input**: Use lattice QCD scalar condensate at μ = Δ*
   as external calibration (Stratum I, evidence B).

Mechanism (2) is most natural within UIDT framework and will be
formulated as TKT-FRG-XICW (ξ-Coleman-Weinberg).

---

*Stratum III throughout. Evidence E-open. No Stratum I/II mixing.*
*Transparency priority: negative result on γ-prediction explicitly stated.*
