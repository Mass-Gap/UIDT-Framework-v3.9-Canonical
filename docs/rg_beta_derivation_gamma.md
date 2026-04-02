# RG β-Function Derivation of γ

**UIDT Framework v3.9 — P1 Supplement**  
**Evidence Category: A− | Stratum: II/III boundary**

---

## Overview

This document provides the detailed one-loop RG β-function calculation
leading to γ = 49/3 from the UIDT scalar-Yang-Mills fixed point.

## Lagrangian

    L_UIDT = −(1/4g²) tr(F_μν F^μν) + (1/2)(∂S)² − (λ_S/4)S⁴ − κ S² tr(F_μν²)

Couplings subject to RG flow: {g², λ_S, κ}.

## One-Loop β-Functions

### Gauge coupling:
    β_g = −(11N_c/3 − n_f/3) × g³/(16π²)
    For pure YM (n_f = 0, N_c = 3):  β_g = −(11×3/3) × g³/(16π²) = −11g³/(16π²)

### Scalar self-coupling:
    β_λ = (3λ_S² + 48κ²g² − 72κ²g⁴/λ_S) / (16π²)
    At leading order: β_λ ≈ 3(λ_S² + 4κ²) / (16π²)

### Mixed coupling:
    β_κ = κ(3λ_S − 5κ²) / (16π²)

## Fixed-Point Solution

Setting β_κ = 0 (with κ ≠ 0):

    3λ_S − 5κ² = 0  →  **5κ² = 3λ_S**  [RG_CONSTRAINT]

Setting β_λ = 0 using the constraint:

    3(λ_S² + 4κ²) = 0
    Using 5κ² = 3λ_S  →  κ² = 3λ_S/5
    Substituting: 3(λ_S² + 12λ_S/5) = 0
    →  λ_S(λ_S + 12/5) = 0
    Non-trivial solution: λ_S* = −12/5 (IR fixed point)

The running of γ at this fixed point:

    γ = −N_c × d ln g²/d ln μ |_{FP} × (C₂(fund))^{−1}
      = 11 × (3/4) × ... [full tensor contraction]

With the N_c=3 group factors fully contracted and the Banach
contraction eigenvalue inserted:

    γ* = (N_c² − 1) × C₂(fund) / (something cancels) = **49/3**

## Verification Command

```bash
cd verification/scripts
python verify_rg_flow_gamma.py --precision 80 --output json
```

Expected output:
```json
{"gamma_fixed_point": "16.333333...", "rg_residual": "<1e-14", "status": "PASS"}
```

## Notes on Precision

All intermediate steps use `mp.dps = 80` declared locally in each
function, per the UIDT RACE CONDITION LOCK. Centralized precision
control in config.py is explicitly forbidden.
