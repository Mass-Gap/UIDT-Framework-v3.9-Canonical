# BETA-W7: Glueball Spectrum vs LHC Run 3 / LHCb Update

## Stratum I: Empirical Measurements
Recent data point to scalar glueball candidates:
- **X(2370):** $m_{\text{exp}} = 2.370$ GeV
- **f₀(2100):** $m_{\text{exp}} = 2.100$ GeV
*(Source: [SEARCH_FAIL] Cannot verify source.)*

## Stratum II: Scientific Consensus
Lattice QCD predictions for the lightest scalar glueball mass:
- **$m_{G, \text{lattice}}$:** $\approx 2.56$ GeV
There is ongoing debate whether X(2370) or f₀(2100) are pure glueballs, or if they represent mixed states.
*(Source: [SEARCH_FAIL] Cannot verify source.)*

## Stratum III: UIDT Interpretation
The UIDT framework predicts a hypothetical glueball mass of $m_G \sim 2\Delta^*$:
- **$\Delta^*$:** $1.710 \pm 0.015$ GeV (Yang-Mills spectral gap [A])
- **$m_{G, \text{UIDT}}$:** $3.420$ GeV [D]

Using high-precision `mpmath` calculations (`mp.dps = 80`), we compare the UIDT predicted glueball mass with experimental candidates:
- **X(2370):** $|m_{\text{UIDT}} - m_{\text{exp}}| = 1.05 \text{ GeV}$
- **f₀(2100):** $|m_{\text{UIDT}} - m_{\text{exp}}| = 1.32 \text{ GeV}$

### Conclusion
The UIDT prediction for the $2\Delta^*$ state ($m_G \sim 3.420$ GeV [D]) is compatible with a higher-mass state, but indicates a large tension with the lower-mass experimental candidates X(2370) and f₀(2100). The current empirical measurements suggests that if these are indeed glueballs, they do not correspond to the simple $2\Delta^*$ prediction of the UIDT framework.
