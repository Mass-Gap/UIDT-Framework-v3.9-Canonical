---
name: "🔬 Falsification Report"
about: "Report experimental data that falsifies an UIDT prediction"
title: "Falsification: [Test Name]"
labels: ["falsification", "needs-review"]
---

## UIDT Falsification Report

Thank you for reporting experimental results relevant to UIDT predictions. Please complete this form with scientific rigor.

---

## Which UIDT Test is Affected?

- [ ] **F1: Lattice QCD Continuum Limit** (Δ = 1.710 ± 0.015 GeV)
- [ ] **F2: Torsion Binding Energy** (E_T ≈ 2.44 MeV)
- [ ] **F3: DESI Dark Energy** (w(z) ≠ -1)
- [ ] **F4: Photonic Isomorphism** (n_critical ≈ 16.339)
- [ ] **F5: LHC Scalar Resonance** (m_S = 1.705 ± 0.015 GeV)
- [ ] **F6: Proton Anchor Ratio** (m_p/f_vac ≈ 8.75)
- [ ] **F7: Casimir Force Anomaly** (+0.59% at 0.66 nm)
- [ ] **F8: Hubble Tension** (H₀ = 70.4 ± 0.16 km/s/Mpc)
- [ ] **Other** (please describe)

---

## Experimental Result

**Prediction from UIDT:**
```
[State the UIDT prediction with uncertainty]
```

**Your measured/observed value:**
```
[Your measurement with full uncertainty analysis]
```

**Confidence level / Significance:**
- [ ] 1σ (68% confidence)
- [ ] 2σ (95% confidence)
- [ ] 3σ (99.7% confidence — theory-threatening)
- [ ] 5σ+ (>99.99999% — falsification threshold)

**z-score or p-value:**
```
z = (your_value - UIDT_prediction) / sqrt(σ²_your + σ²_UIDT)

z = ___________
p-value = ___________
```

---

## Experiment Details

**Experiment/Dataset Name:**
```
[e.g., "LHCb Run 3 Scalar Search", "DESI Year 5 w(z) measurements", etc.]
```

**Reference:**
- ArXiv / DOI: [link]
- Publication status: [ ] Published [ ] Preprint [ ] Internal

**Experimental method summary:**
```
[Brief description of how measurement was obtained]
```

**Systematic uncertainties:**
- Primary: ___________
- Secondary: ___________

---

## Falsification Assessment

**Does this falsify the UIDT prediction?**

| Criterion | Status |
|---|---|
| Discrepancy > 3σ? | [ ] Yes [ ] No |
| Systematic uncertainties controlled? | [ ] Yes [ ] No [ ] Unclear |
| Reproducible by other experiments? | [ ] Yes [ ] No [ ] Unknown |
| Confounds excluded? | [ ] Yes [ ] No [ ] Unclear |

**Overall assessment:**
- [ ] **FALSIFIES** — UIDT prediction excluded at > 3σ
- [ ] **CONSTRAINS** — UIDT parameter space narrowed
- [ ] **SUPPORTS** — Consistent with UIDT
- [ ] **UNCLEAR** — Needs further analysis

---

## Impact on UIDT

**If this is Category A (mathematically proven):**
- [ ] Invalidates core Constants Δ, γ, κ, or λ_S
- [ ] Invalidates RG fixed-point assumption
- [ ] Invalidates Pillar I (QFT closure)
- [ ] Other: __________

**If Category C (calibrated to data):**
- [ ] Invalidates cosmology calibration only
- [ ] Does NOT affect QFT core

---

## Additional Evidence

**Attach:**
- [ ] Data files (CSV, HDF5, ROOT)
- [ ] Analysis scripts
- [ ] Systematic breakdown
- [ ] Cross-validation with other experiments

---

## Contact

**Your name / Institution:**

**Email for follow-up:**

**Expected response timeframe:** (UIDT team aims to respond within 2 weeks)

---

## Reporting Protocol

This falsification report will be:
1. ✅ Reviewed by UIDT PI
2. ✅ Cross-checked against UIDT predictions and uncertainties
3. ✅ Impact assessed on theory status
4. ✅ Response posted in this issue within 14 days
5. ✅ If valid falsification: added to UIDT Evidence Dashboard

**For questions:** Contact badbugs.arts@gmail.com with subject "UIDT Falsification Report"

---

*DOI: 10.5281/zenodo.17835200*
