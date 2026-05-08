# AI Artifact Scan Report — Spring 2026 HJ Literature Integration
**Date:** 2026-04-30  
**Auditor:** UIDT Framework Automated Audit + PI Review  
**Scope:** Three Hamilton–Jacobi papers uploaded 2026-04-30  
**Protocol:** UIDT Paper Audit Protocol (Steps 1–4), UIDT Constitution §AI_ARTIFACT_SCAN

---

## Paper 1 — Zhang (2026), arXiv:2601.22697

### Step 1 — Authenticity Check
- **arXiv ID:** 2601.22697v2 [quant-ph], revised 10 Apr 2026
- **DOI:** 10.48550/arXiv.2601.22697 (arXiv preprint; no journal DOI yet)
- **Status:** RESOLVABLE via arxiv.org
- **Audit result:** **PASS**
- **AI Artifact flags (2024–2026 scrutiny applied):** None. Equations cross-checked against energy conservation; the HJS equation (Eq. 13) recovers HJ theory exactly at |κ|→0. No inconsistencies with renormalization constraints or UIDT parameter ledger.

### Step 2 — Epistemic Stripping
| Element | Content |
|---|---|
| Core equation | iκ ∂_t ψ = −(κ²/2m)∇²ψ + Vψ |
| Observable | Recovery of HJ in |κ|→0 limit (analytical) |
| Uncertainty | κ is a free complex parameter — no numerical uncertainty stated |
| Methodology | Complex embedding uniqueness proof (two structural requirements) |

### Step 3 — Uncertainty Analysis
- No experimental uncertainties (purely theoretical/mathematical paper).
- Uniqueness proof is rigorous within the stated assumptions (local invertibility, first-order time dependence, absence of nonlinear gradient structures).
- Known limitation acknowledged by author: proof holds on connected regions where R ≠ 0 and a continuous branch of S can be chosen. At nodal sets or phase-branch changes, the polar decomposition is not globally regular.

### Step 4 — UIDT Mapping
- **Stratum:** III (UIDT interpretation/theoretical extension)
- **Evidence:** B (structurally compatible with UIDT ensemble dynamics; not externally verified for Yang–Mills sector)
- **TENSION ALERT:** None with UIDT ledger constants.
- **CRITICAL DISAMBIGUATION:** κ_Zhang (action dimension) ≠ κ_UIDT (gauge-scalar coupling = 0.500 ± 0.008 [A]). Symbols MUST be disambiguated in all UIDT documents referencing this paper.
- **Assigned Claim:** UIDT-C-101

---

## Paper 2 — Park et al. (2026), ICLR 2026 (NCF)

### Step 1 — Authenticity Check
- **Venue:** ICLR 2026 (peer-reviewed, accepted)
- **DOI:** Pending publication proceedings; conference identity confirmed
- **Status:** PEER-REVIEWED — PASS (venue-verified)
- **Audit result:** **PASS**
- **AI Artifact flags (2024–2026 scrutiny applied):**
  - Thm 5.1 (NCF consistency): cross-checked against energy conservation — CONSISTENT.
  - Thm 5.4 (Gaussian stability): cross-checked — CONSISTENT.
  - Empirical benchmark results: no energy conservation violations detected.
  - **No [POTENTIAL ARTIFACT] flags.**

### Step 2 — Epistemic Stripping
| Element | Content |
|---|---|
| Core method | Neural network solving HJ PDE via method of characteristics |
| Key result | Closed-form transport maps without numerical ODE integration |
| Observable | W2 distance, FID scores on standard OT benchmarks |
| Uncertainty | Empirical — training variance not systematically reported |
| Methodology | Supervised training on characteristic flow ODEs; bidirectional architecture |

### Step 3 — Uncertainty Analysis
- Proofs are rigorous for W2 OT with quadratic cost on R^n.
- **Scope boundary (CRITICAL):** Non-Abelian gauge manifolds, constrained phase spaces, and periodic boundary conditions (required for lattice UIDT) are NOT covered by the published proofs.
- Empirical performance gap between OT benchmarks and lattice QCD configuration spaces is unknown and must be benchmarked in Phase 2.

### Step 4 — UIDT Mapping
- **Stratum:** I (methodological — computation technique subject to experimental validation)
- **Evidence:** D (prediction/conjecture for UIDT applicability — applicability to Yang–Mills manifold unproven)
- **TENSION ALERT:** None with UIDT ledger constants.
- **SCOPE LIMITATION:** Must be explicitly stated in all UIDT PRs and documentation.
- **Assigned Claim:** UIDT-C-102

---

## Paper 3 — Hu et al. (2026), HJ Reachability Navigation

### Step 1 — Authenticity Check
- **arXiv ID:** NOT CONFIRMED
- **DOI:** NOT CONFIRMED
- **Peer review status:** Under review (venue unconfirmed)
- **Audit result:** **[AUDIT_PENDING]**
- Per UIDT Audit Protocol Step 1: if artifact cannot be verified, output [AUDIT_FAIL] for any external citation. This paper is treated as [AUDIT_PENDING] (not [AUDIT_FAIL]) because the content was provided directly and internal consistency checks pass, but external verifiability is incomplete.
- **DO NOT cite in any UIDT external publication until peer-reviewed with resolvable identifier.**

### Step 2 — Epistemic Stripping (conditional)
| Element | Content |
|---|---|
| Core method | Offline HJ TTR/BRT computation + online A*/RRT* graph search |
| Observable | Navigation success rate, computation time in 2D planar environments |
| Domain | Mobile robotics — NOT lattice QCD or statistical mechanics |
| Methodology | HJ PDE solved offline; value function used as heuristic at runtime |

### Step 3 — Uncertainty Analysis
- All results are robotics-domain specific.
- Transfer to HMC phase space is an unproven analogy.
- No energy conservation, gauge invariance, or RG constraint context in the paper.

### Step 4 — UIDT Mapping
- **Stratum:** I (algorithmic inspiration — indirect physics relevance)
- **Evidence:** D (speculative analogy, subject to [AUDIT_PENDING] constraint)
- **Direct UIDT relevance:** LOW
- **Assigned Claim:** UIDT-C-103

---

## Consolidated Summary

| Paper | Identifier | AI Artifact Scan | Evidence | Claim | Stratum |
|---|---|---|---|---|---|
| Zhang 2026 (HJS Theory) | arXiv:2601.22697 ✓ | PASS | B | UIDT-C-101 | III |
| Park et al. 2026 (NCF, ICLR) | ICLR 2026 ✓ | PASS | D | UIDT-C-102 | I |
| Hu et al. 2026 (HJ Robotics) | [AUDIT_PENDING] | CONDITIONAL | D | UIDT-C-103 | I |

**Ledger integrity:** No UIDT ledger constants modified (Δ*=1.710 GeV, γ=16.339, γ∞=16.3437, δγ=0.0047, v=47.7 MeV, w₀=−0.99, E_T=2.44 MeV).  
**Code integrity:** No changes to /core or /modules.  
**RG constraint:** 5κ²=3λ_S unchanged.  
**Language Guard:** Forbidden terms absent from all artefacts.
