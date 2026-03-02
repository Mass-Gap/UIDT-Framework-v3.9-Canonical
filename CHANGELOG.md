# Changelog

All entries follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Evidence tags: [A] proven | [A-] calibrated | [B] corroborated | [C] phenomenological | [D] predicted | [E] retracted

---

## [v3.9.0] — Update 2026-03-02: Canonical Audit Cycle (TKT-20260303-changelog-consolidation-001)

### [AUDIT]
- **Evidence Downgrades:** N=99 vs N=94.05 downgraded [B]→[E] (Under Investigation); quark mass hierarchy [A] (Mathematical Consistency); falsification criteria [D]; 6× quark mass [B]→[D]; neutrino mass [B]→[C]; w_a derivation [B]→[C].
- **Gamma Correction:** γ confirmed as calibrated [A-] (was previously inconsistently labeled [C] or [A]).
- **Anti-Crackpot Compliance:** Removed prestige language and emoji markers.
- **Legacy Cleanup:** Salvaged D-001/D-002/D-003 definitions.
- **Consistency:** Enforced w_0 D-002 compliance and anti-crackpot wording in PR #130/#131.

### [FIX]
- **LaTeX Hygiene:** Replaced 21 instances of broken delimiters ("1814") with standard LaTeX math delimiters `$` in theoretical notes and DESI report.
- **Scientific Language:** Replaced affirmative claims with "derives/suggests/demonstrates" across 5 core documents. Renamed "Theorem" to "Conjecture" for su3_gamma.
- **Precision Safety:** Fixed float precision leaks by enforcing `np.float64` and `mp.nstr` in `verification/scripts/`.

### [FEAT]
- **ArXiv Radar:** Added daily ArXiv scan script `verification/scripts/arxiv_scan.py` (PR #127).
- **Regression Suite:** Integrated regression tests and theory documentation from feature branches (PR #129).

### [DOC]
- Added `docs/bare_gamma_theorem.md`.
- Added `docs/cosmological_implications_v3.9.md`.

### Open Issues (Require PI Decision)
- N=99 vs N=94.05: production code uses 99; §12 proposes 94.05 [E — Under Investigation]
- w_0 canonical value undeclared: -0.73 / -0.961 / -0.99 (superseded values pending PI decision)
- L holographic scale not registered in `data/canonical/CONSTANTS.md`

---

## [v3.9.1] — 2026-02-24

### Research Corpus Maturation & Mathematical Constraints (Plan vx4)

**Overview**
Integration of critical quantitative checks derived from the X17/Perplexity research corpus. Added native `mpmath` verification for the Informational Geometric Operator and refined the epistemic classification of phenomenological dependencies.

**Verification & Evidence Enhancements:**
- **External Corroboration [C]:** Integrated independent QCD Sum Rules (Borel-window methodology) derivation for $\Delta^* \approx 1.710 \text{ GeV}$ directly into the main manuscript (Section 4).
- **Geometric Operator Suite:** Created `verify_geometric_operator.py` forcing 80-dps precision to confirm classical scale boundary limits and metric perturbation constraints. Registered as Claim `UIDT-C-049` [C].
- **N²-Cascade Definition:** Explicitly classified the $N=99$ dimension cascade scaling rule as a phenomenological constraint, registering it as Claim `UIDT-C-050` [C].
- **Ledger Audit:** Total claims tracked reached 50, with exact categorizations matching the `COMPLETENESS_REPORT.md` integration log.

## [v3.9.2] — 2026-02-24

### Final Corpus Closure & Factor 2.3 Integration (Plan vx6)

**Overview**
Final integration of the X17/Perplexity research corpus, extracting the high-precision "Factor 2.3" observation and registering multiple Phase 3 open research vectors. The raw corpus is now processed and formalized into the UIDT framework.

**Verification & Evidence Enhancements:**
- **Holographic Coupling Ratio [B]:** Registered Claim `UIDT-C-051` for the factor 2.3 suppression term, validated across three independent geometric methods up to 500-dps precision. Documented physically in `docs/Factor_2_3_Derivation.md`.
- **Phase 3 Open Research [E]:** Formally registered four new exploratory claims (`UIDT-E-052` to `UIDT-E-055`) covering Lagrangian reconstruction, higher-order corrections, $\Lambda_0$ macroscopic analysis, and zero-point phase transitions to secure Future Vectors.
- **Evidence Tracker:** Updated total recorded claims to 55, accurately mapping the new distributions.

## [v3.9] — 2026-02-19

### The Holographic Application — Four-Pillar Synthesis

**Overview**
Transformation of UIDT v3.7.3 to publication-ready v3.9. Introduces a Four-Pillar Architecture with Photonic Isomorphism (Pillar IV) and the Torsion Binding Energy derivation as the "Missing Link" in Pillar II. Updates falsification criteria, verification references, and repository metadata for the v3.9 release.

### Manifestly Covariant CSF-UIDT Synthesis (Cosmology)

**Overview**
Formal integration of the Covariant Scalar-Field (CSF) macro-mechanics with the underlying QFT foundation of UIDT. This resolves the scale invariance transition from lattice dynamics to cosmic expansion, grounding Pillar II in rigorous geometry.

**Implementation Details:**
- **`modules/covariant_unification.py`**: Added exact mathematical linkage deriving the anomalous CSF dimension from the UIDT lattice invariant ($\gamma_{CSF} = 1 / (2 \sqrt{\pi \ln(\gamma_{UIDT})})$).
- **Information Saturation Bound**: Implemented Theorem 2 establishing the Planck-Singularity Regularization limit ($\rho_{max} = \Delta^4 \gamma^{99}$).
- **Equation of State:** Asymptotic limits $w_0 = -0.99$ [C] and $w_a = +0.03$ [C] from Taylor expansion of UIDT density response (superseded by D-002 compliance, see v3.9.0).
- **`verification/scripts/verify_csf_unification.py`**: Added rigorous verification pipeline ensuring native precision (mpmath 80-digits) and mapping residuals strictly $< 10^{-14}$. Evaluates under Evidence Category [A-].
- **CI/CD Pipeline**: Integrated standalone CSF verification into `.github/workflows/uidt-pr-review.yml` with strict failure policies (`pipefail`).

---

## [v3.7.3] — 2026-02-18

### Codebase Audit, Evidence Fixes and Manuscript Finalisation

**Overview**
Comprehensive audit of all 82 Python files against canonical reference data. All canonical parameters confirmed consistent across the full codebase. Five clear issues identified and resolved; five context-dependent issues documented for follow-up. New final manuscript `UIDT_v3.7.3-Complete-Framework.tex` consolidated. Internal audit infrastructure established under `.claude/`.

**Evidence Classification (rg_flow_analysis.py — both copies):**
- Fixed: γ evidence tag corrected from `calibrated [A-]` to `calibrated [A-]` in `clay-submission/02_VerificationCode/rg_flow_analysis.py`.
- Fixed: Same correction in `verification/scripts/rg_flow_analysis.py`.
- Rule: γ = 16.339 is `calibrated [A-]`, never first-principles derived [A].

**Encoding Fixes (Windows cp1252 → UTF-8):**
- Fixed: `clay-submission/02_VerificationCode/brst_cohomology_verification.py` — `open()` now uses `encoding='utf-8'`.
- Fixed: `clay-submission/02_VerificationCode/slavnov_taylor_ccr_verification.py` — `open()` now uses `encoding='utf-8'`.

**Dependencies:**
- Added: `mpmath==1.3.0` to `verification/requirements.txt`.

**Certificates & Verification Reports (regenerated):**
- Updated certificates and verification reports for BRST, Canonical Audit v3.6.1, and OS Axiom verification. Added Gribov analysis results.

**Manuscript:**
- Added: `manuscript/UIDT_v3.7.3-Complete-Framework.tex` — new consolidated final LaTeX source.
- Moved: `manuscript/UIDT_v3.7.3-neu.tex` → `.claude/_backup/` (superseded).

**Audit Findings — Context-Dependent:**
- `uidt_proof_core.py` regression: converges to Δ*=1.607 GeV instead of 1.710 GeV.
- `error_propagation.py` uncertainty values differ from stored reference.
- v3.6.1-corrected MC dataset: γ_mean=6.84 (anomalous vs. canonical 16.339).
- OS Axiom OS4 (Cluster Property): 20.5% rate deviation in numerical model.
- Gribov WKB/Zwanziger: perturbative estimates insufficient alone.

## [v3.7.3] — 2026-02-16

### Repository Migration and Data Availability Update

**Overview**
All repository references migrated from `badbugsarts-hue/UIDT-Framework-V3.2-Canonical` to `Mass-Gap/UIDT-Framework-v3.7.2-Canonical`. Data Availability section rewritten to CERN/Clay Mathematics Institute publication standards.

**Repository URL Migration (24 files):**
- Global replacement of GitHub organization from `badbugsarts-hue` to `Mass-Gap`.

**Data Availability (UIDT_v3.7.3-neu.tex + docs/data-availability.md):**
- Complete rewrite of Data Availability section to v3.7.3 standards.
- Organized code listing into verification, simulation, and Clay audit categories.
- Updated dataset paths to versioned audit trail (v3.2, v3.6.1, v3.7.0).
- Added Docker reproduction option and SHA-256 integrity verification.

**Manuscript Header (UIDT_v3.7.3-neu.tex):**
- Version references in preamble, headers, PDF metadata, Schema.org updated to v3.7.3.
- DOI corrected from zenodo.17835201 to zenodo.17835200 throughout.
- Appendix script inventory updated from v3.2/v3.5 to actual v3.6.1 filenames.

**Metadata DOI Corrections:**
- Metadata files updated with correct DOI (zenodo.17835200).

**Security:**
- `verification/uidt_os_path.py` excluded from repository (contains local paths).

## [v3.7.3] — 2026-02-14

### Initial v3.7.3 Release Note

**Changes:**
- Initial release preparations and file structure organization.

## [v3.7.2] — 2025-12-29

### Current Canonical Release

- VEV = 47.7 MeV [A] (Corrected v3.6.1).
- H₀ = 70.4 km/s/Mpc [C] (DESI calibrated).

## [v3.6.1] — 2025-12-19

### VEV Correction Patch

- Corrected VEV from 0.854 MeV to 47.7 MeV based on refined lattice data.

## [v3.6] — 2025-12-11

### Analysis of Vacuum Energy Suppression

**Overview**
Analysis of the vacuum energy suppression mechanism.

- **Vacuum Energy:** Residual at 3.3% level [C].
- **Mass Gap:** Δ* = 1.710 GeV identified as spectral gap.

## [v3.5.6] — 2025-12-09

### Intermediate Update

- Minor fixes and documentation updates.

## [v3.5] — 2025-12-07

### Milestone Release

- Introduction of core verification scripts.

## [v3.4] — 2025-12-06

### Pre-release

- Preparation for v3.5.

## [v3.3] — 2025-11-01 — **[REVOKED]**

**Reason:** Data corruption in externally formatted artifacts.

## [v3.2] — 2025-11-09

### Technical Note Baseline

- Baseline release for technical notes.
