# UIDT Canonical Constants v3.9.0

> **STATUS:** Immutable until next version update  
> **SOURCE:** Framework v3.6.1/v3.7.3/v3.9, DOI: 10.5281/zenodo.17835200  
> **LAST VERIFIED:** 2026-02-28  
> **AUDIT:** Retroactive PR #1–#99 audit completed 2026-02-28

---

## Core Parameters

| Parameter | Symbol | Value | Uncertainty | Category | Notes |
|-----------|--------|-------|-------------|----------|-------|
| **Spectral Gap** | Δ* | 1.710 GeV | ±0.015 | A | Yang-Mills mass gap (NOT particle mass!) |
| **Gamma Invariant** | γ | 16.339 | exact (kinetic) | A- | Phenomenologically determined. ALWAYS [A-]. |
| **Gamma MC Mean** | γ_MC | 16.374 | ±1.005 | A- | Monte Carlo statistical (100k samples) |
| **Bare Gamma** | γ_∞ | 16.3437 | ±0.0005 | B | L→∞ thermodynamic limit (FSS extrapolation) |
| **Coupling** | κ | 0.500 | ±0.008 | A | Non-minimal gauge-scalar |
| **Self-Coupling** | λ_S | 0.417 | ±0.007 | A | Scalar self-interaction |
| **Scalar Mass** | m_S | 1.705 GeV | ±0.015 | D | Predicted, unverified |
| **VEV** | v | 47.7 MeV | — | A | Corrected in v3.6.1 (was 0.854 MeV) |
| **Torsion Energy** | E_T | 2.44 MeV | — | D | f_vac − Δ/γ. 3.75σ FLAG tension (pre-QED) |
| **Vacuum Frequency** | f_vac | 107.10 MeV | — | C | Composite: Δ/γ + E_T. Limited by weakest input. |

---

## Cosmological Parameters

| Parameter | Symbol | Value | Uncertainty | Category | Notes |
|-----------|--------|-------|-------------|----------|-------|
| **Hubble Constant** | H₀ | 70.4 km/s/Mpc | ±0.16 | C | DESI DR2 calibrated (NOT prediction) |
| **Dark Energy EOS** | w₀ | −0.99 | — | C | Canonical dark energy baseline (calibrated). |
| **Holographic L** | L | 8.2 | ±0.1 | C | Effective holographic length (calibrated). |
| **DE Evolution** | w_a | −1.30 | — | C | Calibrated at L=8.2 (cosmology maximum Category C). |
| **Neutrino Sum** | Σmν | ≤ 0.16 eV | — | D | From v/γ⁷ ≈ 0.15 eV. Awaiting KATRIN/JUNO. |
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
| Geometric Energy | E_geo = Δ/γ | 104.66 MeV | A- |
| Branch 1 Residual | — | 3.2×10⁻¹⁴ | B |
| Numerical Closure | — | < 10⁻¹⁴ | B |
| Gamma Deviation | δγ = γ_∞ − γ | 0.0047 | B |
| Relative Geometric Shift | δ = δγ/γ_∞ | 2.8757 × 10⁻⁴ | B |

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

### Gamma Bare vs Dressed
$$\gamma_{\infty} = 16.3437 \quad \text{vs} \quad \gamma_{\text{kinetic}} = 16.339$$

Deviation δγ ≈ 0.0047 (0.029%) — finite-size effect.

---

## Evidence Category Rules (Quick Reference)

```
[A]  Analytically proven    < 10⁻¹⁴ residuals    NEVER for cosmology
[A-] Phenomenological       Calibrated             γ ALWAYS here
[B]  Numerically verified   z < 1σ                 NEVER for cosmology
[C]  Calibrated to data     Fitted                 MAX for cosmology
[D]  Predictive             Unverified             MUST have falsification
[E]  Speculative/withdrawn  N/A                    Mark clearly

Non-existent: [A+], [B+], [C+], [D+]
```

---

## Open Issues (from Audit 2026-02-28)

- **L1:** 10¹⁰ geometric factor UNEXPLAINED
- **L4:** γ NOT derived from RG
- **L5:** N=94.05 steps unjustified (baseline adopted; derivation open)

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| v3.9.0 | 2026-02-28 | Added γ_∞, E_T, f_vac, w_a, Σmν. Audit PRs #1-#99. 53 claims. |
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
γ  = 16.374 ± 1.005      [A-] Monte Carlo mean
γ_∞= 16.3437 ± 0.0005   [B]  Bare (L→∞ extrapolation)
κ  = 0.500 ± 0.008       [A]
λ_S = 0.417 ± 0.007      [A]
v  = 47.7 MeV            [A]  Corrected v3.6.1
m_S = 1.705 ± 0.015 GeV  [D]  Prediction
E_T = 2.44 MeV           [D]  Torsion energy (3.75σ FLAG)
f_vac = 107.10 MeV       [C]  Vacuum frequency (composite)
H₀ = 70.4 ± 0.16 km/s/Mpc [C] DESI calibrated
w₀ = -0.99               [C]  Dark energy EOS
L   = 8.2 ± 0.1           [C]  Holographic length
w_a = -1.30               [C]  Holographic DE evolution (at L=8.2)
Σmν ≤ 0.16 eV            [D]  Neutrino mass sum
```

---

**CITATION:** Rietz, P. (2026). UIDT v3.9. DOI: 10.5281/zenodo.17835200
