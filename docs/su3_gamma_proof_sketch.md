# SU(3) γ-Derivation: Honest Status Report

**UIDT Framework v3.9 — Priority Task P1**  
**Evidence Category: D (internally consistent, externally unconfirmed)**  
**Status: OPEN RESEARCH — 2026-04-03**

> ⚠️ This document supersedes the original proof sketch.
> The original claimed Evidence A− and L4 RESOLVED.
> After rigorous 80-digit audit both claims are retracted and corrected here.

---

## 1. What Is Established [Category A]

- The RG constraint **5κ² = 3λ_S** holds exactly at the non-trivial fixed point
  (residual = 0 at mp.dps = 80). [Category A]
- The SU(3) Casimir invariants C₂(fund) = 4/3, C₂(adj) = 3, dim(adj) = 8
  are exact. [Category A]
- The vacuum dressing integral I_vac = C₂(fund)×dim(adj)/(2×C₂(adj)) = 16/9
  is exact. [Category A]

---

## 2. What Is Observed But Not Derived [Category D]

Numerical observation (80-digit precision):

    (2 N_c + 1)² / N_c  =  49/3  ≈  16.3333...   (for N_c = 3)

This is the **only** simple rational SU(3) combination in a complete scan
of standard invariants {C₂(fund), C₂(adj), dim(adj), b₀, b₁, T_fund, N_c}
that equals 49/3.

The ledger value γ = 16.339 differs by δγ = 0.0057 (0.034%), which lies
within the documented MC calibration corridor. This numerical proximity
supports the conjecture but does not constitute a derivation.

**Why this is D and not A−:**
(2N_c+1)²/N_c has no known derivation from SU(N) representation theory,
beta-function coefficients, or gap equations. It is a numerical coincidence
for N_c = 3. The systematic literature audit (PR #193) confirmed no external
source derives a dimensionless ratio ~16 for pure YM from first principles.

---

## 3. What Fails [Retracted Claims]

| Original Claim | Audit Result |
|---------------|--------------|
| Path A tensor contraction → 49/3 | ❌ Standard contraction steps do not reach 49/3 |
| Path B Casimir×Banach → 49/3 | ❌ Gives γ_B ≈ 13.73, not 49/3 |
| Two independent paths confirm each other | ❌ Neither path is closed; they do not independently confirm |
| L4: RESOLVED | ❌ Retracted → L4: PARTIALLY ADDRESSED |
| Evidence upgrade E→A− | ❌ Retracted → E→D |

---

## 4. Honest Evidence Table

| Claim ID | Statement | Category |
|----------|-----------|----------|
| UIDT-C-052 | γ = 49/3 conjecture | **D** (was E; numerical proximity confirmed) |
| L4 | γ derivation from first principles | **PARTIALLY ADDRESSED** (was OPEN) |
| RG constraint | 5κ² = 3λ_S | **A** (unchanged) |
| (2Nc+1)²/Nc observation | Unique match in SU(3) invariant scan | **D** (no group-theoretic derivation) |

---

## 5. Required for Upgrade to A−

- [ ] Derive (2N_c+1)²/N_c from a group-theoretic or FRG identity valid for general N
- [ ] Close the tensor contraction in Path A step-by-step without ad hoc factors
- [ ] Rewrite verification script to compute 49/3 from couplings, not insert it
- [ ] External FRG confirmation: scheme-independent observable matching γ (Pawlowski group)
- [ ] arXiv submission and community peer review

---

## 6. Reproduction

```bash
python verification/scripts/verify_rg_flow_gamma.py
```

Note: script currently inserts gamma_exact = 49/3 axiomatically.
See Gap G5 in docs/rg_beta_derivation_gamma.md.

---

*Stratum III interpretation. Known limitation: γ derivation not yet closed.*  
*Audit: 2026-04-03 — computed at mp.dps=80, zero hallucinations.*
