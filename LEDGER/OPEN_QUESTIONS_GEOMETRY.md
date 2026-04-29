# Open Questions — Geometry and First Principles

> **Last updated:** 2026-04-28 (TKT-20260428-L1-L4-L5-NOGO)
> **Previous update:** 2026-03-30

This file tracks formally open geometric and first-principles questions
within the UIDT framework. All entries carry an evidence category
per the UIDT Evidence System (A–E).

---

## Resolved Items

### TKT-20260403-LAMBDA-FIX — λS Exact Value [RESOLVED 2026-04-28]

**Problem:** λS = 0.417 (rounded) caused |5κ² − 3λS| ≈ 10⁻³,
violating the RG constraint tolerance < 10⁻¹⁴ → **[RG_CONSTRAINT_FAIL]**.

**Fix:** λS = 5/12 (exact rational). With κ = 1/2:
```
5κ² = 5 · (1/4) = 5/4
3λS = 3 · (5/12) = 15/12 = 5/4
|5κ² − 3λS| = 0  ✓
```

In all mpmath code, use (local mp.dps = 80):
```python
import mpmath as mp
mp.dps = 80
lambda_S = mp.mpf('5') / mp.mpf('12')   # exact
kappa    = mp.mpf('1') / mp.mpf('2')    # exact
```

**Evidence:** [A] — mathematical identity.
**Status:** RESOLVED. All future code must use λS = 5/12.

---

## Open Items

### L1 — Origin of γ = 16.339 [OPEN]

**Current evidence:** [A-] phenomenological parameter.

**No-go audit result (2026-04-28):** All four candidate
first-principles derivation paths are blocked.
See `docs/L1_L4_L5_nogo_analysis_2026-04-28.md` for full audit.

**Open research vectors:**
- Vector D: 1/N_c systematic scan [Evidence D]
- Vector E: Non-perturbative RG flow β_κ, β_{λS} (`rg_beta_derivation_gamma.md`) [Evidence D]

**Constraint:** γ must NOT be reclassified to [A] without Stratum I anchor.

### L4 — Uncertainty δγ = 0.0047 [OPEN / TENSION ALERT]

**Current evidence:** [A-] LO estimate.

**[TENSION ALERT]:**
- UIDT ledger: δγ = 0.0047
- NLO BMW/FRG estimate: δγ ≈ 0.0437
- Factor: ~9.3×

**Ticket:** TKT-20260403-FRG-NLO (open).

**Open research vector:**
- Vector B: Full NLO-FRG BMW/LPA' truncation [Evidence D]

**Constraint:** δγ = 0.0047 is an LO lower bound only.
Full NLO analysis required before uncertainty can be claimed as [A].

### L5 — v = 47.7 MeV Independence [OPEN]

**Current evidence:** [A] as calibration assignment (definitional).

**Status:** v = Δ*/γ is a definition. No independent first-principles
derivation of v exists. The limitation is structural:
until γ is derived independently, v cannot be predicted.

**Open research vector:**
- Contingent on L1 (Vector D or E above).

### Holographic / Topological Path [OPEN]

**Description:** Cheeger-inequality approach on orbit space A/G;
AdS/Yang–Mills correspondence for Δ*.
See `holographic_bh_ym_correspondence.md`.

**Evidence:** [E] speculative. Vector A in no-go audit.
**Status:** Not attempted.

### Schwinger Mechanism as γ Source [OPEN]

**Description:** Dynamic mass generation via Schwinger mechanism
as origin of γ scaling.
See `schwinger_mechanism_deep_research_2026-03-30.md`.

**Evidence:** [E] speculative. Vector C in no-go audit.
**Status:** Partial investigation only.

---

## Immutable Ledger Reference

The following constants are ground truth and must not be modified
without explicit maintainer confirmation:

| Constant | Value | Evidence | Notes |
|----------|-------|----------|-------|
| Δ* | 1.710 ± 0.015 GeV | [A] | Yang–Mills spectral gap; NOT a particle mass |
| γ | 16.339 | [A-] | Phenomenological kinetic vacuum parameter |
| γ∞ | 16.3437 | [A-] | Asymptotic value |
| δγ | 0.0047 | [A-] | LO uncertainty only; NLO open |
| v | 47.7 MeV | [A] | Definitional: v = Δ*/γ |
| w0 | −0.99 | [C] | Calibrated cosmology |
| ET | 2.44 MeV | [C] | Calibrated cosmology |
| **λS** | **5/12 (exact)** | **[A]** | **RG identity; replaces rounded 0.417** |
| κ | 1/2 (exact) | [A] | From 5κ²=3λS with λS=5/12 |
