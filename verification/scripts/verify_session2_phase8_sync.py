#!/usr/bin/env python3
"""UIDT v3.9 Session-2 Phase-8 arithmetic verification."""

from __future__ import annotations

from mpmath import mp


def assert_residual(label: str, value: mp.mpf, expected: mp.mpf, tol: mp.mpf) -> mp.mpf:
    residual = abs(value - expected)
    assert residual < tol, (
        f"{label} residual {mp.nstr(residual, 80)} exceeds {mp.nstr(tol, 20)}"
    )
    print(f"[PASS] {label} residual:", mp.nstr(residual, 80))
    return residual


def main() -> None:
    mp.dps = 80
    tight_tol = mp.mpf("1e-70")
    proof_tol = mp.mpf("1e-14")

    nc = mp.mpf(3)
    gamma_ledger = mp.mpf("16.339")
    delta_star_mev = mp.mpf("1710")
    e_t_mev = mp.mpf("2.44")
    kappa = mp.mpf(1) / mp.mpf(2)
    lambda_s = mp.mpf(5) / mp.mpf(12)

    gamma_bare = (2 * nc + 1) ** 2 / nc
    gamma_wrong = (2 * nc + 1) ** 2 / (nc**2)
    delta_gamma_required = gamma_ledger - gamma_bare
    k_crit_mev = 4 * mp.pi * e_t_mev
    v_s4p1_mev = mp.sqrt(mp.mpf(12) / mp.mpf(5)) * k_crit_mev
    delta_gamma_np = (nc**2 - 1) / (4 * mp.pi**2) * (v_s4p1_mev / delta_star_mev)
    gamma_pred = gamma_bare + delta_gamma_np
    gamma_pred_residual = abs(gamma_pred - gamma_ledger)
    rg_residual = abs(5 * kappa**2 - 3 * lambda_s)

    assert_residual("gamma_bare = 49/3", gamma_bare, mp.mpf(49) / mp.mpf(3), tight_tol)
    assert_residual("wrong denominator = 49/9", gamma_wrong, mp.mpf(49) / mp.mpf(9), tight_tol)
    assert gamma_wrong != gamma_bare
    assert_residual(
        "Delta_gamma_required = 17/3000",
        delta_gamma_required,
        mp.mpf(17) / mp.mpf(3000),
        tight_tol,
    )
    assert delta_gamma_required > 0

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
    assert rg_residual < proof_tol, mp.nstr(rg_residual, 80)

    print("[INFO] gamma_bare:", mp.nstr(gamma_bare, 80))
    print("[INFO] Delta_gamma_required:", mp.nstr(delta_gamma_required, 80))
    print("[INFO] k_crit_mev:", mp.nstr(k_crit_mev, 80))
    print("[INFO] gamma_pred:", mp.nstr(gamma_pred, 80))
    print("[INFO] |gamma_pred - gamma_ledger|:", mp.nstr(gamma_pred_residual, 80))
    print("[PASS] RG constraint residual:", mp.nstr(rg_residual, 80))
    print("ALL SESSION-2 PHASE-8 SYNC CHECKS PASSED")


if __name__ == "__main__":
    main()
