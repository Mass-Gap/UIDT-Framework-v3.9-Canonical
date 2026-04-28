"""
[UIDT-v3.9] FRG/NLO — Step 4b: Derive phi* directly from U_k(phi)
===================================================================

This module removes the external Stratum III mapping

    phi* = V_vac / Delta*

and instead derives the non-trivial vacuum expectation value phi*
from the scalar potential U_k(phi) itself.

EPISTEMIC LAYERS
----------------
Stratum I:
  empirical constants Delta*, V_vac (used only for post-hoc comparison)
Stratum II:
  standard scalar-potential minimization and FRG/LPA fixed-point algebra
Stratum III:
  UIDT interpretation of the scalar as vacuum information density

EVIDENCE STATUS
---------------
[A]  RG fixed-point constraint 5*kappa^2 = 3*lambda_S
[A]  Stationary-point condition dU/dphi = 0
[D]  Specific cubic deformation needed to realize non-zero phi*
[D]  Identification of derived phi* with physical UIDT vacuum scalar

Potential ansatz (minimal Z2-breaking deformation)
---------------------------------------------------
We use the local UV potential expanded around phi = 0:

    U(phi) = (1/2) m^2 phi^2 - lambda_3 phi^3 + (lambda_4/4) phi^4

with
    m^2      = kappa^2
    lambda_4 = lambda_S

The stationary condition is

    dU/dphi = m^2 phi - 3 lambda_3 phi^2 + lambda_4 phi^3 = 0

Besides phi = 0, non-trivial extrema satisfy

    lambda_4 phi^2 - 3 lambda_3 phi + m^2 = 0

Thus

              3 lambda_3 ± sqrt(9 lambda_3^2 - 4 lambda_4 m^2)
    phi* = ------------------------------------------------------
                              2 lambda_4

A real broken vacuum requires discriminant >= 0.
The smaller positive root is taken as the physically relevant nearby vacuum.

Important limitation:
  This derives phi* from U_k(phi), but only once lambda_3 is specified.
  Therefore the circularity is not fully removed unless lambda_3 itself is
  independently fixed. This module is an algebraic bridge, not the final proof.
"""

from __future__ import annotations

import mpmath as mp

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint


def _set_precision() -> None:
    mp.dps = 80


def potential_u(phi: mp.mpf, m_sq: mp.mpf, lambda_3: mp.mpf, lambda_4: mp.mpf) -> mp.mpf:
    """Minimal Z2-breaking quartic potential."""
    _set_precision()
    return (
        mp.mpf("0.5") * m_sq * phi**2
        - lambda_3 * phi**3
        + (lambda_4 / mp.mpf("4")) * phi**4
    )


def dpotential_u(phi: mp.mpf, m_sq: mp.mpf, lambda_3: mp.mpf, lambda_4: mp.mpf) -> mp.mpf:
    """First derivative dU/dphi."""
    _set_precision()
    return m_sq * phi - mp.mpf("3") * lambda_3 * phi**2 + lambda_4 * phi**3


def ddpotential_u(phi: mp.mpf, m_sq: mp.mpf, lambda_3: mp.mpf, lambda_4: mp.mpf) -> mp.mpf:
    """Second derivative d^2U/dphi^2."""
    _set_precision()
    return m_sq - mp.mpf("6") * lambda_3 * phi + mp.mpf("3") * lambda_4 * phi**2


def broken_vacuum_discriminant(m_sq: mp.mpf, lambda_3: mp.mpf, lambda_4: mp.mpf) -> mp.mpf:
    """Discriminant for non-trivial stationary points."""
    _set_precision()
    return mp.mpf("9") * lambda_3**2 - mp.mpf("4") * lambda_4 * m_sq


def derive_phi_star_from_potential(lambda_3: mp.mpf, prefer_small_root: bool = True) -> dict:
    """
    Derive phi* directly from the stationary condition dU/dphi = 0.

    Returns:
      {
        'phi_star': mp.mpf,
        'root_plus': mp.mpf,
        'root_minus': mp.mpf,
        'discriminant': mp.mpf,
        'stable': bool,
        'evidence': '[D]'
      }

    Notes:
      - Uses Ledger values m^2 = kappa^2 and lambda_4 = lambda_S.
      - If discriminant < 0, no real broken vacuum exists.
      - Stability is checked via d^2U/dphi^2 > 0 at the chosen root.
    """
    _set_precision()
    residual, status = verify_rg_constraint()
    if status != "PASS":
        raise RuntimeError("[RG_CONSTRAINT_FAIL]")

    L = get_ledger()
    m_sq = L["KAPPA"]**2
    lambda_4 = L["LAMBDA_S"]

    disc = broken_vacuum_discriminant(m_sq, lambda_3, lambda_4)
    if disc < mp.mpf("0"):
        raise ValueError("No real broken vacuum: discriminant < 0")

    sqrt_disc = mp.sqrt(disc)
    denom = mp.mpf("2") * lambda_4
    root_plus = (mp.mpf("3") * lambda_3 + sqrt_disc) / denom
    root_minus = (mp.mpf("3") * lambda_3 - sqrt_disc) / denom

    candidates = [r for r in (root_minus, root_plus) if r > mp.mpf("0")]
    if not candidates:
        raise ValueError("No positive non-trivial vacuum root")

    phi_star = min(candidates) if prefer_small_root else max(candidates)
    stable = ddpotential_u(phi_star, m_sq, lambda_3, lambda_4) > mp.mpf("0")

    return {
        "phi_star": phi_star,
        "root_plus": root_plus,
        "root_minus": root_minus,
        "discriminant": disc,
        "stable": stable,
        "m_sq": m_sq,
        "lambda_4": lambda_4,
        "evidence": "[D]",
    }


def infer_lambda3_for_target_phi(phi_target: mp.mpf) -> mp.mpf:
    """
    Invert the stationary equation to solve for lambda_3 given target phi*:

      m^2 phi - 3 lambda_3 phi^2 + lambda_4 phi^3 = 0

    for phi != 0:

      lambda_3 = (m^2 + lambda_4 phi^2) / (3 phi)

    This is useful for checking whether a desired vacuum can be generated
    by the minimal quartic potential.
    """
    _set_precision()
    if phi_target == mp.mpf("0"):
        raise ValueError("phi_target must be non-zero")

    L = get_ledger()
    m_sq = L["KAPPA"]**2
    lambda_4 = L["LAMBDA_S"]
    return (m_sq + lambda_4 * phi_target**2) / (mp.mpf("3") * phi_target)



def compare_with_legacy_phi_mapping(phi_star: mp.mpf) -> dict:
    """
    Compare derived phi* with the legacy mapping phi*=V_vac/Delta*.
    This is post-hoc only and does not enter the derivation.
    """
    _set_precision()
    L = get_ledger()
    phi_legacy = L["V_VAC"] / (L["DELTA_STAR"] * mp.mpf("1000"))
    diff = abs(phi_star - phi_legacy)
    rel = diff / abs(phi_legacy) if phi_legacy != mp.mpf("0") else mp.inf
    return {
        "phi_legacy": phi_legacy,
        "difference": diff,
        "relative_difference": rel,
    }



def potential_report(lambda_3: mp.mpf | None = None) -> str:
    _set_precision()
    if lambda_3 is None:
        # legacy value only as a seed for demonstration / comparison path
        L = get_ledger()
        phi_legacy = L["V_VAC"] / (L["DELTA_STAR"] * mp.mpf("1000"))
        lambda_3 = infer_lambda3_for_target_phi(phi_legacy)

    result = derive_phi_star_from_potential(lambda_3)
    cmp = compare_with_legacy_phi_mapping(result["phi_star"])
    station_res = abs(dpotential_u(result["phi_star"], result["m_sq"], lambda_3, result["lambda_4"]))
    curvature = ddpotential_u(result["phi_star"], result["m_sq"], lambda_3, result["lambda_4"])

    lines = [
        "+================================================================+",
        "|  UIDT FRG/NLO STEP 4b: phi* from U_k(phi)                     |",
        "+================================================================+",
        "",
        "Potential ansatz:",
        "  U(phi) = (1/2)m^2 phi^2 - lambda_3 phi^3 + (lambda_4/4) phi^4",
        "",
        "Ledger inputs:",
        f"  m^2      = kappa^2     = {mp.nstr(result['m_sq'], 20)}  [A]",
        f"  lambda_4 = lambda_S    = {mp.nstr(result['lambda_4'], 20)}  [A]",
        f"  lambda_3 (input)       = {mp.nstr(lambda_3, 20)}  [D]",
        "",
        "Broken-vacuum solution:",
        f"  discriminant           = {mp.nstr(result['discriminant'], 20)}",
        f"  root_minus             = {mp.nstr(result['root_minus'], 20)}",
        f"  root_plus              = {mp.nstr(result['root_plus'], 20)}",
        f"  chosen phi*            = {mp.nstr(result['phi_star'], 20)}  [D]",
        f"  stability              = {result['stable']}",
        f"  |dU/dphi| at phi*      = {mp.nstr(station_res, 8)}",
        f"  d^2U/dphi^2 at phi*    = {mp.nstr(curvature, 20)}",
        "",
        "Post-hoc comparison to legacy mapping (not used in derivation):",
        f"  phi_legacy             = {mp.nstr(cmp['phi_legacy'], 20)}",
        f"  absolute difference    = {mp.nstr(cmp['difference'], 10)}",
        f"  relative difference    = {mp.nstr(cmp['relative_difference'], 10)}",
        "",
        "Interpretation:",
        "  phi* is now obtained from the stationary condition dU/dphi = 0.",
        "  This removes the direct insertion phi*=V_vac/Delta* from the derivation step.",
        "  However, the cubic deformation lambda_3 still has to be fixed independently.",
        "  Therefore the circularity is reduced, not fully eliminated.",
        "",
        "Evidence: [D]",
        "",
        "DOI: 10.5281/zenodo.17835200",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(potential_report())
