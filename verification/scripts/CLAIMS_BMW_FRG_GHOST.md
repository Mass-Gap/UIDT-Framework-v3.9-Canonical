# Claims Table: BMW-FRG Ghost-Propagator Z_c(k) + Decoupling-BC

**Component:** `bmw_frg_ghost_decoupling.py`  
**Branch:** `feature/bmw-frg-ghost-decoupling-bc`  
**Depends on:** `feature/bmw-frg-ode-phase2-simplified`  
**Flags:** `[GHOST_SECTOR_FLAG]` `[GRIBOV_NOT_IMPL]` `[EVIDENCE_D]`

---

## Claims

| ID   | Claim                                                                 | Category | Source / Notes                              |
|------|-----------------------------------------------------------------------|----------|---------------------------------------------|
| G-01 | `Z_c(k→0) > 0` — Decoupling boundary condition holds                | [D]      | This PR; prediction                         |
| G-02 | Litim threshold `p_c = 1/4` is analytically exact in d=4            | [A]      | Direct calculation from Litim regulator     |
| G-03 | `Z_c(IR)` compatible with Bogolubsky et al. Lattice-QCD (qualitative)| [B]      | arXiv:0901.0736 — lattice large-volume data |
| G-04 | Ghost contribution `eta_c` modifies Phase-2 gluon anomalous dim `eta_A` | [D]   | Prediction; quantification deferred Phase 3 |
| G-05 | Scaling solution (`Z_c→0`) is **not** implemented; flagged explicitly | —        | [GRIBOV_NOT_IMPL]                           |

---

## Evidence Categories (UIDT)

| Symbol | Meaning                              |
|--------|--------------------------------------|
| [A]    | Mathematically proven                |
| [A-]   | Phenomenological parameter           |
| [B]    | Lattice compatible                   |
| [C]    | Calibrated cosmology                 |
| [D]    | Prediction                           |
| [E]    | Speculative                          |

---

## Affected Ledger Constants

No ledger constants modified. Read-only references:

| Constant  | Value               | Evidence | Role in this PR               |
|-----------|---------------------|----------|--------------------------------|
| Δ*        | 1.710 ± 0.015 GeV  | [A]      | Reference scale only           |
| γ         | 16.339             | [A-]     | Not entered into ghost ODE     |
| v         | 47.7 MeV           | [A]      | Not entered into ghost ODE     |

---

## Open Flags

```
[GHOST_SECTOR_FLAG]  g²(k) = const in this PR.
                     Full coupling to beta_g function deferred to Phase 3.

[GRIBOV_NOT_IMPL]   Gribov-horizon condition not implemented.
                     Decoupling-BC (Z_c(IR) > 0) used as Gribov-free proxy.
                     Gribov-Zwanziger extension is a separate future PR.

[EVIDENCE_D]        All Z_c trajectory outputs are predictions.
                     External lattice calibration requires Phase 3.
```

---

## Reproduction

One-command verification:

```bash
# Smoke test (standalone)
python verification/scripts/bmw_frg_ghost_decoupling.py

# Full pytest suite
python -m pytest verification/tests/test_ghost_decoupling_bc.py -v
```

Expected output (smoke test):

```
p_c == 1/4 verified: residual < 1e-14 [PASS]
Decoupling BC Z_c(IR) > 0: [PASS]
Smoke test complete.
```

---

## DOI / arXiv Resolvability

| Reference                          | Identifier         | Status   |
|------------------------------------|--------------------|----------|
| Bogolubsky et al. (Lattice ghosts) | arXiv:0901.0736    | Verifiable |
| Boucaud et al. (Decoupling sol.)   | arXiv:0803.2161    | Verifiable |
| Wetterich equation                 | Phys.Lett.B 301 (1993) 90 | DOI: 10.1016/0370-2693(93)90726-X |

> [SEARCH_FAIL] arXiv identifiers listed above are standard references;
> live DOI resolution not performed in this PR. Maintainer should verify
> before merging to main.
