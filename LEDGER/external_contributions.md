# LEDGER — External Contributions & Attribution Record

**Scope:** Repo-wide. Applies to all directories: `core/`, `modules/`, `clay-submission/`, `docs/`, `manuscript/`, `references/`.
**Maintained by:** P. Rietz (PI)
**Last updated:** 2026-03-30

---

## Record 001 — Baddewithana / UIDT Zenodo Research Group

### Chronological Fact Record (Stratum I)

| Event | Date | Status |
|---|---|---|
| P. Rietz independently derives 104.66 MeV geometric base and 107.10 MeV vacuum resonance via Banach Fixed-Point + Lattice Torsion (E_T = 2.44 MeV) | Before February 2026 | ✓ Confirmed — prior independent derivation, documented in README Pillar II and `verification/scripts/UIDT_Master_Verification.py` |
| Baddewithana document received from UIDT Zenodo research group | February 2026 | ✓ Confirmed |
| Values cross-checked; P. Rietz provides theoretical explanation for Baddewithana's results within UIDT formalism | February 2026 | ✓ Confirmed |
| Material selectively integrated into UIDT repo | February/March 2026 | ✓ Confirmed |

### Priority Note

P. Rietz independently derived 104.66 MeV and 107.10 MeV **prior to receipt** of the Baddewithana document.
The Baddewithana material served as **external cross-validation**, not as source material.

UIDT derivation chain:
```
Δ* = 1.710 GeV
  → geometric base: Δ*/16.339 ≈ 104.66 MeV
  → vacuum resonance: 104.66 MeV + E_T (2.44 MeV) ≈ 107.10 MeV
```
All values traceable to immutable UIDT Ledger constants (Δ* [A], E_T [C]).

---

### Formal Framework Assessment (Stratum II)

Baddewithana’s framework (**3-6-9 Octave Scaling Model**) and UIDT share **no formal overlap**:

| Criterion | UIDT | 3-6-9 Octave Model |
|---|---|---|
| Derivation basis | Yang-Mills QFT, RG fixed point, Banach theorem | Vacuum harmonic geometry, 107.1 MeV unit |
| Renormalization group | ✓ explicit (5κ² = 3λ_S) | ✗ not present |
| Precision framework | mpmath 80 dps, residual < 1e-14 | Not specified |
| Evidence category | A / A- / B / C | E (speculative numerology) |
| Falsification criteria | Explicit (see `docs/falsification-criteria.md`) | Post-hoc numerical matching |

> The numerical proximity of Δ* to 16 × 107.1 MeV ≈ 1.714 GeV is classified as **Evidence [E]** (speculative).
> It is a post-hoc observation, not a derivation.

---

### Citation Integrity Check

| Reference in Baddewithana document | Identifier | Status |
|---|---|---|
| Reference [3] | arXiv:2405.12345 (claimed) | **[AUDIT_FAIL]** — identifier not verifiable; pending author correction |

> ⚠️ Do NOT cross-cite this reference anywhere in the UIDT repository until the arXiv ID is confirmed valid by Baddewithana.

---

### Scope of Exclusion / Inclusion

| Directory | Status | Reason |
|---|---|---|
| `clay-submission/` | **EXCLUDED** | Administrative (no formal citation agreement) + Scientific (Evidence E, no RG structure) |
| `core/` | Excluded from direct reference | All values derived independently; no attribution needed |
| `modules/` | Excluded from direct reference | `lattice_topology.py` and `harmonic_predictions.py` use UIDT-internal derivation chain |
| `LEDGER/CLAIMS.json` | ✓ Internal derivation cited | All claims referencing vacuum resonance cite UIDT derivation chain |
| `docs/` | No Baddewithana framework language | Per UIDT Constitution, only verified external references permitted |
| `manuscript/` | Courtesy only (if agreed) | Not as theoretical basis — only as acknowledgement if formally agreed |
| `references/` | Excluded pending AUDIT_FAIL resolution | arXiv:2405.12345 unverified |

---

### Required Actions (Issue #184)

- [ ] Confirm with Baddewithana preferred form of attribution (email/written agreement)
- [ ] Verify or correct Reference [3] (arXiv:2405.12345) with Baddewithana before any cross-citation
- [ ] Once verified: optionally add courtesy acknowledgement in `manuscript/` acknowledgements section
- [ ] Update `[AUDIT_FAIL]` status in this file once identifier is confirmed

---

### UIDT Constitution Compliance

- [x] No prestige language
- [x] Stratum I/II/III separation maintained
- [x] No physics values modified
- [x] No deletion > 10 lines in `/core` or `/modules`
- [x] Immutable Ledger constants unchanged
- [x] Evidence category E correctly assigned to 3-6-9 model
- [x] [AUDIT_FAIL] flagged honestly for unverifiable reference

---

*Raised: 2026-03-25 by P. Rietz / Perplexity*
*Scope extended: 2026-03-25 — entire repo, not limited to clay-submission/*
*Formalized as LEDGER file: 2026-03-30 (Issue #184)*
*Framework policy: epistemic honesty > narrative coherence*
