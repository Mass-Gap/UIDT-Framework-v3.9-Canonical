# UIDT Canonical Constants v3.7.3

> **STATUS:** Immutable until next version update  
> **SOURCE:** Framework v3.6.1/v3.7.3, DOI: 10.5281/zenodo.17835200  
> **LAST VERIFIED:** 2026-01-22

---

## Core Parameters

| Parameter | Symbol | Value | Uncertainty | Category | Notes |
|-----------|--------|-------|-------------|----------|-------|
| **Spectral Gap** | Δ* | 1.710 GeV | ±0.015 | A | Yang-Mills mass gap (NOT particle mass!) |
| **Gamma Invariant** | γ | 16.339 | exact (kinetic) | A- | Phenomenologically determined |
| **Gamma SU(3)** | γ_SU3 | 49/3 = 16.333... | — | B→A | SU(3) algebraic candidate for L4 resolution |
| **Gamma MC Mean** | γ_MC | 16.374 | ±1.005 | A- | Monte Carlo statistical |
| **Coupling** | κ | 0.500 | ±0.008 | A | Non-minimal gauge-scalar |
| **Self-Coupling** | λ_S | 0.417 | ±0.007 | A | Scalar self-interaction |
| **Scalar Mass** | m_S | 1.705 GeV | ±0.015 | D | Predicted, unverified |
| **VEV** | v | 47.7 MeV | — | A | Corrected in v3.6.1 (was 0.854 MeV) |

---

## Cosmological Parameters

| Parameter | Symbol | Value | Uncertainty | Category | Notes |
|-----------|--------|-------|-------------|----------|-------|
| **Hubble Constant** | H₀ | 70.4 km/s/Mpc | ±0.16 | C | DESI DR2 calibrated |
| **UIDT Wavelength** | λ_UIDT | 0.660 nm | ±0.005 | C | Characteristic scale |
| **S8 Parameter** | S₈ | 0.814 | ±0.009 | C | Structure growth |
| **Casimir Distance** | d_opt | 0.854 nm | — | D | Optimal measurement (v3.7.1 corrected) |

---

## Derived Quantities

| Quantity | Formula | Value | Category |
|----------|---------|-------|----------|
| RG Fixed Point | 5κ² = 3λ_S | 1.250 ≈ 1.251 | A |
| Perturbative Check | λ_S < 1 | 0.417 ✓ | A |
| Vacuum Stability | V''(v) > 0 | 2.907 ✓ | A |
| Branch 1 Residual | — | 3.2×10⁻¹⁴ | B |
| Numerical Closure | — | < 10⁻¹⁴ | B |

---

## Constraint Equations

### Primary Constraint
$$5\kappa^2 = 3\lambda_S$$

Verification:
```
5 × (0.500)² = 1.250
3 × (0.417) = 1.251
|Difference| = 0.001 < 0.01 → PASS
```

### Gamma Consistency
$$\gamma_{\text{kinetic}} = 16.339 \quad \text{vs} \quad \gamma_{\text{MC}} = 16.374 \pm 1.005$$

Within 1σ → **Consistent**

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| TICK-20260224 | 2026-02-24 | Phase 3 Breakthroughs (SU(3) Gamma Theorem) |
| v3.7.3 | 2026-02-14 | Cleanup: Appendix integration, SEO removal, falsification IDs |
| v3.7.2 | 2025-12-20 | Previous canonical, VEV=47.7 MeV, H₀=70.4 |
| v3.6.1 | 2025-11-15 | VEV correction patch |
| v3.3 | 2025-09-XX | **WITHDRAWN** (formatting errors) |
| v3.2 | 2025-08-XX | Technical Note baseline |

---

## Quick Copy Block

```
Δ* = 1.710 ± 0.015 GeV   [A]  Spectral gap (NOT mass!)
γ  = 16.339 (exact)      [A-] Kinetic VEV derivation
γ_SU3 = 49/3 = 16.333    [B→A] SU(3) algebraic candidate
γ  = 16.374 ± 1.005      [A-] Monte Carlo mean
κ  = 0.500 ± 0.008       [A]
λ_S = 0.417 ± 0.007      [A]
v  = 47.7 MeV            [A]  Corrected v3.6.1
m_S = 1.705 ± 0.015 GeV  [D]  Prediction
H₀ = 70.4 ± 0.16 km/s/Mpc [C] DESI calibrated
```

---

**CITATION:** Rietz, P. (2026). UIDT v3.7.3. DOI: 10.5281/zenodo.17835200
