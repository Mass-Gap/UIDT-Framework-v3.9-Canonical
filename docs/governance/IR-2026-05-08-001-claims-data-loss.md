# Incident Report: CLAIMS.json Data Loss (IR-2026-05-08-001)

**Severity:** 🔴 CRITICAL  
**Discovered:** 2026-05-08 04:34 CEST  
**Root Cause:** PR #386 squash-merge  
**Impact:** Complete loss of 60-claim machine-readable registry  
**Resolution:** Restored from git history

---

## Timeline

| Timestamp | Event | Commit |
|---|---|---|
| 2026-04-29 | Last known good state on main (58 claims, v3.9.8) | `97204c8` |
| 2026-05-01 | Branch `c86e36d` adds claims (60 claims, v3.9.9) | `c86e36d` |
| **2026-05-02** | **PR #386 merged — CLAIMS.json replaced with "CLAIMS_JSON_PLACEHOLDER"** | **`2e781ec`** |
| 2026-05-06 | Branch commit `1a53590` still has valid data (767 lines) | `1a53590` |
| 2026-05-08 | Placeholder discovered during Phase 1 audit | Working tree |

---

## Root Cause Analysis

**PR #386:** "Literature: HJ-Papers Phase-0 Integration v3.9.8 to v3.9.9"

This PR was a large literature integration (HJ-Papers) that included a squash-merge.
During the merge, `LEDGER/CLAIMS.json` was **reduced from 669 lines to 1 line**
containing only the text `CLAIMS_JSON_PLACEHOLDER`.

**Probable mechanism:** The PR branch was likely based on an older commit where
CLAIMS.json had not yet been created or was a placeholder. When the squash-merge
resolved the diff, it took the branch version (placeholder) instead of the main
version (669 lines of valid claims data).

```
Before merge (main @ 97204c8): 669 lines, 58 claims, v3.9.8
After merge (main @ 2e781ec):    1 line,  "CLAIMS_JSON_PLACEHOLDER"
```

**Key finding:** The diff shows `670 +-` — nearly the entire file was deleted
in a single merge operation. The `--stat` output confirms:
```
LEDGER/CLAIMS.json | 670 +--------------------------
```

---

## Data Recovery

The most recent valid version was recovered from commit `1a53590` on branch
`TKT-2026-05-06-desi-wa-tension-patch` which contained:
- **767 lines** (additional DESI w_a tension claims)
- **60 claims** (v3.9.8 + 2 additional from DESI patch)
- All PI overrides (D17) intact
- All evidence categories preserved

Command used:
```bash
git show 1a53590:LEDGER/CLAIMS.json > LEDGER/CLAIMS.json
```

---

## Prevention Measures

1. **CI Guard (proposed):** Add a GitHub Actions check that blocks merges if
   `LEDGER/CLAIMS.json` drops below 100 lines or fails JSON validation.
2. **Squash-merge review:** All squash-merges involving `LEDGER/` should
   require explicit diff review of protected files.
3. **Pre-merge hook:** Validate that CLAIMS.json parses as valid JSON with
   `metadata.total_claims > 0` before any merge to main.

---

**Affected Claims:** All 60 claims (UIDT-C-001 through UIDT-C-103)  
**Data Loss Duration:** 6 days (2026-05-02 to 2026-05-08)  
**Recovery Status:** ✅ COMPLETE — restored to pre-incident state plus DESI patch
