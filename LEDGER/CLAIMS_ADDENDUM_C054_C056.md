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
