# verification/scripts/solve_momentum_frg.py
# UIDT Framework v3.9 — Momentum-Dependent FRG Solver
# Claim:   UIDT-C-070 (Evidence D, Stratum III)
# Target:  FRG fixed point for S F^2 operator in SU(3) Yang-Mills
#          eta_* ~ 0.072 supports gamma ~ (Lambda_UV/Lambda_IR)^{eta_*}
# RULES:
#   - mp.dps = 80 LOCAL (never in config.py)
#   - No float(), no round()
#   - Residual target: |F_i| < 1e-70
#   - RG constraint: 5*kappa^2 = 3*lambda, tolerance < 1e-14
#
# Reproduction:
#   python verification/scripts/solve_momentum_frg.py
# Requirements: mpmath >= 1.3.0

import mpmath as mp


# ---------------------------------------------------------------------------
# Part 1: Cauchy-Deformed Loop Integrator
# ---------------------------------------------------------------------------

class CauchyFRGIntegrator:
    """
    Gauss-Legendre integrator on a Cauchy-deformed contour z(t) = t * exp(i*theta).
    Avoids the kinematic pole at s* ~ 0.526 on the real axis (see GAP_ANALYSIS_CLAY.md).
    [CAUCHY_CLOSURE] protocol: Im(I) < 1e-70 required for physical observables.
    """

    def __init__(self, N_grid=32, Lambda_UV=None, theta_rad=None):
        mp.dps = 80
        self.N = N_grid
        self.Luv_sq = (Lambda_UV or mp.mpf('10')) ** 2
        self.theta = theta_rad or mp.mpf('0.2')
        # Tuning rule: alpha_rec = min(100, 2*N)
        self.alpha = min(mp.mpf('100'), mp.mpf('2') * mp.mpf(self.N))
        self._init_cauchy_grid()

    def _init_cauchy_grid(self):
        mp.dps = 80
        nodes, weights = mp.gauss_legendre(self.N)
        # Scale to t in [0, Lambda_UV^2]
        t_nodes   = [(self.Luv_sq / 2) * (x + 1) for x in nodes]
        t_weights = [(self.Luv_sq / 2) * w for w in weights]
        # Complex rotation
        phase = mp.exp(mp.mpc(0, self.theta))
        self.z_nodes   = [t * phase for t in t_nodes]
        self.z_weights = [w * phase for w in t_weights]

    def theta_smooth(self, z):
        """Analytic continuation of Litim regulator via Fermi-Dirac smoothing."""
        mp.dps = 80
        exponent = self.alpha * (abs(z) - mp.mpf('1'))
        return mp.mpf('1') / (mp.mpf('1') + mp.exp(exponent))

    def evaluate_loop_integral(self, integrand_func, kappa2, w_g, w_S, s):
        """
        Contour integral I(s) = (1/16pi^2) * sum_j W_j * z_j * Theta_smooth(z_j) * f(z_j).
        integrand_func signature: f(z, kappa2, w_g, w_S, s) -> complex mpmath value.
        """
        mp.dps = 80
        result = mp.mpc(0)
        for z, w in zip(self.z_nodes, self.z_weights):
            reg   = z * self.theta_smooth(z)
            fval  = integrand_func(z, kappa2, w_g, w_S, s)
            result += w * reg * fval
        return result / (mp.mpf('16') * mp.pi ** 2)

    def verify_cauchy_closure(self, complex_result, observable_name='Integral'):
        """[CAUCHY_CLOSURE] gate: Im(I) < 1e-70, else [CAUCHY_CLOSURE_FAIL]."""
        mp.dps = 80
        imag_part = abs(complex_result.imag)
        if imag_part > mp.mpf('1e-70'):
            print(f'[CAUCHY_CLOSURE_FAIL] {observable_name}: Im = {mp.nstr(imag_part, 20)}')
            print(f'  -> N={self.N} insufficient or pole proximity. Increase N or theta.')
            return None
        return complex_result.real


# ---------------------------------------------------------------------------
# Part 2: YM Ghost-Gluon Sector Solver (3x3 Newton-Raphson)
# ---------------------------------------------------------------------------

class YMGhostGluonSolver:
    """
    Solves the coupled fixed-point system for the Yang-Mills ghost-gluon sector.
    Eliminates the external DSE input w_g = 0.25 (Stratum II) by generating
    the gluon mass dynamically from the FP gap equation (Evidence D -> C).

    Parameter vector: x = (eta_c, eta_A, w_g)
    Residual:         F(x) = 0 (see equations below)
    Jacobian:         J(x) = dF/dx  (analytical, no finite differences)
    Convergence:      |F_i| < 1e-70 for all i

    Affected constants (all read-only here):
      gamma  = 16.339  [A-]  UNCHANGED
      Delta* = 1.710 GeV [A]  used as external check only
    """

    def __init__(self, g2=None):
        mp.dps = 80
        self.Nc  = mp.mpf('3')
        self.CA  = mp.mpf('3')               # SU(3): C_A = N_c
        self.pi2 = mp.mpf('16') * mp.pi ** 2
        # g^2 at LPA fixed point (UIDT-C-070, Evidence D)
        self.g2  = g2 if g2 is not None else mp.mpf('3.94021354245561')
        self.K   = self.g2 * self.CA / self.pi2

    def residual(self, x):
        """
        F1 = eta_c - K * (1 - eta_A/6) / (1 + w_g)
        F2 = eta_A - (3*g^2/16pi^2) * [13/6*(1-eta_A/6)/(1+w_g) - (1-eta_c/3)/12]
        F3 = (2 - eta_A)*w_g - K/(1+w_g)^2   [gap eq. at fixed point: dt w_g = 0]
        """
        mp.dps = 80
        eta_c, eta_A, w_g = [mp.mpf(str(v)) for v in x]
        K  = self.K
        g2 = self.g2
        p2 = self.pi2

        F1 = eta_c - K * (1 - eta_A / 6) / (1 + w_g)

        F2 = (eta_A
              - (3 * g2 / p2) * (
                  mp.mpf('13') / mp.mpf('6') * (1 - eta_A / 6) / (1 + w_g)
                  - (1 - eta_c / 3) / mp.mpf('12')
              ))

        F3 = (2 - eta_A) * w_g - K / (1 + w_g) ** 2

        return [F1, F2, F3]

    def jacobian(self, x):
        """
        Analytical 3x3 Jacobian J_ij = dF_i/dx_j.
        No finite differences — full 80-dps determinism.
        """
        mp.dps = 80
        eta_c, eta_A, w_g = [mp.mpf(str(v)) for v in x]
        K  = self.K
        g2 = self.g2
        p2 = self.pi2

        inv1  = mp.mpf('1') / (1 + w_g)
        inv2  = inv1 ** 2
        inv3  = inv1 ** 3
        fac_A = 1 - eta_A / 6

        # Row 1: dF1/d(eta_c, eta_A, w_g)
        J11 = mp.mpf('1')
        J12 = K / (6 * (1 + w_g))
        J13 = K * fac_A * inv2

        # Row 2: dF2/d(eta_c, eta_A, w_g)
        J21 = -g2 / (mp.mpf('192') * mp.pi ** 2)
        J22 = mp.mpf('1') + mp.mpf('13') * g2 / (mp.mpf('192') * mp.pi ** 2 * (1 + w_g))
        J23 = mp.mpf('13') * g2 / (mp.mpf('32') * mp.pi ** 2) * fac_A * inv2

        # Row 3: dF3/d(eta_c, eta_A, w_g)
        J31 = mp.mpf('0')
        J32 = -w_g
        J33 = (2 - eta_A) + 2 * K * inv3

        return mp.matrix([
            [J11, J12, J13],
            [J21, J22, J23],
            [J31, J32, J33],
        ])

    def _newton_step(self, x):
        mp.dps = 80
        F = self.residual(x)
        J = self.jacobian(x)
        delta = mp.lu_solve(J, [-f for f in F])
        return [x[i] + delta[i] for i in range(3)]

    def solve(self, start=None, maxiter=200):
        """Newton-Raphson fixed-point search, convergence target |F_i| < 1e-70."""
        mp.dps = 80
        x = [mp.mpf(str(v)) for v in (start or [
            mp.mpf('0.04'), mp.mpf('0.25'), mp.mpf('0.25')
        ])]
        for i in range(maxiter):
            F    = self.residual(x)
            norm = max(abs(f) for f in F)
            if norm < mp.mpf('1e-70'):
                print(f'[CONVERGED] iter={i}  |F|_max={mp.nstr(norm, 10)}')
                return x
            x = self._newton_step(x)
        norm = max(abs(f) for f in self.residual(x))
        print(f'[NOT_CONVERGED] |F|_max={mp.nstr(norm, 10)}')
        return x

    def verify(self, sol):
        """Post-solve verification: eigenvalues, Delta* signal, RG consistency."""
        mp.dps = 80
        eta_c, eta_A, w_g = sol
        print('=== UIDT YM Ghost-Gluon Fixed Point (mp.dps=80) ===')
        print(f'eta_c  = {mp.nstr(eta_c, 25)}')
        print(f'eta_A  = {mp.nstr(eta_A, 25)}')
        print(f'w_g*   = {mp.nstr(w_g,   25)}')
        print(f'  (replaces external DSE input w_g=0.25 [Stratum II])')

        # Delta* consistency check
        delta_star = mp.mpf('1.710')  # [A] canonical, read-only
        diff = abs(w_g - delta_star)
        print(f'\nDelta* check: |w_g* - 1.710| = {mp.nstr(diff, 10)}')
        if diff < mp.mpf('0.1'):
            print('  [SIGNAL] w_g* consistent with Delta* scale (Stratum III)')
        else:
            print('  [INFO]   w_g* != Delta* at current truncation — extend to full Cauchy solver')

        # Stability eigenvalues
        J   = self.jacobian(sol)
        evs = mp.eig(J)[0]
        print('\nStability eigenvalues:')
        for ev in evs:
            tag = '[TRUNCATION_ARTIFACT]' if abs(ev.imag) > mp.mpf('0.1') else '[OK]'
            print(f'  {mp.nstr(ev, 15)}  {tag}')


# ---------------------------------------------------------------------------
# Part 3: Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    mp.dps = 80
    print('=== UIDT FRG Solver — TKT-20260405 ===')
    print(f'mp.dps = {mp.dps}\n')

    # Stage A: YM ghost-gluon fixed point
    print('--- Stage A: YM Ghost-Gluon Sector ---')
    ym = YMGhostGluonSolver()
    sol_ym = ym.solve()
    ym.verify(sol_ym)

    # Stage B: Cauchy integrator self-test (pole avoidance)
    print('\n--- Stage B: Cauchy Integrator Self-Test ---')

    def _test_integrand(z, kappa2, w_g, w_S, s):
        """Dyson self-energy kernel for scalar sector."""
        mp.dps = 80
        denom = ((1 + w_S + s + z) * (1 + w_g + s + z) - kappa2) ** 2
        if abs(denom) < mp.mpf('1e-200'):
            return mp.mpc(0)
        return mp.mpc('1') / denom

    integrator = CauchyFRGIntegrator(N_grid=64)
    raw = integrator.evaluate_loop_integral(
        _test_integrand,
        kappa2=mp.mpf('2.71'),
        w_g=sol_ym[1],   # use dynamically solved eta_A as proxy
        w_S=mp.mpf('0'),
        s=mp.mpf('0'),
    )
    phys = integrator.verify_cauchy_closure(raw, 'Pi_SS(s=0)')
    if phys is not None:
        print(f'Pi_SS(s=0) = {mp.nstr(phys, 20)}  [CAUCHY_CLOSURE OK]')
