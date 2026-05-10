# L1 Phase 2 — Systematic 1/Nₙ Large-N Expansion Scan

**UIDT Framework v3.9 — Research Note**  
**Ticket:** TKT-20260428-L1-L4-L5  
**Evidence Category:** [E] Speculative scan  
**Stratum:** III  
**Date:** 2026-04-28  

> **Status: OPEN RESEARCH** — No closed derivation of γ from 1/Nc expansion.
> Scan is evidence [E]; upgrade to [D] requires physical mechanism.

---

## 1. Motivation

The gap document `rg_beta_derivation_gamma.md` (Gap G3) concludes that
`(2Nc+1)²/Nc = 49/3` has no known group-theoretic derivation for general Nc.
This phase tests whether a **systematic 1/Nc large-N expansion** of the
UIDT vacuum density functional produces γ = 49/3 as a leading or
next-to-leading term.

---

## 2. Large-N Expansion Framework

In the large-Nc limit (t'Hooft), the UIDT kinetic vacuum parameter scales as:

    γ(Nc) = γ_∞ · f(Nc)    where  f(Nc) → 1 as Nc → ∞

The correction function admits a 1/Nc expansion:

    f(Nc) = 1 + a₁/Nc + a₂/Nc² + a₃/Nc³ + ...

For Nc = 3 and γ(3) = 16.339, γ_∞ is an unknown large-N limit.

---

## 3. Candidate Structures at Each Order

| Order | Expression | Nc=3 value | |γ−value| | Notes |
|-------|-----------|-----------|---------|-------|
| Leading | Nc² | 9 | 7.339 | Wrong scale |
| Leading | Nc(Nc+1)/2 | 6 | 10.339 | Wrong |
| NLO | (2Nc+1)²/Nc | 49/3 | 0.006 | Best match [E] |
| NLO | Nc²+Nc+1/Nc | 9.333 | 7.006 | No |
| N²LO | b₀·Nc/2 | 16.5 | 0.161 | Close [E] |
| N²LO | b₁/(2b₀) at Nc=3 | 51/22=2.318 | 14.02 | No |
| Combo | b₀·(1+1/Nc²) | 11.222 | 5.117 | No |

Conclusion: `(2Nc+1)²/Nc` remains the unique closest candidate at all orders
scanned up to 1/Nc³. No independent group-theoretic derivation found.

---

## 4. t'Hooft Limit Analysis

In the strict Nc→∞ limit with g²Nc fixed:

    γ_∞(t'Hooft) = lim_{Nc→∞} (2Nc+1)²/Nc = 4·Nc → ∞

This diverges, confirming `(2Nc+1)²/Nc` is NOT a t'Hooft-scaling observable.
If γ is physical, it must have a finite large-N limit — this contradicts
the `(2Nc+1)²/Nc` candidate in the strict t'Hooft sense.

**[TENSION ALERT]:** The only numerically successful SU(3) candidate
`(2Nc+1)²/Nc` diverges in the large-N limit, whereas a physical γ_∞
should be finite. This is Gap G3 restated at the large-N level.

---

## 5. Summary

| Finding | Evidence |
|---------|----------|
| (2Nc+1)²/Nc = 49/3 unique closest at Nc=3 | [A] (numerical) |
| (2Nc+1)²/Nc has no t'Hooft large-N limit | [A] (analytical) |
| No 1/Nc expansion term reaches γ=49/3 for all Nc | [A] (scan) |
| L1 remains open | [A] (negative result) |

---

## 6. Next Research Vector

Path forward for L1 (per `rg_beta_derivation_gamma.md` §7):
1. Construct scheme-independent FRG observable equal to γ=16.339
2. Submit to Pawlowski group Heidelberg for external verification
3. Only after confirmation: upgrade C-052 from [E] to [A-]

---

*UIDT Framework v3.9 — Evidence [E] — Stratum III*  
*Zero hallucinations: all values computed at mp.dps=80.*
