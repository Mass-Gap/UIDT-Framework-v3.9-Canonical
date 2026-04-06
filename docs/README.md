# UIDT Framework Documentation Index

**Version:** 3.9  
**DOI:** 10.5281/zenodo.17835200  
**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)

## Quick Navigation

### Core Documentation
- [Evidence Classification System](evidence-classification.md) - Categories A through E
- [Falsification Criteria](falsification-criteria.md) - L1-L6 limitations and kill-switches
- [Reproduction Protocol](reproduction-protocol.md) - One-command reproducibility
- [Verification Guide](verification-guide.md) - 80-digit precision testing
- [Data Availability](data-availability.md) - All simulation and verification data

### Theoretical Foundations
- [Cosmological Unification v3.9](Cosmological_Unification_v3.9.md) - H₀, Ω_m, w₀ predictions
- [Cosmological Implications v3.9](cosmological_implications_v3.9.md) - DESI/JWST/ACT alignment
- [Generation Scaling v3.9](Generation_Scaling_v3.9.md) - Quark mass hierarchy
- [Emergent Geometry Section 7](emergent_geometry_section7.md) - Geometric operator construction
- [Theoretical Notes](theoretical_notes.md) - General framework overview

### Mathematical Proofs & Derivations
- [Bare Gamma Theorem](bare_gamma_theorem.md) - γ = 16.339 calibration [A-]
- [SU(3) Gamma Conjecture Audit](su3_gamma_conjecture_audit.md) - RG fixed point analysis
- [SU(3) Gamma Proof Sketch](su3_gamma_proof_sketch.md) - 5κ² = 3λ_S constraint
- [Gribov-Cheeger Proof](gribov_cheeger_proof.md) - Topological quantization
- [GNS Hilbert Construction](gns_hilbert_construction.md) - Operator algebra
- [Kugo-Ojima Criterion](kugo_ojima_criterion.md) - Confinement mechanism

### QCD & Lattice Simulations
- [QCD Derivation](derivation_qcd.md) - Yang-Mills spectral gap
- [Schwinger-Dyson Propagator](schwinger_dyson_propagator.md) - Self-energy equations
- [Wilson Loop String Tension](wilson_loop_string_tension.md) - Confinement observable
- [Spectral Function Positivity](spectral_function_positivity.md) - Källén-Lehmann representation
- [RG 2-Loop Beta](rg_2loop_beta.md) - Renormalization group flow
- [RG Beta Derivation Gamma](rg_beta_derivation_gamma.md) - γ from RG equations

### Experimental Predictions
- [Glueball Spectrum Predictions](glueball_spectrum_predictions.md) - f₀(1710) retracted [E]
- [Heavy Quark Predictions](heavy_quark_predictions.md) - Charm and bottom masses
- [Quark Mass Hierarchy Prediction](quark_mass_hierarchy_prediction.md) - Generation scaling
- [LHC Predictions: Drell-Yan](lhc_predictions_drell_yan.md) - High-energy cross sections
- [LHCb Predictions Paper Draft](lhcb_predictions_paper_draft.md) - B-physics observables
- [DESI DR2 Alignment Report](DESI_DR2_alignment_report.md) - Cosmology validation

### Epistemic Audits & Quality Control
- [Epistemic Audit 2026-03-30](epistemic_audit_2026-03-30.md) - Evidence category review
- [First Principles Evidence Audit 2026-03-30](first_principles_evidence_audit_2026-03-30.md) - Derivation validation
- [Gamma First Principles Crosscheck 2026-03-30](gamma_first_principles_crosscheck_2026-03-30.md) - γ = 16.339 audit
- [Schwinger Mechanism Deep Research 2026-03-30](schwinger_mechanism_deep_research_2026-03-30.md) - Confinement analysis
- [Critical Review 2025](critical_review_2025.md) - Framework limitations
- [Systematic Robustness Report](systematic_robustness_report.md) - Stability analysis

### Specialized Topics
- [CE8 Derivation](CE8_derivation.md) - Exceptional Lie algebra connection
- [Factor 2.3 Derivation](Factor_2_3_Derivation.md) - Vacuum energy residual [L3]
- [Torsion Self-Energy](Torsion_Self_Energy.md) - E_T = 2.44 MeV lattice binding
- [Ghost Sector Lagrangian](ghost_sector_lagrangian.md) - BRST cohomology
- [SI Lagrangian Corrections](si_lagrangian_corrections.md) - Higher-order terms
- [Holographic BH-YM Correspondence](holographic_bh_ym_correspondence.md) - AdS/CFT connection
- [N_dof Phase Transition](ndof_phase_transition.md) - Degrees of freedom evolution
- [v Parameter Tension Note](v_parameter_tension_note.md) - v = 47.7 MeV calibration

### Statistical Methods
- [MCMC Bayesian Calibration](mcmc_bayesian_calibration.md) - Parameter estimation
- [Core Baseline Protocol](core-baseline-protocol.md) - Regression testing

### Process & Governance
- [PR Review Protocol v2.0](PR_Review_Protocol_v2.0.md) - Quality gates A-G
- [Citation Guide](citation-guide.md) - How to cite UIDT
- [Limitations](limitations.md) - Known issues L1-L6
- [Test Results v3.9.0](test_results_v3.9.0.md) - Verification suite output
- [Theory Comparison](theory_comparison.md) - UIDT vs. alternatives
- [Experimental Roadmap](experimental_roadmap.md) - Future validation plans

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

## License

See [LICENSE.md](../LICENSE.md) in the repository root.

---
**Last Updated:** 2026-04-06  
**Framework Version:** 3.9  
**Total Documents:** 50+
