# Falsification Matrix

**UIDT v3.9** | Last Updated: 2026-02-19

> **Purpose:** Define experimental tests that would refute the theory
> **Principle:** A theory that cannot be falsified is not scientific

---

## Overview

The UIDT framework makes **testable predictions** across quantum field theory, lattice QCD, precision laboratory experiments, cosmological observations, and (v3.9) photonic analog platforms. This document specifies the exact experimental thresholds that would **refute the theory** and require major revision.

**Status:** Theory is considered **REFUTED** if any critical test fails at the specified confidence level.

---

## CRITICAL TESTS (Theory-Killing)

### F1: Lattice QCD Continuum Limit 🔴 HIGHEST PRIORITY

**Prediction:**
Yang–Mills spectral gap Δ = 1.710 ± 0.015 GeV (Category A)

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

### F2: Torsion Binding Energy (Missing Link) 🔴 HIGH PRIORITY

**Prediction:**
$E_T \approx 2.44\,\mathrm{MeV}$ (Missing Link)

**Experimental Test:**
Precision hadron spectroscopy / vacuum-scalar resonance calibration

**Falsification Threshold:**
If the observed vacuum resonance can be shown to satisfy
$f_{vac} = \Delta/\gamma$ with no residual term (pure geometry), i.e.
**$E_T \approx 0$ within experimental uncertainty** → **PILLAR II MISSING LINK REFUTED**

**Current Status:**
⚠️ **PENDING** — requires a dedicated precision determination of $f_{vac}$ and a consistent mapping to the mass-gap sector

**Timeline:**
- **2025-2026:** Precision hadron spectroscopy targets for $f_{vac}$ cross-checks

**Falsification Example:**
If experimental measurement yields:
- $E_T = 0.00 \pm 0.05\,\text{MeV}$ → **NO TORSION TERM** → **F2 FAIL (refutes missing-link claim)**
- $E_T = 2.44 \pm 0.10\,\text{MeV}$ → **TORSION TERM CONFIRMED** → **Category D strengthened**

**Verification Protocol:**
1. Determine $f_{vac}$ (vacuum scalar resonance proxy) from a reproducible experimental pipeline
2. Compute $E_{\mathrm{geo}} = \Delta/\gamma$ using canonical $\Delta$ and $\gamma$
3. Compute $E_T = f_{vac} - E_{\mathrm{geo}}$
4. If $E_T$ is consistent with 0 → falsification trigger activated

---

## STRONG TESTS (Pillar-Specific)

### F3: DESI Year 5 Dark Energy Evolution 🔬 ONGOING

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

### F4: Photonic Isomorphism (Metamaterial Analog) 🔬 NEAR-TERM

**Prediction:**
Critical refractive index $n_{\mathrm{critical}} = \gamma \approx 16.339$ (equivalently $\varepsilon_r \approx \gamma^2 \approx 267$) [Category D: analog verification]

**Experimental Test:**
Nonlocal metamaterial analog platform (Song et al., Nature Communications 2025 as the external platform)

**Falsification Threshold:**
Measured transition does not occur at **$n_{\mathrm{critical}} = 16.339 \pm 0.1$** → **PILLAR IV REFUTED**

**Current Status:**
⚠️ **PENDING** — platform exists; UIDT mapping requires a dedicated measurement protocol

**Timeline:**
- **2026:** Analog test campaign (materials + optical characterization)

---

### F5: LHC Scalar Resonance Search (Run 4) 📊 LONG-TERM

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

### F6: Proton Anchor Ratio (Hadron Harmonic Consistency) ⚖️ ONGOING

**Prediction:**
$m_p/f_{vac} \approx 8.75$ [Category D: Unverified]

**Experimental Test:**
Precision determination of $f_{vac}$ (vacuum-scalar resonance proxy) combined with the proton mass anchor

**Falsification Threshold:**
If $m_p/f_{vac}$ deviates from 8.75 at **>3σ** after uncertainty propagation → **PILLAR III ANCHOR REFUTED**

**Current Status:**
⚠️ **PENDING** — depends on a reproducible, externally measurable $f_{vac}$ pipeline

**Verification Protocol:**
1. Measure/estimate $f_{vac}$ from an explicitly documented experimental proxy
2. Compute $m_p/f_{vac}$ with propagated uncertainties
3. If deviation exceeds 3σ → falsification trigger activated

---

### F7: Casimir Force Anomaly (Sub-nanometer) 🧪 LONG-TERM

**Prediction:**
Casimir force anomaly +0.59% at λ = 0.66 nm [Category D: Unverified]

**Experimental Test:**
Next-generation sub-nanometer Casimir force measurements with validated surface systematics

**Falsification Threshold:**
If \|ΔF/F\| < 0.1% @ 0.66 nm with controlled systematics → **CASIMIR PREDICTION REFUTED**

**Current Status:**
❌ **NO DATA** — no public sub-nanometer dataset at the required systematics level

**Open Data:** Researchers can request raw Casimir data at badbugs.arts@gmail.com

---

## MODERATE TESTS (Calibration-Dependent)

### F8: Hubble Tension Resolution (JWST Cycle 3-4) 🌌 SHORT-TERM

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

### F9: Topological Susceptibility (Wilson Flow / Quenched Lattice) 🔬 ONGOING

> Added: 2026-04-13  
> Linked Claim: UIDT-C-056  
> Linked Script: `verification/scripts/verify_wilson_flow_topology.py`

**Prediction:**
Topological susceptibility χ_top^{1/4} ≈ 143 MeV (SVZ leading-order estimate) [Category D]

**Experimental Test:**
Comparison with quenched SU(3) lattice QCD measurements of χ_top^{1/4}

**Falsification Threshold:**
If the fully NLO-corrected χ_top^{1/4} falls **outside** the range [140, 220] MeV → **SVZ ESTIMATE INAPPLICABLE**

**Current Status:**
⚠️ **TENSION** — UIDT SVZ LO: 143 MeV vs quenched lattice: 198.1 ± 2.8 MeV (Dürr et al. 2025, arXiv:2501.08217) (z ≈ 19.7σ (LO), z ≈ 4.2σ (NLO×1.3023))

**Timeline:**
- **2026:** NLO corrections to SVZ estimate (+30–80% expected)
- **2027+:** Dynamical fermion lattice studies

**Falsification Example:**
- NLO-corrected χ_top^{1/4} = 120 MeV (below [140, 220]) → **SVZ APPROACH REFUTED**
- NLO-corrected χ_top^{1/4} = 190 MeV (within lattice band) → **TENSION RESOLVED**

**Verification Protocol:**
1. Compute NLO corrections to SVZ formula using canonical α_s(μ) values
2. Compare corrected χ_top^{1/4} with quenched lattice continuum extrapolation
3. If corrected value inside [140, 220] MeV → tension resolved
4. If outside → falsification trigger activated

**Impact:**
χ_top is a **derived observable** using external inputs (C_GLUON, α_s). Falsification would question the SVZ approach applicability, NOT the core UIDT parameters (Δ*, γ, κ, λ_S).

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
   git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical
   cd UIDT-Framework-v3.9-Canonical
   ```

2. Run verification:
   ```bash
   python verification/scripts/UIDT_Master_Verification.py
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
| **F1** | Δ = 1.710 ± 0.015 GeV | A | Lattice >3σ exclusion | 2026-2028 | ✅ Currently passes (z=0.37σ) |
| **F2** | $E_T \approx 2.44$ MeV | D | $E_T \approx 0$ (pure geometry) | 2025-2026 | ⚠️ Pending |
| **F3** | w(z) dynamic | C | w = -1.00 ± 0.01 (static) | 2027 | ✅ DESI Y1 supports |
| **F4** | $n_{\mathrm{critical}} = 16.339$ | D | $n_{crit} \neq 16.339 \pm 0.1$ | 2026 | ⚠️ Pending |
| **F5** | Scalar $m_S = 1.705 \pm 0.015$ GeV | D | >5σ exclusion (1.5–1.9 GeV) | 2029+ | ⚠️ Pending |
| **F6** | $m_p/f_{vac} \approx 8.75$ | D | >3σ deviation | Ongoing | ⚠️ Pending |
| **F7** | Casimir +0.59% | D | \|ΔF/F\| < 0.1% @ 0.66 nm | 2028+ | ❌ No data exists |
| **F8** | H₀ = 70.4 ± 0.16 km/s/Mpc | C | H₀ ≠ 70.4 at >3σ | 2025-2027 | ⚠️ Uncertain |
| **F9** | χ_top^{1/4} ≈ 143 MeV (SVZ LO) | D | NLO outside [140, 220] MeV | 2026-2027 | ⚠️ Tension (z≈9σ vs lattice) |

---

## Impact Assessment

### If Test 1 (Lattice QCD) FAILS:
- **Category A claims** (Δ, κ, λ_S) invalidated
- **Yang-Mills mass gap proof** refuted
- **Clay Mathematics submission** withdrawn
- **Entire UIDT framework** requires major revision
- **Severity:** 🔴 **THEORY-KILLING**

### If Test 2 (Torsion Binding Energy) FAILS:
- **Missing-link claim** (E_T) invalidated
- **Cosmological folding narrative** requires revision/replacement
- **Core QFT claims** (Category A) **UNAFFECTED**
- **Severity:** 🟡 **PILLAR II MECHANISM REFUTED** (but QFT core survives)

### If Test 3 (DESI) FAILS:
- **Category C calibrations** (H₀, λ_UIDT) invalidated
- **Cosmological pillar** requires recalibration
- **Core QFT claims** (Category A) **UNAFFECTED**
- **Severity:** 🟢 **CALIBRATION UPDATE NEEDED** (not theory-killing)

### If Test 4 (Photonic Isomorphism) FAILS:
- **Analog isomorphism claim** (S(x) ↔ n_eff channel) refuted
- **Photonic pillar** removed from the architecture
- **Core QFT/cosmology/lab pillars** **UNAFFECTED**
- **Severity:** 🟡 **PILLAR IV REFUTED** (but QFT core survives)

---

## Citation

```bibtex
@misc{Rietz2025_Falsification,
  author = {Rietz, Philipp},
  title  = {UIDT v3.9 Falsification Matrix},
  year   = {2026},
  doi    = {10.5281/zenodo.17835200},
  url    = {https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/blob/main/docs/falsification-criteria.md}
}
```

**See also:**
- [Evidence Classification (A-E)](evidence-classification.md)
- [Known Limitations (L1-L6)](limitations.md)
- [Verification Guide](verification-guide.md)

---

**Last Updated:** 2026-04-13
**DOI:** 10.5281/zenodo.17835200
**Next Review:** After DESI Year 3 (2025), Metamaterial analog tests (2026), and Lattice 2026 Conference
