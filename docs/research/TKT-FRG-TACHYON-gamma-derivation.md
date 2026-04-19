# TKT-FRG-TACHYON — Tachyonic UV Boundary for γ Derivation

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-19  
**DOI:** 10.5281/zenodo.17835200  
**Status:** E-open (Stratum III — UIDT interpretation)  
**Depends on:** TKT-FRG-COUPLED (Phase 3b/3c results), PR #302

---

## Motivation

Limitation L4 states: γ = 16.339 is not derived from the UIDT Lagrangian.

Phases 3b and 3c (coupled YM+Scalar FRG flow, GZ-deformed) demonstrated a
fundamental barrier: using v = 47.7 MeV as a UV boundary condition leads to
immediate κ̃ → 0 (symmetry restoration) at k ≈ Δ*, because the 8 massless
gluon loops dominate ∂_t κ̃ by a factor of ~65 over the scalar contribution.

The resolution is standard FRG SSB theory: spontaneous symmetry breaking
requires a **tachyonic UV mass** m²_S(Λ) < 0 as initial condition.
This ticket implements the resulting inversion problem.

---

## Mathematical Formulation

### Effective Action (NLO-LPA' Truncation)

```
Γ_k[A, c, c̄, S] = ∫d⁴x {
    ¼ Z_A(k) F²_μν  +  Z_c(k) c̄(-D²)c
    + Z_S(k) (∂_μS)²  +  U_k(S²/2)
    + ξ_eff Z_A(k) S TrF²
}
```

with dynamical fields:
- U_k(ρ): Local Potential Approximation flow
- Z_A(k): Gluon WFR with Gribov-Zwanziger damping
- Z_S(k): Scalar WFR (LPA', η_S ≠ 0)
- g²_k:   Running YM coupling (1-loop)

### UV Ansatz (Tachyonic Start)

```
U_Λ(ρ) = m²_S(Λ) · ρ  +  λ_S · ρ²,    m²_S(Λ) < 0
```

Dimensionless initial VEV:
```
κ̃(t=0) = -m²_S(Λ) / (2 λ_S Λ²)   >  0
```

### Dimensionless Flow Variables

t = ln(k/Δ*)   (flow parameter: t=0 at UV k=Δ*, t_IR = ln(E_geo/Δ*) ≈ -2.794)

| Variable | Definition | Boundary condition |
|---|---|---|
| κ̃(t) | ρ₀(k)/k² | κ̃(0) = -m²_S/(2λ_S Δ*²) [FREE] |
| λ̃(t) | λ_S (dimensionless in d=4) | λ̃(0) = 5/12 [FIXED, RG constraint] |
| g̃²(t) | g²_k | g̃²(0) = 4π·α_s(Δ*) ≈ 3.77 |
| Z_A(t) | Gluon WFR | Z_A(0) = 1 |

RG constraint (immutable): 5κ² = 3λ_S → λ̃(0) = 5/12

### Coupled Flow Equations (Litim Regulator, d=4)

Threshold functions:
```
L⁴_0(w) = 1/(1+w)
L⁴_1(w) = 1/(1+w)²
```

Gribov-Zwanziger damping:
```
Z_GZ(k) = k⁴ / (k⁴ + M_G⁴),    M_G = 0.65 GeV  [Lattice: Cucchieri & Mendes 2007]
```

Flow equations:
```
[1] ∂_t κ̃ = -2κ̃ + (1/16π²)[(N_S-1)·L⁴_0(0) + L⁴_0(2λ̃κ̃)]
           + (d_adj/16π²)·Z_GZ(k)  -  κ̃·η_S(k)

[2] ∂_t λ̃ = (2λ̃²/16π²)·[(N_S-1)·L⁴_1(0) + 3·L⁴_1(2λ̃κ̃)]  +  2λ̃·η_S(k)

[3] ∂_t g̃² = -(b₀/16π²)·g̃⁴          [1-loop YM]

[4] ∂_t Z_A = -(b₀/16π²)·g̃²·Z_GZ(k)·Z_A
```

where N_S = d_adj + 1 = 9, b₀ = 11·N_c/3 = 11, d_adj = 8.

### Inversion Problem (Core of this TKT)

Define the shooting function:
```
F(κ̃₀) := κ̃(t_IR; κ̃₀)  -  v²/(2·E_geo²)
```

Target:
```
v²/(2·E_geo²) = (47.7 MeV)² / (2·(104.658 MeV)²) = 0.10386411...
```

Goal: find κ̃₀* such that F(κ̃₀*) = 0.

This gives m²_S(Λ) = -2·λ_S·Δ*²·κ̃₀*, and from κ̃(t_IR)·k²_IR = v²/2,
the ratio γ = Δ*/E_geo = 16.339 follows INTERNALLY from the flow.

### Residual Tolerance

|F(κ̃₀*)| < 1e-14  (mpmath dps=80, Constitution requirement)

---

## Epistemic Status

| Layer | Content | Status |
|---|---|---|
| Stratum I | PDG: v (via f_π), α_s(Δ*), M_G (lattice) | Empirical |
| Stratum II | FRG-SSB standard: tachyonic UV mass → SSB | Consensus |
| Stratum III | UIDT: γ from κ̃₀ inversion | TKT-FRG-TACHYON [E-open] |

Evidence target: A for the method, A- for γ_derived if |γ_FRG - γ_canonical|/γ_canonical < 0.1%.

---

## Three-Phase Diagnostic Summary (from TKT-FRG-COUPLED)

| Phase | Method | γ_FRG | Deviation | Status |
|---|---|---|---|---|
| 3b | ξ-Loop (1-loop, analytic) | — | — | UIDT-C-05V WITHDRAWN (tautological) |
| 3c-A | Z_A/Z_S ratio | 1.25 | 92% | ✗ wrong mechanism |
| 3c-B | κ̃→0 transition | 1.004 | 94% | ✗ k_crit ≈ Δ* (gluon loops dominate) |
| 3c-C | LPA freeze scale | — | 188% | ✗ wrong sector |
| **TKT-FRG-TACHYON** | **κ̃₀ inversion** | **TBD** | **TBD** | **OPEN** |

Fundamental barrier identified: gluon loop (+0.0507) >> 2κ̃₀ (+0.00078) at t=0
with v as UV input. Tachyonic start κ̃₀ >> v²/(2Δ*²) required for SSB survival.

---

## Confinement Window (Evidence D)

All three UIDT scales satisfy the ordering:
```
E_geo = 104.7 MeV  <  M_G = 650 MeV  <  Δ* = 1710 MeV
```
This window is preserved in the tachyonic formulation.
Logarithmic partition by M_G:
```
UV segment: ln(Δ*/M_G)  = 0.967  (34.6% of ln γ)
IR segment: ln(M_G/E_geo) = 1.826  (65.4% of ln γ)
Total:       ln(γ) = 2.794
```

---

## Positive Result from Phase 3c (Evidence B-compatible)

Gluon WFR at IR scale:
```
Z_A(k = E_geo) = 1.3603
ln Z_A(E_geo)  = 0.3077
```
Consistent with non-perturbative gluon enhancement in confinement regime
(Bogolubsky et al. 2009, Cucchieri & Mendes 2007).

---

## Dependency Chain

```
Δ* [A]  →  γ [A-]  →  E_geo [A-]  →  f_vac [C]
                ↑
     TKT-FRG-TACHYON: if successful → γ [A]
     → E_geo and f_vac upgrade automatically
```

---

## Known Limitations

- L4: γ NOT yet derived — this TKT is the active attempt.
- The tachyonic mass m²_S(Λ) is a free parameter until fixed by UIDT dynamics.
- η_S set to 0 in LPA; LPA' upgrade needed for full NLO treatment.
- The ξ_eff-vertex coupling to gluons is O(ξ²) and neglected — valid for small ξ.
- M_G = 0.65 GeV from lattice; systematic error ±0.05 GeV propagates into flow.

---

## Constitution Check

- RG constraint: 5κ² = 3λ_S → machine zero ✓
- No float() usage ✓
- mp.dps = 80 local ✓
- No ledger constants modified ✓
- RACE CONDITION LOCK: precision declared inside functions ✓

---

## References

- Wetterich (1993): Exact renormalization group equation for the effective potential
- Berges, Tetradis, Wetterich (2002): Non-perturbative renormalization flow (Phys. Rep. 363)
- Defenu et al., JHEP 05 (2015) 141: Truncation effects in FRG SSB
- Cucchieri & Mendes (2007): Lattice gluon propagator (M_G = 0.65 GeV)
- Bogolubsky et al. (2009): Lattice gluon + ghost propagators
- PDG 2024: f_π = 92.1 ± 0.8 MeV, α_s(M_Z) = 0.1180 ± 0.0009

---

*Stratum III throughout. Evidence E-open. No Stratum I/II mixing.*
