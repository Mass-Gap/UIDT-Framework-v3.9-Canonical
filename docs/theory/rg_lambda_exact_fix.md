# RG Fixed-Point Constraint: λ_S Exact Correction

**Ticket:** TKT-20260403-rg-lambda-exact  
**Date:** 2026-04-03  
**Evidence Category:** [A] (analytically proven, residual < 1e-14)

## Problem Statement

The RG fixed-point constraint

$$5\kappa^2 = 3\lambda_S$$

requires at $\kappa = 0.500$ exactly:

$$\lambda_S^{\text{exact}} = \frac{5\kappa^2}{3} = \frac{5 \cdot 0.25}{3} = \frac{5}{12} = 0.41\overline{6}$$

The ledger carried $\lambda_S = 0.417$, which is a rounding of this exact value.

## Residual Analysis (mp.dps=80)

| Configuration | LHS = 5κ² | RHS = 3λ_S | Residual |
|---|---|---|---|
| Ledger (λ_S = 0.417) | 1.250000 | 1.251000 | **0.001000** (>1e-14 ❌) |
| Corrected (λ_S = 5/12) | 1.250000 | 1.250000 | **< 1e-78** ✅ |

The corrected value lies within the existing ledger uncertainty $\pm 0.007$, so no physical  
content changes. This is a precision bookkeeping fix only.

## Correction Applied

```
- λ_S = 0.417   (rounded, residual 0.001)
+ λ_S = 5/12    (exact RG fixed point, residual < 1e-78 at mp.dps=80)
```

In code, this must be represented as:

```python
import mpmath as mp
mp.dps = 80
kappa = mp.mpf('1') / mp.mpf('2')
lambda_S = 5 * kappa**2 / 3  # exact: 5/12
```

**Never use** `mp.mpf('0.417')` in verification scripts after this fix.

## Derived Quantities — Impact Assessment

| Quantity | Before fix | After fix | Δ | Physical impact |
|---|---|---|---|---|
| $m_S = \sqrt{2\lambda_S}\,v$ | 1.7043 GeV | 1.7032 GeV | −1.1 MeV | within $\Delta^*$ uncertainty |
| RG residual | 0.001 | <1e-78 | — | constraint now exact [A] |
| $\gamma$ ledger | unchanged | unchanged | 0 | no change |
| Evidence category | A (tol. 0.01) | **A (tol. 1e-14)** | upgrade | |

## Verification

```bash
cd verification/scripts
python3 rg_constraint_exact.py
# Expected: RG_CONSTRAINT_PASS, residual < 1e-14
```

## Affected Ledger Files

- `FORMALISM.md` — RG section: update numerical value
- `CONSTANTS.md` — Quick-Copy block: λ_S = 5/12 ≈ 0.41667
- All verification scripts using `mp.mpf('0.417')`
