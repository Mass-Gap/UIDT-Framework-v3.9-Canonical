#!/usr/bin/env python3
"""
UIDT v3.9 — Phase 8.1 P1 delta-gamma 1-loop envelope audit.

This script does NOT derive gamma from first principles. It quantifies the
minimal dimensionless threshold coefficient that a future first-principles
1-loop / non-perturbative computation would need in order to connect

    gamma_bare = 49/3

to the canonical calibrated value

    gamma = 16.339 [A-].

Evidence policy
---------------
- gamma = 16.339 remains [A-].
- gamma_bare = 49/3 remains [D] Stratum III.
- A positive O(1) envelope coefficient is necessary but not sufficient.
- No evidence-category promotion is performed here.

Reproduction
------------
python verification/scripts/verify_phase8_delta_gamma_1loop_envelope.py
"""

from __future__ import annotations

import mpmath as mp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def main() -> None:
    mp.dps = 80

    nc = mp.mpf(3)
    kappa = mp.mpf(1) / mp.mpf(2)
    gamma_ledger = mp.mpf("16.339")
    gamma_bare = (2 * nc + 1) ** 2 / nc
    delta_gamma_required = gamma_ledger - gamma_bare

    # Common dimensionless one-loop scales. These are envelope templates only.
    # They do not encode a complete UIDT Feynman-rule calculation.
    ca_template = nc * kappa**2 / (16 * mp.pi**2)
    adjoint_dof_template = (nc**2 - 1) * kappa**2 / (16 * mp.pi**2)

    required_threshold_ca = delta_gamma_required / ca_template
    required_threshold_adjoint = delta_gamma_required / adjoint_dof_template

    # S4-P1 corrected non-perturbative chain from PR #459 assumptions.
    e_t_mev = mp.mpf("2.44")
    delta_star_mev = mp.mpf("1710")
    k_crit_mev = 4 * mp.pi * e_t_mev
    v_s4p1_mev = mp.sqrt(mp.mpf(12) / mp.mpf(5)) * k_crit_mev
    delta_gamma_np = (nc**2 - 1) / (4 * mp.pi**2) * (v_s4p1_mev / delta_star_mev)
    gamma_pred = gamma_bare + delta_gamma_np
    residual_to_gamma = abs(gamma_pred - gamma_ledger)
    np_to_required_ratio = delta_gamma_np / delta_gamma_required

    require(gamma_bare == mp.mpf(49) / mp.mpf(3), "gamma_bare must be 49/3")
    require(delta_gamma_required == mp.mpf(17) / mp.mpf(3000), "Delta gamma target mismatch")
    require(delta_gamma_required > 0, "Required correction must be positive")

    # Envelope sanity: a viable first-principles path must not require an extreme
    # fine-tuned coefficient at this stage. This is a weak viability gate only.
    require(required_threshold_ca > 0, "C_A threshold coefficient must be positive")
    require(required_threshold_ca < mp.mpf(2), "C_A threshold coefficient is not O(1)")
    require(required_threshold_adjoint > 0, "Adjoint threshold coefficient must be positive")
    require(required_threshold_adjoint < mp.mpf(1), "Adjoint threshold coefficient is not O(1)")

    # The corrected S4-P1 chain should remain close to the required correction but
    # not exactly equal. Equality would be suspicious unless independently derived.
    require(delta_gamma_np > 0, "S4-P1 Delta gamma must be positive")
    require(np_to_required_ratio > mp.mpf("0.99"), "S4-P1 correction too small")
    require(np_to_required_ratio < mp.mpf("1.02"), "S4-P1 correction too large")
    require(residual_to_gamma < mp.mpf("1e-3"), "S4-P1 residual exceeds partial-PASS band")
    require(residual_to_gamma > mp.mpf("1e-14"), "S4-P1 residual must not be misclassified as [A]")

    print("[PASS] gamma_bare =", mp.nstr(gamma_bare, 80))
    print("[PASS] Delta_gamma_required =", mp.nstr(delta_gamma_required, 80))
    print("[PASS] C_A one-loop template =", mp.nstr(ca_template, 80))
    print("[PASS] required threshold coefficient, C_A template =", mp.nstr(required_threshold_ca, 80))
    print("[PASS] adjoint-dof one-loop template =", mp.nstr(adjoint_dof_template, 80))
    print("[PASS] required threshold coefficient, adjoint template =", mp.nstr(required_threshold_adjoint, 80))
    print("[PASS] S4-P1 Delta_gamma_NP =", mp.nstr(delta_gamma_np, 80))
    print("[PASS] S4-P1 / required ratio =", mp.nstr(np_to_required_ratio, 80))
    print("[PASS] gamma_pred =", mp.nstr(gamma_pred, 80))
    print("[PASS] |gamma_pred - gamma_ledger| =", mp.nstr(residual_to_gamma, 80))
    print("[RESULT] PARTIAL-PASS [D]: positive O(1) envelope viable; no first-principles derivation yet")
    print("ALL PHASE-8 P1 ENVELOPE CHECKS PASSED")


if __name__ == "__main__":
    main()
