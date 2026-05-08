# Claims Table -- Quark-Gluon Vertex (Ball-Chiu Decomposition)

## UIDT Evidence System

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-QGV-01 | WTI: (k-p)_mu * Gamma^mu(k,p) = S^{-1}(k) - S^{-1}(p) -- exact | A | Ball, Chiu 1980 DOI:10.1103/PhysRevD.22.2542 | I |
| C-QGV-02 | L_1(k^2,p^2) = [A(k^2)+A(p^2)]/2 -- dominant BC form factor | A | Ball, Chiu 1980 Eq.(3.2) | I |
| C-QGV-03 | L_2(k^2,p^2) = [A(k^2)-A(p^2)]/(k^2-p^2) -- WTI-fixed | A | Ball, Chiu 1980 Eq.(3.2) | I |
| C-QGV-04 | L_3(k^2,p^2) = [B(k^2)-B(p^2)]/(k^2-p^2) -- WTI-fixed | A | Ball, Chiu 1980 Eq.(3.2) | I |
| C-QGV-05 | A(0) = 1 + a_A = 1.30 -- IR quark wavefunction enhancement | B | arXiv:1401.3631 Fig.2 | I/II |
| C-QGV-06 | a_A = 0.30, Lambda_A = 1.0 GeV -- IR dressing parameters | B | arXiv:1401.3631 Fig.2 (fit) | I/II |
| C-QGV-07 | B(0) = m_q*(1+b_B) ~ 0.205 GeV -- constituent quark mass (DCSB) | B | arXiv:2207.06565 Sec.3 | I/II |
| C-QGV-08 | b_B = 40.0, Lambda_B = 0.5 GeV -- DCSB model parameters | D | Phenomenological DCSB model | III |
| C-QGV-09 | L1(k,p) = L1(p,k) symmetric; L2(k,p) = -L2(p,k) anti-symmetric | A | Ball, Chiu 1980, parity | I |
| C-QGV-10 | Delta* = 1.710 GeV != m_q, B(0): Yang-Mills gap distinct from quark mass | A | UIDT Ledger | I |

## Evidence Count

| Category | Count | Description |
|---|---|---|
| A | 4 | Mathematically proven (WTI exact) |
| B | 3 | Lattice / fit compatible |
| D | 3 | Prediction / model-dependent |

## Test Protocol

```bash
cd research/quark_gluon_vertex
python quark_gluon_vertex.py    # 10 checks
```

**Expected: 10 checks, FAIL: 0**

## DOI / arXiv Resolvability

| Paper | arXiv | DOI | Verified |
|---|---|---|---|
| Ball, Chiu 1980 (PRD 22) | -- | 10.1103/PhysRevD.22.2542 | checkmark |
| Curtis, Pennington 1990 (PRD 42) | -- | 10.1103/PhysRevD.42.4165 | checkmark |
| Aguilar, Binosi, Papavassiliou 2014 (PRD 89) | arXiv:1401.3631 | 10.1103/PhysRevD.89.085032 | checkmark |
| Albino et al. 2022 (PRD 106) | arXiv:2207.06565 | 10.1103/PhysRevD.106.034003 | checkmark |

## Parameter Summary

| Parameter | Value | Evidence |
|---|---|---|
| `C_F` | 4/3 | A |
| `a_A` | 0.30 | B |
| `Lambda_A` | 1.0 GeV | B |
| `m_q` | 0.005 GeV | D |
| `b_B` | 40.0 | D |
| `Lambda_B` | 0.5 GeV | D |
| `mu` | 4.3 GeV | A |
| `Delta*` | 1.710 GeV | A |
| `gamma_val` | 16.339 | A- |

## Known Limitations

- Only longitudinal BC components L_1, L_2, L_3 implemented (4 of 12 structures).
- Transverse T_i (i=1..8): not implemented; required for full multiplicative renormalizability.
- A(p^2), B(p^2): model dressing functions; not self-consistently solved via quark SDE.
- b_B, Lambda_B: phenomenological; large uncertainty (Evidence D).
- Quenched: N_f = 0; unquenching shifts L_1 by ~5% at mu.
- Active research framework -- not established physics.
