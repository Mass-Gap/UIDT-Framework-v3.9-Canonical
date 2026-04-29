# FRG/NLO Derivation of γ — Module Overview

**Branch**: `TKT-FRG-GAMMA-NLO`  
**Goal**: Derive γ = 16.339 from the UIDT scalar-gauge Lagrangian via Wetterich FRG at NLO (LPA').  
**Current evidence**: [A-] (phenomenological) — target: [A] (mathematically proven).  
**Maintainer**: P. Rietz — DOI: 10.5281/zenodo.17835200  

---

## Epistemic Status

| Item | Category | Note |
|------|----------|------|
| Δ\* = 1.710 GeV | [A] | Fixed-point proof, Theorem 1 |
| γ = 16.339 | [A-] | Phenomenological; THIS module targets [A] |
| RG constraint 5κ² = 3λS | [A] | Maintained throughout |
| FRG flow for γ | [D] | Prediction, not yet proven |

Upgrade path: [D] → [A] requires closed analytic or high-precision numerical proof  
that `γ(k → 0) = 16.339` with residual < 1e-14.

---

## Module Structure

```
modules/frg_gamma_nlo/
├── README.md                  (this file)
├── lagrangian.py              (Step 1: Lagrangian + symmetry constraints)
├── truncation.py              (Step 2: LPA' truncation + regulator)
└── flow_equations.py          (Step 3: Wetterich flow; mpmath 80-digit)
```

## Dependency Chain

```
Δ* [A]  ⟶  γ [A- → A]  ⟶  E_geo [A- → A]  ⟶  f_vac [C → B]
```

All upgrades are contingent on this module closing the FRG derivation.

---

## Open Tickets

- `TKT-FRG-BRIDGE-01` — dimensional bridge g_fc ↔ Δ* (separate; Path A)
- `TKT-FRG-GAMMA-NLO` — THIS ticket: derive γ from Lagrangian
