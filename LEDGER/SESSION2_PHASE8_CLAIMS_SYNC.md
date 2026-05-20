# Session-2 Phase-8 Claims Sync

> **UIDT Framework:** v3.9 Canonical  
> **Branch:** `TKT-2026-05-17-session2-ledger-sync-phase8`  
> **Date:** 2026-05-17  
> **DOI:** `10.5281/zenodo.17835200`  
> **Status:** Ledger-sync staging document. This file does **not** promote evidence categories and does **not** close L1/L4/L5.  
> **Guardian status:** `GUARDIAN_REVIEW_REQUIRED` because this document stages claims under `LEDGER/`; no direct `CLAIMS.json` mutation is performed.

---

## Purpose

This document stages the Session-2 / Phase-8 claims that must be reviewed before integration into `LEDGER/CLAIMS.json`. It exists because `LEDGER/CLAIMS.json` has a recent recovery history and should not be blindly rewritten without explicit review.

The changes are append-only at the claim level:

1. Correct the Session-2 bare-gamma formula.
2. Recompute `k_crit = 4πE_T` using the canonical `E_T = 2.44 MeV`.
3. Register the S4-P1 gamma-chain as [D] / Stratum III only.
4. Register `[NO-GO-STEP5]` as a documented limitation of the LPA' NLO path.

---

## Guardian / SSOT Gate

This file is intentionally a staging document rather than a direct edit of `LEDGER/CLAIMS.json`.

| Gate | Status | Rationale |
|---|---|---|
| Reviewer | Required | The staged claims touch the evidence ledger surface. |
| Regressor | Required | `python verification/scripts/verify_session2_phase8_sync.py` must pass before any claim migration. |
| Auditor | Required | Evidence tags must remain [D] / Stratum III; no [A], [B], or [C] promotion is requested. |

**Merge condition:** Before any migration into `LEDGER/CLAIMS.json`, the Guardian chain must explicitly return PASS for Reviewer, Regressor, and Auditor. A single failure blocks migration.

---

## Critical Corrections

### C1 — Bare-gamma denominator correction

Incorrect handover expression:

```text
γ_bare = (2Nc+1)^2 / Nc^2
```

For `Nc = 3`, this gives `49/9 = 5.444...`, not `49/3`.

Correct Session-2 expression:

```text
γ_bare(Nc) = (2Nc+1)^2 / Nc
γ_bare(3) = 49/3 = 16.333333333333...
```

Evidence status: **[D] Stratum III**. This is a conjectural algebraic identification, not an [A] derivation.

### C2 — Tachyon threshold numerical correction

With canonical `E_T = 2.44 MeV [C]`:

```text
k_crit = 4πE_T
       = 30.6619442990363820073953994208079481497643733379010328127154592209242881253534 MeV
```

The historical value `30.707 MeV` implies:

```text
E_T = 30.707 / (4π) = 2.4435854187... MeV
```

Therefore `30.707 MeV` must not be recorded as exact for `E_T = 2.44 MeV`.

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|---|
| UIDT-S2-001 | Bare-gamma conjecture | γ_bare(Nc)=((2Nc+1)^2)/Nc; γ_bare(3)=49/3 | [D] | III | PR #367 / Phase-8 intake | Staged | Reject if Δγ correction is negative, >0.012, or SU(4) scaling fails. |
| UIDT-S2-002 | Required positive correction | Δγ_required=17/3000=0.005666666666... | [D] | III | PR #367 / verification script | Staged | Reject L1 ansatz if first-principles Δγ is negative or outside acceptance band. |
| UIDT-S4P1-001 | Tachyon threshold with canonical E_T | k_crit=4πE_T=30.6619442990... MeV | [D] | III | PR #369 / corrected numerical audit | Staged | Fails if regulator-independent Wetterich trace does not reproduce onset within E_T uncertainty. |
| UIDT-S4P1-002 | S4-P1 induced VEV | v_S4P1=sqrt(12/5)·k_crit=47.5012798530... MeV | [D] | III | PR #369 / corrected numerical audit | Staged | Fails if the full flow cannot recover canonical v=47.7 MeV within uncertainty. |
| UIDT-S4P1-003 | Non-perturbative gamma shift | Δγ_NP=0.00562910631489145... | [D] | III | PR #369 / corrected numerical audit | Staged | Fails if full Wetterich flow gives incompatible Δγ_NP. |
| UIDT-S4P1-004 | S4-P1 gamma prediction | γ_pred=16.338962439648224... | [D] | III | PR #369 / corrected numerical audit | Staged | Fails if regulator-independence or full flow shifts γ_pred outside the calibration band. |
| UIDT-S5-001 | `[NO-GO-STEP5]` LPA' NLO physical path | Z_phi(IR, λ3_phys)=1.0000019 ≠ γ | [D] | III | PR #362 | Staged | Overturned only by independently reproduced LPA'+Y/BMW derivation from physical λ3. |

---

## Proposed CLAIMS.json Append Entries

```json
[
  {
    "id": "UIDT-S2-001",
    "statement": "Bare gamma conjecture gamma_bare(Nc) = (2Nc+1)^2/Nc, giving gamma_bare(3) = 49/3 = 16.333333333333...",
    "type": "hypothesis",
    "status": "conjectured",
    "evidence": "D",
    "confidence": 0.55,
    "dependencies": ["UIDT-C-002", "UIDT-C-052", "PR-367"],
    "since": "v3.9-session2-phase8",
    "stratum": "III",
    "notes": "Correct Session-2 denominator is Nc, not Nc^2. The Nc^2 denominator yields 49/9 for SU(3) and is rejected. This does not upgrade gamma beyond [A-].",
    "falsification": "If the required Delta_gamma correction is negative, exceeds 0.012, or SU(4) scaling fails the (2Nc+1)^2/Nc structure."
  },
  {
    "id": "UIDT-S2-002",
    "statement": "Required correction Delta_gamma_required = gamma_ledger - gamma_bare = 17/3000 = 0.005666666666...",
    "type": "derivation",
    "status": "open",
    "evidence": "D",
    "confidence": 0.5,
    "dependencies": ["UIDT-S2-001", "UIDT-C-002", "PR-367"],
    "since": "v3.9-session2-phase8",
    "stratum": "III",
    "notes": "Positive correction required to connect gamma_bare=49/3 to gamma=16.339 [A-]. No first-principles 1-loop computation exists yet.",
    "falsification": "If a first-principles 1-loop or FRG correction gives Delta_gamma < 0 or Delta_gamma > 0.012, the L1 bare-gamma ansatz is rejected."
  },
  {
    "id": "UIDT-S4P1-001",
    "statement": "S4-P1 critical scale k_crit = 4*pi*E_T = 30.6619442990... MeV for E_T = 2.44 MeV.",
    "type": "derivation",
    "status": "conjectured",
    "evidence": "D",
    "confidence": 0.55,
    "dependencies": ["UIDT-C-044", "PR-369"],
    "since": "v3.9-session2-phase8",
    "stratum": "III",
    "notes": "Numerical tachyon-threshold chain. The historical 30.707 MeV value implies E_T≈2.443585 MeV and must not be presented as exact for E_T=2.44 MeV.",
    "falsification": "If regulator-independence checks fail or the full Wetterich trace does not reproduce the onset within the E_T uncertainty band."
  },
  {
    "id": "UIDT-S4P1-002",
    "statement": "S4-P1 induced VEV v_S4P1 = sqrt(12/5)*k_crit = 47.5012798530... MeV using E_T=2.44 MeV.",
    "type": "derivation",
    "status": "conjectured",
    "evidence": "D",
    "confidence": 0.55,
    "dependencies": ["UIDT-S4P1-001", "UIDT-C-004", "PR-369"],
    "since": "v3.9-session2-phase8",
    "stratum": "III",
    "notes": "Research-chain value only. Canonical v=47.7 MeV [A] remains unchanged.",
    "falsification": "If the full flow cannot recover canonical v=47.7 MeV within uncertainty without free-parameter insertion."
  },
  {
    "id": "UIDT-S4P1-003",
    "statement": "S4-P1 non-perturbative gamma shift Delta_gamma_NP = (Nc^2-1)/(4*pi^2)*v_S4P1/Delta* = 0.00562910631489145...",
    "type": "prediction",
    "status": "predicted",
    "evidence": "D",
    "confidence": 0.55,
    "dependencies": ["UIDT-S4P1-002", "UIDT-C-001", "PR-369"],
    "since": "v3.9-session2-phase8",
    "stratum": "III",
    "notes": "Uses Nc=3, Delta*=1.710 GeV, and v_S4P1 in MeV. This is not an algebraic proof.",
    "falsification": "If full Wetterich flow gives incompatible Delta_gamma_NP."
  },
  {
    "id": "UIDT-S4P1-004",
    "statement": "S4-P1 gamma prediction gamma_pred = 16.338962439648224... from gamma_bare + Delta_gamma_NP.",
    "type": "prediction",
    "status": "predicted",
    "evidence": "D",
    "confidence": 0.55,
    "dependencies": ["UIDT-S2-001", "UIDT-S4P1-003", "UIDT-C-002", "PR-369"],
    "since": "v3.9-session2-phase8",
    "stratum": "III",
    "notes": "Suggestive numerical proximity to gamma=16.339 [A-]. Does not upgrade gamma beyond [A-].",
    "falsification": "If full Wetterich flow or regulator-independence checks shift gamma_pred outside the gamma calibration band."
  },
  {
    "id": "UIDT-S5-001",
    "statement": "[NO-GO-STEP5]: LPA' NLO with physical lambda3(UV)=0.034823 yields Z_phi(IR)=1.0000019, not gamma=16.339.",
    "type": "no-go",
    "status": "verified",
    "evidence": "D",
    "confidence": 0.8,
    "dependencies": ["PR-362", "verification/scripts/research/verify_frg_step5_lambda3_flow.py"],
    "since": "v3.9-session2-phase8",
    "stratum": "III",
    "notes": "LPA' NLO alone cannot derive gamma. Shooting solution requires lambda3*=99.638, about 2857 times physical lambda3.",
    "falsification": "If an independently reproduced LPA'+Y or BMW truncation derives gamma from physical lambda3 without violating 5kappa^2=3lambda_S."
  }
]
```

---

## Reproduction Note

Single command:

```bash
python verification/scripts/verify_session2_phase8_sync.py
```

Expected result:

```text
[PASS] gamma_bare formula corrected residual: < 1e-70
[PASS] wrong denominator rejected as 49/9 residual: < 1e-70
[PASS] Delta_gamma_required = 17/3000 residual: < 1e-70
[PASS] k_crit = 4*pi*E_T for E_T=2.44 MeV residual: < 1e-70
[PASS] gamma_pred chain residual: < 1e-70
[PASS] RG constraint residual: 0.0
ALL SESSION-2 PHASE-8 SYNC CHECKS PASSED
```

---

## Verified References

| DOI/arXiv/PR | Status | Used for | Evidence Tag |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | Project DOI | UIDT canonical project identity | n/a |
| PR #367 | Repository-internal merged PR | γ_bare Session-2 derivation context | [D] |
| PR #369 | Repository-internal merged PR | S4-P1 tachyon-threshold chain | [D] |
| PR #362 | Repository-internal merged PR | `[NO-GO-STEP5]` | [D] |
| PR #358 | Repository-internal merged PR | L1/L4/L5 formal no-go context | [D/E context] |

No new external DOI/arXiv source is required for these staged claims. No claim is promoted to [B] or [C].

---

## Limitations

- L1 remains open: γ_bare is not an [A] derivation.
- L4 remains open: S4-P1 is a numerical chain, not a regulator-independent Wetterich proof.
- L5 remains open: N=99 is not derived in this sync.
- The value γ=16.339 remains [A-].
- The historical value `k_crit≈30.707 MeV` is not exact for `E_T=2.44 MeV`.
