# Changelog

All entries follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Evidence tags: [A] proven | [A-] calibrated | [B] corroborated | [C] phenomenological | [D] predicted | [E] retracted

---

## [v3.9.9] — 2026-04-29: Monte Carlo Validation Baseline Restore

### [DATA]
- **Monte Carlo Restore (v3.2/v3.3):** Re-integration of 11 primary validation datasets from internal storage into `simulation/monte_carlo/`.
  - Files: `UIDT_MonteCarlo_summary.csv`, `UIDT_MonteCarlo_correlation_matrix.csv`, `UIDT_MC_Distribution_Plots.png`, etc.
  - Evidence: [C] (Calibrated validation baseline).
  - DOI: 10.5281/zenodo.17554179.

### [FIX]
- **README consistency:** Corrected plot file extensions in `simulation/monte_carlo/README.md` from `.jpg` to `.png` to match actual high-resolution artifacts.
- **Path Cleanup:** Removed redundant/legacy README copies from target directory to maintain structural integrity.

### [VERIFY]
- **Baseline Audit:** Automated verification via `verification/tests/test_monte_carlo_summary.py`.
  - Status: 10/10 PASSED.
  - Results: Mean γ = 16.374 ± 1.005, Correlation r(γ, Ψ) > 0.999.
  - Precision: Native mpmath 80-dps residual check < 10⁻¹⁴ vs. Ledger values.

---

## [v3.9.5] — 2026-04-03: RG Precision Fix & Epistemic Audit Formalisation


### [FIX]
- **TKT-20260403-LAMBDA-FIX:** `λ_S` corrected from rounded decimal 0.417 to exact RG fixed-point definition `5κ²/3 = 0.41̄6̄` in `CANONICAL/CONSTANTS.md`.
  - Deviation: |0.41̄6̄ − 0.417| = 3.3̄ × 10⁻⁴ (within ledger uncertainty ±0.007; **no physics change**).
  - RG constraint residual upgraded: 10⁻³ → < 10⁻¹⁴ (Constitution-compliant).
  - Source: PR #199 audit (§3, `docs/su3_gamma_theorem.md`). Branch: `fix/TKT-20260403-lambda-exact-fixpoint`.

### [AUDIT — Session 2026-04-03]
- **C-γ-01 (PR #199):** Formal derivation of `γ = (2N_c+1)²/N_c` from gap equation **not established**. Closed-form yields γ_closed ≈ 1.908, not 16.339. Evidence [A-] unchanged. Limitation L4 remains open.
- **C-γ-02 downgraded [E] (PR #199):** Claim `δγ = δ_NLO` (Wetterich FRG) not supported. Factor ~9 discrepancy (δ_NLO ≈ 0.0437 vs δγ = 0.0047). New ticket: TKT-20260403-FRG-NLO.
- **[RG_CONSTRAINT_FAIL] resolved (PR #199 → this PR):** Triggered by `λ_S = 0.417` rounding. Fixed by exact definition (see above).
- **γ algebraic derivation (PR #199 §1.4):** `γ = Δ*/v` is a **definitional identity**, not an algebraic theorem. Proximity to 49/3 is a 0.21% numerical coincidence at current precision.

### [DOC]
- `CANONICAL/CONSTANTS.md` version bumped to v3.9.5; epistemic audit metadata table added.
- `docs/su3_gamma_theorem.md` updated with full 80-digit mpmath audit (PR #199).

### Open Tickets Created
- **TKT-20260403-FRG-NLO:** Full NLO FRG truncation study (BMW/LPA') required before δγ = δ_NLO re-evaluation.
- **TKT-20260403-TOPO-CLAIMS:** Register `UIDT-C-TOPO-01/02/03` in CLAIMS.json (PR #190 OT-3).

---

## [v3.9.4b] — 2026-03-30: First-Principles Evidence Audit (Sessions 2026-03-29/30)

### [AUDIT — Session 2026-03-30]
- **Δ* = 1.710 GeV:** Mechanistic support confirmed via Schwinger mechanism (Aguilar et al. 2023, arXiv:2211.12594; Ferreira & Papavassiliou 2025, arXiv:2501.01080). Gap between UIDT Δ* and propagator screening mass m(0) ~ 500–700 MeV documented (different definition). **Not a falsification.** See PR #193.
- **γ = 16.339:** No independent FRG or lattice derivation found producing ~16 as scheme-independent observable. Nearest external value g²★ = 15.0(5) (SU(3) N_f=10, arXiv:2306.07236) is from different theory. **[TENSION ALERT]** Δ = 1.34. Evidence [A-] unchanged. See PR #193.
- **E_T = 2.44 MeV:** No lattice QCD signal for torsion-specific binding energy at MeV scale found. FLAG 2024 tension (3.75σ pre-QED, 0.75σ post-QED) noted. QED correction derivation absent in current docs. Evidence [C]. See PR #193.
- **Wilson Flow / Topological Susceptibility:** SVZ formula corrected (b0 = 11 for SU(3) pure-YM). χ_top^{1/4} ≈ 107 MeV → z ≈ 16σ vs lattice band. Evidence Category D [TENSION ALERT]. C_GLUON and α_s retagged [E] (external). See PR #190.
- **Information Geometry / Fisher Metric:** Research scaffold opened. OS axioms OS0–OS4 satisfied [A]. Fisher metric route to kinetic term derivation: Category [E] (open). See PR #194.

### [DOC]
- `docs/first_principles_evidence_audit_2026-03-30.md` added (PR #193).
- `docs/schwinger_mechanism_deep_research_2026-03-30.md` added (PR #193).
- `docs/gamma_first_principles_crosscheck_2026-03-30.md` added (PR #193).
- `verification/scripts/verify_wilson_flow_topology.py` added with corrected SVZ formula (PR #190).
- `docs/falsification-criteria.md` entry F9 added (topological susceptibility) (PR #190).

### Open Tasks (PI decision required)
- OT-1: Register C_GLUON canonical value in CONSTANTS.md
- OT-2: Register α_s(μ) reference scale in CONSTANTS.md
- OT-3: Register claims UIDT-C-TOPO-01/02/03 in CLAIMS.json
- OT-4: Implement NLO α_s correction to χ_top formula
- OT-5: Coordinate version bump v3.9 → v3.9.5 with CONSTANTS.md header (this PR resolves OT-5)

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
Comprehensive audit of all 82 Python files against canonical reference data. All canonical parameters confirmed consistent across the full codebase. Five clear issues identified and resolved; five context-dependent issues documented for follow-up.

**Evidence Classification (rg_flow_analysis.py — both copies):**
- Fixed: γ evidence tag corrected from `calibrated [A-]` to `calibrated [A-]` in `clay-submission/02_VerificationCode/rg_flow_analysis.py`.
- Fixed: Same correction in `verification/scripts/rg_flow_analysis.py`.
- Rule: γ = 16.339 is `calibrated [A-]`, never first-principles derived [A].

**Encoding Fixes (Windows cp1252 → UTF-8):**
- Fixed: `clay-submission/02_VerificationCode/brst_cohomology_verification.py`
- Fixed: `clay-submission/02_VerificationCode/slavnov_taylor_ccr_verification.py`

**Dependencies:**
- Added: `mpmath==1.3.0` to `verification/requirements.txt`.

## [v3.7.3] — 2026-02-16

### Repository Migration and Data Availability Update

All repository references migrated from `badbugsarts-hue/UIDT-Framework-V3.2-Canonical` to `Mass-Gap/UIDT-Framework-v3.7.2-Canonical`.

## [v3.7.2] — 2025-12-29

### Current Canonical Release

- VEV = 47.7 MeV [A] (Corrected v3.6.1).
- H₀ = 70.4 km/s/Mpc [C] (DESI calibrated).

## [v3.6.1] — 2025-12-19

### VEV Correction Patch

- Corrected VEV from 0.854 MeV to 47.7 MeV based on refined lattice data.

## [v3.6] — 2025-12-11

- **Vacuum Energy:** Residual at 3.3% level [C].
- **Mass Gap:** Δ* = 1.710 GeV identified as spectral gap.

## [v3.3] — 2025-11-01 — **[REVOKED]**

**Reason:** Data corruption in externally formatted artifacts.

## [v3.2] — 2025-11-09

### Technical Note Baseline

- Baseline release for technical notes.
