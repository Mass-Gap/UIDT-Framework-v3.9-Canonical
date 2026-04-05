# UIDT Framework v3.9 — Canonical Limitations

> **Governance:** This file is part of the Immutable Parameter Ledger. Entries may be added (with new IDs) or resolved (with `status: RESOLVED` and date). Historical IDs must never be overwritten or deleted.

---

## Active Limitations

### L1: 10¹⁰ Geometric Factor
**Status:** 🔴 OPEN (HIGHEST PRIORITY)

The factor 10¹⁰ appearing in the vacuum energy density derivation lacks a first-principles geometric derivation. It is currently set by dimensional matching. Resolution requires a complete derivation from the UIDT geometric sector (see UIDT-C-018, UIDT-C-042).

---

### L2: Electron Mass Residual
**Status:** 🔴 OPEN

The UIDT framework does not currently derive the electron mass from first principles. The quark mass hierarchy (UIDT-C-049) proceeds from E_T but does not extend to leptons. A lepton mass derivation mechanism is absent.

---

### L3: Factor 2.3 Holographic Coupling
**Status:** 🟡 PARTIALLY ADDRESSED

The factor 2.3 holographic coupling ratio (UIDT-C-051) is validated across three internal geometric methods at 500-dps but lacks external (lattice or experimental) confirmation. Category [C] ceiling applies until independent verification is achieved.

---

### L4: γ RG First-Principles Derivation
**Status:** 🟡 PARTIALLY ADDRESSED (research vector active)

The canonical value γ = 16.339 is phenomenologically calibrated [A-]. No complete derivation from RG first principles exists. γ must remain [A-] and never be upgraded to [A] without a closed, peer-reviewed derivation chain.

Active research vectors:
- UIDT-C-052: SU(3) Casimir conjecture (49/3 ≈ 16.333) [E]
- UIDT-C-070: FRG truncation-level pathway (η_* ≈ 0.045) [D] — see L8

**Condition for Resolution:** A closed derivation from the UIDT Lagrangian that reproduces γ = 16.339 at Category A precision, independently verified.

---

### L5: N=99 vs N=94.05 Self-Contradiction
**Status:** 🔴 OPEN

N=99 RG cascade steps are used in all production code (covariant_unification.py:27) and verification scripts. PR #87 proposed N=94.05 as a replacement (UIDT-C-046), but the contradiction is unresolved. Both values co-exist in the codebase. See UIDT-C-017, UIDT-C-039, UIDT-C-046, UIDT-C-050.

**Condition for Resolution:** Adopt one value canonically, update all code and scripts, and verify ρ_vac agreement.

---

### L8: FRG Scale Compression and Background-Field Approximation (Claim UIDT-C-070)
**Status:** 🔬 ACTIVE RESEARCH

The FRG derivation of the γ scaling mechanism (UIDT-C-070, Evidence D) proceeds via a scalar anomalous dimension η_* ≈ 0.045, obtained from a stable nontrivial fixed point of the extended FRG truncation (SF², S²F²) at mp.dps = 80. Within the tested truncation, inclusion of the dimension-6 operator S²F² removes the complex IR eigenvalue pair of the minimal SF² basis and yields real infrared eigenvalues.

The remaining limitation is the Background-Field approximation (η_A = 0). With scalar-sector fluctuations alone, the truncation yields a scale ratio ≈ 6.7, below the canonical γ = 16.339.

**Impact:**
- UIDT-C-070 is Evidence Category [D] (analytical projection, not experimentally verified)
- γ = 16.339 remains strictly [A-] (phenomenologically calibrated; see L4)
- The scale gap between η_* ≈ 0.045 and the canonical ratio indicates that gluonic infrared dynamics are quantitatively essential for exact closure

**Condition for Resolution:** Extend the FRG truncation to include full gluonic infrared dynamics (non-trivial η_A, Gribov-Zwanziger propagator). If the resulting fixed-point η_* reproduces the scale ratio γ = 16.339 within the tolerated numerical precision, L8 may be closed and UIDT-C-070 considered for upgrade from [D] toward [C] or [B].

**Note:** L8 is a refinement of the open research vector registered in L4. L4 documents the absence of any complete RG derivation of γ; L8 documents the specific truncation limitation of the current FRG approach within that open vector.

> ⚠️ IDs L6 and L7 are historically resolved entries (archived below). They must not be overwritten.

---

## Limitation Impact Matrix

| ID | Description | Impact Area | Severity |
|----|-------------|-------------|----------|
| L1 | 10¹⁰ geometric factor | Vacuum energy density | 🔴 High |
| L2 | Electron mass absent | Lepton sector | 🔴 High |
| L3 | Factor 2.3 unconfirmed externally | Holographic sector | 🟡 Medium |
| L4 | γ not RG-derived | Core parameter | 🟡 Medium |
| L5 | N=99 vs N=94.05 contradiction | All code | 🔴 High |
| L8 | FRG truncation (η_A = 0) | γ derivation pathway | 🟡 Medium |

---

## Resolved Limitations (Historical)

### L6 — RESOLVED (archived)
*Details archived. ID reserved — do not reuse.*

### L7 — RESOLVED (archived)
*Details archived. ID reserved — do not reuse.*

---

*Maintainer: P. Rietz | UIDT Framework v3.9 | Last updated: 2026-04-05*
*All limitation IDs are permanent. Add new limitations with the next free sequential ID.*
