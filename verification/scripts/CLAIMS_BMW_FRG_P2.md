# Claims Table — BMW-FRG Phase-2 Simplified Solver

**Component:** `bmw_frg_ode_phase2.py`  
**Evidence category:** D (prediction — ghost sector absent)  
**Status flag:** `[GHOST_SECTOR_MISSING]`  
**Constitution compliance:** mp.dps = 80 LOCAL, no float(), residual < 1e-14

---

## Claims

| ID | Claim | Category | Source |
|----|-------|----------|--------|
| C1 | Litim threshold functions l_0^B, l_1^B are analytically exact for the optimised regulator | A | Litim (2001), PRD 64, 105007 |
| C2 | Flow equations for κ and λ_S in LPA with eta_A=0 are standard O(∂²) truncation | A | Berges, Tetradis, Wetterich (2002), Phys.Rept. 363 |
| C3 | RG constraint 5κ² = 3λ_S is enforced throughout | A | UIDT Ledger §RG FIXED POINT |
| C4 | κ(UV) = 0.500 is a Ledger initial condition | A | UIDT Immutable Parameter Ledger |
| C5 | λ_S(UV) = 5κ²/3 = 5/12 follows from C3 and C4 | A | Algebraic consequence of C3, C4 |
| C6 | c_S^phys = 0 in this solver is an artefact of eta_A = 0 | D | [GHOST_SECTOR_MISSING] flag |
| C7 | IR fixpoint existence in κ–λ_S space suggests non-trivial vacuum structure | D | Flow output — prediction only |
| C8 | Ledger constants Δ* = 1.710 GeV [A], γ = 16.339 [A-] are not modified | A | UIDT Ledger |

---

## Reproduction Note

```bash
pip install mpmath
python verification/scripts/bmw_frg_ode_phase2.py
```

Expected output:
- RG constraint residual < 1e-14 at every sampled step
- `[GHOST_SECTOR_MISSING]` flag printed (correct behaviour)
- c_S^phys = 0 (correct artefact, not a failure)
- Fixpoint detection output if UV coupling drives flow to fixed point

---

## DOI / arXiv Resolvability

| Reference | Identifier | Status |
|-----------|-----------|--------|
| Litim optimised regulator | [hep-th/0103195](https://arxiv.org/abs/hep-th/0103195) | Verifiable |
| Berges–Tetradis–Wetterich FRG review | [hep-ph/0005122](https://arxiv.org/abs/hep-ph/0005122) | Verifiable |
| UIDT Framework v3.9 | [zenodo.org/records/18072470](https://zenodo.org/records/18072470) | Verifiable |

---

## Known Limitations

1. **eta_A = 0** — full anomalous dimension requires Z_c from ghost sector (Phase-1 prerequisite)
2. **Euler integrator** — sufficient for fixpoint detection; replace with RK4 for precision work
3. **c_S^phys = 0** — artefact; not a physical prediction
4. **No Gribov–Zwanziger sector** — fundamental limitation of this truncation
5. **Evidence D only** — all IR outputs are predictions, not established results

---

## Stratum Classification

| Stratum | Content |
|---------|--------|
| I | None (no experimental data used) |
| II | LPA truncation methodology; Litim regulator (established QFT technology) |
| III | UIDT mapping of κ, λ_S to vacuum information density; c_S^phys extraction |
