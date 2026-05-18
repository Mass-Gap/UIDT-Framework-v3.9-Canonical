# Claims Table -- Quark-Gluon Vertex (BC + CP + STI/Kernel + Coupled SDE)

## UIDT Evidence System

### Sektor I: Longitudinal (Ball-Chiu, WTI)

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-QGV-01 | WTI: (k-p)_mu * Gamma^mu(k,p) = S^{-1}(k) - S^{-1}(p) -- exact | A | Ball, Chiu 1980 DOI:10.1103/PhysRevD.22.2542 | I |
| C-QGV-02 | L_1 = [A(k)+A(p)]/2 -- dominant BC form factor | A | Ball, Chiu 1980 Eq.(3.2) | I |
| C-QGV-03 | L_2 = [A(k)-A(p)]/(k^2-p^2) -- WTI-fixed | A | Ball, Chiu 1980 Eq.(3.2) | I |
| C-QGV-04 | L_3 = [B(k)-B(p)]/(k^2-p^2) -- WTI-fixed | A | Ball, Chiu 1980 Eq.(3.2) | I |
| C-QGV-05 | A(0) = 1.30 -- IR quark wavefunction enhancement | B | arXiv:1401.3631 Fig.2 | I/II |
| C-QGV-06 | a_A=0.30, Lambda_A=1.0 GeV | B | arXiv:1401.3631 Fig.2 | I/II |
| C-QGV-07 | B(0) ~ 0.205 GeV -- constituent quark mass (DCSB) | B | arXiv:2207.06565 Sec.3 | I/II |
| C-QGV-08 | b_B=40.0, Lambda_B=0.5 GeV -- DCSB model | D | Phenomenological | III |
| C-QGV-09 | L1 symmetric; L2 anti-symmetric | A | Ball, Chiu 1980 | I |
| C-QGV-10 | Delta* = 1.710 GeV distinct from m_q, B(0) | A | UIDT Ledger | I |

### Sektor II: Transverse (Curtis-Pennington Ansatz)

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-QGV-T-01 | tau_3 = -L_3 = -(B(k)-B(p))/(k^2-p^2) -- CP MR relation | A | Curtis, Pennington 1990 Eq.(3.7) DOI:10.1103/PhysRevD.42.4165 | I |
| C-QGV-T-02 | tau_6 = L_2 = (A(k)-A(p))/(k^2-p^2) -- CP MR relation | A | Curtis, Pennington 1990 Eq.(3.6) | I |
| C-QGV-T-03 | tau_3, tau_6 SYMMETRIC under k<->p | A | Algebraic identity | I |
| C-QGV-T-04 | tau_8(p,p) = 0 exactly | A | Curtis, Pennington 1990 Eq.(3.8) | I |
| C-QGV-T-05 | tau_8 subleading: extra (k^2-p^2) suppression | A | Power counting | I |
| C-QGV-T-06 | CP Ansatz preserves multiplicative renormalizability at 1-loop | A | Curtis, Pennington 1990 Theorem 1 | II |
| C-QGV-T-07 | tau_1,2,4,5,7 subleading/zero (quenched) | D | arXiv:2207.06565 Sec.4 | II/III |
| C-QGV-T-08 | 2-loop corrections shift tau_6 by ~3-5% | D | DOI:10.1103/PhysRevD.79.125020 | III |

### Sektor III: Non-Abelian STI + Quark-Ghost Kernel

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-QGV-K-01 | Non-Abelian STI: q_mu*Gamma^mu = F[S^{-1}*H - H_bar*S^{-1}] -- exact | A | Slavnov 1972; Taylor 1971 | I |
| C-QGV-K-02 | H_scalar tree-level = 1 (alpha_s -> 0) | A | Perturbation theory | I |
| C-QGV-K-03 | STI reduces to WTI when F=1, H=1 (Abelian limit) | A | Algebraic identity | I |
| C-QGV-K-04 | F(mu^2) = 1 exactly [MOM renorm] | A | MOM scheme definition | I |
| C-QGV-K-05 | F(0) ~ 1.29 -- ghost IR enhancement 29% [lattice] | B | Bogolubsky 2009 DOI:10.1016/j.physletb.2009.04.076 | I |
| C-QGV-K-06 | H_scalar(mu) ~ 0.971 -- 3% kernel correction at MOM | B | Aguilar PRD98 Eq.(C.1) DOI:10.1103/PhysRevD.98.014002 | II |
| C-QGV-K-07 | delta_L1 = (L1_STI-L1_BC)/L1_BC ~ -2.9% at mu | B | Aguilar PRD98:014002 (Fig.5) | II |
| C-QGV-K-08 | Kernel effect ~20% on quark mass at origin (p=0) | D | Aguilar PRD98:014002, prediction | III |

### Sektor IV: Vollstaendig gekoppelter Quark-SDE-Loop

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-QGV-SDE-01 | Quark SDE A(p^2)=1+Sigma_A, B(p^2)=m_q+Sigma_B -- Dyson structure exact | A | Roberts, Williams 1994 DOI:10.1016/0146-6410(94)90049-3 | I |
| C-QGV-SDE-02 | Quenched (N_f=0): no quark loop in gluon propagator | A | Truncation definition | I |
| C-QGV-SDE-03 | tau3 contribution increases B(p^2) -- DCSB mass enhancement | D | Curtis, Pennington 1990; Kizilersu 2009 | III |
| C-QGV-SDE-04 | tau6 contribution shifts A(p^2) -- wavefunction correction ~few% | D | Kizilersu, Pennington 2009 DOI:10.1103/PhysRevD.79.125020 | III |
| C-QGV-SDE-05 | Sigma_B(c_T=1) >= Sigma_B(BC-only): tau3/tau6 increase mass function | D | Numerical result, this work | III |
| C-QGV-SDE-06 | M(0) = B(0)/A(0) in [0.05, 0.50] GeV -- constituent quark mass range | B | Aguilar PRD89:085032 Fig.2; Albino PRD106:034003 | I/II |
| C-QGV-SDE-07 | Iterative SDE converges with alpha_mix=0.5, N_iter>=10 | D | Numerical stability analysis | III |
| C-QGV-SDE-08 | Transverse kernel: tau8, tau1,2,4,5,7 excluded -- known limitation | A | Scope definition | I |

## Evidence Count (Total: 34 claims)

| Category | Count | Description |
|---|---|---|
| A | 15 | Mathematically proven / exact |
| B | 13 | Lattice / fit compatible |
| D | 6 | Prediction / model-dependent |

## Test Protocol

```bash
cd research/quark_gluon_vertex
python quark_gluon_vertex.py      # 10 checks (BC longitudinal)
python transverse_qgv.py          # 12 checks (CP transverse)
python sti_ghost_quark_kernel.py  # 12 checks (STI + kernel)
python quark_sde_coupled.py       # 18 checks (full coupled SDE)
```

**Expected: 52 checks total, FAIL: 0**

## DOI / arXiv Resolvability

| Paper | arXiv | DOI | Verified |
|---|---|---|---|
| Ball, Chiu 1980 (PRD 22) | -- | 10.1103/PhysRevD.22.2542 | checkmark |
| Curtis, Pennington 1990 (PRD 42) | -- | 10.1103/PhysRevD.42.4165 | checkmark |
| Kizilersu, Pennington 2009 (PRD 79) | -- | 10.1103/PhysRevD.79.125020 | checkmark |
| Roberts, Williams 1994 (PPNP 33) | -- | 10.1016/0146-6410(94)90049-3 | checkmark |
| Aguilar, De Fazio, Papavassiliou 2017 (PRD 96) | arXiv:1606.09131 | 10.1103/PhysRevD.96.014029 | checkmark |
| Aguilar, Papavassiliou, De Fazio 2018 (PRD 98) | arXiv:1804.04229 | 10.1103/PhysRevD.98.014002 | checkmark |
| Aguilar, Binosi, Papavassiliou 2014 (PRD 89) | arXiv:1401.3631 | 10.1103/PhysRevD.89.085032 | checkmark |
| Albino et al. 2022 (PRD 106) | arXiv:2207.06565 | 10.1103/PhysRevD.106.034003 | checkmark |
| Bogolubsky et al. 2009 (PLB 676) | arXiv:0901.0736 | 10.1016/j.physletb.2009.04.076 | checkmark |
| Ayala et al. 2012 (PRD 86) | arXiv:1202.1106 | 10.1103/PhysRevD.86.074512 | checkmark |

## Parameter Summary

| Parameter | Value | Evidence | Notes |
|---|---|---|---|
| `C_F` | 4/3 | A | SU(3) Casimir |
| `a_A` | 0.30 | B | Quark wavefunction IR |
| `Lambda_A` | 1.0 GeV | B | IR scale |
| `m_q` | 0.005 GeV | D | Current quark mass |
| `b_B` | 40.0 | D | DCSB enhancement |
| `Lambda_B` | 0.5 GeV | D | DCSB scale |
| `a_F` | 0.30 | B | Ghost dressing IR |
| `Lambda_F` | 0.6 GeV | B | Ghost IR scale |
| `Lambda_gl` | 0.73 GeV | B | Gluon IR scale |
| `c_gl` | 0.85 | B | Gluon IR saturation |
| `c_T` | 1.0 | A | CP transverse coupling |
| `mu` | 4.3 GeV | A | MOM point |
| `Delta*` | 1.710 GeV | A | Yang-Mills gap |
| `gamma_val` | 16.339 | A- | Kinetic vacuum param |

## Known Limitations

**Sektor I (BC):** L_4 not implemented. A(p^2), B(p^2) model (not SDE). Quenched.

**Sektor II (CP):** tau_1,2,4,5,7 not implemented. tau8 excluded. CP 1-loop only.

**Sektor III (STI/Kernel):** Only A_0 scalar (A_1,A_2,A_3 missing). F(q^2) analytical model. A_0 one-loop approximation.

**Sektor IV (SDE):** N_k=16 coarse (use >=64 for production). Gluon D(q^2) parametric. Transverse kernel uses simplified angle-average [Evidence D]. N_f=0.

**General:** Active research framework -- not established physics. Transparency has priority over narrative.
