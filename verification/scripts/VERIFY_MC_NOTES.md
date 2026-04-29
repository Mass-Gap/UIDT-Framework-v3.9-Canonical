# Verification Script: verify_monte_carlo_research_notes.py

**Status:** ready to run — requires raw CSV from Zenodo

**Evidence categories produced:** [A] (recomputed correlations), [B] (vs stored artefact)

---

## Purpose

Resolves the open `[TENSION ALERT]` for `r(Delta*, Pi_S)`
documented in `simulation/monte_carlo/STRATUM_II_RESULTS.md` §3
and `simulation/monte_carlo/clay_appendix_mc_evidence.tex` §MC.6.

Also verifies the open `[RG_CONSTRAINT_FAIL]` from §MC.7.

---

## One-Command Reproduction

```bash
# Step 1: download raw CSV from Zenodo (19 MB)
curl -L -o simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv \
  "https://zenodo.org/records/17554179/files/UIDT_MonteCarlo_samples_100k.csv"

# Step 2: run audit
python verification/scripts/verify_monte_carlo_research_notes.py \
  --raw  simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv \
  --corr simulation/monte_carlo/UIDT_MonteCarlo_correlation_matrix.csv \
  --hp   simulation/monte_carlo/UIDT_HighPrecision_mean_values.csv
```

---

## What the Script Checks

| Phase | Check | Emits |
|---|---|---|
| 1 | 5κ² = 3λ_S at hp-mean | `[RG_CONSTRAINT_FAIL]` if residual > 1e-14 |
| 2 | Load raw CSV, report columns | `[AUDIT_FAIL]` if not found |
| 3 | Recompute all N(N-1)/2 correlations (mpmath, mp.dps=80) | — |
| 4 | Compare vs stored matrix, |Δr| > 0.05 | `[TENSION ALERT]` |
| 5 | Specific r(Δ*, Π_S) check | `[TENSION ALERT]` or `RESOLVED` |

---

## Known Ahead-of-Run Finding

The stored correlation matrix (`UIDT_MonteCarlo_correlation_matrix.csv`)
contains **8 parameters**: `m_S, kappa, lambda_S, C, alpha_s, Delta, gamma, Psi`.

The column `Pi_S` (or `Π_S`) is **absent** from the stored matrix.

This means the stored claim `r(Delta*, Pi_S) = +0.720284420`
**cannot originate from the 8×8 stored matrix**.
The script will report this as an absent-column finding in Phase 4
and specifically investigate in Phase 5.

Possible resolutions:
1. The raw CSV contains a `Pi_S` column not present in the stored summary matrix.
2. `Pi_S` was mapped to a different column name in an earlier chain version.
3. The value originated from a different (unlisted) simulation run.

The script output will distinguish these cases.

---

## Precision Rules

- `mpmath` with `mp.dps = 80` declared **locally** in each function.
- No `float()`, no `round()`, no `unittest.mock`.
- LEDGER constants defined as string literals, converted via `mp.mpf()`.
- `mp.nstr()` used for all output formatting.

---

## Output Interpretation

| Output line | Meaning |
|---|---|
| `[TENSION ALERT]` | |Δr| > 0.05 — open conflict |
| `[TENSION ALERT] RESOLVED` | stored value reproduced within threshold |
| `[TENSION ALERT] PARTIALLY OPEN` | no numerical conflict but absent columns |
| `[RG_CONSTRAINT_FAIL]` | residual > 1e-14 at hp-mean |
| `[AUDIT_FAIL]` | file not found or column missing |
| `OK` | within threshold |
