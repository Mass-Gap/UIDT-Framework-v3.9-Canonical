# CHANGELOG Audit History Archive — v3.7.3 and Earlier

> **Source:** Entries removed from CHANGELOG.md in PR #201 (commit `38fb409`)  
> **Archived:** 2026-04-05 by audit remediation (Finding F6)  
> **Reason:** PR #201 consolidated CHANGELOG entries, removing historical
> audit findings and version details. This archive preserves the full
> record for traceability.

---

## Archived Entries from v3.7.3 Codebase Audit

The following findings were documented during the v3.7.3 codebase audit
and subsequently removed when CHANGELOG.md was consolidated:

### Context-Dependent Audit Findings (v3.7.3)

These findings were flagged during the comprehensive audit of 82 Python
files against canonical reference data:

1. **`uidt_proof_core.py` regression:** Converges to Δ\* = 1.607 GeV instead
   of 1.710 GeV. This represents a ~6% deviation from the canonical spectral
   gap value [A] and requires investigation of the convergence parameters.

2. **`error_propagation.py` uncertainty values:** Differ from stored reference
   data. The propagated uncertainties need cross-validation against the
   canonical parameter uncertainties in CONSTANTS.md.

3. **v3.6.1-corrected MC dataset anomaly:** γ\_mean = 6.84, which is
   anomalous compared to the canonical γ = 16.339 [A-]. This MC dataset
   produces a value ~58% below the calibrated parameter, suggesting either
   a systematic error in the MC sampling or a different physical regime.

4. **OS Axiom OS4 (Cluster Property):** 20.5% rate deviation in numerical
   model. The Cluster Property verification shows a non-trivial deviation
   that may indicate finite-size effects or algorithmic limitations.

5. **Gribov WKB/Zwanziger estimates:** Perturbative estimates found
   insufficient alone for establishing the Gribov-Zwanziger mechanism
   at the required precision.

### Certificates and Verification Reports (Regenerated)

Updated certificates and verification reports for:
- BRST cohomology verification
- Canonical Audit v3.6.1
- OS Axiom verification
- Gribov analysis results

### Manuscript Consolidation

- Added: `manuscript/UIDT_v3.7.3-Complete-Framework.tex` — consolidated
  final LaTeX source.
- Moved: `manuscript/UIDT_v3.7.3-neu.tex` → `.claude/_backup/` (superseded).

---

## Archived Entries from v3.7.3 Repository Migration

### Full Migration Details

The following details were condensed in PR #201:

- **Repository URL Migration (24 files):** Global replacement of GitHub
  organization from `badbugsarts-hue` to `Mass-Gap`.
- **Data Availability rewrite:** Complete rewrite to v3.7.3 standards.
  Organized code listing into verification, simulation, and Clay audit
  categories. Updated dataset paths to versioned audit trail (v3.2, v3.6.1,
  v3.7.0). Added Docker reproduction option and SHA-256 integrity verification.
- **Manuscript Header updates:** Version references in preamble, headers,
  PDF metadata, Schema.org updated to v3.7.3. DOI corrected from
  zenodo.17835201 to zenodo.17835200 throughout. Appendix script inventory
  updated from v3.2/v3.5 to actual v3.6.1 filenames.
- **Metadata DOI Corrections:** Metadata files updated with correct DOI
  (zenodo.17835200).
- **Security:** `verification/uidt_os_path.py` excluded from repository
  (contains local paths).

---

## Archived Version Entries (Pre-v3.7.2)

### v3.7.3 — 2026-02-14: Initial Release Note

Initial release preparations and file structure organization.

### v3.6 — 2025-12-11: Vacuum Energy Suppression

Analysis of the vacuum energy suppression mechanism.

### v3.5.6 — 2025-12-09: Intermediate Update

Minor fixes and documentation updates.

### v3.5 — 2025-12-07: Milestone Release

Introduction of core verification scripts.

### v3.4 — 2025-12-06: Pre-release

Preparation for v3.5.

---

## Encoding Fixes (Full Detail)

Consolidated in PR #201; original detail preserved here:

- Fixed: `clay-submission/02_VerificationCode/brst_cohomology_verification.py`
  — `open()` now uses `encoding='utf-8'`.
- Fixed: `clay-submission/02_VerificationCode/slavnov_taylor_ccr_verification.py`
  — `open()` now uses `encoding='utf-8'`.

---

*Archive created by audit remediation (OPUS-001 Finding F6).  
Maintainer: P. Rietz — DOI: 10.5281/zenodo.17835200*
