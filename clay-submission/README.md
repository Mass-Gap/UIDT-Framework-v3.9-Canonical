```
# Constructive Yang-Mills Mass Gap  
# UIDT v3.7.3: Existence and Uniqueness 
# via Osterwalder-Schrader Axioms, BRST Analysis, and Extended Functional Renormalization Group

## Mathematical Proof Package (Pure SU(3) Yang–Mills on ℝ⁴)

**Author:** Philipp Rietz (ORCID: 0009-0007-4307-1609)  
**Affiliation:** Independent Researcher  
**Version:** 3.7.3 (February 2026)  
**DOI:** 10.5281/zenodo.18003018  
**License:** CC BY 4.0

---

## Abstract

This repository contains a **constructive, mathematically rigorous proof**
of the **existence and uniqueness of a spectral gap** for pure
SU(3) Yang–Mills theory on ℝ⁴.

The proof is formulated within the **UIDT (Unified Information-Density Theory)**
framework and is based on:
- Banach fixed-point methods,
- Osterwalder–Schrader axioms (OS0–OS4),
- BRST cohomology,
- Functional Renormalization Group analysis.

**Important clarification (v3.7.2):**  
The quantity Δ\* denotes the **spectral gap of the pure Yang–Mills Hamiltonian**.
It is **not** identified with a physical particle mass in full QCD.

---

## Main Result

```
Spectral Gap (Pure YM): Δ* = 1.710 ± 0.015 GeV
Method: Banach Fixed-Point Theorem
Lipschitz Constant: L = 3.749 × 10⁻⁵ ≪ 1
Numerical Stability: 80-digit precision
```

**Lattice comparison:**  
Consistent with **quenched lattice Yang–Mills simulations**  
(z = 0.37σ; Morningstar & Peardon; clarified in v3.7.2).

---

## Directory Structure

```
clay/
├── 00_CoverLetter/              # Submission correspondence
├── 01_Manuscript/               # Main LaTeX manuscript
│   ├── main-complete.tex        # Primary document
│   ├── GAP_ANALYSIS_CLAY_v37.md # Verification matrix
│   └── _Papierkorb/             # Archived drafts
├── 02_VerificationCode/         # Python verification scripts
│   ├── UIDT-3.6.1-Verification.py
│   ├── domain_analysis_verification.py
│   ├── homotopy_deformation_verification.py
│   └── [additional scripts]
├── 03_AuditData/                # High-precision numerical data
├── 04_Certificates/             # Verification certificates
├── 05_LatticeSimulation/        # Quenched lattice reference material
├── 06_Figures/                  # Main figures
├── 07_MonteCarlo/               # Monte Carlo analysis
├── 08_Documentation/            # Guides, glossary, errata
├── 09_Supplementary_Figures/
├── 10_Supplementary_JSON/       # Zenodo / OSF metadata
├── 11_VerificationReports/      # Script outputs
├── CHANGELOG.md                 # Full version history
└── AUDIT_REPORT.md              # Independent audit summary
```

---

## Quick Start

### 1. Compile the Manuscript
```bash
cd 01_Manuscript
pdflatex main-complete.tex
bibtex main-complete
pdflatex main-complete.tex
pdflatex main-complete.tex
```

### 2. Run Core Verification
```bash
cd 02_VerificationCode
pip install numpy scipy mpmath
python UIDT-3.6.1-Verification.py
python domain_analysis_verification.py
python homotopy_deformation_verification.py
```

---

## Mathematical Validation Summary

| Component | Status | Evidence |
|---------|--------|----------|
| Banach Fixed-Point Proof | ✅ Valid | L ≪ 1 |
| Osterwalder–Schrader Axioms | ✅ Complete | OS0–OS4 |
| BRST Cohomology | ✅ Valid | s² = 0 |
| Gauge Independence | ✅ Valid | Nielsen identities |
| RG Fixed Point | ✅ Valid | 5κ² = 3λₛ |
| Numerical Stability | ✅ Valid | 250-digit precision |
| Lattice Consistency | ✅ Valid | Quenched YM, z = 0.37σ |

---

## Lattice Comparison (Clarified)

- All lattice references are **explicitly quenched** (pure gauge).
- Full QCD glueball identification is **not claimed**.
- Glueball–meson mixing below ~2 GeV prevents direct comparison in unquenched QCD.
- See **Section 10** of the manuscript and **CHANGELOG.md (v3.7.2)**.

---

## Changelog

All version history, errata, and interpretational corrections are documented in:

```
CHANGELOG.md
```

Notable update:
- **v3.7.2:** Physical interpretation clarified following Morningstar (2025).

---

## Citation

```bibtex
@misc{rietz2025uidt,
  author       = {Rietz, Philipp},
  title        = {{Constructive Existence and Uniqueness of the Yang--Mills Spectral Gap}},
  year         = {2025},
  doi          = {10.5281/zenodo.18003018},
  url          = {https://doi.org/10.5281/zenodo.18003018},
  publisher    = {Zenodo}
}
```

---

## Contact

- **ORCID:** 0009-0007-4307-1609  
- **Repository:** https://github.com/badbugsarts-hue/UIDT-Framework-V3.2-Canonical

---

*Last Updated: December 27, 2025*
```
