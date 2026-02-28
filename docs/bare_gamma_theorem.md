# Bare Gamma Extrapolation: γ\_∞ Derivation and Evidence Classification

**UIDT Framework v3.9** — *Vacuum Information Density as the Fundamental Geometric Scalar*

- **Author:** P. Rietz (ORCID: [0009-0007-4307-1609](https://orcid.org/0009-0007-4307-1609))
- **DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)
- **Date:** 2026-02-28

---

## 1. Abstract

This document describes the finite-size scaling extrapolation of the UIDT
geometric coupling γ from phenomenological lattice measurements to its
thermodynamic-limit (bare) value γ\_∞. The dressed value γ = 16.339 [A-] is
determined phenomenologically from fits to hadronic and vacuum channel data. By
applying a standard finite-size scaling ansatz to a sequence of increasing
lattice volumes, the bare value γ\_∞ = 16.3437 ± 10⁻⁴ [B] is obtained. The
difference δγ = γ\_∞ − γ = 0.0047 quantifies the vacuum dressing correction
and, through holographic amplification, connects to the CPL dark-energy
parameter w\_a ≈ −1.300 [C]. This exposition complements the formal derivation
in the main manuscript (Appendix III).

---

## 2. Physical Motivation

In the UIDT framework, the spectral gap Δ = 1.710 ± 0.015 GeV [A] anchors the
vacuum information density. The geometric coupling γ relates the spectral gap to
observable hadronic scales. However, any lattice computation is performed in a
finite volume characterised by a dimensionless extent L. Finite-volume effects
dress the bare coupling with power-law corrections that must be removed to
obtain the intrinsic geometric constant γ\_∞.

The distinction matters for two reasons:

1. **Precision:** The dressed γ = 16.339 absorbs finite-volume artefacts.
   Quoting it as a fundamental constant would conflate lattice systematics with
   physics.
2. **Cosmological bridge:** The small dressing shift δγ, when amplified by the
   holographic L⁴ factor, maps onto the dark-energy equation-of-state parameter
   w\_a — providing a testable (Category [C]) connection between QCD vacuum
   structure and late-Universe dynamics.

**Important:** γ = 16.339 is classified [A-] because it is phenomenologically
determined (high-precision fit, not a first-principles derivation). γ\_∞ is
classified [B] because it relies on a numerical extrapolation procedure.

---

## 3. Finite-Size Scaling Ansatz

The standard finite-size scaling form used is:

```
γ(L) = γ_∞ + a / L² + b / L⁴
```

where:

| Symbol | Meaning |
|--------|---------|
| γ(L)   | Measured geometric coupling at lattice extent L |
| γ\_∞   | Bare (infinite-volume) coupling — the target quantity |
| a      | Leading finite-size coefficient (surface/boundary effects) |
| b      | Sub-leading finite-size coefficient (curvature corrections) |
| L      | Dimensionless lattice extent |

**Procedure:**

1. Compute γ(L) for a sequence of lattice extents L = 4, 6, 8, 10, 12, …
2. Fit the ansatz to the measured γ(L) values using weighted least squares.
3. Extract γ\_∞ as the L → ∞ intercept.
4. Estimate uncertainty from fit residuals and systematic variation of the
   truncation order (including or excluding higher-order terms a'/L⁶).

The 1/L² and 1/L⁴ power-law structure follows from the expected scaling of
finite-volume corrections in a gapped system with periodic boundary conditions.

---

## 4. Extrapolation Result

The extrapolation yields:

| Quantity | Value | Evidence Category |
|----------|-------|-------------------|
| γ\_∞    | 16.3437 ± 10⁻⁴ | [B] |
| a (fit coefficient) | O(10⁻²) | — |
| b (fit coefficient) | O(10⁻³) | — |
| χ²/dof  | ≈ 1.0 | — |

The uncertainty ± 10⁻⁴ on γ\_∞ is dominated by the systematic spread across
different fit windows and truncation orders, not by statistical noise on
individual γ(L) measurements.

---

## 5. Vacuum Dressing Mechanism

The dressing shift is defined as:

```
δγ = γ_∞ − γ_phys = 16.3437 − 16.339 = 0.0047
```

The relative geometric shift is:

```
δ = δγ / γ_∞ = 0.0047 / 16.3437 = 2.8757 × 10⁻⁴
```

**Physical interpretation:** In a finite lattice volume, vacuum modes with
wavelengths comparable to the box size are absent. As the volume increases
toward the thermodynamic limit, these long-wavelength modes couple into the
vacuum condensate, slightly increasing the effective geometric coupling. The
shift δγ = 0.0047 quantifies this vacuum mode coupling effect.

This mechanism is analogous to (but distinct from) the running of coupling
constants in perturbative QFT: here, the "running" is with respect to volume
rather than energy scale, and the effect is non-perturbative.

**Evidence classification:** δγ is rated [B/D] — the magnitude [B] follows from
the numerical extrapolation, while the physical interpretation as vacuum
dressing carries an element of model dependence [D].

---

## 6. Holographic Amplification

The key step connecting vacuum structure to cosmology is the holographic
amplification through the L⁴ factor:

```
w_a = −δ × L⁴
```

For the reference holographic extent L = 8.2:

```
L⁴ = 8.2⁴ = 4521.2176
w_a = −2.8757 × 10⁻⁴ × 4521.2176 ≈ −1.300
```

The L⁴ scaling arises from the four-dimensional volume measure in the
holographic mapping between the lattice vacuum and the cosmological dark-energy
sector. A scan over the range L ∈ [8.15, 8.25] shows that w\_a remains within
the DESI-DR2 + Union3 1σ band (−1.59 to −0.95) across the full range.

See `verification/data/holographic_l_range.csv` for the complete scan table.

---

## 7. Evidence Classification

| Quantity | Value | Category | Rationale |
|----------|-------|----------|-----------|
| Δ (spectral gap) | 1.710 ± 0.015 GeV | [A] | Lattice QCD confirmed |
| γ (dressed) | 16.339 | [A-] | Phenomenological fit, high precision |
| γ\_∞ (bare) | 16.3437 ± 10⁻⁴ | [B] | Numerical extrapolation |
| δγ | 0.0047 | [B/D] | Numerically derived, interpretation model-dependent |
| δ (relative shift) | 2.8757 × 10⁻⁴ | [B] | Ratio of numerically determined quantities |
| w\_a | −1.300 | [C] | Cosmological observable, interpretive mapping |

**Important constraints:**
- γ is [A-] and must never be upgraded to [A] (it is phenomenologically, not
  first-principles, determined).
- All cosmological parameters (H₀, w₀, w\_a, S₈) are capped at [C] maximum.

---

## 8. Reproduction

To reproduce the bare gamma extrapolation:

```bash
cd verification/
python verify_bare_gamma.py
```

This script:
1. Reads lattice γ(L) data from `data/gamma_finite_size.csv`
2. Performs the finite-size scaling fit
3. Reports γ\_∞, δγ, δ, and the derived w\_a
4. Generates diagnostic plots in `output/`

Expected output:
```
γ_∞ = 16.3437 ± 0.0001  [B]
δγ  = 0.0047             [B/D]
δ   = 0.00028757         [B]
w_a = -1.300 (L=8.2)     [C]
```

---

## 9. References

1. P. Rietz, "Vacuum Information Density as the Fundamental Geometric Scalar,"
   UIDT Framework v3.9, DOI: [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

2. DESI Collaboration, "DESI DR2 Baryon Acoustic Oscillation Measurements,"
   arXiv: [2503.14738](https://arxiv.org/abs/2503.14738)

3. Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters,"
   arXiv: [1807.06209](https://arxiv.org/abs/1807.06209),
   DOI: [10.1051/0004-6361/201833910](https://doi.org/10.1051/0004-6361/201833910)

4. M. Lüscher, "Volume dependence of the energy spectrum in massive quantum
   field theories. I. Stable particle states,"
   Commun. Math. Phys. **104**, 177 (1986),
   DOI: [10.1007/BF01211589](https://doi.org/10.1007/BF01211589)

5. Y. Chen et al., "Glueball spectrum and matrix elements on anisotropic
   lattices," Phys. Rev. D **73**, 014516 (2006),
   arXiv: [hep-lat/0510074](https://arxiv.org/abs/hep-lat/0510074)
