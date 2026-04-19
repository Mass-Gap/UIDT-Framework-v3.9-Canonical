"""
[UIDT-v3.9] FRG/NLO — Step 2: LPA' Truncation + Regulator
===========================================================

STRATUM ASSIGNMENT:
  Stratum I  : choice of regulator shape (methodological)
  Stratum II : standard LPA' (NLO local potential approximation) in FRG
  Stratum III: projection of UIDT scalar Z_phi(k) onto kinetic term

EPISTEMIC STATUS:
  [D] Prediction: Z_phi(k -> 0) = gamma = 16.339
  [A] RG constraint: 5*kappa^2 = 3*lambda_S maintained throughout flow

TRUNCATION SCHEME (LPA' = NLO):

  The ansatz for the effective average action is:

    Gamma_k[phi] = int d^4x  [ (Z_phi(k)/2)(d_mu phi)^2 + U_k(phi) ]

  This is the NLO (LPA') truncation:
    - LPA  (LO):  Z_phi = 1 (frozen)
    - LPA' (NLO): Z_phi(k) running; captures anomalous dimension eta_phi

  The anomalous dimension is defined as:
    eta_phi(k) = -d ln Z_phi / d ln k

  Physical gamma is recovered in the IR:
    gamma := Z_phi(k -> 0)

REGULATOR:
  Litim optimised regulator (3d or 4d) is the default choice here.
  Callan-Symanzik regulator is provided as an alternative.

  Litim (4d):
    R_k(p^2) = Z_phi(k) * (k^2 - p^2) * theta(k^2 - p^2)

  Callan-Symanzik:
    R_k(p^2) = Z_phi(k) * k^2

Limitation:
  This module defines regulator functions numerically (mpf).
  The full flow integral over loop momentum is computed in flow_equations.py.
  No float() used; all arithmetic is mp.mpf at 80 digits.
"""

from __future__ import annotations
import mpmath as mp


def _set_precision() -> None:
    mp.dps = 80


# =====================================================================
# Regulator functions
# =====================================================================

def litim_regulator(p_sq: mp.mpf, k_sq: mp.mpf, z_phi: mp.mpf) -> mp.mpf:
    """
    Litim optimised regulator (4d):
      R_k(p^2) = Z_phi * (k^2 - p^2) * theta(k^2 - p^2)

    Args:
        p_sq   : p^2 (Euclidean momentum squared), mp.mpf
        k_sq   : k^2 (RG scale squared), mp.mpf
        z_phi  : running kinetic coefficient Z_phi(k), mp.mpf

    Returns:
        mp.mpf: regulator value at (p^2, k^2)
    """
    _set_precision()
    if p_sq >= k_sq:
        return mp.mpf("0")
    return z_phi * (k_sq - p_sq)


def callan_symanzik_regulator(k_sq: mp.mpf, z_phi: mp.mpf) -> mp.mpf:
    """
    Callan-Symanzik regulator:
      R_k = Z_phi * k^2

    Momentum-independent; simple but less accurate for non-perturbative flows.
    """
    _set_precision()
    return z_phi * k_sq


def litim_regulator_derivative(p_sq: mp.mpf, k_sq: mp.mpf, z_phi: mp.mpf) -> mp.mpf:
    """
    k * d R_k / d k  for Litim regulator:
      = 2 * Z_phi * k^2 * theta(k^2 - p^2)

    This appears in the Wetterich flow equation RHS.
    """
    _set_precision()
    if p_sq >= k_sq:
        return mp.mpf("0")
    return mp.mpf("2") * z_phi * k_sq


# =====================================================================
# LPA' projection scheme
# =====================================================================

def project_kinetic_coefficient(
    gamma_effective_action: mp.mpf,
    phi_vev: mp.mpf,
) -> mp.mpf:
    """
    Extract Z_phi(k) from Gamma_k by projecting onto the kinetic operator.

    At the level of LPA', Z_phi(k) is read off as the coefficient of
    (1/2)(d_mu phi)^2 evaluated at phi = phi_vev (vacuum field value).

    Args:
        gamma_effective_action : second functional derivative of Gamma_k
                                 with respect to momentum p^2, at p^2 = 0
                                 and phi = phi_vev, divided by Z_phi_bare.
                                 Passed as mp.mpf.
        phi_vev               : vacuum field value phi* in appropriate units (mp.mpf)

    Returns:
        mp.mpf: Z_phi(k) at this RG scale

    Note:
        In a numerical implementation the caller computes:
          Z_phi(k) = d/d(p^2) Gamma_k^(2)(p^2, phi_vev) |_{p^2=0}
        This function serves as the projection definition; the actual
        computation is performed in flow_equations.py.
    """
    _set_precision()
    # Projection: Z_phi is the p^2 coefficient of Gamma_k^(2).
    # gamma_effective_action here IS that coefficient (caller responsibility).
    return gamma_effective_action


# =====================================================================
# Self-test
# =====================================================================

def truncation_selftest() -> str:
    """Verify regulator arithmetic at a fixed test point."""
    _set_precision()
    k_sq   = mp.mpf("1.710")**2    # k = Delta* = 1.710 GeV (UV start)
    p_sq_a = mp.mpf("1.000")**2    # inside Litim window
    p_sq_b = mp.mpf("2.000")**2    # outside Litim window
    z_test = mp.mpf("1")           # bare kinetic coefficient at UV

    r_a = litim_regulator(p_sq_a, k_sq, z_test)
    r_b = litim_regulator(p_sq_b, k_sq, z_test)
    dr_a = litim_regulator_derivative(p_sq_a, k_sq, z_test)
    r_cs = callan_symanzik_regulator(k_sq, z_test)

    lines = [
        "LPA' Truncation Self-Test",
        "=========================",
        f"k = Delta* = {mp.nstr(mp.sqrt(k_sq), 6)} GeV (UV initial scale)",
        f"Litim R_k(p^2=1.0^2) = {mp.nstr(r_a, 10)}  (expected > 0)",
        f"Litim R_k(p^2=2.0^2) = {mp.nstr(r_b, 4)}  (expected 0)",
        f"Litim dR/dk(p^2=1.0^2) = {mp.nstr(dr_a, 10)}",
        f"Callan-Symanzik R_k     = {mp.nstr(r_cs, 10)}",
    ]

    # Sanity checks (no float, no round)
    assert r_b == mp.mpf("0"), f"[TRUNCATION_FAIL] Litim outside window != 0: {r_b}"
    assert r_a > mp.mpf("0"),  f"[TRUNCATION_FAIL] Litim inside window <= 0: {r_a}"

    lines.append("Status: PASS")
    return "\n".join(lines)


if __name__ == "__main__":
    print(truncation_selftest())
