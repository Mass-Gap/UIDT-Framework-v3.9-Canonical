# Cosmological Implications of the UIDT Framework v3.9

**UIDT Framework v3.9** — *Vacuum Information Density as the Fundamental Geometric Scalar*

- **Author:** P. Rietz (ORCID: [0009-0007-4307-1609](https://orcid.org/0009-0007-4307-1609))
- **DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)
- **Date:** 2026-02-28

---

## 1. Overview

The UIDT framework proposes an interpretive mapping from QCD vacuum structure —
characterised by the spectral gap Δ = 1.710 ± 0.015 GeV [A] and the geometric
coupling γ = 16.339 [A-] — to cosmological parameters. Through the vacuum
dressing mechanism (δγ = 0.0047 [B/D]) and holographic amplification (L⁴
factor), the framework generates predictions for the dark-energy equation of
state and other cosmological observables.

**All cosmological parameters derived within UIDT are capped at Evidence
Category [C].** These are calibrated interpretive mappings, not independent
measurements. The framework proposes consistency with observational data; it
does not claim to resolve existing cosmological tensions.

### Canonical UIDT Cosmological Parameters [C]

| Parameter | UIDT Value | Category |
|-----------|-----------|----------|
| H₀ | 70.4 km/s/Mpc | [C] |
| w₀ | −1 (CPL baseline) | [C] |
| w\_a | −1.300 (via L = 8.2) | [C] |
| Ω\_m | 0.315 (calibrated to Planck) | [C] |
| σ₈ | 0.811 (calibrated to Planck) | [C] |

---

## 2. Parameter Comparison Table

### 2.1 Full Comparison Matrix

| Parameter | Planck 2018 | Planck PR4 | DESI-DR2 | Euclid Q1 | SH0ES | UIDT v3.9 |
|-----------|-------------|------------|----------|-----------|-------|-----------|
| Ω\_m | 0.315 ± 0.007 | 0.317 ± 0.006 | 0.310 ± 0.010 | 0.30–0.32 (prelim.) | — | 0.315 [C] |
| σ₈ | 0.811 ± 0.006 | 0.812 ± 0.006 | — | — | — | 0.811 [C] |
| H₀ (km/s/Mpc) | 67.4 ± 0.5 | 67.5 ± 0.5 | — | — | 73.04 ± 1.04 | 70.4 [C] |
| w₀ | −1 (fixed) | −1 (fixed) | −0.76 to −0.84 | — | — | −1 [C] |
| w\_a | 0 (fixed) | 0 (fixed) | −0.60 to −1.27 | — | — | −1.300 [C] |

**Sources:**
- Planck 2018: arXiv:1807.06209 (TT,TE,EE+lowE+lensing)
- Planck PR4: arXiv:2007.04997 (NPIPE reprocessing)
- DESI-DR2: arXiv:2503.14738 (BAO + SNe Ia combinations)
- Euclid Q1: arXiv:2405.13491 (preliminary, not final release)
- SH0ES: arXiv:2112.04510 (Cepheid-calibrated distance ladder)

### 2.2 Notes on UIDT Values

- **Ω\_m = 0.315:** Calibrated to Planck 2018+lensing central value. Not an
  independent determination.
- **σ₈ = 0.811:** Calibrated to Planck 2018+lensing central value. Not an
  independent determination.
- **H₀ = 70.4 km/s/Mpc:** An intermediate value positioned between the Planck
  early-Universe (67.4) and SH0ES late-Universe (73.04) measurements. This is
  a calibrated proposal, not a resolution of the Hubble tension.
- **w₀ = −1:** Adopted as the CPL baseline (cosmological constant).
- **w\_a = −1.300:** Derived from the vacuum dressing mechanism:
  w\_a = −δ × L⁴ = −0.00028757 × 8.2⁴ ≈ −1.300.

---

## 3. DESI-DR2 Alignment

### 3.1 w\_a Comparison Across Supernova Datasets

The DESI-DR2 BAO data, combined with different Type Ia supernova catalogues,
yield varying constraints on the CPL parameter w\_a:

| SN Dataset | w₀ | w₀ err | w\_a | w\_a err | UIDT w\_a | |Δw\_a|/σ | Tension |
|------------|------|--------|-------|---------|-----------|---------|---------|
| Union3 | −0.76 | 0.11 | −1.27 | 0.32 | −1.300 | 0.09σ | Negligible |
| DESY5 | −0.80 | 0.10 | −0.75 | 0.25 | −1.300 | 2.20σ | Moderate |
| Pantheon+ | −0.84 | 0.09 | −0.60 | 0.28 | −1.300 | 2.50σ | Moderate |

**Methodology note:** The agreement metric |Δw\_a|/σ is a heuristic z-score
computed as |w\_a(UIDT) − w\_a(data)| / σ(data). This does not account for
correlations between w₀ and w\_a, prior volume effects, or systematic
differences between supernova calibration pipelines. These are approximate
indicators, not rigorous statistical tests.

### 3.2 Interpretation

The UIDT prediction w\_a ≈ −1.300 is:
- **Consistent with** DESI-DR2 + Union3 (0.09σ deviation)
- **In moderate tension with** DESI-DR2 + DESY5 (2.20σ) and DESI-DR2 +
  Pantheon+ (2.50σ)

The spread among SN datasets reflects ongoing calibration systematics in the
supernova community, not a unique feature of the UIDT prediction. The Union3
dataset currently provides the strongest alignment with the UIDT prediction;
future convergence of SN calibrations will sharpen this test.

### 3.3 Holographic L-Range Sensitivity

The w\_a prediction depends on the holographic extent L. A scan over
L ∈ [8.15, 8.25] shows:

| L | w\_a | Within Union3 1σ | Within DESY5 1σ |
|---|------|-------------------|-----------------|
| 8.15 | −1.269 | YES | NO |
| 8.20 | −1.300 | YES | NO |
| 8.25 | −1.332 | YES | NO |

All L values in this range produce w\_a consistent with the Union3 band
but outside the DESY5 band. See `verification/data/holographic_l_range.csv`
for the full scan with 0.01 step resolution.

---

## 4. Planck PR4 Consistency

### 4.1 Ω\_m Consistency

| Source | Ω\_m | ±σ |
|--------|------|-----|
| Planck 2018 | 0.315 | 0.007 |
| Planck PR4 (NPIPE) | 0.317 | 0.006 |
| UIDT | 0.315 | — |

The UIDT value Ω\_m = 0.315 is calibrated to the Planck 2018 central value and
is consistent with the Planck PR4 reprocessing within 0.3σ.

### 4.2 σ₈ Consistency

| Source | σ₈ | ±σ |
|--------|-----|-----|
| Planck 2018 | 0.811 | 0.006 |
| Planck PR4 | 0.812 | 0.006 |
| UIDT | 0.811 | — |

The UIDT value σ₈ = 0.811 is calibrated to the Planck 2018 central value.

### 4.3 S₈ Tension Context

The S₈ ≡ σ₈√(Ω\_m/0.3) tension between CMB and weak-lensing surveys is an
active area of research. The UIDT framework does not claim to resolve this
tension. The UIDT values (Ω\_m = 0.315, σ₈ = 0.811) are calibrated to CMB
(Planck) values and therefore sit on the CMB side of the tension by
construction.

---

## 5. Euclid Q1 + DR1 Outlook

### 5.1 Euclid Q1 Preliminary Results

The Euclid Q1 data release (arXiv:2405.13491) provides preliminary constraints:

| Parameter | Euclid Q1 (prelim.) | UIDT |
|-----------|-------------------|------|
| Ω\_m | 0.30–0.32 | 0.315 |

The UIDT value falls within the preliminary Euclid Q1 range. However, Euclid Q1
uncertainties are not yet formally quantified, and this comparison is indicative
only.

### 5.2 Euclid DR1 Expectations

The Euclid DR1 (expected 2026–2027) will provide:

1. **Tightened Ω\_m constraints:** Expected σ(Ω\_m) ∼ 0.004, which will
   provide a more stringent test of the UIDT calibration.

2. **Independent w\_a measurement:** Euclid's combination of weak lensing,
   galaxy clustering, and BAO will constrain the CPL parameters independently
   of supernova data, potentially resolving the current spread among SN
   datasets.

3. **σ₈ from weak lensing:** Euclid's weak-lensing σ₈ measurement will test
   whether the CMB-calibrated UIDT value (0.811) is consistent with
   late-Universe structure growth.

### 5.3 Falsifiable Predictions for Euclid

The UIDT framework predicts:
- Ω\_m consistent with 0.315 ± 0.01 [C]
- w\_a in the range [−1.33, −1.27] for L ∈ [8.15, 8.25] [C]
- σ₈ consistent with 0.811 ± 0.01 [C]

If Euclid DR1 constrains w\_a to lie outside [−1.33, −1.27] at > 2σ, the
holographic amplification model (or the choice of L = 8.2) would require
revision.

---

## 6. KATRIN Neutrino Mass Bound

### 6.1 Current Experimental Status

The KATRIN experiment (arXiv:2406.13516) has established a direct kinematic
upper bound on the electron anti-neutrino mass:

```
m(ν_e) < 0.45 eV (90% CL) — KATRIN 2024
```

This translates to an upper bound on the sum of neutrino masses:

```
Σm_ν < 1.35 eV (direct, kinematic)
```

Cosmological constraints from Planck + BAO provide a tighter bound:

```
Σm_ν < 0.12 eV (95% CL) — Planck 2018 + BAO
```

### 6.2 UIDT Prediction [D]

The UIDT framework generates a prediction for the neutrino mass scale through
the vacuum dressing mechanism. This prediction is classified as Category [D]
(falsifiable prediction, awaiting test):

- The UIDT prediction is consistent with Σm\_ν < 0.45 eV (KATRIN 2024
  kinematic bound).
- More precise tests await KATRIN Phase-III and next-generation cosmological
  surveys.

### 6.3 Tritium Endpoint Anomaly [D]

The UIDT framework also predicts a spectral feature at E\_T = 2.44 MeV [D]
near the tritium beta-decay endpoint. This is a falsifiable prediction that
could be tested by dedicated high-resolution spectroscopy experiments.

---

## 7. Evidence Classification Summary

All cosmological parameters and comparisons in this document are constrained
by the UIDT evidence classification system:

| Parameter | UIDT Value | Category | Rationale |
|-----------|-----------|----------|-----------|
| H₀ | 70.4 km/s/Mpc | [C] | Calibrated intermediate value |
| w₀ | −1 | [C] | CPL baseline assumption |
| w\_a | −1.300 | [C] | Interpretive mapping via holographic amplification |
| Ω\_m | 0.315 | [C] | Calibrated to Planck 2018 |
| σ₈ | 0.811 | [C] | Calibrated to Planck 2018 |
| S₈ | derived | [C] | Follows from Ω\_m and σ₈ |
| Σm\_ν | — | [D] | Falsifiable prediction, awaiting test |
| E\_T | 2.44 MeV | [D] | Falsifiable prediction, awaiting test |

### Category Definitions

| Category | Meaning | Criterion |
|----------|---------|-----------|
| [A] | Lattice QCD confirmed | Residual < 10⁻¹⁴ |
| [A-] | Phenomenological, high precision | Fit-based, not first-principles |
| [B] | Numerically verified | Extrapolation or numerical procedure |
| [C] | Observationally consistent | Interpretive mapping, not independent measurement |
| [D] | Falsifiable prediction | Awaiting experimental test |
| [E] | Speculative / heuristic | Exploratory, not yet testable |

**Gate rules:**
- Cosmology claims NEVER exceed Category [C].
- No prestige language ("proves", "solves", "breakthrough") unless Category [A]
  with residual < 10⁻¹⁴.
- Δ is a SPECTRAL GAP, never "glueball particle mass".
- γ stays [A-], never upgrade to [A].
- H₀, w₀, w\_a, S₈ are ALWAYS [C] maximum.

---

## 8. Reproduction

### 8.1 Regenerate Comparison Data

```bash
cd verification/
python verify_bare_gamma.py          # Bare gamma extrapolation
python verify_cosmological_params.py # Cosmological parameter comparisons
```

### 8.2 Data Files

The comparison data used in this document is stored in:

| File | Location | Contents |
|------|----------|----------|
| `desi_dr2_comparisons.csv` | `verification/data/` | DESI-DR2 w\_a comparisons |
| `planck_desi_euclid_matrix.json` | `verification/data/` | Full parameter comparison matrix |
| `holographic_l_range.csv` | `verification/data/` | L-range scan for w\_a sensitivity |

### 8.3 Verification Checklist

- [ ] All w\_a comparisons use heuristic z-scores (no correlation modeling)
- [ ] All cosmological parameters marked [C]
- [ ] No prestige language in comparisons
- [ ] Uncertainties (±) included for all observational values
- [ ] DOI/arXiv references for all external data sources

---

## 9. References

1. P. Rietz, "Vacuum Information Density as the Fundamental Geometric Scalar,"
   UIDT Framework v3.9, DOI: [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

2. DESI Collaboration, "DESI DR2 Baryon Acoustic Oscillation Measurements,"
   arXiv: [2503.14738](https://arxiv.org/abs/2503.14738)

3. Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters,"
   arXiv: [1807.06209](https://arxiv.org/abs/1807.06209),
   DOI: [10.1051/0004-6361/201833910](https://doi.org/10.1051/0004-6361/201833910)

4. Planck Collaboration, "Planck intermediate results. LVII. Joint Planck-LFI
   and HFI data processing," arXiv: [2007.04997](https://arxiv.org/abs/2007.04997)

5. Euclid Collaboration, "Euclid preparation. Q1 data release,"
   arXiv: [2405.13491](https://arxiv.org/abs/2405.13491)

6. A. G. Riess et al., "A Comprehensive Measurement of the Local Value of the
   Hubble Constant with 1 km/s/Mpc Uncertainty from the Hubble Space Telescope
   and the SH0ES Team," arXiv: [2112.04510](https://arxiv.org/abs/2112.04510),
   DOI: [10.3847/2041-8213/ac5c5b](https://doi.org/10.3847/2041-8213/ac5c5b)

7. KATRIN Collaboration, "Direct neutrino-mass measurement based on 259 days
   of KATRIN data," arXiv: [2406.13516](https://arxiv.org/abs/2406.13516)

8. M. Chevallier and D. Polarski, "Accelerating universes with scaling dark
   matter," Int. J. Mod. Phys. D **10**, 213 (2001),
   DOI: [10.1142/S0218271801000822](https://doi.org/10.1142/S0218271801000822)

9. E. V. Linder, "Exploring the expansion history of the universe,"
   Phys. Rev. Lett. **90**, 091301 (2003),
   arXiv: [astro-ph/0208512](https://arxiv.org/abs/astro-ph/0208512)

10. Y. Chen et al., "Glueball spectrum and matrix elements on anisotropic
    lattices," Phys. Rev. D **73**, 014516 (2006),
    arXiv: [hep-lat/0510074](https://arxiv.org/abs/hep-lat/0510074)
