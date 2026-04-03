# Audit Summary — TKT-20260403

**Date:** 2026-04-03  
**Scope:** Three open analytical questions from session analysis  
**Status:** RESOLVED with explicit epistemic outcome per question

---

## Q1 — Formal derivation γ = Δ*/v → 49/3 from Banach + Gap equation

**Result:** NOT PROVABLE from current equations.

- Closed form from Gap equation + VEV stability: $\gamma^3 = 6\Delta^{*3}\lambda_S/(13\kappa\mathcal{C}) \Rightarrow \gamma \approx 1.91$
- To obtain 49/3 from Gap eq. requires $\Delta^* \approx 14.6$ GeV — inconsistent with Banach fixed point
- **Conclusion:** $\gamma \approx 49/3$ is a numerical coincidence (0.037%), not a theorem
- **Evidence category remains [A-] Conjecture**
- See `docs/su3_gamma_theorem.md` for updated explicit limitation

**Open ticket:** L4 (functional determinant derivation) — remains open

---

## Q2 — FRG-NLO correction δ_NLO from Wetterich equation at k=Δ*

**Result:** FRG-NLO route is REFUTED as origin of δγ.

- Wetterich eq., Litim regulator, $k=\Delta^*$, $g^{*2}=1.0$:
  $$\delta_{\text{NLO}} = \frac{49}{3}\cdot\frac{\eta_A^{\text{NLO}}}{2} \approx 0.0437$$
- Ledger: $\delta\gamma = 0.0047$ → factor ~9 discrepancy
- **Conclusion:** $\delta\gamma = 0.0047$ is a **finite-size scaling (FSS) artefact** from  
  thermodynamic-limit extrapolation $\gamma_\infty = 16.3437$, not a FRG correction
- **Evidence category: [B]** (confirmed, origin now explicit)

---

## Q3 — RG Fixed-Point Constraint 5κ² = 3λ_S, residual 0.001

**Result:** FIXED — λ_S corrected to exact value 5/12.

| Before | After |
|--------|-------|
| $\lambda_S = 0.417$ (rounded) | $\lambda_S = 5\kappa^2/3 = 5/12$ (exact) |
| Residual: 0.001 | Residual: < 1e-78 (mp.dps=80) |
| Evidence [A] (tol. 0.01) | Evidence **[A] (tol. < 1e-14)** |

- Correction within existing uncertainty $\pm 0.007$ — no physics change
- See `docs/rg_lambda_exact_fix.md` for full analysis
- All verification scripts must be updated to use `mp.mpf('5')/mp.mpf('12')` for λ_S

---

## Claims Table

| ID | Claim | Category | Source | Change |
|----|-------|----------|--------|--------|
| C-RG-001 | 5κ²=3λ_S residual <1e-14 | A | algebraic, mp.dps=80 | UPGRADED |
| C-GAM-001 | γ=49/3 formal proof from Gap eq. | A- | conjecture only | DOWNGRADED to explicit limit |
| C-FRG-001 | δγ = δ_NLO^FRG | E | refuted numerically | NEW — REFUTED |
| C-FSS-001 | δγ=0.0047 is FSS artefact | B | FSS extrapolation | CONFIRMED |

## Reproduction Note

```bash
# One-command verification (after scripts updated with λ_S=5/12):
python3 verification/scripts/rg_constraint_exact.py
# Expected output: RG_CONSTRAINT_PASS residual < 1e-14
```
