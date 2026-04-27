# GMC Echo Timing — UIDT Mapping Note

**Status:** Speculative mapping  
**Evidence category:** D/E  
**Created:** 2026-04-27  
**Author:** P. Rietz (UIDT Framework)

---

## The GMC Prediction

The Gravitational Memory Condensate (GMC) mechanism (Rhythm 2026)
predicts a GW echo timing:

    Delta_t_echo(GMC)       = (1/2) * t_Schwarzschild
    Delta_t_echo(canonical) = ~8 * G*M/c^3

Ratio: factor 1/16 difference. Falsifiable with Einstein Telescope (ET3) / LISA.

## UIDT Connection

The GMC uses epsilon_eff = 3 (Euler characteristic of S^2 boundary).
The UIDT torsion correction to the Schwarzschild radius:

    delta_T ~ ET^2 / (M_Planck^2 * c^4)

For stellar-mass BHs (M ~ 10--60 M_sun): delta_T ~ 10^{-40}.
Numerically negligible for all current and near-future detectors.
May be relevant only near the Planck scale.

## Circularity Concern (Appendix A.2)

The topological invariant epsilon_eff = 3 is motivated by the Euler
characteristic of S^2, but the boundary is defined using the standard
Schwarzschild radius. If the GMC mechanism modifies the interior metric,
the boundary definition changes and epsilon_eff may shift.

**Required action:** Clarify with author whether epsilon_eff = 3 is
derived independently of the GR Schwarzschild boundary.

## Falsification Table

| Observable           | GMC prediction | Canonical | UIDT correction |
|----------------------|---------------|-----------|------------------|
| Delta_t / t_S        | 1/2           | ~8        | ~10^{-40} (negligible) |
| Echo frequency f     | c/(pi*r_S)    | same      | negligible       |

## Repository Status

No production code. Integration into modules/ deferred until:
1. Circularity in Appendix A.2 resolved.
2. arXiv/DOI of GMC paper verified ([AUDIT_FAIL] if unverifiable).
