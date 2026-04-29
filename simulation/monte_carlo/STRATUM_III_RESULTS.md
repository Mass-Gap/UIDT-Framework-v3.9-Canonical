# Stratum III — UIDT Mapping, Lattice Comparison, Publication Positioning

**Stratum III maps Stratum I/II results onto the UIDT theoretical framework
and external reference data.**
All UIDT-specific mappings are explicitly labelled as interpretive or predictive.
Cosmological parameters are capped at evidence category [C] maximum.

**Version:** 2026-04-29 (precision update)

---

## 1. Canonical Cosmology Path (retained unchanged)

**This PR does not modify the canonical w_a derivation.**

| Quantity | Value | Category | Reference |
|---|---|---|---|
| w₀ | −0.99 | [C] | Decision D-002 |
| w_a (UIDT canonical) | −1.300 | [C] | bare-gamma holographic dressing, L = 8.2 |
| w_a (DESI DR2 + Union3) | −1.27 ± 0.37 | Stratum I ext. | arXiv:2503.14738 |
| Mahalanobis distance | 0.65 σ | [C] | `docs/DESI_DR2_alignment_report.md` |

> H₀ and S₈ tensions are **NOT declared resolved.**
> Cosmological tensions may not be labelled resolved without Category [A] evidence.

---

## 2. Ψ → w_a Mapping (prediction only)

**Evidence category: [D] — prediction, not confirmed**

A Ψ-based w_a scaling has been discussed in internal UIDT notes. Any such mapping:

- must **not** overwrite the canonical bare-gamma pathway,
- must be separately fitted against the repository reference w_a = −1.27 ± 0.37
  (DESI/Union3) in a clean, independently documented computation,
- must account for the asymmetric-tail behavior of Ψ (Stratum I § 4) before
  any category upgrade beyond [D] is considered.

---

## 3. Lattice QCD Compatibility Test

**Reference:** Morningstar & Peardon, Phys. Rev. D 60, 034509 (1999)
DOI: [10.1103/PhysRevD.60.034509](https://doi.org/10.1103/PhysRevD.60.034509)
arXiv: [hep-lat/9901004](https://arxiv.org/abs/hep-lat/9901004)

Scalar glueball ground-state mass (quenched approximation):
Δ*(lattice) = 1.730 ± 0.090 GeV

MC result (Stratum I § 2):
Δ*(MC) = 1.710044 ± 0.014993 GeV

| Quantity | Value | Category |
|---|---|---|
| χ² | 0.0478 | [B] |
| p-value | 0.8269 | [B] |
| \|z\| | 0.2187 σ | [B] |

**Result [B]:** Δ*(MC) is fully compatible with the Morningstar & Peardon
quenched-lattice determination. The 0.22 σ deviation is well within combined
uncertainties.

**Limitation:** Morningstar & Peardon (1999) uses the quenched approximation.
Unquenched (dynamical-fermion) results may shift the central value; an updated
lattice comparison should be considered for publication.

---

## 4. Corner Plot — Publication Positioning

The 5-parameter corner plot (Δ*, γ, Ψ, κ, λ_S) with LEDGER reference lines confirms:

- All LEDGER reference lines lie within the posterior core regions.
- The κ–λ_S axis shows the near-degenerate linear track expected from 5κ² = 3λ_S.
- r(γ, Ψ) ≈ −0.005 from the 2D contour, indicating statistical independence.

The corner plot is suitable for a methodology section or appendix.
Caption must clarify that LEDGER reference lines are calibrated / phenomenological
values [A/A-], not external experimental measurements.

Plot reproduction code: `PLOTS_REGISTRY.md`.

---

## 5. Summary of LaTeX Appendix (`clay_appendix_mc_evidence.tex`)

The appendix file documents the following sections:

1. MCMC convergence table (all 10 parameters, R̂, N_eff, τ_int)
2. LEDGER consistency: Δ* and γ with z-scores and p-values
3. Holography relation: δγ = 0.0047, L = 8.2, w_a ≈ −1.300 [C]
4. Lattice compatibility: χ², p, |z| vs Morningstar & Peardon (1999)
5. Anti-correlation r(γ, kinetic_VEV) = −0.982 and 2.3-damping mapping
6. **Open tension:** r(Δ*, Π_S) conflict — `[TENSION ALERT]` explicitly retained
7. **Soft RG residual:** `[RG_CONSTRAINT_FAIL]` flag — explicitly retained

The last two items are open. They must not be silently omitted from any
submission that uses this appendix.

---

## 6. Known Limitations (UIDT LIMITATION_POLICY — mandatory)

- L_holographic = 8.2 is a non-canonical free parameter (open issue S1-01).
  All w_a values derived via L⁴ amplification inherit this ambiguity.
- γ is phenomenological [A-], not RG-derived. The γ∞ extrapolation [B]
  inherits this foundational limitation.
- r(Δ*, Π_S) is under active provenance audit (see Stratum II § 3).
- The soft `[RG_CONSTRAINT_FAIL]` at hp-mean level must be resolved before
  any claim that depends on the RG constraint being exactly satisfied is upgraded.
- N = 99 cascade steps have no first-principles derivation (known L5).
- Cosmological tensions (H₀, S₈) are **not** declared resolved.
