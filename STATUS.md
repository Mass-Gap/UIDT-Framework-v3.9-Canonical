# UIDT Framework — Current Status

> **Version:** 3.9 | **Status date:** 2026-05-20 | **DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

---

## Framework State at a Glance

| Dimension | Status |
|---|---|
| **Verification Suite** | Last documented baseline: 78/78 tests pass; current Phase-8 verifiers use local `mp.dps = 80` with explicit residual gates. |
| **Claims Registry** | Main-branch baseline: 60 claims in `LEDGER/CLAIMS.json`; Session-2 claims are staged in PR #459, not migrated. |
| **Evidence Distribution** | Main-branch baseline only until `CLAIMS.json` is explicitly updated through Guardian / SSOT review. |
| **Active Limitations** | L1, L2, L4, L5, L6-FRG remain active; L3 accepted. |
| **Latest Research State** | Phase-8 ledger sync, delta-gamma/SU(4) audit, and reconciliation audit are staged in PR #459 → #460 → #461. |
| **Cleanup Roadmap** | `docs/research/L1_L4_L5_roadmap_2026-05-08.md` is updated by the current cleanup branch. |

---

## Core Parameters (Read-Only)

```text
Δ* = 1.710 ± 0.015 GeV    [A]   Spectral gap (NOT particle mass)
γ  = 16.339                [A-]  Kinetic VEV calibration; NOT RG-derived
κ  = 0.500 ± 0.008         [A]   Non-minimal coupling
λ_S = 5κ²/3 = 0.41̄6̄      [A]   Exact RG fixed-point definition
v  = 47.7 MeV              [A]   Vacuum expectation value
m_S = 1.705 ± 0.015 GeV    [D]   Scalar mass prediction
E_T = 2.44 MeV             [C]   Torsion binding energy
H₀ = 70.4 ± 0.16 km/s/Mpc  [C]   DESI-calibrated; NOT a solved tension
```

---

## Open Limitations

| ID | Problem | Evidence | Next Step |
|---|---|---|---|
| **L1** | 10¹⁰ geometric factor remains first-principles open. | [D]/[E] surface | Define UV/IR scales precisely; test topology/holography paths. |
| **L2** | Electron mass residual remains open. | [E] / unresolved | Electroweak coupling integration. |
| **L4** | `γ = 16.339` is calibrated, not RG-derived. | [A-] for γ; [D] for derivation attempts | Explicit scalar self-energy `Π_S(p²)` and regulator-independent FRG audit. |
| **L5** | `N = 99` steps remain unjustified. | [D] | Resolve N-definition before SU(4) promotion attempts. |
| **L6-FRG** | Minimal FRG truncations are insufficient. | [D] | Full NLO/BMW/Dyson-resummed analysis after cleanup. |

---

## Recent Research Observations (No Evidence Promotion)

1. **Bare-gamma arithmetic:** `γ_bare(3) = (2N_c+1)^2/N_c = 49/3` is an exact arithmetic identity for `N_c=3`, but the physical UIDT identification remains a [D] Stratum III conjecture. It is not an [A] derivation of `γ = 16.339`.
2. **Required correction:** `Δγ_required = 17/3000` [D] is the required positive correction from `49/3` to `γ = 16.339` [A-]. It has not been derived from first principles.
3. **S4-P1 torsion threshold:** for canonical `E_T = 2.44 MeV` [C], define `k_T = 4πE_T = 30.6619442990... MeV` [D]. The historical `30.707 MeV` value implies a slightly different effective `E_T` and is not exact for `E_T = 2.44 MeV`.
4. **S4-P1 gamma chain:** `γ_pred = 16.338962439648224...` [D] is a partial numerical hit; residual to `γ = 16.339` is about `3.7560e-5`, therefore not [A].
5. **SU(4) tension:** `γ_bare(4) = 81/4 = 20.25` [D] is algebraically coherent, but `N_SU4 = 176` conflicts with the standard pure-YM beta-coefficient convention `N_SU4 = 704/3`. This remains `[TENSION ALERT]`.

---

## Symbol Discipline

| Symbol | Meaning | Status |
|---|---|---|
| `k_T` | Torsion-threshold scale `4πE_T ≈ 30.661944 MeV` for `E_T = 2.44 MeV` [C]. | Use for S4-P1 torsion chain. |
| `k_γ` | Gamma-emergent scale near `Δ*/γ ≈ 104.66 MeV` from D2-style inverse problems. | Use for D2 gamma-emergent threshold. |
| `k_crit` | Ambiguous legacy symbol. | Avoid unless context is explicitly stated. |

---

## Navigation

| What | Where |
|---|---|
| Full README | [`README.md`](./README.md) |
| Mathematical Formalism | [`FORMALISM.md`](./FORMALISM.md) |
| Canonical Constants | [`CANONICAL/CONSTANTS.md`](./CANONICAL/CONSTANTS.md) |
| Limitations | [`CANONICAL/LIMITATIONS.md`](./CANONICAL/LIMITATIONS.md) |
| Claims Registry | [`LEDGER/CLAIMS.json`](./LEDGER/CLAIMS.json) |
| Verification Suite | [`verification/`](./verification/) |
| Research Notes | [`docs/research/INDEX.md`](./docs/research/INDEX.md) |
| Active L1/L4/L5 Roadmap | [`docs/research/L1_L4_L5_roadmap_2026-05-08.md`](./docs/research/L1_L4_L5_roadmap_2026-05-08.md) |
| Reconciliation Audit | [`docs/research/L1_L4_L5_research_reconciliation_audit_2026-05-17.md`](./docs/research/L1_L4_L5_research_reconciliation_audit_2026-05-17.md) |
| Precision Addendum | [`docs/research/L1_L4_L5_precision_context_addendum_2026-05-20.md`](./docs/research/L1_L4_L5_precision_context_addendum_2026-05-20.md) |

---

## Governance Note

This status file reports the current documentation and research state. It does not authorize a merge, evidence-category promotion, or direct mutation of `LEDGER/CLAIMS.json`.

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609) | **License:** CC BY 4.0
