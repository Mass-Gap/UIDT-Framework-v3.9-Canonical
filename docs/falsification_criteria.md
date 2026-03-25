# Falsification Criteria — UIDT v3.9

> **Epistemic status:** These criteria define the conditions under which
> UIDT is empirically falsified. Transparency requires their permanent
> inclusion in the repository.  
> **Version:** v3.9

---

## Primary Falsification Conditions

| ID | Condition | Threshold | Confidence Required |
|----|-----------|-----------|---------------------|
| F1 | Glueball $0^{++}$ mass outside UIDT range | $< 1650$ MeV or $> 1780$ MeV | $5\sigma$ |
| F2 | No entropy gradient coupling at resonator | $\delta f/f_0 < 10^{-18}$ (null result) | $5\sigma$ |
| F3 | Cosmological constant strictly static | $|\delta w_a / w_a| < 0.005$ | $3\sigma$ |
| F4 | RG fixed point violated in lattice | $|5\kappa^2 - 3\lambda_S| > 10^{-3}$ | $3\sigma$ |
| F5 | W/Z boson mass shift absent | $\delta m < 5 \times 10^{-7}$ GeV | $5\sigma$ |

## Secondary (Supporting) Conditions

| ID | Condition | Status |
|----|-----------|--------|
| S1 | Pion mass prediction fails at $> 0.1\%$ | Currently satisfied |
| S2 | Proton mass disagreement $> 0.01\%$ | Currently satisfied |
| S3 | Lattice $0^{++}/2^{++}$ ratio outside $1.04 \pm 0.05$ | Not yet tested |

## Mathematical Internal Consistency Checks

| Check | Criterion | Status |
|-------|-----------|--------|
| RG constraint | $|5\kappa^2 - 3\lambda_S| < 10^{-14}$ | ✅ (numerical) |
| Torsion kill switch | $E_T = 0 \Rightarrow \Sigma_T = 0$ exactly | ✅ |
| Vacuum stability | $V''(v) = 2\lambda_S v^2 > 0$ | ✅ |
| Causal structure | $[S(x), S(y)] = 0$ for spacelike | ✅ (formal) |

## Status of Current Evidence

- **F1 (Glueball):** Not yet measured directly; lattice data compatible
- **F2 (Resonator):** Not yet reachable; current limit $10^{-15}$
- **F3 (Dark energy):** DESI DR2 hints at non-zero $w_a$; compatible with UIDT, not conclusive
- **F4 (RG):** Numerically satisfied to $< 10^{-14}$
- **F5 (W/Z):** CMS/ATLAS Run 3 data pending full analysis

## Cross-References

- `docs/experimental_roadmap.md` — timeline for falsification tests
- `FORMALISM.md` — canonical parameter values
- `verification/tests/` — automated RG constraint verification
