# Open Questions: Geometry Sector (OQ-G1 – OQ-G4)

**Registry version:** v3.9.4
**Date opened:** 2026-04-04
**Linked section:** docs/emergent_geometry_section7.md

---

## OQ-G1 — γ Derivation from RG First Principles

| Field | Value |
|-------|-------|
| Status | E-open (pre-existing) |
| Linked claim | UIDT-C-016 |
| Priority | HIGH |
| Blocking | Upgrade of UIDT-C-002 from A- → A |

The kinetic vacuum parameter `γ = 16.339` is phenomenologically determined
(Category A-). The perturbative RG yields `γ_pert ≈ 55.8`, a factor ~3.4
discrepancy documented as Limitation L4. The SU(3) group-theory conjecture
`γ_{SU(3)} = 2(N_c+1)/N_c · N_c=3 ≈ 16.333` (UIDT-C-052, E-open) would
address this if proven from the UIDT Lagrangian.

**Resolution path:** Full FRG flow derivation of γ from `S`-sector
renormalisation, with residual `|γ_derived − 16.339| < 1e-14` at `mp.dps=80`.

---

## OQ-G2 — Factor-10 Geometric Normalisation

| Field | Value |
|-------|-------|
| Status | E-open (pre-existing) |
| Linked claim | UIDT-C-018 |
| Priority | **HIGHEST PRIORITY** |
| Blocking | Coefficients A, B in metric ansatz (Section 7.3) |

The dimensionless coefficient `A` in `g_{μν}^{info}` contains an unresolved
factor-10 geometric normalisation whose first-principles derivation is
outstanding. This is the highest-priority open question in the UIDT
geometry sector.

**Resolution path:** Derive from the FRG effective action truncation;
verify numerically at `mp.dps=80`.

---

## OQ-G3 — Reference Scale μ Registration (NEW, 2026-04-04)

| Field | Value |
|-------|-------|
| Status | E-open (new) |
| Linked claim | UIDT-C-056 |
| Priority | HIGH |
| Blocking | Dimensional consistency of metric ansatz |

The metric ansatz `g_{μν}^{info} = A · [∂_μ S ∂_ν S]_R / μ²` requires an
explicit renormalisation reference scale `μ` to be dimensionless.
The naive candidate `μ = Δ*` is **circular** unless independently derived,
since `Δ* = 1.710 GeV` is the Yang-Mills spectral gap (UIDT-C-001).

**Required action:** Add `μ` to `CANONICAL/CONSTANTS.md` with:
- Numerical value and uncertainty
- Derivation methodology
- Evidence category (expected: C or D until derived)
- Independence check from UIDT-C-001

---

## OQ-G4 — Lorentz-Signature Recovery (NEW, 2026-04-04)

| Field | Value |
|-------|-------|
| Status | E-open (new) |
| Linked claim | UIDT-C-055 |
| Priority | HIGH |
| Blocking | Falsifiability of information-metric hypothesis |

The gradient-bilinear construction must be shown to yield Lorentz signature
`(1,3)`, positivity on spacelike separations, causal structure compatible
with the Yang-Mills propagator light cone, and a well-defined UV limit
`y → x` under explicit renormalisation.

The torsion sector (`E_T = 2.44 MeV`, UIDT-C-044, Cat. C) may contribute
off-diagonal structure; independence from `E_T` must be verified.

**Required action:** Construct explicit Wick-rotation argument or
covariant decomposition showing how gradient bilinears select (1,3)
signature from the Euclidean FRG flow.

---

## Status Table

| ID | Description | Linked Claim | Priority | Status | Since |
|----|-------------|--------------|----------|--------|-------|
| OQ-G1 | γ from RG first principles | UIDT-C-016 | HIGH | E-open | v3.2 |
| OQ-G2 | Factor-10 normalisation | UIDT-C-018 | HIGHEST | E-open | v3.2 |
| OQ-G3 | Reference scale μ registration | UIDT-C-056 | HIGH | E-open | v3.9.4 |
| OQ-G4 | Lorentz-signature recovery | UIDT-C-055 | HIGH | E-open | v3.9.4 |

---

*Last updated: 2026-04-04 | Maintainer: P. Rietz | License: CC BY 4.0*
