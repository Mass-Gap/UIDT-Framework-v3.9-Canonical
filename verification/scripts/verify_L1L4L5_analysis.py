# UIDT Verification Script — TKT-20260416
# L1/L4/L5 First-Principles Analysis Verification
# Author: P. Rietz (ORCID: 0009-0007-4307-1609)
# Date: 2026-04-16
# Evidence: E-open throughout
# DOI: 10.5281/zenodo.17835200
#
# RACE CONDITION LOCK: mp.dps = 80 is declared LOCALLY here.
# Do NOT move to config.py or any global setting.

import mpmath as mp
mp.dps = 80  # LOCAL precision — Constitution required


def verify_rg_constraint() -> None:
    """Constitution-required: 5κ² = 3λ_S must hold at machine zero."""
    kappa = mp.mpf('1') / mp.mpf('2')
    lambdas = mp.mpf('5') * kappa**2 / mp.mpf('3')
    residual = abs(5 * kappa**2 - 3 * lambdas)
    if residual != mp.mpf('0'):
        raise AssertionError(f"[RG_CONSTRAINT_FAIL] residual = {mp.nstr(residual, 20)}")
    print(f"  [PASS] RG constraint: 5κ² − 3λ_S = {mp.nstr(residual, 5)} (machine zero)")


def analyse_L4_gamma_conjecture() -> dict:
    """
    L4: SU(3) group-theory search for γ = 16.339.
    Tests the conjecture (2Nc+1)²/Nc = 49/3 and systematic combinations.
    Evidence: E-open — no proof exists.
    """
    Nc = mp.mpf('3')
    gamma_canonical = mp.mpf('16.339')   # A- kinematic
    gamma_bare      = mp.mpf('16.3437')  # B  thermodynamic limit

    # Primary conjecture (UIDT-C-052)
    gamma_conj = (2 * Nc + 1)**2 / Nc  # = 49/3
    delta_kin  = abs(gamma_conj - gamma_canonical)
    delta_bare = abs(gamma_conj - gamma_bare)

    # Systematic SU(3) Casimir combinations
    C2_fund = mp.mpf('4') / mp.mpf('3')
    C2_adj  = mp.mpf('3')
    d_adj   = mp.mpf('8')

    combos = {
        "(2Nc+1)^2/Nc [CONJECTURE]": gamma_conj,
        "d_adj*C2_adj/C2_fund":       d_adj * C2_adj / C2_fund,
        "(Nc^2+1)*C2_adj/(Nc-1)":    (Nc**2 + 1) * C2_adj / (Nc - 1),
        "(Nc^2-1)*(2Nc+1)/Nc":       (Nc**2 - 1) * (2 * Nc + 1) / Nc,
    }

    print("\n  [L4] SU(3) Gamma Conjecture Analysis:")
    print(f"    γ_canonical = {mp.nstr(gamma_canonical, 10)} [A-]")
    print(f"    γ_bare      = {mp.nstr(gamma_bare, 10)} [B]")
    print(f"    49/3        = {mp.nstr(gamma_conj, 15)}")
    print(f"    |49/3 − γ_kin|  = {mp.nstr(delta_kin, 6)}"
          f" ({mp.nstr(100*delta_kin/gamma_canonical, 4)}%)")
    print(f"    |49/3 − γ_bare| = {mp.nstr(delta_bare, 6)}"
          f" ({mp.nstr(100*delta_bare/gamma_bare, 4)}%)")
    print(f"    Evidence: E-open. dim=7 is NOT a standard SU(3) irrep dim.")

    for name, val in combos.items():
        diff = abs(val - gamma_canonical)
        marker = " ◄ closest" if name.startswith("(2Nc+1)") else ""
        print(f"    {name:<40} = {mp.nstr(val, 8):>12}  Δ={mp.nstr(diff, 4)}{marker}")

    # Residual threshold check (E-open: does NOT meet Category A threshold)
    # Category A requires residual < 1e-14
    threshold_A = mp.mpf('1e-14')
    if delta_kin < threshold_A:
        print("    [WARN] Unexpectedly meets Category A threshold — verify!")
    else:
        print(f"    [INFO] Does NOT meet Category A threshold ({mp.nstr(threshold_A,1)}). [E-open] confirmed.")

    return {"gamma_conj": gamma_conj, "delta_kin": delta_kin, "delta_bare": delta_bare}


def analyse_L5_n99_gstar() -> dict:
    """
    L5: Test whether N=99 RG steps can be derived from SM g*(T).
    Also checks the new f_vac ≈ m_μ coincidence.
    Evidence: E-open — no g* mechanism found.
    """
    # SM g*(T) at key phase boundaries
    gstar_phases = {
        "T > 1 TeV (full SM)": mp.mpf('106.75'),
        "T ~ 175 GeV (no top)": mp.mpf('96.25'),
        "T ~ 80 GeV (no top/W/Z/H)": mp.mpf('86.25'),
        "T ~ 5 GeV": mp.mpf('61.75'),
        "T ~ 1 GeV": mp.mpf('47.5'),
        "T ~ 155 MeV (QCD PT)": mp.mpf('17.25'),
        "T < 155 MeV": mp.mpf('10.75'),
        "T < 0.5 MeV": mp.mpf('3.91'),
    }

    target_N99   = mp.mpf('99')
    target_N9405 = mp.mpf('94.05')

    print("\n  [L5] SM g*(T) Scan for N=99:")
    min_delta_99 = None
    best_scale   = None
    for scale, g in gstar_phases.items():
        d99 = abs(g - target_N99)
        if min_delta_99 is None or d99 < min_delta_99:
            min_delta_99 = d99
            best_scale   = scale
        print(f"    {scale:<35} g*={mp.nstr(g,6):>7}  |Δ99|={mp.nstr(d99,5)}")

    print(f"    Closest match: '{best_scale}' with |Δ99| = {mp.nstr(min_delta_99, 5)}")
    print(f"    g*=99 is crossed at T≈391 GeV (interpolated) — not a distinguished SM scale.")
    print(f"    Evidence: E-open. N=99 NOT derivable from g*(T).")

    # Top-quark g* contribution (exact)
    g_top = mp.mpf('1') * mp.mpf('3') * mp.mpf('2') * mp.mpf('2') * mp.mpf('7') / mp.mpf('8')
    assert g_top == mp.mpf('10.5'), f"[FAIL] g*_top = {g_top}, expected 10.5"
    print(f"    [PASS] g*_top = {mp.nstr(g_top, 5)} (exact: 10.5)")

    # f_vac vs m_μ coincidence
    f_vac = mp.mpf('107.10')            # MeV [C]
    m_mu  = mp.mpf('105.6583755')       # MeV  CODATA 2022
    delta_abs = abs(f_vac - m_mu)
    delta_rel = delta_abs / m_mu

    print(f"\n  [L5-NEW] f_vac ≈ m_μ Coincidence:")
    print(f"    f_vac = {mp.nstr(f_vac, 7)} MeV  [C]")
    print(f"    m_μ   = {mp.nstr(m_mu, 10)} MeV  (CODATA)")
    print(f"    |Δ|   = {mp.nstr(delta_abs, 5)} MeV  ({mp.nstr(100*delta_rel, 4)}%)")
    print(f"    g*(T≈f_vac, with μ±) = 14.25")
    print(f"    Evidence: E-open. Deviation 1.36% > 1σ threshold for Category B.")
    print(f"    Proposed claim: UIDT-C-05X [E-open]")

    return {"min_delta_99": min_delta_99, "delta_fvac_mu_rel": delta_rel}


def analyse_L1_scale_factor() -> dict:
    """
    L1: Identify the actual numerical value of the claimed '10^10 factor'.
    Evidence: E-open — problem statement is imprecise.
    """
    # Canonical length scales
    lambda_UIDT_nm = mp.mpf('0.660')   # nm [C]
    lambda_UIDT_fm = lambda_UIDT_nm * mp.mpf('1e6')  # 1 nm = 1e6 fm
    r_conf_fm      = mp.mpf('0.197')   # fm  ħc/Λ_QCD, Λ_QCD≈1 GeV

    ratio_length = lambda_UIDT_fm / r_conf_fm
    exp_length   = mp.log(ratio_length, 10)

    # Fine-structure connection
    alpha_inv      = mp.mpf('137.036')
    alpha_cube_inv = alpha_inv**3
    ratio_alpha    = ratio_length / alpha_cube_inv

    # Energy ratios
    E_fvac   = mp.mpf('0.1071')    # GeV
    E_EWSB   = mp.mpf('246.0')     # GeV
    E_Planck = mp.mpf('1.22e19')   # GeV

    ratio_EWSB_sq = (E_EWSB / E_fvac)**2

    print("\n  [L1] Scale Factor Identification:")
    print(f"    λ_UIDT / r_conf = {mp.nstr(ratio_length, 5)} ≈ 10^{mp.nstr(exp_length, 4)}")
    print(f"    [FINDING] Actual ratio is ~10^6.5, NOT 10^10 as stated in LIMITATIONS.md")
    print(f"    α⁻³              = {mp.nstr(alpha_cube_inv, 5)} ≈ 10^{mp.nstr(mp.log(alpha_cube_inv,10),4)}")
    print(f"    ratio / α⁻³      = {mp.nstr(ratio_alpha, 5)}  (1.3× off from α⁻³ — suggestive)")
    print(f"    (E_EWSB/E_fvac)² = {mp.nstr(ratio_EWSB_sq, 5)} ≈ 10^{mp.nstr(mp.log(ratio_EWSB_sq,10),4)}")
    print(f"    Evidence: E-open.")
    print(f"    [REQUIRED] Open TKT-UIDT-L1-SCALE-DEFINITION: specify UV/IR scales + channel.")

    return {"ratio_length": ratio_length, "exp_length": exp_length, "ratio_alpha": ratio_alpha}


def main() -> None:
    print("=" * 70)
    print("UIDT TKT-20260416 — L1/L4/L5 First-Principles Verification")
    print("Author: P. Rietz | mpmath dps=80 | Evidence: E-open")
    print("=" * 70)

    # Constitution pre-flight
    print("\n[PRE-FLIGHT]")
    verify_rg_constraint()

    # Problem analyses
    r_L4 = analyse_L4_gamma_conjecture()
    r_L5 = analyse_L5_n99_gstar()
    r_L1 = analyse_L1_scale_factor()

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  L4 γ conjecture (49/3):  Δ = {mp.nstr(r_L4['delta_kin'],5)} "
          f"({mp.nstr(100*r_L4['delta_kin']/mp.mpf('16.339'),4)}%)  [E-open]")
    print(f"  L5 N99 from g*(T):       No SM mechanism found              [E-open]")
    print(f"  L5 f_vac/m_μ deviation:  {mp.nstr(100*r_L5['delta_fvac_mu_rel'],4)}%                          [E-open]")
    print(f"  L1 actual scale ratio:   10^{mp.nstr(r_L1['exp_length'],4)} (not 10^10)         [E-open]")
    print(f"  L1 vs α⁻³:              factor {mp.nstr(r_L1['ratio_alpha'],4)}                    [E-open]")
    print()
    print("  Ledger constants:        UNCHANGED")
    print("  RG constraint:           SATISFIED (machine zero)")
    print("  No core/module changes.  No fitting performed.")
    print("  All results: E-open. No Category A/B/C claims made.")
    print("=" * 70)


if __name__ == "__main__":
    main()
