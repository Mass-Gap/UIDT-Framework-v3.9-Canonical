# UIDT External Contributions Ledger

**Framework:** UIDT v3.9  
**Maintainer:** P. Rietz  
**Created:** 2026-04-03  
**Scope:** Entire repository (all directories, not limited to `clay-submission/`)  
**Policy:** UIDT Constitution v4.1, PAPER AUDIT PROTOCOL

---

## Purpose

This document records external materials that were received, reviewed, or cross-validated during UIDT development, including their precise relationship to UIDT-internal derivations, their evidence status, and any citation integrity findings.

---

## Record 001 — Baddewithana (UIDT Zenodo Research Group)

### Administrative Status

| Field | Value |
|-------|-------|
| Contact | Baddewithana (UIDT Zenodo Research Group) |
| Date received | February 2026 |
| Material type | Independent research document (3-6-9 Octave Scaling Model) |
| Citation agreement | **Not in place** — no formal agreement as of 2026-04-03 |
| Attribution form | Courtesy acknowledgement only (pending formal agreement) |
| `clay-submission/` exclusion | **Active** — administrative + scientific grounds (see below) |

### Chronological Priority Record (Stratum I)

| Event | Date | Documentation |
|-------|------|---------------|
| P. Rietz independently derives 104.66 MeV geometric base and 107.10 MeV vacuum resonance via Banach Fixed-Point + Lattice Torsion (E_T = 2.44 MeV) | **Prior to February 2026** | README Pillar II; `verification/scripts/UIDT_Master_Verification.py` |
| Baddewithana document received | February 2026 | Confirmed |
| P. Rietz provides UIDT theoretical explanation for Baddewithana's numerical results | February 2026 | Confirmed |
| Material cross-validated; selective integration into UIDT | February–March 2026 | Confirmed |

> **Priority conclusion:** P. Rietz independently derived 104.66 MeV and 107.10 MeV **prior to receipt** of the Baddewithana document. The Baddewithana material served as external cross-validation, not as source material. UIDT derivation chain: Δ* = 1.710 GeV → E_geo = Δ*/γ = 104.66 MeV → + E_T = 2.44 MeV → f_vac = 107.10 MeV.

### Formal Framework Assessment (Stratum II)

| Criterion | UIDT | 3-6-9 Octave Scaling Model |
|-----------|------|--------------------------|
| Derivation basis | Yang-Mills QFT, RG fixed point, Banach theorem | Vacuum harmonic geometry, 107.1 MeV base unit |
| Renormalisation group | ✓ explicit (5κ² = 3λ_S, Constitution) | ✗ not present |
| Precision framework | mpmath 80 dps, residual < 10⁻¹⁴ | Not specified |
| Evidence system | A / A- / B / C / D / E with falsification criteria | Not present |
| Falsification criteria | Explicit (FALSIFICATION.md, F1–F9+) | Post-hoc numerical matching |
| Stratum | I–III separated | Not separated |

### Numerical Proximity Assessment (Stratum III)

The numerical proximity Δ* ≈ 16 × 107.1 MeV ≈ 1.714 GeV (vs UIDT Δ* = 1.710 GeV) is classified as **Evidence [E]** (speculative post-hoc observation). It is not a derivation and does not constitute a theoretical connection.

### Citation Integrity Finding

> **[AUDIT_FAIL]** — Reference [3] in the Baddewithana document (cited as arXiv:2405.12345) has not been independently verified. This identifier does not resolve to a known arXiv preprint as of 2026-04-03. **No cross-citation permitted until author provides corrected identifier.**

### Repository-Wide Scope

This attribution and citation integrity requirement applies to **all UIDT directories**:

| Directory | Rule |
|-----------|------|
| `clay-submission/` | Baddewithana 3-6-9 framework **excluded** — administrative (no agreement) + scientific (insufficient rigour for Clay-level submission) |
| `core/` | Any reference to 107.1 MeV as external unit must be flagged; UIDT-internal derivation cited instead |
| `modules/` | `lattice_topology.py`, `harmonic_predictions.py` derive values independently; no attribution to 3-6-9 model |
| `LEDGER/CLAIMS.json` | All claims referencing vacuum resonance cite UIDT internal derivation chain |
| `docs/` | No 3-6-9 Octave Scaling Model language permitted |
| `manuscript/` | Citation to Baddewithana only as courtesy acknowledgement if formally agreed; not as theoretical basis |
| `references/` | External citations must carry verified DOI or arXiv identifier per UIDT evidence standards |

### Required Actions

- [ ] Confirm with Baddewithana preferred form of attribution
- [ ] Add courtesy acknowledgement to `manuscript/` acknowledgements section (pending formal agreement)
- [ ] Verify or correct Reference [3] (arXiv:2405.12345) in Baddewithana document before any cross-citation
- [x] `LEDGER/external_contributions.md` created — **this document**

---

## Addition Protocol (Future Records)

All future external contributions must be registered here before integration. Required fields:

```
### Record NNN — [Contributor]
- Date received:
- Material type:
- Citation agreement: [yes/no/pending]
- Priority record: [UIDT prior / simultaneous / external-first]
- Citation integrity: [verified / [AUDIT_FAIL]]
- Stratum classification: [I/II/III]
- Evidence category: [A–E]
- Repository-wide scope confirmed: [yes/no]
```

---

*Raises Issue #184. Fulfils action item 3 of Issue #184.*  
*Maintainer: P. Rietz — UIDT Framework v3.9*
