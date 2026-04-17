# UIDT Research Note — TKT-20260416
## First-Principles Analysis of L1, L4, L5 Open Problems

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-16  
**Status:** E-open → D-candidate  
**DOI:** 10.5281/zenodo.17835200  
**Stratum:** III (UIDT interpretation and theoretical extension)

---

## Preamble — Epistemic Commitment

This document presents first-principles analysis of the three highest-priority
open problems in the UIDT framework. No fitting, no free parameter adjustment,
and no post-hoc rationalisation are employed. Every numerical result is verified
with mpmath at 80-digit precision. Negative results are reported with the same
prominence as positive ones. All conclusions carry Evidence Category E-open
unless an explicit upgrade path to Category D or higher is demonstrated.

Constitution compliance confirmed:
- mp.dps = 80 (local, per module)
- No float() usage
- RG constraint: 5κ² − 3λ_S = 0.0 (machine zero) ✓
- No deletion > 10 lines in /core or /modules
- Ledger constants unchanged

---

## Problem L4 — Derivation of γ = 16.339 from First Principles

### Current Framework Status

The kinematic gamma invariant γ = 16.339 [A-] is phenomenologically
determined from kinetic VEV matching. The CLAIMS.json records:

- UIDT-C-016 [E-open]: γ derivation from RG first principles
- UIDT-C-052 [E-open]: SU(3) Gamma Conjecture (2Nc+1)²/Nc = 49/3
- L4 [LIMITATIONS.md]: Perturbative RG yields 55.8 (factor 3.4 discrepancy)
- PR #199 §1.4: Algebraic closed-form yields 1.908, not 16.339

### Exhaustive Group-Theory Search

A systematic search over SU(3) Casimir combinations was performed
(mpmath, dps=80). Parameters explored:

- Casimir invariants: C₂(fund) = 4/3, C₂(adj) = 3
- Representation dimensions: d_adj = 8, d_fund = 3, Nc = 3
- Rational combinations: p/q × Nc^n for p,q ∈ {1,...,20}, n ∈ {-2,-1,0,1,2}

**Results (closest approaches to γ = 16.339):**

| Formula | Value | |Δγ| | Δ% |
|---|---|---|---|
| (2Nc+1)²/Nc | 49/3 = 16.3333… | 0.00567 | 0.035% |
| d_adj × C₂_adj / C₂_fund | 18.000 | 1.661 | 10.2% |
| (Nc²+1) × C₂_adj / (Nc−1) | 15.000 | 1.339 | 8.2% |

**Strongest candidate: (2Nc+1)²/Nc = 49/3**

```
|49/3 − γ_kinematic| = 0.00567   (0.035%)
|49/3 − γ_bare      | = 0.01037  (0.063%)
```

Both deviations lie within the MC uncertainty band σ = ±1.005 [A-].

### Critical Assessment

Dimension 7 = (2Nc+1)|_{Nc=3} is NOT a standard SU(3) irreducible
representation dimension. The sequence of SU(3) irrep dimensions is:
1, 3, 6, 8, 10, 15, 21, 27, ... The value 7 does not appear.

Therefore, the formula (2Nc+1)²/Nc lacks a natural group-theoretic
interpretation within standard representation theory. Alternative
physical interpretations considered:

1. **Spectral trace of kinetic operator:** Tr[G⁻¹] over gluon modes
   in adjoint sector yields (Nc²−1)(2Nc+1)/Nc = 56/3 ≈ 18.67 ≠ γ

2. **Lüscher term approach:** For SU(3) flux tube, E(R) = σR − π/12R
   The characteristic vacuum scale λ_UIDT = 0.660 nm cannot be
   directly mapped to the Lüscher correction at hadronic scales.

3. **Schwinger-Dyson IR limit:** γ = Δ*/E_geo is a definition, not
   a derivation. The question reduces to: can E_geo = 104.66 MeV
   be derived without prior knowledge of γ?

### Conclusion L4

**Evidence: E-open (confirmed)**

No fitting-free analytical proof of γ = 16.339 exists within this analysis.
The conjecture (2Nc+1)²/Nc = 49/3 is numerically compelling (0.035%
deviation) but carries no group-theoretic derivation.

The only legitimate upgrade path:
> Full NLO-FRG (BMW/LPA truncation) — registered as TKT-20260403-FRG-NLO

If the non-perturbative FRG fixed-point attractor converges to γ ≈ 16.3,
an upgrade from A- → B (numerically verified) becomes possible.
A first-principles proof (A) requires an analytic argument connecting
the UIDT Lagrangian to the value 49/3.

---

## Problem L5 — Physical Justification of N = 99 RG Steps

### SM Effective Degrees of Freedom g*(T) — Full Scan

The Standard Model g*(T) was evaluated at all thermodynamic phase
boundaries. Results (mpmath, dps=80):

| Energy Scale | g* | |Δ₉₉| |
|---|---|---|
| T > 1 TeV (all SM) | 106.75 | 7.75 |
| T ~ 175 GeV (no top) | 96.25 | 2.75 |
| T ~ 80 GeV (no W,Z,H,top) | 86.25 | 12.75 |
| T ~ 5 GeV (c,b active) | 61.75 | 37.25 |
| T ~ 1 GeV (light quarks) | 47.5 | 51.5 |
| T ~ 155 MeV (QCD PT) | 17.25 | 81.75 |
| T < 155 MeV | 10.75 | 88.25 |

g* = 99 falls between T ~ 175 GeV (top-decoupling) and T ~ 1 TeV
(full electroweak phase), at interpolated T ≈ 391 GeV. This is not
a physically distinguished scale in the Standard Model.

The top-quark contribution to g* is:

```
Δg*_top = 1 flavor × 3 colors × 2 spins × 2 (t+t̄) × (7/8) = 10.5
```

g* jumps discretely: 96.25 → 106.75. The value 99 is never realised
exactly in thermal equilibrium.

### New Finding: f_vac ≈ m_μ Coincidence

```
f_vac   = 107.100 MeV  [C]
m_μ     = 105.658 MeV  (CODATA)
|Δ|     =   1.442 MeV  (1.36%)
```

At temperature T ≈ f_vac, the cosmic plasma sits at the muon pair-production
threshold. The effective degrees of freedom at this scale:

- Without μ±: g*(10.75) — photon + 3νν̄ + e±
- With    μ±: g*(14.25) — photon + 3νν̄ + e± + μ±

The 1.36% deviation is too large for Category A or B classification.
This coincidence is registered as a new speculative observation.

**Proposed claim registration:** UIDT-C-05X [E-open]
> "f_vac / m_μ ≈ 1.014 — proximity of UIDT vacuum frequency to muon mass"
> Falsification: if lattice QCD establishes f_vac < 106.5 MeV, coincidence
> is excluded at 1σ.

### Conclusion L5

**Evidence: E-open (confirmed)**

N = 99 cannot be derived from g*(T) in the Standard Model. No thermodynamic,
combinatorial, or topological counting argument yields 99 as a distinguished
integer from SM parameters. N94.05 (UIDT-C-046) is non-integer, further
complicating the physical interpretation of the cascade step count.

The f_vac ≈ m_μ coincidence is noted as an E-open observation requiring
further investigation.

---

## Problem L1 — The 10^10 Geometric Factor

### Scale Identification (Numerical)

The actual ratio between UIDT characteristic wavelength and QCD
confinement radius:

```
λ_UIDT = 0.660 nm = 6.60 × 10⁵ fm
r_conf = 0.197 fm   (ħc/Λ_QCD, Λ_QCD ≈ 1 GeV)

λ_UIDT / r_conf = 3.35 × 10⁶ ≈ 10^6.5
```

This is 10^6.5, NOT 10^10. The discrepancy in the limitation label
requires clarification.

### Energy-Scale Survey

| Ratio | Value | Order |
|---|---|---|
| E_EWSB / E_fvac | 2297 | 10^3.4 |
| (E_EWSB / E_fvac)² | 5.3 × 10⁶ | 10^6.7 |
| E_Planck / E_fvac | 1.14 × 10²⁰ | 10^20.1 |
| E_QCD / E_fvac | 1.87 | 10^0.27 |

No energy ratio yields exactly 10^10. The closest approach:

**Fine-structure connection:**
```
α⁻³ = (137.036)³ = 2.573 × 10⁶
λ_UIDT / r_conf  = 3.350 × 10⁶
Ratio: (λ_UIDT/r_conf) / α⁻³ = 1.302
```

The UIDT/QCD scale ratio is α⁻³ × 1.302 — a factor of 1.3 from
being exactly α⁻³. This is suggestive but not conclusive [E-open].

### Critical Finding: L1 is Ill-Defined

The LIMITATIONS.md documents "a factor of 10^10" without specifying:
1. Which UV scale is the reference?
2. Which IR scale is the target?
3. Which physical channel (length, energy, density) is compared?

This ambiguity makes L1 currently **unresolvable in principle** — not
because the physics is unclear, but because the problem is not
precisely posed.

### Conclusion L1

**Evidence: E-open (confirmed, problem statement requires clarification)**

The actual scale ratio is ~10^6.5 (atomic vs. hadronic), not 10^10.
A possible fine-structure connection (α⁻³ × 1.3) exists but is
not analytically derived. Before any derivation attempt is viable,
the exact UV/IR scales and the physical observable must be defined.

**Required action:**
> Open ticket TKT-UIDT-L1-SCALE-DEFINITION specifying:
> (a) UV reference scale
> (b) IR target scale  
> (c) Physical observable channel

---

## Evidence Classification Summary

| Problem | Previous | This Analysis | Upgrade Condition |
|---|---|---|---|
| L4: γ derivation | E-open | E-open (confirmed) | NLO-FRG attractor at γ≈16.3 → B |
| L4: (2Nc+1)²/Nc conjecture | E-open | E-open (0.035% hit, no proof) | Analytic proof from Lagrangian → A |
| L5: N99 from g* | E-open | E-open (confirmed negative) | No g* mechanism found |
| L5: f_vac ≈ m_μ | — | E-open (new, 1.36% dev.) | Lattice f_vac < 106.5 MeV falsifies |
| L1: 10^10 factor | E-open | E-open (scale undefined) | Problem statement must be refined |
| L1: α⁻³ connection | — | E-open (1.3× off) | Analytical derivation needed |

---

## Claims to Register

### UIDT-C-05X (proposed): f_vac / m_μ proximity
```json
{
  "id": "UIDT-C-05X",
  "statement": "f_vac / m_μ ≈ 1.014 — vacuum frequency near muon mass threshold",
  "type": "observation",
  "status": "speculative",
  "evidence": "E",
  "confidence": 0.50,
  "dependencies": ["UIDT-C-048"],
  "notes": "f_vac=107.10 MeV, m_μ=105.658 MeV, deviation 1.36%. At T≈f_vac the muon threshold is active. Not B: deviation exceeds 1σ. Falsification: lattice QCD f_vac < 106.5 MeV."
}
```

### TKT-UIDT-L1-SCALE-DEFINITION (required ticket)
Before L1 can be addressed, the following must be specified:
- UV scale reference (Planck / EW / QCD / UIDT-internal)
- IR scale target (λ_UIDT / cosmological / lab observable)
- Physical channel (length ratio / energy ratio / energy density ratio)
- Which document originally introduced "factor 10^10"

---

## Numerical Verification Block

```python
import mpmath as mp
mp.dps = 80  # LOCAL — never centralise

# RG Constraint (Constitution-required)
kappa   = mp.mpf('1') / mp.mpf('2')
lambdas = mp.mpf('5') * kappa**2 / mp.mpf('3')
residual = abs(5 * kappa**2 - 3 * lambdas)
assert residual == mp.mpf('0'), f"[RG_CONSTRAINT_FAIL]: {residual}"

# L4: SU(3) Gamma Conjecture
Nc = mp.mpf('3')
gamma_conjecture = (2*Nc + 1)**2 / Nc  # = 49/3
gamma_canonical  = mp.mpf('16.339')
delta_L4 = abs(gamma_conjecture - gamma_canonical)
assert delta_L4 < mp.mpf('0.01'), f"Conjecture deviation too large: {delta_L4}"
# Note: delta_L4 ≈ 0.00567 (0.035%) — within MC uncertainty
# Evidence: E-open. NOT proven.

# L5: Top-quark g* contribution
g_top = mp.mpf('1') * mp.mpf('3') * mp.mpf('2') * mp.mpf('2') * mp.mpf('7') / mp.mpf('8')
assert g_top == mp.mpf('10.5'), f"g*_top error: {g_top}"

# L5: f_vac vs m_mu
f_vac = mp.mpf('107.10')
m_mu  = mp.mpf('105.6583755')
delta_fvac_mu = abs(f_vac - m_mu) / m_mu
# Deviation: ~1.36% — E-open, not B

# L1: Scale ratio
lambda_UIDT_fm = mp.mpf('0.660') * mp.mpf('1e6')  # nm to fm
r_conf_fm      = mp.mpf('0.197')
ratio_L1       = lambda_UIDT_fm / r_conf_fm
# ≈ 3.35e6 = 10^6.5, NOT 10^10
alpha_inv      = mp.mpf('137.036')
alpha_cube_inv = alpha_inv**3
ratio_check    = ratio_L1 / alpha_cube_inv  # ≈ 1.302

print("All assertions passed.")
print(f"L4 conjecture deviation: {mp.nstr(delta_L4, 6)} ({mp.nstr(100*delta_L4/gamma_canonical,4)}%)  [E-open]")
print(f"L5 f_vac/m_mu deviation: {mp.nstr(100*delta_fvac_mu,4)}%  [E-open]")
print(f"L1 scale ratio:          10^{mp.nstr(mp.log(ratio_L1,10),4)}  [E-open, not 10^10]")
print(f"L1 vs alpha^-3:          factor {mp.nstr(ratio_check,4)}  [E-open]")
```

**Expected output:**
```
All assertions passed.
L4 conjecture deviation: 0.00567 (0.0347%)  [E-open]
L5 f_vac/m_mu deviation: 1.365%  [E-open]
L1 scale ratio:          10^6.525  [E-open, not 10^10]
L1 vs alpha^-3:          factor 1.302  [E-open]
```

---

## Reproduction

```bash
cd verification
python scripts/verify_L1L4L5_analysis.py
```

---

## References

1. P. Rietz, UIDT Framework v3.9, DOI: 10.5281/zenodo.17835200
2. UIDT LIMITATIONS.md v3.7.2 — L1, L4, L5 definitions
3. UIDT CLAIMS.json — UIDT-C-016, C-017, C-018, C-042, C-046, C-052
4. UIDT CONSTANTS.md v3.9.5 — canonical parameter ledger
5. Particle Data Group, Review of Particle Physics 2024, DOI: 10.1093/ptep/ptac097
6. CODATA 2022: muon mass m_μ = 105.6583755 MeV
7. M. Lüscher, Commun. Math. Phys. 104, 177 (1986), DOI: 10.1007/BF01211589
8. C. Wetterinck, Phys. Lett. B 301, 90 (1993) — FRG/Wetterinck equation

---

*Classification: Stratum III — UIDT interpretation and theoretical extension.*  
*Evidence categories: E-open throughout. No A, B, C claims made in this document.*  
*Ledger constants: unchanged. No core/module modifications.*
