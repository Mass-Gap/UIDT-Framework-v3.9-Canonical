# Attribution Record — Baddewithana / UIDT Zenodo Research Group

> **Moved from root:** `issue184.txt` → `docs/archival-notes/` (TKT-20260418)
> **Original location:** `issue184.txt` (root)
> **Reason:** `.txt` raw files do not belong at repository root per architecture rules.
> **Action status:** OPEN — documentation only, no code change required.

---

## Status

OPEN — documentation only, no code change required

## Chronological Fact Record (Stratum I)

| Event | Date | Status |
|---|---|---|
| P. Rietz independently derives 104.66 MeV geometric base and 107.10 MeV vacuum resonance via Banach Fixed-Point + Lattice Torsion (E_T = 2.44 MeV) | **before** receipt | ✔ Confirmed — prior independent derivation, documented in README Pillar II and `verification/scripts/UIDT_Master_Verification.py` |
| Baddewithana document received from UIDT Zenodo research group | February 2026 | ✔ Confirmed |
| Values cross-checked; P. Rietz provides theoretical explanation for Baddewithana's results within UIDT formalism | February 2026 | ✔ Confirmed |
| Material selectively integrated into UIDT repo | February/March 2026 | ✔ Confirmed |

## Priority Note

P. Rietz independently derived 104.66 MeV and 107.10 MeV **prior to receipt** of the Baddewithana document. The Baddewithana material served as external cross-validation, not as source material. UIDT derivation chain: Δ* = 1.710 GeV → geometric base 104.66 MeV → + E_T 2.44 MeV → vacuum resonance 107.10 MeV.

---

## Formal Framework Assessment (Stratum II)

| Criterion | UIDT | 3-6-9 Octave Model |
|---|---|---|
| Derivation basis | Yang-Mills QFT, RG fixed point, Banach theorem | Vacuum harmonic geometry, 107.1 MeV unit |
| Renormalization group | ✔ explicit (5κ² = 3λS) | ✘ not present |
| Precision framework | mpmath 80 dps, residual < 1e-14 | Not specified |
| Evidence category | A / A- / B | E (speculative numerology) |
| Falsification criteria | Explicit (FALSIFICATION.md) | Post-hoc numerical matching |

The numerical proximity of Δ* to 16 × 107.1 MeV ≈ 1.714 GeV is classified as **Evidence [E]** (speculative). It is a post-hoc observation, not a derivation.

---

## ⚠ SCOPE: ENTIRE FRAMEWORK (not limited to clay-submission/)

This attribution and citation integrity requirement applies **repo-wide**:

- `clay-submission/` — Baddewithana exclusion applies (scientific + administrative grounds)
- `core/` — any reference to 107.1 MeV as an external unit must be flagged
- `modules/` — `lattice_topology.py` and `harmonic_predictions.py` derive values independently; no attribution to 3-6-9 model
- `LEDGER/CLAIMS.json` — all claims referencing vacuum resonance must cite UIDT internal derivation chain
- `docs/` — no Baddewithana framework language permitted
- `manuscript/` — citation to Baddewithana only as courtesy acknowledgement if agreed, not as theoretical basis
- `references/` — external citations must carry verified DOI or arXiv identifier per UIDT evidence standards

**Citation integrity check (arXiv:2405.12345 in Baddewithana Ref [3]) is unverified — [AUDIT_FAIL] pending author correction.**

---

## Clay Submission Constraint

⚠ The `clay-submission/` directory must NOT reference Baddewithana's results or the 3-6-9 Octave Scaling Model.

This exclusion is **doubly justified**:
1. **Administrative:** no formal citation agreement in place
2. **Scientific:** the 3-6-9 framework does not meet the rigour standard required for Clay-level submission (no RG structure, no precision verification, Evidence [E] only)

---

## Action Required

1. Confirm with Baddewithana the preferred form of attribution
2. Add courtesy acknowledgement in `LEDGER/external_contributions.md` (to be created)
3. Verify or correct Reference [3] (arXiv:2405.12345) in Baddewithana's document before any cross-citation
4. Scope confirmed: all directories covered, not only clay-submission/

## Does NOT block

- HAL-QCD collaboration document (fully independent, March 2026)
- Zenodo preprint upload
- clay-submission/ (by design)

---

*Raised by: Perplexity / P. Rietz — 2026-03-25*
*Scope corrected: 2026-03-25 — extended to entire framework, not limited to clay-submission/*
*Moved to docs/archival-notes/: 2026-04-18 (TKT-20260418)*
*Framework policy: epistemic honesty > narrative coherence*
