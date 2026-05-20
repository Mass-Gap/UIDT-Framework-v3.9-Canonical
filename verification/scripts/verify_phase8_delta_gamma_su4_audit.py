#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 delta-gamma and SU(4) audit."""

from __future__ import annotations

from mpmath import mp


def nstr(value: mp.mpf) -> str:
    return mp.nstr(value, 80)


def assert_residual(label: str, value: mp.mpf, expected: mp.mpf, tol: mp.mpf) -> mp.mpf:
    residual = abs(value - expected)
    assert residual < tol, (
        f"{label} residual {mp.nstr(residual, 80)} exceeds {mp.nstr(tol, 20)}"
    )
    print(f"[PASS] {label} residual:", nstr(residual))
    return residual


def main() -> None:
    mp.dps = 80
    tight_tol = mp.mpf("1e-70")
    proof_tol = mp.mpf("1e-14")

    gamma_ledger = mp.mpf("16.339")
    delta_star_mev = mp.mpf("1710")
    e_t_mev = mp.mpf("2.44")
    alpha_s_ref = mp.mpf("0.326")
    kappa = mp.mpf(1) / mp.mpf(2)
    lambda_s = mp.mpf(5) / mp.mpf(12)
    nc3 = mp.mpf(3)
    nc4 = mp.mpf(4)

    gamma_bare_su3 = (2 * nc3 + 1) ** 2 / nc3
    wrong_gamma_bare_su3 = (2 * nc3 + 1) ** 2 / (nc3**2)
    delta_gamma_required = gamma_ledger - gamma_bare_su3

    assert_residual("gamma_bare_SU3 = 49/3", gamma_bare_su3, mp.mpf(49) / mp.mpf(3), tight_tol)
    assert_residual("rejected_wrong_denominator_SU3 = 49/9", wrong_gamma_bare_su3, mp.mpf(49) / mp.mpf(9), tight_tol)
    assert gamma_bare_su3 != wrong_gamma_bare_su3
    assert_residual("Delta_gamma_required = 17/3000", delta_gamma_required, mp.mpf(17) / mp.mpf(3000), tight_tol)
    assert delta_gamma_required > 0

    required_c_alpha_over_4pi = delta_gamma_required * 4 * mp.pi / alpha_s_ref
    required_c_alpha_over_pi = delta_gamma_required * mp.pi / alpha_s_ref
    required_c_alpha_over_16pi2 = delta_gamma_required * 16 * mp.pi**2 / alpha_s_ref
    assert required_c_alpha_over_4pi > 0
    assert required_c_alpha_over_4pi < 1

    k_crit_mev = 4 * mp.pi * e_t_mev
    v_s4p1_mev = mp.sqrt(mp.mpf(12) / mp.mpf(5)) * k_crit_mev
    delta_gamma_np = (nc3**2 - 1) / (4 * mp.pi**2) * (v_s4p1_mev / delta_star_mev)
    gamma_pred = gamma_bare_su3 + delta_gamma_np
    residual_to_gamma = abs(gamma_pred - gamma_ledger)
    residual_to_delta_required = abs(delta_gamma_np - delta_gamma_required)
    ratio_delta_np_to_required = delta_gamma_np / delta_gamma_required

    assert k_crit_mev > 0
    assert v_s4p1_mev > 0
    assert delta_gamma_np > 0
    assert residual_to_gamma > proof_tol
    assert residual_to_gamma < mp.mpf("1e-3")
    assert_residual(
        "k_crit = 4*pi*E_T",
        k_crit_mev,
        mp.mpf("30.6619442990363820073953994208079481497643733379010328127154592209242881253534"),
        tight_tol,
    )
    assert_residual(
        "gamma_pred chain",
        gamma_pred,
        mp.mpf("16.338962439648224784189299741156296927101016473597870996977246409594812352084401"),
        tight_tol,
    )

    gamma_bare_su4 = (2 * nc4 + 1) ** 2 / nc4
    assert_residual("gamma_bare_SU4 = 81/4", gamma_bare_su4, mp.mpf(81) / mp.mpf(4), tight_tol)

    n_su4_constant_b0_11 = nc4**2 * mp.mpf(11)
    b0_su4_pure_ym = mp.mpf(11) * nc4 / mp.mpf(3)
    n_su4_pure_ym_b0 = nc4**2 * b0_su4_pure_ym
    n_su4_difference = n_su4_pure_ym_b0 - n_su4_constant_b0_11
    n_su4_relative_difference = n_su4_difference / n_su4_constant_b0_11
    assert_residual("N_SU4 constant-b0 convention = 176", n_su4_constant_b0_11, mp.mpf(176), tight_tol)
    assert_residual("N_SU4 pure-YM b0 convention = 704/3", n_su4_pure_ym_b0, mp.mpf(704) / mp.mpf(3), tight_tol)
    assert_residual("N_SU4 relative difference = 1/3", n_su4_relative_difference, mp.mpf(1) / mp.mpf(3), tight_tol)
    assert n_su4_difference > 0

    rg_residual = abs(5 * kappa**2 - 3 * lambda_s)
    assert rg_residual < proof_tol, nstr(rg_residual)

    print("[P1a] gamma_bare_SU3:", nstr(gamma_bare_su3))
    print("[P1a] Delta_gamma_required:", nstr(delta_gamma_required))
    print("[P1b] C_required if Delta_gamma = C*alpha_s/(4*pi):", nstr(required_c_alpha_over_4pi))
    print("[P1b] C_required if Delta_gamma = C*alpha_s/pi:", nstr(required_c_alpha_over_pi))
    print("[P1b] C_required if Delta_gamma = C*alpha_s/(16*pi^2):", nstr(required_c_alpha_over_16pi2))
    print("[P1b] STATUS: SCALE-CONSISTENT BUT NOT DERIVED [D]")
    print("[P1c] k_crit_mev:", nstr(k_crit_mev))
    print("[P1c] v_S4P1_mev:", nstr(v_s4p1_mev))
    print("[P1c] Delta_gamma_NP:", nstr(delta_gamma_np))
    print("[P1c] gamma_pred:", nstr(gamma_pred))
    print("[P1c] residual_to_gamma:", nstr(residual_to_gamma))
    print("[P1c] residual_to_Delta_gamma_required:", nstr(residual_to_delta_required))
    print("[P1c] ratio_Delta_gamma_NP_to_required:", nstr(ratio_delta_np_to_required))
    print("[P1c] STATUS: PARTIAL NUMERICAL HIT [D], NOT [A]")
    print("[P5] gamma_bare_SU4:", nstr(gamma_bare_su4))
    print("[P5] N_SU4_constant_b0_11:", nstr(n_su4_constant_b0_11))
    print("[P5] b0_SU4_pure_YM:", nstr(b0_su4_pure_ym))
    print("[P5] N_SU4_pure_YM_b0:", nstr(n_su4_pure_ym_b0))
    print("[P5] N_SU4_definition_difference:", nstr(n_su4_difference))
    print("[P5] N_SU4_relative_difference:", nstr(n_su4_relative_difference))
    print("[P5] STATUS: [TENSION ALERT] N_SU4 definition conflict")
    print("[A] RG_CONSTRAINT residual:", nstr(rg_residual))
    print("ALL PHASE-8 DELTA-GAMMA / SU4 AUDIT CHECKS PASSED")


if __name__ == "__main__":
    main()
