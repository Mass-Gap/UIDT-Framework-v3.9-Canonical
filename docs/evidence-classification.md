# Evidence Classification System

**UIDT v3.7.3** | Last Updated: 2026-02-14

> **Purpose:** Transparent classification of all claims by evidence strength
> **Principle:** Every quantitative claim MUST be tagged with Category A-E

---

## Overview

The UIDT framework employs a strict evidence classification system to distinguish between mathematically proven results, phenomenological determinations, numerical verifications, calibrated models, and predictions awaiting experimental confirmation.

**18 total claims** are documented in the framework (see [CLAIMS Registry](../clay-submission/10_VerificationReports/)).

---

## Category A — Mathematically Proven

**Definition:** Complete analytical derivation with numerical residuals < 10⁻¹⁴

**Requirements:**
- Full derivation steps documented in LaTeX
- High-precision numerical verification (mpmath/80-digit precision)
- Residual threshold: |residual| < 10⁻¹⁴
- Independent reproduction possible via [verification scripts](../verification/)

**Verified Claims (Category A):**

| Claim ID | Parameter | Value | Notes |
|----------|-----------|-------|-------|
| UIDT-C-001 | **Spectral Gap** Δ | 1.710 ± 0.015 GeV | Yang-Mills mass gap (NOT particle mass!) |
| UIDT-C-004 | **VEV** v | 47.7 MeV | Corrected from 0.854 MeV in v3.6.1 |
| UIDT-C-005 | **Coupling** κ | 0.500 ± 0.008 | Non-minimal gauge-scalar coupling |
| UIDT-C-006 | **Self-Coupling** λ_S | 0.417 ± 0.007 | Perturbative (< 1) |
| UIDT-C-010 | **RG Fixed Point** | 5κ² = 3λ_S = 1.250 | Residual 0.001 < tolerance |
| UIDT-C-013 | **Vacuum Stability** | V''(v) = 2.907 > 0 | Positive definite |
| UIDT-C-014 | **Perturbative Stability** | λ_S = 0.417 < 1 | Valid expansion |

**Verification:**
```bash
python verification/scripts/UIDT-3.6.1-Verification.py
# Expected: PASS with residuals < 10⁻⁴⁰
```

**Total Category A Claims:** 7

---

## Category A- — Phenomenologically Determined

**Definition:** High-precision determination without first-principles derivation from renormalization group equations

**Requirements:**
- Clear methodology documented
- Numerical precision established
- **Explicitly acknowledges phenomenological nature**
- Open research question for theoretical derivation

**Verified Claims (Category A-):**

| Claim ID | Parameter | Value | Derivation Method | Open Question |
|----------|-----------|-------|-------------------|---------------|
| UIDT-C-002 | **Gamma Invariant** γ | 16.339 (exact) | Kinetic VEV matching | L4: Derive from RG first principles |
| UIDT-C-003 | **Gamma MC Mean** γ | 16.374 ± 1.005 | 100k Monte Carlo samples | L4: RG derivation |

> **CRITICAL NOTE:** γ is **NOT** derived from renormalization group (RG) first principles. The perturbative RG yields γ* ≈ 55.8 (factor 3.4 discrepancy). This is documented as active research limitation **L4** in [limitations.md](limitations.md).

**Total Category A- Claims:** 2

---

## Category B — Numerically Verified / Lattice Consistent

**Definition:** Agreement with independent numerical/lattice QCD calculations

**Requirements:**
- z-score < 1σ for consistency
- Reference to external calculation (Chen et al. 2006, etc.)
- Statistical methodology documented
- Cross-verification with lattice data

**Verified Claims (Category B):**

| Claim ID | Statement | z-Score | Reference |
|----------|-----------|---------|-----------|
| UIDT-C-011 | Lattice QCD consistency | **z = 0.37σ** | Chen et al. (2006) quenched lattice |
| UIDT-C-012 | Numerical closure | < 10⁻¹⁴ | Branch 1 residual 3.2×10⁻¹⁴ |

**Status:** Well within 1σ — excellent agreement with independent calculations

**Total Category B Claims:** 2

---

## Category C — Calibrated to External Data

**Definition:** Model parameters fitted to observational/experimental data

**Requirements:**
- **Explicit data source cited** (DESI DR2, JWST, etc.)
- Fitting methodology documented
- **CANNOT claim independent prediction**
- **ALL cosmology claims are MAXIMUM Category C**

**Calibrated Claims (Category C):**

| Claim ID | Parameter | Value | Data Source | Notes |
|----------|-----------|-------|-------------|-------|
| UIDT-C-008 | **Hubble Constant** H₀ | 70.4 ± 0.16 km/s/Mpc | DESI DR2 (2025) | Calibrated, NOT independent prediction |
| λ_UIDT | **Holographic Scale** | 0.660 ± 0.005 nm | Global fit (DESI/JWST) | Category C |
| S₈ | **Structure Growth** | 0.814 ± 0.009 | Weak lensing data | Category C |

> **⚠️ CRITICAL RULE:** ALL cosmological claims are Category C or lower. **NEVER** Category A or B for cosmology.

**Total Category C Claims:** 3 (including 1 implicit λ_UIDT)

---

## Category D — Predicted, Unverified

**Definition:** Theoretical predictions awaiting experimental confirmation

**Requirements:**
- Clear falsification criterion
- No experimental confirmation yet
- Listed in [falsification-criteria.md](falsification-criteria.md)
- Timeline for experimental test

**Predicted Claims (Category D):**

| Claim ID | Prediction | Falsification Test | Timeline |
|----------|------------|-------------------|----------|
| UIDT-C-007 | **Scalar Mass** m_S = 1.705 ± 0.015 GeV | LHC Run 4: >5σ exclusion in 1.5-1.9 GeV | 2029+ |
| UIDT-C-009 | **Casimir Anomaly** +0.59% at 0.66 nm | Precision measurement: \|ΔF/F\| < 0.1% excludes | 2028+ |
| d_opt | **Optimal Casimir Distance** 0.854 nm | Sub-nanometer force measurements | Technology-limited |

> **IMPORTANT:** Category D claims are predictions, **NOT** verified facts. They represent testable hypotheses that could refute the theory if excluded experimentally.

**Total Category D Claims:** 2 (+ 1 implicit d_opt)

---

## Category E — Speculative / Open / Withdrawn

**Definition:** Exploratory hypotheses, active research questions, or retracted claims

**Sub-categories:**
- **E-open:** Active research questions
- **E-speculative:** Early-stage hypotheses
- **E-withdrawn:** Previously claimed, now formally retracted

**Category E Claims:**

| Claim ID | Statement | Sub-Type | Status | Notes |
|----------|-----------|----------|--------|-------|
| UIDT-C-015 | Glueball identification at 1.71 GeV | **E-withdrawn** | Retracted 2025-12-25 | Δ is spectral gap, NOT particle mass |
| UIDT-C-016 | γ derivation from RG first principles | **E-open** | Active research | Perturbative RG gives γ* ≈ 55.8 |
| UIDT-C-017 | N=99 RG steps justification | **E-open** | Active research | Phenomenological, no theoretical derivation |
| UIDT-C-018 | 10¹⁰ geometric factor derivation | **E-open** | **HIGHEST PRIORITY** | Unresolved, affects λ_UIDT interpretation |

**Total Category E Claims:** 4

---

## Upgrade/Downgrade Rules

### Upgrade Path

```
E → D: Theoretical foundation established, falsification criterion defined
D → C: Experimental data obtained, model calibrated
C → B: Independent numerical verification from external groups
B → A-: Systematic derivation achieved (phenomenological)
A- → A: First-principles derivation with residuals < 10⁻¹⁴
```

### Downgrade Triggers

```
A → B: Numerical residuals exceed 10⁻¹⁴ threshold
B → C: Lattice inconsistency detected (z-score > 3σ)
C → D: Data source invalidated or retracted
D → E: Experimental falsification confirmed
Any → E-withdrawn: Explicit retraction by author
```

### Documentation Requirement

Every category change MUST be logged with:
- Timestamp
- Previous category
- New category
- Justification
- Reference (publication, data, analysis)

---

## Statistical Summary

| Category | Count | Percentage |
|----------|-------|------------|
| A (Proven) | 7 | 38.9% |
| A- (Phenomenological) | 2 | 11.1% |
| B (Numerically Verified) | 2 | 11.1% |
| C (Calibrated) | 1 | 5.6% |
| D (Predicted) | 2 | 11.1% |
| E (Open/Withdrawn) | 4 | 22.2% |
| **Total** | **18** | **100%** |

**Verified (A+A-+B):** 11 claims (61.1%)
**Testable (D):** 2 claims (11.1%)
**Calibrated (C):** 1 claim (5.6%)
**Open Research (E):** 4 claims (22.2%)

---

## Quick Reference Table

| Category | Residual Threshold | Cosmology Allowed? | Requires Derivation? | Can Be Falsified? |
|----------|-------------------|--------------------|---------------------|-------------------|
| **A** | < 10⁻¹⁴ | ❌ Never | ✅ Full analytical | ✅ Yes (if residuals fail) |
| **A-** | N/A | ❌ Never | ⚠️ Phenomenological | ✅ Yes (if RG derivation contradicts) |
| **B** | z < 1σ | ❌ Never | ✅ Numerical | ✅ Yes (if lattice excludes >3σ) |
| **C** | N/A | ✅ **Maximum** | ❌ Calibration only | ✅ Yes (if data source invalid) |
| **D** | N/A | ✅ Yes | ❌ Prediction only | ✅ **Yes (primary purpose)** |
| **E** | N/A | ✅ Yes | ❌ Speculative | ⚠️ Withdrawn/Exploratory |

---

## How to Use This System

### For Researchers

1. **Reading claims:** Check the evidence category before citing
2. **Extending UIDT:** Clearly classify your new claims (A-E)
3. **Challenging UIDT:** Focus falsification efforts on Category D predictions

### For Reviewers

1. **Verify categories:** Cross-check claim categories against verification data
2. **Challenge upgrades:** Ensure upgrades (e.g., D→C) meet strict criteria
3. **Demand transparency:** Require explicit category tags in all statements

### For Journal Editors

1. **Abstract review:** Ensure abstract mentions evidence classification
2. **Supplementary data:** Verify full category breakdown is provided
3. **Falsification:** Confirm Category D predictions have clear experimental tests

---

## Citation

```bibtex
@misc{Rietz2025_EvidenceClassification,
  author = {Rietz, Philipp},
  title  = {UIDT Evidence Classification System v3.7.3},
  year   = {2025},
  doi    = {10.5281/zenodo.17835200},
  url    = {https://github.com/badbugsarts-hue/UIDT-Framework-v3.7.3-Canonical}
}
```

**See also:**
- [Known Limitations (L1-L6)](limitations.md)
- [Falsification Criteria](falsification-criteria.md)
- [Verification Guide](verification-guide.md)

---

**Last Updated:** 2026-02-05
**DOI:** 10.5281/zenodo.17835200
