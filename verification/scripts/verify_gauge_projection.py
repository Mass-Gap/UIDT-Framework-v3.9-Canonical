"""
UIDT VERIFICATION SCRIPT: GAUGE-CONSISTENT MANIFOLD TRANSPORT
==============================================================
Author: P. Rietz (ORCID: 0009-0007-4307-1609)
DOI: 10.5281/zenodo.17835200
Evidence Category: A

Standalone verification script for modules/gauge_projection.py.
Runs all formal consistency checks and prints structured evidence report.

Usage:
    python verification/scripts/verify_gauge_projection.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mpmath import mp, mpf, eye, matrix, det
mp.dps = 80  # Local precision declaration (AGENTS.md)

from modules.gauge_projection import (
    GellMannBasis,
    lie_algebra_inject,
    project_to_su3,
    svd_condition_check,
    MetropolisDetailedBalanceGuard,
    haar_measure_drift,
    topological_charge_bias,
    _trace,
    _dagger,
    _frobenius_norm,
)


def section(title, category="A"):
    print(f"\n{'='*70}")
    print(f"  [{category}] {title}")
    print(f"{'='*70}")


def result(name, residual, threshold, passed):
    status = "PASS" if passed else "FAIL"
    print(f"  {name:.<50s} {status}")
    print(f"    Residual : {mp.nstr(residual, 8)}")
    print(f"    Threshold: {mp.nstr(threshold, 8)}")
    return passed


def main():
    mp.dps = 80
    print("=" * 70)
    print("  UIDT GAUGE PROJECTION VERIFICATION SUITE")
    print("  Module: modules/gauge_projection.py")
    print("  Evidence Category: A (mathematical core)")
    print("  DOI: 10.5281/zenodo.17835200")
    print("=" * 70)

    all_passed = True

    # =========================================================================
    # SECTION 1: Gell-Mann Basis Algebra
    # =========================================================================
    section("Gell-Mann Generator Algebra")
    basis = GellMannBasis()

    # 1a. Orthonormality
    ortho = basis.verify_orthonormality()
    all_passed &= result(
        "Tr(T^a T^b) = delta^{ab}/2",
        ortho, mpf('1e-14'), ortho < mpf('1e-14')
    )

    # 1b. Tracelessness
    trace = basis.verify_tracelessness()
    all_passed &= result(
        "Tr(T^a) = 0",
        trace, mpf('1e-14'), trace < mpf('1e-14')
    )

    # 1c. Hermiticity
    max_herm = mpf('0')
    for a in range(8):
        Ta = basis.get(a)
        diff = _frobenius_norm(Ta - _dagger(Ta))
        if diff > max_herm:
            max_herm = diff
    all_passed &= result(
        "T^a = T^{a,dag} (Hermiticity)",
        max_herm, mpf('1e-14'), max_herm < mpf('1e-14')
    )

    # =========================================================================
    # SECTION 2: SU(3) Reprojection
    # =========================================================================
    section("SU(3) Polar Decomposition Reprojection")

    # 2a. Identity
    I3 = eye(3)
    U_id = project_to_su3(I3)
    id_res = _frobenius_norm(U_id - I3)
    all_passed &= result(
        "P(I) = I (identity preserved)",
        id_res, mpf('1e-70'), id_res < mpf('1e-70')
    )

    # 2b. Unitarity after perturbation
    from mpmath import mpc
    W = eye(3)
    W[0, 1] = mpc('0.05', '0.03')
    W[1, 0] = mpc('-0.05', '0.03')
    W[2, 2] = mpc('1.02', '-0.01')
    U_pert = project_to_su3(W)
    unit_res = _frobenius_norm(_dagger(U_pert) * U_pert - eye(3))
    all_passed &= result(
        "||U^dag U - I|| after perturbation",
        unit_res, mpf('1e-70'), unit_res < mpf('1e-70')
    )

    # 2c. Determinant
    det_res = abs(det(U_pert) - mpf('1'))
    all_passed &= result(
        "|det(U) - 1| after perturbation",
        det_res, mpf('1e-70'), det_res < mpf('1e-70')
    )

    # 2d. Idempotence
    U_double = project_to_su3(U_pert)
    idemp_res = _frobenius_norm(U_double - U_pert)
    all_passed &= result(
        "P(P(W)) = P(W) (idempotence)",
        idemp_res, mpf('1e-70'), idemp_res < mpf('1e-70')
    )

    # 2e. Large perturbation
    W_large = matrix([
        [mpc('2.0', '0.5'),  mpc('0.3', '-0.2'), mpc('0.1', '0.1')],
        [mpc('-0.3', '0.2'), mpc('1.5', '-0.3'),  mpc('0.2', '0.0')],
        [mpc('0.1', '-0.1'), mpc('-0.2', '0.1'),  mpc('1.8', '0.4')]
    ])
    U_large = project_to_su3(W_large)
    large_unit = _frobenius_norm(_dagger(U_large) * U_large - eye(3))
    all_passed &= result(
        "Large perturbation reprojection",
        large_unit, mpf('1e-70'), large_unit < mpf('1e-70')
    )

    # =========================================================================
    # SECTION 3: Lie Algebra Injection
    # =========================================================================
    section("Lie Algebra Injection")

    # 3a. Zero perturbation
    coeffs_zero = [mpf('0')] * 8
    U_zero = lie_algebra_inject(I3, coeffs_zero)
    zero_res = _frobenius_norm(U_zero - I3)
    all_passed &= result(
        "Zero perturbation preserves link",
        zero_res, mpf('1e-14'), zero_res < mpf('1e-14')
    )

    # 3b. Small perturbation -> near SU(3)
    coeffs_small = [mpf('0.001')] * 8
    U_small = lie_algebra_inject(I3, coeffs_small, coupling_ag=mpf('0.1'))
    U_small_proj = project_to_su3(U_small)
    small_unit = _frobenius_norm(_dagger(U_small_proj) * U_small_proj - eye(3))
    all_passed &= result(
        "Inject -> reproject -> unitarity",
        small_unit, mpf('1e-70'), small_unit < mpf('1e-70')
    )

    # =========================================================================
    # SECTION 4: SVD Condition Monitor
    # =========================================================================
    section("SVD Condition Monitor")

    # 4a. Identity passes
    passed_svd, kappa_id, _ = svd_condition_check(I3)
    kappa_res = abs(kappa_id - mpf('1'))
    all_passed &= result(
        "Identity condition number = 1",
        kappa_res, mpf('1e-14'), kappa_res < mpf('1e-14')
    )

    # 4b. Kill-switch activation
    W_ill = eye(3)
    W_ill[0, 0] = mpf('1e15')
    W_ill[1, 1] = mpf('1e-5')
    passed_ill, kappa_ill, _ = svd_condition_check(W_ill)
    all_passed &= result(
        "Kill-switch triggers for kappa > 10^12",
        mpf('0') if not passed_ill else mpf('1'),
        mpf('0.5'),
        not passed_ill
    )

    # =========================================================================
    # SECTION 5: Detailed Balance Guard
    # =========================================================================
    section("Metropolis Detailed Balance Guard")

    guard = MetropolisDetailedBalanceGuard()

    # 5a. Symmetric proposal = standard Metropolis
    from mpmath import exp as mp_exp
    delta_S = mpf('0.5')
    p_acc = guard.acceptance_probability(delta_S, mpf('0'), mpf('0'))
    expected = mp_exp(-delta_S)
    sym_res = abs(p_acc - expected)
    all_passed &= result(
        "Symmetric proposal = exp(-dS)",
        sym_res, mpf('1e-14'), sym_res < mpf('1e-14')
    )

    # 5b. Favorable action -> accept
    p_fav = guard.acceptance_probability(mpf('-1'), mpf('0'), mpf('0'))
    fav_res = abs(p_fav - mpf('1'))
    all_passed &= result(
        "Favorable action -> P_acc = 1",
        fav_res, mpf('1e-14'), fav_res < mpf('1e-14')
    )

    # =========================================================================
    # SECTION 6: Haar Measure Drift
    # =========================================================================
    section("Haar Measure Conservation")

    # 6a. Identity ensemble
    matrices_id = [eye(3)] * 20
    passed_h1, max_d1, _ = haar_measure_drift(matrices_id)
    all_passed &= result(
        "Identity ensemble drift = 0",
        max_d1, mpf('1e-70'), max_d1 < mpf('1e-70')
    )

    # 6b. Reprojected ensemble
    matrices_proj = []
    for i in range(10):
        W_i = eye(3)
        eps = mpf(str(i)) * mpf('0.01')
        W_i[0, 1] = mpc(eps, eps / 2)
        W_i[1, 0] = mpc(-eps, eps / 2)
        matrices_proj.append(project_to_su3(W_i))
    passed_h2, max_d2, mean_d2 = haar_measure_drift(matrices_proj)
    all_passed &= result(
        "Reprojected ensemble drift < 10^{-10}",
        max_d2, mpf('1e-10'), max_d2 < mpf('1e-10')
    )

    # =========================================================================
    # SECTION 7: Topological Charge Bias
    # =========================================================================
    section("Topological Charge Bias Detection", "B")

    q_hist = [mpf('1'), mpf('-1'), mpf('0'), mpf('1'), mpf('-1'),
              mpf('0'), mpf('1'), mpf('-1'), mpf('0'), mpf('0')]
    passed_topo, mean_Q, sigma_Q, ratio = topological_charge_bias(q_hist)
    all_passed &= result(
        "Symmetric Q-history unbiased",
        ratio, mpf('2'), passed_topo
    )

    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    if all_passed:
        print("  VERIFICATION RESULT: ALL CHECKS PASSED")
        print("  Evidence Category: A (mathematical core)")
    else:
        print("  VERIFICATION RESULT: *** FAILURES DETECTED ***")
        print("  Review output above for failing tests.")
    print("  DOI: 10.5281/zenodo.17835200")
    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
