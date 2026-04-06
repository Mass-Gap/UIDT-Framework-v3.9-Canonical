# Rescue-PR A3: OPUS Advisory for Dirty-Branch File Recovery

> **FOR OPUS / PI REVIEW — 2026-04-05**

## Situation

29 files recovered from 5 dirty branches that were never cleanly merged
into main. These branches contain a mix of legitimate code (verification
scripts, audit infrastructure, core implementations) and junk (arxiv_scan.py,
terminal artifacts, UIDT-OS leaks). Only the legitimate files were rescued.

## Critical Items Requiring PI Review

### 1. `core/banach_proof.py` (62 lines) — ⚠️ HIGH PRIORITY

**Source:** `feature/core-verification-baseline`

This file implements the Banach fixed-point iteration T(Δ) → Δ*. It touches
the `core/` directory which is under the 3-Phase Lock protocol. The file is
**new** (not a modification of existing code), so the 10-line deletion limit
does not apply. However:

- The file must be independently verified to produce Δ* = 1.710 ± 0.015 GeV
- The contraction mapping T must satisfy the Lipschitz constant L < 1
- Import of mpmath and `mp.dps = 80` is correctly local (line 6-7)
- Lambda = 1.000 GeV (renormalization scale) — verify this is the intended value

**Recommendation:** Review before merge. Run `py -3 core/banach_proof.py`
and verify output matches expected Δ*.

### 2. `core/rg_closure.py` (41 lines) — ⚠️ HIGH PRIORITY

**Source:** `feature/core-verification-baseline`

This file implements the RG fixed-point constraint 5κ² = 3λ_S. It
correctly derives λ_S from the exact relation `(5/3) * κ²` rather than
the rounded value 0.417. Contains explicit linter protection comment.

**Recommendation:** Review before merge. Verify residual is exactly 0.

### 3. Audit Suite (15 scripts, ~2500 lines) — ℹ️ MEDIUM PRIORITY

**Source:** `feature/plan-a1-execute-uidt-qa-audit`

Professional quality: uses `@dataclass`, git integration, SHA-256 hashing,
timestamp-based snapshots. Covers:
- `framework_integrity_audit.py` (1490 lines, main audit engine)
- `dimensional_analysis.py`, `tolerance_enforcement.py`
- `claims_test_coverage_map.py`, `proof_completeness_audit.py`
- etc.

**Evaluation:** These appear to be **current and useful** — they were written
for the February 2026 QA sweep and have not been superseded by a later
framework. The audit functions are complementary to the existing
`verification/scripts/` suite.

No λ_S = 0.417 found in any audit file.

**Recommendation:** Merge is safe. These are read-only analysis tools.

### 4. Registries (4 JSON files) — ℹ️ LOW PRIORITY

**Source:** `feature/plan-a1-execute-uidt-qa-audit`

Static reference data:
- `axioms_registry.json` (100 lines)
- `symbol_registry.json` (93 lines)
- `units_registry.json` (68 lines)
- `tickets_registry.json` (14 lines)

**Recommendation:** Merge is safe. Static reference data, no precision impact.

## Excluded Files (by design)

| File | Reason |
|------|--------|
| `arxiv_scan.py` | Root-level junk |
| `tickets_new.json` | Root-level junk |
| `LEDGER/FALSIFICATION.md` (from dirty branches) | Stale, main has better version |
| `UIDT-OS/CANONICAL/CONSTANTS.md` (from #193/#195) | UIDT-OS internal, never commit |
| `UIDT-OS/LEDGER/CHANGELOG.md` (from #193/#195) | UIDT-OS internal, never commit |
| `docs/archive/UIDT_Framework-2025.zip` | Binary archive, too large |
| `epistemic_risk_map.json`, `findings.json`, `metrics.json`, etc. | Root-level internal |
| `verification/REORGANIZATION_SUMMARY.md` | Superseded by current structure |

---

*Author: P. Rietz | DOI: 10.5281/zenodo.17835200*
