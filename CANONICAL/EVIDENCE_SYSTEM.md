---
title: UIDT Evidence Classification System - Operational Specification
version: "3.7.2"
doi: 10.5281/zenodo.17835200
last_updated: "2026-01-22"
status: canonical
purpose: Operational specification for UIDT evidence classification, validation, and governance
scope: Defines system-level rules, database integration, access control, and validation protocols
maintainer: UIDT-OS Framework
---

# UIDT Evidence Classification System

## Purpose

This document serves as the **comprehensive operational specification** for the UIDT evidence classification system. It consolidates classification rules, validation logic, access control, and database integration into a single authoritative source for evidence system operations.

**Scope:**
- System-level evidence classification rules
- Database integration and synchronization protocols
- Access control and modification rights
- Validation workflows and enforcement mechanisms
- Parameter-specific rules and constraints

**Related Documents:**
- `CANONICAL/EVIDENCE.md` - Classification reference
- `LEDGER/CLAIMS.json` - Claim tracking database
- `LEDGER/claims.schema.json` - JSON schema for claims
- `LEDGER/FALSIFICATION.md` - Falsification criteria
- `SKILL.md` - Agent behavioral rules

---

## Evidence Categories

### Category A — Analytically Proven
**Definition:** Mathematical proof with residuals < 10⁻¹⁴

**Requirements:**
- Complete LaTeX derivation
- mpmath/high-precision verification
- Independent reproduction possible
- Residual threshold: |residual| < 10⁻¹⁴

**Examples:**
- Δ = 1.710 ± 0.015 GeV (spectral gap) [A]
- κ = 0.500 ± 0.008 [A]
- λ_S = 5κ²/3 = 0.41̄6̄ ± 0.007 [A]
- 5κ² = 3λ_S constraint [A]
- v = 47.7 MeV [A]

---

### Category A- — Phenomenologically Determined
**Definition:** High-precision determination without first-principles derivation

**Requirements:**
- Clear methodology documented
- Numerical precision established
- Acknowledges phenomenological nature

**Examples:**
- γ = 16.339 (kinetic VEV) [A-]
- γ = 16.374 ± 1.005 (MC mean) [A-]

> **Special Rule:** γ MUST always be [A-], NEVER [A]. See CANONICAL/LIMITATIONS.md L4.

---

### Category B — Numerically Verified / Lattice Consistent
**Definition:** Agreement with independent numerical/lattice calculations

**Requirements:**
- z-score < 1σ for consistency
- Reference to external calculation
- Statistical methodology documented

**Examples:**
- Lattice QCD consistency: z = 0.37σ [B]
- Branch 1 residual: 3.2×10⁻¹⁴ [B]

---

### Category C — Calibrated to External Data
**Definition:** Fitted to observational/experimental data

> ⚠️ **RULE:** ALL cosmology claims MUST be Category C or lower. NEVER A/B.

**Examples:**
- H₀ = 70.4 ± 0.16 km/s/Mpc (DESI DR2) [C]
- λ_UIDT = 0.660 ± 0.005 nm [C]
- S₈ = 0.814 ± 0.009 [C]

---

### Category D — Predictive, Unverified
**Definition:** Theoretical prediction awaiting experimental test

**Examples:**
- Casimir anomaly: +0.59% at 0.66 nm [D]
- m_S = 1.705 ± 0.015 GeV [D]
- LHC scalar resonance 1.5-1.9 GeV [D]

---

### Category E — Speculative / Open / Withdrawn
**Sub-types:** E-speculative, E-open, E-withdrawn

**Examples:**
- γ RG derivation [E-open]
- Glueball ID [E-withdrawn, 2025-12-25]
- N=99 justification [E-open]

---

## Evidence Category Summary

| Category | Description | Residual Threshold | Cosmology Allowed | Requires Derivation |
|----------|-------------|-------------------|-------------------|---------------------|
| A | Analytically Proven | < 10⁻¹⁴ | ❌ No | ✅ Full |
| A- | Phenomenologically Determined | N/A | ❌ No | ⚠️ Phenomenological |
| B | Numerically Verified | z < 1σ | ❌ No | ✅ Numerical |
| C | Calibrated to External Data | N/A | ✅ Yes (max) | ❌ Calibration only |
| D | Predictive, Unverified | N/A | ✅ Yes | ❌ Prediction only |
| E | Speculative/Open/Withdrawn | N/A | ✅ Yes | ❌ Speculative |

---

## Upgrade / Downgrade Rules

### Upgrade Path
```
E → D: Theoretical foundation established
D → C: Calibration to data achieved
C → B: Independent numerical verification
B → A-: Systematic derivation (phenomenological)
A- → A: First-principles derivation with < 10⁻¹⁴ residuals
```

### Downgrade Triggers
```
A → B: Residuals exceed 10⁻¹⁴
B → C: Lattice inconsistency (z > 3σ)
C → D: Data source invalidated
D → E: Experimental falsification
Any → E-withdrawn: Explicit retraction
```

### Documentation Requirement
Every category change MUST be logged in `LEDGER/CLAIMS.json` with timestamp, previous/new category, justification, and reference.

---

## Parameter Quick Reference

| Parameter | Symbol | Evidence | Reason |
|-----------|--------|----------|--------|
| Spectral Gap | Δ | A | Analytical proof, residual < 10⁻¹⁴ |
| Gamma Invariant | γ | A- | Phenomenological, NOT from RG |
| Coupling | κ | A | RG fixed point |
| Self-Coupling | λ_S | A | RG fixed point, perturbative |
| VEV | v | A | Corrected v3.6.1 |
| Scalar Mass | m_S | D | Prediction, awaiting LHC |
| Hubble Constant | H₀ | C | DESI DR2 calibrated |
| Casimir Anomaly | ΔF/F | D | Prediction, falsifiable |

---

**CITATION:** Rietz, P. (2025). UIDT v3.7.2. DOI: 10.5281/zenodo.17835200
