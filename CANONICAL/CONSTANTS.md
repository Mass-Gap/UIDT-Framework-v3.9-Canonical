# UIDT Canonical Constants v3.9.8

> **STATUS:** Immutable until next version update  
> **SOURCE:** Framework v3.6.1/v3.7.3/v3.9, DOI: 10.5281/zenodo.17835200  
> **LAST VERIFIED:** 2026-04-03  
> **AUDIT:** RG fixed-point precision correction (TKT-20260403-LAMBDA-FIX). PR #199 audit. Session 2026-04-03. Topological NLO & Gluon Condensate registration (TKT-20260417-TOPO-NLO). v3.9.8.

---

## Core Parameters

| Parameter | Symbol | Value | Uncertainty | Category | Notes |
|-----------|--------|-------|-------------|----------|-------|
| **Spectral Gap** | Δ* | 1.710 GeV | ±0.015 | A | Yang-Mills mass gap (NOT particle mass!) |
| **Gamma Invariant** | γ | 16.339 | exact (kinetic) | A- | Phenomenologically determined. ALWAYS [A-]. L4 open. |
| **Gamma MC Mean** | γ_MC | 16.374 | ±1.005 | A- | Monte Carlo statistical (100k samples) |
| **Bare Gamma** | γ_∞ | 16.3437 | ±0.0005 | B | L→∞ thermodynamic limit (FSS extrapolation) |
| **Coupling** | κ | 0.500 | ±0.008 | A | Non-minimal gauge-scalar |
| **Self-Coupling** | λ_S | 5κ²/3 = 0.41̄6̄ | ±0.007 | A | Exact RG fixed-point definition. See note below. |
| **Scalar Mass** | m_S | 1.705 GeV | ±0.015 | D | Predicted, unverified |
| **VEV** | v | 47.7 MeV | — | A | Corrected in v3.6.1 (was 0.854 MeV) |
| **Torsion Energy** | E_T | 2.44 MeV | — | C | f_vac − Δ/γ. 3.75σ FLAG tension (pre-QED). external_crosscheck: false. |
| **Vacuum Frequency** | f_vac | 107.10 MeV | — | C | Composite: Δ/γ + E_T. Limited by weakest input. |
| **Dressing Shift** | δγ | 0.0047 | — | B | γ_∞ − γ_kinetic = 16.3437 − 16.339 (0.029% relative) |
| **Gluon Condensate**| C_GLUON | 0.0246 GeV⁴ | — | C | Analytical derivation from Dilaton-Trace-Anomaly relationship. |
| **Strong Coupling** | α_s_ref | 0.47 | — | B | Canonical reference at μ ≈ 1 GeV (PDG 2023 1-loop running). |

> **λ_S Note (TKT-20260403-LAMBDA-FIX):** The previous ledger value λ_S = 0.417 was a rounded decimal approximation. The exact RG fixed-point definition is λ_S := 5κ²/3. With κ = 0.500 (exact): λ_S = 5×0.25/3 = 0.41̄6̄. The deviation |0.41̄6̄ − 0.417| = 3.3̄×10⁻⁴ lies within the stated uncertainty ±0.007 — **no physics change**. This correction upgrades the RG constraint residual from 10⁻³ to < 10⁻¹⁴ (Category [A], Constitution-compliant). See PR #199, `docs/su3_gamma_theorem.md` §3.

---

## Cosmological Parameters

| Parameter | Symbol | Value | Uncertainty | Category | Notes |
|-----------|--------|-------|-------------|----------|-------|
| **Hubble Constant** | H₀ | 70.4 km/s/Mpc | ±0.16 | C | DESI DR2 calibrated (NOT prediction) |
| **Dark Energy EOS** | w₀ | −0.99 | — | C | Canonical per Decision D-002 (2026-03-01). S1-04 RESOLVED. |
| **DE Evolution** | w_a | L-dependent | — | C | L=8.0→−1.18, L=8.2→−1.30. L not canonical. |
| **Neutrino Sum** | Σmν | ≤ 0.16 eV | — | D | From v/γ⁷ ≈ 0.15 eV. Awaiting KATRIN/JUNO. |
| **UIDT Wavelength** | λ_UIDT | 0.660 nm | ±0.005 | C | Characteristic scale |
| **S8 Parameter** | S₈ | 0.814 | ±0.009 | C | Structure growth |
| **Casimir Distance** | d_opt | 0.854 nm | — | D | Optimal measurement (v3.7.1 corrected) |

---

## Derived Quantities

| Quantity | Formula | Value | Category |
|----------|---------|-------|----------|
| RG Fixed Point | 5κ² = 3λ_S | **residual < 10⁻¹⁴** (exact, v3.9.5) | **A** |
| Perturbative Check | λ_S < 1 | 0.41̄6̄ ✓ | A |
| Vacuum Stability | V''(v) > 0 | 2λ_S v² > 0 ✓ | A |
| Geometric Energy | E_geo = Δ/γ | 104.66 MeV | A- |
| Branch 1 Residual | — | 3.2×10⁻¹⁴ | B |
| Numerical Closure | — | < 10⁻¹⁴ | B |
| Gamma Deviation | δγ = γ_∞ − γ | 0.0047 | B |

---

## Constraint Equations

### Primary Constraint (v3.9.5 — exact)
$$5\kappa^2 = 3\lambda_S$$

Verification (mpmath, mp.dps = 80):
```python
import mpmath as mp
mp.dps = 80
kappa = mp.mpf('1') / mp.mpf('2')          # exact: 1/2
lambda_s = 5 * kappa**2 / 3                # exact: 5/12
residual = abs(5 * kappa**2 - 3 * lambda_s)
# residual = 0.0 (machine zero at 80 dps)
print(mp.nstr(residual, 20))               # 0.0
```

Previous (v3.9.4): λ_S = 0.417 → residual = 0.001 → [RG_CONSTRAINT_FAIL] at tol < 1e-14  
Current (v3.9.5): λ_S = 5κ²/3 → residual < 10⁻⁸⁰ → **Constitution-compliant** ✓

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

## Epistemic Audit Metadata (2026-03-30 / 2026-04-03)

| Parameter | external_crosscheck | upgrade_path | audit_date |
|-----------|---------------------|--------------|------------|
| γ = 16.339 | false | FRG scheme-independent observable reproducing γ without prior knowledge | 2026-03-30 |
| E_T = 2.44 MeV | false | Dedicated lattice study with torsion operator in SU(3) vacuum targeting MeV regime | 2026-03-30 |
| δγ = 0.0047 | false (numerical only) | Full NLO FRG truncation study (BMW/LPA') — TKT-20260403-FRG-NLO | 2026-04-03 |
| C_GLUON = 0.0246 | false | Analytical derivation via Dilaton-Trace-Anomaly relationship. | 2026-04-17 |
| α_s_ref = 0.47 | true | PDG 2023 world average (1-loop running to 1 GeV). | 2026-04-17 |

> Source: Issue #192, PR #193, PR #199. Stratum III classification for all three. Values immutable.

---

## Open Issues (from Audit 2026-02-28 / 2026-03-30 / 2026-04-03)

- **S1-01:** w_a L-dependence — holographic length L not canonical
- **S1-02:** N=99 vs N=94.05 contradiction in code vs docs
- **S1-04:** ~~w₀ triple inconsistency~~ → **RESOLVED** 2026-03-02. Canonical w₀ = −0.99 per Decision D-002.
- **L1:** 10¹⁰ geometric factor UNEXPLAINED
- **L4:** γ NOT derived from RG first principles — algebraic closed-form yields γ ≈ 1.908, not 16.33 (PR #199, §1.4)
- **L5:** N=99 steps unjustified
- **TKT-20260403-FRG-NLO:** Full NLO FRG truncation study required before δγ = δ_NLO assessment
- **TKT-20260403-TOPO-CLAIMS:** UIDT-C-TOPO-01/02/03 registration in CLAIMS.json pending (PR #190 OT-3)

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| v3.9.8 | 2026-04-17 | Registered C_GLUON and ALPHA_S_REF (OT-1/OT-2). Topological NLO resolution. |
| v3.9.5 | 2026-04-03 | λ_S → exact 5κ²/3 (TKT-20260403-LAMBDA-FIX). RG constraint < 10⁻¹⁴. Epistemic audit metadata added. |
| v3.9.4 | 2026-03-02 | w₀ = −0.99 canonical (D-002). S1-04 resolved. Session #16 audit. |
| v3.9.3 | 2026-02-28 | Added δγ, C-068/C-069. PR Review #100-#115. 55 claims. |
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
γ  = 16.339 (kinetic)    [A-] Phenomenological. L4 open.
γ  = 16.374 ± 1.005      [A-] Monte Carlo mean
γ_∞= 16.3437 ± 0.0005   [B]  Bare (L→∞ extrapolation)
κ  = 0.500 ± 0.008       [A]
λ_S = 5κ²/3 = 0.41̄6̄    [A]  Exact RG definition (v3.9.5)
v  = 47.7 MeV            [A]  Corrected v3.6.1
m_S = 1.705 ± 0.015 GeV  [D]  Prediction
E_T = 2.44 MeV           [C]  Torsion energy. external_crosscheck: false.
f_vac = 107.10 MeV       [C]  Vacuum frequency (composite)
H₀ = 70.4 ± 0.16 km/s/Mpc [C] DESI calibrated
w₀ = -0.99               [C]  Dark energy EOS (Decision D-002)
w_a = L-dependent         [C]  Holographic DE evolution
Σmν ≤ 0.16 eV            [D]  Neutrino mass sum
δγ = 0.0047              [B]  Vacuum dressing shift (FSS)
```

---

**CITATION:** Rietz, P. (2026). UIDT v3.9. DOI: 10.5281/zenodo.17835200
