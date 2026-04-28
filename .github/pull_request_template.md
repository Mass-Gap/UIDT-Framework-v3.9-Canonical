# [UIDT-v3.9] `<Component>`: `<Description>`

> **PR Naming Rule:** `[UIDT-v3.9] <Component>: <Description>`  
> Delete all instructional comments before submitting.

---

## 1. Summary

<!-- One paragraph: what changed and why. -->

---

## 2. Affected Constants & Evidence Categories

| Constant | Ledger Value | Evidence Category | Changed? |
|---|---|---|---|
| Δ* | 1.710 ± 0.015 GeV | [A] | ☐ yes / ☑ no |
| γ | 16.339 | [A-] | ☐ yes / ☑ no |
| γ∞ | 16.3437 | [B] | ☐ yes / ☑ no |
| δγ | 0.0047 | [B/D] | ☐ yes / ☑ no |
| v | 47.7 MeV | [A] | ☐ yes / ☑ no |
| w0 | −0.99 | [C] | ☐ yes / ☑ no |
| ET | 2.44 MeV | [C] | ☐ yes / ☑ no |

> **If any constant is marked "yes": this PR requires an explicit Ledger Amendment with independent Reproduction Note.**

---

## 3. Epistemic Stratum

Which stratum does this PR primarily affect?

- [ ] Stratum I — Empirical measurements / experimental uncertainties / observational data  
- [ ] Stratum II — Scientific consensus / field status / review knowledge  
- [ ] Stratum III — UIDT interpretation / model mapping / theoretical extension

> Strata must not be mixed in a single commit. If changes span multiple strata, split into separate PRs.

---

## 4. RG Constraint Check

Is the constraint `5 κ² = 3 λ_S` (residual tolerance |LHS − RHS| < 1e-14) still satisfied?

- [ ] Yes — verified with mpmath (mp.dps = 80, local)
- [ ] Not applicable (no /core or /modules code touched)
- [ ] No → **[RG_CONSTRAINT_FAIL]** — PR must not be merged

> λ_S = 5/12 (exact) per TKT-20260403-LAMBDA-FIX. Never use λ_S = 0.417 (rounded).

---

## 5. L1 / L4 / L5 Deficiency Status

| Deficiency | Description | Status in this PR |
|---|---|---|
| **L1** | Holographic L⁴ factor unexplained | ☐ Unchanged / ☐ Partially addressed / ☐ Resolved |
| **L4** | γ not RG-derived from first principles | ☐ Unchanged / ☐ Partially addressed / ☐ Resolved |
| **L5** | N=99 not derived from YM axioms | ☐ Unchanged / ☐ Partially addressed / ☐ Resolved |

> If any deficiency is marked "Resolved": attach independent derivation + one-command Reproduction Note.

---

## 6. Pre-Flight Checklist

- [ ] No `float()` or `round()` introduced — all calculations use `mpmath.mpf`
- [ ] `mp.dps = 80` declared **locally** (not in config.py or global scope)
- [ ] No deletion > 10 lines in `/core` or `/modules` without explicit confirmation
- [ ] Ledger constants unchanged (or Ledger Amendment filed)
- [ ] No known TypeErrors, syntax errors, or intentional crashes introduced
- [ ] All new citations have verified DOI or arXiv identifier
- [ ] Verification scripts placed in `verification/tests/` or `verification/scripts/` only

---

## 7. Reproduction Note

```bash
# One-command verification of this PR's claims:
# e.g.: cd verification/ && python verify_<component>.py
```

---

## 8. Claims Table

| Claim ID | Category (A/A-/B/C/D/E) | Source (arXiv/DOI/UIDT-internal) |
|---|---|---|
| | | |

---

*UIDT Constitution v4.1 compliant. Communicate results to maintainer in German; repository outputs in English.*
