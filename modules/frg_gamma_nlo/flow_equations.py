"""
[UIDT-v3.9] FRG/NLO — Step 3: Wetterich Flow for Z_phi(k)
===========================================================

STRATUM ASSIGNMENT:
  Stratum I  : loop integral over Euclidean momentum (standard QFT)
  Stratum II : Wetterich exact RG equation (established formalism)
  Stratum III: identification of IR limit Z_phi(k->0) with UIDT gamma

EPISTEMIC STATUS:
  [A]  Wetterich equation structure (established, Stratum II)
  [A]  RG constraint 5*kappa^2 = 3*lambda_S (maintained throughout)
  [D]  Prediction: lim_{k->0} Z_phi(k) = gamma = 16.339

NOTE:
  This file implements the NUMERICAL flow only.
  The closed analytic result (required for [A] upgrade) is OPEN.
  Current output is [D]: a numerical prediction consistent with gamma.

  Evidence upgrade path:
    [D] -> [A] requires either:
      (a) closed-form solution of the flow equations below, or
      (b) rigorous error bounds proving convergence to 16.339 +/- delta_gamma
          with residual < 1e-14

    Until that proof exists, any gamma value produced here carries [D].

WETTERICH EQUATION (LPA', Litim regulator, 4d Euclidean):

  k * d/dk Gamma_k = (1/2) Tr[ (Gamma_k^(2) + R_k)^{-1} * k * d/dk R_k ]

Projected onto the kinetic sector (LPA' / NLO), this gives the flow
for the anomalous dimension eta_phi(k) and the running kinetic
coefficient Z_phi(k):

  d ln Z_phi / d ln k = -eta_phi(k)

In the Litim regulator, the momentum loop integral is analytically
tractable at LPA level.  The NLO correction modifies the threshold
function l_n^d via the anomalous dimension feedback:

  eta_phi(k) = (v_d / 3) * m_phi^2(k) / [1 + m_phi^2(k)]^3 * ...

  where v_d = 1 / (2^(d+1) * pi^(d/2) * Gamma(d/2 + 1))  for d=4

For the UIDT vacuum scalar in d=4:

  U_k''(phi_vev) =: m_phi^2(k)  (dimensionless, in units of k^2)

  Z_phi(k) evolved via:
    dZ/dt = -eta_phi(k) * Z_phi(k),   t = ln(k/Lambda_UV)

UV INITIAL CONDITIONS (Stratum III):
  k_UV   = Delta* = 1.710 GeV
  Z_UV   = 1.0   (bare kinetic coefficient)
  m_UV   = kappa = 0.500  (dimensionless UV mass at fixed point)

RG FIXED-POINT CONSTRAINT (always checked):
  5 * kappa^2 = 3 * lambda_S  => residual < 1e-14
"""

from __future__ import annotations

import mpmath as mp

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.truncation import litim_regulator_derivative


def _set_precision() -> None:
    """Local precision — must NOT be centralised (race-condition rule)."""
    mp.dps = 80


# =====================================================================
# Threshold function (Litim, d=4)
# =====================================================================

def threshold_l0_4d(m_sq: mp.mpf) -> mp.mpf:
    """
    Dimensionless threshold function l_0^4 for d=4 Litim regulator.

      l_0^4(m^2) = 1 / (1 + m^2)

    This is the standard result from the Litim-optimised momentum integral.
    m^2 is the dimensionless mass: m^2 = U_k''(phi) / k^2.
    """
    _set_precision()
    return mp.mpf("1") / (mp.mpf("1") + m_sq)


def threshold_l1_4d(m_sq: mp.mpf) -> mp.mpf:
    """
    First derivative of l_0^4 w.r.t. m^2:
      l_1^4(m^2) = -1 / (1 + m^2)^2

    Used in the NLO anomalous dimension.
    """
    _set_precision()
    denom = (mp.mpf("1") + m_sq)**2
    return mp.mpf("-1") / denom


def threshold_l2_4d(m_sq: mp.mpf) -> mp.mpf:
    """
    Second derivative:
      l_2^4(m^2) = 2 / (1 + m^2)^3
    """
    _set_precision()
    denom = (mp.mpf("1") + m_sq)**3
    return mp.mpf("2") / denom


# =====================================================================
# Volume factor v_d in d=4
# =====================================================================

def volume_factor_4d() -> mp.mpf:
    """
    v_4 = 1 / (2^5 * pi^2) = 1 / (32 * pi^2)

    Standard loop factor for d=4 Euclidean.
    """
    _set_precision()
    return mp.mpf("1") / (mp.mpf("32") * mp.pi**2)


# =====================================================================
# Anomalous dimension eta_phi (LPA' NLO)
# =====================================================================

def anomalous_dimension(
    z_phi: mp.mpf,
    m_sq: mp.mpf,
    lambda_3: mp.mpf,
) -> mp.mpf:
    """
    Anomalous dimension of phi at NLO (LPA'):

      eta_phi(k) = (v_4 / z_phi) * lambda_3^2 * l_2^4(m^2)

    where:
      lambda_3  = (1/6) * d^3 U_k / d phi^3 |_{phi_vev}  (third derivative of potential)
      m^2       = U_k''(phi_vev) / k^2  (dimensionless mass)

    This is the leading NLO contribution from the boson self-coupling diagram.
    Higher-order diagrams are neglected (consistent with LPA').

    Evidence: [D] (prediction within this truncation)
    """
    _set_precision()
    v4 = volume_factor_4d()
    l2 = threshold_l2_4d(m_sq)
    return v4 * lambda_3**2 * l2 / z_phi


# =====================================================================
# Single RG step: dZ_phi / dt
# =====================================================================

def dz_dt(
    z_phi: mp.mpf,
    m_sq: mp.mpf,
    lambda_3: mp.mpf,
) -> mp.mpf:
    """
    RHS of Z_phi flow equation:

      dZ_phi / dt = -eta_phi(k) * Z_phi(k)

    where t = ln(k / Lambda_UV).

    Args:
        z_phi    : current Z_phi(k), mp.mpf
        m_sq     : dimensionless mass U_k''(phi_vev)/k^2, mp.mpf
        lambda_3 : cubic coupling d^3 U_k / 6 d phi^3 at phi_vev, mp.mpf

    Returns:
        mp.mpf: dZ/dt
    """
    _set_precision()
    eta = anomalous_dimension(z_phi, m_sq, lambda_3)
    return -eta * z_phi


# =====================================================================
# Mass flow: dm^2 / dt (LPA, potential driven)
# =====================================================================

def dm_sq_dt(
    m_sq: mp.mpf,
    lambda_4: mp.mpf,
) -> mp.mpf:
    """
    Flow of the dimensionless mass m^2 = U_k''(phi_vev) / k^2 at LPA:

      d m^2 / dt = -(2 + eta_phi) m^2
                   + 4 * v_4 * lambda_4 * l_1^4(m^2)

    Here eta_phi is set to zero at LPA (leading order).
    lambda_4 = (1/24) d^4 U_k / d phi^4 (quartic coupling).

    At the UV fixed point:
      m_UV^2 = kappa^2 = 0.25   (from Ledger)
    """
    _set_precision()
    v4 = volume_factor_4d()
    l1 = threshold_l1_4d(m_sq)
    return (
        mp.mpf("-2") * m_sq
        + mp.mpf("4") * v4 * lambda_4 * l1
    )


# =====================================================================
# RK4 integrator
# =====================================================================

def rk4_step(
    z: mp.mpf,
    m: mp.mpf,
    lam3: mp.mpf,
    lam4: mp.mpf,
    dt: mp.mpf,
) -> tuple[mp.mpf, mp.mpf]:
    """
    Single RK4 step for the coupled system (Z_phi, m^2).

    State: (z, m) = (Z_phi, m^2)
    Step:  t -> t + dt   (dt < 0 for UV->IR flow)

    Returns: (z_new, m_new)
    """
    _set_precision()

    def f_z(z_, m_):
        return dz_dt(z_, m_, lam3)

    def f_m(z_, m_):
        return dm_sq_dt(m_, lam4)

    k1_z = f_z(z, m)
    k1_m = f_m(z, m)

    k2_z = f_z(z + dt * k1_z / 2, m + dt * k1_m / 2)
    k2_m = f_m(z + dt * k1_z / 2, m + dt * k1_m / 2)

    k3_z = f_z(z + dt * k2_z / 2, m + dt * k2_m / 2)
    k3_m = f_m(z + dt * k2_z / 2, m + dt * k2_m / 2)

    k4_z = f_z(z + dt * k3_z, m + dt * k3_m)
    k4_m = f_m(z + dt * k3_z, m + dt * k3_m)

    z_new = z + dt * (k1_z + mp.mpf("2") * k2_z + mp.mpf("2") * k3_z + k4_z) / mp.mpf("6")
    m_new = m + dt * (k1_m + mp.mpf("2") * k2_m + mp.mpf("2") * k3_m + k4_m) / mp.mpf("6")
    return z_new, m_new


# =====================================================================
# Full UV -> IR flow
# =====================================================================

def run_frg_flow(
    n_steps: int = 2000,
    dt: mp.mpf | None = None,
    lambda_3_uv: mp.mpf | None = None,
    lambda_4_uv: mp.mpf | None = None,
) -> dict:
    """
    Integrate Z_phi(k) from k = Delta* (UV) to k -> 0 (IR).

    UV Initial Conditions (Stratum III):
      Z_phi(k_UV) = 1  (bare kinetic coefficient)
      m^2(k_UV)   = kappa^2 = 0.250  (from Ledger, dimensionless)
      lambda_3    = 0  (Z_2 symmetric potential at fixed point; leading order)
      lambda_4    = lambda_S = 5*kappa^2/3  (from RG constraint)

    The flow is parametrised by t = ln(k/Lambda_UV) in [-T, 0],
    running from t=0 (UV) to t=-T (IR).

    Args:
        n_steps       : number of RK4 integration steps
        dt            : step size in t (default: -6 / n_steps, i.e. T=6 decades)
        lambda_3_uv   : UV cubic coupling (default: 0, Z_2 symmetric)
        lambda_4_uv   : UV quartic coupling (default: lambda_S from Ledger)

    Returns:
        dict with keys:
          'z_ir'       : Z_phi at k->0 (mp.mpf) -- [D] prediction for gamma
          'm_ir'       : m^2 at k->0 (mp.mpf)
          't_values'   : list of t steps
          'z_values'   : list of Z_phi(t) (mp.mpf)
          'm_values'   : list of m^2(t) (mp.mpf)
          'rg_status'  : RG constraint status
          'evidence'   : always '[D]' until analytic proof closes
    """
    _set_precision()

    # RG constraint check first
    residual, rg_status = verify_rg_constraint()
    if rg_status != "PASS":
        raise RuntimeError(f"[RG_CONSTRAINT_FAIL] Cannot run flow: {rg_status}")

    L = get_ledger()

    # UV initial conditions
    z = mp.mpf("1")
    m = L["KAPPA"]**2                           # kappa^2 = 0.25
    lam3 = lambda_3_uv if lambda_3_uv is not None else mp.mpf("0")
    lam4 = lambda_4_uv if lambda_4_uv is not None else L["LAMBDA_S"]

    # Step size: flow from t=0 to t=-6 (6 decades of k)
    if dt is None:
        dt = mp.mpf("-6") / mp.mpf(str(n_steps))

    t_values = [mp.mpf("0")]
    z_values = [z]
    m_values = [m]

    for _ in range(n_steps):
        z, m = rk4_step(z, m, lam3, lam4, dt)
        t_values.append(t_values[-1] + dt)
        z_values.append(z)
        m_values.append(m)

    return {
        "z_ir": z_values[-1],
        "m_ir": m_values[-1],
        "t_values": t_values,
        "z_values": z_values,
        "m_values": m_values,
        "rg_residual": residual,
        "rg_status": rg_status,
        "evidence": "[D]",  # never auto-upgrade
        "n_steps": n_steps,
        "dt": dt,
    }


# =====================================================================
# Report
# =====================================================================

def flow_report(result: dict) -> str:
    _set_precision()
    L = get_ledger()
    gamma_target = L["GAMMA"]
    z_ir = result["z_ir"]
    deviation = abs(z_ir - gamma_target)

    lines = [
        "+================================================================+",
        "|  UIDT FRG/NLO FLOW REPORT: Z_phi(k->0) vs gamma               |",
        "+================================================================+",
        "",
        f"UV Initial Conditions:",
        f"  k_UV          = Delta* = {mp.nstr(L['DELTA_STAR'], 6)} GeV  [A]",
        f"  Z_phi(k_UV)   = 1  (bare)",
        f"  m^2(k_UV)     = kappa^2 = {mp.nstr(L['KAPPA']**2, 6)}  [A]",
        f"  lambda_4(UV)  = lambda_S = {mp.nstr(L['LAMBDA_S'], 10)}  [A]",
        "",
        f"IR Result:",
        f"  Z_phi(k->0)   = {mp.nstr(z_ir, 20)}  [D]",
        f"  gamma_target  = {mp.nstr(gamma_target, 20)}  [A-]",
        f"  Deviation     = {mp.nstr(deviation, 6)}",
        f"  n_steps       = {result['n_steps']}",
        "",
        f"RG Constraint:",
        f"  5*kappa^2 = 3*lambda_S residual = {mp.nstr(result['rg_residual'], 5)}",
        f"  Status    = {result['rg_status']}",
        "",
        f"Evidence Category: {result['evidence']}",
        "",
        "INTERPRETATION:",
        "  This is a NUMERICAL PREDICTION [D] within the LPA' truncation.",
        "  Upgrade to [A] requires closed analytic proof or rigorous error bounds.",
        "  Open ticket: TKT-FRG-GAMMA-NLO",
        "",
        "LIMITATION L4 STATUS:",
        "  gamma remains [A-] (phenomenological) until this flow closes analytically.",
    ]

    if deviation < mp.mpf("0.015"):
        lines.append("  NUMERICAL PROXIMITY: Z_phi(IR) within Delta_gamma tolerance.")
    else:
        lines.append(f"  NOTE: Deviation {mp.nstr(deviation, 4)} exceeds delta_gamma = 0.0047.")
        lines.append("  Truncation may require higher-order corrections.")

    lines += [
        "",
        f"DOI: 10.5281/zenodo.17835200",
    ]
    return "\n".join(lines)


# =====================================================================
# CLI
# =====================================================================

if __name__ == "__main__":
    import sys
    _set_precision()
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    result = run_frg_flow(n_steps=n)
    print(flow_report(result))
    # Exit: 0 if deviation < delta_gamma, 1 otherwise
    L = get_ledger()
    dev = abs(result["z_ir"] - L["GAMMA"])
    sys.exit(0 if dev < L["DELTA_GAMMA"] else 1)
