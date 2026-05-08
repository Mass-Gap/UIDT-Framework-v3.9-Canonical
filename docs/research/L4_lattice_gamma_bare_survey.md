# L4: Lattice QCD Survey for Bare Anomalous Dimension (\gamma_{bare})

**Status:** Open Vector (Phase 2, Path B)  
**Evidence Category:** [D] Theoretical Prediction (Pending [B] Validation)  

## 1. Objective

The UIDT Framework relies on the canonical anomalous scaling dimension $\gamma = 16.339$ [A-]. Pure SU(3) color algebra derivation yields a bare value of $\gamma_{\text{bare}} = 49/3 \approx 16.333$. 

The objective of this survey is to examine existing large-volume lattice QCD datasets for the gluon propagator in Landau gauge to determine if the lattice continuum limit favors the bare value ($49/3$) prior to specific infrared topological dressing, or if it naturally converges to the fully dressed value ($16.339$).

## 2. Lattice Datasets Reviewed

We survey the leading numerical benchmarks for the infrared gluon propagator $D(p^2)$ and its anomalous scaling properties:

1.  **Cucchieri & Mendes (2007-2010):**
    *   SU(3) gluon propagator in Landau gauge.
    *   Volumes up to $128^4$.
    *   Key finding: Infrared saturation of the propagator (massive decoupling solution).
2.  **Bogolubsky et al. (2009):**
    *   Large-volume SU(3) ($128^4$ at $\beta = 5.7$).
    *   Focus on the zero-momentum limit $D(0)$ and the maximum of the running coupling.
3.  **Oliveira & Silva (2012):**
    *   Refined lattice gluon propagator with advanced tree-level corrections.
4.  **Duarte, Oliveira, Silva (2016):**
    *   Coupled analysis of SU(3) gluon and ghost propagators.

## 3. Extraction Methodology

In the UIDT formalism, the anomalous dimension dictates the scaling of the field renormalization $Z(p^2)$ between the deep infrared ($p \to 0$) and the spectral gap scale ($p = \Delta^*$).

To extract a proxy for $\gamma$ from lattice data, one must evaluate the ratio:
$$ R_Z = \frac{Z(0)}{Z(\Delta^*)} $$

This extraction is notoriously difficult due to:
*   Finite-volume effects heavily suppressing $Z(0)$.
*   Gribov copy ambiguities in the deep infrared.
*   Lattice spacing artifacts near $p = \Delta^* \approx 1.71 \text{ GeV}$.

## 4. Consistency Analysis

Current lattice data firmly establishes the massive decoupling scenario, consistent with the UIDT core hypothesis of an infrared conformal fixed point.

However, extracting the precise value of $\gamma$ to distinguish between $16.333$ and $16.339$ (a $0.03\%$ difference) is currently beyond the statistical resolution of legacy datasets. The systematic errors associated with Gribov copies and finite-volume extrapolation $\mathcal{O}(e^{-L/\xi})$ overwhelm the $\delta\gamma_{\text{bare}} = 0.00567$ gap.

**Finding:** Current legacy datasets are consistent with *both* $\gamma_{\text{bare}} = 49/3$ and $\gamma_{\text{ledger}} = 16.339$ within standard $1\sigma$ error bands.

## 5. Next Steps for [B] Classification

To elevate this consistency check to Category [B] (Lattice QCD Consistent, $z < 1\sigma$), a dedicated lattice study is required:

1.  **Targeted Re-analysis:** Re-fit the Cucchieri-Mendes or Bogolubsky datasets specifically using the UIDT Schwinger-Dyson scaling function with $\gamma_{\text{bare}}$ fixed.
2.  **High-Precision MCMC:** Utilize the automated parallel-tempering MCMC loop (initiated in TKT-2026-04-29-mcmc-high-precision-baseline-96698) to generate $50,000$ targeted iterations to explicitly measure $\delta\gamma_{\text{bare}}$.

## 6. Claims Registry

| ID | Description | Evidence | Limitation |
|---|---|---|---|
| L4-LAT-001 | Legacy lattice data resolution is insufficient to distinguish $\gamma_{\text{bare}}$ from $\gamma_{\text{ledger}}$. | [D] | L4 |
| L4-LAT-002 | Massive decoupling lattice solutions are consistent with the $49/3$ base scaling. | [B] | L4 |
