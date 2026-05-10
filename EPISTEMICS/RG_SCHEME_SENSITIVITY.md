# Renormalisation Scheme Sensitivity Analysis

**Evidence Category: D (open task)**  
**Stratum: II–III**  
**Maintainer: P. Rietz**  
**Last reviewed: 2026-05-10**

---

## 1. Problem Statement

Every QFT calculation with renormalisation group (RG) running depends on the chosen
regularisation and renormalisation scheme.  Physical observables must be scheme-independent
at the non-perturbative level, but intermediate quantities (coupling constants, anomalous
dimensions, fixed-point coordinates) are scheme-dependent.

Currently, UIDT v3.9 uses a single scheme (dimensional regularisation with MS-bar subtraction
as implemented in the RG module).  The stability of Δ*, γ, and ET under scheme variation
has **not** been systematically verified.

---

## 2. Required Verification (Open Task)

For each of the following scheme variants, compute Δ*, γ, ET and compare to ledger values:

| Scheme | Status |
|--------|--------|
| MS-bar (current baseline) | ✅ Implemented |
| MOM (momentum subtraction) | ⬜ Not implemented |
| Wilsonian block-spin | ⬜ Not implemented |
| Lattice-matched scheme (RI-SMOM) | ⬜ Not implemented |

Acceptance criterion: variation of Δ* < ± 0.015 GeV across all schemes (i.e., within the
existing A-category error bar).

---

## 3. Limitation L8 (New)

> **L8**: The UIDT mass-gap calculation has been performed in the MS-bar scheme only.
> Scheme independence has not been demonstrated.  Until M-SS-1 (see Section 4) is complete,
> the Evidence category of Δ* must be understood as conditional on this scheme choice.

---

## 4. Milestones

| Milestone | Description | Status |
|-----------|-------------|--------|
| M-SS-1 | Implement MOM scheme in `modules/rg_flow.py` and verify Δ* stability | ⬜ Open |
| M-SS-2 | Wilsonian scheme cross-check | ⬜ Open |
| M-SS-3 | Publish scheme-independence analysis as supplementary note | ⬜ Open |
