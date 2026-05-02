"""
UIDT FRG Solver — Dormand-Prince RK45, 80-dps mpmath
Adaptive Wetterich flow with Litim regulator under LPA.

Architecture: UIDT_FRG_Solver_RK45
Module location: verification/scripts/frg_solver_rk45.py

UIDT Constitution compliance:
  - mp.dps = 80 declared locally in every method
  - No float() usage
  - RG constraint 5κ² = 3λS enforced at start
  - VacuumInstabilityException for IR divergence
  - Ledger constants: Δ* = 1.710 GeV, κ_UV ≈ 1.0 (dimensionless)
"""

from mpmath import mp, mpf, exp, log, sqrt, fabs, nstr


class VacuumInstabilityException(Exception):
    """
    Raised when the IR denominator k² + m² collapses below 1e-70.
    The k_crit value at which the topological protection breaks
    is encoded in the exception message.
    """
    pass


class UIDT_FRG_Solver_RK45:
    """
    Dormand-Prince RK45 solver for the Wetterich FRG flow equation
    under the Local Potential Approximation (LPA) with the Litim regulator.

    State vector: [kappa, lambda_S, m_squared]
      kappa    — dimensionless field minimum (κ)  [Evidence A-]
      lambda_S — quartic self-coupling (λS)       [Evidence A-]
      m_squared — scalar mass squared (m²)        [Evidence B]

    RG-flow variable: t = ln(k/k_UV), flows from 0 (UV) to t_end < 0 (IR).

    All arithmetic in mp.dps = 80 (local declaration per UIDT Constitution).
    """

    def __init__(self, tol_str='1e-14', min_step_str='1e-20'):
        mp.dps = 80

        # --- Tolerance and step-size guards ---
        self.tol       = mpf(tol_str)
        self.min_step  = mpf(min_step_str)
        self.max_step  = mpf('0.5')

        # ---------------------------------------------------------------
        # Dormand-Prince Butcher tableau — exact rational mpf values
        # Reference: Dormand & Prince (1980), J. Comput. Appl. Math. 6, 19-26
        # ---------------------------------------------------------------
        mp.dps = 80

        # c-nodes (time fractions)
        self.c2 = mpf('1') / mpf('5')
        self.c3 = mpf('3') / mpf('10')
        self.c4 = mpf('4') / mpf('5')
        self.c5 = mpf('8') / mpf('9')
        self.c6 = mpf('1')
        self.c7 = mpf('1')

        # a-matrix (lower triangular)
        self.a21 = mpf('1') / mpf('5')

        self.a31 = mpf('3') / mpf('40')
        self.a32 = mpf('9') / mpf('40')

        self.a41 = mpf('44') / mpf('45')
        self.a42 = mpf('-56') / mpf('15')
        self.a43 = mpf('32') / mpf('9')

        self.a51 = mpf('19372') / mpf('6561')
        self.a52 = mpf('-25360') / mpf('2187')
        self.a53 = mpf('64448') / mpf('6561')
        self.a54 = mpf('-212') / mpf('729')

        self.a61 = mpf('9017') / mpf('3168')
        self.a62 = mpf('-355') / mpf('33')
        self.a63 = mpf('46732') / mpf('5247')
        self.a64 = mpf('49') / mpf('176')
        self.a65 = mpf('-5103') / mpf('18656')

        # b-coefficients — 5th-order solution (propagated)
        self.b1 = mpf('35') / mpf('384')
        self.b2 = mpf('0')
        self.b3 = mpf('500') / mpf('1113')
        self.b4 = mpf('125') / mpf('192')
        self.b5 = mpf('-2187') / mpf('6784')
        self.b6 = mpf('11') / mpf('84')
        self.b7 = mpf('0')

        # e-coefficients — error estimate (difference b5th - b4th)
        self.e1 = mpf('71') / mpf('57600')
        self.e2 = mpf('0')
        self.e3 = mpf('-71') / mpf('16695')
        self.e4 = mpf('71') / mpf('1920')
        self.e5 = mpf('-17253') / mpf('339200')
        self.e6 = mpf('22') / mpf('525')
        self.e7 = mpf('-1') / mpf('40')

    # ------------------------------------------------------------------
    # Physical kernel
    # ------------------------------------------------------------------

    def litim_core(self, k, m_squared):
        """
        Evaluates the Litim regulator fraction:
            k^4 / (k² + m²)
        This is the analytically integrated result of the Litim-regulated
        one-loop flow in d=4 under LPA, up to a prefactor of 1/(16π²).

        IR-divergence guard: raises VacuumInstabilityException when
        |k² + m²| < 1e-70.
        """
        mp.dps = 80
        k_sq      = k * k
        denom     = k_sq + m_squared

        if fabs(denom) < mpf('1e-70'):
            raise VacuumInstabilityException(
                f"VACUUM_INSTABILITY_TRIGGER: denominator collapsed "
                f"at k = {nstr(k, 30, strip_zeros=False)}, "
                f"denom = {nstr(denom, 30, strip_zeros=False)}"
            )

        return (k_sq * k_sq) / denom

    def beta_functions(self, t, state):
        """
        LPA β-functions for [κ, λS, m²] with Litim regulator in d=4.

        Wetterich equation under LPA:
            ∂_t V_k = (1/(16π²)) * k^4 / (k² + V''_k)

        For the O(N=1) scalar theory in the symmetric phase, with
        V''_k = m²_k, the β-functions are derived from the one-loop
        Wetterich equation with ∂_t R_k = 2k² Θ(k²-q²).

        Flow equations (one-loop LPA, Litim regulator, d=4, N=1):
            ∂_t m²  = 12 α λS L          where L = k^4/(k²+m²)
            ∂_t λS  = -36 α λS² L²/k^4
            ∂_t κ   = 0                   (subleading at d=4, LO)

        Prefactor: α = 1/(16π²)
        Evidence category: B (lattice-compatible one-loop structure).
        """
        mp.dps = 80
        k        = exp(t)           # k = e^t (t = ln k/k_UV, k_UV=1 GeV)
        kappa, lambda_s, m_sq = state[0], state[1], state[2]

        # Prefactor α = 1/(16π²)
        pi      = mp.pi
        alpha   = mpf('1') / (mpf('16') * pi * pi)

        L       = self.litim_core(k, m_sq)    # k^4/(k²+m²)
        k_sq    = k * k

        # N=1 scalar: (N+2)=3, (N+8)=9, standard O(N) LPA coefficients
        dm_sq   = mpf('12') * alpha * lambda_s * L

        # ∂_t λS: Landau-pole generating term
        dlambda = mpf('-36') * alpha * lambda_s * lambda_s * L * L / (k_sq * k_sq)

        # κ flow subleading at d=4 LO
        dkappa  = mpf('0')

        return [dkappa, dlambda, dm_sq]

    # ------------------------------------------------------------------
    # RK45 step
    # ------------------------------------------------------------------

    def _rk45_step(self, t, state, h):
        """
        Single Dormand-Prince step. Returns (y5, error_norm).
        y5 = 5th-order solution; error_norm = L∞ of normalised error vector.
        """
        mp.dps = 80

        def F(tt, ss):
            return self.beta_functions(tt, ss)

        def add(s, ds, fac):
            return [s[i] + fac * ds[i] for i in range(len(s))]

        def addm(base, *pairs):
            n = len(base)
            result = list(base)
            for fac, ds in pairs:
                for i in range(n):
                    result[i] = result[i] + fac * ds[i]
            return result

        k1 = F(t,                   state)
        k2 = F(t + self.c2 * h,     add(state, k1, self.a21 * h))
        k3 = F(t + self.c3 * h,     addm(state,
                                         (self.a31 * h, k1),
                                         (self.a32 * h, k2)))
        k4 = F(t + self.c4 * h,     addm(state,
                                         (self.a41 * h, k1),
                                         (self.a42 * h, k2),
                                         (self.a43 * h, k3)))
        k5 = F(t + self.c5 * h,     addm(state,
                                         (self.a51 * h, k1),
                                         (self.a52 * h, k2),
                                         (self.a53 * h, k3),
                                         (self.a54 * h, k4)))
        k6 = F(t + self.c6 * h,     addm(state,
                                         (self.a61 * h, k1),
                                         (self.a62 * h, k2),
                                         (self.a63 * h, k3),
                                         (self.a64 * h, k4),
                                         (self.a65 * h, k5)))

        # 5th-order propagation
        y5 = addm(state,
                  (self.b1 * h, k1),
                  (self.b3 * h, k3),
                  (self.b4 * h, k4),
                  (self.b5 * h, k5),
                  (self.b6 * h, k6))

        # FSAL: 7th stage evaluated at y5
        k7 = F(t + h, y5)

        # Error vector (dense output difference)
        err = addm([mpf('0')] * len(state),
                   (self.e1 * h, k1),
                   (self.e3 * h, k3),
                   (self.e4 * h, k4),
                   (self.e5 * h, k5),
                   (self.e6 * h, k6),
                   (self.e7 * h, k7))

        # L∞ norm of error, normalised by state magnitude
        err_norm = max(
            fabs(err[i]) / (mpf('1e-10') + fabs(y5[i]))
            for i in range(len(y5))
        )

        return y5, err_norm

    # ------------------------------------------------------------------
    # RG-constraint verification
    # ------------------------------------------------------------------

    def verify_rg_constraint(self, kappa, lambda_s):
        """
        Verifies the UIDT RG fixed-point constraint: 5κ² = 3λS.
        Raises AssertionError with [RG_CONSTRAINT_FAIL] if violated.
        Tolerance: |LHS - RHS| < 1e-14.
        """
        mp.dps = 80
        lhs = mpf('5') * kappa * kappa
        rhs = mpf('3') * lambda_s
        residual = fabs(lhs - rhs)
        if residual >= mpf('1e-14'):
            raise AssertionError(
                f"[RG_CONSTRAINT_FAIL] 5κ²={nstr(lhs,20)} ≠ 3λS={nstr(rhs,20)}, "
                f"residual={nstr(residual,10)}"
            )
        return residual

    # ------------------------------------------------------------------
    # Main solve loop
    # ------------------------------------------------------------------

    def solve(self, t_start_str, t_end_str, initial_state_strs,
              verify_constraint=True):
        """
        Integrate the FRG flow from t_start (UV) to t_end (IR).

        Parameters
        ----------
        t_start_str : str
            Start RG-time, e.g. '0' (k = k_UV = 1 GeV).
        t_end_str : str
            End RG-time, e.g. '-10' (k = e^{-10} k_UV ≈ 45 MeV).
        initial_state_strs : list[str]
            [kappa_UV, lambda_S_UV, m_squared_UV] as strings.
        verify_constraint : bool
            If True, verifies 5κ² = 3λS at UV entry (default True).

        Returns
        -------
        history : list of (t, state) tuples
        status  : 'COMPLETE' | 'VACUUM_INSTABILITY' | 'STIFF_HALT'
        k_crit  : mpf or None — scale at which instability triggered
        """
        mp.dps = 80

        t      = mpf(t_start_str)
        t_end  = mpf(t_end_str)
        state  = [mpf(v) for v in initial_state_strs]
        h      = mpf('-0.1')   # negative: UV → IR direction

        if t <= t_end:
            raise ValueError("t_start must be > t_end (UV → IR flow).")

        if verify_constraint:
            self.verify_rg_constraint(state[0], state[1])

        history = [(t, list(state))]
        status  = 'COMPLETE'
        k_crit  = None

        while t > t_end:
            # Clip final step to exactly reach t_end
            if t + h < t_end:
                h = t_end - t

            try:
                y5, err_norm = self._rk45_step(t, state, h)
            except VacuumInstabilityException as e:
                status = 'VACUUM_INSTABILITY'
                k_crit = exp(t)
                history.append((t, list(state)))
                print(f"[VACUUM_INSTABILITY] {e}")
                print(f"  k_crit = {nstr(k_crit, 30)} GeV")
                break

            # Accept step if error within tolerance or step size at minimum
            if err_norm < self.tol or fabs(h) <= self.min_step:
                t     = t + h
                state = y5
                history.append((t, list(state)))

            # Adaptive step-size: h_new = h * safety * (tol/err)^0.2
            if err_norm > mpf('0'):
                safety  = mpf('9') / mpf('10')
                h_new   = h * safety * (self.tol / err_norm) ** mpf('1') / mpf('5')
                h_new   = h * safety * (self.tol / err_norm) ** (mpf('1') / mpf('5'))
            else:
                h_new = h * mpf('5')

            # Clamp to [min_step, max_step]
            if fabs(h_new) > self.max_step:
                h_new = -self.max_step if h < mpf('0') else self.max_step
            if fabs(h_new) < self.min_step:
                print(f"[SYSTEM-HALT] Step size {nstr(fabs(h_new),10)} "
                      f"< min_step {nstr(self.min_step,10)}. Flow stiff at t={nstr(t,15)}.")
                status = 'STIFF_HALT'
                break

            h = h_new

        return history, status, k_crit


# ------------------------------------------------------------------
# Standalone baseline test: t=0 (UV) → t=-10 (IR)
# ------------------------------------------------------------------

def run_baseline_test():
    """
    Physical UV initial conditions satisfying 5κ² = 3λS exactly:
      κ_UV   = 1          (mpf exact)
      λS_UV  = 5/3        (mpf exact fraction)
      m²_UV  = 0          (symmetric phase entry)
    """
    mp.dps = 80

    kappa_UV   = mpf('1')
    lambda_UV  = mpf('5') / mpf('3')
    m_sq_UV    = mpf('0')

    solver = UIDT_FRG_Solver_RK45(tol_str='1e-14', min_step_str='1e-20')

    print("=" * 60)
    print("UIDT_FRG_Solver_RK45 — Baseline Test")
    print(f"  κ_UV   = {nstr(kappa_UV,  20)}")
    print(f"  λS_UV  = {nstr(lambda_UV, 20)}")
    print(f"  m²_UV  = {nstr(m_sq_UV,   20)}")
    lhs = mpf('5') * kappa_UV * kappa_UV
    rhs = mpf('3') * lambda_UV
    print(f"  RG constraint 5κ²=3λS: {nstr(lhs,5)} = {nstr(rhs,5)}  ✓")
    print("=" * 60)

    history, status, k_crit = solver.solve(
        t_start_str='0',
        t_end_str='-10',
        initial_state_strs=[
            nstr(kappa_UV,  40),
            nstr(lambda_UV, 40),
            nstr(m_sq_UV,   40),
        ],
        verify_constraint=True,
    )

    print(f"\nStatus : {status}")
    print(f"Steps  : {len(history)}")
    if k_crit is not None:
        print(f"k_crit = {nstr(k_crit, 30)} GeV")

    print("\n--- Final state ---")
    t_f, s_f = history[-1]
    print(f"  t     = {nstr(t_f,   20)}")
    print(f"  κ     = {nstr(s_f[0], 20)}")
    print(f"  λS    = {nstr(s_f[1], 20)}")
    print(f"  m²    = {nstr(s_f[2], 20)}")

    return history, status, k_crit


if __name__ == "__main__":
    run_baseline_test()
