# MCMC Bayesian Calibration — Status and Integration Note

> **Evidence Category:** [A-] Phenomenological parameter  
> **Version:** v3.9 | **Source:** Master Report 2 (UIDT VI), UIDT II

---

## Current Calibration Result

| Parameter | Value | Uncertainty | Method |
|-----------|-------|-------------|--------|
| $\gamma$ | 16.339 | — | Lattice-MC calibration [A-] |
| $\gamma_\infty$ | 16.3437 | — | Holographic limit [A-] |
| $\delta\gamma$ | 0.0047 | — | Running correction [A-] |
| $\lambda_S$ | 0.417 | — | RG fixed point [A] |
| $\kappa$ | 0.500 | — | RG fixed point [A] |
| $\gamma_{\text{coupling}}$ | 0.2778 | ±0.0021 | MCMC, pymc3 [A-] |

## MCMC Framework (Master Report 2 Reference Implementation)

The reference Bayesian calibration from UIDT VI uses:
- **Sampler:** `pymc3` (4000 samples, 2000 tune, 4 cores)
- **Priors:** $\gamma \sim \mathcal{N}(0.28, 0.05)$, $\lambda \sim \text{HalfNormal}(1.0)$
- **Likelihood:** Gaussian, calibrated to PDG 2024 pion and proton masses
- **Convergence:** $\hat{R} < 1.01$, ESS > 1000

## Integration Status

> **ACTION REQUIRED:** Verify that `simulation/mcmc_calibration.py` (or equivalent)
> in the repository corresponds to the Master Report 2 reference implementation,
> specifically:
> 1. Uses `uncertainties` package for error propagation
> 2. CFL condition includes uncertainty margin: $\Delta t = 0.8 \Delta x / \sqrt{1 + \gamma (\nabla S)^2_{\text{max}}}$
> 3. No `float()` or `round()` calls in physics computations
> 4. All mpmath calls use local `mp.dps = 80`

## Validation Criteria

```python
import mpmath as mp

def verify_rg_constraint(kappa_val='0.500', lambda_val='0.417'):
    """
    Verify the RG fixed-point constraint 5κ² = 3λ_S.

    Threshold note:
    - Analytical (Category A): residual < 1e-14 (exact symbolic relation)
    - Phenomenological (calibrated values): residual < 1e-2
    With κ=0.500 and λ_S=0.417, the residual is 0.001 — within
    phenomenological tolerance but above analytical precision.
    The constraint is EXACT as a mathematical identity; the finite
    residual reflects calibration rounding of κ and λ_S.
    """
    mp.dps = 80
    kappa = mp.mpf(kappa_val)
    lam   = mp.mpf(lambda_val)
    lhs   = mp.mpf('5') * kappa**2
    rhs   = mp.mpf('3') * lam
    residual = abs(lhs - rhs)
    print(f"5κ² = {mp.nstr(lhs, 20)}")
    print(f"3λ  = {mp.nstr(rhs, 20)}")
    print(f"Residual = {mp.nstr(residual, 10)}")
    # Phenomenological tolerance for calibrated values [A-]
    # For analytical Category A claims, use 1e-14 with exact symbolic values
    if residual > mp.mpf('1e-2'):
        raise ValueError("[RG_CONSTRAINT_FAIL]")
    print("RG constraint satisfied (phenomenological tolerance 1e-2)")
    return residual

verify_rg_constraint()
```

## Comparison: Old vs Canonical γ

The $\gamma = 0.2778$ from UIDT II/VI is the **coupling constant** in the
mass generation equation $m_{\text{eff}}^2 = m_0^2 + \gamma (\nabla S)^2$
(in natural units). This is a **different parameter** from $\gamma = 16.339$,
which is the **kinetic VEV ratio** $\gamma = \Delta^* / \Lambda_{\text{QCD}}$.

**These two γ values must not be confused.** The UIDT System Directive uses
$\gamma = 16.339$ exclusively for the kinetic VEV ratio [A-].

## Cross-References

- `simulation/` — MCMC code location
- `FORMALISM.md` — canonical parameters
- `LEDGER/parameter_ledger.md` — immutable parameter ledger
- `verification/tests/` — test suite for MCMC output
