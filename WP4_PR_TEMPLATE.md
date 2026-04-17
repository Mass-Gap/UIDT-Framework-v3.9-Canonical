# Pull Request: Canonical N=99 Resolution (WP-4)

**Title:** `[UIDT-v3.9] Core: WP-4 Canonical N=99 Resolution & Archival of N=94.05`

## Affected Constants
- **Scaling Steps (N):** `99` — [Category A-] Canonical fit-parameter
- **Proposed Baseline (N):** `94.05` — [Category E] Archived

## Description
This PR formally implements the PI decision to resolve the epistemic and technical contradiction regarding the cosmological scaling parameter $N$.
1. **Creation:** `core/covariant_unification.py` to establish canonical `N=99` vacuum energy computation.
2. **Ledger Update:** `UIDT-C-050` verified active ([A-]), while the contradictory hypothesis `UIDT-C-046` ($N=94.05$) is formally archived ([E]).
3. **Verification:** `verification/scripts/verify_N_comparison.py` validates the deviation factor utilizing exact `mpmath` 80-digit precision.
4. **Documentation:** `ndof_phase_transition.md`, `theoretical_notes.md`, and `limitations.md` (L5) have been cleansed of the contradictory N=94.05 baseline.

## Audit Checklist
- [x] No `mp.dps=80` global state encapsulation. Exact precision declared locally.
- [x] All residuals tested with pure math logic in isolated validation scripts.
- [x] Linter overrides actively respected for explicit `umpath` limits.
- [x] `CHANGELOG.md` bumped with new v3.9.8 `[FIX]` entry.
