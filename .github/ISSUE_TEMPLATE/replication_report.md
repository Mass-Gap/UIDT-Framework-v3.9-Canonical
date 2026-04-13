---
name: Replication Report
about: Report results from independent replication of UIDT calculations
title: '[REPLICATION] '
labels: replication, verification
assignees: ''
---

## Replication Summary

**Claim Replicated:** (e.g., UIDT-C-001: Mass Gap Δ = 1.710 ± 0.015 GeV)  
**Original Evidence Category:** [A / A- / B / C / D / E]  
**Replication Status:** [SUCCESS / PARTIAL / FAILED]

## Replication Details

### Original Result
**Value:** (e.g., Δ = 1.710 GeV)  
**Uncertainty:** (e.g., ±0.015 GeV)  
**Precision:** (e.g., mp.dps = 80)  
**Source:** (e.g., `verification/scripts/uidt_v3_6_1_verification.py`)

### Replicated Result
**Value:** (e.g., Δ = 1.7098 GeV)  
**Uncertainty:** (e.g., ±0.016 GeV)  
**Precision:** (e.g., mp.dps = 100)  
**Method:** (describe your replication method)

### Comparison
**Absolute Difference:** |Original - Replicated| = (e.g., 0.0002 GeV)  
**Relative Difference:** (Original - Replicated) / Original = (e.g., 0.012%)  
**Z-Score:** (e.g., 0.01σ - well within uncertainty)  
**Residual:** (for Category [A] claims, e.g., 3.2×10⁻¹⁴)

## Replication Environment

### Software
- **Language:** (e.g., Python 3.11.5)
- **Libraries:** (e.g., mpmath 1.3.0, numpy 1.24.3)
- **Operating System:** (e.g., Ubuntu 22.04 LTS)
- **Hardware:** (e.g., Intel i9-12900K, 64GB RAM)

### Code
- **Repository:** (link to your replication code, if public)
- **Commit Hash:** (if using UIDT repository)
- **Modifications:** (describe any changes to original code)

### Data
- **Input Data:** (source of input parameters)
- **External Data:** (any external data used for comparison)
- **Data Version:** (e.g., FLAG 2024, DESI DR2)

## Replication Method

### Approach
- [ ] Exact reproduction (same code, same parameters)
- [ ] Independent implementation (different code, same algorithm)
- [ ] Alternative method (different algorithm, same physics)
- [ ] Experimental comparison (compare with measured data)

### Steps Taken
1. (describe step-by-step replication process)
2. (e.g., "Downloaded code from GitHub")
3. (e.g., "Installed dependencies via pip")
4. (e.g., "Ran verification script with mp.dps = 100")
5. (e.g., "Compared output with CANONICAL/CONSTANTS.md")

### Challenges Encountered
- (describe any difficulties during replication)
- (e.g., "Missing dependency: mpmath not in requirements.txt")
- (e.g., "Numerical instability at mp.dps > 100")

## Results

### Numerical Verification
**Residual:** (for Category [A] claims)
- Original: (e.g., 3.2×10⁻¹⁴)
- Replicated: (e.g., 2.8×10⁻¹⁴)
- **Status:** [PASS / FAIL] (< 10⁻¹⁴ required for [A])

### Statistical Verification
**Z-Score:** (for Category [B] claims)
- Original: (e.g., 0.37σ)
- Replicated: (e.g., 0.41σ)
- **Status:** [PASS / FAIL] (< 1σ required for [B])

### Experimental Verification
**Comparison with Data:** (for Category [C] claims)
- UIDT Prediction: (e.g., H₀ = 70.4 ± 0.16 km/s/Mpc)
- Experimental Value: (e.g., DESI DR2: 70.4 ± 0.16 km/s/Mpc)
- **Status:** [CONSISTENT / INCONSISTENT]

## Discrepancies

### Identified Issues
- [ ] No discrepancies found
- [ ] Minor numerical differences (within uncertainty)
- [ ] Significant discrepancies (>3σ)
- [ ] Code errors discovered
- [ ] Mathematical errors discovered

### Details
(describe any discrepancies in detail)

**Potential Causes:**
- (e.g., "Rounding differences at high precision")
- (e.g., "Different random seed for Monte Carlo")
- (e.g., "Bug in original code: line 127")

**Severity:**
- [ ] LOW: Cosmetic (no impact on conclusions)
- [ ] MEDIUM: Numerical (within stated uncertainty)
- [ ] HIGH: Significant (affects evidence category)
- [ ] CRITICAL: Fatal (invalidates claim)

## Recommendations

### Evidence Category
**Current:** [A / A- / B / C / D / E]  
**Recommended:** [A / A- / B / C / D / E]  
**Justification:** (explain any recommended change)

### Code Improvements
- (suggest improvements to original code)
- (e.g., "Add input validation for κ parameter")
- (e.g., "Document precision requirements in docstring")

### Documentation Updates
- (suggest updates to documentation)
- (e.g., "Add replication instructions to README")
- (e.g., "Update CANONICAL/CONSTANTS.md with new uncertainty")

## Reproducibility Assessment

### FAIR Principles
- [x] **Findable:** Code and data available on GitHub/Zenodo
- [x] **Accessible:** Open access, no paywalls
- [x] **Interoperable:** Standard formats (Python, JSON, Markdown)
- [x] **Reusable:** Clear documentation, permissive license

### Ease of Replication
- [ ] **EASY:** Replicated in < 1 hour
- [ ] **MODERATE:** Replicated in 1-8 hours
- [ ] **DIFFICULT:** Replicated in > 8 hours
- [ ] **IMPOSSIBLE:** Could not replicate

**Time Spent:** (e.g., 2 hours)

### Barriers to Replication
- (list any obstacles encountered)
- (e.g., "Missing requirements.txt")
- (e.g., "Undocumented environment variables")
- (e.g., "Proprietary software required")

## Additional Comments

(any other observations, suggestions, or feedback)

---

## Replication Checklist

- [ ] Original result reproduced within stated uncertainty
- [ ] Code reviewed for errors
- [ ] Documentation reviewed for clarity
- [ ] Comparison with external data (if applicable)
- [ ] Residual < 10⁻¹⁴ for Category [A] claims
- [ ] Z-score < 1σ for Category [B] claims
- [ ] Replication code available (link provided)
- [ ] Results documented in this issue

---

**Replicator Information:**
- **Name:** (optional)
- **Affiliation:** (optional)
- **ORCID:** (optional)
- **Contact:** (optional)

**Date:** (YYYY-MM-DD)

---

**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**DOI:** 10.5281/zenodo.17835200

**Replication Protocol:**
1. Download code from GitHub (https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical)
2. Install dependencies: `pip install -r requirements.txt`
3. Run verification script: `python verification/scripts/uidt_v3_6_1_verification.py`
4. Compare output with CANONICAL/CONSTANTS.md
5. Document results in this issue
6. Submit pull request with any corrections (optional)
