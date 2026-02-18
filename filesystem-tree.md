# UIDT-Framework-V3.6.1 Filesystem Tree

## Root Directory Structure

```
UIDT-Framework-V3.6.1/
├── .gitignore                          # Git ignore rules
├── CHANGELOG.md                       # Project change history
├── CITATION.cff                      # Citation information
├── CONTRIBUTING.md                   # Contribution guidelines
├── GLOSSARY.md                       # Project glossary
├── LICENSE.md                        # License information
├── metadata.xml                      # Project metadata
├── README.md                         # Project README
├── SECURITY.md                       # Security information
├── .cursor/                          # Cursor IDE configuration
├── .kilocode/                        # Kilocode configuration
├── clay-submission/                  # Clay Mathematics Institute submission materials
├── docs/                             # Documentation
├── figures/                          # Visual figures
├── manuscript/                       # Main manuscript
├── metadata/                         # Project metadata files
├── references/                       # Reference materials
├── simulation/                       # Simulation code
├── Supplementary_Results/            # Supplementary results
├── Supporting_Documents/            # Supporting documents
└── verification/                     # Verification and validation code
```

## 1. Clay Submission Directory (/clay-submission/)

This directory contains all materials prepared for the Clay Mathematics Institute submission.

```
clay-submission/
├── CHANGELOG.md                      # Submission change log
├── CONTRIBUTING.md                   # Contribution guidelines
├── Dockerfile.clay_audit             # Docker configuration for audit
├── GLOSSARY.md                       # Submission glossary
├── LICENSE.md                        # License
├── README.md                         # Submission README
├── REFERENCES.bib                    # BibTeX references
├── requirements.txt                  # Python dependencies
├── 00_CoverLetter/                  # Cover letter materials
│   ├── CoverLetter_Clay.pdf          # Cover letter PDF
│   └── CoverLetter_Clay.tex          # LaTeX source
├── 01_Manuscript/                   # Main manuscript files
│   ├── GAP_ANALYSIS_CLAY_v37.md      # Gap analysis
│   ├── main-complete.tex            # Complete main manuscript
│   ├── main.tex                     # Main manuscript core
│   ├── UIDT_Appendix_A_OS_Axioms.tex # OS axioms appendix
│   ├── UIDT_Appendix_B_BRST.tex     # BRST symmetry appendix
│   ├── UIDT_Appendix_C_Numerical.tex # Numerical methods appendix
│   ├── UIDT_Appendix_D_Auxiliary.tex # Auxiliary methods appendix
│   ├── UIDT_Appendix_G_Extended.tex  # Extended results appendix
│   ├── UIDT_Appendix_H_GapAnalysis.tex # Gap analysis appendix
│   ├── UIDT-v3.7.1_Erratum_MassGap_Interpretation.pdf # Erratum
│   └── UIDT-v3.7.1-Complete.pdf      # Complete PDF
├── 02_VerificationCode/             # Verification code
│   ├── brst_cohomology_verification.py # BRST cohomology verification
│   ├── checksums_sha256_gen.py      # Checksum generation
│   ├── domain_analysis_verification.py # Domain analysis
│   ├── error_propagation.py         # Error propagation
│   ├── final_audit_comparison.py    # Final audit comparison
│   ├── gribov_analysis_verification.py # Gribov analysis
│   ├── gribov_suppression_verification.py # Gribov suppression
│   ├── homotopy_deformation_verification.py # Homotopy deformations
│   ├── os_axiom_verification.py     # OS axioms verification
│   ├── rg_flow_analysis.py          # RG flow analysis
│   ├── slavnov_taylor_ccr_verification.py # Slavnov-Taylor CCR
│   ├── udt_canonical_audit_v2.py    # Canonical audit v2
│   ├── UIDT_Clay_Verifier.py        # Clay verifier engine
│   ├── udt_complete_clay_audit.py   # Complete Clay audit
│   ├── udt_proof_core.py            # Proof core
│   ├── UIDT_Proof_Engine.py         # Proof engine
│   └── UIDT-3.6.1-Verification.py   # Verification script
├── 03_AuditData/                    # Audit data
│   ├── AUDIT_REPORT.md              # Audit report
│   ├── 3.2/                         # Version 3.2 data
│   │   ├── README_Monte-Carlo.html   # Monte Carlo README (HTML)
│   │   ├── README-Monte-Carlo.md    # Monte Carlo README (Markdown)
│   │   ├── UIDT_gamma_vs_Psi_scatter.png # Gamma vs Psi scatter
│   │   ├── UIDT_HighPrecision_mean_values.csv # High precision means
│   │   ├── UIDT_histograms_Delta_gamma_Psi.png # Histograms
│   │   ├── UIDT_joint_Delta_gamma_hexbin.png # Hexbin visualization
│   │   ├── UIDT_MonteCarlo_correlation_matrix.csv # Correlation matrix
│   │   ├── UIDT_MonteCarlo_samples_100k.csv # 100k samples
│   │   ├── UIDT_MonteCarlo_summary_table_short.csv # Summary table
│   │   ├── UIDT_MonteCarlo_summary_table.tex # LaTeX summary table
│   │   └── UIDT_MonteCarlo_summary.csv # Summary CSV
│   ├── 3.6.1-corrected/            # Version 3.6.1 corrected data
│   │   ├── UIDT_Canonical_Audit_Certificate.txt # Canonical audit certificate
│   │   ├── UIDT_HighPrecision_Constants.csv # High precision constants
│   │   ├── UIDT_MonteCarlo_correlation_matrix.csv # Correlation matrix
│   │   ├── UIDT_MonteCarlo_samples_100k.csv # 100k samples
│   │   └── UIDT_MonteCarlo_summary.csv # Summary CSV
│   └── 3.7.0-(gamma-alpha_s-correlation_weak)/ # Version 3.7.0 data
│       ├── UIDT_Clay_Audit_Certificate.txt # Clay audit certificate
│       ├── UIDT_HighPrecision_Constants.csv # High precision constants
│       ├── UIDT_MonteCarlo_correlation_matrix.csv # Correlation matrix
│       ├── UIDT_MonteCarlo_samples_100k.csv # 100k samples
│       └── UIDT_MonteCarlo_summary.csv # Summary CSV
├── 04_Certificates/                 # Verification certificates
│   ├── BRST_Verification_Certificate.txt # BRST verification certificate
│   ├── Canonical_Audit_v3.6.1_Certificate.txt # Canonical audit certificate
│   ├── MASTER_VERIFICATION_CERTIFICATE.txt # Master verification certificate
│   └── SHA256_MANIFEST.txt          # SHA256 checksums
├── 05_LatticeSimulation/           # Lattice simulation code
│   ├── UIDTv3_7_2_HMC_Real.py      # HMC real simulation
│   ├── UIDTv3.6.1_Ape-smearing.py  # Ape smearing
│   ├── UIDTv3.6.1_CosmologySimulator.py # Cosmology simulator
│   ├── UIDTv3.6.1_Evidence_Analyzer.py # Evidence analyzer
│   ├── UIDTv3.6.1_HMC_Optimized.py  # Optimized HMC
│   ├── UIDTv3.6.1_Lattice_Validation.py # Lattice validation
│   ├── UIDTv3.6.1_Monitor-Auto-tune.py # Auto-tune monitor
│   ├── UIDTv3.6.1_Omelyna-Integrator2o.py # Omelyna integrator
│   ├── UIDTv3.6.1_Scalar-Analyse.py # Scalar analysis
│   ├── UIDTv3.6.1_su3_expm_cayley_hamiltonian-Modul.py # SU(3) Hamiltonian
│   ├── UIDTv3.6.1_UIDT-test.py      # UIDT test
│   └── UIDTv3.6.1_Update-Vector.py # Update vector
├── 06_Figures/                     # Manuscript figures
│   ├── UIDT_Fig__Suppl_S1_Detailed_Parameter_Dist.png # Parameter distribution
│   ├── UIDT_Fig_01_Static_Potential_Balanced.png # Static potential
│   ├── UIDT_Fig_02_Vacuum_Energy_Resolution.png # Vacuum energy resolution
│   ├── UIDT_Fig_04_Lattice_Continuum_Limit.png # Lattice-continuum limit
│   ├── UIDT_Fig_06_Hubble_Tension_Analysis.png # Hubble tension
│   ├── UIDT_Fig_07_Kappa_Stability.png # Kappa stability
│   ├── UIDT_Fig_07_Universal_Gamma_Scaling.png # Gamma scaling
│   ├── UIDT_Fig_12_1_Stability_Landscape.png # Stability landscape
│   ├── UIDT_Fig_12_2_MC_Posterior_Analysis.png # MC posterior
│   ├── UIDT_Fig_12_3_Info_Flux_Correlation.png # Info flux correlation
│   ├── UIDT_Fig_12_4_Gamma_Unification_Map.png # Gamma unification
│   └── UIDT_Fig_Suppl_S2_Consistency_Z_Scores.png # Z-scores
├── 07_MonteCarlo/                  # Monte Carlo results
│   ├── MC_Statistics_Summary.txt   # MC statistics summary
│   └── UIDT_MC_samples_summary.csv # MC samples summary
├── 08_Documentation/               # Additional documentation
│   ├── DATA_AVAILABILITY.md        # Data availability info
│   ├── Mathematical_Step_by_Step.md # Mathematical steps
│   ├── Reviewer_Guide_Step_by_Step.md # Reviewer guide
│   └── Visual_Proof_Atlas.md       # Visual proof atlas
├── 09_Supplementary_JSON/          # Supplementary JSON metadata
│   ├── .osf.json                   # OSF configuration
│   ├── .zenodo.json                # Zenodo configuration
│   └── codemeta.json               # Code meta
└── 10_VerificationReports/        # Verification reports
    ├── core_proof_log_3.6.1.txt    # Core proof log
    ├── COTA_CRITICISM_VERIFICATION_2025-01-04.md # Criticism verification
    ├── Dockerfile_Structural_Audit_20251229.md # Docker structural audit
    ├── domain_analysis_results.txt # Domain analysis results
    ├── gribov_analysis_results.txt # Gribov analysis results
    ├── High-Precision-Iteration-Log.de # High precision iteration log (German)
    ├── homotopy_analysis_results.txt # Homotopy analysis results
    ├── kappa_scan_results.csv      # Kappa scan results
    ├── os_axiom_verification_results.txt # OS axiom results
    ├── SHA256_MANIFEST_Dockerfile_Audit_20251229.txt # SHA256 manifest for Docker audit
    ├── Verification_Report_v3.5.6.txt # V3.5.6 report
    ├── Verification_Report_v3.6.1.md # V3.6.1 report
    ├── Verification_Report-3.6.txt # V3.6 report
    ├── Verification_Report-v3.6.1-ERROR-PROPAGATION-ANALYSIS.txt # Error propagation
    ├── Verification_Report-v3.6.1-Lattice-Validating.txt # Lattice validation
    ├── Verification_Report-v3.6.1-RG-FIXED-POINT-ANALYSIS.txt # RG fixed point
    ├── Verification_Report-v3.6.1-Scalar-Mass-Test.txt # Scalar mass test
    └── Verification_Report-v3.6.1-String-Tension.txt # String tension test
```

## 2. Documentation Directory (/docs/)

```
docs/
├── citation-guide.md                # Citation guidelines
├── data-availability.md             # Data availability
├── evidence-classification.md      # Evidence classification
├── falsification-criteria.md       # Falsification criteria
├── limitations.md                  # Project limitations
├── verification-guide.md           # Verification guide
└── validation/
    └── UIDT_v37-fin-max_Validation_Report.md # V3.7 final max validation
```

## 3. Figures Directory (/figures/)

```
figures/
├── supplementary/                  # Supplementary figures
    ├── UIDT-FIG-1_UIDT_Code_Output_Raw_A.png
    ├── UIDT-FIG-2_UIDT_Code_Output_Raw_B.png
    ├── UIDT-FIG-3_UIDT_Code_Output_Raw_C.png
    ├── UIDT-FIG-4_UIDT_Fig1-3.6.1__Banach_Convergence.png
    ├── UIDT-FIG-5_UIDT_Fig2-3.6.1__Gamma_Scaling_Map.png
    ├── UIDT-FIG-6_UIDT_Fig3-3.6.1__Stability_Landscape.png
    ├── UIDT-FIG-7_UIDT_Fig4-3.6.1__Parameter_Posterior.png
    ├── UIDT-FIG-8_UIDT_Fig_01_Static_Potential_Balanced.png
    ├── UIDT-FIG-9_UIDT_Fig_02_Vacuum_Energy_Resolution.png
    ├── UIDT-FIG-10_UIDT_Fig_04_Lattice_Continuum_Limit.png
    ├── UIDT-FIG-11_UIDT_Fig_05_HMC_Simulation_Diagnostics.png
    ├── UIDT-FIG-12_UIDT_Fig_06_Hubble_Tension_Analysis.png
    ├── UIDT-FIG-13_UIDT_Fig_07_Kappa_Stability.png
    ├── UIDT-FIG-14_UIDT_Fig_07_Universal_Gamma_Scaling.png
    ├── UIDT-FIG-15_UIDT_Fig_12_1_Stability_Landscape.png
    ├── UIDT-FIG-16_UIDT_Fig_12_2_MC_Posterior_Analysis.png
    ├── UIDT-FIG-17_UIDT_Fig_12_3_Info_Flux_Correlation.png
    ├── UIDT-FIG-18_UIDT_Fig_12_4_Gamma_Unification_Map.png
    ├── UIDT-FIG-19_UIDT_Internal_Parameter_Overview.png
    ├── UIDT-FIG-20_UIDT_Suppl_Fig_S1_Detailed_Parameter_Dist.png
    ├── UIDT-FIG-21_UIDT_Suppl_Fig_S2_Consistency_Z_Scores.png
    ├── UIDT-FIG-22_UIDT_Vis_Render_General_A.png
    └── UIDT-FIG-23_UIDT_Vis_Render_General_B.png
```

## 4. Manuscript Directory (/manuscript/)

```
manuscript/
├── UIDT_v3.7.3_Complete-Framework.pdf # Complete framework PDF
├── UIDT_v3.7.3-Complete-Framework.tex # LaTeX source
├── UIDT-Audit-Report-V3.2.pdf        # V3.2 audit report
├── UIDT-Cover-Letter_v3.6.1.pdf     # V3.6.1 cover letter
└── UIDT-Technical-Note-V3.2.pdf     # V3.2 technical note
```

## 5. Metadata Directory (/metadata/)

```
metadata/
├── codemeta.json                     # Code meta metadata
├── metadata.json                     # Project metadata
├── osf.json                          # OSF metadata
├── UIDT-Omega_Final-Synthesis.yaml  # Omega final synthesis
├── UIDT-Supplementary_MonteCarlo_HighPrecision.yaml # MC high precision
└── zenodo.json                       # Zenodo metadata
```

## 6. References Directory (/references/)

```
references/
├── biblatex.cfg                      # BibLaTeX configuration
└── REFERENCES.bib                    # BibTeX references
```

## 7. Simulation Directory (/simulation/)

```
simulation/
├── UIDT-3.6.1-visual.py              # Visualization script
├── udt-cosmic-simulation.py         # Cosmic simulation
├── UIDTv3_6_1_HMC_Real.py          # HMC real simulation
├── UIDTv3.6.1_Ape-smearing.py      # Ape smearing
├── UIDTv3.6.1_CosmologySimulator.py # Cosmology simulator
├── UIDTv3.6.1_Evidence_Analyzer.py # Evidence analyzer
├── UIDTv3.6.1_HMC_Optimized.py      # Optimized HMC
├── UIDTv3.6.1_Monitor-Auto-tune.py # Auto-tune monitor
├── UIDTv3.6.1_Omelyna-Integrator2o.py # Omelyna integrator
├── UIDTv3.6.1_Scalar-Analyse.py     # Scalar analysis
├── UIDTv3.6.1_su3_expm_cayley_hamiltonian-Modul.py # SU(3) Hamiltonian
├── UIDTv3.6.1_UIDT-test.py          # UIDT test
└── UIDTv3.6.1_Update-Vector.py      # Update vector
```

## 8. Verification Directory (/verification/)

```
verification/
├── requirements.txt                  # Python dependencies
├── data/                            # Verification data
│   ├── lattice_comparison.xlsx      # Lattice comparison
│   ├── udt_solutions.csv            # UIDT solutions
│   ├── Verification_Report_v3.5.6.txt # V3.5.6 report
│   ├── Verification_Report_v3.6.1.md # V3.6.1 report
│   ├── Verification_Report-3.6.txt # V3.6 report
│   ├── Verification_Report-core_proof_log_3.6.1.txt # Core proof log
│   ├── Verification_Report-kappa_scan_results.csv # Kappa scan
│   ├── Verification_Report-v3.6.1-ERROR-PROPAGATION-ANALYSIS.txt # Error propagation
│   ├── Verification_Report-v3.6.1-Lattice-Validating.txt # Lattice validation
│   ├── Verification_Report-v3.6.1-RG-FIXED-POINT-ANALYSIS.txt # RG fixed point
│   ├── Verification_Report-v3.6.1-Scalar-Mass-Test.txt # Scalar mass test
│   └── Verification_Report-v3.6.1-String-Tension.txt # String tension test
├── docker/                           # Docker configuration
│   └── Dockerfile                   # Dockerfile
└── scripts/                         # Verification scripts
    ├── error_propagation.py         # Error propagation
    ├── rg_flow_analysis.py          # RG flow analysis
    ├── udt_proof_core.py            # Proof core
    ├── UIDT-3.6.1-Verification-visual.py # Visual verification
    └── UIDT-3.6.1-Verification.py   # Main verification script
```

## Project Overview

The UIDT-Framework-V3.6.1 is a comprehensive theoretical physics framework for modeling vacuum information density as the fundamental scalar. It includes:

### Key Features:
- **Theoretical Framework**: Complete mathematical formulation with axiomatic basis
- **Verification System**: Extensive verification and validation codebase
- **Simulation Infrastructure**: Lattice simulation and cosmology modeling
- **Audit Capabilities**: Comprehensive audit and verification reporting
- **Documentation**: Detailed explanations, guides, and technical documentation

### Main Directories:
- `/clay-submission/`: Materials for Clay Mathematics Institute submission
- `/docs/`: Project documentation and guides
- `/figures/`: Visual figures and diagrams
- `/manuscript/`: Main theoretical manuscript
- `/simulation/`: Simulation and modeling code
- `/verification/`: Verification and validation system
- `/metadata/`: Project metadata and configuration

### Version History:
- V3.2: Initial version with Monte Carlo data
- V3.6.1: Current canonical version with corrected data
- V3.7.0: Gamma-alpha_s correlation variant
- V3.7.1: Erratum and complete version
- V3.7.2: Updated version with HMC real simulation
- V3.7.3: Complete framework version