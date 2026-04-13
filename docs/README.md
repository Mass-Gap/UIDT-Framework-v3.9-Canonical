# UIDT Framework Documentation Index

**Version:** 3.9  
**DOI:** 10.5281/zenodo.17835200  
**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)

## Quick Navigation

### 📐 Foundations (Mathematical Proofs - Clay Math Relevant)
- [Bare Gamma Theorem](foundations/bare_gamma_theorem.md) - γ = 16.339 calibration [A-]
- [SU(3) Gamma Conjecture Audit](foundations/su3_gamma_conjecture_audit.md) - RG fixed point analysis
- [SU(3) Gamma Proof Sketch](foundations/su3_gamma_proof_sketch.md) - 5κ² = 3λ_S constraint
- [Gribov-Cheeger Proof](foundations/gribov_cheeger_proof.md) - Topological quantization
- [GNS Hilbert Construction](foundations/gns_hilbert_construction.md) - Operator algebra
- [Kugo-Ojima Criterion](foundations/kugo_ojima_criterion.md) - Confinement mechanism
- [CE8 Derivation](foundations/CE8_derivation.md) - Exceptional Lie algebra connection
- [Factor 2.3 Derivation](foundations/Factor_2_3_Derivation.md) - Vacuum energy residual [L3]
- [Torsion Self-Energy](foundations/Torsion_Self_Energy.md) - E_T = 2.44 MeV lattice binding
- [Ghost Sector Lagrangian](foundations/ghost_sector_lagrangian.md) - BRST cohomology
- [SI Lagrangian Corrections](foundations/si_lagrangian_corrections.md) - Higher-order terms

### ⚛️ QCD & Lattice (CERN/FLAG/ILDG Relevant)
- [QCD Derivation](qcd-lattice/derivation_qcd.md) - Yang-Mills spectral gap
- [Schwinger-Dyson Propagator](qcd-lattice/schwinger_dyson_propagator.md) - Self-energy equations
- [Wilson Loop String Tension](qcd-lattice/wilson_loop_string_tension.md) - Confinement observable
- [Spectral Function Positivity](qcd-lattice/spectral_function_positivity.md) - Källén-Lehmann representation
- [RG 2-Loop Beta](qcd-lattice/rg_2loop_beta.md) - Renormalization group flow
- [RG Beta Derivation Gamma](qcd-lattice/rg_beta_derivation_gamma.md) - γ from RG equations
- [N_dof Phase Transition](qcd-lattice/ndof_phase_transition.md) - Degrees of freedom evolution
- [Holographic BH-YM Correspondence](qcd-lattice/holographic_bh_ym_correspondence.md) - AdS/CFT connection
- [MCMC Bayesian Calibration](qcd-lattice/mcmc_bayesian_calibration.md) - Parameter estimation

### 🔬 Predictions (Experimental - LHC/DESI)
- [Glueball Spectrum Predictions](predictions/glueball_spectrum_predictions.md) - f₀(1710) retracted [E]
- [Heavy Quark Predictions](predictions/heavy_quark_predictions.md) - Charm and bottom masses
- [Quark Mass Hierarchy Prediction](predictions/quark_mass_hierarchy_prediction.md) - Generation scaling
- [LHC Predictions: Drell-Yan](predictions/lhc_predictions_drell_yan.md) - High-energy cross sections
- [LHCb Predictions Paper Draft](predictions/lhcb_predictions_paper_draft.md) - B-physics observables
- [DESI DR2 Alignment Report](predictions/DESI_DR2_alignment_report.md) - Cosmology validation
- [Cosmological Unification v3.9](predictions/Cosmological_Unification_v3.9.md) - H₀, Ω_m, w₀ predictions
- [Cosmological Implications v3.9](predictions/cosmological_implications_v3.9.md) - DESI/JWST/ACT alignment
- [Generation Scaling v3.9](predictions/Generation_Scaling_v3.9.md) - Quark mass hierarchy
- [Emergent Geometry Section 7](predictions/emergent_geometry_section7.md) - Geometric operator construction
- [v Parameter Tension Note](predictions/v_parameter_tension_note.md) - v = 47.7 MeV calibration

### 📋 Governance (Quality & Standards)
- [Evidence Classification System](governance/evidence-classification.md) - Categories A through E
- [Falsification Criteria](governance/falsification-criteria.md) - L1-L6 limitations and kill-switches
- [Limitations](governance/limitations.md) - Known issues L1-L6
- [Reproduction Protocol](governance/reproduction-protocol.md) - One-command reproducibility
- [Verification Guide](governance/verification-guide.md) - 80-digit precision testing
- [Data Availability](governance/data-availability.md) - All simulation and verification data
- [Citation Guide](governance/citation-guide.md) - How to cite UIDT
- [Core Baseline Protocol](governance/core-baseline-protocol.md) - Regression testing
- [PR Review Protocol v2.0](governance/PR_Review_Protocol_v2.0.md) - Quality gates A-G
- [Experimental Roadmap](governance/experimental_roadmap.md) - Future validation plans
- [Theory Comparison](governance/theory_comparison.md) - UIDT vs. alternatives
- [Theoretical Notes](governance/theoretical_notes.md) - General framework overview

### 🔍 Audits (Epistemic Quality Control)
- [Epistemic Audit 2026-03-30](audits/epistemic_audit_2026-03-30.md) - Evidence category review
- [First Principles Evidence Audit 2026-03-30](audits/first_principles_evidence_audit_2026-03-30.md) - Derivation validation
- [Gamma First Principles Crosscheck 2026-03-30](audits/gamma_first_principles_crosscheck_2026-03-30.md) - γ = 16.339 audit
- [Schwinger Mechanism Deep Research 2026-03-30](audits/schwinger_mechanism_deep_research_2026-03-30.md) - Confinement analysis
- [Critical Review 2025](audits/critical_review_2025.md) - Framework limitations
- [Systematic Robustness Report](audits/systematic_robustness_report.md) - Stability analysis
- [Test Results v3.9.0](audits/test_results_v3.9.0.md) - Verification suite output

### Subdirectories
- [archival-notes/](archival-notes/) - Historical development notes
- [archive/](archive/) - Deprecated or superseded documents
- [qa/](qa/) - Quality assurance reports and PR reviews
- [research/](research/) - Ongoing research and exploratory work

## Evidence Categories

All quantitative claims in UIDT are tagged with evidence categories:

| Category | Name | Threshold |
|----------|------|-----------|
| **[A]** | Mathematically Proven | Residual < 10⁻¹⁴ |
| **[A-]** | Phenomenologically Determined | Calibrated, permanent |
| **[B]** | Lattice QCD Consistent | z ≈ 0.37σ |
| **[C]** | Calibrated | DESI/JWST/ACT data |
| **[D]** | Predicted | Unconfirmed |
| **[E]** | Withdrawn/Speculative | Retracted |

## Known Limitations

- **L1:** 10¹⁰ geometric factor - UNEXPLAINED
- **L2:** Electron mass - 23% residual
- **L3:** Vacuum energy - factor 2.3 residual
- **L4:** γ = 16.339 - NOT derived from RG first principles [A-]
- **L5:** N = 99 RG steps - empirically chosen
- **L6:** Glueball f₀(1710) - RETRACTED [E] since 2025-12-25

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) in the repository root for guidelines on:
- Evidence classification requirements
- Numerical precision standards (mp.dps = 80)
- PR review protocol
- Anti-tampering rules

## File System Laws (Extended)

This documentation structure enforces the following File System Laws:

### Original Laws (L-FS-01 through L-FS-10)
See the repository's file structure governance documentation.

### Extended Laws for External Research Compatibility

| Law | Description | Rationale |
|-----|-------------|-----------|
| **L-FS-11** | **External Metadaten-Pflicht**: Every publication-relevant directory (`clay-submission/`, `manuscript/`, `docs/`) must contain `metadata.yaml` or `codemeta.json` with Dublin-Core-compatible fields. | HAL/Zenodo/CDS interoperability |
| **L-FS-12** | **Reproduzierbarkeits-Manifest**: Every directory with verification/simulation code must contain a `reana.yaml`-compatible workflow description or at minimum a `REPRODUCE.md`. | CERN CAP/REANA compatibility |
| **L-FS-13** | **Docs-Taxonomie**: `docs/` follows a four-layer taxonomy: `foundations/`, `qcd-lattice/`, `predictions/`, `governance/`, `audits/`. | FLAG-Review compatibility, reviewer orientation |

### Compliance Status

- ✅ **L-FS-11:** `docs/metadata.yaml` and `clay-submission/metadata.yaml` created (Dublin Core)
- ✅ **L-FS-12:** `clay-submission/REPRODUCE.md` created (REANA-compatible)
- ✅ **L-FS-13:** Four-layer taxonomy implemented (50+ documents organized)

## License

See [LICENSE.md](../LICENSE.md) in the repository root.

---
**Last Updated:** 2026-04-06  
**Framework Version:** 3.9  
**Total Documents:** 50+
