# TKT-FRG-XI-LOOP: Analytische 1-Schleifen ξ-Vertex Analyse

**Ticket:** TKT-FRG-XI-LOOP  
**Follows from:** TKT-20260416-Phase3-FRG-NLO-gamma.md  
**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-16  
**Stratum:** III  
**Evidence:** E-open (negative results documented)  
**Constitution compliance:** mpmath dps=80, no float(), RG-constraint machine zero

---

## Objective

Explicitly compute the 1-loop contribution of the ξ S TrF² vertex to
∂_t Z_k and ∂_t Z_S, and test whether the conjecture UIDT-C-05V
(Δη = η_A - η_S = 1) follows analytically.

---

## Setup: ξ-Vertex Feynman Rules

```
L_mix = ξ_eff / Λ × S × Tr[F_μν F^μν]
```

With UIDT structural identity:

```
ξ_eff × Δ* = κ = 0.5   [A — exact]
```

The vertex couples one scalar insertion to two gluon lines.

---

## 1-Loop Contributions (Litim Regulator)

### η_A|ξ — Scalar loop in gluon 2-point function

```
η_A|ξ = 3 ξ_eff² v² c₄ k²
```

Numerical values:
- η_A|ξ(k = Δ*) = 5.40 × 10⁻⁶
- η_A|ξ(k = E_geo) = 2.02 × 10⁻⁸

### η_A|_YM — Gluon-Ghost loop (pure YM, 1-loop running)

```
η_A|_YM = b₀ g²_k / (16π²)
```

Numerical values (with α_s(Δ*) = 0.3):
- η_A|_YM(k = Δ*) = 0.2626
- η_A|_YM(k = E_geo) = 0.1515

**Dominance ratio:** η_A|_YM / η_A|ξ ≈ 48600 at k = Δ*

### η_S|ξ — Gluon loop in scalar 2-point function

```
η_S|ξ = ξ_eff² c₄ k² × 3 d_adj
```

Numerical values:
- η_S|ξ(k = Δ*) = 0.01900
- η_S|ξ(k = E_geo) = 7.12 × 10⁻⁵

---

## Critical Ratio Analysis

```
η_A|ξ / η_S|ξ = v² / d_adj = (47.7 MeV)² / 8 = 2.84 × 10⁻⁴ GeV²
```

Key finding: **η_A|ξ << η_S|ξ by factor ~3500.**

The ξ-vertex amplifies the SCALAR wave-function renormalization STRONGER
than the gluon WFR. This means the ξ-loop alone would produce:

```
γ_eff|ξ = exp(∫[η_S|ξ - η_A|ξ] dt) < 1
```

This is the OPPOSITE direction required for γ = 16.339.

---

## UIDT-C-05V Status: REFUTED AT 1-LOOP

The conjecture UIDT-C-05V proposed:

```
Δη = η_A - η_S = 1   (over confining regime)
```

The 1-loop ξ-vertex computation shows:
- η_A|ξ dominates only if v >> Δ* (violated: v = 47.7 MeV << Δ*)
- The YM sector dominates η_A by a factor ~48600
- The ξ-vertex contributes negatively to the Z_k/Z_S ratio

**Conclusion: UIDT-C-05V is refuted at 1-loop order for the ξ-vertex mechanism.**

The Δη ~ 1 numerical coincidence from Phase 3 was a result of:

```
ln(γ) / |ln(E_geo/Δ*)| = 2.7934 / 2.7936 ≈ 1
```

This is equivalent to the statement:

```
γ ≈ Δ*/E_geo  AND  ln(Δ*/E_geo) ≈ ln(γ)
```

...which is tautologically true by definition! It contains no physical
mechanism, only a mathematical identity from the definition of γ.

---

## Revised FRG Strategy: E_geo as Freezing Scale

Alternative FRG interpretation: E_geo is the scale k_freeze where the
physical minimum ρ_phys(k) = k² ρ̃_0(k) stops evolving:

```
d/dk ρ_phys(k) = 0

⇒  ρ̃_0 = (c₄ d_adj) / [2(1 + 2λ ρ̃_0)]
```

Solving this quadratic gives:

```
ρ̃_0^freeze = 0.012534

k_freeze = sqrt(ρ_phys / ρ̃_0^freeze)
         = sqrt((47.7 MeV)²/2 / 0.012534)
         = 301.3 MeV
```

**Comparison:**
- k_freeze = 301 MeV
- E_geo = 104.7 MeV
- Deviation: 188% — the LPA freezing scale does NOT reproduce E_geo.

---

## Conclusions for Limitation L4

| Approach | Result | Status |
|---|---|---|
| UIDT-C-05V: Δη = 1 from ξ-loop | Refuted at 1-loop | E-open → WITHDRAWN |
| YM dominance of η_A | Confirmed | Structural |
| LPA freezing scale k_freeze | 301 MeV ≠ E_geo | Inconsistent |
| Full non-perturbative FRG | Not computed | E-open |

**L4 remains E-open.** The FRG analysis demonstrates that:

1. γ is NOT determined by 1-loop ξ-vertex physics
2. The relevant mechanism must be non-perturbative (Confinement sector)
3. The LPA approximation is insufficient; higher truncations or external
   Confinement input (Gribov-Zwanziger, DSE) are required

---

## Positive Structural Results

Despite the negative results for C-05V, this analysis establishes:

**Finding 1:** ξ_eff × Δ* = κ = 0.5 [A] is a genuine structural identity
in the UIDT Lagrangian, not an accident. It ensures the ξ-coupling is
controlled by the Yang-Mills spectral scale.

**Finding 2:** The ξ-loop contribution to η_S is numerically non-negligible
(η_S|ξ ≈ 0.019 at k = Δ*) and represents a genuine NLO effect on the
scalar sector that must be included in any complete FRG analysis.

**Finding 3:** The YM sector completely dominates the gluon anomalous
dimension (η_A|_YM >> η_A|ξ by factor ~48600). This means future FRG
work on γ must focus on the non-perturbative YM sector, not the scalar
coupling.

---

## Updated Dependency Chain and Evidence

```
Δ* [A] → γ [A-] → E_geo [A-] → f_vac [C]
```

γ upgrade path: A- → D requires non-perturbative SU(3) FRG with
Confinement input (Gribov-Zwanziger or Dyson-Schwinger boundary condition).

---

## Open Tickets Revised

| Ticket | Status | Notes |
|---|---|---|
| UIDT-C-05V (Δη=1) | WITHDRAWN | Refuted at 1-loop |
| TKT-FRG-CONFINEMENT | OPEN — HIGH | Critical path for L4 resolution |
| TKT-FRG-XI-LOOP | CLOSED | This document |
| UIDT-C-05W (γ_alg = N_c b₀/(2κ+1)) | E-open | 0.99% algebraic coincidence, no derivation |

---

## Constitution Compliance

- mpmath dps=80 declared locally
- No float() used
- RG-Constraint |5κ² - 3λ_S| = 0 (machine zero)
- No Ledger constants modified
- All new claims tagged appropriately
- Negative results (C-05V withdrawal) reported transparently

*Transparency has priority over narrative.*
