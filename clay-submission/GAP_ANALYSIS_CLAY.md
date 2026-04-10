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

### Kinematic Pole — Numerical Finding (2026-04-06, mp.dps=80)

**[KINEMATIC_POLE_FOUND] Session audit 2026-04-06**

A deterministic 80-decimal-place evaluation of the Dyson-resummed
denominator

    D(s) = ((1 + w_S + s)(1 + w_g + s) - tilde_kappa^2)^2

on a Gauss-Chebyshev grid (N=32 nodes, s in [0,10]) reveals a real
kinematic pole at:

    s* ≈ 0.525946698109906   (at w_g = 0.25, tilde_kappa^2 = 2.71, w_S = 0)
    min |D(s)| on grid = 2.233e-2   (node index 4, s ≈ 0.480)

The analytic pole condition (1+s)(1+w_g+s) = tilde_kappa^2 yields the
critical threshold for pole suppression:

    w_g_crit = tilde_kappa^2 - 1 = 2.71 - 1 = 1.710

**Numerical coincidence (Stratum III, Evidence D — NOT a proof):**

    w_g_crit = tilde_kappa^2 - 1 = 1.710 = Delta* / GeV   [Ledger, Evidence A]

This numerical identity is documented as a topological boundary
condition for future momentum-dependent solvers. It is classified
strictly as Stratum III / Evidence D (theoretical signal). It does NOT
constitute a derivation of Delta* from the FRG sector, and it does NOT
upgrade the Evidence category of Delta* = 1.710 GeV (which remains A)
or of UIDT-C-070 (which remains D).

**Physical interpretation (Gribov-Zwanziger signal):**

The pole on the positive real Euclidean momentum axis signals that the
gluon propagator does not admit a simple real-mass-shell spectral
representation in the infrared (positivity violation). This is the
mathematical footprint of confinement in the Gribov-Zwanziger scenario:
the gluon evades asymptotic particle interpretation. The necessity of
contour deformation into the complex plane is the direct numerical
consequence of this confinement mechanism.

The physical w_g at the fixed-point scale k_FP = 1.7 GeV is:

    w_g(k_FP) = m_g^2 / k_FP^2 = (0.5 GeV)^2 / (1.7 GeV)^2 ≈ 0.087

This is far below w_g_crit = 1.710. Strategy 1 (raise w_g) would
require m_g > 2.22 GeV, which is unphysical. The pole is a genuine
feature of the IR regime and cannot be removed by parameter adjustment.

---

### Mandatory Solver Architecture: Cauchy Contour Deformation

All future implementations of solve_momentum_frg.py MUST use Cauchy
contour deformation (Fischer-group standard) to handle the kinematic
pole. The following constraints are binding:

**Deformation angle:** theta >= 0.2 rad
At theta = 0.2 rad: |D(s* e^{i*theta})| ≈ 0.120 (safe for Newton-Raphson).
At theta = 0.1 rad: |D(s* e^{i*theta})| ≈ 0.030 (marginal, avoid).

**Holomorphicity requirement:**
The Litim regulator contains a Heaviside step function Theta(k^2 - q^2).
On the complex momentum plane, this function is NOT holomorphic, which
violates the Cauchy integral theorem and destroys contour closure.
It MUST be replaced by a smooth analytic approximation, e.g.:

    Theta_smooth(s) = 1 / (exp(alpha * (|s| - 1)) + 1)

where alpha is the sharpness parameter. For mp.dps = 80, alpha must be
tuned to the grid resolution N:

    alpha_recommended = min(100, 2 * N)

If |Im(Pi_SS)| does not fall below 1e-14 after integration, alpha must
be increased. If |Im(Pi_SS)| does not fall below 1e-70, the contour
deformation is insufficient and theta must be increased.

**[CAUCHY_CLOSURE] verification protocol:**
Every run of solve_momentum_frg.py must output:

    [CAUCHY_CLOSURE_OK]   Im(Pi_SS) = <value>    if |Im| < 1e-14
    [CAUCHY_CLOSURE_FAIL] Im(Pi_SS) = <value>    if |Im| >= 1e-14

A [CAUCHY_CLOSURE_FAIL] output invalidates the numerical result of
that run and must not be used to update any claim evidence category.

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
the d_t integral with the full momentum-dependent vertices,
evaluated on the Cauchy-deformed contour (theta >= 0.2 rad).

**Step 3 — Coupled Integro-Differential Flow System:**
The resulting system is a coupled set of flow equations for:

    { tilde_kappa^2(p^2, k),  tilde_lambda_SF(p^2, k),
      eta_A(k),               eta_S(k) }

with full p^2-dependent mixed threshold functions l_{n,m}^4(w_g, w_S, p^2/k^2).
This system must be solved numerically with mp.dps = 80 via a
Newton-Raphson iteration on the fixed-point condition
beta_i(g*) = 0 for all couplings simultaneously.
The Gauss-Legendre quadrature on the Cauchy-deformed contour replaces
the Gauss-Chebyshev grid used in the preliminary LPA runs.

---

### Dependency for Future Updates

A formal upgrade of Evidence Category for UIDT-C-070, or exact
numerical reproduction of gamma = 16.339 (Evidence A-) from
first principles, requires ALL of the following:

1. Deterministic solution of the momentum-dependent integro-differential
   system (Steps 1-3), verified with mp.dps = 80 and
   [CAUCHY_CLOSURE_OK] on all integration nodes.

2. Verification that the fixed-point value eta_* shifts from the
   current massless-truncation value (~0.072) toward the
   phenomenological threshold (~0.063, derived from gamma calibration)
   upon inclusion of gluon decoupling effects.

3. Confirmation that the complex eigenvalues of the stability matrix
   (currently +/-0.654i, classified as truncation artefact, Evidence D)
   become real upon extending the truncation to include S^2 F^2 with
   full momentum dependence.

4. [CAUCHY_CLOSURE_OK] verified for all integration nodes at the
   fixed-point parameter values.

Until all four conditions are verified:
- gamma = 16.339 remains strictly Evidence A- (phenomenological)
- UIDT-C-070 remains Evidence D (analytical projection)
- Delta* = 1.710 GeV remains Evidence A (independent of FRG sector)
- No merge of these claims into a single A-grade result is permitted

---

### Claims and Evidence Table

| Claim ID    | Statement                                        | Evidence | Status     | Stratum |
|-------------|--------------------------------------------------|----------|------------|---------|
| UIDT-C-070  | FRG fixed point eta_* ~0.072 for S F^2          | D        | predicted  | III     |
| UIDT-C-002  | gamma = 16.339 (kinematic VEV, not derived)     | A-       | calibrated | II      |
| [NOTE]      | w_g_crit = kappa^2-1 = 1.710 = Delta*/GeV       | D        | signal     | III     |

GAP-FRG-001 is the precise mathematical boundary between these claims.
It defines what must be done before the arrow of evidence can run
from C-070 toward C-002.

The kinematic pole coincidence (w_g_crit = Delta*/GeV) is a Stratum III
signal. It may motivate future investigation but does not constitute
evidence for any existing or new claim at Evidence level C or above.

---

### Reproduction Note

All numerical results referenced here are reproducible via:

    python verification/scripts/derive_rg_gamma.py       (LPA fixed point)
    python verification/scripts/solve_momentum_frg.py    (Cauchy solver, future)

with mp.dps = 80 set locally inside each script (not globally).
Full console output archived in output/rg_run_log.txt.
Session audit logs:
  [AUDIT_FAIL] c3/c4 Hessian projection: 2026-04-06
  [KINEMATIC_POLE_FOUND] s* = 0.5259, w_g_crit = 1.710: 2026-04-06
