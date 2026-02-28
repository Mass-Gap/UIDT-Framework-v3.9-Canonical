# Vacuum Dressing Mechanism in the UIDT Framework

**UIDT Framework v3.9** — *Vacuum Information Density as the Fundamental Geometric Scalar*

- **Author:** P. Rietz (ORCID: [0009-0007-4307-1609](https://orcid.org/0009-0007-4307-1609))
- **DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)
- **Date:** 2026-02-28

---

## 1. Introduction

In the UIDT framework, the vacuum is not an inert background but a structured
medium whose information density is characterised by the spectral gap
Δ = 1.710 ± 0.015 GeV [A] and the geometric coupling γ. When computed on a
finite lattice, γ acquires "dressing" from the boundary conditions and the
truncated mode spectrum. The term *vacuum dressing* refers to the systematic
shift between the bare (infinite-volume) coupling γ\_∞ and the physically
measured (finite-volume) coupling γ.

This document provides a physical explanation of the dressing mechanism, its
quantitative characterisation, and its implications — including the interpretive
mapping to the cosmological dark-energy parameter w\_a [C].

**Terminological note:** In earlier internal drafts, this effect was referred to
as "Vakuumreibung" (vacuum friction). The English-language term *vacuum dressing*
is preferred in the canonical repository, as it more precisely captures the
finite-volume mode-coupling origin of the shift without implying a dissipative
process.

---

## 2. The Dressing Shift

The dressing shift is defined as:

```
δγ = γ_∞ − γ_phys = 16.3437 − 16.339 = 0.0047
```

| Quantity | Value | Category |
|----------|-------|----------|
| γ (dressed, physical) | 16.339 | [A-] |
| γ\_∞ (bare, thermodynamic limit) | 16.3437 ± 10⁻⁴ | [B] |
| δγ (dressing shift) | 0.0047 | [B/D] |

The dressed value γ = 16.339 is the phenomenologically determined coupling that
appears in all finite-volume lattice computations. It is classified [A-] because
it is obtained from high-precision fits rather than a first-principles
derivation.

The bare value γ\_∞ = 16.3437 ± 10⁻⁴ is obtained through finite-size scaling
extrapolation (see `bare_gamma_theorem.md` for details) and is classified [B].

---

## 3. Relative Geometric Shift

The relative geometric shift normalises the dressing correction:

```
δ = δγ / γ_∞ = 0.0047 / 16.3437 = 2.8757 × 10⁻⁴
```

This dimensionless quantity δ = 0.00028757 [B] represents the fractional change
in the geometric coupling due to vacuum dressing. Despite its smallness, δ
becomes cosmologically significant through holographic amplification (Section 5).

---

## 4. Physical Interpretation

### 4.1 Vacuum Mode Coupling

In a finite lattice of dimensionless extent L, the spectrum of vacuum
fluctuations is discretised: modes with wavelengths λ > L are absent. As L
increases, longer-wavelength modes become available and couple into the vacuum
condensate, modifying the effective geometric coupling.

The mechanism can be understood as follows:

1. **Infrared mode truncation:** At finite L, the lowest available momentum is
   p\_min ∼ 2π/L. Modes below this threshold do not contribute to the vacuum
   structure.

2. **Mode-coupling cascade:** As L grows, newly available long-wavelength modes
   couple non-perturbatively to the existing vacuum condensate, incrementally
   shifting the effective coupling toward its infinite-volume value.

3. **Saturation:** The corrections decay as 1/L² (leading) and 1/L⁴
   (sub-leading), consistent with the finite-size scaling ansatz:
   ```
   γ(L) = γ_∞ + a/L² + b/L⁴
   ```

### 4.2 Finite-Volume Effects vs. Perturbative Running

The vacuum dressing shift is conceptually distinct from the running of coupling
constants in perturbative QFT:

| Aspect | Perturbative running | Vacuum dressing |
|--------|---------------------|-----------------|
| Variable | Energy scale μ | Volume extent L |
| Mechanism | Loop corrections | Non-perturbative mode coupling |
| Regime | UV/IR | Purely IR |
| Magnitude | Logarithmic | Power-law (1/L²) |

---

## 5. Holographic Amplification

The central quantitative connection to cosmology is the holographic
amplification:

```
w_a = −δ × L⁴
```

The L⁴ factor arises from the four-dimensional volume measure in the holographic
mapping. For the reference holographic extent L = 8.2:

```
L⁴ = 8.2⁴ = 4521.2176
w_a = −2.8757 × 10⁻⁴ × 4521.2176 ≈ −1.300
```

This amplification converts the tiny vacuum dressing shift (δ ∼ 3 × 10⁻⁴) into
a cosmologically observable dark-energy parameter of order unity.

### L-Range Sensitivity

The holographic extent L is not precisely determined from first principles
within the current framework. A scan over L ∈ [8.15, 8.25] yields:

| L    | L⁴       | w\_a    |
|------|----------|---------|
| 8.15 | 4411.95  | −1.269  |
| 8.20 | 4521.22  | −1.300  |
| 8.25 | 4632.50  | −1.332  |

All values fall within the DESI-DR2 + Union3 1σ band (w\_a ∈ [−1.59, −0.95]).
The complete scan is available in `verification/data/holographic_l_range.csv`.

---

## 6. Cosmological Connection

### 6.1 w\_a Comparison

The UIDT prediction w\_a ≈ −1.300 [C] can be compared against observational
constraints from DESI-DR2 (arXiv:2503.14738):

| Dataset | w\_a (observed) | σ | UIDT w\_a | Agreement |
|---------|----------------|---|-----------|-----------|
| DESI-DR2 + Union3 | −1.27 ± 0.32 | 0.32 | −1.300 | 0.09σ |
| DESI-DR2 + DESY5 | −0.75 ± 0.25 | 0.25 | −1.300 | 2.20σ |
| DESI-DR2 + Pantheon+ | −0.60 ± 0.28 | 0.28 | −1.300 | 2.50σ |

**Note:** Agreement\_sigma values are heuristic z-scores computed as
|w\_a(UIDT) − w\_a(data)| / σ(data), without modelling parameter correlations.
The strong agreement with DESI+Union3 and the tension with DESI+Pantheon+
reflect the current spread in supernova calibration systematics, not a
definitive validation or falsification of the UIDT mapping.

### 6.2 Interpretive Framework

The cosmological connection is an *interpretive mapping* from QCD vacuum
structure to dark-energy parameters. It is not an independent measurement. All
cosmological parameters derived within UIDT are capped at Evidence Category [C].

**Language constraints:**
- Use "consistent with", "calibrated to", "proposes" — never "resolves",
  "solves", or "proves" for cosmological claims.

---

## 7. Category D Predictions

The vacuum dressing mechanism generates several falsifiable predictions
(Category [D]) that can be tested by future experiments:

1. **Neutrino mass sum:** Σm\_ν < 0.45 eV, testable by KATRIN Phase-III and
   cosmological neutrino mass bounds.

2. **Dark-energy equation of state:** w\_a in the range [−1.33, −1.27] for
   L ∈ [8.15, 8.25], testable by DESI-DR2 final analysis and Euclid DR1.

3. **Holographic extent L:** If future measurements converge on w\_a outside
   the range [−1.33, −1.27], either L deviates from 8.2 or the holographic
   amplification mechanism requires revision.

4. **Tritium endpoint anomaly:** E\_T = 2.44 MeV [D], a predicted spectral
   feature near the tritium beta-decay endpoint.

5. **Finite-size scaling universality:** The 1/L² + 1/L⁴ ansatz predicts
   specific coefficients (a, b) that can be verified by independent lattice
   groups using different discretisation schemes.

See `FALSIFICATION.md` in the repository root for the complete falsification
protocol.

---

## 8. Limitations

1. **Interpretive framework:** The cosmological connection is a calibrated
   mapping, not a first-principles derivation. Cosmology claims are
   [C] maximum.

2. **Holographic extent:** L = 8.2 is not derived from first principles within
   UIDT v3.9. It is chosen for consistency with DESI-DR2 + Union3 data.

3. **Supernova calibration dependence:** The w\_a comparison is sensitive to
   the choice of supernova dataset. The UIDT prediction is consistent with
   Union3 but in tension with Pantheon+ and DESY5.

4. **Model dependence of δγ:** The physical interpretation of the dressing
   shift as vacuum mode coupling (rather than, e.g., a lattice discretisation
   artefact) carries Category [D] model dependence.

5. **No independent cosmological measurement:** UIDT does not provide an
   independent measurement of w\_a; it provides an interpretive prediction
   that must be compared against observational data.

---

## 9. References

1. P. Rietz, "Vacuum Information Density as the Fundamental Geometric Scalar,"
   UIDT Framework v3.9, DOI: [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

2. DESI Collaboration, "DESI DR2 Baryon Acoustic Oscillation Measurements,"
   arXiv: [2503.14738](https://arxiv.org/abs/2503.14738)

3. Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters,"
   arXiv: [1807.06209](https://arxiv.org/abs/1807.06209),
   DOI: [10.1051/0004-6361/201833910](https://doi.org/10.1051/0004-6361/201833910)

4. KATRIN Collaboration, "Direct neutrino-mass measurement based on 259 days
   of KATRIN data," arXiv: [2406.13516](https://arxiv.org/abs/2406.13516)

5. M. Lüscher, "Volume dependence of the energy spectrum in massive quantum
   field theories," Commun. Math. Phys. **104**, 177 (1986),
   DOI: [10.1007/BF01211589](https://doi.org/10.1007/BF01211589)

6. M. Chevallier and D. Polarski, "Accelerating universes with scaling dark
   matter," Int. J. Mod. Phys. D **10**, 213 (2001),
   DOI: [10.1142/S0218271801000822](https://doi.org/10.1142/S0218271801000822)

7. E. V. Linder, "Exploring the expansion history of the universe,"
   Phys. Rev. Lett. **90**, 091301 (2003),
   arXiv: [astro-ph/0208512](https://arxiv.org/abs/astro-ph/0208512)
