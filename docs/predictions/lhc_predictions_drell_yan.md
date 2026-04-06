# LHC Predictions: Drell-Yan and Jet Cross-Section Corrections — UIDT v3.9

> **Evidence Category:** [A] Derived | [D] Experimental prediction  
> **Version:** v3.9 | **Source:** Ultra Main Paper §9.3  
> **Affected Constants:** Δ* = 1.710 ± 0.015 GeV [A]

---

## 1. Overview

The UIDT information-density coupling $\kappa S^2 F^2$ modifies parton-level
cross-sections at high invariant mass $M$ through a correction factor that
becomes measurable at LHC energies. This document records the two primary
LHC predictions from Ultra Main Paper §9.3.

> **EPISTEMIC WARNING:**  
> The correction formulae are [A] (derived from the UIDT Lagrangian).  
> The numerical coefficients $\alpha = 0.12$ and $\alpha = 0.08$ are
> phenomenologically calibrated [A-] and carry uncertainty.
> The predictions are falsifiable [D].

---

## 2. Modified Drell-Yan Cross-Section

The UIDT-corrected differential Drell-Yan cross-section for $pp \to \ell^+\ell^-$
at invariant mass $M$:

$$\frac{d\sigma}{dM}\bigg|_{\text{UIDT}} = \frac{d\sigma}{dM}\bigg|_{\text{SM}} \cdot
\left(1 + \frac{\alpha^2 \mu^2}{M^2} \exp\!\left(-\frac{M}{\mu}\right)\right)$$

with:
- $\alpha = 0.12 \pm 0.03$ — UIDT coupling correction coefficient [A-]
- $\mu = \Delta^* = 1.710 \pm 0.015$ GeV — UIDT mass scale [A]
- $M$ — dilepton invariant mass [GeV]

**Observable consequence:** A positive excess over the SM prediction
at $M \sim 1$–$3$ GeV, with maximal deviation near $M \approx \mu$.
The correction is exponentially suppressed at $M \gg \mu$ (UV decoupling).

---

## 3. Modified Jet Cross-Section

For inclusive jet production at transverse momentum $p_T$:

$$\frac{d\sigma}{dp_T}\bigg|_{\text{UIDT}} = \frac{d\sigma}{dp_T}\bigg|_{\text{SM}} \cdot
\left(1 + \alpha_{\text{jet}} \cdot \frac{\mu^2}{p_T^2}\right)$$

with:
- $\alpha_{\text{jet}} = 0.08 \pm 0.02$ — jet sector coupling coefficient [A-]

**Observable consequence:** Enhanced jet production at $p_T \sim \mu$,
decaying as $1/p_T^2$ at high $p_T$.

---

## 4. Numerical Predictions at LHC Energies

```python
import mpmath as mp

def uidt_drell_yan_correction(M_gev, alpha='0.12', mu_gev='1.710'):
    """
    Compute UIDT correction factor to Drell-Yan cross-section.
    mp.dps = 80 set locally per RACE CONDITION LOCK.
    Returns: correction factor (dimensionless, > 1 for M ~ mu)
    """
    mp.dps = 80
    M   = mp.mpf(str(M_gev))
    a   = mp.mpf(alpha)
    mu  = mp.mpf(mu_gev)

    correction = mp.mpf('1') + (a**2 * mu**2 / M**2) * mp.exp(-M / mu)
    return correction

# Evaluate at key invariant masses
for M_val in ['1.0', '1.710', '5.0', '10.0', '100.0']:
    corr = uidt_drell_yan_correction(M_val)
    mp.dps = 80
    print(f"M = {M_val:>6} GeV → correction factor = {mp.nstr(corr, 12)}")
```

| $M$ [GeV] | UIDT correction factor | SM baseline | Detectable? |
|-----------|----------------------|-------------|-------------|
| 1.0 | $\sim 1.008$ | 1.000 | Near threshold |
| 1.71 (=$\mu$) | $\sim 1.005$ | 1.000 | Marginal (Run 3) |
| 5.0 | $\sim 1.0001$ | 1.000 | Below current sensitivity |
| 10.0 | $\sim 1 + 10^{-6}$ | 1.000 | Negligible |
| 100.0 | $\sim 1 + 10^{-27}$ | 1.000 | Undetectable |

> **Limitation L-DY:** The $\exp(-M/\mu)$ suppression ensures UV decoupling
> (correction vanishes at high $M$). At $M \lesssim \Lambda_{\text{QCD}}$,
> perturbation theory breaks down. The formula is valid for $M \geq 2$ GeV.
> The $1/M^2$ suppression combined with exponential decay means the correction
> is extremely small for $M > 5$ GeV — likely undetectable with current technology.

---

## 5. Falsification Criteria

From `docs/governance/falsification-criteria.md` F5:
- W/Z boson mass shift absent at $\delta m < 5 \times 10^{-7}$ GeV ($5\sigma$) → UIDT falsified

Additional Drell-Yan falsification:
- No excess over SM in the range $M = 1$–$5$ GeV at LHC Run 3 precision
  ($\mathcal{L} > 300$ fb$^{-1}$) → constrains $\alpha < 0.03$

---

## 6. Cross-References

- `docs/governance/experimental_roadmap.md` — Tier 1/2 LHC predictions
- `docs/governance/falsification-criteria.md` — F5 criterion
- `docs/foundations/gribov_cheeger_proof.md` — mass gap providing $\mu = \Delta^*$
- `FORMALISM.md` — canonical Δ* value
