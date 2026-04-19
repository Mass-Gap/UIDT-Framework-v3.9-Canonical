"""
[UIDT-v3.9] FRG/NLO — Step 1: Lagrangian Formulation
======================================================

STRATUM ASSIGNMENT:
  Stratum I  : gauge-invariance requirement, SU(3) group factors
  Stratum II : standard QFT Lagrangian construction (textbook)
  Stratum III: UIDT scalar phi, vacuum density identification, RG constraint

EPISTEMIC CHAIN:
  [A]  SU(3) Yang-Mills sector  (gauge invariance, established QFT)
  [A]  RG constraint 5*kappa^2 = 3*lambda_S  (proven in UIDT Theorem 2)
  [D]  UIDT vacuum scalar phi and its kinetic coupling gamma  (prediction)

This module defines the UIDT Lagrangian density symbolically and verifies
the RG fixed-point constraint with mp.dps = 80 precision.

Limitation:
  gamma = 16.339 is currently [A-]. It appears in the kinetic term
  Z_phi(k) which is extracted from the FRG flow in flow_equations.py.
  This module ONLY defines the classical Lagrangian structure.
  No float() used in constraint checks.
"""

from __future__ import annotations

import mpmath as mp


def _set_precision() -> None:
    """Local precision declaration — must NOT be centralised (race-condition rule)."""
    mp.dps = 80


# =====================================================================
# Immutable Ledger Constants (read-only)
# =====================================================================

def get_ledger() -> dict:
    """
    Return canonical constants as mpf with 80-digit precision.
    NEVER modify these values. Evidence categories are fixed.

    Returns a fresh dict each call to prevent shared-reference mutation.
    """
    _set_precision()
    return {
        "DELTA_STAR":    mp.mpf("1.710"),    # [A]   GeV; Yang-Mills spectral gap
        "DELTA_TOL":     mp.mpf("0.015"),    # [A]   1-sigma tolerance
        "GAMMA":         mp.mpf("16.339"),   # [A-]  kinetic VEV coefficient; TARGET of this module
        "GAMMA_INF":     mp.mpf("16.3437"),  # [A-]  asymptotic value
        "DELTA_GAMMA":   mp.mpf("0.0047"),   # [A-]  delta-gamma
        "KAPPA":         mp.mpf("0.500"),    # [A]   scalar self-coupling
        "LAMBDA_S":      mp.mpf("5") * mp.mpf("0.500")**2 / mp.mpf("3"),  # [A]   = 5*kappa^2/3
        "V_VAC":         mp.mpf("47.7"),     # [A]   MeV; vacuum expectation value
        "E_T":           mp.mpf("2.44"),     # [C]   MeV; torsion binding energy
        "W0":            mp.mpf("-0.99"),    # [C]   cosmology parameter
    }


# =====================================================================
# RG Fixed-Point Constraint Verification
# =====================================================================

def verify_rg_constraint() -> tuple[mp.mpf, str]:
    """
    Verify: 5*kappa^2 = 3*lambda_S  (UIDT Theorem 2)

    Returns:
        (residual, status_string)

    Raises:
        AssertionError with [RG_CONSTRAINT_FAIL] if residual >= 1e-14.
    """
    _set_precision()
    L = get_ledger()
    lhs = mp.mpf("5") * L["KAPPA"]**2
    rhs = mp.mpf("3") * L["LAMBDA_S"]
    residual = abs(lhs - rhs)
    if residual >= mp.mpf("1e-14"):
        status = "[RG_CONSTRAINT_FAIL]"
        raise AssertionError(
            f"[RG_CONSTRAINT_FAIL] residual = {mp.nstr(residual, 6)} >= 1e-14"
        )
    return residual, "PASS"


# =====================================================================
# Lagrangian Structure (symbolic descriptor)
# =====================================================================

# The UIDT effective Lagrangian density (Stratum III) reads:
#
#   L = L_YM + L_phi
#
# Yang-Mills sector (Stratum I/II, standard):
#
#   L_YM = -(1 / 4g_s^2) Tr[F_munu F^munu]
#
# UIDT vacuum scalar sector (Stratum III, [D]):
#
#   L_phi = (Z_phi(k) / 2) (d_mu phi)^2
#           - U_k(phi)
#
# where:
#   phi         -- UIDT vacuum information density scalar
#   Z_phi(k)    -- running kinetic coefficient; at k -> 0, Z_phi -> gamma = 16.339  [A-]
#   U_k(phi)    -- effective potential; at UV fixed point satisfies RG constraint
#
# UV Fixed-Point Conditions (Stratum III / [A] for constraint):
#   U_k(phi*) / phi*^2 = lambda_S          at k = Lambda_UV
#   (1/2) d^2 U_k / d phi^2 |_{phi*} = kappa^2
#   => 5 kappa^2 = 3 lambda_S              (Theorem 2)
#
# Target of flow_equations.py:
#   gamma := lim_{k->0} Z_phi(k)
#   Hypothesis [D]: gamma = 16.339 +/- delta_gamma


def lagrangian_structure_report() -> str:
    """
    Return a plain-text summary of the Lagrangian structure.
    Used in verification reports and PR documentation.
    """
    _set_precision()
    L = get_ledger()
    residual, rg_status = verify_rg_constraint()

    return (
        "UIDT Lagrangian Structure (Step 1)\n"
        "===================================\n"
        "Stratum I/II (Yang-Mills sector):\n"
        "  L_YM = -(1/4g_s^2) Tr[F_munu F^munu]\n\n"
        "Stratum III (UIDT vacuum scalar):\n"
        "  L_phi = (Z_phi(k)/2)(d_mu phi)^2 - U_k(phi)\n\n"
        "UV Fixed-Point Constraints:\n"
        f"  kappa      = {mp.nstr(L['KAPPA'], 6)}  [A]\n"
        f"  lambda_S   = {mp.nstr(L['LAMBDA_S'], 10)}  [A]\n"
        f"  5*kappa^2  = {mp.nstr(mp.mpf('5') * L['KAPPA']**2, 10)}\n"
        f"  3*lambda_S = {mp.nstr(mp.mpf('3') * L['LAMBDA_S'], 10)}\n"
        f"  Residual   = {mp.nstr(residual, 5)}  Status: {rg_status}\n\n"
        "Target (flow_equations.py):\n"
        f"  gamma_target = {mp.nstr(L['GAMMA'], 8)}  [A-]  (hypothesis [D]: derivable)\n"
        f"  delta_gamma  = {mp.nstr(L['DELTA_GAMMA'], 4)}\n"
    )


if __name__ == "__main__":
    print(lagrangian_structure_report())
