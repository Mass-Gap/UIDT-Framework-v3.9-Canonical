# UIDT-Framework v3.9 — Canonical Filesystem Tree

> **Last updated:** 2026-03-12 (v3.9 canonical state, post PR #180–183)
> **Status:** Authoritative reference for repository structure.
> Agents must not create directories outside this tree without explicit approval.

---

## Root Directory Structure

```
UIDT-Framework-v3.9-Canonical/
├── .editorconfig                     # Editor configuration
├── .gitattributes                    # Git attributes
├── .gitignore                        # Git ignore rules
├── CHANGELOG.md                      # Project change history
├── CITATION.cff                      # Citation information
├── CONTRIBUTING.md                   # Contribution guidelines
├── FORMALISM.md                      # Core equation reference (public)
├── GLOSSARY.md                       # Project glossary
├── LICENSE.md                        # License information
├── metadata.xml                      # Project metadata (Zenodo/OSF)
├── README.md                         # Project README
├── SECURITY.md                       # Public security & disclosure policy
├── filesystem-tree.md                # This file — canonical structure reference
├── .github/                          # GitHub Actions, templates
├── CANONICAL/                        # Canonical constants and evidence system
├── clay-submission/                  # Clay Mathematics Institute submission
├── core/                             # Core UIDT proof engine (protected)
├── docs/                             # Project documentation
├── figures/                          # Visual figures
├── LEDGER/                           # Claims, changelog, traceability
├── LOCAL/                            # Local runtime artifacts (logs, scripts, DB)
├── manuscript/                       # Main theoretical manuscript
├── metadata/                         # Zenodo/OSF/CodeMeta metadata files
├── modules/                          # Physical modules (protected)
├── references/                       # BibTeX references
├── simulation/                       # HMC/Lattice simulation code
└── verification/                     # Verification and validation system
```

### Removed (obsolete — do NOT recreate)

| Directory | Reason | Canonical replacement |
|-----------|--------|-----------------------|
| `Supplementary_Results/` | Non-canonical root placement | `verification/results/` |
| `Supporting_Documents/` | Non-canonical root placement | `docs/` |
| `UIDT-OS/` | Replaced by `CANONICAL/` + `LEDGER/` + `LOCAL/` | see below |
| `data/` | Non-canonical root placement | `verification/data/` |
| `arxiv_scan.py` (root) | Scripts do not belong at root | `LOCAL/scripts/` |

---

## 1. CANONICAL/

Immutable canonical parameters, evidence system, and known limitations.
Modification requires dual approval + `LEDGER/CHANGELOG.md` entry.

```
CANONICAL/
├── CONSTANTS.md                      # Immutable parameter ledger (A/A- evidence)
├── EVIDENCE.md                       # Evidence category classification reference
├── EVIDENCE_SYSTEM.md                # Operational specification (v3.7.2)
├── FALSIFICATION.md                  # Falsification criteria and thresholds
└── LIMITATIONS.md                    # Known limitations (L1–L6)
```

---

## 2. LEDGER/

Append-only claims database, changelog, and traceability map.

```
LEDGER/
├── CHANGELOG.md                      # Version history and decision log
├── CLAIMS.json                       # Machine-readable evidentiary claims (v3.9.4)
├── claims.schema.json                # JSON schema for CLAIMS.json validation
├── FALSIFICATION.md                  # Falsification tracking (mirror of CANONICAL/)
└── tickets_new.json                  # Open tickets (TKT-AUDIT-*)
```

---

## 3. LOCAL/

Local runtime environment. Not for public consumption — internal agent use only.

```
LOCAL/
├── schema_sqlite.sql                 # SQLite schema v1.0 (UIDT-OS DB)
├── logs/
│   ├── findings.json                 # Audit QA findings log
│   └── traceability.json             # Claim-to-source traceability map (TKT-AUDIT-007)
└── scripts/
    └── arxiv_scan.py                 # ArXiv monitoring script (RESEARCH-MODE)
```

---

## 4. Clay Submission (/clay-submission/)

```
clay-submission/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── Dockerfile.clay_audit
├── GLOSSARY.md
├── LICENSE.md
├── README.md
├── REFERENCES.bib
├── requirements.txt
├── 00_CoverLetter/
│   ├── CoverLetter_Clay.pdf
│   └── CoverLetter_Clay.tex
├── 01_Manuscript/
│   ├── GAP_ANALYSIS_CLAY_v37.md
│   ├── main-complete.tex
│   ├── main.tex
│   ├── UIDT_Appendix_A_OS_Axioms.tex
│   ├── UIDT_Appendix_B_BRST.tex
│   ├── UIDT_Appendix_C_Numerical.tex
│   ├── UIDT_Appendix_D_Auxiliary.tex
│   ├── UIDT_Appendix_G_Extended.tex
│   ├── UIDT_Appendix_H_GapAnalysis.tex
│   ├── UIDT-v3.7.1_Erratum_MassGap_Interpretation.pdf
│   └── UIDT-v3.7.1-Complete.pdf
├── 02_VerificationCode/
│   ├── brst_cohomology_verification.py
│   ├── checksums_sha256_gen.py
│   ├── domain_analysis_verification.py
│   ├── error_propagation.py
│   ├── final_audit_comparison.py
│   ├── gribov_analysis_verification.py
│   ├── gribov_suppression_verification.py
│   ├── homotopy_deformation_verification.py
│   ├── os_axiom_verification.py
│   ├── rg_flow_analysis.py
│   ├── slavnov_taylor_ccr_verification.py
│   ├── udt_canonical_audit_v2.py
│   ├── UIDT_Clay_Verifier.py
│   ├── udt_complete_clay_audit.py
│   ├── udt_proof_core.py
│   ├── UIDT_Proof_Engine.py
│   └── UIDT-3.6.1-Verification.py
├── 03_AuditData/
│   ├── AUDIT_REPORT.md
│   ├── 3.2/
│   ├── 3.6.1-corrected/
│   └── 3.7.0-(gamma-alpha_s-correlation_weak)/
├── 04_Certificates/
│   ├── BRST_Verification_Certificate.txt
│   ├── Canonical_Audit_v3.6.1_Certificate.txt
│   ├── MASTER_VERIFICATION_CERTIFICATE.txt
│   └── SHA256_MANIFEST.txt
├── 05_LatticeSimulation/
├── 06_Figures/
├── 07_MonteCarlo/
│   ├── MC_Statistics_Summary.txt
│   └── UIDT_MC_samples_summary.csv
├── 08_Documentation/
│   ├── DATA_AVAILABILITY.md
│   ├── Mathematical_Step_by_Step.md
│   ├── Reviewer_Guide_Step_by_Step.md
│   └── Visual_Proof_Atlas.md
├── 09_Supplementary_JSON/
│   ├── .osf.json
│   ├── .zenodo.json
│   └── codemeta.json
└── 10_VerificationReports/
    ├── core_proof_log_3.6.1.txt
    ├── Verification_Report_v3.6.1.md
    └── [additional reports]
```

---

## 5. Documentation (/docs/)

```
docs/
├── citation-guide.md
├── data-availability.md
├── evidence-classification.md
├── falsification-criteria.md
├── heavy_quark_predictions.md
├── lhcb_predictions_paper_draft.md
├── limitations.md
├── su3_gamma_theorem.md
├── verification-guide.md
└── validation/
    └── UIDT_v37-fin-max_Validation_Report.md
```

---

## 6. Figures (/figures/)

```
figures/
└── supplementary/
    └── [UIDT-FIG-1 through UIDT-FIG-23 — PNG figures]
```

---

## 7. Manuscript (/manuscript/)

```
manuscript/
├── UIDT_v3.7.3_Complete-Framework.pdf
├── UIDT_v3.7.3-Complete-Framework.tex
├── UIDT-Audit-Report-V3.2.pdf
├── UIDT-Cover-Letter_v3.6.1.pdf
└── UIDT-Technical-Note-V3.2.pdf
```

---

## 8. Metadata (/metadata/)

```
metadata/
├── codemeta.json
├── metadata.json
├── osf.json
├── UIDT-Omega_Final-Synthesis.yaml
├── UIDT-Supplementary_MonteCarlo_HighPrecision.yaml
└── zenodo.json
```

---

## 9. References (/references/)

```
references/
├── biblatex.cfg
└── REFERENCES.bib
```

---

## 10. Simulation (/simulation/)

```
simulation/
├── UIDT-3.6.1-visual.py
├── udt-cosmic-simulation.py
├── UIDTv3_6_1_HMC_Real.py
├── UIDTv3.6.1_Ape-smearing.py
├── UIDTv3.6.1_CosmologySimulator.py
├── UIDTv3.6.1_Evidence_Analyzer.py
├── UIDTv3.6.1_HMC_Optimized.py
├── UIDTv3.6.1_Monitor-Auto-tune.py
├── UIDTv3.6.1_Omelyna-Integrator2o.py
├── UIDTv3.6.1_Scalar-Analyse.py
├── UIDTv3.6.1_su3_expm_cayley_hamiltonian-Modul.py
├── UIDTv3.6.1_UIDT-test.py
└── UIDTv3.6.1_Update-Vector.py
```

---

## 11. Verification (/verification/)

```
verification/
├── requirements.txt
├── data/                             # Verification output data (read-only)
│   ├── README.md
│   ├── lattice_comparison.xlsx
│   ├── udt_solutions.csv
│   └── [Verification_Report_* files]
├── docker/
│   └── Dockerfile
├── results/                          # Auto-generated verification reports
│   └── Verification_Report_v3.6.1.md
├── scripts/                          # Verification scripts
│   ├── error_propagation.py
│   ├── rg_flow_analysis.py
│   ├── udt_proof_core.py
│   ├── UIDT-3.6.1-Verification-visual.py
│   ├── UIDT-3.6.1-Verification.py
│   ├── verify_heavy_quark_predictions.py
│   └── verify_su3_gamma_theorem.py
└── tests/                            # Unit tests (NEVER at root level)
```

---

## Architecture Rules (enforced)

- **No `tests/` at root** — always `verification/tests/`
- **No scripts at root** — always `LOCAL/scripts/` or `verification/scripts/`
- **No `tmp/`, `temp/`, `scratch/`** in public repo
- **No `Supplementary_*/`, `Supporting_*/`** at root
- **`CANONICAL/`** is immutable — dual approval required for any change
- **`LEDGER/CLAIMS.json`** is append-only — modifications require justification + timestamp
- **`core/` and `modules/`** are protected — mass deletion (>10 lines) requires explicit confirmation

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| v3.6.1 | 2026-02-24 | Initial canonical state, VEV corrected |
| v3.7.0 | — | γ–αs correlation variant |
| v3.7.1 | — | Erratum: mass gap interpretation |
| v3.7.2 | — | HMC real simulation, DESI DR2 |
| v3.7.3 | — | Complete framework PDF |
| v3.9.4 | 2026-03-02 | 55 claims, C-068/C-069 added |
| **v3.9 canonical** | **2026-03-12** | **UIDT-OS restructured → CANONICAL/LEDGER/LOCAL. Root cleaned (PR #180–183).** |
