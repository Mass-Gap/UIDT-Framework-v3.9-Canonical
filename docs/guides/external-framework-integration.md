# External Framework Integration Strategy

**Repository**: Mass-Gap/UIDT-Framework-v3.9-Canonical
**External framework**: [cblab/raumzeit](https://github.com/cblab/raumzeit)
**Repository ID**: 1207002944
**DOI**: 10.5281/zenodo.17835200
**Date**: 2026-04-19
**Status**: Active

---

## Overview

The UIDT v3.9 framework predicts the Yang-Mills mass gap and related
physical constants from vacuum information density as a fundamental
geometric scalar.  The cblab/raumzeit framework independently simulates
emergent geometry in growing causal graphs using purely local edge rules.

This document defines three integration paths to test whether UIDT
predictions emerge naturally from causal-set dynamics.

---

## Path A: Spectral Gap Direct Search  ✅ ACTIVE

**Target constant**: Δ\* = 1.710 ± 0.015 GeV  [A]

**Observable**: `g_fc = ds(front) - ds(core)` from K7 fixed-anchor measurements.

**Rationale**: The spectral dimension gap between the outer and inner
shells of a BFS region measures how strongly geometry differentiates
between short-range and long-range structure.  If the vacuum information
density hypothesis is correct, this gap should reflect the fundamental
spectral gap of the theory.

**Implementation**: `verification/scripts/hybrid_uidt_raumzeit_spectral_gap.py`

**Evidence target**: [E] (Speculative — no dimensional bridge to GeV scale)

**Status**: Implemented in this PR.

---

## Path B: Vacuum Information Density as Ball Coherence  ⏳ FUTURE

**Target constant**: γ = 16.339  [A-]

**Observable**: V9 ball coherence sector-balance ratio.

**Rationale**: The V9 term in raumzeit rewards edges that enhance sphere
shell balance across multiple radii.  The `sector_balance_gain()` function
distributes influence across first-branch sectors.  If the UIDT γ invariant
is a universal geometric property, the equilibrium sector-balance ratio
should converge to ≈ 16.339 in the large-N limit.

**Key function**: `v9_ball_coherence_term()` (archive/reference-monolith)

**Evidence target**: [E] (Speculative — convergence test, no bridge equation)

**Status**: Design phase.  Requires:
1. Extracting sector-balance statistics from batch runs
2. Testing convergence across N = [500, 1000, 2000, 5000]
3. Comparing against γ = 16.339 with uncertainty quantification

---

## Path C: Torsion Binding Energy from Layer Profiles  ⏳ FUTURE

**Target constant**: E\_T = 2.44 MeV  [C]

**Observable**: `log₂(peak_layer_ratio)` from K5/K7 layer-profile diagnostics.

**Rationale**: Layer profiles measure the internal depth distribution of
causal intervals.  The ratio `peak_layer_size / occupied_layers` encodes
the structural binding of the lattice.  If the UIDT torsion binding
hypothesis is correct, `log₂(ratio) ≈ log₂(2.44) ≈ 1.28`.

**Key function**: Layer-profile computation from `causal-set-engine/
src/causal_set_engine/observables/cst/layer_profiles.py`

**Evidence target**: [C] (Scenario-dependent)

**Status**: Conceptual.  Requires:
1. Implementing layer-profile extraction in batch post-processing
2. Statistical analysis of binding signatures across configs
3. Comparison with E\_T = 2.44 MeV proxy

---

## Risk Assessment

| Path | Risk | Key Uncertainty | Contingency |
|------|------|-----------------|-------------|
| A | 🟢 LOW | g\_fc mapping to energy scale | Paths B, C viable alternatives |
| B | 🟡 MEDIUM | V9 equilibrium convergence at finite N | Increase N; alternative balance metrics |
| C | 🟡 MEDIUM | Layer-profile stability across configs | Test multiple baseline/v8a/v9a configs |

---

## Timeline

| Phase | Timeline | Deliverable |
|-------|----------|-------------|
| 1 — Merge & Activate | Week 1 | Path A script merged; CI test added |
| 2 — First Batch Test | Week 2–3 | Run v9a\_fast batch; validate g\_fc clustering |
| 3 — Path B Design | Week 4–5 | Sector-balance extraction; γ convergence test |
| 4 — Path C Design | Week 6–7 | Layer-profile binding analysis |
| 5 — Unification | Week 8+ | Unified hybrid verifier; evidence package |

---

## Quality Gate Compliance

- [x] Parameter consistency (Rule 03): all constants read-only
- [x] Evidence integrity (Rule 02): claims tagged with categories
- [x] Numerical rigor (Rule 04): no mocking; real measurements
- [x] Anti-tampering (Rule 05): additive only
- [x] Language (Rule 08): professional academic English
- [x] DOI (Rule 14): 10.5281/zenodo.17835200
- [x] External reference immutability: cblab/raumzeit pinned
- [x] Strata separation (Rule 14): math ≠ interpretation

---

*Maintainer: P. Rietz — DOI: 10.5281/zenodo.17835200*
