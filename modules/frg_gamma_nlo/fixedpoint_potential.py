"""
[UIDT-v3.9] FRG/NLO — Step 4: Fixed-Point Potential Analysis + lambda_3(UV)
=============================================================================

STRATUM ASSIGNMENT:
  Stratum I  : potential shape constraints from UV fixed point (measurable)
  Stratum II : standard FRG fixed-point equations (LPA, established)
  Stratum III: identification of Z_2-breaking VEV with UIDT vacuum phi*

EPISTEMIC STATUS:
  [A]  RG constraint 5*kappa^2 = 3*lambda_S (Theorem 2)
  [A]  LPA fixed-point equation structure (standard FRG, Stratum II)
  [D]  Identification phi* = V_vac / Delta* (UIDT Stratum III conjecture)
  [D]  Resulting lambda_3(UV) value

OPEN QUESTION (this module):
  The LPA' flow requires lambda_3 = (1/6) d^3 U_k / d phi^3 |_{phi_vev} != 0
  to produce non-trivial Z_phi(IR) != 1.

  At the Z_2-symmetric fixed point lambda_3 = 0 by symmetry.
  Physical relevance requires Z_2 breaking via a non-zero VEV phi*.

  This module derives lambda_3(UV) from the fixed-point potential U*(phi)
  expanded around the UIDT vacuum expectation value phi*.

FIXED-POINT POTENTIAL (LPA, d=4):

  The LPA fixed-point equation (t-derivative = 0) reads:

    0 = -4 U* + 2 phi * dU*/dphi + (v_4 / (1 + U*''))

  where primes denote derivatives with respect to phi, and
  v_4 = 1/(32*pi^2).

  Expanding U*(phi) around the VEV phi* in Taylor series:

    U*(phi) = sum_{n=0}^{N} a_n * (phi - phi*)^n / n!

  The couplings are:
    a_0 = U*(phi*)         (potential at VEV)
    a_1 = U*'(phi*) = 0    (VEV condition: first derivative vanishes)
    a_2 = U*''(phi*)       = m_phi^2 * k^2  (mass term; at k=Delta*: a_2 = kappa^2)
    a_3 = U*'''(phi*)      = 3! * lambda_3  (cubic coupling: Z_2 breaking)
    a_4 = U*''''(phi*)     = 4! * lambda_4  (quartic: = lambda_S at fixed point)

VEV IDENTIFICATION (Stratum III, [D]):

  UIDT identifies the vacuum scalar VEV with:
    phi* = V_vac / Delta*

  where:
    V_vac  = 47.7 MeV  [A]  (UIDT vacuum expectation value)
    Delta* = 1710 MeV  [A]  (spectral gap, same units)

  => phi* = 47.7 / 1710 = 0.027895...  (dimensionless, [D])

  The non-zero VEV phi* != 0 signals spontaneous Z_2 breaking.
  Differentiating U*(phi) three times at phi = phi* then yields
  lambda_3(UV) != 0.

DERIVATION OF lambda_3(UV):

  From the fixed-point equation differentiated w.r.t. phi at phi = phi*:

    d/dphi [LPA FP eq] gives a relation between a_2, a_3, phi*, v_4.

  Specifically (see fixed_point_derivative_relation() below):

    a_3 = a_2 * (3 - 2*phi* * a_2_deriv) / phi*

  At leading order in phi* << 1:
    a_3 ~ a_2 / phi*  * (correction factor)

  The precise value is computed numerically with mp.mpf at 80 digits.

LIMITATION:
  phi* is identified via Stratum III mapping [D].
  lambda_3(UV) therefore carries evidence [D].
  This is the weakest link in the current derivation chain.
"""

from __future__ import annotations

import mpmath as mp

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.flow_equations import volume_factor_4d, threshold_l1_4d


def _set_precision() -> None:
    """Local precision — must NOT be centralised (race-condition rule)."""
    mp.dps = 80


# =====================================================================
# VEV identification (Stratum III, [D])
# =====================================================================

def compute_phi_vev() -> mp.mpf:
    """
    Compute the dimensionless UIDT vacuum scalar VEV.

      phi* = V_vac / Delta*

    Uses Ledger values V_vac = 47.7 MeV, Delta* = 1710 MeV.

    Evidence: [D] (Stratum III identification; V_vac and Delta* are [A])

    Returns:
        mp.mpf: phi* (dimensionless)
    """
    _set_precision()
    L = get_ledger()
    # Both in MeV for consistent dimensionless ratio
    v_mev = L["V_VAC"]                     # 47.7 MeV [A]
    delta_mev = L["DELTA_STAR"] * mp.mpf("1000")  # 1710 MeV [A]
    phi_star = v_mev / delta_mev
    return phi_star


# =====================================================================
# LPA fixed-point equation and its derivatives
# =====================================================================

def lpa_fixedpoint_rhs(
    phi: mp.mpf,
    u_val: mp.mpf,
    u_pp: mp.mpf,
) -> mp.mpf:
    """
    RHS of the LPA fixed-point equation in d=4:

      F(phi) = -4 U* + 2 phi * U*' + v_4 / (1 + U*'')

    At the fixed point F = 0.

    Args:
        phi   : field value, mp.mpf
        u_val : U*(phi), mp.mpf
        u_pp  : U*''(phi) = d^2 U* / d phi^2, mp.mpf

    Note:
        U*' = dU*/dphi.  At the VEV phi*, U*' = 0 by definition.
        This function is used to verify the VEV condition.
    """
    _set_precision()
    v4 = volume_factor_4d()
    # U*' = 0 at VEV; for general phi pass u_p separately if needed.
    # Here we compute only the VEV-specific form (u_p = 0).
    u_p = mp.mpf("0")  # VEV condition
    return (
        mp.mpf("-4") * u_val
        + mp.mpf("2") * phi * u_p
        + v4 / (mp.mpf("1") + u_pp)
    )


def fixed_point_mass(
    phi_star: mp.mpf,
    kappa: mp.mpf,
) -> mp.mpf:
    """
    Dimensionless squared mass at the UV fixed point.

      m^2_UV = kappa^2

    This is the a_2 coefficient in the Taylor expansion of U* around phi*.
    Directly from the Ledger: kappa = 0.500, so m^2_UV = 0.250.

    Evidence: [A]
    """
    _set_precision()
    return kappa**2


def fixed_point_derivative_relation(
    phi_star: mp.mpf,
    m_sq: mp.mpf,
    lambda_4: mp.mpf,
) -> mp.mpf:
    """
    Derive lambda_3(UV) from the first-order consistency condition
    of the LPA fixed-point equation differentiated at phi = phi*.

    The LPA fixed-point equation differentiated w.r.t. phi at phi = phi*
    (using U*' = 0, U*'' = m^2) gives:

      d/dphi F |_{phi*} = 0

      -4 U*' + 2 U*' + 2 phi* U*'' + v_4 * (-U*''' / (1+m^2)^2) = 0
      -2 * 0  + 2 phi* m^2 - v_4 * a_3 / (1 + m^2)^2 = 0

    Solving for a_3 = U*'''(phi*) = 3! * lambda_3:

      a_3 = 2 phi* m^2 * (1 + m^2)^2 / v_4

    Therefore:
      lambda_3 = a_3 / 6 = phi* * m^2 * (1 + m^2)^2 / (3 * v_4)

    Evidence: [D] (depends on phi* identification)

    Args:
        phi_star : dimensionless VEV phi*, mp.mpf  [D]
        m_sq     : dimensionless m^2 at UV, mp.mpf  [A]
        lambda_4 : quartic coupling at UV (unused at this order), mp.mpf  [A]

    Returns:
        mp.mpf: lambda_3(UV)  [D]
    """
    _set_precision()
    v4 = volume_factor_4d()
    one_plus_m = mp.mpf("1") + m_sq
    # a_3 = U*'''(phi*)
    a_3 = mp.mpf("2") * phi_star * m_sq * one_plus_m**2 / v4
    # lambda_3 = a_3 / 3!  (Taylor convention: U* = sum a_n (phi-phi*)^n / n!)
    lambda_3 = a_3 / mp.mpf("6")
    return lambda_3


# =====================================================================
# Full UV coupling set
# =====================================================================

def derive_uv_couplings() -> dict:
    """
    Derive the complete set of UV initial conditions for the FRG flow.

    Returns a dict with:
      phi_star   : dimensionless VEV  [D]
      m_sq_uv    : kappa^2  [A]
      lambda_3   : cubic coupling at UV  [D]
      lambda_4   : lambda_S = 5*kappa^2/3  [A]
      rg_residual: 5*kappa^2 - 3*lambda_S  [A]
      evidence   : '[D]'  (phi_star identification is weakest link)
    """
    _set_precision()
    residual, rg_status = verify_rg_constraint()
    if rg_status != "PASS":
        raise RuntimeError(f"[RG_CONSTRAINT_FAIL] {rg_status}")

    L = get_ledger()
    phi_star = compute_phi_vev()
    m_sq = fixed_point_mass(phi_star, L["KAPPA"])
    lambda_3 = fixed_point_derivative_relation(phi_star, m_sq, L["LAMBDA_S"])

    return {
        "phi_star":    phi_star,
        "m_sq_uv":     m_sq,
        "lambda_3":    lambda_3,
        "lambda_4":    L["LAMBDA_S"],
        "rg_residual": residual,
        "rg_status":   rg_status,
        "evidence":    "[D]",
    }


# =====================================================================
# Consistency check: LPA FP equation at phi*
# =====================================================================

def verify_fixedpoint_consistency(couplings: dict) -> tuple[mp.mpf, str]:
    """
    Verify the LPA fixed-point equation is approximately satisfied at phi*.

      F(phi*) = -4 U*(phi*) + v_4 / (1 + m^2)

    U*(phi*) is estimated from the fixed-point condition integrated
    from phi=0 to phi=phi* at leading order:

      U*(phi*) ~ (1/2) m^2 phi*^2  (harmonic approximation)

    The residual F(phi*) / (v_4/(1+m^2)) measures relative deviation
    from the fixed point.  For phi* << 1 this is small.

    Returns:
        (relative_residual, status)
    """
    _set_precision()
    v4 = volume_factor_4d()
    phi_star = couplings["phi_star"]
    m_sq = couplings["m_sq_uv"]

    # Leading-order estimate of U*(phi*)
    u_star = mp.mpf("0.5") * m_sq * phi_star**2

    f_val = lpa_fixedpoint_rhs(phi_star, u_star, m_sq)
    ref = v4 / (mp.mpf("1") + m_sq)
    relative_residual = abs(f_val) / abs(ref)

    if relative_residual < mp.mpf("0.1"):
        status = "CONSISTENT"
    else:
        status = "LARGE_RESIDUAL"

    return relative_residual, status


# =====================================================================
# Report
# =====================================================================

def fixedpoint_report(couplings: dict | None = None) -> str:
    _set_precision()
    if couplings is None:
        couplings = derive_uv_couplings()

    rel_res, fp_status = verify_fixedpoint_consistency(couplings)

    lines = [
        "+================================================================+",
        "|  UIDT FRG/NLO STEP 4: Fixed-Point Potential + lambda_3(UV)    |",
        "+================================================================+",
        "",
        "STRATUM III VEV IDENTIFICATION [D]:",
        f"  V_vac    = 47.7 MeV          [A]",
        f"  Delta*   = 1710.0 MeV        [A]",
        f"  phi*     = V_vac / Delta*    [D]",
        f"           = {mp.nstr(couplings['phi_star'], 20)}",
        "",
        "UV FIXED-POINT COUPLINGS:",
        f"  m^2_UV   = kappa^2           [A]",
        f"           = {mp.nstr(couplings['m_sq_uv'], 20)}",
        f"  lambda_4 = lambda_S          [A]",
        f"           = {mp.nstr(couplings['lambda_4'], 20)}",
        f"  lambda_3 = phi* m^2(1+m^2)^2 / (3*v_4)  [D]",
        f"           = {mp.nstr(couplings['lambda_3'], 20)}",
        "",
        "FIXED-POINT CONSISTENCY (LPA, harmonic approx):",
        f"  Relative residual F(phi*)/ref = {mp.nstr(rel_res, 6)}",
        f"  Status                        = {fp_status}",
        "",
        f"RG CONSTRAINT:",
        f"  5*kappa^2 = 3*lambda_S residual = {mp.nstr(couplings['rg_residual'], 5)}",
        f"  Status = {couplings['rg_status']}",
        "",
        f"Evidence: {couplings['evidence']}",
        "",
        "INTERPRETATION:",
        "  phi* != 0 signals spontaneous Z_2 breaking in U_k.",
        "  lambda_3(UV) != 0 enables non-trivial Z_phi(IR) > 1 in the FRG flow.",
        "  The weakest link is the Stratum III identification phi* = V_vac/Delta*.",
        "  Until this is derived from first principles, lambda_3 remains [D].",
        "",
        "NEXT STEP:",
        "  Pass lambda_3(UV) into flow_equations.run_frg_flow() and verify",
        f"  that Z_phi(IR) approaches gamma = 16.339.",
        "",
        "DOI: 10.5281/zenodo.17835200",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(fixedpoint_report())
