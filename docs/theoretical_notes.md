# Theoretical Notes & Methodology

## Parameter Precision Guardrails

**Evidence Category B (Constructive Safeguard)**
[cite: 2026-02-22]

To ensure mathematical determinism and prevent Python float degradation before intensive numerical operations, all scalar simulation parameters in v3.6.1 are now protected by **80-digit mpmath initialization**.

The following constants in `simulation/` scripts (specifically `UIDTv3_6_1_HMC_Real.py`) are instantiated as high-precision `mp.mpf` objects:
- `TARGET_DELTA` = `1.710035046742` (Exact Geometric Operator value)
- `TARGET_GAMMA` = `16.339` (Canonical)
- `KAPPA`, `LAMBDA_S`, `M_S`, `GLUON_CONDENSATE`

This "Precision Guardrail" ensures that the initial conditions of the HMC evolution are bit-exact across platforms, before they are inevitably cast to standard floating-point precision for GPU/numpy acceleration. This hybrid approach balances **Epistemic Integrity** (at initialization) with **Computational Performance** (during execution).
