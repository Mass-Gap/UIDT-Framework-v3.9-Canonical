# UIDT Framework Verification System

Verification infrastructure for the Unified Information-Density Theory framework.

**DOI:** 10.5281/zenodo.17835200  
**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)

## Directory Structure

```
verification/
├── audits/              # Audit scripts for framework integrity
├── registries/          # Machine-readable parameter and axiom registries
├── scripts/             # Verification test scripts
├── data/                # Verification data and reports
├── results/             # Audit outputs and test results
│   └── audits/          # Audit-specific results
└── tests/               # Unit tests for verification system
```

## Registries

Machine-readable specifications of framework parameters and axioms.

### axioms_registry.json
Formal axioms with dependency graph and evidence references.

### symbol_registry.json
Canonical parameters with values, uncertainties, and evidence categories.

### units_registry.json
Dimensional analysis specifications for all parameters.

### tickets_registry.json
Verification tickets with status tracking and evidence links.

## Audit Scripts

Located in `verification/audits/`. All scripts:
- Use `mpmath.mp.dps = 80` for numerical precision
- Exit with code 0 on success, 1 on failure
- Generate JSON output in `verification/results/audits/`
- Follow UIDT Constitution rules

### Core Audits

**framework_integrity_audit.py**  
Comprehensive multi-pass audit covering structural integrity, formal consistency, 
phenomenological coherence, and strategic alignment.

**proof_completeness_audit.py**  
Verifies all axioms have complete derivation chains.

**symbol_consistency_check.py**  
Checks for duplicate or inconsistent symbol definitions.

**dimensional_analysis.py**  
Verifies dimensional consistency of all parameters.

**tolerance_enforcement.py**  
Ensures all measurements include proper uncertainties.

**formal_dependency_graph.py**  
Generates formal dependency graph from axioms.

**parameter_drift_detector.py**  
Detects parameter changes across versions.

### Strategic Audits

**scope_drift_audit.py**  
Analyzes framework evolution to detect scope expansion beyond core problem.

**feature_creep_audit.py**  
Monitors module count and structural complexity growth.

**symbol_growth_audit.py**  
Tracks symbol registry growth rate and theorem-to-hypothesis ratio.

### Validation Audits

**falsification_thresholds_extract.py**  
Extracts operational falsification criteria from framework parameters.

**claims_test_coverage_map.py**  
Maps theoretical claims to verification scripts.

**manuscript_consistency_audit.py**  
Verifies consistency between manuscript claims and computational results.

**release_regression_audit.py**  
Verifies theoretical consistency across framework releases.

**global_assessment_audit.py**  
Synthesizes all audit results to identify weakest evidence domains and risks.

## Usage

Run individual audits:
```bash
python verification/audits/proof_completeness_audit.py
python verification/audits/dimensional_analysis.py
```

Run comprehensive framework audit:
```bash
python verification/audits/framework_integrity_audit.py
```

## Evidence Categories

All parameters carry evidence tags:

- **[A]** Analytically Proven (residuals < 10⁻¹⁴)
- **[A-]** Phenomenologically Determined
- **[B]** Numerically Verified / Lattice Consistent
- **[C]** Calibrated to External Data
- **[D]** Predictive, Unverified
- **[E]** Speculative / Open / Withdrawn

## Numerical Requirements

All verification scripts must:
- Declare `mp.dps = 80` locally (never centralized)
- Use native `mpmath` objects (no mocking)
- Verify residuals < 10⁻¹⁴ for Category A claims
- Verify residuals < 10⁻² for phenomenological constraints

## Known Limitations

- **L1** 10¹⁰ geometric factor: UNEXPLAINED
- **L2** Electron mass: 23% residual, under investigation
- **L3** Vacuum energy residual: factor 2.3
- **L4** γ NOT derived from RG first principles [A-]
- **L5** N=99 RG steps: empirically chosen
- **L6** Glueball f0(1710): RETRACTED [E] since 2025-12-25

---

**Maintainer:** P. Rietz  
**Email:** badbugs.arts@gmail.com  
**Framework Version:** UIDT v3.9
