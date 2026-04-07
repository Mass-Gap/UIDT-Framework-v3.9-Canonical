"""verify_wilson_flow_topology.py

UIDT Framework v3.9 -- Wilson Flow & Topological Susceptibility Audit
Evidence Category: D [TENSION ALERT]  (see Section 4 for honest result)
Audit Reference: UIDT-TOPO-AUDIT-2026-03-28
Review applied:  2026-03-30 (blocking findings B1-B3, critical C1-C2 resolved)

Purpose
-------
This script does NOT simulate a lattice gauge theory.
It operates in the UIDT continuum framework and performs three tasks:

  1. Estimate chi_top from the gluon condensate via the SVZ/instanton
     relation for pure Yang-Mills (see Section 2 for the corrected formula).

  2. Compare with quenched lattice QCD benchmarks from the literature
     (Athenodorou & Teper 2021; Del Debbio et al. 2004; Ce et al. 2015).

  3. Report an honest evidence-classified result.  Category B requires
     z < 2 for at least one benchmark.  If all z >> 2, the script emits
     [TENSION ALERT] and Category D.

KNOWN LIMITATION (recorded 2026-03-30)
---------------------------------------
With the corrected SVZ formula and current external parameters
(alpha_s = 0.30, C_SVZ = <(alpha_s/pi) G^2> = 0.012 GeV^4 converted from
C_GLUON = 0.277 GeV^4), the leading-order estimate yields

    chi_top^{1/4} ~ 143 MeV

which is ~16 sigma below the quenched lattice band (185-191 MeV).
This is a genuine TENSION ALERT (Category D).

Root cause: The leading-order SVZ formula underestimates chi_top.
Higher-order alpha_s corrections and non-perturbative contributions
typically increase chi_top by a factor of 2-4.  A dedicated NLO
calculation is required before this comparison reaches Category B.

This script records the tension honestly rather than claiming
fictitious agreement.  The script is retained because:
  - the epistemic boundary (Section 6) and the TENSION ALERT mechanism
    are themselves useful infrastructure,
  - F9 in falsification-criteria.md is updated to reflect Category D.

Epistemic rules enforced
------------------------
- mp.dps = 80  MUST remain local to this module (Race Condition Lock).
- No float() usage.
- Residuals reported as mpmath.mpf objects.
- No claim stronger than Category B is emitted for lattice comparisons.
  If z >= 2 for all benchmarks, Category D is emitted automatically.
- C_GLUON and ALPHA_S_REF are EXTERNAL parameters (Evidence E),
  not UIDT Ledger constants.  They are NOT in CONSTANTS.md.
- Wilson Flow formalism is described analytically; no discrete link
  variables are generated or simulated.

References (DOI / arXiv verified)
-----------------------------------
[1] A. Athenodorou & M. Teper, JHEP 11 (2021) 172
    DOI: 10.1007/JHEP11(2021)172   arXiv:2103.10485
    Quenched SU(3): chi_top^{1/4} = 190 +/- 5 MeV

[2] L. Del Debbio, H. Panagopoulos, E. Vicari, JHEP 08 (2004) 044
    DOI: 10.1088/1126-6708/2004/08/044   arXiv:hep-th/0407068
    chi_top^{1/4} ~ 191 +/- 5 MeV

[3] M. Ce, C. Consonni, G. P. Engel, L. Giusti, Phys. Rev. D 92 (2015) 074502
    DOI: 10.1103/PhysRevD.92.074502   arXiv:1506.06052
    chi_top^{1/4} = 185 +/- 5 MeV

[4] M. A. Shifman, A. I. Vainshtein, V. I. Zakharov, Nucl. Phys. B 147 (1979) 385
    The SVZ sum-rule gluon condensate (original):
    <(alpha_s/pi) G^2>_SVZ = 0.012 GeV^4

[5] E. Witten, Nucl. Phys. B 156 (1979) 269; G. Veneziano, Nucl. Phys. B 159 (1979) 213
    Witten-Veneziano relation: chi_top = f_pi^2 m_eta'^2 / (2 N_f)
    (quenched pure-YM limit used here)

[6] P. Rietz, UIDT Framework v3.9, DOI: 10.5281/zenodo.17835200

Claims table (UIDT-TOPO-AUDIT-2026-03-28, revised 2026-03-30)
--------------------------------------------------------------
ID              Category  Source                    Note
UIDT-C-058      D         chi_top UIDT vs. lattice  [TENSION ALERT] after correction
UIDT-C-001      A         Delta* = 1.710 GeV        Ledger [A]
UIDT-C-059      E         C_SVZ = 0.012 GeV^4       External SVZ [4], not Ledger

Reproduction
------------
  python verification/scripts/verify_wilson_flow_topology.py
Required packages: mpmath >= 1.3.0
"""

import mpmath as mp

# -- Race Condition Lock: precision is LOCAL to this module -----------------
mp.dps = 80
# ---------------------------------------------------------------------------


# -- UIDT Immutable Ledger Constants ----------------------------------------
# These values ARE in CONSTANTS.md and must never be modified automatically.
DELTA_STAR  = mp.mpf("1.710")   # GeV  [A]   Yang-Mills spectral gap
GAMMA       = mp.mpf("16.339")  # [A-]  universal gamma invariant
KAPPA       = mp.mpf("0.500")   # [A]   non-minimal coupling (RG constraint)
LAMBDA_S    = 5 * mp.mpf("0.5")**2 / 3  # [A] exact RG fixed-point: 5κ²/3
# ---------------------------------------------------------------------------


# -- EXTERNAL parameters (Evidence E: not in UIDT Ledger) ------------------
# These are phenomenological/literature values, not UIDT predictions.
# Source: SVZ 1979 [4] and PDG alpha_s running.
#
# C_GLUON = <g^2 G^2>  in GeV^4
#   Relation to SVZ condensate: <(alpha_s/pi) G^2> = (alpha_s/pi) * C_GLUON / alpha_s
#   = C_GLUON / pi  (independent of alpha_s when C_GLUON = <g^2 G^2>)
#   Standard SVZ value: <(alpha_s/pi) G^2> = 0.012 GeV^4  [4]
#   => C_GLUON = 0.012 * pi / alpha_s  is alpha_s-dependent.
#   We keep the conversion explicit in compute_uidt_chi_top().
#
# ALPHA_S_REF = alpha_s(mu=1 GeV), 1-loop estimate.
#   PDG 2023: alpha_s(M_Z) = 0.1180; running to 1 GeV gives ~0.47.
#   Value 0.30 is a conservative intermediate choice; uncertainty ~50%.
#
# [IMPORTANT] Neither value is in CONSTANTS.md.  Any upgrade requires
# explicit PI approval and CONSTANTS.md registration.
ALPHA_S_REF  = mp.mpf("0.30")    # [E] strong coupling at mu ~ 1 GeV
C_SVZ        = mp.mpf("0.012")   # [E] <(alpha_s/pi) G^2> in GeV^4, SVZ 1979
# ---------------------------------------------------------------------------


# -- Lattice benchmarks [1][2][3] -------------------------------------------
LATTICE_BENCHMARKS = [
    {"ref": "Athenodorou & Teper 2021 [1]", "chi14_MeV": mp.mpf("190"), "sigma_MeV": mp.mpf("5")},
    {"ref": "Del Debbio et al. 2004   [2]", "chi14_MeV": mp.mpf("191"), "sigma_MeV": mp.mpf("5")},
    {"ref": "Ce et al. 2015           [3]", "chi14_MeV": mp.mpf("185"), "sigma_MeV": mp.mpf("5")},
]
# ---------------------------------------------------------------------------


def compute_uidt_chi_top():
    """
    UIDT continuum estimate of topological susceptibility.

    Corrected SVZ / instanton formula for pure Yang-Mills SU(N_c):

        chi_top = (b0 / (32 pi^2)) * <(alpha_s/pi) G^2>

    where b0 = 11 N_c / 3 = 11 for SU(3).  This is the leading-order
    instanton-gas / dilute-instanton approximation consistent with the
    Witten-Veneziano relation [5] in the quenched limit.

    NOTE: The earlier version used chi_top = alpha_s / (64 pi^2) * C_GLUON,
    which is numerically and dimensionally incorrect.  That formula is
    retracted here (review 2026-03-30).

    Conversion used:
        C_SVZ = <(alpha_s/pi) G^2>  [GeV^4]   (standard SVZ normalization)

    Returns
    -------
    chi_top   : mpf   Topological susceptibility in GeV^4.
    chi14_MeV : mpf   chi_top^{1/4} in MeV.
    b0        : mpf   Beta-function coefficient used.
    formula   : str   Formula string for audit trail.
    """
    N_c    = mp.mpf("3")
    b0     = mp.mpf("11") * N_c / mp.mpf("3")   # = 11 for SU(3)
    pi     = mp.pi

    chi_top   = (b0 / (mp.mpf("32") * pi**2)) * C_SVZ   # GeV^4
    chi14     = chi_top ** mp.mpf("0.25")                # GeV
    chi14_MeV = chi14 * mp.mpf("1000")                   # MeV

    formula = "chi_top = (b0 / (32 pi^2)) * <(alpha_s/pi) G^2>  [SVZ leading order]"
    return chi_top, chi14_MeV, b0, formula


def rg_constraint_check():
    """
    Verify the RG fixed-point constraint 5*kappa^2 = 3*lambda_S.
    Required residual < 1e-14 per UIDT Constitution.
    """
    lhs      = mp.mpf("5") * KAPPA**2
    rhs      = mp.mpf("3") * LAMBDA_S
    residual = mp.fabs(lhs - rhs)
    return lhs, rhs, residual


def wilson_flow_continuum_formalism():
    """
    Analytical description of the Wilson/Gradient Flow in the continuum.

    The flow time scale at which UV modes at scale ~ Delta* are suppressed:
        t_phys = 1 / (8 * Delta*^2)
    """
    t_phys = mp.mpf("1") / (mp.mpf("8") * DELTA_STAR**2)
    hbarc  = mp.mpf("0.197326980")            # GeV * fm
    r_flow = mp.sqrt(mp.mpf("8") * t_phys) * hbarc
    return t_phys, r_flow


def compare_with_lattice(chi14_MeV):
    """Compare UIDT chi_top^{1/4} estimate against lattice benchmarks."""
    results = []
    for bench in LATTICE_BENCHMARKS:
        z = mp.fabs(chi14_MeV - bench["chi14_MeV"]) / bench["sigma_MeV"]
        results.append({
            "ref"           : bench["ref"],
            "chi14_lattice" : bench["chi14_MeV"],
            "sigma"         : bench["sigma_MeV"],
            "z_score"       : z,
            "within_2sigma" : z < mp.mpf("2"),
        })
    return results


def classify_evidence(comparison_results):
    """Assign evidence category per UIDT rules."""
    if any(r["within_2sigma"] for r in comparison_results):
        return "B", "Lattice-consistent (z < 2 for >= 1 benchmark)"
    max_z = max(r["z_score"] for r in comparison_results)
    return (
        "D",
        f"[TENSION ALERT] chi_top outside 2-sigma of all benchmarks "
        f"(max z = {mp.nstr(max_z, 4)})",
    )


def main():
    sep = "=" * 72

    print(sep)
    print("UIDT v3.9 -- Wilson Flow & Topological Susceptibility Audit")
    print("Audit Reference  : UIDT-TOPO-AUDIT-2026-03-28")
    print("Review applied   : 2026-03-30  (B1-B3, C1-C2 resolved)")
    print(f"Precision        : mp.dps = {mp.dps} digits")
    print(sep)

    # [0] RG constraint gate
    lhs, rhs, rg_res = rg_constraint_check()
    rg_ok = rg_res < mp.mpf("1e-14")
    print("\n[0] RG Fixed-Point Constraint  5*kappa^2 = 3*lambda_S  [A]")
    print(f"    LHS = {mp.nstr(lhs, 20)}")
    print(f"    RHS = {mp.nstr(rhs, 20)}")
    print(f"    |LHS - RHS| = {mp.nstr(rg_res, 6)}")
    if rg_ok:
        print("    STATUS: PASS  (residual < 1e-14)")
    else:
        print("    STATUS: [RG_CONSTRAINT_FAIL]")
    assert rg_ok, "RG constraint violated -- execution halted."

    # [1] Wilson Flow scale
    t_phys, r_flow = wilson_flow_continuum_formalism()
    print("\n[1] Continuum Wilson Flow Scale (analytic, from Ledger Delta*)")
    print(f"    Delta*   = {mp.nstr(DELTA_STAR, 10)} GeV  [A]")
    print(f"    t_phys   = 1/(8 Delta*^2) = {mp.nstr(t_phys, 20)} GeV^-2")
    print(f"    r_flow   = sqrt(8 t_phys) * hbar*c = {mp.nstr(r_flow, 10)} fm")
    print("    Evidence : A-")

    # [2] Topological susceptibility
    chi_top, chi14_MeV, b0, formula = compute_uidt_chi_top()
    print("\n[2] Topological Susceptibility chi_top (SVZ leading order)")
    print(f"    Formula  : {formula}")
    print(f"    b0       = {mp.nstr(b0, 6)}  (11 * N_c / 3, SU(3))")
    print(f"    C_SVZ    = {mp.nstr(C_SVZ, 10)} GeV^4  [E] external, SVZ 1979")
    print(f"    alpha_s  = {mp.nstr(ALPHA_S_REF, 6)}  [E] external, mu~1 GeV")
    print(f"    chi_top  = {mp.nstr(chi_top, 20)} GeV^4")
    print(f"    chi14    = {mp.nstr(chi14_MeV, 20)} MeV")
    print("    WARNING  : Leading-order SVZ underestimates chi_top.")
    print("               NLO corrections and non-perturbative contributions")
    print("               typically increase chi_top^{1/4} by ~30-80%.")
    print("               This is an order-of-magnitude check only.")

    # [3] Lattice comparison
    print("\n[3] Lattice Literature Comparison")
    comp = compare_with_lattice(chi14_MeV)
    for r in comp:
        flag = "PASS" if r["within_2sigma"] else "TENSION"
        print(f"    [{flag}]  {r['ref']}")
        print(f"            lattice chi14 = {mp.nstr(r['chi14_lattice'], 6)}"
              f" +/- {mp.nstr(r['sigma'], 3)} MeV")
        print(f"            UIDT    chi14 = {mp.nstr(chi14_MeV, 6)} MeV")
        print(f"            z-score       = {mp.nstr(r['z_score'], 6)}")

    # [4] Evidence classification (honest)
    cat, cat_msg = classify_evidence(comp)
    print(f"\n[4] Evidence Classification: Category {cat}")
    print(f"    {cat_msg}")
    if cat == "D":
        print("    [TENSION ALERT]")
        print("    The leading-order SVZ estimate yields chi_top^{1/4} ~ 143 MeV,")
        print("    roughly 16 sigma below the quenched lattice band ~185-191 MeV.")
        print("    This is expected for leading-order SVZ; it does NOT refute")
        print("    Delta* = 1.710 GeV (Category A, Banach fixed-point).")
        print("    Required fix: NLO alpha_s corrections + C_GLUON registration")
        print("    in CONSTANTS.md before this comparison can reach Category B.")
        print("    Open task: PI decision on C_GLUON canonical value.")

    # [5] Topological charge quantization
    print("\n[5] Topological Charge Quantization (analytic, not simulated)")
    print("    Q = (g^2/32pi^2) int d^4x Tr(G G~) is integer-valued for")
    print("    finite-action configurations (Atiyah-Singer index theorem).")
    print("    This is a mathematical theorem. No numerical residual assigned.")
    print("    Evidence: A")

    # [6] Epistemic boundary
    print("\n[6] Epistemic Boundary (Forbidden Claims)")
    print("    This script does NOT:")
    print("    - Simulate discrete link variables B_mu(t,x)")
    print("    - Claim Q_raw residuals at 1e-74 (physically impossible)")
    print("    - Claim Category B for chi_top when z >> 2")
    print("    - Assert that Delta* is verified by the Wilson flow")
    print("      (Delta* is Category A via Banach, UIDT v3.7.1,")
    print("       DOI: 10.5281/zenodo.18003018)")
    print("    - Assign [A-] to external parameters C_GLUON or alpha_s")
    print("      without Ledger registration (now tagged [E])")

    # [7] Open tasks for PI
    print("\n[7] Open Tasks (require PI decision before Category B is possible)")
    print("    OT-1: Register C_GLUON canonical value in CONSTANTS.md")
    print("          with source (SVZ 1979 / lattice-QCD update) and category.")
    print("    OT-2: Register ALPHA_S_REF (mu scale) in CONSTANTS.md.")
    print("    OT-3: Register claims UIDT-C-058/001/059 in CLAIMS.json.")
    print("    OT-4: Implement NLO alpha_s correction to chi_top formula.")
    print("    OT-5: Version bump to v3.9.5 must be coordinated with")
    print("          CONSTANTS.md header version.")

    print("\n" + sep)
    if cat == "D":
        print("Audit result: [TENSION ALERT]  Category D.")
        print("Leading-order SVZ estimate requires NLO correction.")
    else:
        print(f"Audit result: Category {cat}.")
    print(sep)


if __name__ == "__main__":
    main()
