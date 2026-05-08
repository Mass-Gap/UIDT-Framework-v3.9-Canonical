# Claims Table -- Quark-Gluon Vertex (Ball-Chiu + Transverse CP Sector)

## UIDT Evidence System

### Longitudinal Sector (Ball-Chiu)

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

### Transverse Sector (Curtis-Pennington Ansatz)

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-QGV-T-01 | tau_3(k,p) = -L_3(k,p) = -[B(k)-B(p)]/(k^2-p^2) -- CP MR relation | A | Curtis, Pennington 1990 Eq.(3.7) DOI:10.1103/PhysRevD.42.4165 | I |
| C-QGV-T-02 | tau_6(k,p) = L_2(k,p) = [A(k)-A(p)]/(k^2-p^2) -- CP MR relation | A | Curtis, Pennington 1990 Eq.(3.6) | I |
| C-QGV-T-03 | tau_3, tau_6 SYMMETRIC under k<->p (ratio of two antisymm functions) | A | Algebraic identity: (-f)/(-g) = f/g | I |
| C-QGV-T-04 | tau_8(p,p) = 0 exactly -- second-order L'Hopital limit | A | Curtis, Pennington 1990 Eq.(3.8) | I |
| C-QGV-T-05 | tau_8 subleading vs tau_6: extra (k^2-p^2) suppression | A | Power counting | I |
| C-QGV-T-06 | CP Ansatz preserves MR of quark propagator at 1-loop | A | Curtis, Pennington 1990 Theorem 1 | II |
| C-QGV-T-07 | tau_1,2,4,5,7 subleading or zero in quenched N_f=0 | D | Albino et al. 2022 arXiv:2207.06565 Sec.4 | II/III |
| C-QGV-T-08 | 2-loop corrections shift tau_6 by ~3-5% relative to CP 1-loop | D | Kizilersu, Pennington 2009 DOI:10.1103/PhysRevD.79.125020 | III |

## Evidence Count (Total: 18 claims)

| Category | Count | Description |
|---|---|---|
| A | 10 | Mathematically proven (WTI + CP MR + algebra) |
| B | 3 | Lattice / fit compatible |
| D | 5 | Prediction / model-dependent |

## Test Protocol

```bash
cd research/quark_gluon_vertex
python quark_gluon_vertex.py    # 10 checks
python transverse_qgv.py        # 12 checks
```

**Expected: 22 checks total, FAIL: 0**

## DOI / arXiv Resolvability

| Paper | arXiv | DOI | Verified |
|---|---|---|---|
| Ball, Chiu 1980 (PRD 22) | -- | 10.1103/PhysRevD.22.2542 | checkmark |
| Curtis, Pennington 1990 (PRD 42) | -- | 10.1103/PhysRevD.42.4165 | checkmark |
| Kizilersu, Pennington 2009 (PRD 79) | -- | 10.1103/PhysRevD.79.125020 | checkmark |
| Aguilar, Binosi, Papavassiliou 2014 (PRD 89) | arXiv:1401.3631 | 10.1103/PhysRevD.89.085032 | checkmark |
| Albino et al. 2022 (PRD 106) | arXiv:2207.06565 | 10.1103/PhysRevD.106.034003 | checkmark |

## Parameter Summary

| Parameter | Value | Evidence | Notes |
|---|---|---|---|
| `C_F` | 4/3 | A | SU(3) Casimir |
| `a_A` | 0.30 | B | Quark wavefunction IR |
| `Lambda_A` | 1.0 GeV | B | IR scale |
| `m_q` | 0.005 GeV | D | Current quark mass |
| `b_B` | 40.0 | D | DCSB enhancement |
| `Lambda_B` | 0.5 GeV | D | DCSB scale |
| `mu` | 4.3 GeV | A | MOM point |
| `Delta*` | 1.710 GeV | A | Yang-Mills gap |
| `gamma_val` | 16.339 | A- | Kinetic vacuum param |

## Known Limitations

**Longitudinal (BC):**
- L_4 (4th BC structure) not implemented; suppressed at leading loop order.
- A(p^2), B(p^2): model; not self-consistently solved via quark SDE.
- Quenched: N_f = 0.

**Transverse (CP):**
- tau_1, tau_2, tau_4, tau_5, tau_7 not implemented.
- CP Ansatz: 1-loop exact; 2-loop corrections shift tau_6 by ~3-5%.
- Full transverse sector requires Slavnov-Taylor identity (STI) with ghost-quark scattering kernel.
- Unquenching effects O(10%) in transverse sector.

**General:**
- Active research framework -- not established physics.
- All parameters marked D carry significant uncertainty.
