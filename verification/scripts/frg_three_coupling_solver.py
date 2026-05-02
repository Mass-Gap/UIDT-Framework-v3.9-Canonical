"""UIDT Framework v3.9 — Three-Coupling FRG Solver

Couplings: (kappa_FRG, lambda_S, g_s)
Regulator: Litim (optimised), d=4 Euclidean
Method:    Dormand-Prince RK45, 80-dps mpmath throughout

EVIDENCE REGISTER
-----------------
kappa_FRG   [D]   – dimensionless field minimum rho_0/k^2; flows UV->IR
kappa_coup  [A-]  – scalar-gluon coupling kappa=0.5 (LEDGER, IMMUTABLE)
lambda_S    [A-]  – scalar quartic (LEDGER, IMMUTABLE)
g_s         [B]   – 1-loop QCD running coupling, Nc=3, Nf=0

SYMBOL DISAMBIGUATION
----------------------
kappa_FRG  != kappa_coup
  kappa_FRG  lives inside the FRG effective potential U_k(rho).
             At the Wilson-Fisher fixed point kappa_FRG* ~ 1/(6*lambda_S_*).
  kappa_coup is the Lagrangian coupling L_int = -(kappa_coup/4) S^2 F^2.
             It appears in the RG constraint 5*kappa_coup^2 = 3*lambda_S.
  A matching condition kappa_coup = f(kappa_FRG, k_match, g_s) is
  CURRENTLY AN OPEN PROBLEM within UIDT. No analytic form is committed here.
  Any numerical identification of the two objects is [TENSION ALERT] until
  a derivable matching equation is established.

QCD BETA FUNCTION (1-loop, pure glue, Nc=3, Nf=0)
--------------------------------------------------
b0 = (11*Nc - 2*Nf) / (3 * 16*pi^2)  [exact rational in mpmath]
beta_g = -b0 * g_s^3

LPA SCALAR BETA FUNCTIONS (Litim, d=4, O(1) scalar field)
----------------------------------------------------------
With dimensionless mass u = m_k^2 / k^2 and Litim threshold function:
  l_0 = 1 / (1 + u)^2
  partial_t lambda_S = (lambda_S^2 * l_0^2 * 4) / (4*pi^2)
  partial_t kappa_FRG = kappa_FRG - (lambda_S * l_0) / (4*pi^2)
  partial_t u = -2*u + (lambda_S * l_0) / (4*pi^2)
  (g_s enters only through a g_s^2 * kappa_coup^2 threshold correction;
   that correction is set to zero here until the matching is resolved.)

CONSTITUTION COMPLIANCE
------------------------
- mp.dps=80 declared locally inside EVERY method
- No float(), no round(), no centralised precision
- RG constraint 5*kappa_coup^2 = 3*lambda_S checked at UV entry
- VacuumInstabilityException raised when |1+u|^2 < 1e-70
- STIFF_HALT when adaptive step falls below min_step
- Mass Deletion Lock: no block >10 lines deleted without confirmation
"""

from mpmath import mp, mpf, exp, pi, fabs, nstr


class VacuumInstabilityException(Exception):
    pass


class RGConstraintViolation(Exception):
    pass


# ---------------------------------------------------------------------------
# Immutable ledger constants  [Evidence A-]
# ---------------------------------------------------------------------------
def _ledger():
    mp.dps = 80
    kappa_coup = mpf('1') / mpf('2')                       # kappa_coup = 0.5  [A-]
    lambda_S   = mpf('5') * kappa_coup**2 / mpf('3')       # RG constraint [A-]
    return kappa_coup, lambda_S


KAPPA_COUP_LEDGER, LAMBDA_S_LEDGER = _ledger()


# ---------------------------------------------------------------------------
# Three-Coupling Solver
# ---------------------------------------------------------------------------
class UIDT_FRG_ThreeCoupling_RK45:
    """Dormand-Prince RK45 solver for (kappa_FRG, lambda_S_run, u, g_s).

    State vector: [kappa_FRG, lambda_S_run, u, g_s]
    where u = m_k^2 / k^2 (dimensionless mass squared)

    Parameters
    ----------
    tol_str     : RK45 local error tolerance (string for exact mpf)
    min_step_str: minimum allowed step size before STIFF_HALT
    Nc          : number of QCD colours (default 3)
    Nf          : number of active quark flavours (default 0, pure glue)
    """

    def __init__(self,
                 tol_str='1e-10',
                 min_step_str='1e-20',
                 Nc=3,
                 Nf=0):
        mp.dps = 80
        self.tol      = mpf(tol_str)
        self.min_step = mpf(min_step_str)
        self.Nc       = mpf(str(Nc))
        self.Nf       = mpf(str(Nf))

        # Dormand-Prince Butcher tableau — exact rational mpf
        self.c2  = mpf('1')  / mpf('5')
        self.c3  = mpf('3')  / mpf('10')
        self.c4  = mpf('4')  / mpf('5')
        self.c5  = mpf('8')  / mpf('9')
        self.a21 = mpf('1')   / mpf('5')
        self.a31 = mpf('3')   / mpf('40')
        self.a32 = mpf('9')   / mpf('40')
        self.a41 = mpf('44')  / mpf('45')
        self.a42 = mpf('-56') / mpf('15')
        self.a43 = mpf('32')  / mpf('9')
        self.a51 = mpf('19372')  / mpf('6561')
        self.a52 = mpf('-25360') / mpf('2187')
        self.a53 = mpf('64448')  / mpf('6561')
        self.a54 = mpf('-212')   / mpf('729')
        self.a61 = mpf('9017')   / mpf('3168')
        self.a62 = mpf('-355')   / mpf('33')
        self.a63 = mpf('46732')  / mpf('5247')
        self.a64 = mpf('49')     / mpf('176')
        self.a65 = mpf('-5103')  / mpf('18656')
        self.b1  = mpf('35')    / mpf('384')
        self.b3  = mpf('500')   / mpf('1113')
        self.b4  = mpf('125')   / mpf('192')
        self.b5  = mpf('-2187') / mpf('6784')
        self.b6  = mpf('11')    / mpf('84')
        self.e1  = mpf('71')     / mpf('57600')
        self.e3  = mpf('-71')    / mpf('16695')
        self.e4  = mpf('71')     / mpf('1920')
        self.e5  = mpf('-17253') / mpf('339200')
        self.e6  = mpf('22')     / mpf('525')
        self.e7  = mpf('-1')     / mpf('40')

    def _beta_gs(self, g_s):
        """1-loop QCD: beta_g = -b0 * g_s^3
        b0 = (11*Nc - 2*Nf) / (3 * 16*pi^2)  — exact mpf
        Evidence: B
        """
        mp.dps = 80
        numerator   = mpf('11') * self.Nc - mpf('2') * self.Nf
        denominator = mpf('3') * mpf('16') * pi**2
        b0 = numerator / denominator
        return -b0 * g_s**3

    def _litim_l0(self, u):
        mp.dps = 80
        denom = (mpf('1') + u)**2
        if fabs(denom) < mpf('1e-70'):
            raise VacuumInstabilityException(
                f"VACUUM_INSTABILITY_TRIGGER: Litim denominator (1+u)^2 -> 0, u = {nstr(u, 15)}"
            )
        return mpf('1') / denom

    def _beta_scalar(self, kappa_frg, lam, u):
        """Returns (d_kappa_frg, d_lam, d_u).
        Standard O(N=1) LPA beta functions, Litim regulator, d=4.
        g_s^2 threshold correction set to zero pending matching resolution.
        [OPEN_MATCHING_PROBLEM]
        """
        mp.dps = 80
        l0  = self._litim_l0(u)
        pre = mpf('1') / (mpf('4') * pi**2)

        d_lam   =  mpf('4') * lam**2 * l0**2 * pre
        d_kappa =  kappa_frg - lam * l0 * pre
        d_u     = -mpf('2') * u + lam * l0 * pre

        return d_kappa, d_lam, d_u

    def _rhs(self, t, state):
        mp.dps = 80
        kappa_frg, lam, u, g_s = state
        d_kappa, d_lam, d_u = self._beta_scalar(kappa_frg, lam, u)
        d_gs = self._beta_gs(g_s)
        return [d_kappa, d_lam, d_u, d_gs]

    def _dp_step(self, t, state, h):
        mp.dps = 80
        f  = self._rhs
        k1 = f(t, state)
        s2 = [state[i] + h * self.a21 * k1[i] for i in range(4)]
        k2 = f(t + h * self.c2, s2)
        s3 = [state[i] + h * (self.a31*k1[i] + self.a32*k2[i]) for i in range(4)]
        k3 = f(t + h * self.c3, s3)
        s4 = [state[i] + h * (self.a41*k1[i] + self.a42*k2[i] + self.a43*k3[i]) for i in range(4)]
        k4 = f(t + h * self.c4, s4)
        s5 = [state[i] + h * (self.a51*k1[i] + self.a52*k2[i] + self.a53*k3[i] + self.a54*k4[i]) for i in range(4)]
        k5 = f(t + h * self.c5, s5)
        s6 = [state[i] + h * (self.a61*k1[i] + self.a62*k2[i] + self.a63*k3[i] + self.a64*k4[i] + self.a65*k5[i]) for i in range(4)]
        k6 = f(t + h, s6)
        y5 = [state[i] + h * (self.b1*k1[i] + self.b3*k3[i] + self.b4*k4[i] + self.b5*k5[i] + self.b6*k6[i]) for i in range(4)]
        k7 = f(t + h, y5)
        err_vec = [h * (self.e1*k1[i] + self.e3*k3[i] + self.e4*k4[i] + self.e5*k5[i] + self.e6*k6[i] + self.e7*k7[i]) for i in range(4)]
        err = max(fabs(e) for e in err_vec)
        return y5, err

    def _check_rg_constraint(self, kappa_coup, lam):
        mp.dps = 80
        lhs      = mpf('5') * kappa_coup**2
        rhs      = mpf('3') * lam
        residual = fabs(lhs - rhs)
        if residual > mpf('1e-14'):
            raise RGConstraintViolation(
                f"[RG_CONSTRAINT_FAIL] 5*kappa_coup^2 - 3*lambda_S = {nstr(residual, 20)}"
            )

    def solve(self,
              t_start_str='-0.001',
              t_end_str='-8.0',
              kappa_frg_uv_str='0.1',
              lam_uv_str=None,
              u_uv_str='0.01',
              gs_uv_str='1.0'):
        """Run FRG flow UV -> IR.

        Parameters (all strings for exact mpf)
        ----------
        t_start_str      : RG time t = ln(k/Lambda_UV)
        t_end_str        : IR endpoint
        kappa_frg_uv_str : UV dimensionless field minimum
        lam_uv_str       : UV lambda_S (None = use LEDGER)
        u_uv_str         : UV dimensionless mass squared
        gs_uv_str        : UV strong coupling g_s

        Returns
        -------
        history : list of (t, [kappa_FRG, lam, u, g_s])
        report  : dict with endpoint summary and TENSION_ALERT flags
        """
        mp.dps = 80

        lam_uv     = LAMBDA_S_LEDGER if lam_uv_str is None else mpf(lam_uv_str)
        kappa_coup = KAPPA_COUP_LEDGER

        self._check_rg_constraint(kappa_coup, lam_uv)

        t     = mpf(t_start_str)
        t_end = mpf(t_end_str)
        state = [mpf(kappa_frg_uv_str), lam_uv, mpf(u_uv_str), mpf(gs_uv_str)]
        h     = mpf('-0.05')

        history = [(t, list(state))]
        status  = 'RUNNING'
        k_crit  = None
        steps   = 0

        while t > t_end:
            try:
                y_new, err = self._dp_step(t, state, h)
            except VacuumInstabilityException as exc:
                status = 'VACUUM_INSTABILITY'
                k_crit = exp(t)
                print(f"[VACUUM_INSTABILITY] k_crit = {nstr(k_crit, 15)} GeV | {exc}")
                break
            except Exception as exc:
                status = f'SOLVER_ERROR: {exc}'
                break

            if err < self.tol:
                t     = t + h
                state = y_new
                history.append((t, list(state)))
                steps += 1
                if err > mpf('0'):
                    h = h * min(mpf('4'), mpf('0.9') * (self.tol / err) ** mpf('0.2'))
            else:
                if err > mpf('0'):
                    h = h * mpf('0.9') * (self.tol / err) ** mpf('0.2')

            if fabs(h) < self.min_step:
                status = 'STIFF_HALT'
                k_crit = exp(t)
                print(f"[STIFF_HALT] t = {nstr(t, 10)}, k = {nstr(k_crit, 10)} GeV")
                break

        if status == 'RUNNING':
            status = 'COMPLETED'

        kf, lf, uf, gsf = state[0], state[1], state[2], state[3]
        wf_kappa_analytic = mpf('1') / (mpf('6') * lf) if lf != 0 else mpf('0')
        tension_ratio     = fabs(kf - kappa_coup) / kappa_coup if kappa_coup != 0 else mpf('0')

        report = {
            'status':               status,
            'steps':                steps,
            'k_crit_GeV':           nstr(exp(t_end) if k_crit is None else k_crit, 15),
            't_final':              nstr(t, 15),
            'kappa_FRG_final':      nstr(kf, 15),
            'lambda_S_final':       nstr(lf, 15),
            'u_final':              nstr(uf, 15),
            'g_s_final':            nstr(gsf, 15),
            'WF_kappa_analytic':    nstr(wf_kappa_analytic, 15),
            'TENSION_kFRG_vs_coup': nstr(tension_ratio, 10),
            'OPEN_MATCHING_PROBLEM':
                'kappa_coup = f(kappa_FRG, k_match, g_s) is NOT YET DERIVED. '
                'Numerical identification of kappa_FRG with kappa_coup is [TENSION ALERT]. '
                'Evidence for any shifted-FP claim: B (lattice-compatible) at best.',
        }

        return history, report


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    mp.dps = 80
    print("=" * 72)
    print("UIDT FRG Three-Coupling Solver  |  Nc=3, Nf=0, Litim d=4, mp.dps=80")
    print("=" * 72)

    solver = UIDT_FRG_ThreeCoupling_RK45(tol_str='1e-10', min_step_str='1e-20', Nc=3, Nf=0)

    history, report = solver.solve(
        t_start_str      = '-0.01',
        t_end_str        = '-8.0',
        kappa_frg_uv_str = '0.1',
        lam_uv_str       = None,
        u_uv_str         = '0.01',
        gs_uv_str        = '1.2',
    )

    print("\nSOLVER REPORT")
    print("-" * 72)
    for key, val in report.items():
        print(f"  {key:<30} : {val}")
    print("-" * 72)
    print(f"  Steps accepted               : {report['steps']}")
    print(f"  History length               : {len(history)}")
    print("=" * 72)
