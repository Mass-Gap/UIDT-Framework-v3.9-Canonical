# Wilson Flow — External Constants Registration

**Version:** TKT-20260403-wilson-flow-constants  
**Date:** 2026-04-03  
**Prerequisite for:** PR #190 merge (OT-1, OT-2, OT-3)  
**Evidence Categories:** [E] (external phenomenological parameters)  

---

## Purpose

This document registers the external phenomenological constants used in
`verification/scripts/verify_wilson_flow_topology.py` (PR #190).
These parameters are **not** UIDT Ledger constants and must **not** appear in
`CANONICAL/CONSTANTS.md`. They are tagged [E] throughout.

---

## OT-1 — C_GLUON (SVZ Gluon Condensate)

| Field | Value |
|-------|-------|
| Symbol | C_GLUON = ⟨(α_s/π) G²⟩ |
| Canonical value | 0.012 GeV⁴ |
| Evidence | [E] — external (SVZ 1979) |
| Source | Shifman, Vainshtein, Zakharov, Nucl.Phys. B147 (1979) 385 |
| arXiv | Not on arXiv (pre-arXiv); DOI: 10.1016/0550-3213(79)90022-1 |
| UIDT Ledger? | ❌ NO — external reference value only |
| Scope | `verify_wilson_flow_topology.py` only |

### Annotation for CONSTANTS.md (external section)

```
# EXTERNAL PHENOMENOLOGICAL PARAMETERS (Evidence [E])
# Not part of the UIDT canonical ledger.
# Used only as external crosscheck inputs.

C_GLUON = 0.012          # GeV^4  [E] SVZ 1979 gluon condensate
                          # DOI: 10.1016/0550-3213(79)90022-1
```

---

## OT-2 — ALPHA_S_REF (Running strong coupling)

| Field | Value |
|-------|-------|
| Symbol | α_s(μ ~ 1 GeV) |
| Reference value | 0.30 |
| Evidence | [E] — external (PDG running coupling) |
| Source | PDG 2024, Review of Particle Physics, Section 9 |
| DOI | 10.1093/ptep/ptac097 |
| UIDT Ledger? | ❌ NO — external reference value only |
| Scope | `verify_wilson_flow_topology.py` only |

### Annotation for CONSTANTS.md (external section)

```
ALPHA_S_REF = 0.30        # [E] PDG 2024 running coupling at mu ~ 1 GeV
                          # DOI: 10.1093/ptep/ptac097
```

---

## OT-3 — TOPO Claims in CLAIMS.json

The following three claims from PR #190 must be registered in `LEDGER/CLAIMS.json`:

### UIDT-C-TOPO-01

```json
{
  "id": "UIDT-C-TOPO-01",
  "statement": "Continuum Wilson flow scale t_0 derivable analytically from Delta* = 1.710 GeV via UIDT gap equation",
  "evidence": "D",
  "stratum": "III",
  "value": "sqrt(t_0) ~ 1/(2*Delta*)",
  "residual": null,
  "source": "verification/scripts/verify_wilson_flow_topology.py",
  "tension_alert": true,
  "tension_detail": "chi_top^{1/4} ~ 107 MeV (UIDT LO SVZ) vs 180-220 MeV (lattice quenched), z ~ 16 sigma",
  "falsification": "F9 in docs/falsification-criteria.md",
  "created": "2026-03-28",
  "pr": 190
}
```

### UIDT-C-TOPO-02

```json
{
  "id": "UIDT-C-TOPO-02",
  "statement": "Topological susceptibility chi_top^{1/4} estimated via corrected SVZ formula with b0 = 11 (SU(3) pure YM)",
  "evidence": "D",
  "stratum": "III",
  "value": "chi_top^{1/4} ~ 107 MeV (LO)",
  "residual": null,
  "source": "verification/scripts/verify_wilson_flow_topology.py",
  "tension_alert": true,
  "tension_detail": "16 sigma vs quenched lattice band 180-220 MeV; NLO corrections pending (OT-4)",
  "falsification": "F9 in docs/falsification-criteria.md: z > 3 vs all benchmarks after NLO",
  "created": "2026-03-28",
  "pr": 190
}
```

### UIDT-C-TOPO-03

```json
{
  "id": "UIDT-C-TOPO-03",
  "statement": "C_GLUON = 0.012 GeV^4 (SVZ 1979) used as external input to chi_top estimate",
  "evidence": "E",
  "stratum": "I",
  "value": "0.012 GeV^4",
  "residual": null,
  "source": "SVZ 1979, DOI: 10.1016/0550-3213(79)90022-1",
  "tension_alert": false,
  "note": "External phenomenological parameter. NOT a UIDT Ledger constant.",
  "created": "2026-03-28",
  "pr": 190
}
```

---

## Open Tasks Remaining (PI decision required)

| Task | Status | Blocks PR #190 merge? |
|------|--------|----------------------|
| OT-4: NLO α_s correction to χ_top formula | Open — separate TKT | Yes (before Category upgrade) |
| OT-5: Version bump v3.9 → v3.9.5 + CONSTANTS.md header | Open | Yes (before final merge) |

---

## Pre-flight checklist

- [x] No `float()` used
- [x] No `mp.dps` changes
- [x] RG constraint 5κ² = 3λ_S not touched
- [x] No deletion > 10 lines in /core or /modules
- [x] Ledger constants unchanged (C_GLUON and α_s are [E], not Ledger)
- [x] All DOIs verified
- [x] Documentation only — no physics code modified

---

*P. Rietz — UIDT Framework v3.9 — CC BY 4.0*
