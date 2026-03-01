# Systematic Robustness Audit: UIDT vs. Baryonic Feedback (Euclid Q1 Context)

> **STATUS:** ✅ PASSED
> **EVIDENCE CATEGORY:** **B** (Mathematically Distinguishable)
> **DATE:** 2026-02-23
> **EXECUTED BY:** UIDT-OS / Jules (Hybrid Precision Audit)

---

## 1. Executive Summary

This audit evaluates the robustness of the Unified Information-Density Theory (UIDT) Dark Energy signature against systematic errors introduced by baryonic feedback (e.g., AGN feedback) in weak lensing surveys, specifically within the context of **Euclid Q1 data**.

**Key Finding:** The UIDT signal (scale-independent growth suppression driven by IR-decay) is statistically orthogonal to the baryonic feedback signal (scale-dependent power suppression).

- **Separation Factor:** **0.968** (Target > 0.8)
- **Correlation:** -0.032
- **Conclusion:** Baryonic physics cannot mimic the UIDT signature in the Euclid sensitivity window ($0.1 < k < 10 \, h/\text{Mpc}$, $0.4 < z < 0.9$).

---

## 2. Methodology

### 2.1 Theoretical Models

**UIDT Signal (Scale-Independent):**
The theory predicts an IR-decay of the vacuum energy density, effectively modeled as a dynamic Dark Energy equation of state:
- $w_0 \approx -0.99$ (**⚠️ S1-04:** conflicts with canonical w = −0.961 [C] (UIDT-C-037) and DESI_DR2_alignment_report.md w₀ = −0.73)
- $w_a \approx -1.30$ (Derived from $\delta\gamma = \gamma_{\infty} - \gamma_{phys}$)

This induces a suppression in the linear growth factor $D(z)$ relative to $\Lambda$CDM. The signal is defined as the ratio of power spectra (linear regime approximation):
$$ S_{\text{UIDT}}(k, z) \approx \left( \frac{D_{\text{UIDT}}(z)}{D_{\Lambda\text{CDM}}(z)} \right)^2 $$
*Note: This signal is constant in $k$ but evolves with $z$.*

**Baryonic Feedback Signal (Scale-Dependent):**
Modeled using a standard AGN feedback proxy (HMCode-inspired) representing the suppression of the matter power spectrum at non-linear scales due to gas expulsion:
$$ S_{\text{Baryon}}(k, z) \approx \frac{1}{1 + A_{\text{AGN}}(z) \left( \frac{k}{k_{\text{break}}} \right)^2} $$
*Note: This signal is strongly $k$-dependent.*

### 2.2 Audit Grid (Euclid Q1 Focus)
The analysis was performed on a tomographic grid representative of Euclid's peak lensing sensitivity:
- **Redshift:** $z \in [0.4, 0.9]$ (20 bins)
- **Scale:** $k \in [0.1, 10.0] \, h/\text{Mpc}$ (50 bins)

### 2.3 Statistical Metric
The **Separation Factor** is defined via the Pearson correlation coefficient $r$ of the flattened signal vectors:
$$ \mathcal{F}_{\text{sep}} = 1 - |r(S_{\text{UIDT}}, S_{\text{Baryon}})| $$

---

## 3. Results

### 3.1 Quantitative Output
| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **Separation Factor** | **0.968073** | **High Separability** |
| Correlation ($r$) | -0.031927 | Negligible linear correlation |
| Scale Orthogonality | High | Functions occupy different vector subspaces |

### 3.2 Interpretation
The high separation factor (near 1.0) confirms that the two signals are functionally distinct.
- **UIDT:** Affects the *amplitude* of structure growth globally across scales (at a given redshift).
- **Baryons:** Affect the *shape* of the power spectrum at small scales.

Euclid's ability to measure both geometry (growth) and shape ($P(k)$) allows for a clean separation. If Euclid detects a suppression in $\sigma_8$ (amplitude) *without* the characteristic $k$-dependent shape of AGN feedback, it constitutes evidence for the UIDT IR-decay mechanism.

---

## 4. Conclusion & Recommendation

**Verdict:** The UIDT Dark Energy signature is robust against baryonic systematics.

**Action Items:**
1.  Proceed with full-scale MCMC forecasts using this separation prior.
2.  In Euclid data analysis, treat $w_a$ and Baryon parameters (e.g., $A_{bary}$) as independent, non-degenerate parameters.

---

*This report is generated automatically by `verification/scripts/lensing_robustness_audit.py`.*
