# PR Claims Table — Monte Carlo Research Notes Integration

**PR:** [UIDT-v3.9] simulation/monte_carlo: integrate audited MC research notes
**Date:** 2026-04-29
**Maintainer:** P. Rietz

This table satisfies the UIDT PR Gate requirement:
every scientific claim must have an ID, evidence category, and source identifier.

---

## Claims

| ID | Stratum | Claim | Category | Source Identifier | Status |
|---|---|---|---|---|---|
| S1-MC-01 | I | All 10 MC parameters satisfy publication-level convergence (R̂ < 1.001, N_eff > 99 000, τ_int ≈ 0.50) | [A] | `UIDT_MonteCarlo_samples_100k.csv` raw-chain audit | ✅ supported |
| S1-MC-02 | I | Δ* MC posterior is consistent with LEDGER: residual 4.4 × 10⁻⁵ GeV, 0.003 σ, p = 0.998 | [A] | raw-chain audit vs LEDGER [A] | ✅ supported |
| S1-MC-03 | I | γ MC posterior is consistent with LEDGER: residual 0.035, 0.035 σ, p = 0.972 | [A-] | raw-chain audit vs LEDGER [A-] | ✅ supported |
| S1-MC-04 | I | γ and Ψ show strongest non-Gaussian / asymmetric-tail behavior; all others near-Gaussian | [A] | raw-chain posterior shape statistics | ✅ supported |
| S1-MC-05 | I | RG constraint 5κ² = 3λ_S satisfied in hp-mean check within tolerance 1 × 10⁻¹⁴ | [A] | `test_monte_carlo_summary.py` | ✅ supported |
| S2-MC-01 | II | MC γ-posterior propagates to γ∞(MC) = 16.369 ± 1.005, consistent with canonical γ∞ = 16.3437 [B] | [A-]/[B] | `STRATUM_II_RESULTS.md` §1 + `bare_gamma_theorem.md` | ✅ supported |
| S2-MC-02 | II | r(γ, kinetic_VEV) = −0.982 supports anti-proportional coupling interpretation | [B] | `UIDT_MonteCarlo_correlation_matrix.csv` | ✅ supported |
| S2-MC-03 | II | r(κ, λ_S) ≈ +0.99 is a direct consequence of RG fixed-point constraint | [A] | correlation matrix + RG derivation | ✅ supported |
| S2-MC-04 | II | r(Δ*, Π_S) = +0.720 from stored matrix is **not** independently reproduced from raw chain | [TENSION] | stored matrix vs raw-chain audit | ⚠️ flagged |
| S3-MC-01 | III | Canonical w_a = −1.300 pathway (bare-gamma holographic dressing) is retained unchanged | [C] | `docs/DESI_DR2_alignment_report.md` | ✅ retained |
| S3-MC-02 | III | UIDT vs DESI DR2+Union3: Mahalanobis distance 0.65 σ | [C] | `docs/DESI_DR2_alignment_report.md` + arXiv:2503.14738 | ✅ retained |
| S3-MC-03 | III | Ψ → w_a mapping is a prediction only; must not overwrite canonical pathway | [D] | `STRATUM_III_RESULTS.md` §2 | ✅ constrained |
| S3-MC-04 | III | Δ*(MC) compatible with Morningstar & Peardon quenched-lattice: χ² = 0.048, p = 0.827, \|z\| = 0.22 σ | [B] | DOI:10.1103/PhysRevD.60.034509 + arXiv:hep-lat/9901004 | ✅ supported |
| S3-MC-05 | III | Corner plot LEDGER reference lines lie within posterior core — visual consistency check | [A-] | `PLOTS_REGISTRY.md` + corner plot figure | ✅ supported |

---

## DOI / arXiv Resolvability Check

| Identifier | Type | Verified |
|---|---|---|
| 10.5281/zenodo.17835200 | Zenodo canonical DOI | ✅ |
| 10.5281/zenodo.17554179 | Zenodo dataset DOI | ✅ |
| 10.1103/PhysRevD.60.034509 | Morningstar & Peardon (1999) | ✅ |
| hep-lat/9901004 | arXiv identifier | ✅ |
| 2503.14738 | DESI DR2 arXiv | ✅ |

---

## Reproduction Note

```bash
# Existing verification test (covers S1-MC-02, S1-MC-03, S1-MC-05)
pytest verification/tests/test_monte_carlo_summary.py -v
```

Pending (to cover S1-MC-01, S1-MC-04, S2-MC-02, S2-MC-04, S3-MC-04):
```bash
python verification/scripts/verify_monte_carlo_research_notes.py
```
(script to be added in a follow-up PR)

---

## Affected Constants and Evidence Categories

**No immutable LEDGER constant is modified by this PR.**

Referenced constants (read-only):

| Constant | Value | Category |
|---|---|---|
| Δ* | 1.710 ± 0.015 GeV | [A] |
| γ | 16.339 | [A-] |
| γ∞ | 16.3437 ± 1 × 10⁻⁴ | [B] |
| δγ | 0.0047 | [B/D] |
| w₀ | −0.99 | [C] |
| ET | 2.44 MeV | [C] |
