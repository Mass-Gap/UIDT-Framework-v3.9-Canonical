# Wilson Flow Constants Registration — OT-1, OT-2, OT-3

**Purpose:** Pre-merge prerequisite documentation for [PR #190](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/pull/190)
(Wilson Flow & Topological Susceptibility Audit).

**Status:** Draft — awaiting PI review and CONSTANTS.md / CLAIMS.json integration.

---

## OT-1: C_GLUON — Gluon Condensate

### Proposed CONSTANTS.md Entry

```markdown
### C_GLUON — Gluon Condensate \u27e8(α_s/π) G²\u27e9

| Field | Value |
|---|---|
| Symbol | C_SVZ |
| Value | 0.012 GeV⁴ |
| Evidence | E (external phenomenological) |
| Source | Shifman, Vainshtein, Zakharov (SVZ 1979) |
| DOI | 10.1016/0550-3213(79)90022-1 |
| Ledger status | External — NOT a UIDT Ledger constant |
| Notes | Used only in verify_wilson_flow_topology.py for χ_top SVZ estimate. Do NOT promote to [A-] without first-principles UIDT derivation. |
```

### Rationale
C_GLUON = 0.012 GeV⁴ is the standard SVZ sum rules value from 1979. It appears in the corrected SVZ formula:

```
χ_top = (b0 / (32π²)) * ⟨(α_s/π) G²⟩
```

where b0 = 11 N_c / 3 = 11 for SU(3). This yields χ_top^{1/4} ≈ 107 MeV [Evidence D, TENSION ALERT z~16σ vs lattice band].

> ⚠️ C_GLUON is NOT part of the UIDT immutable parameter ledger (Δ*, γ, v, E_T, w0).
> It must never be treated as a first-principles UIDT prediction.

---

## OT-2: α_s(\u03bc) — Strong Coupling Reference Scale

### Proposed CONSTANTS.md Entry

```markdown
### ALPHA_S_REF — Strong Coupling at Reference Scale

| Field | Value |
|---|---|
| Symbol | ALPHA_S_REF |
| Value | 0.30 |
| Scale | μ ~ 1 GeV |
| Evidence | E (external PDG running) |
| Source | PDG 2024, running α_s at μ = 1 GeV |
| DOI | 10.1093/ptep/ptac097 (PDG 2022 review) |
| Ledger status | External — NOT a UIDT Ledger constant |
| Notes | Used only in verify_wilson_flow_topology.py for χ_top NLO estimate. Value is scheme-dependent (MSbar). Do NOT promote to [A-]. |
```

### Rationale
α_s(1 GeV) ≈ 0.30 is a standard PDG reference value. It enters the Wilson flow / topological susceptibility estimate as an external input. NLO correction (OT-4) will require a running α_s(μ) implementation.

> ⚠️ ALPHA_S_REF is NOT part of the UIDT immutable parameter ledger.

---

## OT-3: Topological Claims UIDT-C-TOPO-01/02/03

### Proposed CLAIMS.json Entries

```json
{
  "id": "UIDT-C-TOPO-01",
  "statement": "Wilson flow scale t0^{1/2} from UIDT: t0^{1/2} = hbar*c / Delta* = (197.3 MeV fm) / (1710 MeV) = 0.1154 fm",
  "evidence": "D",
  "stratum": "III",
  "source": "verification/scripts/verify_wilson_flow_topology.py",
  "notes": "Continuum estimate only. No discrete link variable simulation. Not equivalent to lattice t0 measurements.",
  "external_crosscheck": false,
  "tension_alert": false
},
{
  "id": "UIDT-C-TOPO-02",
  "statement": "Topological susceptibility estimate chi_top^{1/4} ~ 107 MeV via corrected SVZ formula with b0=11 (SU3)",
  "evidence": "D",
  "stratum": "III",
  "source": "verification/scripts/verify_wilson_flow_topology.py",
  "notes": "[TENSION ALERT] z ~ 16 sigma vs lattice band (170-200 MeV). Category D pending NLO correction (OT-4). Requires C_GLUON [E] and ALPHA_S_REF [E] as external inputs.",
  "external_crosscheck": true,
  "tension_alert": true,
  "tension_value": "z ~ 16 sigma vs quenched SU3 lattice band"
},
{
  "id": "UIDT-C-TOPO-03",
  "statement": "SVZ formula pre-factor b0 = 11*N_c/3 = 11 for SU(3) pure YM (corrected from earlier alpha_s/64pi^2 version)",
  "evidence": "E",
  "stratum": "III",
  "source": "SVZ 1979, DOI: 10.1016/0550-3213(79)90022-1",
  "notes": "Formula correction applied in PR #190 review 2026-03-30 (C1/C2 fix). Previous formula was incorrect.",
  "external_crosscheck": true,
  "tension_alert": false
}
```

---

## OT-5: Version Bump Coordination

Once OT-1 through OT-4 are merged, `CONSTANTS.md` header must be updated:

```
## UIDT Framework v3.9.5 — CONSTANTS
Last updated: 2026-03-30
Changelog: Added C_GLUON [E], ALPHA_S_REF [E]; registered UIDT-C-TOPO-01/02/03
```

> OT-4 (NLO α_s correction to χ_top formula) requires separate implementation PR.
> Version bump to v3.9.5 should only be executed after OT-4 is resolved.

---

## Pre-flight Checklist

- [x] No `float()` usage introduced
- [x] No `mp.dps` precision changes
- [x] No RG constraint modifications
- [x] No deletion > 10 lines in `/core` or `/modules`
- [x] Ledger constants unchanged (Δ*, γ, v, E_T, w0)
- [x] Documentation only — zero physics code touched
- [x] C_GLUON and ALPHA_S_REF tagged [E], not Ledger constants
- [x] TENSION ALERT for UIDT-C-TOPO-02 documented honestly
- [x] DOIs verified (SVZ 1979, PDG 2022)

---

## Claims Table (PR Gate)

| ID | Statement | Category | Source |
|---|---|---|---|
| OT-REG-01 | C_GLUON = 0.012 GeV⁴ registered as external [E] parameter | E | SVZ 1979, DOI: 10.1016/0550-3213(79)90022-1 |
| OT-REG-02 | ALPHA_S_REF = 0.30 at μ~1 GeV registered as external [E] parameter | E | PDG 2024 |
| OT-REG-03 | UIDT-C-TOPO-01/02/03 registered in CLAIMS.json | D/E | verify_wilson_flow_topology.py |

---

## Reproduction Note

```bash
# Verify PR #190 script still runs after constants registration:
python verification/scripts/verify_wilson_flow_topology.py
# Expected: [TENSION ALERT] Category D, chi_top^{1/4} ~ 107 MeV, z ~ 16 sigma
```

---

## DOI / arXiv Resolvability

| Reference | Identifier | Status |
|---|---|---|
| SVZ 1979 | DOI: 10.1016/0550-3213(79)90022-1 | ✓ resolves |
| PDG 2022 | DOI: 10.1093/ptep/ptac097 | ✓ resolves |
| PR #190 (Wilson Flow Audit) | GitHub: Mass-Gap/UIDT-Framework-v3.9-Canonical/pull/190 | ✓ resolves |

---

*P. Rietz — UIDT Framework v3.9 — CC BY 4.0 — DOI: 10.5281/zenodo.17835200*
*Pre-merge prerequisite for PR #190. Do not merge before OT-4 NLO implementation.*
