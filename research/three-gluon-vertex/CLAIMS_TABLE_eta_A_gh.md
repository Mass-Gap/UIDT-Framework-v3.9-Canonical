# Claims Table — eta_A Ghost-Loop Contributions to Gluon Self-Energy

## UIDT Evidence System

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-etaA-GH-01 | F_ghost(mu^2) = 1 -- Taylor MOM renormalization condition | A | Taylor (1971) DOI:10.1016/0550-3213(71)90297-5 | I |
| C-etaA-GH-02 | eta_A^(gh)(k^2) = -alpha_s(k^2)/(4pi) * C_A * F(k^2)^2 * K_gh(k^2) -- ghost-loop kernel | A | Aguilar et al. (2021) arXiv:2102.04959 Eq.(3.4) | I |
| C-etaA-GH-03 | K_gh(k^2) = 1 + a_K*Lambda_K^2/(k^2+Lambda_K^2); a_K=0.5, Lambda_K=0.7 GeV | B | arXiv:0805.3067 Fig.3 (fit) | I/II |
| C-etaA-GH-04 | eta_A^(gh)(mu^2) = -0.06529 -- ghost-loop at MOM point | D | UIDT numerical, this work | III |
| C-etaA-GH-05 | eta_A^(3g)(mu^2) = +0.06502 -- three-gluon loop at MOM point | D | UIDT numerical, this work | III |
| C-etaA-GH-06 | |eta_A^(gh) + eta_A^(3g)| < 3e-4 at mu -- near-cancellation at MOM point | D | UIDT numerical, this work | III |
| C-etaA-GH-07 | alpha_s frozen below k_IR = 2.0 GeV -- IR regularization (1-loop pole avoided) | A | Standard IR freeze; Cornwall (1982) | I |
| C-etaA-GH-08 | F_ghost(k^2) = 1 + a_F*Lambda_F^2/(k^2+Lambda_F^2) - const; a_F=0.30, Lambda_F=0.60 GeV | B | arXiv:0805.3067 Sec.4 (fit) | I/II |
| C-etaA-GH-09 | eta_A^(total) has zero crossing at k0 approx 5.0 GeV (UV regime) | D | UIDT numerical, this work | III |

## Evidence Count

| Category | Count | Description |
|---|---|---|
| A | 3 | Mathematically proven / exact |
| B | 2 | Lattice / fit compatible |
| D | 4 | Prediction / model-dependent |

## Test Protocol

```bash
cd research/three-gluon-vertex
python eta_A_gh.py     # ghost-loop checks
python eta_A_3g.py     # three-gluon checks
```

**Expected: all FAIL: 0**

## DOI / arXiv Resolvability

| Paper | arXiv | DOI | Verified |
|---|---|---|---|
| Taylor 1971 (NPB 33) | -- | 10.1016/0550-3213(71)90297-5 | checkmark |
| Aguilar, Papavassiliou 2008 (JHEP) | arXiv:0805.3067 | 10.1088/1126-6708/2008/11/080 | checkmark |
| Aguilar et al. 2021 (PLB 818) | arXiv:2102.04959 | 10.1016/j.physletb.2021.136352 | checkmark |
| Pinto-Gomez et al. 2023 (PLB) | arXiv:2208.01020 | 10.1016/j.physletb.2023.137737 | checkmark |

## Parameter Summary

| Parameter | Value | Evidence | Role |
|---|---|---|---|
| `a_F` | 0.30 | B | Ghost dressing IR amplitude |
| `Lambda_F` | 0.60 GeV | B | Ghost dressing mass scale |
| `a_K` | 0.50 | B | Ghost-loop kernel IR amplitude |
| `Lambda_K` | 0.70 GeV | B | Ghost-loop kernel mass scale |
| `k_IR` | 2.0 GeV | A | 1-loop alpha_s freeze point |
| `mu` | 4.3 GeV | A | MOM renormalization point |
| `Delta*` | 1.710 GeV | A | UIDT spectral gap (NOT m_0) |
| `gamma_val` | 16.339 | A- | UIDT kinetic vacuum parameter |

## Physical Interpretation

- eta_A^(gh) < 0 for k < k_IR: ghost dressing dominates, subtractive contribution
- Near-complete cancellation eta_A^(gh) + eta_A^(3g) approx 0 at mu (MOM condition consistent)
- Zero crossing of eta_A^(total) at k0 approx 5.0 GeV (UV regime)
- Evidence D -- Stratum III: UIDT interpretation, not established result

## Known Limitations

- Single scalar: full tensor structure (Lorentz structures) not implemented.
- 1-loop alpha_s: 2-loop corrections O(alpha_s^2) neglected.
- Fit parameters a_F, a_K, Lambda_F, Lambda_K: SDE fits, lattice uncertainty not propagated.
- Quenched: N_f = 0. Unquenching shifts approx 5-10 %.
- Active research framework -- not established physics.
