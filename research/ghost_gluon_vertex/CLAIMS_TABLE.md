# Claims Table -- Ghost-Gluon Vertex H(k,q)

## UIDT Evidence System

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-GGV-01 | Z_1^F = 1 exactly in Landau gauge (Taylor theorem) | A | Taylor (1971) DOI:10.1016/0550-3213(71)90297-5 | I |
| C-GGV-02 | H(0, mu^2) = 1 -- Taylor renormalization condition | A | arXiv:0805.3067 Sec.3 | I |
| C-GGV-03 | delta_H = 9*C_A / (44*C_A - 8*N_f) = 9/44 (quenched) -- UV anomalous dimension | A | arXiv:2102.04959 Eq.(A.3), 1-loop | I |
| C-GGV-04 | H_IR(k^2) = 1 + a_H*k^2/(k^2+m_H^2); H_IR(0)=1, H_IR(inf)=1+a_H | A | arXiv:0805.3067 Eq.(4.3) | I |
| C-GGV-05 | H_UV(s^2) = [alpha_s(s^2)/alpha_s(mu^2)]^{9/44}; monotone decreasing for s > mu | A | 1-loop RG, arXiv:2102.04959 App.A | I |
| C-GGV-06 | a_H = 0.20 -- IR enhancement amplitude | B | arXiv:0805.3067 Fig.3 (fit) | I/II |
| C-GGV-07 | m_H = 0.50 GeV -- IR mass scale of ghost-gluon vertex | B | arXiv:0805.3067 Fig.3 (fit) | I/II |
| C-GGV-08 | H(k,q) >= 1 for k,q in [0, mu]: IR enhancement of ghost-gluon coupling | D | Numerical SDE, arXiv:0805.3067 Sec.4 | III |

## Evidence Count

| Category | Count | Description |
|---|---|---|
| A | 5 | Mathematically proven |
| B | 2 | Lattice / fit compatible |
| D | 1 | Prediction / model-dependent |

## Test Protocol

```bash
cd research/ghost_gluon_vertex
python ghost_gluon_vertex.py    # 10 checks
```

**Expected: 10 checks, FAIL: 0**

## DOI / arXiv Resolvability

| Paper | arXiv | DOI | Verified |
|---|---|---|---|
| Taylor 1971 (NPB 33) | -- | 10.1016/0550-3213(71)90297-5 | checkmark |
| Aguilar, Papavassiliou 2008 (JHEP) | arXiv:0805.3067 | 10.1088/1126-6708/2008/11/080 | checkmark |
| Aguilar et al. 2021 (PLB 818) | arXiv:2102.04959 | 10.1016/j.physletb.2021.136352 | checkmark |

## Parameter Summary

| Parameter | Value | Evidence |
|---|---|---|
| `delta_H` | 9/44 = 0.20454... | A |
| `a_H` | 0.20 | B |
| `m_H` | 0.50 GeV | B |
| `mu` | 4.3 GeV | A |
| `Delta*` | 1.710 GeV | A |
| `gamma_val` | 16.339 | A- |

## Known Limitations

- H_IR: single scalar; full tensorial structure (3 Lorentz structures) not implemented.
- UV running: 1-loop only; 2-loop corrections O(alpha_s^2) neglected.
- a_H, m_H: fit values from SDE; lattice uncertainty not propagated.
- Quenched approximation: N_f = 0.
- Active research framework -- not established physics.
