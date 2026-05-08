# Claims Table — Three-Gluon Vertex / Soft-Gluon Form Factor

## UIDT Evidence System

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-3GV-01 | α_sg = Z1_sg · F₀ · a = 0.115920... — log slope of Γ_sg(s²) | A | arXiv:2102.04959 Eq. (32) | I |
| C-3GV-02 | β_sg = 0.661835... — normalization offset at µ = 4.3 GeV | A | Derived: 1 − α_sg·ln(µ²); arXiv:2208.01020 Eq. (21) | I |
| C-3GV-03 | Γ_sg(µ²) = 1 — MOM renormalization condition | A | arXiv:2208.01020 Eq. (21) | I |
| C-3GV-04 | Planar degeneracy: Γ₁(q²,r²,p²) ≈ Γ_sg(s²) | B | arXiv:2208.01020 Eq. (28) | I/II |
| C-3GV-05 | Gluon mass m = 350 MeV restores planar degeneracy in perturbation theory | B | arXiv:2208.01020 Sec. 6, Fig. 7 | II |
| C-3GV-06 | IR zero-crossing of Γ_sg at s_zero ≈ 0.058 GeV | A | Derived analytically | I |
| C-3GV-07 | s_zero ≠ Δ* — IR zero-crossing of Γ_sg is NOT the spectral gap | A | Distinct observables | I |
| C-3GV-08 | UIDT Δ* = 1.710 GeV — Yang-Mills spectral gap (unchanged) | A | UIDT Ledger | I |
| C-3GV-09 | α2 = c/4 · Z1_sym · F₀ = −0.041650... — log slope of Γ₂ˢʸᵐ(s²) | A | arXiv:2102.04959 Eq. (33) | I |
| C-3GV-10 | Γ₂_sat = −3/4·(α_sym + c/2 + d/3) = −0.005860... — IR saturation value | A | arXiv:2102.04959 Eq. (33) | I |
| C-3GV-11 | Γ₂ˢʸᵐ(µ²) = 0 — transverse renormalization condition | A | Standard MOM, arXiv:2102.04959 Sec. 4 | I |
| C-3GV-12 | Γ₂ˢʸᵐ monotone decreasing from IR toward µ: Γ₂(0.3) > Γ₂(2.0) | A | Derived (c < 0, d < 0 ⇒ alpha2 < 0) | I |
| C-3GV-13 | Γ₂ˢʸᵐ ~ O(0.1) · Γ₁ˢʸᵐ — subdominant; ~10% of leading form factor | B | arXiv:2208.01020 Sec. 5, Fig. 5 | I/II |

## Test Protocol

```bash
cd research/three-gluon-vertex
python etaA_lsg_fit.py
```

**Expected output (9 checks, all residuals = 0.0 < 1e-14):**

```
[PASS]  Gamma_sg(mu) - 1                              residual = 0.0
[PASS]  Gamma1_sym(mu) - 1                            residual = 0.0
[PASS]  Gamma2_sym(mu)                                residual = 0.0
[PASS]  Gamma1_bisect(2.0, 0) - Gamma_sg(2.0)         residual = 0.0
[PASS]  alpha_sg > 0                                  residual = 0.0
[PASS]  Gamma2_sat < 0 (|sat| check)                  residual = 0.0
[PASS]  Gamma2_sym monotone (g2_low > g2_high)        residual = 0.0
[PASS]  Delta_star unchanged                          residual = 0.0
[PASS]  gamma_val unchanged                           residual = 0.0
Total: 9  |  PASS: 9  |  FAIL: 0
```

## DOI / arXiv Resolvability

| Paper | arXiv | DOI | Verified |
|---|---|---|---|
| Aguilar et al. 2021 (PLB 818) | arXiv:2102.04959 | 10.1016/j.physletb.2021.136352 | ✅ |
| Pinto-Gómez et al. 2022 (PLB 838) | arXiv:2208.01020 | 10.1016/j.physletb.2023.137737 | ✅ |

## Parameter Summary

| Parameter | Value (80-digit mpmath) | Evidence | Eq. |
|---|---|---|---|
| `alpha_sg` | 0.115920... | A | Eq. (32) [A] |
| `alpha_sym` | 0.109480... | A | Eq. (32) [A] |
| `alpha2` | −0.041650... | A | Eq. (33) [A] |
| `beta_sg` | 0.661835... | A | Derived, Eq. (21) [B] |
| `Gamma2_sat` | −0.005860... | A | Eq. (33) [A] |
| `m_gluon` | 0.350 GeV | B | Sec. 6 Fig. 7 [B] |
| `alpha_s` | 0.27 | B | Fig. 7 [B] |
| `mu` | 4.3 GeV | A | Tab. 1 [B] |
| `Delta*` | 1.710 GeV | A | UIDT Ledger |

## Known Limitations

- IR log fit assumes massless-ghost dominance; valid for s < 1 GeV.
- `a = 0.046` is SDE-derived; lattice uncertainty not propagated here.
- `Gamma2_sym` contribution (~10% of `Gamma1`) not included in planar degeneracy approximation Eq. (28); see C-3GV-13.
- `s_zero ≈ 0.058 GeV` from pure log extrapolation — actual IR behaviour modified by gluon mass threshold at m_gluon = 350 MeV.
- Active research framework — not established physics.
