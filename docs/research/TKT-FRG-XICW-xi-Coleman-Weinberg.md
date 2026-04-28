# TKT-FRG-XICW — ξ_eff Coleman-Weinberg Analysis

**Author:** P. Rietz  
**Date:** 2026-04-19  
**Status:** E-open (Stratum III — speculative)  
**Depends on:** TKT-FRG-TACHYON (target: m²_S = −0.1188578 GeV²)  
**Script:** `verification/scripts/verify_FRG_xicw.py`  
**Constitution:** mp.dps=80 local, no float(), RG-constraint machine zero ✓

---

## Objective

Show that the tachyonic UV mass

\[ m^2_S(\Lambda) = -0.1188578\,\text{GeV}^2 \]

found in TKT-FRG-TACHYON follows from the UIDT coupling term

\[ \mathcal{L}_{\xi} = \xi_{\text{eff}}\, S\, \text{Tr}\, F^2 \]

without using γ as input.

---

## Mechanism

### One-Loop CW Formula [Stratum III]

Integrating out gluon fluctuations at k = Δ* with the GZ propagator:

```
m²_S(Λ) = − ξ_eff² · <TrF²>_Λ

<TrF²>_Λ = d_adj · (1/16π²) · Δ*⁴ · Z_GZ(Δ*)

Z_GZ(k)  = k⁴ / (k⁴ + M_G⁴)    [Gribov-Zwanziger]
```

### Numerical Values

```
d_adj               = 8    (SU(3))
Δ*                  = 1.710 GeV  [A]
M_G                 = 0.65 GeV   [B]
Z_GZ(Δ*)            = 0.97954989
<TrF²>_Δ*           = 0.42430804 GeV⁴
```

---

## ξ_eff Determination

### From Inversion (consistency check)

```
ξ_eff²  = |m²_S| / <TrF²>_Δ*  =  0.2801215
ξ_eff   = 0.52926506  (required)
```

### Loop-Order Structure

With αs(Δ*) ≈ 0.3, g²(Δ*) = 4π·αs = 3.7699:

```
ξ_eff = C_xi · g²(Δ*) / (16π²)
C_xi  = 22.170  (required from target)
```

---

## C_xi Candidate Scan

All group-theory candidates sorted by deviation from target:

| Candidate | Value | |dev| | dev% |
|---|---|---|---|
| **2b₀ + 1/b₀** | **22.091** | **0.079** | **0.36%** ← |
| 2b₀ | 22.000 | 0.170 | 0.77% |
| 2b₀ + Nc/d_adj | 22.375 | 0.205 | 0.93% |
| b₀·Nc/√2 | 23.335 | 1.165 | 5.25% |
| 3d_adj − Nc | 21.000 | 1.170 | 5.28% |
| d_adj·Nc | 24.000 | 1.830 | 8.26% |
| b₀²/(2Nc) | 20.167 | 2.003 | 9.04% |

b₀ = 11Nc/3 = 11 for SU(3).

**Best candidate: C_xi = 2b₀ + 1/b₀**

---

## Physical Interpretation of C_xi = 2b₀ + 1/b₀

```
C_xi = 2b₀ + 1/b₀
     = 2·(11Nc/3) + 3/(11Nc)
     = 22 + 1/11   for SU(3)
```

**Conjecture [E-open]:**  
The factor `2b₀` corresponds to the two-loop anomalous dimension coefficient
for the composite operator `S·TrF²` under the adjoint representation.
The `1/b₀` term is a subleading correction of order O(g²/(16π²b₀)) from
the scalar-gluon mixing vertex renormalization.

Formally, this structure arises if the beta function for ξ_eff takes the form:

```
β_ξ = − (b₀ + 1/(2b₀)) · g² · ξ_eff / (8π²)
```

and ξ_eff is evaluated at the GZ fixed point k = Δ*.

**This interpretation is Stratum III and requires analytical confirmation.**

---

## Prediction vs. Target

```
C_xi (best)         = 22.0909  (= 2b₀ + 1/b₀)
ξ_eff (predicted)   = 0.52738161
ξ_eff (required)    = 0.52926506
Δξ_eff              = 0.001884

m²_S (predicted)    = −0.1180133724 GeV²
m²_S (target)       = −0.1188578047 GeV²
|Δm²_S|             = 0.000844 GeV²
Deviation           = 0.71%
```

The 0.71% gap suggests the CW formula with C_xi = 2b₀ + 1/b₀ is **consistent
but not exact** at this truncation level. Sources of residual deviation:

1. Next-to-leading GZ corrections to <TrF²> (beyond LPA)
2. Two-loop contribution to β_ξ
3. Scheme dependence of αs at k = Δ* (PDG: αs(M_Z) = 0.1179 → αs(1.71 GeV) ≈ 0.30–0.32)

---

## What Would Close L4

To lift γ from Evidence A− to Evidence A, the following chain is required:

```
Step 1: Prove C_xi = 2b₀ + 1/b₀ analytically from UIDT Lagrangian
        (Feynman diagram calculation of β_ξ at NLO)
        → gives ξ_eff(Δ*) without γ as input

Step 2: Show <TrF²>_Δ* = d_adj/(16π²) · Δ*⁴ · Z_GZ(Δ*)
        is the correct GZ condensate in the UIDT vacuum
        (lattice check or SD-equation derivation)
        → confirms m²_S = −ξ_eff² · <TrF²>

Step 3: Insert m²_S into TKT-FRG-TACHYON inversion
        → κ̃₀* is now fully determined from Δ*, M_G, αs

Step 4: Read off γ = Δ* / E_geo where E_geo = κ̃₀-dependent scale
        from the IR flow, without using γ_canonical as input
        → γ is predicted: Evidence A achieved
```

**Current status:** Step 1 (analytical derivation of C_xi) is the blocking sub-task.
The numerical gap of 0.71% is compatible with NLO corrections and does not
disprove the mechanism — but it does not confirm it either.

---

## L4 Status Update

| Sub-task | Status |
|---|---|
| FRG flow + GZ deformation | ✓ Complete |
| Tachyonic UV boundary κ̃₀* | ✓ Complete |
| ξ_eff-CW mechanism identified | ✓ Complete (this TKT) |
| C_xi = 2b₀+1/b₀ numerical fit | ✓ 0.71% deviation |
| Analytical proof of C_xi | ✗ **Open — next TKT** |
| <TrF²> from SD / lattice | ✗ Open |
| γ predicted without γ as input | ✗ Open (requires above) |

**L4 remains E-open.** Barrier is now further localized:
the missing ingredient is the analytical derivation of β_ξ → C_xi.

---

## Next TKT: TKT-FRG-BETAXI

Compute β_ξ for the coupling ξ_eff S TrF² at NLO in UIDT framework.
Verify whether β_ξ produces C_xi = 2b₀ + 1/b₀ analytically.

---

## Constitution Check

```
|5κ²−3λ_S|  = 0.0  (machine zero) ✓
mp.dps      = 80 (local) ✓
float()     : NOT used ✓
Ledger constants: unchanged ✓
C_xi scan: 13 candidates evaluated ✓
```

---

*Stratum III throughout. Evidence E-open.*  
*0.71% numerical compatibility is suggestive, not conclusive.*  
*Transparency priority: limitation explicitly stated.*
