# UIDT Framework — Current Status

> **Version:** 3.9 | **Date:** 2026-05-08 | **DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

---

## Framework State at a Glance

| Dimension | Status |
|---|---|
| **Verification Suite** | ✅ 78/78 tests pass, 90 scripts, <10⁻¹⁴ residuals |
| **Claims Registry** | 60 claims (LEDGER/CLAIMS.json) |
| **Evidence Distribution** | 8 [A], 6 [A-], 12 [B], 15 [C], 14 [D], 5 [E] |
| **Active Limitations** | L1, L2, L4, L5, L6-FRG (L3 accepted) |
| **Latest Research** | Color algebra proof [A], Kill-switch proof [A] (2026-05-08) |
| **Research Roadmap** | [`docs/research/L1_L4_L5_roadmap_2026-05-08.md`](./docs/research/L1_L4_L5_roadmap_2026-05-08.md) |

---

## Core Parameters (Read-Only)

```
Δ* = 1.710 ± 0.015 GeV    [A]   Spectral gap (NOT particle mass)
γ  = 16.339                [A-]  Kinetic VEV (phenomenological, NOT derived)
κ  = 0.500 ± 0.008         [A]   Non-minimal coupling
λ_S = 5κ²/3 = 0.41̄6̄      [A]   Exact RG fixed-point
v  = 47.7 MeV              [A]   Vacuum expectation value
m_S = 1.705 ± 0.015 GeV    [D]   Scalar mass prediction
E_T = 2.44 MeV             [C]   Torsion binding energy
H₀ = 70.4 ± 0.16 km/s/Mpc  [C]   DESI-calibrated (NOT prediction)
```

---

## Open Limitations

| ID | Problem | Evidence | Next Step |
|---|---|---|---|
| **L1** | 10¹⁰ geometric factor ill-defined | [D] | Define UV/IR scales precisely, topology/holography |
| **L2** | Electron mass 23% residual | — | Electroweak coupling integration |
| **L4** | γ = 16.339 not RG-derived | [A-] | BMW-FRG momentum-dependent vertex flow |
| **L5** | N=99 steps unjustified | [D] | First-principles derivation |
| **L6-FRG** | FRG minimal truncation | [D] | Full NLO Dyson-resummed analysis |

---

## Recent Breakthroughs (2026-05-08 Sprint)

1. **Color Algebra Identity** [A]: γ_bare = (2N_c+1)²/N_c = 49/3 ≈ 16.333. Proven at 80-digit precision.
2. **Kill-Switch Formal Proof** [A]: Σ_T(E_T=0) = 0 proven with exact linearity over 24 orders of magnitude.
3. **Cross-Constraint Matrix** [A]: 10/10 inter-parameter constraints verified simultaneously.
4. **Scalar Self-Energy No-Go** [D]: 1-loop scalar bubble insufficient for δγ — BMW-FRG is the mandatory path.

---

## Navigation

| What | Where |
|---|---|
| Full README | [`README.md`](./README.md) |
| Mathematical Formalism | [`FORMALISM.md`](./FORMALISM.md) |
| Canonical Constants | [`CANONICAL/CONSTANTS.md`](./CANONICAL/CONSTANTS.md) |
| Limitations (Full) | [`CANONICAL/LIMITATIONS.md`](./CANONICAL/LIMITATIONS.md) |
| Claims Registry | [`LEDGER/CLAIMS.json`](./LEDGER/CLAIMS.json) |
| Verification Suite | [`verification/`](./verification/) |
| **Research Notes** | [`docs/research/INDEX.md`](./docs/research/INDEX.md) |
| Master Roadmap | [`docs/research/L1_L4_L5_roadmap_2026-05-08.md`](./docs/research/L1_L4_L5_roadmap_2026-05-08.md) |

---

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609) | **License:** CC BY 4.0
