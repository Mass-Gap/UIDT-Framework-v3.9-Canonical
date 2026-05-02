# UIDT v3.9 Core Baseline Verification Protocol

## Scope
Mathematical Core (Category A) only. No peripheral modules.

## Canonical Constants
- Mass Gap: Δ = 1.710035... GeV
- RG Constraint: 5κ² = 3λ_S
- Lipschitz: L < 1

## One-Command Reproduction
```bash
python verification/scripts/UIDT_Core_Baseline.py
```

### Expected Output
```text
[1] BANACH FIXED-POINT PROOF (Mass Gap)...
   > Δ* = 1.710035046742213182... GeV
   > Lipschitz L = 0.00003749... (< 1: ✅ CONTRACTION)

[2] RG CONSTRAINT CLOSURE (Proposition 5.5)...
   > Residual: 0.0
   > Status: ✅ CLOSED

[3] GEOMETRIC OPERATOR PRECISION (80-digit audit)...
   > Residual at n=1089: 2.1e-81
   > Status: ✅ STABLE

==================================================================
CORE BASELINE STATUS: ✅ PASSED
==================================================================
```

## Acceptance Criteria
1. All residuals < 1e-14
2. Lipschitz constant < 1
3. No runtime errors

## Evidence Category
[A] Mathematical Self-Consistency
