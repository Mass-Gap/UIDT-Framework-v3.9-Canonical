# Data Availability Statement — UIDT v3.9

**Version:** 3.9 (Canonical Release)
**DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)
**License:** MIT (code) / CC-BY-4.0 (data and documentation)

---

All data, code, and computational resources required to reproduce the results
presented in the UIDT framework are publicly available under open-source
licenses.

---

## 1. Repository Overview

| Field | Value |
| :--- | :--- |
| **Repository** | [Mass-Gap/UIDT-Framework-v3.9-Canonical](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical) |
| **Version** | v3.9 (Canonical Release) |
| **Status** | Scientifically closed — all claims version-tagged and verified |
| **License** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (data) / MIT (code) |
| **DOI** | [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200) |
| **Author** | Philipp Rietz ([ORCID: 0009-0007-4307-1609](https://orcid.org/0009-0007-4307-1609)) |

---

## 2. Canonical Repositories

| Platform | Resource | Link |
| :--- | :--- | :--- |
| **GitHub** | Source code and documentation | [Mass-Gap/UIDT-Framework-v3.9-Canonical](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical) |
| **OSF** | Project registration and supplementary materials | [10.17605/OSF.IO/Q8R74](https://doi.org/10.17605/OSF.IO/Q8R74) |
| **Zenodo** | Permanent archival record (CERN infrastructure) | [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200) |

---

## 3. Repository Structure

### 3.1 Canonical Verification Suite (`verification/scripts/`)

| File | Description |
| :--- | :--- |
| `UIDT_Master_Verification.py` | Four-Pillar Master Verification Suite (v3.9); proves mass gap, Banach convergence, and spectral expansions |
| `UIDT-3.6.1-Verification.py` | Newton–Raphson solver for coupled field equations; computes Δ, γ, κ, λ_S, m_S with residuals < 10⁻¹⁴ |
| `UIDT-3.6.1-Verification-visual.py` | Visualization engine generating Figures 12.1–12.4 |
| `rg_flow_analysis.py` | RG flow analysis confirming the fixed-point relation 5κ² = 3λ_S |
| `error_propagation.py` | Full uncertainty budget and Monte Carlo error propagation |
| `modules/geometric_operator.py` | Core geometric operator engine (mass-gap derivation chain) |

### 3.2 Lattice QCD Simulation Pipeline (`simulation/`)

| File | Description |
| :--- | :--- |
| `UIDTv3.6.1_HMC_Optimized.py` | GPU-optimized Hybrid Monte Carlo lattice QCD pipeline |
| `UIDTv3_6_1_HMC_Real.py` | Full real-valued HMC with SU(3) gauge group |
| `UIDTv3.6.1_Omelyna-Integrator2o.py` | Omelyan second-order symplectic integrator |
| `UIDTv3.6.1_Ape-smearing.py` | APE smearing for noise reduction in glueball correlators |
| `UIDTv3.6.1_su3_expm_cayley_hamiltonian-Modul.py` | SU(3) Lie-algebra module (Cayley–Hamilton decomposition) |
| `UIDTv3.6.1_Scalar-Analyse.py` | Scalar correlator extraction and effective-mass analysis |
| `UIDTv3.6.1_Monitor-Auto-tune.py` | Step-size auto-tuning and acceptance rate diagnostics |
| `UIDTv3.6.1_Update-Vector.py` | Gauge-link update vectors for Metropolis–Hastings |
| `UIDTv3.6.1_CosmologySimulator.py` | Cosmological observable synthesis (H₀, S₈, w(z)) |
| `UIDTv3.6.1_Evidence_Analyzer.py` | Evidence classification engine (Categories A–E) |
| `UIDT-3.6.1-visual.py` | Lattice visualization and diagnostic plots |
| `uidt-cosmic-simulation.py` | Cosmic evolution simulator with γ(z) scaling |

### 3.3 Clay Mathematics Institute Submission Audit (`clay-submission/`)

The `clay-submission/` directory contains a self-contained submission package
structured according to the Clay Mathematics Institute Millennium Prize Problem
requirements:

| Directory | Contents |
| :--- | :--- |
| `00_CoverLetter/` | Formal submission cover letter |
| `01_Manuscript/` | Definitive manuscript PDF |
| `02_VerificationCode/` | 17 specialized verification scripts (BRST cohomology, Gribov analysis, homotopy deformation, Slavnov–Taylor identities, OS axiom verification, SHA-256 checksums, Clay audit pipelines) |
| `03_AuditData/` | Versioned numerical audit data (see Section 4) |
| `04_Certificates/` | Audit certificates |
| `05_LatticeSimulation/` | Complete lattice QCD simulation suite |
| `06_Figures/` | Publication-quality figures |
| `07_MonteCarlo/` | Monte Carlo statistics summary |
| `08_Documentation/` | Technical documentation |
| `09_Supplementary_JSON/` | Machine-readable metadata (codemeta.json) |
| `10_VerificationReports/` | Formal verification reports |

A containerized reproduction environment is provided via
`clay-submission/Dockerfile.clay_audit`.

---

## 4. Datasets

### 4.1 Versioned Audit Data (`clay-submission/03_AuditData/`)

The audit data directory maintains a complete version history across three
development stages:

| Directory | Content |
| :--- | :--- |
| `3.2/` | Original v3.2 Monte Carlo data: 100,000 samples (10 parameters), full 8×8 correlation matrix, statistical summary, high-precision mean values |
| `3.6.1-corrected/` | Corrected v3.6.1 audit data with updated high-precision constants and recomputed Monte Carlo ensembles |
| `3.7.0-(gamma-alpha_s-correlation_weak)/` | v3.7.0 data isolating the γ–α_s correlation structure |
| `AUDIT_REPORT.md` | Comprehensive audit report documenting all corrections and version transitions |

### 4.2 Verification Data (`verification/data/`)

| File | Content |
| :--- | :--- |
| `uidt_solutions.csv` | Two-branch solution table with perturbativity flags |
| `Verification_Report-kappa_scan_results.csv` | κ-scan results for stability landscape analysis |
| `lattice_comparison.xlsx` | Compilation of lattice QCD glueball mass determinations |
| Verification reports (`.txt`, `.md`) | RG flow, error propagation, scalar mass, string tension, lattice validation |

### 4.3 Monte Carlo Summary (`clay-submission/07_MonteCarlo/`)

| File | Content |
| :--- | :--- |
| `UIDT_MC_samples_summary.csv` | Aggregated Monte Carlo sample statistics |
| `MC_Statistics_Summary.txt` | Descriptive statistics and convergence diagnostics |

---

## 5. Figure Regeneration

All figures can be regenerated deterministically:

| Figure | Script | Data Dependency |
| :--- | :--- | :--- |
| Fig. 12.1 | `UIDT-3.6.1-Verification-visual.py` | `kappa_scan_results.csv` |
| Fig. 12.2 | `UIDT-3.6.1-Verification-visual.py` | `UIDT_MonteCarlo_samples_100k.csv` |
| Fig. 12.3 | `UIDT-3.6.1-Verification-visual.py` | `UIDT_MonteCarlo_samples_100k.csv` |
| Fig. 12.4 | `UIDT-3.6.1-Verification-visual.py` | `UIDT_HighPrecision_mean_values.csv` |

---

## 6. Reproduction Protocol

```bash
# Clone repository
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical
cd UIDT-Framework-v3.9-Canonical

# Install dependencies
pip install -r verification/requirements.txt

# Core verification (reproduces Tables 1-3, canonical solution & spectra)
python verification/scripts/UIDT_Master_Verification.py

# Uncertainty budget and error propagation
python verification/scripts/error_propagation.py

# RG flow fixed-point analysis
python verification/scripts/rg_flow_analysis.py

# Cosmological predictions (reproduces H0, S8 values)
python simulation/UIDTv3.6.1_CosmologySimulator.py

# Generate all figures (reproduces Figures 12.1-12.4)
python verification/scripts/UIDT-3.6.1-Verification-visual.py

# Full Clay audit (optional; containerized)
cd clay-submission
docker build -f Dockerfile.clay_audit -t uidt-audit .
docker run uidt-audit
```

**Computational requirements:**

- Standard desktop (Intel i5 or equivalent, 16 GB RAM)
- Python >= 3.10 with numpy >= 1.24, scipy >= 1.10, matplotlib >= 3.7, pandas >= 2.0
- Total runtime: ~10 min (excluding HMC full lattice run)
- HMC full lattice: requires GPU (NVIDIA CUDA), runtime ~24 h for 32⁴ lattice

Data integrity can be verified independently via
`clay-submission/02_VerificationCode/checksums_sha256_gen.py`.

---

## 7. External Data Sources

| Source | Reference | Access |
| :--- | :--- | :--- |
| **DESI DR2** | arXiv:2503.14738 (DESI Collaboration, 2025) | Official DESI data portal |
| **Lattice QCD** | Peer-reviewed publications (see References) | Individual results cited in manuscript |
| **Planck 2018** | arXiv:1807.06209 (Planck Collaboration, 2020) | ESA Planck Legacy Archive |
| **JWST** | JWST CCHP team | STScI MAST archive |

---

## 8. Version Control and Long-Term Preservation

| Platform | Role | Preservation |
| :--- | :--- | :--- |
| **GitHub** | Active development under `Mass-Gap` organization | Issue tracking, CI |
| **Zenodo** | Permanent DOI-based archival | 20+ years (CERN Data Centre) |
| **OSF** | Preregistration and supplementary materials | Permanent DOI |

---

## 9. Supersession Notice

All data and derivations from previous iterations (v1.6.1, v3.3, etc.) are
formally superseded. Version 3.9 represents the canonical release of the UIDT
framework. The v3.3 Zenodo record has been permanently withdrawn due to data
corruption (see Version History notice in the manuscript).

---

**Contact for data access issues:** pr88@gmx.de

© 2025 Philipp Rietz — DOI: [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)
