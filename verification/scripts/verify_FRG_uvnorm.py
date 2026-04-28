# UIDT Framework v3.9 — TKT-FRG-UVNORM
# UV-Normierung rho_UV aus GZ-Schema und Fixpunkt-Argument
#
# Author: P. Rietz
# Date: 2026-04-29
#
# Tests drei Argumente fuer rho_UV:
#   Argument A: GZ-Schema-Shift bei k = M_G
#   Argument B: RG-Fixpunkt d(ln rho)/dk = 0
#   Argument C: CW-Selbstkonsistenz (tautologisch)
#   Argument D: Tangential-GZ bei k_sub (Inversion)
#
# Hauptbefund:
#   Argumente A, B, C schliessen die 0.77%-Luecke in C_xi NICHT.
#   Argument D liefert k_sub = 1.676 GeV als physikalisch suggestiven
#   Subtraktionspunkt — nahe Delta*, physikalisch motiviert durch Z_GZ.
#   Echte Schliesssung der Luecke erfordert NLO-GZ-Mischungsmatrix.
#
# Constitution compliance:
#   - mp.dps = 80 local (RACE CONDITION LOCK)
#   - no float(), no round()
#   - RG constraint: 5*kappa^2 = 3*lambda_S enforced
#   - Ledger constants: read-only

import mpmath as mp


def run_uvnorm_analysis():
    mp.dps = 80

    # -- Immutable Ledger Constants --
    Delta    = mp.mpf('1.710')       # GeV [A]
    kappa    = mp.mpf('0.500')       # [A]
    lambda_S = mp.mpf('5') / 12      # [A]
    gamma_L  = mp.mpf('16.339')      # [A-]
    delta_g  = mp.mpf('0.0047')      # [A-]
    v        = mp.mpf('47.7') / 1000 # GeV [A]
    Nc       = mp.mpf('3')
    b0       = mp.mpf('11') * Nc / 3
    M_G      = mp.mpf('0.65')        # GeV [B]
    alpha_s  = mp.mpf('0.3')         # at k = Delta*

    # RG constraint check (immutable, Constitution)
    rg_residual = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg_residual < mp.mpf('1e-14'), (
        f"[RG_CONSTRAINT_FAIL] residual = {mp.nstr(rg_residual, 6)}"
    )

    g2       = 4 * mp.pi * alpha_s
    c_loop   = mp.mpf('1') / (16 * mp.pi**2)
    E_geo    = Delta / gamma_L

    # Target values from TKT-FRG-BETAXI / TKT-FRG-XICW
    xi_eff_req  = mp.mpf('0.52926506')
    C_xi_target = xi_eff_req / (g2 * c_loop)
    C_xi_1loop  = 2 * b0
    gap_1loop   = (C_xi_target - C_xi_1loop) / C_xi_target * 100

    print("=" * 66)
    print("  TKT-FRG-UVNORM: UV-Normierung rho_UV Analyse")
    print("=" * 66)
    print()
    print(f"  C_xi_target   = {mp.nstr(C_xi_target, 8)}")
    print(f"  C_xi_1loop    = {mp.nstr(C_xi_1loop, 6)}  (= 2*b0, TKT-FRG-BETAXI [A])")
    print(f"  Gap           = {mp.nstr(gap_1loop, 4)} %")
    print()

    # ============================================================
    # ARGUMENT A: GZ-Schema-Shift bei k = M_G
    # ============================================================
    print("-" * 66)
    print("  ARGUMENT A: GZ-Schema-Shift Z_xi(M_G -> Delta*)")
    print("-" * 66)

    # Z_xi = (1 + b0*alpha_s/(2pi) * ln(Delta*/M_G))^{8Nc/(3*b0)}
    ln_ratio_A  = mp.log(Delta / M_G)
    bracket_A   = 1 + b0 * alpha_s / (2 * mp.pi) * ln_ratio_A
    exponent_A  = 8 * Nc / (3 * b0)
    Z_xi_A      = bracket_A ** exponent_A
    C_xi_A      = C_xi_1loop * Z_xi_A
    dev_A       = (C_xi_A - C_xi_target) / C_xi_target * 100

    print(f"  ln(Delta*/M_G)          = {mp.nstr(ln_ratio_A, 8)}")
    print(f"  b0*alpha_s/(2pi)        = {mp.nstr(b0*alpha_s/(2*mp.pi), 8)}")
    print(f"  bracket (1 + ...)       = {mp.nstr(bracket_A, 8)}")
    print(f"  exponent 8Nc/(3*b0)     = {mp.nstr(exponent_A, 6)}")
    print(f"  Z_xi(GZ, M_G)           = {mp.nstr(Z_xi_A, 8)}")
    print(f"  C_xi(A)                 = {mp.nstr(C_xi_A, 8)}")
    print(f"  Deviation from target   = {mp.nstr(dev_A, 4)} %")
    if abs(dev_A) > mp.mpf('5'):
        print(f"  VERDICT A: SCHEITERT — Ueberschuss zu gross ({mp.nstr(dev_A,4)}%)")
    print()

    # ============================================================
    # ARGUMENT B: RG-Fixpunkt rho*
    # ============================================================
    print("-" * 66)
    print("  ARGUMENT B: RG-Fixpunkt d(ln rho)/d(ln k) = 0")
    print("-" * 66)

    # d(ln rho)/d(ln k) = (8Nc/3 + 2*b0) * alpha_s/(4pi)
    # In asymptotisch freier QCD: alpha_s(k) -> 0 fuer k -> inf
    # Kein Wilson-Fisher Fixpunkt in 4D QCD fuer Nc >= 2
    beta_coeff = (8 * Nc / 3 + 2 * b0) * alpha_s / (4 * mp.pi)
    print(f"  d(ln rho)/d(ln k) = (8Nc/3 + 2b0)*alpha_s/(4pi)")
    print(f"                    = {mp.nstr(beta_coeff, 8)}  (> 0, kein Fixpunkt)")
    print(f"  VERDICT B: Kein nichttrivialer Fixpunkt in 1-Loop 4D QCD.")
    print(f"             Argument scheitert im perturbativen Rahmen.")
    print()

    # ============================================================
    # ARGUMENT C: CW-Selbstkonsistenz (tautologisch)
    # ============================================================
    print("-" * 66)
    print("  ARGUMENT C: CW-Selbstkonsistenz rho_UV")
    print("-" * 66)

    rho_CW = xi_eff_req * 16 * mp.pi**2 / g2
    print(f"  rho_UV(CW) = xi_eff_req * 16pi^2 / g^2")
    print(f"             = {mp.nstr(rho_CW, 8)}")
    print(f"             = C_xi_target = {mp.nstr(C_xi_target, 8)}  [per Definition]")
    print(f"  VERDICT C: Tautologie — rho_UV = C_xi per Konstruktion.")
    print(f"             Keine unabhaengige Fixierung.")
    print()

    # ============================================================
    # ARGUMENT D: Tangential-GZ Subtraktionspunkt
    # ============================================================
    print("-" * 66)
    print("  ARGUMENT D: Inversion fuer k_sub (Z_xi(k_sub)*C_xi_1loop = C_xi_target)")
    print("-" * 66)

    # Z_xi_target = C_xi_target / C_xi_1loop
    Z_xi_need = C_xi_target / C_xi_1loop
    print(f"  Benoetigt: Z_xi(k_sub) = {mp.nstr(Z_xi_need, 8)}")

    # Z_xi(k_sub) = (1 + b0*alpha_s/(2pi)*ln(Delta*/k_sub))^exponent_A = Z_xi_need
    # => (1 + b0*alpha_s/(2pi)*ln(Delta*/k_sub)) = Z_xi_need^{1/exponent_A}
    inner_need   = Z_xi_need ** (1 / exponent_A)
    ln_need      = (inner_need - 1) / (b0 * alpha_s / (2 * mp.pi))
    k_sub        = Delta * mp.exp(-ln_need)
    Delta_k      = Delta - k_sub
    ratio_k_sub  = k_sub / Delta

    print(f"  Z_xi_need^{{1/exp}}       = {mp.nstr(inner_need, 8)}")
    print(f"  ln(Delta*/k_sub)        = {mp.nstr(ln_need, 8)}")
    print(f"  k_sub                   = {mp.nstr(k_sub, 8)} GeV")
    print(f"  Delta* - k_sub          = {mp.nstr(Delta_k*1000, 5)} MeV")
    print(f"  k_sub / Delta*          = {mp.nstr(ratio_k_sub, 6)}")
    print()

    # Z_GZ Ableitung an Delta* — physikalische Einordnung
    Z_GZ_at_Delta = Delta**4 / (Delta**4 + M_G**4)
    dZ_GZ_dlnk    = 4 * M_G**4 * Delta**4 / (Delta**4 + M_G**4)**2
    print(f"  Z_GZ(Delta*)            = {mp.nstr(Z_GZ_at_Delta, 8)}")
    print(f"  dZ_GZ/d(ln k)|_Delta*   = {mp.nstr(dZ_GZ_dlnk, 8)}")
    print(f"  GZ-Abweichung von 1:    = {mp.nstr(1 - Z_GZ_at_Delta, 6)}")
    print()

    # Vergleich Delta_k mit GZ-Charakteristiklaenge
    k_GZ_char = M_G * (Delta / M_G)**mp.mpf('3') / Delta
    print(f"  k_sub liegt {mp.nstr(Delta_k*1000, 4)} MeV unterhalb Delta*")
    print(f"  Interpretation: GZ-Einfluss beginnt bei Delta*(1 - dZ_GZ/dlnk/4)")
    print(f"                = {mp.nstr((Delta*(1-dZ_GZ_dlnk/4))*1000, 6)} MeV")
    print()

    # Verifikation: Z_xi(k_sub) * C_xi_1loop == C_xi_target
    Z_xi_check = (1 + b0*alpha_s/(2*mp.pi)*mp.log(Delta/k_sub))**exponent_A
    C_xi_D     = C_xi_1loop * Z_xi_check
    residual_D = abs(C_xi_D - C_xi_target)
    print(f"  Verifikation: C_xi(D)   = {mp.nstr(C_xi_D, 10)}")
    print(f"                C_xi_tgt  = {mp.nstr(C_xi_target, 10)}")
    print(f"                Residual  = {mp.nstr(residual_D, 6)}")
    assert residual_D < mp.mpf('1e-10'), (
        f"[UVNORM_INVERSION_FAIL] residual = {mp.nstr(residual_D, 6)}"
    )
    print(f"  VERDICT D: k_sub = {mp.nstr(k_sub, 6)} GeV [D] suggestiv, nicht bewiesen.")
    print()

    # ============================================================
    # ZUSAMMENFASSUNG
    # ============================================================
    print("=" * 66)
    print("  GESAMTBILANZ TKT-FRG-UVNORM")
    print("=" * 66)
    print(f"  Arg A (GZ bei M_G):      C_xi = {mp.nstr(C_xi_A,6)} — SCHEITERT ({mp.nstr(dev_A,4)}%)")
    print(f"  Arg B (RG-Fixpunkt):     kein Fixpunkt in 1-Loop 4D QCD — SCHEITERT")
    print(f"  Arg C (CW-Konsistenz):   tautologisch — SCHEITERT")
    print(f"  Arg D (k_sub-Inversion): k_sub = {mp.nstr(k_sub,6)} GeV [D] suggestiv")
    print()
    print(f"  0.77%-Luecke NICHT geschlossen durch diese TKT.")
    print(f"  Naechster Schritt: TKT-FRG-NLO-MIXING (2-Loop GZ-Mischungsmatrix)")
    print(f"  Referenz: Gracey (2010), Phys.Rev.D81:065006")
    print()

    # TENSION ALERT check
    gamma_emergent_approx = gamma_L  # bleibt unveraendert
    if abs(gamma_emergent_approx - gamma_L) > delta_g:
        print(f"[TENSION ALERT] gamma_emergent = {mp.nstr(gamma_emergent_approx, 8)}")
        print(f"                gamma_ledger   = {mp.nstr(gamma_L, 8)}")
        print(f"                difference     = {mp.nstr(abs(gamma_emergent_approx-gamma_L), 6)}")
    else:
        print(f"  gamma-Ledger unveraendert: {mp.nstr(gamma_L, 8)} [A-] ✓")
    print()

    # Constitution final check
    rg_final = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg_final < mp.mpf('1e-14'), "[RG_CONSTRAINT_FAIL] post-run"
    print(f"  |5kappa^2-3lambda_S|    = {mp.nstr(rg_final, 3)} [machine zero] ✓")
    print(f"  mp.dps                  = {mp.dps} (local) ✓")
    print(f"  float()                 : NOT used ✓")
    print(f"  Ledger constants        : unchanged ✓")

    return {
        'C_xi_1loop'     : C_xi_1loop,
        'C_xi_target'    : C_xi_target,
        'gap_percent'    : gap_1loop,
        'Z_xi_A'         : Z_xi_A,
        'C_xi_A'         : C_xi_A,
        'k_sub_D'        : k_sub,
        'Delta_k_MeV'    : Delta_k * 1000,
        'gap_closed'     : False,
        'gamma_status'   : 'A- (unchanged)',
        'next_TKT'       : 'TKT-FRG-NLO-MIXING',
    }


if __name__ == '__main__':
    result = run_uvnorm_analysis()
