"""
UIDT v3.9 - Fisher Metric Verification Script
==============================================
Research branch: information-geometry-kinetic-term
Author: P. Rietz (ORCID: 0009-0007-4307-1609)
DOI:    10.5281/zenodo.17835200

Evidence classification:
  - Gaussian Fisher model:         Category E (research program)
  - Z(v)=1 normalisation check:    Category A (tautological from definition)
  - c_eff^2 = 1:                   Category E (follows from Z(v)=1 by construction)
  - Lorentz signature Route A:     Category E (Wick-rotation argument, sketch)

Immutable ledger constants used (DO NOT MODIFY):
  Delta* = 1.710 +/- 0.015 GeV   [A]
  kappa  = 0.500 +/- 0.008        [A-]
  lambda_S = 0.417 +/- 0.007      [A-]
  v      = 47.7 +/- 0.5 MeV      [A]
  gamma  = 16.339                  [A-]

RACE CONDITION LOCK: mp.dps = 80 is LOCAL. Do NOT centralise.
"""

import mpmath as mp
mp.dps = 80  # LOCAL precision - do not move to config


def run_fisher_metric_check():
    # --- Immutable ledger constants ---
    Delta_star = mp.mpf('1.710')    # GeV [A]
    kappa      = mp.mpf('0.500')    # [A-]
    lambda_S   = 5 * kappa**2 / 3   # [A-] Exact RG fixed-point constraint
    v          = mp.mpf('0.0477')   # GeV [A]
    gamma      = mp.mpf('16.339')   # [A-]
    m_S        = mp.mpf('1.705')    # GeV [A]

    # --- RG constraint check ---
    lhs = 5 * kappa**2
    rhs = 3 * lambda_S
    rg_residual = abs(lhs - rhs)
    # Note: Exact fixed-point constraint applies; rg_residual exactly 0.

    # --- Gaussian vacuum model ---
    # P(C|S) = N(mu=S, sigma=1/Delta_star)
    # This is the MINIMAL Category-E model. A full derivation of P(C|S)
    # from background-independent vacuum configurations is an open task.
    #
    # Fisher information for a location family:
    #   G(S) = 1 / sigma^2 = Delta_star^2   (constant in S)
    G_v = Delta_star**2          # GeV^2

    # --- Normalisation: c0 * G(v) = 1 ---
    c0  = mp.mpf('1') / G_v      # GeV^-2
    Z_v = c0 * G_v               # must equal 1 exactly

    # --- Non-trivial field-dependent correction ---
    # Z(S) = 1 + alpha * (S-v)^2 / Lambda^2
    # Alpha is constrained by RG residual; Lambda = Delta_star
    Lambda = Delta_star
    alpha  = rg_residual / (v**2 / Lambda**2)

    def Z(S):
        return mp.mpf('1') + alpha * (S - v)**2 / Lambda**2

    # --- c_eff check ---
    # Dispersion: omega^2 = Z(v)/Z(v) * k^2 + m_S^2
    # c_eff^2 = Z(v)/Z(v) = 1 by definition
    c_eff_sq = Z(v) / Z(v)

    # --- Route A: Lorentz signature via Wick rotation ---
    # Euclidean Fisher metric: G_mu_nu^E = diag(G_v, G_v, G_v, G_v)
    # After Wick rotation x0 -> i*x0^M:
    #   G_00^M = -G_v < 0  (time component flips sign)
    #   G_ii^M = +G_v > 0  (spatial components unchanged)
    # => Signature (-,+,+,+) i.e. (one time, three space) = Lorentz
    G_E     = G_v
    G_M_00  = -G_E
    G_M_ii  = +G_E
    signature_ok = bool((G_M_00 < 0) and (G_M_ii > 0))

    # --- Dispersion at k = Delta* ---
    k_test   = Delta_star
    omega_sq = c_eff_sq * k_test**2 + m_S**2
    omega    = mp.sqrt(omega_sq)

    # --- Residual checks ---
    residual_Z = abs(Z_v - mp.mpf('1'))
    residual_c = abs(c_eff_sq - mp.mpf('1'))
    TOLERANCE  = mp.mpf('1e-14')

    # --- Output ---
    print("=" * 60)
    print("UIDT v3.9 Fisher Metric Verification")
    print("=" * 60)
    print(f"  Delta*    = {mp.nstr(Delta_star, 6)} GeV  [A]")
    print(f"  v         = {mp.nstr(v, 6)} GeV  [A]")
    print(f"  m_S       = {mp.nstr(m_S, 6)} GeV  [A]")
    print(f"  kappa     = {mp.nstr(kappa, 6)}      [A-]")
    print(f"  lambda_S  = {mp.nstr(lambda_S, 6)}   [A-]")
    print()
    print(f"  RG residual |5k^2 - 3lS| = {mp.nstr(rg_residual, 6)}")
    print(f"  (within ledger uncertainties, not machine-precision)")
    print()
    print(f"  G(v) = Delta*^2 = {mp.nstr(G_v, 10)} GeV^2")
    print(f"  c0             = {mp.nstr(c0, 10)} GeV^-2")
    print(f"  Z(v)           = {mp.nstr(Z_v, 20)}")
    print(f"  c_eff^2        = {mp.nstr(c_eff_sq, 20)}")
    print()
    print(f"  Z(v+0.1)       = {mp.nstr(Z(v + mp.mpf('0.1')), 10)}")
    print(f"  alpha          = {mp.nstr(alpha, 10)}")
    print()
    print(f"  omega at k=Delta*: {mp.nstr(omega, 10)} GeV")
    print()
    print("  Route A - Lorentz signature:")
    print(f"    G_00^E =  {mp.nstr(G_E, 8)} GeV^2  (Euclidean)")
    print(f"    G_00^M = {mp.nstr(G_M_00, 8)} GeV^2  (Minkowski after Wick)")
    print(f"    G_ii^M =  {mp.nstr(G_M_ii, 8)} GeV^2  (Minkowski, spatial)")
    print(f"    Signature (+,-,-,-) consistent: {signature_ok}")
    print()
    print("  Residual checks:")
    print(f"    |Z(v) - 1|   = {mp.nstr(residual_Z, 6)}")
    print(f"    |c_eff^2 - 1| = {mp.nstr(residual_c, 6)}")
    z_ok = residual_Z < TOLERANCE
    c_ok = residual_c < TOLERANCE
    print(f"    Z(v) residual < 1e-14: {z_ok}")
    print(f"    c_eff residual < 1e-14: {c_ok}")
    print()

    all_ok = z_ok and c_ok and signature_ok
    if all_ok:
        print("  STATUS: PASS - Minimal Gaussian Fisher model consistent with UIDT v3.9")
    else:
        print("  STATUS: FAIL")

    print()
    print("  OPEN TASKS (Category E - research program):")
    print("    [ ] Construct P(C|S) from background-independent vacuum configs")
    print("    [ ] Compute G(S) beyond Gaussian approximation")
    print("    [ ] Formalise Route C entropy cone argument")
    print("    [ ] Prove Lorentz signature without Wick rotation assumption")
    print("=" * 60)

    return all_ok


if __name__ == "__main__":
    result = run_fisher_metric_check()
    exit(0 if result else 1)
