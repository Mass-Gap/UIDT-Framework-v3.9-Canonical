# UIDT Framework v3.9 — TKT-FRG-BETAXI
# Analytical derivation of beta function for xi_eff
#
# Author: P. Rietz
# Date: 2026-04-19
#
# Key results:
#   beta_xi = (8Nc/3) * alpha_s/(4pi) * xi_eff  [EXACT at 1-loop, Evidence A]
#   C_xi^(1-loop) = 2*b0 = 22.000  (0.77% from target 22.170)
#   C_xi^(conjecture) = 2*b0 + 1/b0 = 22.091  (0.36% gap)
#   The 1/b0 term is genuinely two-loop: CANNOT be proven at 1-loop
#   gamma remains Evidence A- (not A)
#
# Constitution compliance:
#   - mp.dps = 80 local (RACE CONDITION LOCK)
#   - no float(), no round()
#   - RG constraint: 5*kappa^2 = 3*lambda_S enforced

import mpmath as mp


def run_betaxi_analysis():
    mp.dps = 80

    # -- Immutable Ledger Constants --
    Delta    = mp.mpf('1.710')
    kappa    = mp.mpf('0.500')
    lambda_S = mp.mpf('5') / 12
    Nc       = mp.mpf('3')
    d_adj    = Nc**2 - 1
    b0       = mp.mpf('11') * Nc / 3
    M_G      = mp.mpf('0.65')
    alpha_s  = mp.mpf('0.3')

    assert abs(5*kappa**2 - 3*lambda_S) < mp.mpf('1e-14'), (
        "[RG_CONSTRAINT_FAIL]"
    )

    g2     = 4 * mp.pi * alpha_s
    c_loop = mp.mpf('1') / (16 * mp.pi**2)
    C_A    = Nc

    # Target
    xi_eff_req = mp.mpf('0.52926506')
    C_xi_target = xi_eff_req / (g2 * c_loop)

    print("=" * 62)
    print("  TKT-FRG-BETAXI: Analytical beta_xi for xi_eff")
    print("=" * 62)
    print()

    # -- One-loop anomalous dimensions --
    coeff_A = -mp.mpf('13') / 6 * Nc
    coeff_S = -C_A
    coeff_comp = coeff_S / 2 + coeff_A

    # Verify analytical simplification
    coeff_expected = -mp.mpf('8') / 3 * Nc
    assert abs(coeff_comp - coeff_expected) < mp.mpf('1e-14'), (
        f"[ANALYTICAL_FAIL] coeff_comp mismatch: "
        f"{mp.nstr(coeff_comp,8)} != {mp.nstr(coeff_expected,8)}"
    )

    print("  One-loop anomalous dimensions (pure YM, Landau gauge):")
    print(f"    gamma_A coeff: {mp.nstr(coeff_A, 6)} * alpha_s/(4pi)")
    print(f"    gamma_S coeff: {mp.nstr(coeff_S, 6)} * alpha_s/(4pi)")
    print(f"    gamma_comp   = gamma_S/2 + gamma_A")
    print(f"                 = {mp.nstr(coeff_comp, 8)} * alpha_s/(4pi)")
    print(f"                 = -(8/3)*Nc = {mp.nstr(coeff_expected, 8)} * alpha_s/(4pi) [A]")
    print()

    # -- Beta function for xi_eff --
    print("  Beta function: beta_xi = +(8Nc/3) * alpha_s/(4pi) * xi_eff")
    print()

    # -- C_xi at 1-loop --
    C_xi_1loop = 2 * b0
    dev_1loop  = abs(C_xi_1loop - C_xi_target) / C_xi_target * 100
    print("  C_xi determination:")
    print(f"    C_xi (1-loop, rho_UV=1) = 2*b0         = {mp.nstr(C_xi_1loop, 6)}")
    print(f"    C_xi (conjecture)       = 2*b0 + 1/b0  = {mp.nstr(2*b0+1/b0, 6)}")
    print(f"    C_xi (required)         =               {mp.nstr(C_xi_target, 6)}")
    print(f"    Deviation (1-loop):   {mp.nstr(dev_1loop, 4)} %")
    print(f"    Deviation (conject.): "
          f"{mp.nstr(abs(2*b0+1/b0-C_xi_target)/C_xi_target*100, 4)} %")
    print()

    # -- Two-loop estimate --
    b1 = mp.mpf('34') / 3 * Nc**2
    Delta_C_NLO = b1 / b0 * alpha_s / (4 * mp.pi) * 2 * b0
    print("  Two-loop correction estimate:")
    print(f"    b1 = 34*Nc^2/3 = {mp.nstr(b1, 5)}")
    print(f"    Delta_C_NLO ~ (b1/b0)*(alpha_s/4pi)*2*b0 = {mp.nstr(Delta_C_NLO, 5)}")
    print(f"    1/b0 = {mp.nstr(mp.mpf('1')/b0, 6)}")
    print(f"    => 1/b0 is NOT the two-loop result (Delta_C_NLO >> 1/b0)")
    print()

    # -- Verdict --
    print("-" * 62)
    print("  VERDICT")
    print("-" * 62)
    print("  PROVEN [A]: beta_xi = (8Nc/3)*alpha_s/(4pi)*xi_eff")
    print(f"  PROVEN [A+assumption]: C_xi^LO = 2*b0 = {mp.nstr(C_xi_1loop, 4)}")
    print("  NOT PROVEN: C_xi = 2*b0 + 1/b0 (requires 2-loop)")
    print("  CONSEQUENCE: gamma remains Evidence A-")
    print()

    # -- Constitution check --
    rg = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg < mp.mpf('1e-14'), "[RG_CONSTRAINT_FAIL] post-run"
    print(f"  |5kappa^2-3lambda_S| = {mp.nstr(rg, 3)} [machine zero] checked")
    print(f"  mp.dps = {mp.dps} (local) checked")
    print(f"  float(): NOT used checked")

    return {
        'beta_xi_coeff'  : mp.mpf('8') * Nc / 3,
        'C_xi_1loop'     : C_xi_1loop,
        'C_xi_conjecture': 2*b0 + mp.mpf('1')/b0,
        'C_xi_target'    : C_xi_target,
        'deviation_1loop': dev_1loop,
        'gamma_proven'   : False,  # gamma NOT yet A
    }


if __name__ == '__main__':
    result = run_betaxi_analysis()
