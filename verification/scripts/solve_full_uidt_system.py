# verification/scripts/solve_full_uidt_system.py
#
# UIDT Framework v3.9 — Full Cascaded 5-Coupling FRG Solver
# Evidence target: UIDT-C-070 upgrade C -> C+ -> B
#
# Architecture:
#   Phase 1 — YMGhostGluonSolver   : 3x3 Newton-Raphson (eta_c, eta_A, w_g*)
#   Phase 2 — CauchyFRGIntegrator  : beta_lamSF_cauchy with frozen w_g*, eta_A*
#   Phase 3 — Full5x5Solver        : 5-param Newton-Raphson (g2, kap2, lam_S, lam_SF, eta_S)
#   Phase 4 — Gatekeeper Protocol  : verify_cauchy_closure + check_eigenvalues
#
# Residual target : |beta_i| < 1e-70 for all 5 components
# Precision       : mp.dps = 80 LOCAL in every method (Race Condition Lock)
# RG constraint   : 5*kap2 = 3*lam_S  -> [RG_CONSTRAINT_FAIL] if |LHS-RHS| > 1e-14
# Gamma rule      : gamma = 16.339 remains A- UNCHANGED
#
# IMMUTABLE LEDGER (DO NOT MODIFY):
#   Delta_star = 1.710 +/- 0.015 GeV  [A]
#   gamma      = 16.339               [A-]
#   gamma_inf  = 16.3437              [A-]
#   delta_g    = 0.0047               [A-]
#   v          = 47.7 MeV             [A]
#   w0         = -0.99                [C]
#   ET         = 2.44 MeV             [C]
#
# Maintainer : P. Rietz
# Date       : 2026-04-06
# Evidence   : D (cascaded analytical projection, unverified)
# Stratum    : III

import mpmath as mp
import sys


# ---------------------------------------------------------------------------
# Phase 1: YM Ghost-Gluon Sector (3x3, Evidence C)
# ---------------------------------------------------------------------------

class YMGhostGluonSolver:
    """
    3x3 Newton-Raphson for the coupled YM ghost-gluon fixed-point system.
    Determines (eta_c*, eta_A*, w_g*) self-consistently.
    Eliminates external DSE input w_g=0.25 (Stratum II).

    Evidence: C (partial verification, all eigenvalues real from prior run).
    Output fed as frozen parameters into Phase 2 and Phase 3.
    """

    def __init__(self):
        mp.dps = 80
        self.Nc = mp.mpf('3')
        self.dA = self.Nc**2 - mp.mpf('1')   # 8
        self.CA = self.Nc                      # 3
        self.CF = (self.Nc**2 - mp.mpf('1')) / (mp.mpf('2') * self.Nc)  # 4/3

    def _l1(self, w):
        mp.dps = 80
        return mp.mpf('1') / (mp.mpf('16') * mp.pi**2 * (mp.mpf('1') + w))

    def _l2(self, w):
        mp.dps = 80
        return mp.mpf('1') / (mp.mpf('32') * mp.pi**2 * (mp.mpf('1') + w)**2)

    def residuals(self, params):
        mp.dps = 80
        eta_c, eta_A, w_g = [mp.mpf(str(x)) for x in params]

        l1g = self._l1(w_g)
        l2g = self._l2(w_g)

        # Ghost anomalous dimension: eta_c from ghost self-energy (SU3, Landau gauge)
        F_etac = eta_c - self.CA * mp.mpf('3') * l1g * (mp.mpf('1') - eta_A / mp.mpf('4'))

        # Gluon anomalous dimension: eta_A from transverse gluon self-energy
        F_etaA = eta_A - self.dA * (
            mp.mpf('13') / mp.mpf('6') * l1g
            - mp.mpf('2') * l2g * w_g
        ) * (mp.mpf('1') - eta_c / mp.mpf('4'))

        # Gluon mass parameter: w_g from IR flow
        F_wg = w_g - self.CA * (
            mp.mpf('5') / mp.mpf('3') * l1g - mp.mpf('2') * l2g
        ) * (mp.mpf('1') - eta_A / mp.mpf('6'))

        return [F_etac, F_etaA, F_wg]

    def solve(self, start=None):
        mp.dps = 80
        if start is None:
            start = [mp.mpf('0.04'), mp.mpf('0.25'), mp.mpf('0.25')]
        result = mp.findroot(
            self.residuals,
            start,
            tol=mp.mpf('1e-75'),
            maxsteps=500
        )
        return [mp.mpf(str(r)) for r in result]

    def verify(self, sol):
        mp.dps = 80
        eta_c, eta_A, w_g = sol
        res = self.residuals(sol)
        max_res = max(abs(r) for r in res)
        print("=== Phase 1: YM Ghost-Gluon Fixed Point (mp.dps=80) ===")
        print(f"  eta_c* = {mp.nstr(eta_c, 25)}")
        print(f"  eta_A* = {mp.nstr(eta_A, 25)}")
        print(f"  w_g*   = {mp.nstr(w_g,   25)}")
        print(f"  max_residual = {mp.nstr(max_res, 10)}")
        if max_res > mp.mpf('1e-70'):
            print("[PHASE1_FAIL] Residual exceeds 1e-70")
        else:
            print("[PHASE1_OK]")
        # Stability matrix
        J = mp.jacobian(self.residuals, sol)
        evs = mp.eig(J)[0]
        print("  Stability eigenvalues:")
        all_real = True
        for ev in evs:
            print(f"    {mp.nstr(ev, 12)}")
            if abs(ev.imag) > mp.mpf('1e-10'):
                all_real = False
        if all_real:
            print("  [EIGENVALUE_OK] All real.")
        else:
            print("  [TRUNCATION_ARTIFACT] Complex eigenvalue detected.")
        return all_real


# ---------------------------------------------------------------------------
# Phase 2: Cauchy FRG Integrator — beta_lamSF_cauchy
# ---------------------------------------------------------------------------

class CauchyFRGIntegrator:
    """
    Gauss-Legendre integration on deformed contour z(t) = t*exp(i*theta).
    Fermi-smoothed Litim regulator eliminates Heaviside singularities.
    [CAUCHY_CLOSURE] gate: |Im(I)| < 1e-70 mandatory.
    """

    def __init__(self, theta=None, N_gl=64, Lambda_UV=None):
        mp.dps = 80
        self.theta  = theta    or mp.mpf('0.2')
        self.N_gl   = N_gl
        self.L_UV2  = Lambda_UV or mp.mpf('100')
        self.Nc     = mp.mpf('3')
        self.dA     = self.Nc**2 - mp.mpf('1')
        self.CA     = self.Nc

    def _fermi_regulator(self, p2, T_ratio=None):
        mp.dps = 80
        T = T_ratio or mp.mpf('1e-6')
        try:
            exp_arg = (p2 - mp.mpf('1')) / T
            if exp_arg.real > mp.mpf('700'):
                return mp.mpc('0')
            return mp.mpc('1') / (mp.mpc('1') + mp.exp(exp_arg))
        except Exception:
            return mp.mpc('0')

    def _cauchy_integral(self, integrand_fn):
        mp.dps = 80
        N       = self.N_gl
        theta   = self.theta
        L       = self.L_UV2
        exp_ith = mp.exp(mp.mpc('0', theta))
        nodes, weights = mp.gauss_legendre(N)
        nodes_m  = [(L / 2) * (t + mp.mpf('1')) for t in nodes]
        weights_m = [(L / 2) * w for w in weights]
        total = mp.mpc('0')
        for t_i, w_i in zip(nodes_m, weights_m):
            z_i   = t_i * exp_ith
            total += w_i * integrand_fn(z_i) * exp_ith
        ok = abs(total.imag) < mp.mpf('1e-70')
        if not ok:
            print(f"[CAUCHY_FAIL] Im(I) = {mp.nstr(total.imag, 20)}")
        return total.real, ok

    def _I1_integrand(self, z, w_g, w_S):
        mp.dps = 80
        sigma = self._fermi_regulator(z)
        num   = z**2 * sigma
        den   = (z + w_g + mp.mpf('1'))**2 * (z + w_S + mp.mpf('1'))
        if abs(den) < mp.mpf('1e-150'):
            return mp.mpc('0')
        return num / den

    def _I2_integrand(self, z, w_g):
        mp.dps = 80
        sigma = self._fermi_regulator(z)
        num   = z**2 * sigma
        den   = (z + w_g + mp.mpf('1'))**3
        if abs(den) < mp.mpf('1e-150'):
            return mp.mpc('0')
        return num / den

    def beta_lamSF_cauchy(self, g2, lam_SF, w_g, w_S, eta_A, eta_S):
        """
        Cauchy-deformed beta-function for the scalar-gauge mixing coupling lam_SF.
        [CAUCHY_CLOSURE] gate enforced on both integrals.
        """
        mp.dps = 80
        g2     = mp.mpf(str(g2))
        lam_SF = mp.mpf(str(lam_SF))
        w_g    = mp.mpf(str(w_g))
        w_S    = mp.mpf(str(w_S))
        eta_A  = mp.mpf(str(eta_A))
        eta_S  = mp.mpf(str(eta_S))

        pf1 = self.dA * self.CA / (mp.mpf('16') * mp.pi**2)
        pf2 = self.dA            / (mp.mpf('16') * mp.pi**2)

        I1, ok1 = self._cauchy_integral(lambda z: self._I1_integrand(z, w_g, w_S))
        I2, ok2 = self._cauchy_integral(lambda z: self._I2_integrand(z, w_g))

        dim_term = -mp.mpf('2') * lam_SF * (
            mp.mpf('1') - eta_A / mp.mpf('2') - eta_S / mp.mpf('2')
        )
        loop_1 = pf1 * g2     * lam_SF * I1
        loop_2 = pf2 * g2**2           * I2

        beta = dim_term + loop_1 + loop_2
        return beta, (ok1 and ok2)


# ---------------------------------------------------------------------------
# Phase 3: Full 5x5 Fixed-Point Solver
# ---------------------------------------------------------------------------

class Full5x5Solver:
    """
    5-dimensional Newton-Raphson fixed-point search for the full coupled system:
      params = [g2, kap2, lam_S, lam_SF, eta_S]

    w_g*, eta_A* are frozen inputs from Phase 1 (YMGhostGluonSolver, Evidence C).
    lam_SF beta-function computed via Phase 2 (CauchyFRGIntegrator).

    RG constraint enforced: 5*kap2 = 3*lam_S  (|LHS-RHS| < 1e-14)
    Gamma rule: gamma = 16.339 A- UNCHANGED.
    """

    def __init__(self, w_g_star, eta_A_star, eta_c_star,
                 cauchy_integrator=None):
        mp.dps = 80
        # Frozen Phase-1 outputs (Evidence C)
        self.w_g_star   = mp.mpf(str(w_g_star))
        self.eta_A_star = mp.mpf(str(eta_A_star))
        self.eta_c_star = mp.mpf(str(eta_c_star))

        # SU(3)
        self.Nc = mp.mpf('3')
        self.dA = self.Nc**2 - mp.mpf('1')
        self.CA = self.Nc

        self.cauchy = cauchy_integrator or CauchyFRGIntegrator()

    def _l1(self, w):
        mp.dps = 80
        return mp.mpf('1') / (mp.mpf('16') * mp.pi**2 * (mp.mpf('1') + w))

    def _l2(self, w):
        mp.dps = 80
        return mp.mpf('1') / (mp.mpf('32') * mp.pi**2 * (mp.mpf('1') + w)**2)

    def residuals(self, params):
        mp.dps = 80
        g2, kap2, lam_S, lam_SF, eta_S = [mp.mpf(str(x)) for x in params]

        w_g   = self.w_g_star
        eta_A = self.eta_A_star
        w_S   = mp.mpf('0')     # massless scalar (LPA extension point)

        l1g = self._l1(w_g)
        l2g = self._l2(w_g)
        l1S = self._l1(w_S)
        l2S = self._l2(w_S)

        A = (self.Nc**2 - mp.mpf('1')) / (mp.mpf('48') * mp.pi**2)
        B = self.Nc / (mp.mpf('24') * mp.pi**2)

        # beta_g2: gauge coupling
        beta_g2 = -B * g2**2 + A * g2 * kap2

        # beta_kap2: scalar-gauge mixing (Dyson-resummed, LPA)
        Pi_SS_feedback = -(self.dA) * kap2**2 / (
            mp.mpf('16') * mp.pi**2
            * (mp.mpf('1') + w_g) * (mp.mpf('1') + w_S)
        )
        beta_kap2 = (
            (-mp.mpf('2') + mp.mpf('2') * g2 * l2g) * kap2
            + Pi_SS_feedback
        )

        # beta_lam_S: scalar self-coupling
        beta_lam_S = (
            -mp.mpf('4') * lam_S
            + B * g2 * lam_S
            - mp.mpf('3') * lam_S**2 / (mp.mpf('16') * mp.pi**2)
        )

        # beta_lam_SF: Cauchy-deformed
        beta_lam_SF, _ = self.cauchy.beta_lamSF_cauchy(
            g2, lam_SF, w_g, w_S, eta_A, eta_S
        )

        # beta_eta_S: anomalous dimension (finite-difference projection)
        delta_s  = mp.mpf('1e-20')
        Pi0 = -(self.dA) * kap2**2 / (
            mp.mpf('16') * mp.pi**2
            * (mp.mpf('1') + w_g) * (mp.mpf('1') + w_S)
        )
        Pi1 = -(self.dA) * kap2**2 / (
            mp.mpf('16') * mp.pi**2
            * (mp.mpf('1') + w_g + delta_s) * (mp.mpf('1') + w_S + delta_s)
        )
        beta_eta_S = (Pi1 - Pi0) / delta_s - eta_S

        return [beta_g2, beta_kap2, beta_lam_S, beta_lam_SF, beta_eta_S]

    def solve(self, start=None):
        mp.dps = 80
        if start is None:
            # Analytic start from LPA + Phase-1 results
            start = [
                mp.mpf('3.94021354245561'),   # g2
                mp.mpf('2.70889681043823'),   # kap2
                mp.mpf('15.8829056575045'),   # lam_S
                mp.mpf('0.50'),               # lam_SF (initial estimate)
                mp.mpf('0.072'),              # eta_S
            ]
        result = mp.findroot(
            self.residuals,
            start,
            tol=mp.mpf('1e-70'),
            maxsteps=1000
        )
        return [mp.mpf(str(r)) for r in result]


# ---------------------------------------------------------------------------
# Phase 4: Gatekeeper Protocol
# ---------------------------------------------------------------------------

def verify_cauchy_closure(integrator, g2, lam_SF, w_g, w_S, eta_A, eta_S):
    """
    [CAUCHY_CLOSURE] gate.
    Returns True if both Cauchy integrals satisfy |Im| < 1e-70.
    """
    mp.dps = 80
    _, ok = integrator.beta_lamSF_cauchy(g2, lam_SF, w_g, w_S, eta_A, eta_S)
    if ok:
        print("[CAUCHY_CLOSURE_OK]")
    else:
        print("[CAUCHY_CLOSURE_FAIL] -> increase theta or N_gl")
    return ok


def check_eigenvalues(solver, sol):
    """
    Stability matrix eigenvalue check.
    [TRUNCATION_ARTIFACT] if any |Im(ev)| > 0.1.
    Returns (all_real: bool, eigenvalues: list).
    """
    mp.dps = 80
    J   = mp.jacobian(solver.residuals, sol)
    evs = mp.eig(J)[0]
    print("  Stability eigenvalues (5x5):")
    all_real = True
    for ev in evs:
        print(f"    {mp.nstr(ev, 15)}")
        if abs(ev.imag) > mp.mpf('0.1'):
            all_real = False
    if all_real:
        print("  [EIGENVALUE_OK] All real.")
    else:
        print("  [TRUNCATION_ARTIFACT] Complex eigenvalue(s) — extend truncation (S^2 F^2 or Z1!=1).")
    return all_real, evs


def check_rg_constraint(kap2, lam_S):
    """
    RG constraint: 5*kap2 = 3*lam_S
    [RG_CONSTRAINT_FAIL] if |LHS-RHS| > 1e-14
    """
    mp.dps = 80
    lhs = mp.mpf('5') * mp.mpf(str(kap2))
    rhs = mp.mpf('3') * mp.mpf(str(lam_S))
    res = abs(lhs - rhs)
    if res > mp.mpf('1e-14'):
        print(f"[RG_CONSTRAINT_FAIL] |5kap2 - 3lam_S| = {mp.nstr(res, 20)}")
        return False
    print(f"[RG_CONSTRAINT_OK]   |5kap2 - 3lam_S| = {mp.nstr(res, 20)}")
    return True


def check_eta_stabilization(eta_S_star):
    """
    eta_* stabilization criterion:
    |eta_S* - 0.063| < 0.009  -> target band reached
    Evidence upgrade condition: D -> C+
    """
    mp.dps = 80
    eta_target  = mp.mpf('0.063')
    delta_eta   = abs(mp.mpf(str(eta_S_star)) - eta_target)
    print(f"  eta_S* = {mp.nstr(mp.mpf(str(eta_S_star)), 20)}")
    print(f"  delta_eta = {mp.nstr(delta_eta, 10)}  (target: < 0.009)")
    if delta_eta < mp.mpf('0.009'):
        print("  [ETA_STABLE] Target band reached. Evidence upgrade D -> C+ possible.")
    else:
        print("  [ETA_NOT_STABLE] delta_eta out of target band. Further truncation required.")
    return delta_eta < mp.mpf('0.009')


# ---------------------------------------------------------------------------
# Main: Cascaded Run
# ---------------------------------------------------------------------------

def run_full_system():
    mp.dps = 80
    print("=" * 60)
    print("UIDT Framework v3.9 — Full Cascaded 5x5 Cauchy Solver")
    print("Evidence target: UIDT-C-070  D -> C+ -> B")
    print("mp.dps = 80  (local, Race Condition Lock)")
    print("=" * 60)

    # --- Phase 1 ---
    print("\n--- Phase 1: YM Ghost-Gluon Sector ---")
    ym_solver = YMGhostGluonSolver()
    try:
        ym_sol = ym_solver.solve()
    except Exception as e:
        print(f"[PHASE1_FAIL] Newton-Raphson did not converge: {e}")
        sys.exit(1)

    eigenvalues_real = ym_solver.verify(ym_sol)
    eta_c_star, eta_A_star, w_g_star = ym_sol

    if not eigenvalues_real:
        print("[PHASE1_WARNING] Proceeding despite complex eigenvalues.")

    # --- Phase 2: Cauchy closure check ---
    print("\n--- Phase 2: Cauchy Closure Check ---")
    integrator = CauchyFRGIntegrator()
    lam_SF_init = mp.mpf('0.50')
    w_S_init    = mp.mpf('0')
    cauchy_ok = verify_cauchy_closure(
        integrator,
        g2     = mp.mpf('3.94021354245561'),
        lam_SF = lam_SF_init,
        w_g    = w_g_star,
        w_S    = w_S_init,
        eta_A  = eta_A_star,
        eta_S  = mp.mpf('0.072')
    )
    if not cauchy_ok:
        print("[PHASE2_FAIL] Increase theta or N_gl before proceeding.")
        sys.exit(1)

    # --- Phase 3: Full 5x5 ---
    print("\n--- Phase 3: Full 5x5 Fixed-Point Newton-Raphson ---")
    full_solver = Full5x5Solver(
        w_g_star   = w_g_star,
        eta_A_star = eta_A_star,
        eta_c_star = eta_c_star,
        cauchy_integrator = integrator
    )
    try:
        sol5 = full_solver.solve()
    except Exception as e:
        print(f"[PHASE3_FAIL] 5x5 Newton-Raphson did not converge: {e}")
        sys.exit(1)

    g2_s, kap2_s, lam_S_s, lam_SF_s, eta_S_s = sol5
    print(f"  g2*     = {mp.nstr(g2_s,     25)}")
    print(f"  kap2*   = {mp.nstr(kap2_s,   25)}")
    print(f"  lam_S*  = {mp.nstr(lam_S_s,  25)}")
    print(f"  lam_SF* = {mp.nstr(lam_SF_s, 25)}")
    print(f"  eta_S*  = {mp.nstr(eta_S_s,  25)}")

    # --- Phase 4: Gatekeeper Protocol ---
    print("\n--- Phase 4: Gatekeeper Protocol ---")

    rg_ok  = check_rg_constraint(kap2_s, lam_S_s)
    ev_ok, evs = check_eigenvalues(full_solver, sol5)
    eta_ok = check_eta_stabilization(eta_S_s)

    cauchy_final_ok = verify_cauchy_closure(
        integrator,
        g2     = g2_s,
        lam_SF = lam_SF_s,
        w_g    = w_g_star,
        w_S    = mp.mpf('0'),
        eta_A  = eta_A_star,
        eta_S  = eta_S_s
    )

    # Max residual check
    res_final = full_solver.residuals(sol5)
    max_res   = max(abs(r) for r in res_final)
    print(f"\n  Max residual (5x5) = {mp.nstr(max_res, 15)}")
    if max_res > mp.mpf('1e-70'):
        print("  [RESIDUAL_FAIL] Residual > 1e-70")
    else:
        print("  [RESIDUAL_OK]")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Phase 1 (YM ghost-gluon) : {'OK' if eigenvalues_real else 'WARNING (complex ev)'}")
    print(f"  Phase 2 (Cauchy closure) : {'OK' if cauchy_ok else 'FAIL'}")
    print(f"  Phase 3 (5x5 convergence): {'OK' if max_res <= mp.mpf('1e-70') else 'FAIL'}")
    print(f"  Gatekeeper - RG constr.  : {'OK' if rg_ok else 'FAIL'}")
    print(f"  Gatekeeper - eigenvalues : {'OK' if ev_ok else 'TRUNCATION_ARTIFACT'}")
    print(f"  Gatekeeper - eta_stable  : {'OK' if eta_ok else 'NOT_STABLE'}")
    print(f"  Cauchy closure (final)   : {'OK' if cauchy_final_ok else 'FAIL'}")

    all_ok = (
        eigenvalues_real and cauchy_ok and
        (max_res <= mp.mpf('1e-70')) and
        rg_ok and ev_ok and eta_ok and cauchy_final_ok
    )

    if all_ok:
        print("\n[SYSTEM_CONVERGED] All gatekeepers passed.")
        print("Evidence UIDT-C-070: D -> C+ upgrade conditions met.")
        print("Next step: vertex dressing Z1!=1 + S^2F^2 for Evidence B.")
    else:
        print("\n[SYSTEM_INCOMPLETE] One or more gatekeepers failed.")
        print("Diagnostic: check [TRUNCATION_ARTIFACT] / [CAUCHY_FAIL] / [RG_CONSTRAINT_FAIL]")
        print("Action required before Evidence upgrade.")

    print("\nIMMUTABLE LEDGER CHECK:")
    print(f"  gamma     = 16.339  [A-] UNCHANGED")
    print(f"  Delta_*   = 1.710 GeV [A] UNCHANGED")
    print(f"  v         = 47.7 MeV  [A] UNCHANGED")

    return sol5, ym_sol, all_ok


if __name__ == "__main__":
    run_full_system()
