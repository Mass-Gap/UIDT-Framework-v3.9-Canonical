# L4: 1-Loop Vacuum Correction (\delta\gamma_{bare}) and the Color Algebra Gap

**Status:** Open Vector (Phase 1, Path B)  
**Evidence Category:** [D] Theoretical Prediction  
**Related Script:** `verification/scripts/verify_L4_delta_gamma_1loop.py`

## 1. Problem Statement

In the UIDT Framework (v3.9.6), there is a known tension in the formulation of the anomalous scaling dimension $\gamma$. The canonical phenomenological value required to match cosmological and lattice bounds is:
$$ \gamma_{\text{ledger}} = 16.339 \quad [\text{A-}] $$

However, the pure algebraic derivation for an $SU(3)$ gauge theory based on scaling dimensions yields the "bare" parameter:
$$ \gamma_{\text{bare}} = \frac{49}{3} \approx 16.333333333333332 $$

The difference between these two quantities defines the "color algebra gap", denoted $\delta\gamma_{\text{bare}}$:
$$ \delta\gamma_{\text{bare}} = \gamma_{\text{ledger}} - \gamma_{\text{bare}} = 0.005666666666668 $$

*(Note: This is strictly distinct from the finite-size scaling dressing $\delta\gamma = 0.0047$, which bridges the lattice $V \to \infty$ continuum limit to the canonical phenomenological value.)*

This document addresses **Limitation L4**: The missing first-principles RG derivation of the full $\gamma = 16.339$. Our hypothesis (Path B) is that $\delta\gamma_{\text{bare}}$ originates from a 1-loop vacuum correction at the scale $p = \Delta^*$.

## 2. Ledger Consistency Check

All input values for this derivation are anchored in the `CONSTANTS.md` ledger as Category [A] or [A-] evidence:

*   **Spectral Gap:** $\Delta^* = 1.710 \text{ GeV}$ [A]
*   **Vacuum Expectation:** $v = 47.7 \text{ MeV}$ [A]
*   **Coupling Constant:** $\kappa = 0.5$ [A]
*   **RG Fixed Point:** $\lambda_S = 5\kappa^2 / 3 = 5/12 \approx 0.41667$ [A]

The precision arithmetic evaluation in `mpmath` (`mp.dps=80`) strictly enforces these constraints.

## 3. Feynman Diagram Structure

The correction is hypothesized to arise from the 1-loop scalar bubble diagram evaluated precisely at the mass gap scale. We consider the interaction vertex governed by the effective coupling derived from $\lambda_S$.

The scalar self-energy $\Pi_S(p^2)$ contributes to the wave-function renormalization $Z_\phi$:
$$ Z_\phi(p^2) = 1 - \frac{d\Pi_S(p^2)}{dp^2} $$

The anomalous dimension correction is defined through the logarithmic derivative of $Z_\phi$ with respect to the momentum scale $k$, evaluated at $k = \Delta^*$:
$$ \Delta\gamma_{\text{1-loop}} = - \left. \frac{d(\ln Z_\phi)}{d(\ln k)} \right|_{k=\Delta^*} $$

## 4. Analytical Approximation (Path B Bound)

For an effective $SU(3)$ scalar field, the 1-loop loop integral yields a correction proportional to the square of the effective coupling $g_{\text{eff}}^2$.

$$ g_{\text{eff}}^2 \propto \frac{\lambda_S^2}{16\pi^2} $$

With a color factor $N_c = 3$ (yielding algebraic constants like $9/4$), the analytical structure bound is expected to be:
$$ \Delta\gamma_{\text{1-loop}} \propto g_{\text{eff}}^2 \cdot \frac{9}{4} \cdot f\left(\frac{\Delta^*}{v}\right) $$

where $f(\Delta^*/v)$ is a scaling function relating the deep infrared VE to the spectral gap. The goal of Path B is to rigorously prove that:
$$ \Delta\gamma_{\text{1-loop}} \equiv \delta\gamma_{\text{bare}} = 0.005666... $$

## 5. Falsifiability and Limitations

This hypothesis is falsifiable. The following conditions would immediately rule out Path B and reclassify the approach to [E] (Withdrawn):

1.  **BMW Truncation Failure:** If a full Functional Renormalization Group (FRG) analysis using BMW (Blaizot-Mendez-Galain-Wschebor) momentum-dependent truncation demonstrates that the 1-loop contribution to the anomalous dimension has the *wrong sign* (i.e., it decreases rather than increases $\gamma$).
2.  **Topological Dominance:** If topological susceptibility corrections (e.g., instanton gas contributions) are shown to be the dominant source of the $0.00567$ shift, rendering the perturbative 1-loop bubble negligible.

**Critical NO-GO Status:** As documented in `TKT-20260429-FRG-STEP5-lambda3-flow.md`, evaluating this gap using Local Potential Approximation (LPA') at NLO fails by three orders of magnitude. The full momentum-dependent BMW truncation is strictly required for this derivation.

## 6. Claims Registry Additions

| ID | Description | Evidence | Limitation |
|---|---|---|---|
| L4-DG-001 | Defines $\delta\gamma_{\text{bare}} = 0.005666...$ as the color algebra gap. | [A-] | L4 |
| L4-DG-002 | Proposes $\Delta\gamma_{\text{1-loop}}$ at $p=\Delta^*$ as the source of $\delta\gamma_{\text{bare}}$. | [D] | L4 |

## 7. Reproduction

The target numerical bounds are verified via:
```bash
python verification/scripts/verify_L4_delta_gamma_1loop.py
```
This script confirms the 80-digit precision arithmetic for the gap target.
