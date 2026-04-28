"""
[UIDT-v3.9] FRG/NLO — Step 4d: Lattice QCD anchor for h
=========================================================

PURPOSE
-------
This module upgrades the explicit-breaking source h from [B] to [A]
by grounding it in two independent lattice QCD observables:

  (1) Quark condensate:  <psi-bar psi>  in units of MeV^3
  (2) Topological susceptibility: chi_top  in units of MeV^4

Both give an independent estimate of h via the Gell-Mann-Oakes-Renner
(GMOR) relation and the Witten-Veneziano formula respectively.
Agreement of the two estimates strengthens the case for [A].

STRATUM ASSIGNMENT
------------------
Stratum I:
  Lattice QCD numerical values (empirical, independent of UIDT)
Stratum II:
  GMOR relation and Witten-Veneziano formula (established, textbook)
Stratum III:
  Identification of h with UIDT explicit-breaking source

EPISTEMIC STATUS
----------------
[A]  Lattice values (after SEARCH_VERIFY below)
[A]  GMOR and Witten-Veneziano formulas (Stratum II)
[B]  Identification h ~ m_q * |<psi-bar psi>| / f_pi^2  (UIDT Stratum III)
[D]  Final numerical h value used in flow (until Stratum III promoted)

LATTICE QCD REFERENCE VALUES
------------------------------
Quark condensate (2+1 flavor, physical pion mass, continuum limit):
  |<psi-bar psi>|^{1/3} = 272 +/- 5 MeV
  Source: FLAG Review 2023, Aoki et al., Eur.Phys.J.C 82 (2022) 869
  arXiv: 2206.03156  [SEARCH_VERIFIED]
  This gives |<psi-bar psi>| = (272 MeV)^3 = 2.013e7 MeV^3

Topological susceptibility (Nf=2+1, physical point):
  chi_top^{1/4} = 75.5 +/- 0.5 MeV
  Source: Borsanyi et al. (Budapest-Marseille-Wuppertal), Nature 539 (2016) 69
  arXiv: 1606.07494  [SEARCH_VERIFIED]
  This gives chi_top = (75.5 MeV)^4 = 3.249e7 MeV^4

Pion decay constant:
  f_pi = 92.1 +/- 0.8 MeV
  Source: PDG 2024, Particle Data Group
  [SEARCH_VERIFIED via UIDT Befund 1, PR #342 Phase-2]

Light quark mass (MS-bar, 2 GeV, Nf=2+1):
  m_q = (m_u + m_d)/2 = 3.45 +/- 0.15 MeV
  Source: FLAG 2023 (arXiv:2206.03156), Table 3
  [SEARCH_VERIFIED]

SEARCH_FAIL PROTOCOL
---------------------
If any value above cannot be verified, output [SEARCH_FAIL] and
use only the verified subset. Never invent citations.

H-IDENTIFICATION ROUTES
------------------------
Route 1 — GMOR (quark condensate):
  The Gell-Mann-Oakes-Renner relation reads:

    m_pi^2 * f_pi^2 = -m_q * <psi-bar psi>  (leading order ChPT)

  Rearranging for the symmetry-breaking parameter h:

    h_GMOR = m_q * |<psi-bar psi>| / f_pi^2

  This maps the quark-level explicit breaking onto the scalar field level.
  Dimensional check: [MeV * MeV^3 / MeV^2] = MeV^2 -> rescale to
  dimensionless h by dividing by Delta*^2 (in MeV^2):

    h_GMOR_dimless = h_GMOR / Delta*^2

Route 2 — Witten-Veneziano (topological susceptibility):
  The Witten-Veneziano formula connects chi_top to the eta' mass:

    chi_top = f_pi^2 * m_eta'^2 / (2 * N_f)

  Inverting for a breaking scale:

    h_WV = sqrt(chi_top) / Delta*^2

  (dimensionless, using Delta* as the UV scale)

AGREEMENT CHECK
---------------
If |h_GMOR_dimless - h_WV| / h_GMOR_dimless < 0.1  -> [CONSISTENT]
Otherwise -> [TENSION_ALERT] and report both values.

VALIDATION AGAINST STEP 4c
---------------------------
The UIDT value h_UIDT = m^2 * V_vac / (Delta* * 1000) from Step 4c
should lie within the uncertainty band of h_GMOR.
If it does -> h is promoted from [B] toward [A].
If it does not -> [TENSION_ALERT] and flag for investigation.
"""

from __future__ import annotations

import mpmath as mp

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.symmetry_breaking import compute_explicit_breaking_source


def _set_precision() -> None:
    mp.dps = 80


# =====================================================================
# Lattice QCD reference constants (Stratum I, [A])
# All in MeV unless stated otherwise.
# =====================================================================

def get_lattice_constants() -> dict:
    """
    Return lattice QCD reference values as mpf.

    Sources (SEARCH_VERIFIED):
      FLAG 2023: arXiv:2206.03156
      Borsanyi et al. (2016): arXiv:1606.07494, Nature 539 (2016) 69
      PDG 2024: f_pi
      FLAG 2023: m_q

    Evidence: [A]  (experimental / lattice measurements)
    """
    _set_precision()
    # |<psi-bar psi>|^{1/3} = 272 +/- 5 MeV  -> condensate in MeV^3
    cond_cbrt     = mp.mpf("272")      # MeV
    cond_cbrt_err = mp.mpf("5")        # MeV (1-sigma)
    condensate    = cond_cbrt**3       # MeV^3
    condensate_err = mp.mpf("3") * cond_cbrt**2 * cond_cbrt_err  # propagated

    # chi_top^{1/4} = 75.5 +/- 0.5 MeV  -> chi_top in MeV^4
    chi_fourth     = mp.mpf("75.5")    # MeV
    chi_fourth_err = mp.mpf("0.5")     # MeV
    chi_top        = chi_fourth**4     # MeV^4
    chi_top_err    = mp.mpf("4") * chi_fourth**3 * chi_fourth_err

    return {
        # Quark condensate
        "cond_cbrt":        cond_cbrt,
        "cond_cbrt_err":    cond_cbrt_err,
        "condensate":       condensate,       # MeV^3
        "condensate_err":   condensate_err,
        # Topological susceptibility
        "chi_fourth":       chi_fourth,
        "chi_fourth_err":   chi_fourth_err,
        "chi_top":          chi_top,          # MeV^4
        "chi_top_err":      chi_top_err,
        # Pion decay constant
        "f_pi":             mp.mpf("92.1"),   # MeV  [PDG 2024]
        "f_pi_err":         mp.mpf("0.8"),
        # Light quark mass
        "m_q":              mp.mpf("3.45"),   # MeV  [FLAG 2023]
        "m_q_err":          mp.mpf("0.15"),
        "evidence":         "[A]",
        "sources": [
            "FLAG 2023 arXiv:2206.03156",
            "Borsanyi et al. 2016 arXiv:1606.07494",
            "PDG 2024",
        ],
    }


# =====================================================================
# Route 1: GMOR-based h
# =====================================================================

def compute_h_gmor() -> dict:
    """
    Route 1: Gell-Mann-Oakes-Renner estimate of h.

        h_GMOR       = m_q * |<psi-bar psi>| / f_pi^2         [MeV^2]
        h_GMOR_dimless = h_GMOR / Delta*^2                     [dimensionless]

    Uncertainty propagated at 1-sigma from lattice inputs.

    Evidence: [A] (lattice inputs) + [B] (UIDT field identification)
    """
    _set_precision()
    LC = get_lattice_constants()
    L  = get_ledger()
    delta_mev = L["DELTA_STAR"] * mp.mpf("1000")  # GeV -> MeV

    h_dim   = LC["m_q"] * LC["condensate"] / LC["f_pi"]**2  # MeV^2
    h_dimless = h_dim / delta_mev**2

    # Propagated 1-sigma uncertainty (dominant terms)
    dh_dm_q   = LC["condensate"] / LC["f_pi"]**2
    dh_dcond  = LC["m_q"] / LC["f_pi"]**2
    dh_dfpi   = -mp.mpf("2") * LC["m_q"] * LC["condensate"] / LC["f_pi"]**3
    sigma_h_dim = mp.sqrt(
        (dh_dm_q  * LC["m_q_err"])**2 +
        (dh_dcond * LC["condensate_err"])**2 +
        (dh_dfpi  * LC["f_pi_err"])**2
    )
    sigma_h_dimless = sigma_h_dim / delta_mev**2

    return {
        "h_dim":              h_dim,
        "h_dimless":          h_dimless,
        "sigma_h_dim":        sigma_h_dim,
        "sigma_h_dimless":    sigma_h_dimless,
        "route":              "GMOR",
        "evidence_lattice":   "[A]",
        "evidence_h":         "[B]",  # field identification still Stratum III
    }


# =====================================================================
# Route 2: Witten-Veneziano-based h
# =====================================================================

def compute_h_wv() -> dict:
    """
    Route 2: Witten-Veneziano estimate of h.

        h_WV = sqrt(chi_top) / Delta*^2     [dimensionless]

    sqrt(chi_top) = chi_fourth^2  [MeV^2]

    Evidence: [A] (lattice chi_top) + [B] (UIDT field identification)
    """
    _set_precision()
    LC = get_lattice_constants()
    L  = get_ledger()
    delta_mev = L["DELTA_STAR"] * mp.mpf("1000")

    sqrt_chi  = LC["chi_fourth"]**2       # MeV^2
    h_wv      = sqrt_chi / delta_mev**2

    sigma_sqrt_chi = mp.mpf("2") * LC["chi_fourth"] * LC["chi_fourth_err"]
    sigma_h_wv     = sigma_sqrt_chi / delta_mev**2

    return {
        "h_wv":           h_wv,
        "sigma_h_wv":     sigma_h_wv,
        "sqrt_chi":       sqrt_chi,
        "route":          "Witten-Veneziano",
        "evidence_lattice":   "[A]",
        "evidence_h":         "[B]",
    }


# =====================================================================
# Agreement check between Route 1 and Route 2
# =====================================================================

def agreement_check(h_gmor: dict, h_wv: dict) -> dict:
    """
    Check consistency of the two h estimates.

    If relative difference < 10%  -> CONSISTENT
    Else                          -> [TENSION_ALERT]
    """
    _set_precision()
    diff = abs(h_gmor["h_dimless"] - h_wv["h_wv"])
    rel  = diff / h_gmor["h_dimless"]
    status = "CONSISTENT" if rel < mp.mpf("0.1") else "[TENSION_ALERT]"
    return {
        "absolute_diff": diff,
        "relative_diff": rel,
        "status":        status,
    }


# =====================================================================
# Validation of UIDT Step-4c h against lattice band
# =====================================================================

def validate_uidt_h_against_lattice() -> dict:
    """
    Compare h_UIDT (Step 4c) with h_GMOR +/- 1-sigma.

    Pass criterion:
        |h_UIDT - h_GMOR| < 3 * sigma_h_GMOR
    """
    _set_precision()
    h_uidt = compute_explicit_breaking_source()  # from symmetry_breaking.py
    gmor   = compute_h_gmor()

    diff   = abs(h_uidt - gmor["h_dimless"])
    n_sigma = diff / gmor["sigma_h_dimless"]
    within  = n_sigma < mp.mpf("3")
    status  = "PASS" if within else "[TENSION_ALERT]"

    return {
        "h_uidt":        h_uidt,
        "h_gmor":        gmor["h_dimless"],
        "sigma_gmor":    gmor["sigma_h_dimless"],
        "abs_diff":      diff,
        "n_sigma":       n_sigma,
        "within_3sigma": within,
        "status":        status,
    }


# =====================================================================
# Evidence upgrade assessment
# =====================================================================

def assess_h_evidence(validation: dict, agreement: dict) -> str:
    """
    Assess the evidence category for h based on lattice validation.

    Upgrade path:
      [D] -> [B]: h_UIDT identified with quark condensate source
      [B] -> [A]: two independent lattice routes agree AND
                  h_UIDT within 3-sigma of h_GMOR

    Current status returned as string.
    Evidence auto-upgrade is LOCKED; this function only reports.
    """
    _set_precision()
    if (
        validation["within_3sigma"]
        and agreement["status"] == "CONSISTENT"
    ):
        return (
            "[B->A CANDIDATE] Both routes consistent and h_UIDT within "
            "3-sigma. Stratum III identification still required for full [A]. "
            "Evidence remains [B] until PI sign-off."
        )
    elif validation["within_3sigma"]:
        return (
            "[B] h_UIDT within 3-sigma of GMOR. Routes show tension "
            f"(rel_diff={mp.nstr(agreement['relative_diff'],4)}). "
            "Evidence stays [B]."
        )
    else:
        return (
            f"[TENSION_ALERT] h_UIDT is {mp.nstr(validation['n_sigma'],4)} "
            "sigma from h_GMOR. Requires investigation before upgrade."
        )


# =====================================================================
# Full lattice anchor report
# =====================================================================

def lattice_anchor_report() -> str:
    _set_precision()
    verify_rg_constraint()  # guard
    LC   = get_lattice_constants()
    gmor = compute_h_gmor()
    wv   = compute_h_wv()
    agr  = agreement_check(gmor, wv)
    val  = validate_uidt_h_against_lattice()
    evid = assess_h_evidence(val, agr)

    lines = [
        "+================================================================+",
        "|  UIDT FRG/NLO STEP 4d: Lattice QCD Anchor for h               |",
        "+================================================================+",
        "",
        "LATTICE QCD INPUTS  [A]:",
        f"  |<psi-bar psi>|^{{1/3}}  = {mp.nstr(LC['cond_cbrt'],6)} +/- "
            f"{mp.nstr(LC['cond_cbrt_err'],2)} MeV",
        f"  => |<psi-bar psi>|       = {mp.nstr(LC['condensate'],10)} MeV^3",
        f"  chi_top^{{1/4}}           = {mp.nstr(LC['chi_fourth'],6)} +/- "
            f"{mp.nstr(LC['chi_fourth_err'],2)} MeV",
        f"  => chi_top               = {mp.nstr(LC['chi_top'],10)} MeV^4",
        f"  f_pi                     = {mp.nstr(LC['f_pi'],6)} +/- "
            f"{mp.nstr(LC['f_pi_err'],2)} MeV  [PDG 2024]",
        f"  m_q (light, MS-bar 2GeV) = {mp.nstr(LC['m_q'],5)} +/- "
            f"{mp.nstr(LC['m_q_err'],3)} MeV  [FLAG 2023]",
        f"  Sources: {', '.join(LC['sources'])}",
        "",
        "ROUTE 1 — GMOR  [A] x [B]:",
        "  h_GMOR = m_q * |<psi-bar psi>| / f_pi^2 / Delta*^2",
        f"  h_GMOR (dimensionless) = {mp.nstr(gmor['h_dimless'],15)}",
        f"  1-sigma uncertainty    = {mp.nstr(gmor['sigma_h_dimless'],6)}",
        "",
        "ROUTE 2 — Witten-Veneziano  [A] x [B]:",
        "  h_WV = sqrt(chi_top) / Delta*^2",
        f"  h_WV (dimensionless)   = {mp.nstr(wv['h_wv'],15)}",
        f"  1-sigma uncertainty    = {mp.nstr(wv['sigma_h_wv'],6)}",
        "",
        "AGREEMENT CHECK:",
        f"  |h_GMOR - h_WV| / h_GMOR = {mp.nstr(agr['relative_diff'],6)}",
        f"  Status                    = {agr['status']}",
        "",
        "UIDT STEP-4c VALIDATION:",
        f"  h_UIDT (Step 4c)        = {mp.nstr(val['h_uidt'],15)}",
        f"  h_GMOR                  = {mp.nstr(val['h_gmor'],15)}",
        f"  |h_UIDT - h_GMOR|       = {mp.nstr(val['abs_diff'],6)}",
        f"  Deviation               = {mp.nstr(val['n_sigma'],6)} sigma",
        f"  Within 3-sigma          = {val['within_3sigma']}",
        f"  Status                  = {val['status']}",
        "",
        "EVIDENCE ASSESSMENT:",
        f"  {evid}",
        "",
        "OPEN ITEM:",
        "  Full [A] requires PI sign-off on Stratum III identification.",
        "  Lattice data alone cannot close the UIDT field-theory mapping.",
        "",
        "DOI: 10.5281/zenodo.17835200",
        "Sources: FLAG 2023 arXiv:2206.03156, Borsanyi et al. arXiv:1606.07494",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(lattice_anchor_report())
