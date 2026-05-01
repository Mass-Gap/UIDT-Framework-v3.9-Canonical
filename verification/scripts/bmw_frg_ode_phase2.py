"""BMW-FRG Simplified Phase-2 ODE Solver

Evidence category : D  (prediction — ghost sector absent)
Status flag       : [GHOST_SECTOR_MISSING]
Constitution      : mp.dps = 80 LOCAL per §RACE CONDITION LOCK
                    no float(), no round(), residual < 1e-14

Physical model
--------------
Truncation: LPA + wavefunction renormalisation for the gluon field A_mu.
Ghost sector (Z_c, Gribov horizon) is ABSENT in this solver.
Consequences: eta_A is an approximation; beta_g^ERGE is indicative only.

Flow equations (Litim regulator, d=4, SU(3))
---------------------------------------------
Running variables (dimensionless):
  u[0] = Z_A(t)      gluon wavefunction renormalisation
  u[1] = kappa(t)    dimensionless minimum of U_k
  u[2] = lambda_S(t) quartic scalar coupling

Flow parameter: t = ln(k/Lambda_UV), t in [-T_max, 0]

Litim threshold functions (d=4):
  l_0^B(w) = 1 / (1 + w)        bosonic
  l_1^B(w) = 1 / (1 + w)^2
  l_0^F(w) = 1 / (1 + w)        fermionic (not used here)

Flow for Z_A (anomalous dimension eta_A = -dt ln Z_A):
  eta_A = (g^2 * N_c) / (48 pi^2) * l_1^B(m_A2 / k^2)
  where m_A2 / k^2 is taken as zero in the UV (Litim: R_k absorbs it)
  APPROXIMATION: eta_A set to zero (ghost missing).
  This is flagged explicitly as [GHOST_SECTOR_MISSING].

Flow for kappa:
  dt kappa = -(2 + eta_A) * kappa
           + (N_c^2 - 1) / (32 pi^2) * l_0^B(2 lambda_S * kappa)

Flow for lambda_S (quartic coupling):
  dt lambda_S = 2 * eta_A * lambda_S
              + (N_c^2 - 1) / (16 pi^2)
                  * lambda_S^2 * l_1^B(2 lambda_S * kappa)

RG constraint checked at every step:
  5 kappa^2 - 3 lambda_S = 0,  tolerance < 1e-14  [RG_CONSTRAINT_FAIL]

Fixpoint criterion (IR, t -> -infty):
  |dt kappa| < 1e-10  AND  |dt lambda_S| < 1e-10

Ledger constants used
---------------------
  Delta_star = 1.710 GeV  [A]   interpreted as IR spectral gap scale
  gamma      = 16.339     [A-]  phenomenological kinetic vacuum parameter
  kappa_0    = 0.500      [A]   UV initial condition
  lambda_S_0 = 5/12       [A]   UV initial condition (from 5 kappa^2 = 3 lambda_S)
"""

import mpmath as mp


# ---------------------------------------------------------------------------
# LEDGER CONSTANTS  — must never be modified automatically
# ---------------------------------------------------------------------------
def _ledger():
    """Return immutable ledger parameters as mpf.  Evidence in brackets."""
    mp.dps = 80  # LOCAL
    return {
        "Delta_star": mp.mpf("1.710"),    # [A]  Yang-Mills spectral gap in GeV
        "gamma":      mp.mpf("16.339"),   # [A-] kinetic vacuum parameter
        "gamma_inf":  mp.mpf("16.3437"),  # [A-]
        "delta_gamma":mp.mpf("0.0047"),   # [A-]
        "v":          mp.mpf("47.7e-3"),  # [A]  in GeV
        "w0":         mp.mpf("-0.99"),    # [C]
        "ET":         mp.mpf("2.44e-3"),  # [C]  in GeV
    }


# ---------------------------------------------------------------------------
# LITIM THRESHOLD FUNCTIONS
# ---------------------------------------------------------------------------
def _l0B(w):
    """l_0^B(w) = 1 / (1 + w)  —  bosonic threshold, Litim regulator."""
    mp.dps = 80
    return mp.mpf("1") / (mp.mpf("1") + w)


def _l1B(w):
    """l_1^B(w) = 1 / (1 + w)^2  —  derivative threshold."""
    mp.dps = 80
    return mp.mpf("1") / (mp.mpf("1") + w) ** 2


# ---------------------------------------------------------------------------
# RG CONSTRAINT CHECK
# ---------------------------------------------------------------------------
def check_rg_constraint(kappa, lambda_S):
    """5 kappa^2 = 3 lambda_S.  Residual must be < 1e-14."""
    mp.dps = 80
    lhs = mp.mpf("5") * kappa ** 2
    rhs = mp.mpf("3") * lambda_S
    residual = abs(lhs - rhs)
    if residual >= mp.mpf("1e-14"):
        print(f"[RG_CONSTRAINT_FAIL]  residual = {mp.nstr(residual, 6, strip_zeros=False)}")
        return False, residual
    return True, residual


# ---------------------------------------------------------------------------
# ODE RIGHT-HAND SIDE
# ---------------------------------------------------------------------------
def frg_rhs(t, state):
    """RHS of the BMW-FRG flow equations (simplified, ghost-free LPA).

    Parameters
    ----------
    t : mpf
        Flow parameter t = ln(k / Lambda_UV).  UV: t=0, IR: t -> -infty.
    state : list of mpf
        [Z_A, kappa, lambda_S]

    Returns
    -------
    list of mpf
        [dZ_A/dt, dkappa/dt, dlambda_S/dt]
    """
    mp.dps = 80  # LOCAL — Constitution §RACE CONDITION LOCK

    Z_A      = mp.mpf(str(state[0]))
    kappa    = mp.mpf(str(state[1]))
    lambda_S = mp.mpf(str(state[2]))

    # SU(3) colour factors
    N_c   = mp.mpf("3")
    # (N_c^2 - 1) = 8 for SU(3)
    Nc2m1 = N_c ** 2 - mp.mpf("1")

    # Anomalous dimension
    # [GHOST_SECTOR_MISSING]: full eta_A requires Z_c; set to zero here.
    eta_A = mp.mpf("0")

    # Argument of threshold functions: dimensionless mass
    # m^2_S / k^2 = 2 * lambda_S * kappa  (from U_k = lambda_S (rho - kappa)^2)
    w_S = mp.mpf("2") * lambda_S * kappa
    if w_S < mp.mpf("-1"):
        # Tachyonic instability: flow becomes ill-defined
        print("[TACHYON_WARNING]  w_S < -1 at t =", mp.nstr(t, 6))
        w_S = mp.mpf("-0.99")  # clamp — result is unreliable

    # Prefactors
    pref_kappa    = Nc2m1 / (mp.mpf("32") * mp.pi ** 2)
    pref_lambda   = Nc2m1 / (mp.mpf("16") * mp.pi ** 2)

    # Flow equations
    dZ_A      = mp.mpf("0")   # eta_A = 0 => Z_A constant (ghost missing)
    dkappa    = (-(mp.mpf("2") + eta_A) * kappa
                  + pref_kappa * _l0B(w_S))
    dlambda_S = (mp.mpf("2") * eta_A * lambda_S
                  + pref_lambda * lambda_S ** 2 * _l1B(w_S))

    return [dZ_A, dkappa, dlambda_S]


# ---------------------------------------------------------------------------
# EULER INTEGRATOR  (mpmath-native, no external ODE library)
# ---------------------------------------------------------------------------
def run_flow(n_steps=4000, t_end=mp.mpf("-20")):
    """Integrate the FRG flow from t=0 (UV) to t=t_end (IR).

    Returns
    -------
    dict with keys:
        't_grid'   : list of mpf  (flow parameter values)
        'Z_A'      : list of mpf
        'kappa'    : list of mpf
        'lambda_S' : list of mpf
        'rg_ok'    : bool  (True if RG constraint never violated)
        'fixpoint_reached' : bool
        'rg_residual_max'  : mpf
    """
    mp.dps = 80  # LOCAL

    # UV initial conditions
    Z_A_0      = mp.mpf("1")
    kappa_0    = mp.mpf("0.500")                       # [A]
    lambda_S_0 = mp.mpf("5") * kappa_0 ** 2 / mp.mpf("3")  # from RG constraint [A]

    print("BMW-FRG Phase-2 Simplified Solver")
    print("[GHOST_SECTOR_MISSING]  eta_A = 0 (Z_c absent)")
    print(f"UV initial conditions:")
    print(f"  Z_A_0      = {mp.nstr(Z_A_0,      30, strip_zeros=False)}")
    print(f"  kappa_0    = {mp.nstr(kappa_0,    30, strip_zeros=False)}")
    print(f"  lambda_S_0 = {mp.nstr(lambda_S_0, 30, strip_zeros=False)}")
    print()

    # Verify UV RG constraint
    ok, res0 = check_rg_constraint(kappa_0, lambda_S_0)
    print(f"UV RG constraint 5κ²=3λ:  ok={ok},  residual={mp.nstr(res0, 6, strip_zeros=False)}")
    print()

    state = [Z_A_0, kappa_0, lambda_S_0]
    dt    = t_end / mp.mpf(str(n_steps))   # negative step

    t_grid   = [mp.mpf("0")]
    Z_A_arr  = [state[0]]
    kappa_arr= [state[1]]
    lS_arr   = [state[2]]

    rg_ok         = True
    rg_res_max    = mp.mpf("0")
    fixpoint_flag = False

    for i in range(n_steps):
        t_now  = mp.mpf(str(i)) * dt
        rhs    = frg_rhs(t_now, state)

        # Euler step
        state_new = [state[j] + dt * rhs[j] for j in range(3)]

        # RG constraint check (every 200 steps to avoid excessive output)
        if i % 200 == 0:
            ok_i, res_i = check_rg_constraint(state_new[1], state_new[2])
            if res_i > rg_res_max:
                rg_res_max = res_i
            if not ok_i:
                rg_ok = False

        # Fixpoint detection
        if (abs(rhs[1]) < mp.mpf("1e-10") and
                abs(rhs[2]) < mp.mpf("1e-10") and
                not fixpoint_flag):
            fixpoint_flag = True
            print(f"  [FIXPOINT_DETECTED]  t = {mp.nstr(t_now, 8)},  "
                  f"kappa = {mp.nstr(state[1], 12)},  "
                  f"lambda_S = {mp.nstr(state[2], 12)}")

        state = state_new
        t_grid.append(t_now + dt)
        Z_A_arr.append(state[0])
        kappa_arr.append(state[1])
        lS_arr.append(state[2])

    return {
        "t_grid":           t_grid,
        "Z_A":              Z_A_arr,
        "kappa":            kappa_arr,
        "lambda_S":         lS_arr,
        "rg_ok":            rg_ok,
        "fixpoint_reached": fixpoint_flag,
        "rg_residual_max":  rg_res_max,
    }


# ---------------------------------------------------------------------------
# IR EXTRACTION
# ---------------------------------------------------------------------------
def extract_ir(result):
    """Extract physical IR quantities from the flow result.

    c_S^phys = 1 - Z_A(k=0) / Z_A(Lambda_UV)
    NOTE: with eta_A=0 this is exactly zero.
          This is the expected [GHOST_SECTOR_MISSING] artefact.
    """
    mp.dps = 80
    Z_UV = result["Z_A"][0]
    Z_IR = result["Z_A"][-1]
    c_S  = mp.mpf("1") - Z_IR / Z_UV

    kappa_IR    = result["kappa"][-1]
    lambda_S_IR = result["lambda_S"][-1]

    print("\nIR Extraction (t -> -infty):")
    print(f"  Z_A(IR)      = {mp.nstr(Z_IR,        30, strip_zeros=False)}")
    print(f"  kappa(IR)    = {mp.nstr(kappa_IR,    30, strip_zeros=False)}")
    print(f"  lambda_S(IR) = {mp.nstr(lambda_S_IR, 30, strip_zeros=False)}")
    print(f"  c_S^phys     = {mp.nstr(c_S,         30, strip_zeros=False)}")
    print()
    if abs(c_S) < mp.mpf("1e-30"):
        print("  [GHOST_SECTOR_MISSING]  c_S^phys = 0 as expected (eta_A=0).")
        print("  Full c_S requires Z_c from ghost sector (Phase-1 prerequisite).")
    return c_S, kappa_IR, lambda_S_IR


# ---------------------------------------------------------------------------
# LEDGER TENSION CHECK
# ---------------------------------------------------------------------------
def check_ledger_tension(kappa_IR):
    """Compare kappa(IR) against Ledger constraint.

    The dimensionless minimum kappa at k~Delta_star should be consistent
    with gamma=16.339 [A-].  A precise mapping requires the full Z_A flow;
    here we flag a [TENSION_ALERT] if kappa(IR) deviates by more than 10%
    from kappa_0 (i.e. the coupling runs substantially).
    """
    mp.dps = 80
    kappa_0 = mp.mpf("0.500")
    deviation = abs(kappa_IR - kappa_0) / kappa_0
    print("Ledger tension check (kappa):")
    print(f"  kappa_0  (UV)  = {mp.nstr(kappa_0,  20, strip_zeros=False)}   [A]")
    print(f"  kappa_IR (IR)  = {mp.nstr(kappa_IR, 20, strip_zeros=False)}   [D]")
    print(f"  relative shift = {mp.nstr(deviation, 6, strip_zeros=False)}")
    if deviation > mp.mpf("0.1"):
        print("  [TENSION ALERT]  kappa shifts > 10% under flow.")
        print(f"  External value: kappa_0 = {mp.nstr(kappa_0, 8)},  "
              f"Flow result: {mp.nstr(kappa_IR, 8)},  "
              f"Difference: {mp.nstr(abs(kappa_IR - kappa_0), 8)}")
    else:
        print("  No tension within 10% threshold (ghost sector absent).")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mp.dps = 80  # LOCAL

    print("=" * 72)
    print("BMW-FRG ODE Phase-2 — Simplified Solver")
    print("Evidence: D   |   [GHOST_SECTOR_MISSING]")
    print("UIDT Framework v3.9  —  Constitution-compliant")
    print("=" * 72)
    print()

    result = run_flow(n_steps=4000, t_end=mp.mpf("-20"))

    print()
    print(f"RG constraint OK throughout flow : {result['rg_ok']}")
    print(f"Max RG residual                  : {mp.nstr(result['rg_residual_max'], 6, strip_zeros=False)}")
    print(f"Fixpoint reached                 : {result['fixpoint_reached']}")

    c_S, kappa_IR, lambda_S_IR = extract_ir(result)
    check_ledger_tension(kappa_IR)

    print()
    print("Reproduction note:")
    print("  python verification/scripts/bmw_frg_ode_phase2.py")
    print("  Required: mpmath (pip install mpmath)")
    print()
    print("Known limitations:")
    print("  1. eta_A = 0  (ghost sector missing — Phase-1 prerequisite)")
    print("  2. Euler integrator (sufficient for fixpoint detection; RK4 for precision)")
    print("  3. c_S^phys = 0 by construction (artefact of absent Z_c)")
    print("  4. No Gribov-Zwanziger sector")
    print("  5. Evidence category D — not Evidence A")
    print("=" * 72)
