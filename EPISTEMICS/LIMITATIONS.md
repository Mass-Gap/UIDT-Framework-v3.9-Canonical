# Known Limitations of UIDT v3.9

**Maintainer: P. Rietz**  
**Last reviewed: 2026-05-10**

All limitations are classified by stratum and evidence category.  This list is authoritative;
partial lists in individual documents defer to this file.

---

| ID | Description | Stratum | Evidence | Open task / milestone |
|----|-------------|---------|----------|-----------------------|
| L1 | Electron mass residual: UIDT does not predict me from first principles | III | D | — |
| L2 | γ = 16.339 is phenomenological; no first-principles derivation from S(x) | II–III | A− | — |
| L3 | Cosmological calibration (w₀, ET) uses observational priors; not a genuine prediction | II–III | C | DESI Kill-switch K4 |
| L4 | Photonic n_crit prediction untested experimentally | III | D | Kill-switch K5 |
| L5 | Casimir anomaly at 0.66 nm has not been measured; feasibility uncertain | III | D | Kill-switch K3 |
| L6 | LLM audits do not substitute for independent peer review | II | — | See INDEPENDENT_REPRODUCTION_PROTOCOL.md |
| L7 | No direct operationalisation of S(x) as a local field value | III | D | See OPERATIONAL_S_FIELD.md |
| L8 | Scheme independence of Δ* not verified beyond MS-bar | II–III | D | See RG_SCHEME_SENSITIVITY.md |
| L9 | Continuum mathematics not derived from discrete information ontology | III | E | See SCOPE_AND_NON_SCOPE.md |
| L10 | Bekenstein–Hawking entropy S = A/4 not reproduced | III | E | See SCOPE_AND_NON_SCOPE.md |
| L11 | SU(3) gauge group assumed, not derived from UIDT information geometry | III | E | See SCOPE_AND_NON_SCOPE.md |
| L12 | Clay committee recognition absent; constructive candidate only | II–III | D | See CLAY_COMPLIANCE_STATUS.md |

---

## Usage Rule

Any document in this repository that makes a quantitative claim must either:
1. Reference a limitation from this table that bounds the claim, **or**
2. Carry an Evidence category that already encodes the limitation (e.g., Evidence D = prediction).

Violations must be flagged in PR review under checklist item C-LIM.
