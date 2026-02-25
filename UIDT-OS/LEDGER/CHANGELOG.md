# UIDT-OS Changelog

All notable changes to claims, parameters, and concepts.

Format: [CLAIM-ID] [DATE] [OLD→NEW] [REASON]

## [TICK-20260224-Phase3_Discoveries] — Phase 3 Discoveries

### Track A: SU(3) Gamma Theorem
- NEW: docs/su3_gamma_theorem.md — L4 candidate resolution
- NEW: verification/scripts/verify_su3_gamma_theorem.py
- NEW: UIDT-C-056, UIDT-C-057 in CLAIMS.json
- MOD: L4 status → "candidate_solution_identified"
- Limitation impact: L4 (partial)

### Track B: Heavy Quark Spectroscopy
- NEW: docs/heavy_quark_predictions.md
- NEW: docs/lhcb_predictions_paper_draft.md
- NEW: verification/scripts/verify_heavy_quark_predictions.py
- NEW: UIDT-C-058, UIDT-C-059 in CLAIMS.json
- MOD: harmonic_predictions.py — uncertainty propagation added

---

## [v3.9.2] - 2026-02-24

### Unified PRX Corpus Assimilation
- **Claim ID:** UIDT-C-043, UIDT-C-044
- **New Value:** Formal integration of CSF macro-mechanics.
- **Category:** `[C]` Phenomenological mapping.
- **Reason:** Constitutional remediation enforced. Removed false `[A-]` claims; EoS correctly registered as placeholder variants.
- **Verification:** `verify_csf_unification.py`

---

## [v1.0.0] - 2026-01-22

### Initial Release
- Created UIDT-OS from SKILL v5.2 + GROK-UIDT-OS integration
- Migrated 18 claims from Framework v3.7.2
- Established A-E evidence classification
- Implemented MUST/MUST-NOT loading protocol

### Claims Status at v1.0.0
| Category | Count |
|----------|-------|
| A (proven) | 7 |
| A- (phenomenological) | 2 |
| B (numerical) | 2 |
| C (calibrated) | 1 |
| D (predicted) | 2 |
| E (speculative/withdrawn) | 4 |

---

## Historical Changes (Pre-UIDT-OS)

### [2025-12-25] Glueball Withdrawal
- **UIDT-C-015:** verified [B] → withdrawn [E]
- **Reason:** Δ = 1.710 GeV is spectral gap, NOT particle mass
- **Impact:** Interpretation-only, numerical results unchanged

### [2025-12-20] H₀ Update (v3.7.2)
- **UIDT-C-008:** 70.92 ± 0.40 → 70.4 ± 0.16 km/s/Mpc
- **Source:** DESI DR2 calibration
- **Category:** Remains C (calibrated)

### [2025-11-15] VEV Correction (v3.6.1)
- **UIDT-C-004:** 0.854 MeV → 47.7 MeV
- **Reason:** Calculation error in v3.2
- **Impact:** Major correction, all derived quantities updated

---

## Change Log Template

```
### [YYYY-MM-DD] Change Title
- **Claim ID:** UIDT-C-XXX
- **Old Value:** ...
- **New Value:** ...
- **Category Change:** X → Y (if applicable)
- **Reason:** ...
- **Verification:** Script/Reference
- **Impact:** ...
```

---

## Pending Reviews

| Claim | Next Review | Trigger |
|-------|-------------|---------|
| UIDT-C-008 (H₀) | DESI DR3 | w measurement precision |
| UIDT-C-009 (Casimir) | Experimental | Sub-nm force measurement |
| UIDT-C-007 (m_S) | LHC Run 4 | Low-mass scalar search |

---

**Maintainer:** Philipp Rietz  
**DOI:** 10.5281/zenodo.17835200
