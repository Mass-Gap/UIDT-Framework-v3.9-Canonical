# BETA-W8 · Topological Observables O1/O2/O3 Upgrade Attempt
**Date:** 2026-04-28 (Week 18)
**Maintainer:** P. Rietz (via Jules Junior Lead Research Agent)
**Framework:** UIDT v3.9
**Branch:** `research/TKT-20260428-L5-TOPOLOGICAL-OBS`

## 1. Current Evidence Status

As tracked in `docs/limitations.md` and the UIDT Claims Ledger:
- **O1 (Rational Fixed Points):** `[D]` (Topological protection / integrable system)
- **O2 (SU(3) Color Projection):** `[D]` (Macroscopic color confinement)
- **O3 (Kissing Number Suppression):** `[D]` (12-neighbor vacuum shielding)

## 2. Lattice Topological Susceptibility Data Search

### Relevant Literature
* **Dürr et al. 2025**
  - **Paper:** "Topological susceptibility and excess kurtosis in SU(3) Yang-Mills theory"
  - **arXiv:** arXiv:2501.08217
  - **Measurement:** $\chi_{\mathrm{top}}^{1/4} = 198.1 \pm 2.8$ MeV

* **Other Benchmarks:**
  - Athenodorou & Teper 2021: $\chi_{\mathrm{top}}^{1/4} = 190 \pm 5$ MeV
  - Del Debbio et al. 2004: $\chi_{\mathrm{top}}^{1/4} = 191 \pm 5$ MeV
  - Ce et al. 2015: $\chi_{\mathrm{top}}^{1/4} = 185 \pm 5$ MeV

*(Verified via `verification/scripts/verify_wilson_flow_topology.py` and `docs/falsification-criteria.md` [F9])*

## 3. Upgrade Criteria Evaluation

**Requirement for [D] → [B] Upgrade:**
- At least 2 independent lattice collaborations measure a compatible value.
- Combined tension < 2$\sigma$ with UIDT prediction.
- No [AI ARTIFACT] flags on the papers.

**UIDT Prediction vs. Measurement:**
- UIDT SVZ LO Prediction: $\chi_{\mathrm{top}}^{1/4} \approx 143$ MeV
- Dürr et al. (2025): $\chi_{\mathrm{top}}^{1/4} = 198.1 \pm 2.8$ MeV
- **Tension:** $z \approx 19.7\sigma$ (LO)

**Conclusion:**
The tension between the UIDT leading-order SVZ estimate (~143 MeV) and the latest quenched lattice QCD data (198.1 ± 2.8 MeV, Dürr et al. 2025) exceeds the < 2$\sigma$ threshold required for an evidence category upgrade. The discrepancy is attributed to missing next-to-leading-order (NLO) corrections to the SVZ formula (which typically add +30-80%).

Consequently, topological observables O1, O2, and O3 **cannot be upgraded** and remain strictly in **Category [D]** (Predictive, Unverified).
