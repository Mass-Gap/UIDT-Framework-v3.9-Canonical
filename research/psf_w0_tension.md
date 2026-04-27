# PSF / DESI DR2 — w0 Tension Note

**Status:** [TENSION ALERT]  
**Evidence category:** B (lattice-compatible / observationally flagged)  
**Created:** 2026-04-27  
**Author:** P. Rietz (UIDT Framework)

---

## Stratum I — Empirical Data

| Source | w0 | Uncertainty (1sigma) | Reference |
|--------|----|---------------------|-----------|
| DESI DR2 (2025) | -0.727 | +/-0.068 | DESI Collaboration, arXiv:2503.14738 |
| Pantheon+ / SH0ES | -0.90 | +/-0.14 | Brout et al. 2022 |
| Planck 2018 + BAO | -1.03 | +/-0.03 | Aghanim et al. 2020 |

## Stratum II — Scientific Consensus

The DESI DR2 w0 = -0.727 +/- 0.068 is in tension with LambdaCDM (w0 = -1)
at approximately 3.9sigma when combined with CMB and SNIa data.
The H0 and S8 tensions remain unresolved; neither is declared solved here.

## Stratum III — UIDT Ledger Value

| Parameter | UIDT Ledger | Evidence | Note |
|-----------|-------------|----------|------|
| w0 | -0.99 | C | Calibrated cosmology; not a fit to DESI DR2 |

**Tension quantification:**

    Delta_w0 = |w0(DESI) - w0(UIDT)| = |-0.727 - (-0.99)| = 0.263
    sigma_combined ~= 0.068  (DESI-dominated)
    Delta_w0 / sigma ~= 3.9sigma

This tension is real and must be acknowledged in any UIDT publication
touching the dark-energy sector. It does NOT constitute a falsification
of UIDT: w0 = -0.99 [C] is a calibrated cosmology estimate, not a
precision fit. Updated calibration against DESI DR2 is deferred to a
follow-up analysis.

## Recommended Action

1. Cite DESI DR2 explicitly in any UIDT paper discussing w0.
2. Add a note in the main UIDT manuscript: the ledger value w0 = -0.99 [C]
   was calibrated against pre-DESI datasets.
3. Do NOT update the ledger value automatically -- ledger changes require
   explicit author confirmation per UIDT Constitution §3.
4. `modules/psf_polymer.py` must not be merged until w0 tension is
   resolved or explicitly bracketed with uncertainty.

## Relation to PSF (Rhythm 2026)

The Plastic Spacetime Framework (IJMPD7178) predicts a phantom crossing
weff < -1 as a transient. The PSF is consistent with DESI DR2 (w0 ~ -0.7)
for specific tau choices, while the UIDT ledger w0 = -0.99 is closer to
LambdaCDM. Mapping the PSF parameter space onto UIDT's calibrated w0 is
the prerequisite for modules/psf_polymer.py integration.
