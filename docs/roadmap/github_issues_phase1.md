# Phase 1: Core Stabilization (March - May 2026)

This phase focuses on stabilizing the core documentation and ensuring absolute clarity on limitations and scope.

## Issue #1: Restructure README into Three-Layer Architecture
- **Priority:** CRITICAL
- **Deadline:** 2026-03-15
- **Branch:** `feature/three-layer-readme`
- **Description:**
  The current README mixes core mathematical results with phenomenological extensions. We must restructure it into three distinct layers:
  1.  **Layer 1 (Core Math):** Banach Fixed Point, Spectral Gap $\Delta^*$, Pure YM. [Category A]
  2.  **Layer 2 (Phenomenology):** $\gamma$ scaling, hadron spectrum, calibrated parameters. [Category A-/C]
  3.  **Layer 3 (Speculation):** Cosmology, Dark Energy, predictions. [Category C/D]
  Each layer must have distinct headers and evidence warnings.

## Issue #2: Integrate v3.7.1 Erratum into v3.9 main text
- **Priority:** HIGH
- **Deadline:** 2026-03-20
- **Description:**
  The v3.7.1 Erratum clarifies that $\Delta^* = 1.710$ GeV is the spectral gap of **Pure SU(3) Yang-Mills**, not the observable particle mass in full QCD with quarks. This distinction is crucial to avoid conflict with Lattice QCD results for full QCD. This clarification must be integrated into the main text of the manuscript and the README.

## Issue #3: Expand Known Limitations Table
- **Priority:** MEDIUM
- **Deadline:** 2026-03-25
- **Description:**
  Expand the "Known Limitations" table in `README.md` and `LIMITATIONS.md`. It must appear **before** any claims of success or the Falsification Matrix.
  Required entries:
  - L1: 10^10 Geometric Hierarchy (Unexplained).
  - L2: Electron Mass Discrepancy (23%).
  - L3: Vacuum Energy Residual (Factor 2.3).
  - L4: $\gamma$ Scaling (Calibrated, not derived).
  - L5: N=99 Steps (Empirical).
  - L6: Glueball Retraction (UIDT-C-015).
