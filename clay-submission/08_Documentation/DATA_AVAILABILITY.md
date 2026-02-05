# Data Availability Statement - UIDT v3.7.2 
 
## Structural Integrity Audit: 24.12.2025 
**Project:** A Constructive Proof of the Yang-Mills Mass Gap 
**Status:** Verified Repository Architecture 
 
### 1. Canonical Submission Structure 
The following hierarchical tree documents the physical existence of all modules-
 required for the independent verification of the mass gap value Delta* = 1.710 GeV.
 This includes the algorithmic kernels and the 5,000,000 MCMC samples. 
 
```
UIDT-FRAMEWORK-V3.6.1\SUPPLEMENTARY_CLAY_MASS_GAP_SUBMISSION
|   CHANGELOG.md
|   CITATION.cff
|   CONTRIBUTING.md
|   DATA_AVAILABILITY.md
|   Dockerfile.clay_audit
|   GLOSSARY.md
|   LICENSE.md
|   README.md
|   REFERENCES.bib
|   requirements.txt
|   UIDT_FileSystem_Manifest.txt
|   
+---00_CoverLetter
|       CoverLetter_Clay.pdf
|       CoverLetter_Clay.tex
|       
+---01_Manuscript
|       GAP_ANALYSIS_CLAY_v37.md
|       main-complete.tex
|       main.tex
|       UIDT-v3.7.1_Complete.pdf
|       UIDT-v3.7.1_Erratum_MassGap_Interpretation.pdf
|       UIDT_Appendix_A_OS_Axioms.tex
|       UIDT_Appendix_B_BRST.tex
|       UIDT_Appendix_C_Numerical.tex
|       UIDT_Appendix_D_Auxiliary.tex
|       UIDT_Appendix_G_Extended.tex
|       UIDT_Appendix_H_GapAnalysis.tex
|       
+---02_VerificationCode
|       brst_cohomology_verification.py
|       checksums_sha256_gen.py
|       domain_analysis_verification.py
|       error_propagation.py
|       final_audit_comparison.py
|       gribov_analysis_verification.py
|       gribov_suppression_verification.py
|       homotopy_deformation_verification.py
|       os_axiom_verification.py
|       rg_flow_analysis.py
|       slavnov_taylor_ccr_verification.py
|       UIDT-3.6.1-Verification.py
|       uidt_canonical_audit_v2.py
|       UIDT_Clay_Verifier.py
|       uidt_complete_clay_audit.py
|       uidt_proof_core.py
|       UIDT_Proof_Engine.py
|       
+---03_AuditData
|   |   AUDIT_REPORT.md
|   |   
|   +---3.2
|   |       README-Monte-Carlo.md
|   |       README_Monte-Carlo.html
|   |       UIDT_gamma_vs_Psi_scatter.png
|   |       UIDT_HighPrecision_mean_values.csv
|   |       UIDT_histograms_Delta_gamma_Psi.png
|   |       UIDT_joint_Delta_gamma_hexbin.png
|   |       UIDT_MonteCarlo_correlation_matrix.csv
|   |       UIDT_MonteCarlo_samples_100k.csv
|   |       UIDT_MonteCarlo_summary.csv
|   |       UIDT_MonteCarlo_summary_table.tex
|   |       UIDT_MonteCarlo_summary_table_short.csv
|   |       
|   +---3.6.1-corrected
|   |       UIDT_Canonical_Audit_Certificate.txt
|   |       UIDT_HighPrecision_Constants.csv
|   |       UIDT_MonteCarlo_correlation_matrix.csv
|   |       UIDT_MonteCarlo_samples_100k.csv
|   |       UIDT_MonteCarlo_summary.csv
|   |       
|   \---3.7.0-(gamma-alpha_s-correlation_weak)
|           UIDT_Clay_Audit_Certificate.txt
|           UIDT_HighPrecision_Constants.csv
|           UIDT_MonteCarlo_correlation_matrix.csv
|           UIDT_MonteCarlo_samples_100k.csv
|           UIDT_MonteCarlo_summary.csv
|           
+---04_Certificates
|       BRST_Verification_Certificate.txt
|       Canonical_Audit_v3.6.1_Certificate.txt
|       Grand_Audit_Certificate.txt
|       MASTER_VERIFICATION_CERTIFICATE.txt
|       SHA256_MANIFEST.txt
|       
+---05_LatticeSimulation
|       UIDTv3.6.1_Ape-smearing.py
|       UIDTv3.6.1_CosmologySimulator.py
|       UIDTv3.6.1_Evidence_Analyzer.py
|       UIDTv3.6.1_Hmc-Diagnostik.py
|       UIDTv3.6.1_HMC-MASTER-SIMULATION.py
|       UIDTv3.6.1_HMC_Optimized.py
|       UIDTv3.6.1_Lattice_Validation.py
|       UIDTv3.6.1_Monitor-Auto-tune.py
|       UIDTv3.6.1_Omelyna-Integrator2o.py
|       UIDTv3.6.1_Scalar-Analyse.py
|       UIDTv3.6.1_su3_expm_cayley_hamiltonian-Modul.py
|       UIDTv3.6.1_UIDT-test.py
|       UIDTv3.6.1_Update-Vector.py
|       UIDTv3_6_1_HMC_MASTER_SIMULATION.py
|       
+---06_Figures
|       UIDT_Fig_01_Static_Potential_Balanced.png
|       UIDT_Fig_02_Vacuum_Energy_Resolution.png
|       UIDT_Fig_04_Lattice_Continuum_Limit.png
|       UIDT_Fig_05_HMC_Simulation_Diagnostics.png
|       UIDT_Fig_06_Hubble_Tension_Analysis.png
|       UIDT_Fig_07_Kappa_Stability.png
|       UIDT_Fig_07_Universal_Gamma_Scaling.png
|       UIDT_Fig_12_1_Stability_Landscape.png
|       UIDT_Fig_12_2_MC_Posterior_Analysis.png
|       UIDT_Fig_12_3_Info_Flux_Correlation.png
|       UIDT_Fig_12_4_Gamma_Unification_Map.png
|       UIDT_Fig_Suppl_S2_Consistency_Z_Scores.png
|       UIDT_Fig__Suppl_S1_Detailed_Parameter_Dist.png
|       
+---07_MonteCarlo
|       MC_Statistics_Summary.txt
|       UIDT_MC_samples_summary.csv
|       
+---08_Documentation
|       GLOSSARY.md
|       Mathematical_Step_by_Step.md
|       Reviewer_Guide_Step_by_Step.md
|       UIDT_v3_7_1_Correction_Guide_Clay.md
|       Visual_Proof_Atlas.md
|       
+---09_Supplementary_JSON
|       .osf.json
|       .zenodo.json
|       codemeta.json
|       
\---10_VerificationReports
        core_proof_log_3.6.1.txt
        domain_analysis_results.txt
        homotopy_analysis_results.txt
        kappa_scan_results.csv
        os_axiom_verification_results.txt
        Verification_Report-3.6.txt
        Verification_Report-v3.6.1-ERROR-PROPAGATION-ANALYSIS.txt
        Verification_Report-v3.6.1-HMC-SIMULATION.txt
        Verification_Report-v3.6.1-Lattice-Validating.txt
        Verification_Report-v3.6.1-MASTER-SIMULATION.txt
        Verification_Report-v3.6.1-RG-FIXED-POINT-ANALYSIS.txt
        Verification_Report-v3.6.1-Scalar-Mass-Test.txt
        Verification_Report-v3.6.1-String-Tension.txt
        Verification_Report_v3.5.6.txt
        Verification_Report_v3.6.1.md
        
```  
  
### 2. Reproducibility and Access  
Independent researchers may utilize the `Dockerfile.clay_audit` provided in the root directory to execute the verification scripts against the datasets listed above. All materials are organized according to the UIDT v3.7.0 Canonical Framework.  
  
---  
UIDT Structural Audit v3 
