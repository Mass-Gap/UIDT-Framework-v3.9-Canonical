---
name: Verification Request
about: Request independent verification of a UIDT claim or numerical result
title: '[VERIFY] '
labels: verification, peer-review
assignees: ''
---

## Claim to Verify

**Claim ID:** (e.g., UIDT-C-001, UIDT-C-054)  
**Statement:** (brief description of the claim)  
**Current Evidence Category:** [A / A- / B / C / D / E]

## Verification Request Type

- [ ] Numerical verification (reproduce calculation)
- [ ] Analytical verification (check mathematical proof)
- [ ] Experimental verification (compare with data)
- [ ] Code review (check implementation)
- [ ] Statistical verification (check uncertainty quantification)

## Current Status

**Source File(s):**
- (e.g., `verification/scripts/uidt_v3_6_1_verification.py`)
- (e.g., `CANONICAL/CONSTANTS.md`)

**Current Result:**
- (e.g., Δ = 1.710 ± 0.015 GeV)
- (e.g., Residual = 3.2×10⁻¹⁴)

**Precision Used:**
- (e.g., mp.dps = 80)
- (e.g., Monte Carlo samples = 100k)

## Verification Method

**Proposed Approach:**
- (describe how you plan to verify the claim)
- (e.g., "Re-run calculation with independent code")
- (e.g., "Compare with lattice QCD data from FLAG 2024")

**Tools/Software:**
- (e.g., Python 3.11 + mpmath)
- (e.g., Mathematica 13.2)
- (e.g., Lattice QCD simulation)

**Expected Timeline:**
- (e.g., 1 week for numerical verification)
- (e.g., 1 month for experimental comparison)

## Success Criteria

**Verification Passes If:**
- [ ] Numerical result matches within stated uncertainty
- [ ] Residual < 10⁻¹⁴ for Category [A] claims
- [ ] z-score < 1σ for Category [B] claims
- [ ] Consistent with external data for Category [C] claims

**Verification Fails If:**
- [ ] Numerical discrepancy > 3σ
- [ ] Residual > 10⁻¹⁴ for Category [A] claims
- [ ] Code error discovered
- [ ] Mathematical proof invalid

## Potential Issues

**Known Limitations:**
- (e.g., L1: 10¹⁰ geometric factor unexplained)
- (e.g., L4: γ not derived from RG first principles)

**Dependencies:**
- (list any claims this depends on)
- (e.g., UIDT-C-005: κ = 0.500 ± 0.008)

**Falsification Risk:**
- (describe what would falsify this claim)
- (e.g., "If lattice QCD excludes Δ at >5σ")

## Additional Context

**Motivation:**
- (why is this verification important?)
- (e.g., "Required for Clay Millennium Prize submission")
- (e.g., "Experimental test planned at LHC")

**References:**
- (relevant papers, data sources, etc.)

**Contact:**
- (your name/email if you want to be contacted)

---

**Verification Protocol:**
1. Independent reproduction of numerical result
2. Code review by second researcher
3. Comparison with external data (if available)
4. Statistical significance assessment
5. Update LEDGER/CLAIMS.json with verification status
6. Document results in verification/reports/

**Evidence Category Upgrade Path:**
- [E] → [D]: Prediction formulated with falsification criteria
- [D] → [C]: Calibrated to external data
- [C] → [B]: Numerically verified with z < 1σ
- [B] → [A]: Analytically proven with residual < 10⁻¹⁴
- [A] → [A-]: Phenomenologically determined (permanent)

---

**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**DOI:** 10.5281/zenodo.17835200
