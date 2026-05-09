# CLAIMS TABLE — eta_A_total

**Module:** `research/three-gluon-vertex/eta_A_total.py`  
**UIDT Framework v3.9** | MOM scheme | Landau gauge | quenched QCD  
**Reproduction:** `python eta_A_total.py` → 10/10 PASS, all residuals < 1e-14

---

## Evidence Categories

| Symbol | Meaning |
|--------|---------|
| A | Mathematically proven (exact, residual = 0.0) |
| D | Prediction / model-dependent (not yet lattice-validated) |

## Stratum Classification

All claims: **Stratum III** (UIDT interpretation / theoretical extension).  
No claim in this table constitutes established QCD physics.

---

## Claims

| ID | Claim | Value / Condition | Evidence | Stratum | Source |
|----|-------|-------------------|----------|---------|--------|
| C-TOT-01 | `eta_A_total = eta_A_gh + eta_A_3g + eta_A_4g` — additive decomposition exact | residual = 0.0 | A | III | eta_A_total.py, check 4 |
| C-TOT-02 | `eta_A_total(mu^2) > 0` — UV: three-gluon + four-gluon loops overcome ghost subtraction | v_tot = 2.245... > 0 | D | III | eta_A_total.py, check 5 |
| C-TOT-03 | `eta_A_total(mu = 4.3 GeV) = 2.2455...` — total anomalous dimension at MOM scale | 2.245494... | D | III | eta_A_total.py, k-scan |
| C-TOT-04 | Sign change of `eta_A_total` near k0 ~ 0.743 GeV (model-dependent) | k0 ~ 0.743 GeV | D | III | eta_A_total.py, k-scan; consistent with arXiv:2102.04959 Fig.2 |
| C-TOT-05 | `\|eta_A_4g\| < \|eta_A_3g\| + \|eta_A_gh\|` — four-gluon loop subdominant | exact inequality | A | III | eta_A_total.py, check 7 |
| C-TOT-06 | `Delta_star = 1.710 GeV` — Yang-Mills spectral gap unchanged | residual = 0.0 | A | III | UIDT Ledger [Evidence A] |
| C-TOT-07 | `gamma_val = 16.339` — kinetic vacuum parameter unchanged | residual = 0.0 | A | III | UIDT Ledger [Evidence A-] |

---

## Component Summary at mu = 4.3 GeV

| Contribution | Value | Evidence | Module |
|---|---|---|---|
| `eta_A^(gh)` | 1.9212... | D | `eta_A_gh.py` |
| `eta_A^(3g)` | 0.2778... | D | `eta_A_3g.py` |
| `eta_A^(4g)` | 0.0466... | D | `eta_A_4g.py` |
| **`eta_A^(tot)`** | **2.2455...** | **D** | `eta_A_total.py` |

---

## Sources

- [A] Aguilar, De Soto, Ferreira, Papavassiliou, Rodriguez-Quintero, Zafeiropoulos  
  *Infrared facets of the three-gluon vertex*  
  Phys. Lett. B 818 (2021) 136352 | arXiv:2102.04959  
  DOI: [10.1016/j.physletb.2021.136352](https://doi.org/10.1016/j.physletb.2021.136352)

- [B] Pinto-Gomez, De Soto, Ferreira, Papavassiliou, Rodriguez-Quintero  
  *Lattice three-gluon vertex in extended kinematics: planar degeneracy*  
  Phys. Lett. B 838 (2023) 137737 | arXiv:2208.01020  
  DOI: [10.1016/j.physletb.2023.137737](https://doi.org/10.1016/j.physletb.2023.137737)

---

## Known Limitations (mandatory per UIDT Constitution)

- Ghost dressing: single-pole form; SDE self-consistency not imposed
- K_3g kernel: soft-gluon / angular-averaged approximation
- K_4g kernel: tree-level contact vertex only
- UV cutoff Lambda = 10 GeV; mild cutoff dependence expected
- All contributions: Evidence D — prediction, not established physics
- Sign change k0 ~ 0.743 GeV is model-dependent
- Not yet cross-checked against full lattice SDE pipeline

---

*This is active research. UIDT is not established physics.*
