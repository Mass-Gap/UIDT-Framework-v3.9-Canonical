# LEDGER Addendum: UIDT-C-070

**Status:** Proposed — pending canonical review before merge into LEDGER/CLAIMS.json  
**Date:** 2026-05-03  
**Source:** `docs/BH_geometry/israel_darmois_matching_2026-05-03.md`  
**Related PR:** TKT-20260503-israel-darmois-research-note-C070

> This claim is proposed at Evidence [D] and must pass the validation workflow
> before integration into the canonical CLAIMS.json.
> No existing claim is modified by this addendum.

---

## UIDT-C-070

```json
{
  "id": "UIDT-C-070",
  "statement": "FRW geometry is not reproducible as the interior metric of a UIDT black hole via Israel-Darmois junction conditions with the UIDT scalar condensate as source",
  "type": "constraint",
  "status": "proposed",
  "evidence": "D",
  "confidence": 0.90,
  "dependencies": [
    "UIDT-C-001",
    "UIDT-C-004",
    "UIDT-C-005",
    "UIDT-C-006"
  ],
  "since": "v3.9.5",
  "notes": "Derived via Israel-Darmois matching at r = r_c (static and dynamic boundary cases). Static case: MB-I-2 forces da/dtau = 0 (static universe, not expanding FRW). Dynamic case: [K_theta_theta] = 0 yields r_dot_c^2 = -r_S/r_c < 0 (no real solution). The consistent interior geometry in the potential-dominated regime (rho < 0.5) is Gravastar-type with Lambda_eff(r) = 8piG xi_S^2 (48)^2 G^4 M^4 / (lambda_S r^8), proportional to r^{-8}. NEC satisfied; SEC violated (mechanism for de-Sitter-type repulsion). The tau-redefinition ansatz used in prior UIDT BH work (tau ~ |S|^2) is not reproduced by the EFE. See docs/BH_geometry/israel_darmois_matching_2026-05-03.md for full derivation. Structural problem OQ-BH-003 (r_c >> r_S) remains open.",
  "falsification": "If a valid coordinate transformation exists mapping the derived Gravastar-type interior metric to a FRW metric via a diffeomorphism preserving the Israel-Darmois boundary conditions, claim is refuted. Alternatively, if a surface-layer scenario (S_ab != 0) yields consistent FRW matching, claim scope is reduced to the S_ab = 0 case."
}
```

---

## Associated Open Questions

```json
[
  {
    "id": "OQ-BH-001",
    "question": "Does Lambda_eff(r) proportional to r^{-8} regularise the central singularity at r = 0?",
    "evidence": "E",
    "dependencies": ["UIDT-C-070"],
    "notes": "Lambda_eff diverges as r -> 0. Singularity theorems assume SEC; SEC is violated here. Penrose theorem may not apply. Numerical GR required."
  },
  {
    "id": "OQ-BH-002",
    "question": "Full nonlinear EFE fixpoint system: G_munu = 8piG T^S_munu(S_0(R[g])) — does a self-consistent solution exist and what is its topology?",
    "evidence": "E",
    "dependencies": ["UIDT-C-070", "UIDT-C-001"],
    "notes": "Self-referential: S_0 depends on Kretschner scalar which depends on metric which is sourced by S_0. Requires numerical GR or fixed-point iteration."
  },
  {
    "id": "OQ-BH-003",
    "question": "The structural problem r_c >> r_S: does UIDT condensation occur outside the horizon, making it an extragalactic rather than black-hole-internal phenomenon?",
    "evidence": "D",
    "dependencies": ["UIDT-C-070", "UIDT-C-001", "UIDT-C-004"],
    "notes": "r_c/r_S ~ 10^7 to 10^11 for stellar to supermassive BHs. Condensation at r_c >> r_S is in the weak-field regime. This may require reinterpretation of the entire BH scenario."
  },
  {
    "id": "OQ-BH-004",
    "question": "Does a surface-layer (domain wall) scenario with S_ab != 0 at r_c permit consistent FRW matching?",
    "evidence": "E",
    "dependencies": ["UIDT-C-070"],
    "notes": "C-070 proves exclusion only for S_ab = 0 (no shell). A domain wall at r_c with non-zero surface tension might relax the matching constraints."
  }
]
```

---

## Ledger Impact Summary

| Field | Before | After merge |
|-------|--------|-------------|
| Total claims | 56+ | +1 |
| Category D (predicted) | — | +1 (C-070) |
| Existing claims modified | — | **None** |
| Constants modified | — | **None** |

---

*Proposed: 2026-05-03 | Author: P. Rietz | Review required before CLAIMS.json update*
