# [REVIEW-DELTA-NOTICE] — critical_review_2025.md vs epistemic_audit_2026-03-30.md

**Raised:** 2026-04-18  
**Ticket:** TKT-20260418-REVIEW-DELTA  
**Status:** 🔴 PENDING — requires P. Rietz manual decision  
**UIDT Rule:** Epistemic Stratification (UIDT Constitution v4.1, EVIDENCE STRATIFICATION, LANGUAGE RULES)

---

## Background

A structural diff between `docs/critical_review_2025.md` and `docs/epistemic_audit_2026-03-30.md`
reveals four category and framing divergences that **require maintainer decision** before
any automated merge or update can occur.

Per UIDT Constitution: no AI may autonomously change evidence categories, downgrade/upgrade claims,
or alter stratum assignments. These are maintainer-only decisions.

---

## Delta Table

| Parameter / Claim | critical_review_2025.md | epistemic_audit_2026-03-30.md | Delta | Decision required |
|---|---|---|---|---|
| **δγ = 0.0047 — FRG NLO claim** | Not mentioned; `γ = 16.339` cited as [A−] without FRG-NLO qualifier | Explicitly **downgraded to [E]** (PR #199 addendum): factor ~9 discrepancy vs `δ_NLO`; upgrade requires TKT-20260403-FRG-NLO | Claim δγ = δ_NLO absent from 2025 review | Should 2025 review be annotated or superseded? |
| **E_T = 2.44 MeV evidence category** | Not explicitly categorised; treated as derived (neutral) | Corrected to **[C]** (was [D] in some earlier docs); FLAG 2024 tension documented at 3.75σ pre-QED | Category upgrade C > D implicit in 2025 | Confirm [C] as the single canonical assignment |
| **Cosmological constant claim framing** | `DESI DR2 suggests possible dark energy evolution: compatible with UIDT [C]` — correct Stratum II language | DESI calibration confirmed as calibration input for [C] parameters; H₀ tension explicitly **not resolved** | No conflict in framing, but 2025 review cites `report.2025.pdf (DOI: osf.io/wdyxc)` as source — DOI resolvability not verified in 2026 audit | Verify DOI `10.17605/osf.io/wdyxc` is still live and points to correct document |
| **Cross-references in 2025 review** | References `docs/falsification_criteria.md` (stub, **now archived**) and `docs/theory_comparison.md` (file not found in current tree) | — | Two broken cross-references | Either update links or add deprecation note in 2025 file |

---

## Broken Cross-References in critical_review_2025.md

| Broken link | Status | Replacement |
|---|---|---|
| `docs/falsification_criteria.md` | ❌ **Archived** (TKT-20260418, PR #319) | → `docs/falsification-criteria.md` |
| `docs/theory_comparison.md` | ❌ **File not found** in repository | Create or remove reference |

---

## Recommended Actions (for P. Rietz to decide)

1. **Confirm [C] as canonical category for E_T = 2.44 MeV** across all documents
2. **Verify DOI** `10.17605/osf.io/wdyxc` is live and correct
3. **Decide fate of `docs/critical_review_2025.md`**: annotate broken links in-place, or move to archive and replace with a pointer to `epistemic_audit_2026-03-30.md`
4. **Create or remove** `docs/theory_comparison.md` reference
5. **Confirm** whether `δγ = δ_NLO` claim needs to be explicitly marked [E] in the 2025 review for consistency

---

> Per UIDT Constitution v4.1 — LIMITATION POLICY:  
> *"Transparency has priority over narrative. Known limitations must always be acknowledged."*  
> This notice is a documentation action only. No evidence category has been changed.
> No canonical constant has been modified. No stratum assignment has been altered.

---

_Filed by: UIDT AI assistant — 2026-04-18. Awaiting maintainer decision._
