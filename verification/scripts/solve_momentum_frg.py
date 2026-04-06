# verification/scripts/solve_momentum_frg.py
# UIDT Framework v3.9 -- Momentum-Dependent FRG Solver
# Claim:   UIDT-C-070 (Evidence D, Stratum III)
# Target:  FRG fixed point for S F^2 operator in SU(3) Yang-Mills
#          eta_* ~ 0.072 supports gamma ~ (Lambda_UV/Lambda_IR)^{eta_*}
#
# GOVERNANCE (UIDT Constitution):
#   - mp.dps = 80 LOCAL in every method (Race Condition Lock: NEVER in config.py)
#   - No float(), no round(), no silent approximation
#   - Residual target: |F_i| < 1e-70 for all components
#   - RG constraint 5*kappa^2 = 3*lambda: tolerance < 1e-14  => [RG_CONSTRAINT_FAIL]
#   - Ledger constants IMMUTABLE: gamma=16.339 [A-], Delta*=1.710 GeV [A], v=47.7 MeV [A]
#   - No unittest.mock / MagicMock / patch in verification
#   - Mass Deletion Lock: do not remove > 10 lines from /core or /modules without confirmation
#
# Two-stage solver:
#   Stage A: YMGhostGluonSolver   -- dynamic (eta_c, eta_A, w_g) from ghost-gluon DSE
#   Stage B: CauchyFRGIntegrator  -- contour-deformed Gauss-Legendre for Pi_SS(p^2)
#
# Evidence upgrade path:
#   D  (current)  -- LPA, eta_A=0, p^2=0 -- eta_* ~ 0.072, complex eigenvalues possible
#   C  (target)   -- dynamic w_g* + Dyson resummation via Cauchy integrator
#   B  (future)   -- full d/dp^2 projection + S^2F^2 operator + eta_A != 0
#
# Reproduction:
#   python verification/scripts/solve_momentum_frg.py
#   Requirements: Python 3.x, mpmath >= 1.3.0
#   Output log:  output/rg_run_log_momentum.txt

import mpmath as mp
import os

# ---------------------------------------------------------------------------
# IMMUTABLE LEDGER CONSTANTS  (UIDT Constitution -- do NOT modify)
# ---------------------------------------------------------------------------
_GAMMA_LEDGER   = '16.339'   # [A-] phenomenological kinetic VEV
_DELTA_STAR_GEV = '1.710'    # [A]  Yang-Mills spectral gap
_V_MEV          = '47.7'     # [A]  vacuum VEV
_W0_LEDGER      = '-0.99'    # [C]  dark-energy EOS parameter
_ET_LEDGER      = '2.44'     # [C]  torsion threshold MeV
# ---------------------------------------------------------------------------


class CauchyFRGIntegrator:
    """
    Gauss-Legendre integration on a Cauchy-deformed contour

        z(t) = t * exp(i * theta),   t in [0, sqrt(Lambda_UV_sq)]

    to avoid Minkowski-space poles in the momentum-space FRG flow.
    Fermi-Dirac smoothing of the Litim regulator for analytic continuation.

    Gate:  Im(integral) < 1e-70  =>  [CAUCHY_CLOSURE OK]
           otherwise             =>  [CAUCHY_CLOSURE FAIL]

    Tuning rule: alpha_rec = min(100, 2*N_grid)
    """

    def __init__(self, N_grid=64, Lambda_UV=None, theta_rad=None):
        mp.dps = 80
        self.N      = N_grid
        self.Luv_sq = (Lambda_UV or mp.mpf('10')) ** 2
        self.theta  = theta_rad if theta_rad is not None else mp.mpf('0.2')
        self.alpha  = min(mp.mpf('100'), mp.mpf('2') * mp.mpf(self.N))
        self._init_cauchy_grid()

    def _init_cauchy_grid(self):
        mp.dps = 80
        nodes, weights = mp.gauss_legendre(self.N)
        t_nodes   = [(self.Luv_sq / 2) * (x + 1) for x in nodes]
        t_weights = [(self.Luv_sq / 2) * w for w in weights]
        phase = mp.exp(mp.mpc(0, self.theta))
        self.z_nodes   = [t * phase for t in t_nodes]
        self.z_weights = [w * phase for w in t_weights]

    def theta_smooth(self, z):
        """Fermi-Dirac smooth continuation of Litim Theta(k^2 - q^2)."""
        mp.dps = 80
        return mp.mpf('1') / (mp.mpf('1') + mp.exp(self.alpha * (abs(z) - mp.mpf('1'))))

    def evaluate_loop_integral(self, integrand_func, kappa2, w_g, w_S, s):
        """
        I(s) = (1/16pi^2) * SUM_j  W_j * z_j * Theta_smooth(z_j) * f(z_j)
        integrand_func: f(z, kappa2, w_g, w_S, s) -> mpmath complex
        """
        mp.dps = 80
        result = mp.mpc(0)
        for z, w in zip(self.z_nodes, self.z_weights):
            fval   = integrand_func(z, kappa2, w_g, w_S, s)
            result += w * z * self.theta_smooth(z) * fval
        return result / (mp.mpf('16') * mp.pi ** 2)

    def verify_cauchy_closure(self, complex_result, label='Integral'):
        """[CAUCHY_CLOSURE] gate."""
        mp.dps = 80
        im = abs(complex_result.imag)
        if im > mp.mpf('1e-70'):
            print(f'[CAUCHY_CLOSURE FAIL] {label}: Im = {mp.nstr(im, 20)}')
            print(f'  -> Increase N_grid or theta; check for pole proximity.')
            return None
        print(f'[CAUCHY_CLOSURE OK]   {label}: Im = {mp.nstr(im, 20)}')
        return complex_result.real


class YMGhostGluonSolver:
    """
    Self-consistent 3x3 Newton-Raphson for the YM ghost-gluon sector.
    Replaces Stratum-II DSE input w_g=0.25 with a dynamically solved w_g*.

    Parameter vector: x = (eta_c, eta_A, w_g)
    Residuals (Taylor-scheme Landau gauge, SU(N_c)):
      F1 = eta_c - K*(1 - eta_A/6)/(1+w_g)
      F2 = eta_A - (3g^2/16pi^2)*[13/6*(1-eta_A/6)/(1+w_g) - (1-eta_c/3)/12]
      F3 = (2-eta_A)*w_g - K/(1+w_g)^2

    Analytical 3x3 Jacobian -- no finite differences.
    Convergence: max|F_i| < 1e-70
    """

    def __init__(self, g2=None):
        mp.dps = 80
        self.Nc  = mp.mpf('3')
        self.pi2 = mp.mpf('16') * mp.pi ** 2
        self.g2  = g2 if g2 is not None else mp.mpf('3.94021354245561')
        self.K   = self.g2 * self.Nc / self.pi2

    def residual(self, x):
        mp.dps = 80
        eta_c, eta_A, w_g = [mp.mpf(str(v)) for v in x]
        K  = self.K
        g2 = self.g2
        p2 = self.pi2
        F1 = eta_c - K * (1 - eta_A / 6) / (1 + w_g)
        F2 = (eta_A
              - (3 * g2 / p2) * (
                  mp.mpf('13') / mp.mpf('6')
                  * (1 - eta_A / 6) / (1 + w_g)
                  - (1 - eta_c / 3) / mp.mpf('12')
              ))
        F3 = (2 - eta_A) * w_g - K / (1 + w_g) ** 2
        return [F1, F2, F3]

    def jacobian(self, x):
        """Analytical 3x3 Jacobian J_ij = dF_i/dx_j."""
        mp.dps = 80
        eta_c, eta_A, w_g = [mp.mpf(str(v)) for v in x]
        K  = self.K
        g2 = self.g2
        p2 = self.pi2
        inv1 = mp.mpf('1') / (1 + w_g)
        inv2 = inv1 ** 2
        inv3 = inv1 ** 3
        fA   = 1 - eta_A / 6

        J11 = mp.mpf('1')
        J12 = K * inv1 / mp.mpf('6')
        J13 = K * fA * inv2

        J21 = -g2 / (mp.mpf('12') * p2)
        J22 = mp.mpf('1') + mp.mpf('13') * g2 / (mp.mpf('192') * mp.pi ** 2 * (1 + w_g))
        J23 = mp.mpf('13') * g2 / (mp.mpf('32') * mp.pi ** 2) * fA * inv2

        J31 = mp.mpf('0')
        J32 = -w_g
        J33 = (2 - eta_A) + 2 * K * inv3

        return mp.matrix([[J11, J12, J13], [J21, J22, J23], [J31, J32, J33]])

    def solve(self, start=None, maxiter=300):
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
            J     = self.jacobian(x)
            delta = mp.lu_solve(J, [-f for f in F])
            x     = [x[k] + delta[k] for k in range(3)]
        norm = max(abs(f) for f in self.residual(x))
        print(f'[NOT_CONVERGED] |F|_max={mp.nstr(norm, 10)}')
        return x

    def verify(self, sol):
        mp.dps = 80
        eta_c, eta_A, w_g = sol
        lines = []
        lines.append('=== UIDT YM Ghost-Gluon Fixed Point (mp.dps=80) ===')
        lines.append(f'eta_c  = {mp.nstr(eta_c, 40)}')
        lines.append(f'eta_A  = {mp.nstr(eta_A, 40)}')
        lines.append(f'w_g*   = {mp.nstr(w_g,   40)}')
        lines.append('  (replaces external DSE input w_g=0.25 [Stratum II])')
        delta_wg = abs(w_g - mp.mpf('0.25'))
        lines.append(f'delta_wg (vs DSE seed 0.25) = {mp.nstr(delta_wg, 20)}')

        J   = self.jacobian(sol)
        evs = mp.eig(J)[0]
        lines.append('Stability eigenvalues:')
        for ev in evs:
            tag = '  [TRUNCATION_ARTIFACT]' if abs(ev.imag) > mp.mpf('0.1') else '  [OK]'
            lines.append(f'  {mp.nstr(ev, 15)}{tag}')
        for ln in lines:
            print(ln)
        return lines


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    mp.dps = 80
    log_lines = []

    def log(s=''):
        print(s)
        log_lines.append(str(s))

    log('=== UIDT FRG Solver -- TKT-20260405 ===')
    log(f'mp.dps = {mp.dps}  (local, UIDT Race Condition Lock)')
    log(f'Ledger: gamma={_GAMMA_LEDGER} [A-]  Delta*={_DELTA_STAR_GEV} GeV [A]  v={_V_MEV} MeV [A]')
    log()

    # Stage A: YM ghost-gluon sector
    log('--- Stage A: YM Ghost-Gluon Sector ---')
    ym = YMGhostGluonSolver()
    sol_ym = ym.solve()
    eta_c_star, eta_A_star, w_g_star = sol_ym
    verify_lines = ym.verify(sol_ym)
    log_lines.extend(verify_lines)
    log()

    # Stage B: Cauchy integrator self-test
    log('--- Stage B: Cauchy Integrator Self-Test ---')

    def _dyson_kernel(z, kappa2, w_g, w_S, s):
        mp.dps = 80
        denom = ((1 + w_S + s + z) * (1 + w_g + s + z) - kappa2) ** 2
        if abs(denom) < mp.mpf('1e-200'):
            return mp.mpc(0)
        return mp.mpc('1') / denom

    integrator = CauchyFRGIntegrator(N_grid=64)
    raw = integrator.evaluate_loop_integral(
        _dyson_kernel,
        kappa2=mp.mpf('2.71'),
        w_g=w_g_star,
        w_S=mp.mpf('0'),
        s=mp.mpf('0'),
    )
    phys = integrator.verify_cauchy_closure(raw, 'Pi_SS(s=0, w_g*)')
    if phys is not None:
        log(f'Pi_SS(s=0, w_g*) = {mp.nstr(phys, 40)}')
    log()

    # RG constraint check: 5*kappa^2 = 3*lambda  (LPA seed values)
    kappa2_seed = mp.mpf('2.71')
    lam_seed    = mp.mpf('15.88')
    lhs    = 5 * kappa2_seed
    rhs    = 3 * lam_seed
    rg_res = abs(lhs - rhs)
    if rg_res > mp.mpf('1e-14'):
        log(f'[RG_CONSTRAINT_FAIL] |5*kappa^2 - 3*lambda| = {mp.nstr(rg_res, 20)}')
    else:
        log(f'[RG_CONSTRAINT_OK]   |5*kappa^2 - 3*lambda| = {mp.nstr(rg_res, 20)}')
    log()

    # Write output log
    here    = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, '..', '..', 'output')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'rg_run_log_momentum.txt')
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(log_lines))
    print(f'[LOG WRITTEN] {out_path}')


if __name__ == '__main__':
    main()
