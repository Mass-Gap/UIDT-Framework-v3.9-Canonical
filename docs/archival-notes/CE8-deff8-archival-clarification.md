# Archival Clarification: CE8/E8 Motif and Effective Dimension d_eff = 8

**Status:** Draft — pending review  
**TKT:** TKT-20260326  
**Evidence Category:** A- (archival finding) / E (Stratum III interpretation)  
**Affected Constants:** None  
**Ledger Impact:** None

---

## 1. Purpose

This note clarifies the archival status of the CE8/E8 motif and the present use of the
effective dimension `d_eff = 8` within the UIDT framework. It separates what is
documented in older UIDT manuscripts (Stratum I/II) from what constitutes a new
interpretive mapping (Stratum III).

---

## 2. What the Archived UIDT Documents Contain

The following features are verifiably present in the older UIDT manuscripts
(UIDT IV, UIDT VI, UIDT Master Report Edition 2):

| Feature | Evidence | Location |
|---|---|---|
| CE8/E8 notation with `f_E8 = 248` | A- | UIDT IV §2.2, UIDT Master VI §5.2 |
| 1-loop beta-function for coupling λ | A- | UIDT VI §6, UIDT Master VI §4.2.1 |
| 2-loop beta-function extension | A- | UIDT Master VI §6.2 |
| General RG fixed-point discussion | A- | UIDT IV §3.1, UIDT Master VI §4.2.2 |
| Infrared fixed point at γ ≈ 0.278 | A- | UIDT IV §3.1 |

These findings are directly verifiable by text search in the archived documents.

---

## 3. What the Archived Documents Do NOT Contain

The following are **not** documented in the older manuscripts:

- An explicit functional renormalization group (FRG / Wetterich equation) derivation.
- A projection onto an `S F²` operator sector.
- A verified anomalous dimension result `η_S ≈ 2`.
- A derivation or derivation chain leading to `d_eff = 8`.

The absence of these items has been verified by systematic inspection of the archived texts.

---

## 4. Stratum Assignment

| Claim | Stratum | Category |
|---|---|---|
| Archived documents contain CE8/E8 motifs with `f_E8 = 248`. | I (archival) | A- |
| Archived documents contain general 1-loop / 2-loop RG language. | I (archival) | A- |
| Archived documents do NOT document an explicit FRG derivation of `d_eff = 8`. | I (negative archival finding) | A- |
| Current use of `d_eff = 8` is a UIDT interpretive mapping of the archived CE8 motif. | III (interpretive) | E |

---

## 5. Required Language for Manuscripts and PRs

Any present or future use of `d_eff = 8` in manuscripts, code, or framework documents
**must** be accompanied by one of the following labels:

- **(E) Stratum III UIDT interpretation — not derived from FRG in archived documents.**
- **Conjectural UIDT mapping. Explicit FRG derivation pending.**

Use of `d_eff = 8` without such a label constitutes an overclaim and must be flagged
by the evidence-validation pipeline.

---

## 6. Claims Table (PR Gate)

| ID | Statement | Category | Source |
|---|---|---|---|
| PR-ARCH-001 | Archived UIDT docs contain CE8/E8 motifs with `f_E8 = 248`. | A- | UIDT IV §2.2; UIDT Master VI §5.2 |
| PR-ARCH-002 | Archived UIDT docs contain 1-loop and 2-loop RG language. | A- | UIDT VI §6; UIDT Master VI §4.2.1, §6.2 |
| PR-ARCH-003 | Archived UIDT docs do not document an explicit FRG derivation of `d_eff = 8`. | A- | Negative finding; verified by inspection |
| PR-ARCH-004 | Current `d_eff = 8` is a Stratum III interpretive mapping, not a proven archival result. | E | UIDT governance (EVIDENCE_SYSTEM.md; AGENTS.md) |

---

## 7. Reproduction Note

**One-command verification:**

```
grep -r "CE8\|fE8\|248\|1-loop\|2-loop\|Wetterich\|eta_S\|d_eff" docs/ manuscript/
```

For the archived PDFs, verify manually:
- `UIDT4_FieldTheory_BridgingScales.pdf`
- `UIDT6-Information-Dynamical-Field-Theory.pdf`
- `UIDT_Master-_Report-Edition-2.pdf`

---

## 8. DOI / arXiv Resolvability

This PR adds no external scientific claim. All statements refer to internal archival
documents. External DOI/arXiv resolvability check: **not required for this patch.**

---

## 9. Affected Constants

**None.** The canonical parameter ledger (CONSTANTS.md) is unchanged.

---

## 10. Open Questions for Review

- [ ] Should `d_eff = 8` receive a formal TKT tracking entry in LEDGER_CLAIMS.json as
  an open E-category claim?
- [ ] Is a Wetterich-projection onto the `S F²` sector a planned research item?
  If so, it should be registered as a D/E claim with a falsification criterion.
- [ ] Should older UIDT manuscript references be added to REFERENCES.bib with
  explicit archival-document identifiers?

---

*Document created: 2026-03-26*  
*Author: UIDT Framework maintenance*  
*Status: DRAFT — awaiting review by P. Rietz*
