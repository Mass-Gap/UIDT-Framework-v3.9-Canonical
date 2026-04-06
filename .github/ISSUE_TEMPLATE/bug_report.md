---
name: Bug Report - Numerical Discrepancy
about: Report numerical precision issues, residual violations, or unexpected test failures
title: '[BUG] '
labels: bug, numerical-precision
assignees: ''
---

## Bug Description

<!-- Provide a clear and concise description of the numerical discrepancy -->

## Expected Behavior

**Expected Value:**  
<!-- e.g., Δ = 1.710 GeV -->

**Evidence Category:**  
<!-- [A / A- / B / C / D / E] -->

**Precision Target:**  
<!-- e.g., Residual < 10^-14 for Category A -->

## Actual Behavior

**Actual Value:**  
<!-- e.g., Δ = 1.712 GeV -->

**Residual:**  
<!-- e.g., |expected - actual| = 0.002 GeV -->

**Precision Achieved:**  
<!-- e.g., Residual = 1.2e-3 (FAILS Category A threshold) -->

## Reproduction Steps

1. <!-- Step 1 -->
2. <!-- Step 2 -->
3. <!-- Step 3 -->

**Minimal Reproduction Command:**
```bash
# Provide a single command to reproduce the issue
python verification/scripts/verify_spectral_gap.py
```

## Environment

**Python Version:**  
<!-- e.g., 3.11.5 -->

**mpmath Version:**  
<!-- e.g., 1.3.0 -->

**mpmath Precision (mp.dps):**  
<!-- e.g., 80 -->

**Operating System:**  
<!-- e.g., Ubuntu 22.04, Windows 11, macOS 14 -->

**Hardware:**  
<!-- e.g., Intel i7-12700K, 32GB RAM -->

## Affected Constants

<!-- List all physical constants affected by this bug -->

| Symbol | Expected | Actual | Category | Residual |
|--------|----------|--------|----------|----------|
| Δ | 1.710 GeV | 1.712 GeV | A | 0.002 |
| <!-- Add more rows as needed --> |

## Limitation Impact

<!-- Does this bug affect any known limitations (L1-L6)? -->

- [ ] L1: 10¹⁰ geometric factor
- [ ] L2: Electron mass (23% residual)
- [ ] L3: Vacuum energy (factor 2.3)
- [ ] L4: γ = 16.339 (not RG-derived)
- [ ] L5: N = 99 RG steps
- [ ] L6: Glueball f₀(1710) (retracted)
- [ ] None

## Falsification Risk

<!-- Could this bug trigger a falsification criterion? -->

- [ ] **CRITICAL:** Residual > 10^-2 for Category A claim
- [ ] **HIGH:** Residual > 10^-6 for Category A claim
- [ ] **MEDIUM:** Residual > 1σ for Category B claim
- [ ] **LOW:** Minor precision degradation
- [ ] **NONE:** No falsification risk

## Additional Context

<!-- Add any other context, logs, or screenshots -->

```
# Paste relevant error messages or log output here
```

## Proposed Solution

<!-- If you have a hypothesis about the cause or a potential fix, describe it here -->

## Checklist

- [ ] I have verified this is not a duplicate issue
- [ ] I have provided a minimal reproduction command
- [ ] I have included all relevant environment details
- [ ] I have calculated the residual using mpmath (not float)
- [ ] I have checked if this affects any falsification criteria

---
**DOI:** 10.5281/zenodo.17835200  
**Framework Version:** 3.9  
**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)
