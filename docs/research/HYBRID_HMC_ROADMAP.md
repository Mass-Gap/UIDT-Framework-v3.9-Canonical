# UIDT Hybrid HMC + Tensor Guidance Framework — Phase Roadmap v2.0

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**DOI:** 10.5281/zenodo.17835200  
**Date:** 2026-05-09  
**Evidence Category:** D (roadmap — speculative/experimental)

---

## Strategic Evidence Classification

| Module | Status | Evidence |
|--------|--------|----------|
| 80-digit Banach/HMC Core | Numerically validated | A/B |
| Gauge-Consistent Manifold Transport | Implemented (this release) | A |
| Tensor-Network Proposal Engine | Heuristic acceleration | D |
| Topological freezing mitigation | Known lattice problem | B |
| Mixed-precision acceptance | Numerically plausible | C |
| Full TN→UIDT mapping | Unresolved | D |
| FRG/TN hybridization | Experimental | D |

> **Critical architectural invariant:** Tensor networks are NOT part of the
> mass-gap proof (Category A/B). They are exclusively a sampling/ergodicity
> acceleration tool (Category D). This separation is Clay-critical.

---

## Fundamental Constraint

All proposals from heuristic engines (TN, ML, normalizing flows) must satisfy:

1. **Gauge invariance:** U_μ(x) ∈ SU(3)
2. **Haar measure conservation:** invariant integration measure
3. **Osterwalder–Schrader positivity:** reflection positivity of transfer matrix
4. **Detailed balance:** P(U→U') e^{−S[U]} = P(U'→U) e^{−S[U']}
5. **Ergodicity:** all configurations reachable
6. **BRST compatibility:** consistent with cohomological structure

Tensor networks typically violate at least 2 of these implicitly. The
`modules/gauge_projection.py` module enforces constraints 1–4 explicitly.

---

## Phase 0 — Formal Consistency Layer (CURRENT)

**Before any code.** Mathematical proofs and computational audits.

### Deliverables
1. ✅ Gauge covariance — Gell-Mann basis algebra verified (residuals < 10⁻¹⁴)
2. ✅ Detailed balance — Symmetrized proposal kernel implemented
3. ✅ Haar measure conservation — Newton-Schulz polar decomposition (residuals < 10⁻⁷⁰)
4. ✅ SVD condition monitoring — Kill-switch at κ > 10¹²
5. ⏳ Ergodicity preservation — Formal proof pending
6. ⏳ Reflection positivity safety — Formal proof pending
7. ⏳ BRST compatibility — Connection to existing BRST verification

### Implementation
- `modules/gauge_projection.py` — Gauge-consistent manifold transport (Cat. A)
- `verification/tests/test_gauge_projection.py` — 30 tests, native mpmath
- `verification/scripts/verify_gauge_projection.py` — Standalone verification

---

## Phase I — Minimal SU(2) Sandbox

**NOT SU(3) yet.** Begin with SU(2), L=4.

| Advantage | Significance |
|-----------|-------------|
| Smaller group manifold | More stable projection |
| Analytically controllable | Easier debugging |
| Faster autocorrelation stats | Early validation |
| Known exact results | Clean benchmarking |

### Deliverables
- SU(2) version of gauge_projection.py (parameterized)
- Minimal 4⁴ lattice HMC with SU(2) Wilson action
- Baseline τ_Q measurement (pure HMC)
- First TN proposal test (MPS, bond dim χ=4)
- Detailed balance verification on SU(2) ensemble

### Success criterion
- τ_Q^{hybrid} / τ_Q^{HMC} measurable
- All kill-switches operational
- Acceptance rate > 5%

---

## Phase II — Pure Yang-Mills Benchmark

**NO UIDT S-field yet.** Standard Wilson action only:

S_W = β Σ_P (1 − (1/3) Re Tr U_P)

### Rationale
Without isolating the gauge sector first, it is impossible to determine
whether any improvement originates from the TN proposal or the UIDT coupling.

### Deliverables
- Pure SU(3) Wilson action HMC at β=6.0
- Baseline measurements: ⟨P⟩, string tension, τ_Q
- TN-guided proposal with gauge_projection.py gatekeeper
- Comparative τ_Q measurement

### Success criterion
- τ_Q^{hybrid} / τ_Q^{HMC} < 0.5 (preliminary)
- No detailed balance violations > 10⁻⁸
- No Haar drift > 10⁻¹⁰

---

## Phase III — UIDT Coupling Injection

**Only after Phase II validates the gauge sector.**

Introduce the UIDT scalar-gauge coupling:

L_int = (κ/Λ) S Tr(F²)

### Deliverables
- Full UIDT lattice action with TN-guided proposals
- Spectral gap extraction with hybrid sampler
- Comparison to pure HMC results from existing simulation

### Success criterion
- Δ* consistent with canonical value 1.710 ± 0.015 GeV [A]
- τ_Q^{hybrid} / τ_Q^{HMC} < 0.1 (target breakthrough)
- All audit system checks passing (see table below)

---

## Audit System (Kill-Switch Table)

| Test | Threshold | Meaning |
|------|-----------|---------|
| Detailed balance violation | > 10⁻⁸ | Immediate halt |
| Haar measure drift | > 10⁻¹⁰ | Invalid ensemble |
| SVD condition explosion | > 10¹² | Numerical instability |
| Topological bias | > 2σ | Ensemble falsified |
| Acceptance rate | < 5% | Inefficient |
| τ_Q improvement | < 2× | No practical benefit |

---

## Precision Architecture

| Layer | Precision | Purpose |
|-------|-----------|---------|
| TN contraction | FP64 | Heuristic direction only |
| SU(3) reprojection | mp.dps=80 | Group projection (algebraic exactness) |
| Action evaluation | mp.dps=80 | Physical decision |
| Banach solver | mp.dps=80 | Gap stability |
| Observables | adaptive | Error control |

---

## Key Benchmark Metric

The primary efficiency metric is NOT acceptance rate. It is:

**τ_Q^{hybrid} / τ_Q^{HMC}**

Target: < 0.1

This measures the reduction in topological autocorrelation time, which is
the only physically meaningful indicator of whether the TN-guided proposal
engine overcomes topological freezing.

---

## Realistic Assessment

| Architecture | Realistic Chance |
|-------------|-----------------|
| TN as full solver | Low |
| TN as proposal accelerator | Moderate |
| TN+HMC topology mitigation | Plausible |
| TN replacing lattice MC | Unrealistic |

The fundamental challenge is the entanglement volume law in 4D non-abelian
gauge theories. MPS/PEPS methods excel in 1D and some 2D systems but face
exponential scaling in 4D SU(3). The TN-as-proposal strategy sidesteps this
by not requiring the TN to represent the full quantum state.

---

## References

- Luscher, M. (2010). JHEP 08, 071. arXiv:1006.4518
- Luscher, M. (2010). Comm. Math. Phys. 293, 899-919.
- Duane, S. et al. (1987). Phys. Lett. B 195, 216.
- Boyda, D. et al. (2021). Phys. Rev. D 103, 014506. arXiv:2008.05456
- Kanwar, G. et al. (2020). Phys. Rev. Lett. 125, 121601. arXiv:2003.06413
