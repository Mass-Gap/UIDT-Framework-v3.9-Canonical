# Contributing to UIDT v3.7.1

## Overview

This repository contains the Clay Mathematics Institute submission package for the Yang-Mills Mass Gap proof. Contributions that strengthen the mathematical rigor or improve verification reproducibility are welcome.

## Types of Contributions

### 1. Bug Reports

If you find an error in the mathematical derivations or verification code:

1. Check existing issues first
2. Provide:
   - Precise location (file, line, equation number)
   - Nature of the error
   - Suggested correction (if applicable)
   - Verification that the error affects the central claim

### 2. Verification Improvements

Contributions to enhance reproducibility:

- Higher-precision implementations (>80 digits)
- Alternative numerical methods
- Cross-platform compatibility fixes
- Docker/container improvements

### 3. Documentation

- Clarifications of mathematical arguments
- Additional examples
- Translation to other languages

### 4. Independent Validation

If you independently verify the mass gap result:

1. Document your method
2. Provide your computed value with uncertainty
3. Submit as a verification report

## What We Cannot Accept

Due to the nature of a Clay Mathematics Institute submission:

- **No cosmological extensions** (H₀, S₈, dark energy)
- **No technology applications** (Casimir, propulsion)
- **No modifications to canonical constants** without rigorous justification
- **No changes that weaken mathematical rigor**

## Code Standards

### Python

- Use `mpmath` with `mp.dps = 80` minimum
- Include docstrings with dimensional analysis
- All numerical claims must be reproducible
- Follow PEP 8 style

### LaTeX

- Use standard AMS packages
- Number all equations
- Include proof environments
- Cross-reference all theorems

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes with clear commit messages
4. Run all verification scripts
5. Update documentation as needed
6. Submit PR with:
   - Summary of changes
   - Mathematical justification
   - Verification output

## Mathematical Review

All contributions affecting the proof will undergo review for:

1. **Logical consistency** with existing theorems
2. **Dimensional correctness** of all equations
3. **Numerical precision** (80-digit verification)
4. **Gauge invariance** preservation

## Contact

For questions regarding contributions:

- **ORCID:** 0009-0007-4307-1609
- **DOI:** 10.5281/zenodo.17835200

## Acknowledgment

Contributors who provide significant improvements will be acknowledged in future versions of the manuscript.

---

**License:** All contributions are licensed under CC BY 4.0.
