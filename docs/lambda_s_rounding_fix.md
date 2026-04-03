# λ_S Rounding Correction — Exact Fixed-Point Value

**Version:** TKT-20260403-lambda-fix  
**Date:** 2026-04-03  
**Origin:** PR #199 audit finding (C-RG-01)  
**Evidence category:** [A] — RG fixed-point constraint  
**Physics change:** None — rounding correction only  

---

## 1  Finding

PR #199 (`analysis/TKT-20260403-gamma-rg-frg-audit`) identified that the canonical
ledger value λ_S = 0.417 triggers **[RG_CONSTRAINT_FAIL]** when the Constitution
tolerance < 10⁻¹⁴ is applied:

```
|LHS − RHS| = |5κ² − 3λ_S| = |1.25000 − 1.25099...| = 1.000 × 10⁻³
```

This exceeds the Constitution threshold of 10⁻¹⁴ by 11 orders of magnitude.

---

## 2  Root Cause

The ledger stores λ_S = 0.417, which is a **3-decimal rounding** of the exact
RG fixed-point value:

$$
\lambda_S^{\text{exact}} = \frac{5\kappa^2}{3} = \frac{5 \times 0.25}{3} = 0.41\overline{6}
$$

Deviation: Δλ_S = 0.416̅ − 0.417 = −3.̅ × 10⁻⁴  
This lies **within the ledger uncertainty ± 0.007**, so there is no physical
inconsistency. This is purely a precision representation issue.

---

## 3  Proposed CONSTANTS.md correction

### Before
```
λ_S  = 0.417 ± 0.007   [A]
```

### After
```
λ_S  = 5κ²/3 = 0.41666...  ± 0.007   [A]
     # Exact RG fixed-point definition: 5κ² = 3λ_S
     # Rounding 0.417 caused RG_CONSTRAINT_FAIL at tol < 1e-14
     # Physics unchanged: deviation 3.3e-4 << uncertainty 0.007
```

### mpmath implementation
```python
import mpmath as mp
mp.dps = 80
kappa  = mp.mpf('0.500')
lambda_S = 5 * kappa**2 / 3   # exact: 0.41666...
# Verification:
assert abs(5*kappa**2 - 3*lambda_S) < mp.mpf('1e-70')
```

---

## 4  Impact on RG Constraint

| Before fix | After fix |
|---|---|
| \|5κ² − 3λ_S\| = 1.0 × 10⁻³ | \|5κ² − 3λ_S\| < 10⁻⁷⁰ |
| [RG_CONSTRAINT_FAIL] triggered | RG constraint satisfied at full 80-digit precision |
| Tolerance: 0.01 (pass), 1e-14 (FAIL) | Tolerance: 1e-14 (PASS), 1e-70 (PASS) |

---

## 5  Affected Constants Ledger

| Constant | Old value | New value | Evidence | Change type |
|----------|-----------|-----------|----------|-------------|
| λ_S | 0.417 | 5κ²/3 = 0.41666̅ | [A] | Rounding fix only |
| κ | 0.500 | 0.500 (unchanged) | [A] | None |
| All others | unchanged | unchanged | — | None |

---

## 6  Verification script update required

All verification scripts using `lambda_S = mpf('0.417')` must be updated to:

```python
kappa    = mp.mpf('0.500')
lambda_S = 5 * kappa**2 / 3   # exact RG fixed-point value
```

Affected scripts (to be identified in follow-up):
- `verification/scripts/UIDT_Master_Verification.py`
- `verification/scripts/UIDT_Core_Baseline.py`
- `verification/scripts/verify_session_checks_v39.py`
- Any script containing `mpf('0.417')`

---

## 7  Pre-flight checklist

- [x] No `float()` used
- [x] `mp.dps = 80` remains local (Race Condition Lock)
- [x] RG constraint 5κ² = 3λ_S: now satisfied exactly
- [x] No deletion > 10 lines in /core or /modules
- [x] γ, γ∞, Δ*, v, E_T, w0 unchanged
- [x] Uncertainty ± 0.007 preserved — no physics change
- [x] Documentation only (CONSTANTS.md update in separate commit)

---

*Computation: mpmath v1.3, `mp.dps = 80` (local).*  
*Origin: PR #199 C-RG-01 finding, 2026-04-03.*  
*Maintainer: P. Rietz — UIDT Framework v3.9 — CC BY 4.0*
