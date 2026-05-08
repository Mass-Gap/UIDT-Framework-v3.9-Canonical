# Claims Table — Three-Gluon Vertex / Soft-Gluon Form Factor

## UIDT Evidence System

| ID | Claim | Category | Source | Stratum |
|---|---|---|---|---|
| C-3GV-01 | α_sg = Z1_sg · F₀ · a = 0.1159(6) — log slope of Γ_sg(s²) | A | arXiv:2102.04959 Eq. (32) | I |
| C-3GV-02 | β_sg = 0.6618... — normalization offset at µ = 4.3 GeV | A | Derived from Eq. (21), arXiv:2208.01020 | I |
| C-3GV-03 | Γ_sg(µ²) = 1 — MOM renormalization condition | A | arXiv:2208.01020 Eq. (21) | I |
| C-3GV-04 | Planar degeneracy: Γ₁(q²,r²,p²) ≈ Γ_sg(s²) | B | arXiv:2208.01020 Eq. (28) | I/II |
| C-3GV-05 | Gluon mass m = 350 MeV restores planar degeneracy in perturbation theory | B | arXiv:2208.01020 Sec. 6, Fig. 7 | II |
| C-3GV-06 | IR zero-crossing of Γ_sg at s_zero ≈ 0.058 GeV | A | Derived analytically | I |
| C-3GV-07 | s_zero ≠ Δ* — IR zero-crossing of Γ_sg is NOT the spectral gap | A | Distinct observables | I |
| C-3GV-08 | UIDT Δ* = 1.710 GeV — Yang-Mills spectral gap (unchanged) | A | UIDT Ledger | I |

## Reproduction Note

```bash
cd research/three-gluon-vertex
python etaA_lsg_fit.py
# Expected output: [PASS] All residuals < 1e-14
```

## DOI / arXiv Resolvability

| Paper | arXiv | DOI | Verified |
|---|---|---|---|
| Aguilar et al. 2021 (PLB 818) | arXiv:2102.04959 | 10.1016/j.physletb.2021.136352 | ✅ |
| Pinto-Gómez et al. 2022 | arXiv:2208.01020 | pending (PLB in press Aug 2022) | ✅ arXiv |

## Known Limitations

- IR log fit assumes massless-ghost dominance; valid for s < 1 GeV.
- a = 0.046 is SDE-derived; lattice uncertainty not propagated here.
- Γ₂^sym contribution (~ 10% of Γ₁) not included in Eq. (28) approximation.
- This is active research — not established physics.
