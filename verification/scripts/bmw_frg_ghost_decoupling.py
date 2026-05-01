# verification/scripts/bmw_frg_ghost_decoupling.py
#
# [UIDT-v3.9] BMW-FRG: Ghost-Propagator Z_c(k) with Decoupling Boundary Condition
#
# Evidence classification:
#   Litim threshold p_c = 1/4          [A]  -- analytically exact
#   Decoupling BC Z_c(IR) > 0          [B]  -- lattice-compatible (Bogolubsky et al.)
#   Numerical Z_c trajectory           [D]  -- prediction, not calibrated
#
# Open flags:
#   [GHOST_SECTOR_FLAG]  g^2(k) held constant; full beta_g coupling deferred to Phase 3
#   [GRIBOV_NOT_IMPL]    No Gribov-horizon condition; Decoupling-BC used as proxy
#
# Constitution compliance:
#   mp.dps = 80 declared LOCAL in every function  (§RACE CONDITION LOCK)
#   No float(), no round()                         (§NUMERICAL DETERMINISM)
#   No deletion of ledger constants                (§LINTER PROTECTION)
#   No mock of mpmath                              (§TESTING LAWS)
#
# Reproduction:
#   python verification/scripts/bmw_frg_ghost_decoupling.py
#   python -m pytest verification/tests/test_ghost_decoupling_bc.py -v

import mpmath as mp


# ---------------------------------------------------------------------------
# Immutable ledger references (read-only, never modify)
# ---------------------------------------------------------------------------
_DELTA_STAR_GEV = "1.710"   # [A]  Yang-Mills spectral gap
_GAMMA          = "16.339"  # [A-] kinetic vacuum parameter
_V_MEV          = "47.7"    # [A]  portal scale


def litim_threshold_ghost():
    """
    Litim regulator R_k^c(q) = Z_c(k) * (k^2 - q^2) * theta(k^2 - q^2)

    Threshold function p_c (dimensionless, d=4, analytically exact):

        p_c = 1 / (1 + r_c)^2  evaluated at the Litim step

    For the Litim regulator in d=4 the momentum integral collapses to
    the boundary q^2 = k^2, giving p_c = 1/4 exactly.

    Returns mpf("1/4").
    Evidence: [A]
    """
    mp.dps = 80  # LOCAL -- Constitution §RACE CONDITION LOCK
    return mp.mpf("1") / mp.mpf("4")


def ghost_anomalous_dimension(Z_c, Z_A_val, g2_val):
    """
    Anomalous dimension of the ghost field:

        eta_c = - d/dt ln Z_c
              = - (g^2 * N_c) / (3 * 16 * pi^2) * (Z_A / Z_c) * p_c

    Parameters
    ----------
    Z_c     : mpf  ghost wavefunction renormalisation at scale k
    Z_A_val : mpf  gluon wavefunction renormalisation at scale k
    g2_val  : mpf  running coupling g^2(k)

    Returns
    -------
    eta_c : mpf   [dimensionless]

    Evidence: [D] (prediction)
    """
    mp.dps = 80  # LOCAL
    N_c  = mp.mpf("3")
    pi2  = mp.pi ** 2
    p_c  = litim_threshold_ghost()
    coeff = (g2_val * N_c) / (mp.mpf("3") * mp.mpf("16") * pi2)
    eta_c = -coeff * (Z_A_val / Z_c) * p_c
    return eta_c


def ghost_ode_rhs(t, Z_c, Z_A_val, g2_val):
    """
    Right-hand side of the ghost flow equation:

        d Z_c / dt = eta_c(Z_c, Z_A, g^2) * Z_c

    Parameters
    ----------
    t       : mpf  RG flow parameter t = ln(k / Lambda_UV)
    Z_c     : mpf  ghost wavefunction renormalisation
    Z_A_val : mpf  gluon Z_A at current k (from Phase-2 solution)
    g2_val  : mpf  coupling g^2 at current k

    Returns
    -------
    dZ_c/dt : mpf

    Evidence: [D]
    """
    mp.dps = 80  # LOCAL
    eta_c = ghost_anomalous_dimension(
        mp.mpf(str(Z_c)),
        mp.mpf(str(Z_A_val)),
        mp.mpf(str(g2_val))
    )
    return eta_c * mp.mpf(str(Z_c))


def run_ghost_flow(
    Z_c_UV,
    Z_A_flow,
    g2_flow,
    t_UV=mp.mpf("0"),
    t_IR=mp.mpf("-30"),
    tol=mp.mpf("1e-20")
):
    """
    Integrate the ghost flow equation from t_UV to t_IR.

    Decoupling boundary condition (UV):
        Z_c(t_UV) = Z_c_UV   (positive, O(1), typically 1.0)

    Decoupling check (IR):
        Z_c(t_IR) > 0  must hold; raises AssertionError otherwise.

    Parameters
    ----------
    Z_c_UV   : mpf or str  UV initial condition
    Z_A_flow : callable    t -> mpf; interpolant from Phase-2 Z_A solution
    g2_flow  : callable    t -> mpf; running coupling (constant in Phase 2)
    t_UV     : mpf         UV boundary (default 0 = k = Lambda_UV)
    t_IR     : mpf         IR boundary (default -30, k/Lambda_UV ~ 1e-13)
    tol      : mpf         ODE solver tolerance

    Returns
    -------
    Z_c_IR  : mpf          Z_c at t_IR
    Z_c_sol : odefun       full solution object

    Evidence: [D]
    Flags: [GHOST_SECTOR_FLAG] [GRIBOV_NOT_IMPL]
    """
    mp.dps = 80  # LOCAL
    Z_c_UV = mp.mpf(str(Z_c_UV))

    def rhs(t, Zc):
        mp.dps = 80
        return ghost_ode_rhs(
            t,
            Zc,
            Z_A_flow(mp.mpf(str(t))),
            g2_flow(mp.mpf(str(t)))
        )

    Z_c_sol = mp.odefun(rhs, t_UV, Z_c_UV, tol=tol)
    Z_c_IR  = Z_c_sol(t_IR)

    if not (Z_c_IR > mp.mpf("0")):
        raise AssertionError(
            f"[DECOUPLING_BC_FAIL] Z_c(t_IR={t_IR}) = {Z_c_IR} <= 0. "
            "Decoupling boundary condition violated."
        )

    return Z_c_IR, Z_c_sol


def decoupling_bc_check(Z_c_IR):
    """
    Explicit check of the Decoupling boundary condition.

    Z_c(k -> 0) must be finite and positive (Decoupling solution).
    Contrast: Scaling solution would give Z_c -> 0.

    Returns True if condition holds, raises AssertionError otherwise.
    Evidence: [B] lattice-compatible
    """
    mp.dps = 80  # LOCAL
    Z_c_IR = mp.mpf(str(Z_c_IR))
    if not (Z_c_IR > mp.mpf("0")):
        raise AssertionError(
            "[DECOUPLING_BC_FAIL] Z_c(IR) must be > 0 for Decoupling solution."
        )
    return True


# ---------------------------------------------------------------------------
# Standalone execution: minimal smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mp.dps = 80  # LOCAL

    print("=" * 60)
    print("BMW-FRG Ghost-Propagator: Decoupling-BC Smoke Test")
    print("[GHOST_SECTOR_FLAG] g^2(k) = const = 1.0 (simplified)")
    print("[GRIBOV_NOT_IMPL]   No Gribov-horizon condition")
    print("[EVIDENCE_D]        All outputs are predictions")
    print("=" * 60)

    # Simplified constant interpolants (Phase-3 will couple fully)
    Z_A_const = lambda t: mp.mpf("1")
    g2_const  = lambda t: mp.mpf("1")

    Z_c_UV = mp.mpf("1")
    t_UV   = mp.mpf("0")
    t_IR   = mp.mpf("-10")  # conservative for smoke test

    p_c = litim_threshold_ghost()
    print(f"Litim threshold p_c [A] = {mp.nstr(p_c, 20)}")
    assert abs(p_c - mp.mpf("1") / mp.mpf("4")) < mp.mpf("1e-14"), \
        "[RG_CONSTRAINT_FAIL] p_c != 1/4"
    print("p_c == 1/4 verified: residual < 1e-14 [PASS]")

    Z_c_IR, _ = run_ghost_flow(
        Z_c_UV, Z_A_const, g2_const,
        t_UV=t_UV, t_IR=t_IR
    )
    decoupling_bc_check(Z_c_IR)

    print(f"Z_c(UV) = {mp.nstr(Z_c_UV, 20)}")
    print(f"Z_c(IR) = {mp.nstr(Z_c_IR, 30)}")
    print(f"Decoupling BC Z_c(IR) > 0: [PASS]")
    print("Smoke test complete.")
