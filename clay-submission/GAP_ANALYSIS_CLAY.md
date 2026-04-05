# GAP ANALYSIS — CLAY SUBMISSION
# UIDT Framework — Open Mathematical Problems (Stratum III)
# Maintainer: P. Rietz | Last updated: 2026-04-06

---

## GAP-FRG-001

**Title:** Momentum-Dependent Vertex Projection and Dyson Resummation
         in the S F^2 Sector

**Evidence Status:** Currently limited to Category D
                    (massless truncation, no momentum projection)

**Linked Claim:** UIDT-C-070 (FRG fixed point, eta_* ≈ 0.072, Evidence D)

**Linked Limitation (Everyday):** CANONICAL/LIMITATIONS.md → L6-FRG

---

### Problem Statement (Analytical Roadblock)

The derivation of the scale compression parameter gamma via the scalar
anomalous dimension eta_* at the FRG fixed point (Claim UIDT-C-070)
requires stabilisation against the infrared decoupling of gluons
(Appelquist-Carazzone decoupling theorem). A deterministic analysis of
the Wetterich equation establishes that the Local Potential Approximation
(LPA) is fundamentally insufficient for this purpose.

**Established result (Stratum III, Evidence D — session audit 2026-04-06):**

The Dyson resummation of the scalar self-energy Pi_SS via the mixed
propagator G_SA ~ tilde_kappa generates a nonlinear feedback term in
beta_(tilde_kappa^2):

    delta_beta_(tilde_kappa^2) ~ -(d-1) * d_A * tilde_kappa^4 * l_2^4(w_g)
                               = -24 * tilde_kappa^4 * l_2^4(w_g)

Coefficients:
  d_A = 8     (SU(3) adjoint dimension, N_c^2 - 1)
  d-1 = 3     (transverse tensor contraction in d=4)
  l_2^4(w_g) = 1 / [16 pi^2 (1 + w_g)^3]   (Litim threshold function)

Physical consequence: this negative feedback destabilises the fixed
point under growth of tilde_kappa^2. The operator S F^2 cannot
stabilise itself within the 1-loop FRG. The only source of positive
stabilisation is the next-higher dimension-6 operator tilde_lambda_SF
(S^2 F^2) acting through an indirect tadpole channel on the scalar
propagator — a channel that is not accessible within the LPA.

**Why this is a Clay-level gap:**

Gamma in the UIDT is inseparably linked to the mass-gap generation
mechanism (Delta* = 1.710 ± 0.015 GeV). The missing mathematical
apparatus — a full momentum-dependent vertex projection — is precisely
the bridge between the current 80-dps numerics and a complete analytical
Yang-Mills proof. This gap describes exactly the step that is absent in
any existing non-perturbative derivation of a scalar-gauge coupling
hierarchy in SU(3) Yang-Mills theory.

**Audit note — [AUDIT_FAIL] 2026-04-06:**
Earlier projections c3 = -8, c4 = +16 were derived from a naive
Hessian expansion (O(V^3) and O(V^2) respectively) and were found
incorrect:
- The O(V^3) term projects onto other operators, not S F^2 directly.
- The O(V^2) tadpole does not close internal scalar lines.
These values must not enter any numerical implementation.
The correct nonlinear coefficient -24 follows from the Dyson resummation
of the full 2x2 (S,A) propagator matrix.

---

### Required Resolution (Solution Path)

To close GAP-FRG-001 and enable a potential upgrade of UIDT-C-070
beyond Evidence Category D, three steps are required:

**Step 1 — Momentum Projection (partial_p^2 expansion):**
Transition from the LPA to a full momentum-dependent vertex projection.
The beta-functions must be extracted via:

    beta_g = lim_{p^2 -> 0} partial_t [ partial_{p^2} Gamma^(2)(p^2) ]

This requires computing the full p^2-dependent two-point function
Gamma^(2)(p^2) and projecting onto each operator monomial.

**Step 2 — Self-Consistent Propagator Resummation:**
The full 2x2 propagator matrix in (S, A^a_mu) field space must be
inverted non-perturbatively, retaining all off-diagonal entries
G_SA ~ tilde_kappa. The self-energy Pi_SS must be computed under
the d_t integral with the full momentum-dependent vertices.

**Step 3 — Coupled Integro-Differential Flow System:**
The resulting system is a coupled set of flow equations for:

    { tilde_kappa^2(p^2, k),  tilde_lambda_SF(p^2, k),
      eta_A(k),               eta_S(k) }

with full p^2-dependent mixed threshold functions l_{n,m}^4(w_g, w_S, p^2/k^2).
This system must be solved numerically with mp.dps = 80 via a
Newton-Raphson iteration on the fixed-point condition
beta_i(g*) = 0 for all couplings simultaneously.

---

### Dependency for Future Updates

A formal upgrade of Evidence Category for UIDT-C-070, or exact
numerical reproduction of gamma = 16.339 (Evidence A-) from
first principles, requires ALL of the following:

1. Deterministic solution of the momentum-dependent integro-differential
   system (Steps 1-3), verified with mp.dps = 80.

2. Verification that the fixed-point value eta_* shifts from the
   current massless-truncation value (~0.072) toward the
   phenomenological threshold (~0.063, derived from gamma calibration)
   upon inclusion of gluon decoupling effects.

3. Confirmation that the complex eigenvalues of the stability matrix
   (currently +/-0.654i, classified as truncation artefact, Evidence D)
   become real upon extending the truncation to include S^2 F^2 with
   full momentum dependence.

Until all three conditions are verified:
- gamma = 16.339 remains strictly Evidence A- (phenomenological)
- UIDT-C-070 remains Evidence D (analytical projection)
- No merge of these two claims into a single A-grade result is permitted

---

### Claims and Evidence Table

| Claim ID    | Statement                                   | Evidence | Status     | Stratum |
|-------------|----------------------------------------------|----------|------------|----------|
| UIDT-C-070  | FRG fixed point eta_* ~0.072 for S F^2      | D        | predicted  | III      |
| UIDT-C-002  | gamma = 16.339 (kinematic VEV, not derived) | A-       | calibrated | II       |

GAP-FRG-001 is the precise mathematical boundary between these claims.
It defines what must be done before the arrow of evidence can run
from C-070 toward C-002.

---

### Reproduction Note

All numerical results referenced here are reproducible via:

    python verification/scripts/derive_rg_gamma.py

with mp.dps = 80 set locally inside that script (not globally).
Full console output archived in output/rg_run_log.txt.
Session audit log for [AUDIT_FAIL] c3/c4: 2026-04-06.
