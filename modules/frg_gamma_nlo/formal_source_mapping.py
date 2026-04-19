"""
[UIDT-v3.9] Formal Lagrangian extension for explicit symmetry breaking
===================================================================

This module closes the Stratum-III mapping required in Step 4d by
introducing a formal effective-source term in the UIDT scalar sector:

    L_eff  ⊃  + h * phi

Equivalently, in the effective potential convention used by the framework:

    U_eff(phi) = U_sym(phi) - h * phi

with

    U_sym(phi) = (1/2) m^2 phi^2 + (lambda_4 / 4) phi^4

This is the standard explicit-symmetry-breaking structure familiar from
Landau-Ginzburg / linear sigma model effective descriptions of QCD chiral
symmetry breaking, where the source is linearly coupled to the order
parameter.

Stratum assignment
------------------
Stratum I:
  Lattice QCD values for <psi-bar psi> and chi_top
Stratum II:
  Standard EFT statement that an external source coupled to the order
  parameter enters linearly in the effective action / potential
Stratum III:
  UIDT identification of phi as the effective scalar order parameter of the
  vacuum-information sector, with h inherited from the QCD condensate anchor

Evidence categories
-------------------
[A]   algebraic identities in this module
[A-]  UIDT ledger parameters gamma, etc. (not altered here)
[B]   lattice-anchored h input from Step 4d
[D]   phenomenological embedding of the UIDT scalar into the chiral-style EFT

Important limitation
--------------------
This module provides the formal field-theoretic closure of the mapping:
  h_QCD  ->  h * phi term in U_eff
It does NOT claim a first-principles derivation from QCD path-integral
bosonization. Therefore the embedding remains transparent and should be
reported as a controlled effective-theory identification.
"""

from __future__ import annotations

import mpmath as mp

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.lattice_anchor import compute_h_gmor, compute_h_wv


def _set_precision() -> None:
    mp.dps = 80


# ---------------------------------------------------------------------
# Effective potential with explicit source
# ---------------------------------------------------------------------

def symmetric_potential(phi: mp.mpf, m_sq: mp.mpf, lambda_4: mp.mpf) -> mp.mpf:
    """
    Symmetric quartic potential:

        U_sym(phi) = 1/2 m^2 phi^2 + 1/4 lambda_4 phi^4

    Evidence: [A]
    """
    _set_precision()
    return (
        mp.mpf("0.5") * m_sq * phi**2
        + mp.mpf("0.25") * lambda_4 * phi**4
    )



def effective_potential(phi: mp.mpf, m_sq: mp.mpf, lambda_4: mp.mpf, h: mp.mpf) -> mp.mpf:
    """
    Effective potential with explicit source term:

        U_eff(phi) = U_sym(phi) - h phi

    Evidence: [A] for the algebra; Stratum III for the identification.
    """
    _set_precision()
    return symmetric_potential(phi, m_sq, lambda_4) - h * phi



def effective_potential_derivative(
    phi: mp.mpf, m_sq: mp.mpf, lambda_4: mp.mpf, h: mp.mpf
) -> mp.mpf:
    """
    First derivative:

        dU_eff/dphi = m^2 phi + lambda_4 phi^3 - h

    Stationary condition gives the same cubic equation used in Step 4c.

    Evidence: [A]
    """
    _set_precision()
    return m_sq * phi + lambda_4 * phi**3 - h



def effective_potential_second_derivative(
    phi: mp.mpf, m_sq: mp.mpf, lambda_4: mp.mpf
) -> mp.mpf:
    """
    Second derivative:

        d^2U_eff/dphi^2 = m^2 + 3 lambda_4 phi^2

    Evidence: [A]
    """
    _set_precision()
    return m_sq + mp.mpf("3") * lambda_4 * phi**2


# ---------------------------------------------------------------------
# Formal source-identification map
# ---------------------------------------------------------------------

def identify_effective_source_from_gmor() -> dict:
    """
    Formal source map using Step 4d GMOR anchor.

    Returns a dictionary that states the effective-source identification:

        h_eff := h_GMOR

    This is the formal Stratum-III closure used by UIDT.
    Evidence of the returned number remains [B] until explicit sign-off.
    """
    _set_precision()
    gmor = compute_h_gmor()
    return {
        "source_name": "h_eff",
        "value": gmor["h_dimless"],
        "sigma": gmor["sigma_h_dimless"],
        "origin": "GMOR lattice anchor",
        "stratum": "III",
        "evidence": "[B]",
    }



def identify_effective_source_crosscheck() -> dict:
    """
    Cross-check source map using the WV anchor.

    Evidence remains [B].
    """
    _set_precision()
    wv = compute_h_wv()
    return {
        "source_name": "h_eff_crosscheck",
        "value": wv["h_wv"],
        "sigma": wv["sigma_h_wv"],
        "origin": "Witten-Veneziano lattice anchor",
        "stratum": "III",
        "evidence": "[B]",
    }



def derive_stationary_equation_from_lagrangian() -> str:
    """
    Human-readable derivation note.

    This is kept as a string helper so that reports / PR notes can cite the
    exact forward chain without re-deriving it ad hoc.
    """
    return (
        "Starting from U_eff(phi)=1/2 m^2 phi^2 + 1/4 lambda_4 phi^4 - h phi, "
        "the stationarity condition dU_eff/dphi=0 yields m^2 phi + lambda_4 phi^3 - h = 0. "
        "Therefore the Step-4c cubic equation is not an imposed reconstruction target but "
        "the Euler-Lagrange stationary condition of the explicitly broken effective potential."
    )



def derive_lambda3_from_shift(phi0: mp.mpf, lambda_4: mp.mpf) -> mp.mpf:
    """
    Shift phi = phi0 + delta and read off cubic coefficient:

        lambda_3 = 3 lambda_4 phi0

    Evidence: [A]
    """
    _set_precision()
    return mp.mpf("3") * lambda_4 * phi0



def formal_mapping_report() -> str:
    """
    Full formal report for the Stratum-III closure.
    """
    _set_precision()
    verify_rg_constraint()
    ledger = get_ledger()
    gmor = identify_effective_source_from_gmor()
    wv = identify_effective_source_crosscheck()

    lines = [
        "+================================================================+",
        "|  UIDT FRG/NLO STEP 4e: Formal Lagrangian Closure              |",
        "+================================================================+",
        "",
        "FORMAL EFFECTIVE POTENTIAL:",
        "  U_eff(phi) = 1/2 m^2 phi^2 + 1/4 lambda_4 phi^4 - h phi",
        "",
        "STATIONARY EQUATION:",
        "  dU_eff/dphi = m^2 phi + lambda_4 phi^3 - h = 0",
        "",
        "INTERPRETATION:",
        "  The Step-4c cubic equation is the Euler-Lagrange stationary condition",
        "  of the explicitly broken effective UIDT scalar potential.",
        "",
        "SOURCE IDENTIFICATION:",
        f"  h_eff (GMOR anchor) = {mp.nstr(gmor['value'], 15)} +/- {mp.nstr(gmor['sigma'], 6)}",
        f"  h_eff (WV cross-check)= {mp.nstr(wv['value'], 15)} +/- {mp.nstr(wv['sigma'], 6)}",
        "",
        "CUBIC COUPLING AFTER SHIFT phi = phi0 + delta:",
        "  lambda_3 = 3 lambda_4 phi0",
        "",
        "EPISTEMIC NOTE:",
        "  This closes the formal Stratum-III mapping h_QCD -> h phi in the effective UIDT",
        "  scalar sector, but does not yet constitute a first-principles bosonization proof.",
        "  Evidence stays transparent and must be reported accordingly.",
        "",
        "LEDGER CHECK:",
        f"  Delta* = {mp.nstr(ledger['DELTA_STAR'], 8)} GeV [A]",
        f"  gamma  = {mp.nstr(ledger['GAMMA'], 8)} [A-]",
        f"  gamma∞ = {mp.nstr(ledger['GAMMA_INF'], 8)} [A-]",
        "",
        "DOI: 10.5281/zenodo.17835200",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(formal_mapping_report())
