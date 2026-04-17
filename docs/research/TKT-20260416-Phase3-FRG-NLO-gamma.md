# TKT-20260416 Phase 3: FRG/NLO Analysis — γ-Derivation via Wetterinck Equation

**Ticket:** TKT-20260403-FRG-NLO  
**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-16  
**Stratum:** III (UIDT interpretation and theoretical extension)  
**Evidence target:** E-open → D-candidate  
**Constitution compliance:** mpmath dps=80, no float(), RG-constraint machine zero

---

## Objective

Address Limitation L4: γ = 16.339 is currently a phenomenological parameter [A-]
not derived from first principles. This note investigates whether a Functional
Renormalization Group (FRG) approach can derive E_geo = Δ*/γ = 104.658 MeV from
the UIDT Lagrangian, thereby lifting γ to evidence category D (first-principles
compatible).

The operative definition is:

```
γ ≡ Δ* / E_geo    [A-]
```

FRG target: **Derive E_geo = 104.658 MeV from the RG flow** of the UIDT
Lagrangian. Then γ = Δ*/E_geo = 16.339 follows without separate input.

---

## Framework: FRG Truncation

### UIDT Lagrangian (NLO Truncation)

```
Γ_k[A,S] = ∫d⁴x { Z_k/4 F²_μν + Z_S/2 (∂S)² + V_k(S) + ξ_k/Λ × S × TrF² }
```

Anomale Dimensionen:
- η_A(k) = -∂_t ln Z_k    (Gluon wave function renormalization)
- η_S(k) = -∂_t ln Z_S    (Scalar wave function renormalization)

Projection formula for γ_eff:

```
γ_eff(k) = lim_{q²→0} ∂_{k²}[Γ_k^{AA}(q²)] / ∂_{k²}[Γ_k^{SS}(q²)]
```

### Litim Regulator (Optimised)

```
R_k(q²) = Z_k (k² - q²) θ(k² - q²)
```

Advantage: Threshold functions l_n(w) = 1/(1+w)^{n+1} are analytic.

### LPA Beta Functions (d=4, SU(3), N_f=0)

```
∂_t V_k(ρ) = c_4 k⁶ { 1/(1 + V''_k) + (N_c²-1) }

c_4 = 1/(32π²)
```

Symmetry-breaking ansatz:

```
V_k(ρ) = λ_k (ρ - ρ_0(k))²

∂_t λ_k = c_4 × 2λ_k² × d_adj / (1 + 2λ_k ρ_0)²
∂_t ρ_0  = c_4 × d_adj / (1 + 2λ_k ρ_0)
```

---

## UV Boundary Conditions (at k_UV = Δ* = 1.710 GeV)

| Parameter | Physical value | Dimensionless at k_UV |
|---|---|---|
| ρ_0(k_UV) = v²/2 | 0.001138 GeV² [A] | ρ̃_0 = 3.891×10⁻⁴ |
| λ_S | 5/12 ≈ 0.41667 [A] | marginal (d=4) |
| κ | 0.500 [A] | — |
| ξ_eff = κ/Δ* | 0.2924 GeV⁻¹ | ξ_eff × Δ* = κ = 0.5 |

RG-Constraint verified: |5κ² - 3λ_S| = 0 (machine zero, dps=80)

---

## Key Structural Finding: ξ × Δ* = κ

The non-minimal coupling ξ_k/Λ × S × TrF² has the property:

```
ξ_eff × Δ* = (κ/Δ*) × Δ* = κ = 0.5   [A — exact, Ledger]
```

This dimensionless combination κ is a **Ledger parameter [A]**. It connects
the non-minimal coupling directly to the RG fixed point. The ξ-vertex drives
the differential running of Z_k vs. Z_S, creating the γ_eff ratio:

```
(∂_t Z_k)_ξ ~ ξ_eff² × S_vac² × c_4 × f(Δ/k)
```

---

## Algebraic Search: γ from UIDT Parameters

Systematic search over expressions in {κ, λ_S, N_c, b₀, d_adj}:

| Expression | Value | |Δγ| | Status |
|---|---|---|---|
| N_c × b₀ / (2κ+1) | 16.500 | 0.161 (0.99%) | Best algebraic candidate |
| 4/κ² | 16.000 | 0.339 (2.07%) | Simple but off |
| b₀²/(2N_c+1) | 17.286 | 0.947 (5.79%) | Too large |
| All others | — | > 3 | — |

Conclusion: **No simple algebraic expression in the UV parameters reproduces
γ = 16.339 to better than 0.99%.** γ is not purely algebraically
determined from the UV sector.

### Best Algebraic Candidate [E-open, UIDT-C-05W]

```
γ_alg = N_c × b₀ / (2κ + 1) = 3 × 11 / 2 = 33/2 = 16.500

|γ_alg - γ_canonical| = 0.161  (0.99%)
Within MC uncertainty (σ = ±1.005): YES
Group-theoretic derivation: ABSENT
Evidence: E-open
```

---

## Two Forward Paths for L4 Resolution

### Path A — Numerical FRG Flow

Full numerical integration of the coupled system:

```
dλ/dt = c_4 × 2λ² × d_adj / (1 + 2λρ̃_0)²
dρ̃_0/dt = c_4 × d_adj / (1 + 2λρ̃_0)
dZ_k/dt = c_4 × k² × I_A(g_k, λ, Z_k, Z_S, ξ_k)
dZ_S/dt = c_4 × k² × I_S(g_k, λ, Z_k, Z_S, ξ_k)
```

from k_UV = Δ* to k_IR = E_geo.

γ_eff = Z_k(k_IR) / Z_S(k_IR) evaluated at k_IR.

**Blocker:** Requires non-perturbative IR input for the SU(3) sector
(Confinement mechanism). Without it, the flow diverges before reaching k_IR.

**Status:** D-candidate if consistent with Confinement model.

### Path B — Anomalous Dimension via ξ-Vertex

If η_A - η_S ≡ Δη is approximately constant over the flow interval:

```
γ_eff ~ exp[Δη × |t_flow|]  where t_flow = ln(E_geo/Δ*) = -2.794

Required: Δη = ln(γ) / |t_flow| = ln(16.339) / 2.794 = 1.003
```

This is a remarkably clean number: **Δη ≈ 1** (unit anomalous dimension).

```
Required anomalous dimension difference:
Δη = ln(γ_canonical) / |ln(E_geo/Δ*)|
   = ln(16.339) / ln(Δ*/E_geo)
   = 2.7934 / 2.7936
   ≈ 1.0000
```

**New Conjecture UIDT-C-05V [E-open]:**
The ξ-vertex drives exactly Δη = η_A - η_S = 1 over the confining regime,
implying γ_eff = exp(|t_flow|) = Δ*/E_geo = γ.

This would mean: E_geo is the natural IR scale of the theory (where Z_k/Z_S = e).

---

## Critical Constraint: Confinement

The FRG flow for SU(3) Yang-Mills has:
- Gaussian UV fixed point: g*(UV) = 0
- No perturbative IR fixed point
- Confinement requires non-perturbative physics (Gribov copies, monopole condensation, etc.)

This means: **The FRG alone (in LPA or NLO) cannot close the flow without
additional Confinement input.** This is the fundamental limitation of Path A.

Possible supplements:
1. Gribov-Zwanziger propagator (modifies IR gluon propagator)
2. Dyson-Schwinger truncation (provides IR gluon mass)
3. Lattice QCD input for Z_k(k < Λ_QCD)

---

## Evidence Summary

| Claim | Value | Category | Notes |
|---|---|---|---|
| γ = Δ*/E_geo | 16.339 | A- | Unchanged |
| ξ_eff × Δ* = κ | 0.5 (exact) | A | Structural identity |
| γ_alg = N_c b₀/(2κ+1) | 16.500 (0.99%) | E-open | Best algebraic approx. |
| Δη = 1 conjecture | E-open | C-05V | Requires ξ-loop calculation |
| Full FRG flow | Not computed | E-open | Needs Confinement input |

---

## Dependency Chain Update

```
Δ* [A] → γ [A-] → E_geo [A-] → f_vac [C]
              ↑
        [FRG Path A/B]
        (currently E-open)
```

Upgrade path: A- → D requires demonstration of Path A or B consistency.
A- → B requires lattice validation of E_geo prediction.

---

## Constitution Compliance

- mpmath dps=80 declared locally in all computations
- No float() used
- RG-Constraint |5κ² - 3λ_S| = 0 (machine zero)
- No Ledger constants modified
- No deletion > 10 lines in /core or /modules
- All claims tagged E-open
- Stratum III throughout — no Stratum I/II mixing

---

## Open Tickets Generated

| Ticket ID | Description | Priority |
|---|---|---|
| UIDT-C-05V | Δη = 1 conjecture from ξ-vertex | High |
| UIDT-C-05W | γ_alg = N_c b₀/(2κ+1) algebraic candidate | Medium |
| TKT-FRG-CONFINEMENT | Identify Confinement input for Path A | Highest |
| TKT-FRG-XI-LOOP | Compute ξ² loop contribution to η_A - η_S | High |

---

## Next Steps

1. **TKT-FRG-XI-LOOP:** Compute the one-loop ξ-vertex contribution to
   ∂_t Z_k explicitly and check whether Δη ≈ 1 emerges analytically.

2. **TKT-FRG-CONFINEMENT:** Survey Gribov-Zwanziger and DSE approaches
   for non-perturbative IR boundary condition compatible with UIDT.

3. **Path B verification:** If Δη = 1 is confirmed analytically from the
   ξ-vertex, this would be the first first-principles derivation of γ
   in UIDT. Target evidence: D-candidate → pending lattice check → B.

---

*Stratum III. Evidence: E-open. Transparency has priority over narrative.*
