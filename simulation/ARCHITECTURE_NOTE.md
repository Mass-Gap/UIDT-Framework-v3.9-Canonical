# UIDT Framework: Architecture Note
**Context:** GPU-Trigger Simulation Parity (Task 23)
**Date:** 2026-04-18
**Status:** Code-Health Document

## 1. PRECISION ARCHITECTURE (Dual-Layer)
The UIDT HMC simulation correctly employs a dual-layer precision architecture. This separation is NOT a defect, but the correct structural approach:

*   **HMC Evolution Steps:** The Markov-Chain Monte Carlo (MCMC) evolution steps are computed using `float64` / `complex128` precision via NumPy. This is the standard in the Lattice-QCD community. Because the HMC process is inherently stochastic, a precision of 80 digits during gauge field evolution is physically meaningless.
*   **Observable Extraction:** The final extraction of deterministic UIDT observables (e.g., Δ*, γ, E_T, v, w_0) requires absolute precision to guarantee closure. This step strictly enforces `mp.dps=80` via `mpmath`, fulfilling the deterministic requirements of the UIDT Constitution.

## 2. IDENTIFIED BOTTLENECKS (From Task 23)
The following technical bottlenecks have been identified in the canonical simulation script (`simulation/UIDTv3_6_1_HMC_Real.py`) regarding potential GPU execution:

*   **`np.roll` Memory Overhead:** The use of `np.roll` is not in-place and generates O(N) memory overhead by creating tensor copies. In a GPU pipeline, stencil-indexing is vastly preferred.
*   **`scipy.linalg.expm`:** This relies on Padé-Approximation on `float64`. While perfectly sufficient for the HMC gauge evolution (where coefficients |a_i| << 1), it is not equivalent to mpmath precision (which is intentionally not used here).
*   **Python `for`-Loops:** The use of Python-level loops via `np.ndindex` is fundamentally incompatible with GPU-dispatch architectures due to the Python GIL and loop overhead.
*   **SVD/QR on 3x3 Matrices:** Standard implementations of SVD/QR decompositions on small 3x3 SU(3) matrices are highly inefficient on GPUs.

## 3. GPU-PORTATION PATH (Recommendation Only)
For future development, migrating the HMC core to GPU hardware is technically feasible and recommended under the following parameters:

*   **`float64` GPU via CuPy/PyTorch/JAX:** The HMC core can be ported using `float64` precision. This is NOT a "precision loss", but the correct domain for stochastic lattice methods.
*   **CPU-Only `mp.dps=80` Post-Processing:** The `mpmath` extraction of observables remains strictly CPU-bound and occurs only after the GPU-accelerated HMC generation is complete.
*   **CGBN (Arbitrary Precision GPU Library):** Listed as a potential alternative for specialized high-precision GPU tasks, but not required for standard HMC.

## 4. INCOMMENSURABILITY (Clarification)
**UIDT HMC vs. LHCb Allen GPU Trigger**
Any direct benchmark or "parity comparison" between the UIDT HMC simulation and the LHCb Run 3 Allen GPU trigger is categorically invalid:

*   **LHCb Run 3 Allen:** A real-time 30-MHz event selection and track reconstruction pipeline optimized for pattern matching in live proton-proton collisions.
*   **UIDT HMC:** An offline Lattice-QCD Markov Chain algorithm simulating the vacuum path integral over hours or days.

These two systems are incommensurable. A parity benchmark between them is conceptually flawed and will not be pursued.
