# Falsification Matrix

**UIDT v3.7.2**

> **Purpose:** Define experimental tests that would refute the theory
> **Principle:** A theory that cannot be falsified is not scientific

---

## Overview

The UIDT framework makes **testable predictions** across quantum field theory, lattice QCD, precision laboratory experiments, and cosmological observations. This document specifies the exact experimental thresholds that would **refute the theory** and require major revision.

**Status:** Theory is considered **REFUTED** if any critical test fails at the specified confidence level.

---

## CRITICAL TESTS (Theory-Killing)

### Test 1: Lattice QCD Continuum Limit 🔴 HIGHEST PRIORITY

**Prediction:**
Yang-Mills spectral gap Δ = 1.710 ± 0.015 GeV [Category A]

**Experimental Test:**
Next-generation quenched lattice QCD continuum extrapolation

**Falsification Threshold:**
Continuum limit excludes 1.710 GeV at **>3σ confidence** with full systematic uncertainties

**Current Status:**
✅ **PASSED** — z = 0.37σ agreement with Chen et al. (2006) quenched lattice

**Timeline:**
- **2026-2028:** Next generation lattice studies (finer grids, larger volumes)
- **2029+:** Full dynamical fermion analysis

**Falsification Example:**
If lattice continuum limit yields:
- Δ_lattice = 1.900 ± 0.050 GeV (3.8σ exclusion) → **THEORY REFUTED**
- Δ_lattice = 1.750 ± 0.080 GeV (0.5σ agreement) → **THEORY CONFIRMED**

**Verification Protocol:**
1. Monitor arXiv:hep-lat for new lattice QCD publications
2. Extract continuum limit from published data
3. Compute z-score: z = |Δ_UIDT - Δ_lattice| / √(σ²_UIDT + σ²_lattice)
4. If z > 3 → falsification trigger activated

**Contact:** Lattice 2026 Conference proceedings

---

### Test 2: Casimir Precision Experiments ⚠️ TECHNOLOGY-LIMITED

**Prediction:**
Casimir force anomaly +0.59% at λ = 0.66 nm [Category D: Unverified]

**Experimental Test:**
Sub-nanometer parallel-plate Casimir force measurements

**Falsification Threshold:**
Measurement at λ = 0.66 nm with <0.3% uncertainty excludes anomaly:
**|ΔF/F|_measured < 0.1%** → **PREDICTION REFUTED**

**Current Status:**
❌ **NO PEER-REVIEWED DATA EXISTS** (Category D: awaiting experimental test)

**Technical Challenges:**
- Sub-nanometer plate separation control (< 1 Å precision)
- Surface roughness < 0.1 nm RMS
- Electrostatic potential cancellation < 1 mV
- Temperature stability < 10 mK

**Timeline:**
- **2026-2027:** Technology development (AFM-based Casimir apparatus)
- **2028+:** Precision measurements (if funding secured)

**Falsification Example:**
If experimental measurement yields:
- |ΔF/F| = 0.03 ± 0.08% → **NO ANOMALY DETECTED** (within 1σ) → **CATEGORY D CLAIM REFUTED**
- |ΔF/F| = 0.61 ± 0.12% → **ANOMALY CONFIRMED** (5σ) → **CATEGORY D UPGRADED TO C**

**Verification Protocol:**
1. Contact precision Casimir groups (van Blokland Lab, Lambrecht/Reynaud)
2. Request measurements at d = 0.66 nm ± 0.05 nm
3. Compare F_measured vs. F_Lifshitz(standard)
4. Statistical significance: >5σ for confirmation, <3σ for exclusion

**Open Data:** Researchers can request raw Casimir data at badbugs.arts@gmail.com

---

## STRONG TESTS (Pillar-Specific)

### Test 3: DESI Year 5 Dark Energy Evolution 🔬 ONGOING

**Prediction:**
Dynamic dark energy w(z) ≠ -1 at high redshift (DESI DR2 calibrated) [Category C]

**Experimental Test:**
DESI Year 5 final data release (2027)

**Falsification Threshold:**
If w(z) = -1.000 ± 0.005 at **all redshifts** (pure cosmological constant) → **PILLAR II CALIBRATION QUESTIONED**

**Current Status:**
✅ **SUPPORTED** — DESI Year 1: w₀ = -0.762 ± 0.196 (1.2σ deviation from Λ)

**Timeline:**
- **2025:** DESI Year 3 data release
- **2027:** DESI Year 5 final release
- **2029+:** Euclid/Rubin cross-validation

**Falsification Example:**
- w(z) = -1.00 ± 0.01 (static Λ) → **DESI calibration invalid** → **Category C downgraded**
- w(z) = -0.70 ± 0.05 (dynamic) → **DESI calibration validated** → **Category C maintained**

**Verification Protocol:**
Monitor DESI publications for equation-of-state w(z) constraints

---

### Test 4: LHC Scalar Resonance Search (Run 4) 📊 LONG-TERM

**Prediction:**
Scalar particle m_S = 1.705 ± 0.015 GeV [Category D: Unverified]

**Experimental Test:**
LHC Run 4 (2029+) search for 0⁺⁺ resonance in:
- Diphoton channel (γγ)
- Four-pion decay (4π)
- Gluon fusion production

**Falsification Threshold:**
**>5σ exclusion** of 0⁺⁺ resonance in 1.5-1.9 GeV mass window with full branching ratios

**Current Status:**
⚠️ **PENDING** — No dedicated LHC search in 1.6-1.8 GeV range yet

**Timeline:**
- **2029+:** LHC Run 4 (High-Luminosity phase)
- **2032+:** Analysis of full dataset

**Falsification Example:**
- No 0⁺⁺ resonance in 1.5-1.9 GeV (>5σ exclusion) → **m_S PREDICTION REFUTED**
- Resonance at 1.71 ± 0.03 GeV (>5σ detection) → **m_S PREDICTION CONFIRMED**

**Verification Protocol:**
Monitor ATLAS/CMS publications for light scalar searches

---

## MODERATE TESTS (Calibration-Dependent)

### Test 5: Hubble Tension Resolution (JWST Cycle 3-4) 🌌 SHORT-TERM

**Prediction:**
H₀ = 70.4 ± 0.16 km/s/Mpc (DESI-calibrated) [Category C]

**Experimental Test:**
JWST Cycle 3-4 Cepheid calibrations + TRGB measurements

**Falsification Threshold:**
If independent measurements converge to H₀ ≠ 70.4 km/s/Mpc at >3σ:
- **H₀ = 67.0 ± 0.3 km/s/Mpc** (Planck confirmed) → **DESI CALIBRATION QUESTIONED**
- **H₀ = 73.0 ± 0.5 km/s/Mpc** (SH0ES confirmed) → **DESI CALIBRATION QUESTIONED**

**Current Status:**
⚠️ **UNCERTAIN** — JWST early results show 72.6 ± 2.0 km/s/Mpc (1.1σ from UIDT)

**Timeline:**
- **2025-2026:** JWST Cycle 3 Cepheid program
- **2027:** Combined JWST+DESI analysis

**Impact:**
H₀ is **calibrated [C]**, not independent prediction. Falsification would question DESI DR2 data, not UIDT core.

---

## VERIFICATION PROTOCOL FOR RESEARCHERS

### Step 1: Monitor Experimental Literature

**Recommended Sources:**
- arXiv:hep-lat (Lattice QCD)
- arXiv:hep-ex (LHC experiments)
- arXiv:astro-ph.CO (Cosmology)
- arXiv:cond-mat.mes-hall (Casimir experiments)

**Automated Alerts:**
Set arXiv alerts for keywords:
- "Yang-Mills mass gap"
- "Casimir force sub-nanometer"
- "DESI dark energy"
- "LHC scalar resonance 1.7 GeV"

### Step 2: Reproduce Falsification Tests

**Independent Verification:**
1. Clone repository:
   ```bash
   git clone https://github.com/badbugsarts-hue/UIDT-Framework-v3.7.2-Canonical
   cd UIDT-Framework-v3.7.2-Canonical
   ```

2. Run verification:
   ```bash
   python verification/scripts/UIDT-3.6.1-Verification.py
   # Expected: PASS with residuals < 10⁻⁴⁰
   ```

3. Compare with experimental data:
   - Lattice: Check z-score vs. published continuum limits
   - Casimir: Compare ΔF/F predictions vs. measurements (when available)

### Step 3: Report Findings

**If Falsification Detected:**
1. Open GitHub Issue with:
   - Experimental reference (DOI/arXiv)
   - Statistical significance (z-score, p-value)
   - Confidence level (σ)
   - Reproduction steps

2. Email: badbugs.arts@gmail.com with subject "UIDT Falsification Report"

**If Confirmation Detected:**
1. Upgrade evidence category (D → C or C → B)
2. Document in CHANGELOG.md
3. Submit update to Zenodo (new DOI version)

---

## Falsification Summary Table

| Test ID | Prediction | Category | Falsification Threshold | Timeline | Status |
|---------|------------|----------|------------------------|----------|--------|
| **T1** | Δ = 1.710 GeV | A | Lattice >3σ exclusion | 2026-2028 | ✅ Currently passes (z=0.37σ) |
| **T2** | Casimir +0.59% | D | \|ΔF/F\| < 0.1% @ 0.66 nm | 2028+ | ❌ No data exists |
| **T3** | w(z) dynamic | C | w = -1.00 ± 0.01 (static) | 2027 | ✅ DESI Y1 supports |
| **T4** | m_S = 1.705 GeV | D | LHC >5σ exclusion 1.5-1.9 GeV | 2029+ | ⚠️ No search yet |
| **T5** | H₀ = 70.4 km/s/Mpc | C | >3σ from 70.4 (independent) | 2025-2026 | ⚠️ JWST ongoing |

---

## Impact Assessment

### If Test 1 (Lattice QCD) FAILS:
- **Category A claims** (Δ, κ, λ_S) invalidated
- **Yang-Mills mass gap proof** refuted
- **Clay Mathematics submission** withdrawn
- **Entire UIDT framework** requires major revision
- **Severity:** 🔴 **THEORY-KILLING**

### If Test 2 (Casimir) FAILS:
- **Category D claims** (Casimir, holographic scale) invalidated
- **Limitation L1** (10¹⁰ factor) unresolved
- **Cosmological predictions** downgraded to pure phenomenology
- **Core QFT claims** (Category A) **UNAFFECTED**
- **Severity:** 🟡 **PILLAR III REFUTED** (but QFT core survives)

### If Test 3 (DESI) FAILS:
- **Category C calibrations** (H₀, λ_UIDT) invalidated
- **Cosmological pillar** requires recalibration
- **Core QFT claims** (Category A) **UNAFFECTED**
- **Severity:** 🟢 **CALIBRATION UPDATE NEEDED** (not theory-killing)

### If Test 4 (LHC) FAILS:
- **Category D prediction** (m_S) refuted
- **Scalar sector** interpretation incorrect
- **Core QFT claims** (Δ, κ, λ_S) **UNAFFECTED**
- **Severity:** 🟡 **PREDICTION FAILED** (theory survives)

---

## Citation

```bibtex
@misc{Rietz2025_Falsification,
  author = {Rietz, Philipp},
  title  = {UIDT v3.7.2 Falsification Matrix},
  year   = {2025},
  doi    = {10.5281/zenodo.17835200},
  url    = {https://github.com/badbugsarts-hue/UIDT-Framework-v3.7.2-Canonical/blob/main/docs/falsification-criteria.md}
}
```

**See also:**
- [Evidence Classification (A-E)](evidence-classification.md)
- [Known Limitations (L1-L6)](limitations.md)
- [Verification Guide](verification-guide.md)

---

**Last Updated:** 2026-02-05
**DOI:** 10.5281/zenodo.17835200
**Next Review:** After DESI Year 3 (2025) and Lattice 2026 Conference
