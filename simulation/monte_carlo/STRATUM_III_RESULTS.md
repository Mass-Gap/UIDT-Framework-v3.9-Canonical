# Stratum III — UIDT Mapping, Lattice Comparison, Publication Positioning

**Stratum III maps Stratum I/II results onto the UIDT theoretical framework
and external reference data.**
All UIDT-specific mappings are explicitly labelled as interpretive or predictive.
Cosmological parameters are capped at evidence category [C] maximum.

---

## 1. Canonical Cosmology Path (retained)

**This PR does not modify the canonical w_a derivation.**

The existing repository derivation:

| Quantity | Value | Category | Source |
|---|---|---|---|
| δγ | 0.0047 | [B/D] | `docs/bare_gamma_theorem.md` |
| L (holographic length) | 8.2 (non-canonical free parameter) | — | `docs/DESI_DR2_alignment_report.md` |
| w_a(canonical) | −1.300 | [C] | holographic dressing pathway |
| w_0(canonical) | −0.99 | [C] | Decision D-002 |

External reference (DESI DR2 + Union3):

| Quantity | Value | Source |
|---|---|---|
| w_0 (observed) | −0.67 ± 0.09 | arXiv:2503.14738 |
| w_a (observed) | −1.27 ± 0.37 | arXiv:2503.14738 |
| Mahalanobis distance UIDT vs data | 0.65 σ | `docs/DESI_DR2_alignment_report.md` |

**Status:** compatible (0.65 σ), classified [C]. H₀ and S₈ tensions are **not** declared resolved.

---

## 2. Ψ → w_a Forecast (prediction only)

**Evidence category: [D] — prediction, not confirmed**

The MC posterior for Ψ shows non-Gaussian tails (Stratum II §5).
A Ψ-based w_a mapping has been discussed qualitatively in UIDT internal notes.

**This mapping must not overwrite the canonical bare-gamma pathway.**
Any Ψ → w_a inference remains at category [D] until:
- the Ψ non-Gaussianity is analytically characterized,
- an independent verification script reproduces the mapping numerically,
- the result is formally separated from the [C]-classified canonical w_a.

---

## 3. Lattice QCD Compatibility Test

**Reference lattice value:**
Morningstar & Peardon (1999), scalar glueball ground state:
Δ*(lattice) = 1.730 ± 0.090 GeV
DOI: [10.1103/PhysRevD.60.034509](https://doi.org/10.1103/PhysRevD.60.034509)
arXiv: [hep-lat/9901004](https://arxiv.org/abs/hep-lat/9901004)

**MC result (Stratum I):** Δ*(MC) = 1.710044 ± 0.014993 GeV

| Quantity | Value | Category |
|---|---|---|
| χ² | 0.0478 | [B] |
| p-value | 0.8269 | [B] |
| \|z\| | 0.2187 σ | [B] |

**Interpretation [B]:** Δ*(MC) is fully compatible with the Morningstar & Peardon
quenched-lattice determination. The 0.22 σ deviation is well within the
combined uncertainty. This supports a lattice-compatible classification [B]
but does not constitute a first-principles derivation [A].

**Limitation note:** Morningstar & Peardon (1999) is a quenched-approximation result.
Unquenched (dynamical-fermion) lattice results may shift the central value and
should be consulted for a fully updated comparison.

---

## 4. Corner Plot and Posterior Geometry (publication positioning)

The 5-parameter corner plot (Δ*, γ, Ψ, κ, λ_S) with LEDGER reference lines
confirms:

- All LEDGER reference lines lie within the posterior core regions.
- The κ–λ_S axis shows a near-degenerate linear track consistent with
  the RG fixed-point constraint 5κ² = 3λ_S.
- The γ–Ψ 2D contour shows r ≈ −0.005, indicating statistical independence
  of these two parameters at the MC sampling level.

**Publication use:** The corner plot is suitable for a methodology section
or appendix. It must be captioned to clarify that LEDGER reference lines
represent calibrated/phenomenological values [A/A-], not external measurements.

Plot file locations and reproduction code: see `PLOTS_REGISTRY.md`.

---

## 5. Known Limitations (mandatory per UIDT LIMITATION_POLICY)

- **L_holographic = 8.2** is a non-canonical free parameter (S1-01 open issue).
  All w_a values derived via L⁴ amplification inherit this ambiguity.
- **γ is phenomenological [A-]**, not RG-derived. The γ∞ extrapolation [B]
  inherits this limitation.
- **r(Δ*, Π_S)** is under active provenance audit. See Stratum II §3.
- **N = 99 cascade steps** used in vacuum energy calculations have no
  first-principles justification (known limitation L5).
- Cosmological tensions (H₀, S₈) are **not** declared resolved in this PR.
