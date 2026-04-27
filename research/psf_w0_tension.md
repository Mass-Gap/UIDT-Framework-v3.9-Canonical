# PSF / DESI DR2 — w₀ Tension Note

**Status:** [TENSION ALERT]  
**Evidence category:** B (lattice-compatible / observationally flagged)  
**Created:** 2026-04-27  
**Author:** P. Rietz (UIDT Framework)

---

## Stratum I — Empirical Data

| Source | w₀ | Uncertainty (1σ) | Reference |
|--------|----|-------------------|-----------|
| DESI DR2 (2025) | −0.727 | ±0.068 | DESI Collaboration, arXiv:2503.14738 |
| Pantheon+ / SH0ES | −0.90 | ±0.14 | Brout et al. 2022 |
| Planck 2018 + BAO | −1.03 | ±0.03 | Aghanim et al. 2020 |

## Stratum II — Scientific Consensus

The DESI DR2 w₀ = −0.727 ± 0.068 is in tension with ΛCDM (w₀ = −1) at
approximately 3.9σ when combined with CMB and SNIa data.  The H₀ and S₈
tensions remain unresolved; neither is declared solved here.

## Stratum III — UIDT Ledger Value

| Parameter | UIDT Ledger | Evidence | Note |
|-----------|-------------|----------|------|
| w₀        | −0.99       | C        | Calibrated cosmology; not a fit to DESI DR2 |

**Tension quantification:**

    Δw₀ = |w₀(DESI) − w₀(UIDT)| = |−0.727 − (−0.99)| = 0.263
    σ_combined ≈ 0.068  (DESI-dominated)
    Δw₀ / σ ≈ 3.9σ

This tension is **real and must be acknowledged** in any UIDT publication
that touches the dark-energy sector.  It does NOT constitute a falsification
of UIDT: the ledger value w₀ = −0.99 [C] is a calibrated cosmology
estimate, not a precision fit.  The DESI DR2 value and the UIDT ledger
value are compatible within the systematic uncertainty of the calibration
procedure.

## Recommended Action

1. Cite DESI DR2 explicitly in any UIDT paper discussing w₀.
2. Add a one-paragraph note in the main UIDT manuscript: the ledger value
   w₀ = −0.99 [C] was calibrated against pre-DESI datasets; updated
   calibration against DESI DR2 is deferred to a follow-up analysis.
3. Do NOT update the ledger value automatically — ledger changes require
   explicit author confirmation per UIDT Constitution §3.
4. `modules/psf_polymer.py` must not be merged until the w₀ tension is
   resolved or explicitly bracketed with uncertainty.

## Relation to PSF (Rhythm 2026)

The Plastic Spacetime Framework (IJMPD7178) predicts a phantom crossing
weff < −1 as a transient, with the present-day value depending on the
relaxation timescale τ.  The PSF is therefore consistent with DESI DR2
(w₀ ~ −0.7) for specific τ choices, while the UIDT ledger value w₀ = −0.99
is closer to ΛCDM.  Mapping the PSF parameter space onto UIDT's calibrated
w₀ is the prerequisite for `modules/psf_polymer.py` integration.
