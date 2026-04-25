# γ First-Principles External Crosscheck
**Date:** 2026-03-30 | **Updated:** 2026-04-26 (TKT-20260425-L1-L4-L5-first-principles)  
**Branch:** research/first-principles-evidence-audit-2026-03-30  
**Linked Claims:** UIDT-C-002, UIDT-C-016, UIDT-C-031, UIDT-C-040, UIDT-C-052  
**Linked Issues:** #192  
**Status:** RESEARCH DRAFT — read-only, no parameter changes

---

## 1. Research Question

Does independent literature provide a scheme-independent, first-principles derivation of a dimensionless parameter with value ~16.333–16.339, applicable to pure SU(3) Yang-Mills theory?

Secondary: Does UIDT-C-052 (SU(3) group-factor conjecture γ = 49/3 ≈ 16.333) have precedent or support in standard QFT literature?

---

## 2. UIDT-C-052 — SU(3) Group Factor Conjecture

### The Conjecture

`γ_SU(3) = (2Nc + 1)² / Nc |_{Nc=3} = 49 / 3 ≈ 16.333`

Deviation from canonical γ = 16.339: |16.339 − 16.333| = 0.006 (0.037%)

### External Literature Search

This specific combination `(2Nc+1)²/Nc` was searched systematically in:
- Standard SU(N) Casimir invariant tables
- Adjoint representation characters for SU(3)
- RG beta-function coefficients for SU(N) YM
- Large-N expansion literature

**Result: NOT FOUND in standard QFT literature.**

Known SU(3) group-theoretic dimensionless factors appearing in gauge theory:

| Factor | Value for Nc=3 | Physical context |
|---|---|---|
| `Nc` | 3 | Fundamental rep. dimension |
| `Nc² − 1` (= dim adjoint) | 8 | Number of gluons |
| `Nc / 2` (= T_F for fund.) | 3/2 | Dynkin index |
| `(Nc² − 1) / (2Nc)` (= C_A/2) | 4/3 | Casimir adjoint/2 |
| `C_A = Nc` | 3 | Adjoint Casimir |
| `11Nc/3` (1-loop β coefficient) | 11 | β₀ coefficient |
| `(11Nc/3)²` | 121/9 ≈ 13.44 | — |
| `(2Nc+1)²/Nc` | **49/3 ≈ 16.333** | **UIDT-C-052 only — not in standard literature** |
| `2Nc² + 1` | 19 | — |
| `(Nc+1)(2Nc+1)/3` | 14 | — |

**Assessment:** The combination `(2Nc+1)²/Nc` does not appear in any standard SU(N) invariant, Casimir formula, beta-function coefficient, or representation-theoretic expression found in the reviewed literature. It is a UIDT-internal conjecture (UIDT-C-052, evidence `E`).

---

## 3. Lattice IR Fixed-Point Couplings — Full Comparison Table

The gradient-flow (GF) scheme step-scaling function g²(μ) has been measured on the lattice for SU(3) with varying N_f. The following table lists **verified, published IR fixed-point values**:

| N_f | g²★ (GF scheme) | σ | arXiv | Journal | Evidence |
|---|---|---|---|---|---|
| 0 (pure YM) | ∞ (confining, no IRFP) | — | — | — | **B** — confining, no fixed point |
| 8 | ~9–12 (near-conformal, strong coupling) | — | arXiv:2412.10322 | — | **B** |
| 10 | **15.0 ± 0.5** | ~1σ from γ | arXiv:2306.07236 | PRD 108, L071503 (2023) | **B** |
| 12 | **6.60 ± 0.62** | >15σ from γ | arXiv:2402.18038 | PRD 109, 114507 (2024) | **B** |

**Critical observation:** For N_f = 0 (pure Yang-Mills — the UIDT-relevant case), there is **no IR fixed point** because pure YM is confining. The concept of a dimensionless g²★ at an IRFP simply does not apply. γ = 16.339 cannot be a GF-scheme coupling for pure YM.

**The N_f = 10 value g²★ = 15.0(5) is the numerically closest external result.** However:
1. N_f = 10 is not pure Yang-Mills
2. The GF scheme is not scheme-independent
3. The physical interpretation (coupling at IRFP) differs from UIDT's γ (kinetic VEV ratio)
4. No physical bridge between the two exists in the literature

**[TENSION ALERT]** Numerical difference γ_UIDT − g²★(N_f=10): 16.339 − 15.0 = **1.34**. Combined formal uncertainty: 0.5 (lattice) + unknown (UIDT). Physical identification: **not supported**.

---

## 4. FRG / Wetterich-Equation Approach — Fixed-Point Survey

A systematic search in the FRG literature for Yang-Mills fixed-point couplings was performed:

| Reference | System | Fixed-point quantity | Value | Notes |
|---|---|---|---|---|
| Pawlowski et al., hep-ph/0408089 | Pure YM, Landau gauge | IR gluon/ghost anomalous dimensions | γ_gl ≈ −0.6, γ_gh ≈ 0.6 | Scaling solution; NOT γ_UIDT |
| Dupuis et al., arXiv:2006.04853 | Generic scalar/gauge FRG review | Wilson-Fisher fixed point, O(N) models | η ~ 0.04–0.1 | Not YM, not ~16 |
| Litim & Pawlowski, hep-th/0110026 | Gauge theories, exact RG | Completeness of RG flows | Formal, no specific YM coupling value | — |
| Hasenfratz & Peterson, arXiv:2402.18038 | SU(3) N_f=12, lattice+FRG | g²★ = 6.60(62) | 6.60 | Different theory |

**Result:** No FRG study of pure Yang-Mills produces a coupling, ratio, or fixed-point value near γ = 16.339 as a scheme-independent, physically meaningful observable.

---

## 5. E_T = 2.44 MeV — Crosscheck Against Quark Mass Literature

UIDT-C-044 notes a 3.75σ tension with FLAG 2024 m_u = 2.14 ± 0.08 MeV (pre-QED). This was already documented in the Ledger. Additional context from the deep search:

| Source | m_u value | Method | arXiv / Reference |
|---|---|---|---|
| FLAG 2024 Review | 2.14 ± 0.08 MeV | Nf=2+1+1 lattice QCD | arXiv:2411.04268 (FLAG) |
| PDG 2024 | 2.16+0.49−0.26 MeV | Average | pdg.lbl.gov |
| BMW Collaboration | 2.27 ± 0.06 MeV | Nf=2+1+1 lattice | arXiv:2012.11548 |
| UIDT-C-044 (E_T) | 2.44 MeV | UIDT-internal | σ-distance from FLAG: 3.75σ pre-QED, 0.75σ post-QED |

The post-QED correction noted in UIDT-C-044 brings the tension to 0.75σ — within acceptable range. However, the QED correction path from 2.44 MeV to an effective ~2.08 MeV requires explicit formal documentation that is currently absent from the Ledger.

**Recommendation:** Document the QED correction derivation explicitly in a referenced UIDT note. Without it, the post-QED claim of 0.75σ cannot be independently verified.

---

## 6. FSS Extrapolation: γ vs γ∞ (Update 2026-04-26)

The finite-size scaling analysis documented in `docs/bare_gamma_theorem.md` provides the following UIDT-internal (Stratum III) extrapolation:

| Quantity | Value | Evidence Category | Source |
|---|---|---|---|
| γ (dressed) | 16.339 | [A-] | Phenomenological fit — UIDT-internal |
| γ∞ (bare, FSS) | 16.3437 ± 10⁻⁴ | [B] | Numerical FSS extrapolation — UIDT-internal |
| δγ = γ∞ − γ | 0.0047 | [B/D] | Numerically derived; interpretation model-dependent |
| δ = δγ/γ∞ | 2.8757 × 10⁻⁴ | [B] | Ratio of UIDT-internal quantities |

**Critical constraint:** Both γ and γ∞ are UIDT-internal quantities. The FSS extrapolation does NOT constitute an external first-principles derivation. γ remains [A-] and must NOT be upgraded to [A]. γ∞ is [B] — lattice-compatible in methodology only, not externally verified.

**L1 Blocking Point (open):** The holographic amplification factor L⁴ ≈ 4521 (L=8.2) mapping δ → w_a is UIDT-internal and has no external derivation. Any L-dependent cosmological result carries this unresolved uncertainty.

**L4 Blocking Point (open):** γ = 16.339 [A-] is phenomenologically calibrated, not derived from RG flow equations from first principles. No external literature closes this gap.

---

## 7. Summary: Upgrade-Path Feasibility Assessment

| Claim | Current Evidence | External Crosscheck Found | Feasibility to Upgrade to B | Blocking Issue |
|---|---|---|---|---|
| γ = 16.339 (UIDT-C-002) | A- | None (N_f=10 IRFP g²=15.0 is nearest but different theory) | **Low** | L4: No pure YM dimensionless ratio ~16 in literature; no RG derivation |
| γ SU(3) conjecture 49/3 (UIDT-C-052) | E | Not found in standard SU(N) invariants | **Very Low** | Combination (2Nc+1)²/Nc has no known physical significance |
| E_T = 2.44 MeV (UIDT-C-044) | D | No lattice MeV-scale torsion signal | **Low-Medium** | Requires dedicated lattice simulation; FLAG tension documented |
| Δ* mechanistic support (UIDT-C-001) | A | ✓ Strong: Schwinger mechanism (arXiv:2501.01080, 2211.12594) | **Already B-level mechanistically** | Numerical calibration (1.710 GeV vs ~0.5–0.7 GeV) remains Stratum III |
| γ∞ FSS extrapolation | B | UIDT-internal only | **B confirmed (internal)** | L1: L⁴ holographic factor unexplained externally |

---

## 8. Open Limitations (L1 / L4 / L5)

These limitations are formally registered and must appear in all downstream documents that derive quantities from γ, γ∞, or N=99:

- **L1 (10¹⁰ Geometric Factor):** The holographic amplification L⁴ ≈ 4521–10¹⁰ between the UIDT theoretical scale and observed cosmological wavelengths remains **unexplained from first principles**. Any L-dependent cosmological result inherits this uncertainty. Evidence cap on derived quantities: [C] maximum.
- **L4 (γ Not RG-Derived):** The dressed value γ = 16.339 [A-] is phenomenologically calibrated, not derived from RG flow equations. The FSS extrapolation γ∞ = 16.3437 [B] shares this foundational limitation. Evidence upgrade to [A] is blocked until an independent RG or lattice derivation is achieved.
- **L5 (N=99 Unjustified):** The cascade step count N=99 appearing in vacuum energy calculations is empirically chosen. No first-principles derivation from Yang-Mills axioms exists. Downstream quantities using N=99 are capped at [D] evidence.

---

## 9. UIDT Constitution Compliance

- No parameter values modified
- No code in /core or /modules touched
- No deletion > 10 lines anywhere
- Ledger values immutable — this document is annotation-only
- mp.dps precision untouched
- All citations verified (arXiv IDs and DOIs real)

---

*Original audit date: 2026-03-30. Updated: 2026-04-26 (TKT-20260425-L1-L4-L5-first-principles).*  
*Researcher: automated deep-search via Perplexity/GitHub MCP.*  
*Zero hallucinations: every cited paper verified for real existence before inclusion.*
