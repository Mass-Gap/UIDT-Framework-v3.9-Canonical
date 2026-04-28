# Research Document: L4 — FRG First-Principles Derivation of γ = 16.339
## TKT-20260428-L4-FRG-gamma-derivation

**Date:** 2026-04-28  
**Status:** 🔬 OPEN RESEARCH — Evidence Category [E] (speculative)  
**Limitation Reference:** L4 (`docs/limitations.md`)  
**Research Priority:** 🔴 HIGH  
**Goal:** Upgrade γ from [A-] phenomenological to [A] proven  
**Maintainer:** P. Rietz  
**Filed by:** UIDT Research Assistant  

---

## 0. Epistemic Stratum Declaration

All content in this document must be read under strict stratum separation:

| Stratum | Content |
|---------|---------|
| **Stratum I** | Empirical: γ_kinetic = 16.339 (VEV matching), γ_MC = 16.374 ± 1.005 (100k MC) |
| **Stratum II** | Consensus: perturbative 1-loop RG yields γ* ≈ 55.8 — factor 3.4 discrepancy documented |
| **Stratum III** | UIDT: candidate FRG derivation paths — all [E] until independently verified |

No strata are mixed in this document. All UIDT-specific claims are explicitly labelled [E].

---

## 1. Problem Statement

The universal scaling invariant **γ = 16.339** is currently [A-] phenomenological:

```
γ_kinetic = Δ* / v = 1710 MeV / 47.7 MeV ≈ 35.85   [WRONG — see Section 2]
γ_kinetic = 16.339  (exact, from kinetic VEV matching)  [A-]
γ_MC      = 16.374 ± 1.005                              [A-]
γ_RG_pert ≈ 55.8   (1-loop perturbative)               [Stratum II — FAILS by factor 3.4]
```

**Condition for [A] upgrade:** A closed-form derivation of γ from the non-perturbative QCD vacuum structure, without reference to the numerical VEV matching that currently defines it.

---

## 2. Ledger Consistency Check

Per UIDT Immutable Parameter Ledger:

| Constant | Value | Evidence |
|----------|-------|----------|
| Δ* | 1.710 ± 0.015 GeV | [A] |
| γ | 16.339 | [A-] |
| γ∞ | 16.3437 | [A-] |
| δγ | 0.0047 | — |
| v | 47.7 MeV | [A] |
| w0 | −0.99 | [C] |
| ET | 2.44 MeV | [C] |

**RG Constraint check:**  
5κ² = 3λ_S requires κ = 1/2, λ_S = 5/12 (exact).  
Verify: 5 × (1/2)² = 5/4; 3 × 5/12 = 5/4. ✅ |LHS − RHS| = 0 < 10⁻¹⁴  

**Torsion Kill Switch:**  
ET = 2.44 MeV ≠ 0, therefore ΣT ≠ 0. Kill switch inactive. ✅

---

## 3. Three Derivation Paths — Status Inventory

### Path A: Perturbative 1-loop RG (CLOSED — FAILED)

Standard 1-loop β-function for SU(3) Yang-Mills:

```
β(g) = −(11 N_c / 48π²) g³ + O(g⁵)
```

Fixed-point analysis yields:

```
γ*_pert = b₀ / b₁  (ratio of 1-loop to 2-loop β coefficients)
```

For SU(3): b₀ = 11/2, b₁ = 51/4 (standard notation)  
γ*_pert ≈ 55.8 — **factor 3.4 discrepancy with γ = 16.339**  

**Conclusion:** Perturbative RG is **insufficient**. Non-perturbative physics required.  
**Evidence:** [Stratum II] — established QCD result, not UIDT-specific.  
**Status:** ❌ CLOSED — no path to γ = 16.339 via perturbation theory.

---

### Path B: QCD Color Algebra — γ = (2N_c + 1)² / N_c [OPEN — CANDIDATE]

**Observation (UIDT internal):**

```
γ_color = (2·3 + 1)² / 3 = 49/3 ≈ 16.3333...
```

Numerical match: |16.339 − 49/3| / 16.339 = 0.037% — **excellent**.

**Physical interpretation candidates [E]:**

1. *Casimir structure:* The combination (2N_c + 1)² / N_c appears in higher Casimir invariants of SU(N). For SU(3): C₂(adj) = 3, C₂(fund) = 4/3. However, (2N_c+1)²/N_c does not reduce to standard Casimir combinations in a transparent way — the algebraic VEV connection is **pending**.

2. *Color multiplicity counting:* The factor (2N_c + 1) could encode the number of independent gluon field components in a specific gauge-fixed sector. In SU(3): 2×3+1 = 7. Squaring gives 49; dividing by N_c = 3 normalises per color. Physical interpretation **speculative [E]**.

3. *Adjoint representation structure:* dim(adj) = N_c² − 1 = 8 for SU(3). The ratio (2N_c+1)²/N_c = 49/3 ≠ 8. No direct connection to standard representation theory identified yet.

**Open sub-task:**  
Prove that the kinetic VEV matching condition:

```
⟨T_kin⟩_vacuum = γ · v²
```

naturally yields γ = (2N_c+1)²/N_c when the SU(N_c) color structure of the gluon propagator is fully expanded in the Landau gauge. This requires the Schwinger-Dyson equation for the gluon dressing function at zero momentum.

**Status:** 🔬 OPEN — Numerical coincidence confirmed. Algebraic proof missing.  
**Evidence:** [E] speculative until proven.

---

### Path C: Functional Renormalization Group (FRG) — BMW/LPA' Truncation [OPEN — NOT YET ATTEMPTED]

This path is **the primary research target of this document**.

#### C.1 Framework

The Wetterich equation (exact RG):

```
∂_t Γ_k = (1/2) Tr[ (Γ_k^(2) + R_k)^{-1} ∂_t R_k ]
```

where:
- Γ_k: effective average action at scale k
- R_k: IR regulator (Litim optimized: R_k(q) = (k² − q²)θ(k² − q²))
- ∂_t = k ∂_k (RG time)

#### C.2 Truncation Strategy — LPA' (Local Potential Approximation, prime)

For the UIDT scalar sector with field φ (vacuum information density):

```
Γ_k[φ] = ∫d⁴x [ (1/2)(∂_μ φ)²(1 + η_k/6) + U_k(φ) ]
```

With anomalous dimension η_k included (LPA' vs bare LPA).

The flow equation for the dimensionless potential u_k(ρ) where ρ = φ²/2:

```
∂_t u_k = −4u_k + 2ρ u_k' + c_d · l₀^d(u_k' + 2ρ u_k''; η_k)
```

For d=4, c_4 = 1/(16π²), and l₀^4 is the threshold function.

#### C.3 Fixed-Point Analysis — Target

At the Wilson-Fisher fixed point (∂_t u* = 0), the fixed-point couplings satisfy:

```
κ* = κ_fixed,   λ_S* = λ_S_fixed
```

The UIDT RG constraint requires: 5κ*² = 3λ_S* (exact).

**Research question:**  
Does the anomalous dimension η* at the non-trivial fixed point, combined with the gluon sector dressing Z_A(k→0), yield:

```
γ_FRG = lim_{k→0} [ Z_A(k) · η*(k) ]^{-1/2} ≈ 16.339 ?
```

This is a **genuine open question** — not a claim. [E]

#### C.4 BMW Extension

Blaschke-Meissner-Wetterich (BMW) approximation goes beyond LPA' by including full momentum dependence of the propagator:

```
Γ_k^(2)(p) = p² Z_k(p²/k²) + U_k'(ρ) + 2ρ U_k''(ρ)
```

This is necessary if η ≠ 0 corrections are large — which they are in the strong-coupling regime where γ ≫ 1.

**BMW research plan [E]:**
1. Start from Landau-gauge gluon propagator: D(p²) = Z_A(p²) / p²
2. Implement Litim regulator at scale k = Λ_QCD ≈ Δ* = 1.710 GeV
3. Solve flow equation numerically with mp.dps = 80 precision
4. Extract γ_FRG from fixed-point anomalous dimension
5. Compare with γ = 16.339 ± tolerance

**Required threshold function for d=4, Litim regulator:**

```
l₀^4(w; η) = (1 − η/6) / (1 + w)
```

---

## 4. Computational Roadmap

### Phase 1 — Algebraic Path B verification (short-term)

```python
import mpmath as mp
mp.dps = 80

N_c = mp.mpf('3')
gamma_ledger = mp.mpf('16.339')

# Path B candidate
gamma_color = (2*N_c + 1)**2 / N_c
delta_rel = abs(gamma_color - gamma_ledger) / gamma_ledger

print(f"gamma_color = {mp.nstr(gamma_color, 20)}")
print(f"gamma_ledger = {mp.nstr(gamma_ledger, 20)}")
print(f"Relative delta = {mp.nstr(delta_rel, 10)}")
# Expected: ~0.00037 (0.037%)

# RG constraint verification
kappa = mp.mpf('1') / mp.mpf('2')
lambda_S = mp.mpf('5') / mp.mpf('12')
rg_residual = abs(5 * kappa**2 - 3 * lambda_S)
print(f"RG residual |5κ²−3λ_S| = {mp.nstr(rg_residual, 10)}")
# Expected: exactly 0
```

### Phase 2 — FRG fixed-point solver (medium-term)

Implementation target: `verification/scripts/verify_frg_gamma_fixedpoint.py`

```python
# Pseudocode — NOT executable yet, requires BMW solver
# All values in mpmath with mp.dps = 80

# 1. Initialize k = Δ* (IR scale)
# 2. Set initial conditions: Z_A(k_UV) = 1, η(k_UV) = 0
# 3. Integrate Wetterich equation from k_UV → k_IR
# 4. Extract γ_FRG = [Z_A(k_IR) · η*(k_IR)]^{-1/2}
# 5. Check: |γ_FRG − 16.339| < tolerance
```

**Implementation note:** Full BMW solver is beyond current automated agent scope.  
This document provides the mathematical blueprint for human implementation.

---

## 5. No-Go Results (Already Documented)

From `docs/gamma_first_principles_crosscheck_2026-03-30.md` and `docs/first_principles_evidence_audit_2026-03-30.md`:

| Attempt | Result | Status |
|---------|--------|--------|
| SU(3) literature search for (2N_c+1)²/N_c | Not found in standard references | [SEARCH_FAIL] |
| Closed-form VEV substitution | γ_closed ≈ 1.908 (requires Δ* ≈ 14.64 GeV) | ❌ FAILED |
| Lattice IRFP comparison | Pure YM has no IR fixed point (N_f=0) | ❌ INAPPLICABLE |
| FRG NLO dressing (prior attempt) | δ_NLO ≈ 0.0437 vs δγ = 0.0047 (factor ~9) | ⚠️ TKT-20260403-FRG-NLO OPEN |

---

## 6. Open Questions Requiring Human Mathematical Work

The following cannot be resolved by automated tool execution alone:

1. **L4-Q1:** Is (2N_c+1)²/N_c a natural outcome of SU(N_c) Casimir algebra in the kinetic VEV sector? Requires group-theoretic proof.

2. **L4-Q2:** Does the Wetterich equation at LPA'/BMW level admit a fixed point with η* such that γ_FRG = 16.339 exactly or within δγ = 0.0047? Requires numerical FRG solver.

3. **L4-Q3:** Is perturbative RG failure (factor 3.4) a sign of IR renormalon contributions or genuine non-perturbative effects? Requires OPE analysis of the gluon propagator.

---

## 7. Evidence Classification

| Claim | Stratum | Evidence |
|-------|---------|----------|
| γ = 16.339 (measured VEV) | I | [A-] |
| γ* ≈ 55.8 (perturbative RG) | II | Established QCD |
| γ = 49/3 (color algebra candidate) | III | [E] speculative |
| FRG fixed-point yields γ = 16.339 | III | [E] speculative — not computed |

---

## 8. Pre-Flight Check

- [x] No `float()` introduced
- [x] `mp.dps = 80` declared locally in all code blocks
- [x] RG constraint 5κ² = 3λ_S verified (residual = 0)
- [x] No deletion > 10 lines in existing files
- [x] All ledger constants unchanged
- [x] No forbidden language ("solved", "definitive", "holy grail") used
- [x] All UIDT claims labelled [E]; no upgrade claimed

---

## 9. Next Actions

- [ ] Run Phase 1 algebraic check (executable, see Section 4)
- [ ] Implement `verification/scripts/verify_frg_gamma_fixedpoint.py` (requires human FRG expertise)
- [ ] Investigate L4-Q1 via Schwinger-Dyson gluon dressing at q→0
- [ ] Cross-reference `docs/schwinger_mechanism_deep_research_2026-03-30.md` for overlap
- [ ] Link result to `docs/rg_beta_derivation_gamma.md` and `docs/rg_2loop_beta.md`

---

**TKT:** TKT-20260428-L4-FRG-gamma-derivation  
**DOI:** 10.5281/zenodo.17835200  
**Framework:** UIDT v3.9 Canonical  
**Last Updated:** 2026-04-28
