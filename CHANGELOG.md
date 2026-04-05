# UIDT Framework Changelog

> **Format:** Narrative changelog for external readers and release documentation.
> For the internal transactional claim ledger, see `UIDT-OS/LEDGER/CHANGELOG.md`.

---

## [v3.9.5] — 2026-04-05

### FRG Fixed-Point Analysis — Extended Truncation (TKT-20260405)

**Overview**
Extended FRG truncation analysis for the γ scaling mechanism. The minimal SF² basis from
the preliminary run is augmented by the dimension-6 operator S²F², stabilizing the infrared
flow of the truncated system and isolating the Background-Field approximation (η_A = 0) as
the remaining barrier to exact numerical closure of γ = 16.339.

**Changes:**

- **Claim Added [D]:** UIDT-C-070 — stable nontrivial UV/IR fixed point for the extended
  SU(3) Yang-Mills scalar sector (SF², S²F²). Extracted scalar anomalous dimension
  η_* ≈ 0.045 supports the structural form γ ∼ (Λ_UV / Λ_IR)^{η_*} within the tested
  truncation.

- **Truncation Upgrade:** The minimal SF² basis produced complex IR eigenvalues (truncation
  artifact). Inclusion of S²F² yields real infrared eigenvalues in the tested 4×4 system.

- **Limitation Added:** L8 documents the Background-Field approximation (η_A = 0) as the
  remaining open vector for γ closure. Full Gribov-Zwanziger dynamics are required for
  exact numerical reproduction of γ = 16.339.

- **Governance:**
  Canonical γ = 16.339 remains strictly [A-] per L4 and UIDT-C-002.
  UIDT-C-016 (γ RG derivation, E-open) remains open; UIDT-C-070 establishes a concrete
  truncation-level pathway but does not resolve it.

**Verification:**
```bash
python verification/scripts/derive_rg_gamma_extended.py
```
Expected output: fixed-point coordinates, η_* ≈ 0.045, four real negative eigenvalues.
Full log: `output/rg_run_log_extended.txt`

**Open Issues:**
- Extend truncation to η_A ≠ 0 (Gribov-Zwanziger sector) to close L8.

---

