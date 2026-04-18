# LEDGER Addendum: UIDT-C-054 to UIDT-C-056

**Status:** Proposed — pending canonical review before merge into LEDGER/CLAIMS.json

> These claims are proposed at E-open and must pass the validation workflow
> in EVIDENCE_SYSTEM.md before integration into the canonical CLAIMS.json.
> No existing claim is modified by this addendum.

---

## UIDT-C-054

```json
{
  "id": "UIDT-C-054",
  "statement": "Gradient bilinear [∂_μ S ∂_ν S]_R as candidate metric seed in emergent geometry",
  "type": "hypothesis",
  "status": "proposed",
  "evidence": "E",
  "confidence": 0.50,
  "dependencies": ["UIDT-C-001", "UIDT-C-002", "UIDT-C-018"],
  "since": "v3.9.4",
  "notes": "Operator mixing under RG must be controlled. Positive-definiteness not yet shown. Links to open question OQ-G2 (factor-10 normalisation). Source: docs/emergent_geometry_section7.md §7.3.",
  "falsification": "If operator mixing under the ERG destroys positive-definiteness of g_{μν}^{info} at all renormalisation scales μ, claim is refuted."
}
```

---

## UIDT-C-055

```json
{
  "id": "UIDT-C-055",
  "statement": "Information-geometric distance d²(x,y) = -log(G_R(x,y;μ)/G_R(μ)) induces a Lorentz metric of signature (1,3)",
  "type": "hypothesis",
  "status": "proposed",
  "evidence": "E",
  "confidence": 0.45,
  "dependencies": ["UIDT-C-054", "UIDT-C-016"],
  "since": "v3.9.4",
  "notes": "Lorentz signature (1,3), positivity on spacelike separations, causal structure, and UV short-distance limit y→x are all undemonstrated. Cutoff- and scheme-dependence per [PTEP 2018, 023B02]. Links to OQ-G4. Source: docs/emergent_geometry_section7.md §7.3.",
  "falsification": "If signature (1,3) cannot be recovered from G_R at any renormalisation scale within UIDT truncation, claim is refuted."
}
```

---

## UIDT-C-056

```json
{
  "id": "UIDT-C-056",
  "statement": "A renormalisation reference scale μ is required for dimensional consistency of g_{μν}^{info}; μ is not yet canonically registered in CONSTANTS.md",
  "type": "constraint",
  "status": "proposed",
  "evidence": "E",
  "confidence": 0.90,
  "dependencies": ["UIDT-C-018", "UIDT-C-001"],
  "since": "v3.9.4",
  "notes": "Corrects dimensional inconsistency in naive ansatz g_{μν} ~ (1+Δ*²)δ_{μν} where Δ* has dimension GeV. Requires Δ*²/μ² for dimensionless metric factor. Candidate μ=Δ* is circular unless independently derived. HIGHEST PRIORITY for canonical registration. Links to OQ-G3. Source: docs/emergent_geometry_section7.md §7.3.",
  "falsification": "If no μ exists such that g_{μν}^{info} is dimensionless and background-independent, dimensional consistency of the ansatz fails."
}
```

---

## Ledger Impact Summary

| Field | Before | After merge |
|-------|--------|-------------|
| Total claims | 55 | 58 |
| Category E (open) | 12 | 15 |
| Existing claims modified | — | **None** |
| Constants modified | — | **None** |

---

*Proposed: 2026-04-04 | Author: P. Rietz | Review required before CLAIMS.json update*

---

## NLO-FRG Topological Susceptibility Update (TKT-20260417-WP1-NLO-FRG)

> **Date:** 2026-04-18 | **Script:** `verification/scripts/nlo_frg_topological_susceptibility.py`

The χ_top tension documented in `UIDT-C-TOPO-01` has been re-evaluated
using NLO corrections from three independent enhancement channels:

| Channel | Factor | Source |
|---------|--------|--------|
| Perturbative NLO | F_NLO = 1.350 | 1 + (α_s/π) · b₀/3, [5] |
| Anomalous Scaling | F_η = 1.125 | (Δ*/Λ_QCD)^{η_*}, UIDT-C-070 |
| Dyson Resummation | F_Dyson = 1.279 | (1 + w_g_phys)³, GAP_ANALYSIS_CLAY.md |
| **Combined** | **F_total = 1.943** | Product of three channels |

**Result:**

| Metric | LO (before) | NLO (after) |
|--------|-------------|-------------|
| χ_top^{1/4} | 142.98 MeV | 168.81 MeV |
| z-score (min, vs Cè 2015) | ~8.4σ | **3.24σ** |
| z-score (max, vs Del Debbio 2004) | ~9.6σ | 4.44σ |
| Category A gates | PASS | PASS |

**Assessment:** The NLO correction reduces the tension from ~8-16σ → ~3.2-4.4σ.
This is a dramatic improvement but does **not** yet reach the Category B threshold (z < 2).
Status: **UNDER TENSION (CONTROLLED)** — further reduction requires full momentum-dependent
vertex projection (GAP-FRG-001).

> C-056 in CLAIMS.json is already reframed as EFT correction via PR #303 (v3.9.7).
> C-096 (NLO-RG conjecture, [E]) is registered.
> C-TOPO-01 remains Category D with CONTROLLED tension annotation.

---

## OPUS Advisory: Claim-ID Namespace (2026-04-05)

> **FOR OPUS / PI REVIEW:**
>
> The OPUS-001 audit flagged a potential collision between:
> - **UIDT-C-054, C-055, C-056** (this addendum — emergent geometry claims)
> - **UIDT-C-TOPO-01, C-TOPO-02, C-TOPO-03** (Wilson flow, PR #190)
>
> **Resolution:** No collision exists. The Wilson flow claims use a **TOPO-**
> prefixed namespace (`UIDT-C-TOPO-01/02/03`), while the geometry claims
> use the standard **numeric** namespace (`UIDT-C-054/055/056`).
>
> These are orthogonal claim families:
> - **C-054–056:** Emergent geometry (gradient bilinear, distance functional, μ scale)
> - **C-TOPO-01–03:** Topological susceptibility (χ_top vs. lattice, Δ* anchor, C_SVZ)
>
> **Action required:** When integrating into CLAIMS.json, confirm that the
> TOPO namespace is maintained as a separate claim series (not mapped to
> numeric IDs). This prevents future collisions if additional geometry
> claims enter the C-057+ range.
