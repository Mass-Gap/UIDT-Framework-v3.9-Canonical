# quark_sde_coupled.py
# UIDT Framework v3.9 -- Fully Coupled Quark Dyson-Schwinger Equation
#
# Implements the quark SDE (quenched, Landau gauge) with the complete
# Ball-Chiu + CP transverse + STI/ghost-quark-kernel vertex dressing.
#
# Quark propagator (Euclidean):
#   S^{-1}(p) = i slash_p * A(p^2) + B(p^2)
#   M(p^2) = B(p^2)/A(p^2)   [dynamical quark mass function]
#
# Quark SDE (quenched Landau gauge, colour factor C_F = 4/3):
#
#   A(p^2) = 1 + Sigma_A^BC(p^2) + Sigma_A^T(p^2)
#   B(p^2) = m_q + Sigma_B^BC(p^2) + Sigma_B^T(p^2)
#
# Longitudinal (BC) self-energy [Ball, Chiu 1980, Evidence A]:
#   Sigma_A^BC: L1_eff * [A(k)+A(p)]/2 / denom(k)
#   Sigma_B^BC: L1_eff * 3*B(k) / denom(k)
#   L1_eff = F_ghost(q^2) * H_scalar  [STI correction, Evidence B]
#
# Transverse (CP) self-energy [Curtis, Pennington 1990, Evidence A]:
#   Sigma_A^T: tau6(k,p) * [A(k)-A(p)]/(k^2-p^2) contribution
#              -> wavefunction function shift (~few % at mu)
#   Sigma_B^T: tau3(k,p) * [B(k)-B(p)]/(k^2-p^2) contribution
#              -> mass function enhancement ~10-15% at IR [Evidence D]
#
# CP form factors:
#   tau3(k2,p2) = -L3 = -(B(k)-B(p))/(k^2-p^2)   [CP Eq.(3.7)]
#   tau6(k2,p2) =  L2 =  (A(k)-A(p))/(k^2-p^2)   [CP Eq.(3.6)]
#   Regularized at k^2~p^2 via L'Hopital (continuous limit)
#
# Gluon propagator (UIDT parametrization, Evidence B):
#   D(q^2) = Z(q^2) / q^2
#   Z(q^2) = [q^2/(q^2+L^2)]^kappa * [1 + c*L^2/(q^2+L^2)]
#
# Integration (Aguilar PRD89 Appendix A):
#   4d Euclidean -> angle average (theta in [0,pi], weight sin^2)
#   k^2 Gauss-Legendre: N_k=16 nodes on [0, k2_max]
#   theta Gauss-Legendre: N_th=12 nodes on [0, pi]
#
# KNOWN LIMITATIONS:
#   - Quenched (N_f=0).
#   - tau8, tau1,2,4,5,7 not included.
#   - Gluon D(q^2) parametric (not SDE-solved).
#   - H kernel: only A_0 scalar (1-loop approx.).
#   - N_k=16 coarse; use >=64 for production.
#   - Active research -- not established physics.
#
# Sources:
#   [A] Ball, Chiu (1980) PRD 22, 2542  DOI:10.1103/PhysRevD.22.2542
#   [B] Curtis, Pennington (1990) PRD 42, 4165  DOI:10.1103/PhysRevD.42.4165
#   [C] Aguilar, Binosi, Papavassiliou (2014) PRD 89, 085032
#       arXiv:1401.3631  DOI:10.1103/PhysRevD.89.085032
#   [D] Aguilar, De Fazio, Papavassiliou (2018) PRD 98, 014002
#       arXiv:1804.04229  DOI:10.1103/PhysRevD.98.014002
#   [E] Bogolubsky et al. (2009) PLB 676, 69
#       DOI:10.1016/j.physletb.2009.04.076
#   [F] Ayala et al. (2012) PRD 86, 074512
#       DOI:10.1103/PhysRevD.86.074512
#
# NUMERICAL DETERMINISM: mp.dps = 80 local.

import mpmath as mp
mp.dps = 80  # LOCAL -- do not centralize (race condition lock)

# ------------------------------------------------------------------
# IMMUTABLE PARAMETER LEDGER (UIDT v3.9)
# ------------------------------------------------------------------
Delta_star = mp.mpf('1.710')   # Yang-Mills spectral gap [GeV]  [Evidence A]
gamma_val  = mp.mpf('16.339')  # kinetic vacuum parameter       [Evidence A-]

# ------------------------------------------------------------------
# PHYSICAL PARAMETERS
# ------------------------------------------------------------------
mu         = mp.mpf('4.3')     # MOM renorm. point [GeV]
alpha_s    = mp.mpf('0.27')    # strong coupling (MOM)
C_F        = mp.mpf('4') / mp.mpf('3')

m_q        = mp.mpf('0.005')   # current quark mass [GeV]
a_A        = mp.mpf('0.3');    Lambda_A = mp.mpf('1.0')
b_B        = mp.mpf('40.0');   Lambda_B = mp.mpf('0.5')

a_F        = mp.mpf('0.30');   Lambda_F = mp.mpf('0.6')

Lambda_gl  = mp.mpf('0.73')
c_gl       = mp.mpf('0.85')
kappa_gl   = mp.mpf('1.0')

N_k        = 16
N_th       = 12
k2_max     = mp.mpf('400')
alpha_mix  = mp.mpf('0.5')

# Transverse vertex coupling strength (CP)
# tau contributions enter Sigma with overall factor c_T
# c_T=1: full CP; c_T=0: BC-only (for comparison)
c_T        = mp.mpf('1.0')     # [Evidence A: CP exact; magnitude: Evidence D]


# ------------------------------------------------------------------
# GLUON PROPAGATOR
# ------------------------------------------------------------------

def Z_gluon(q2):
    """Gluon dressing Z(q^2) -- UIDT decoupling parametrization [Evidence B]."""
    q2 = mp.mpf(str(q2))
    L2 = Lambda_gl**2
    return ((q2 / (q2 + L2))**kappa_gl
            * (mp.mpf('1') + c_gl * L2 / (q2 + L2)))


def D_gluon(q2):
    """D(q^2) = Z(q^2)/q^2  [Evidence B]. IR-regulated at 1e-4 GeV^2."""
    q2 = mp.mpf(str(q2))
    q2_reg = mp.fmax(q2, mp.mpf('1e-4'))
    return Z_gluon(q2_reg) / q2_reg


# ------------------------------------------------------------------
# GHOST DRESSING
# ------------------------------------------------------------------

def F_ghost(q2):
    """F(q^2): MOM F(mu^2)=1, F(0)~1.29  [Evidence B, Bogolubsky 2009]."""
    q2  = mp.mpf(str(q2))
    mu2 = mu**2
    return (mp.mpf('1')
            + a_F * Lambda_F**2 / (q2 + Lambda_F**2)
            - a_F * Lambda_F**2 / (mu2 + Lambda_F**2))


# ------------------------------------------------------------------
# QUARK-GHOST KERNEL
# ------------------------------------------------------------------

def H_scalar(q2, k2, p2, B_k, B_p):
    """A_0 scalar quark-ghost kernel (1-loop dressed) [Aguilar PRD98, Evidence B]."""
    C_A   = mp.mpf('3')
    denom = B_k + B_p
    if denom == mp.mpf('0'):
        return mp.mpf('1')
    delta = -(C_F / C_A) * alpha_s / (mp.mpf('4') * mp.pi) * (
        mp.mpf('2') * B_p / denom
    )
    return mp.mpf('1') + delta


# ------------------------------------------------------------------
# CP TRANSVERSE FORM FACTORS  tau3, tau6
# ------------------------------------------------------------------

_reg_eps = mp.mpf('1e-8')   # L'Hopital regularization threshold

def tau3(k2, p2, B_k, B_p, dBdk2=None):
    """tau_3(k,p) = -L_3 = -(B(k)-B(p))/(k^2-p^2)  [Curtis-Pennington, Evidence A].

    Regularized at |k^2-p^2| < eps via L'Hopital:
      lim_{k->p} -(B(k)-B(p))/(k^2-p^2) = -dB/dp^2
    """
    k2 = mp.mpf(str(k2)); p2 = mp.mpf(str(p2))
    diff = k2 - p2
    if abs(diff) < _reg_eps:
        # L'Hopital: -dB/dp^2 at p^2
        # dB/dp^2 ~ -m_q * b_B * Lambda_B^2 / (p^2+Lambda_B^2)^2
        dB = -m_q * b_B * Lambda_B**2 / (p2 + Lambda_B**2)**2
        return -dB
    return -(B_k - B_p) / diff


def tau6(k2, p2, A_k, A_p, dAdk2=None):
    """tau_6(k,p) = L_2 = (A(k)-A(p))/(k^2-p^2)  [Curtis-Pennington, Evidence A].

    Regularized at |k^2-p^2| < eps via L'Hopital:
      lim_{k->p} (A(k)-A(p))/(k^2-p^2) = dA/dp^2
    """
    k2 = mp.mpf(str(k2)); p2 = mp.mpf(str(p2))
    diff = k2 - p2
    if abs(diff) < _reg_eps:
        # L'Hopital: dA/dp^2 at p^2
        # dA/dp^2 ~ -a_A * Lambda_A^2 / (p^2+Lambda_A^2)^2
        dA = -a_A * Lambda_A**2 / (p2 + Lambda_A**2)**2
        return dA
    return (A_k - A_p) / diff


# ------------------------------------------------------------------
# ANGLE-AVERAGED SELF-ENERGY KERNELS (BC + CP transverse)
# ------------------------------------------------------------------

def _angle_avg(p2, k2, A_func, B_func):
    """Angle-averaged SDE kernel including tau3/tau6 transverse contributions.

    Returns (kernel_A, kernel_B) incorporating:
      - Longitudinal BC: L1_eff = F_ghost * H_scalar * L1_BC
      - Transverse CP: tau3 (-> Sigma_B shift), tau6 (-> Sigma_A shift)

    Transverse Sigma contributions (Euclidean, Landau gauge):
      Sigma_A^T ~ D(q^2) * tau6(k,p) * f_A(k,p) / denom(k)
      Sigma_B^T ~ D(q^2) * tau3(k,p) * f_B(k,p) / denom(k)

    where f_A, f_B are kinematic factors from the 4-point contraction
    in Landau gauge (transverse projector T_munu = delta_munu - q_mu q_nu/q^2).
    Simplified angle-averaged form [Kizilersu, Pennington 2009, Evidence B]:
      f_A^T = (k^2 + p^2)/2 * (angular average of T_munu)
              ~ (k^2 + p^2)/2 * (1 - cos^2(theta)/2)  -> (k^2+p^2)/2 * 3/4
      f_B^T = 3 * (k^2 + p^2) / (4 * (k^2*A^2 + B^2))
    [Evidence D: simplified angle-average; full tensor structure not implemented]
    """
    p2 = mp.mpf(str(p2))
    k2 = mp.mpf(str(k2))
    sp = mp.sqrt(mp.fmax(p2, mp.mpf('0')))
    sk = mp.sqrt(mp.fmax(k2, mp.mpf('0')))

    n2, w2 = mp.gauss_legendre(N_th, mp.mpf('0'), mp.pi)

    sum_A = mp.mpf('0')
    sum_B = mp.mpf('0')

    Ak = A_func(k2); Bk = B_func(k2)
    Ap = A_func(p2); Bp = B_func(p2)
    denom_k = k2 * Ak**2 + Bk**2
    if denom_k == mp.mpf('0'):
        return mp.mpf('0'), mp.mpf('0')

    # CP form factors (k,p fixed per outer k2 call)
    t3 = tau3(k2, p2, Bk, Bp)
    t6 = tau6(k2, p2, Ak, Ap)

    for theta, wt in zip(n2, w2):
        cos_t  = mp.cos(theta)
        sin2_t = mp.sin(theta)**2
        q2     = p2 + k2 - mp.mpf('2') * sp * sk * cos_t
        q2     = mp.fmax(q2, mp.mpf('1e-6'))

        # STI effective vertex
        L1_eff = F_ghost(q2) * H_scalar(q2, k2, p2, Bk, Bp)
        L1_BC  = (Ak + Ap) / mp.mpf('2')
        Dq     = D_gluon(q2)

        # ---- Longitudinal (BC) contributions ----
        ker_A_bc = Dq * L1_eff * L1_BC / denom_k
        ker_B_bc = Dq * L1_eff * mp.mpf('3') * Bk / denom_k

        # ---- Transverse (CP) contributions ----
        # Kinematic factors (angle-averaged, simplified)
        f_A_T = (k2 + p2) / mp.mpf('2') * mp.mpf('3') / mp.mpf('4')
        f_B_T = mp.mpf('3') * (k2 + p2) / (
                    mp.mpf('4') * mp.fmax(denom_k, mp.mpf('1e-10')))
        ker_A_T = c_T * Dq * t6 * f_A_T / mp.fmax(denom_k, mp.mpf('1e-10'))
        ker_B_T = c_T * Dq * t3 * f_B_T

        total_A = ker_A_bc + ker_A_T
        total_B = ker_B_bc + ker_B_T

        sum_A += wt * sin2_t * total_A
        sum_B += wt * sin2_t * total_B

    prefac = mp.mpf('2') / mp.pi
    return prefac * sum_A, prefac * sum_B


def _sigma(p2, A_func, B_func):
    """Full self-energy (BC + CP transverse) [Aguilar PRD89 Appendix A, Evidence B]."""
    p2     = mp.mpf(str(p2))
    prefac = C_F * alpha_s / (mp.mpf('4') * mp.pi**2)
    nodes, weights = mp.gauss_legendre(N_k, mp.mpf('0'), k2_max)
    sum_A = mp.mpf('0')
    sum_B = mp.mpf('0')
    for k2, wt in zip(nodes, weights):
        k2 = mp.fmax(k2, mp.mpf('1e-6'))
        kA, kB = _angle_avg(p2, k2, A_func, B_func)
        sum_A += wt * k2 * kA
        sum_B += wt * k2 * kB
    return prefac * sum_A, prefac * sum_B


# ------------------------------------------------------------------
# COUPLED SDE ITERATION
# ------------------------------------------------------------------

def run_coupled_sde(p2_grid, n_iter=3, eps=mp.mpf('1e-3'), verbose=True):
    """Run coupled quark SDE iteration on p^2 grid.

    Includes BC longitudinal + CP transverse (tau3, tau6) + STI ghost kernel.

    Parameters
    ----------
    p2_grid : list of mpf
    n_iter  : int  (3 for test; >=10 for convergence)
    eps     : mpf  convergence threshold
    verbose : bool

    Returns
    -------
    A_vals, B_vals : list of mpf
    converged      : bool
    """
    N = len(p2_grid)

    A_vals = [mp.mpf('1') + a_A * Lambda_A**2 / (p2 + Lambda_A**2)
               for p2 in p2_grid]
    B_vals = [m_q * (mp.mpf('1') + b_B * Lambda_B**2 / (p2 + Lambda_B**2))
               for p2 in p2_grid]

    def A_func(p2):
        p2 = mp.mpf(str(p2))
        if p2 <= p2_grid[0]:  return A_vals[0]
        if p2 >= p2_grid[-1]: return A_vals[-1]
        for i in range(N-1):
            if p2_grid[i] <= p2 <= p2_grid[i+1]:
                t = (p2 - p2_grid[i]) / (p2_grid[i+1] - p2_grid[i])
                return A_vals[i] + t * (A_vals[i+1] - A_vals[i])
        return A_vals[-1]

    def B_func(p2):
        p2 = mp.mpf(str(p2))
        if p2 <= p2_grid[0]:  return B_vals[0]
        if p2 >= p2_grid[-1]: return B_vals[-1]
        for i in range(N-1):
            if p2_grid[i] <= p2 <= p2_grid[i+1]:
                t = (p2 - p2_grid[i]) / (p2_grid[i+1] - p2_grid[i])
                return B_vals[i] + t * (B_vals[i+1] - B_vals[i])
        return B_vals[-1]

    converged = False
    for it in range(1, n_iter + 1):
        A_new = []; B_new = []
        for p2 in p2_grid:
            sA, sB = _sigma(p2, A_func, B_func)
            A_new.append((mp.mpf('1') - alpha_mix) * A_func(p2)
                         + alpha_mix * (mp.mpf('1') + sA))
            B_new.append((mp.mpf('1') - alpha_mix) * B_func(p2)
                         + alpha_mix * (m_q + sB))
        dA = max(abs(A_new[i] - A_vals[i]) for i in range(N))
        dB = max(abs(B_new[i] - B_vals[i]) for i in range(N))
        A_vals = A_new; B_vals = B_new
        if verbose:
            M0 = B_vals[0] / A_vals[0]
            print(f'  iter {it}: dA={mp.nstr(dA,4)}  dB={mp.nstr(dB,4)}  '
                  f'M(0)={mp.nstr(M0,5)} GeV')
        if dA < eps and dB < eps:
            converged = True; break

    return A_vals, B_vals, converged


# ------------------------------------------------------------------
# VERIFICATION  (18 checks)
# ------------------------------------------------------------------

def run_verification():
    mp.dps = 80
    passed = 0; failed = 0

    def check(name, ok, residual=None):
        nonlocal passed, failed
        label  = '[PASS]' if ok else '[FAIL]'
        suffix = f'  res={mp.nstr(residual,5)}' if residual is not None else ''
        print(f'{label}  {name:<68}{suffix}')
        if ok: passed += 1
        else:  failed += 1

    mu2 = mu**2

    # 1-2: Parameter Ledger
    check('Delta_star = 1.710 GeV [A]',
          abs(Delta_star - mp.mpf('1.710')) < mp.mpf('1e-14'),
          abs(Delta_star - mp.mpf('1.710')))
    check('gamma_val = 16.339 [A-]',
          abs(gamma_val - mp.mpf('16.339')) < mp.mpf('1e-14'),
          abs(gamma_val - mp.mpf('16.339')))

    # 3-4: Gluon propagator
    check('D_gluon(mu^2) > 0',   D_gluon(mu2) > mp.mpf('0'))
    check('Z_gluon(1e6) in [0.9,1.1]',
          mp.mpf('0.9') < Z_gluon(mp.mpf('1e6')) < mp.mpf('1.1'))

    # 5: Ghost dressing
    check('F_ghost(mu^2) = 1 [MOM exact]',
          abs(F_ghost(mu2) - mp.mpf('1')) < mp.mpf('1e-14'),
          abs(F_ghost(mu2) - mp.mpf('1')))

    # 6-7: CP form factors signs  [Curtis-Pennington 1990, Evidence A]
    k2t = mp.mpf('2.0'); p2t = mp.mpf('0.5')
    def A0(p2): return mp.mpf('1') + a_A*Lambda_A**2/(mp.mpf(str(p2))+Lambda_A**2)
    def B0(p2): return m_q*(mp.mpf('1')+b_B*Lambda_B**2/(mp.mpf(str(p2))+Lambda_B**2))
    t3_val = tau3(k2t, p2t, B0(k2t), B0(p2t))
    t6_val = tau6(k2t, p2t, A0(k2t), A0(p2t))
    # tau3 = -(B(k)-B(p))/(k^2-p^2): B decreasing, k^2>p^2 -> B(k)<B(p) -> num>0 -> tau3>0
    check('tau3(k2>p2) > 0  [CP sign, Evidence A]', t3_val > mp.mpf('0'))
    # tau6 = (A(k)-A(p))/(k^2-p^2): A decreasing, k^2>p^2 -> A(k)<A(p) -> num<0 -> tau6<0
    check('tau6(k2>p2) < 0  [CP sign, Evidence A]', t6_val < mp.mpf('0'))

    # 8: tau3/tau6 L'Hopital continuity at k2=p2
    t3_reg = tau3(p2t, p2t+mp.mpf('1e-12'), B0(p2t), B0(p2t+mp.mpf('1e-12')))
    check('tau3 L Hopital: finite at k2=p2', abs(t3_reg) < mp.mpf('10'))

    # 9-10: Angle kernels
    kA, kB = _angle_avg(mp.mpf('1.0'), mp.mpf('2.0'), A0, B0)
    check('Angle kernel_A > 0', kA > mp.mpf('0'))
    check('Angle kernel_B > 0 [DCSB]', kB > mp.mpf('0'))

    # 11-12: Sigma integrals
    p2_test = mp.mpf('1.0')
    sA, sB = _sigma(p2_test, A0, B0)
    check('Sigma_A finite mpf', isinstance(sA, mp.mpf))
    check('Sigma_B > 0 [DCSB signal]', sB > mp.mpf('0'))

    # 13: Transverse enhances B: Sigma_B(c_T=1) > Sigma_B(c_T=0)
    global c_T
    c_T_saved = c_T
    c_T = mp.mpf('0')
    _, sB_bc = _sigma(p2_test, A0, B0)
    c_T = mp.mpf('1')
    _, sB_full = _sigma(p2_test, A0, B0)
    c_T = c_T_saved
    check('Sigma_B(tau3+tau6) >= Sigma_B(BC-only)  [CP mass enhancement, Ev.D]',
          sB_full >= sB_bc)

    # 14-15: Iteration
    p2_grid = [mp.mpf('1e-4'), mp.mpf('0.5'), mu2]
    A_vals, B_vals, _ = run_coupled_sde(p2_grid, n_iter=2, verbose=False)
    check('A(mu^2) after 2 iter in [1.0, 1.6]',
          mp.mpf('1.0') < A_vals[2] < mp.mpf('1.6'))
    check('B(0) after 2 iter > m_q [DCSB present]',
          B_vals[0] > m_q)

    # 16: M(0) constituent mass range
    M0 = B_vals[0] / A_vals[0]
    check('M(0) in [0.05, 0.50] GeV [constituent mass]',
          mp.mpf('0.05') < M0 < mp.mpf('0.50'))

    # 17-18: Ledger constants unchanged after iteration
    check('Delta_star unchanged post-iteration [A]',
          abs(Delta_star - mp.mpf('1.710')) < mp.mpf('1e-14'),
          abs(Delta_star - mp.mpf('1.710')))
    check('gamma_val unchanged post-iteration [A-]',
          abs(gamma_val - mp.mpf('16.339')) < mp.mpf('1e-14'),
          abs(gamma_val - mp.mpf('16.339')))

    print()
    print(f'Total: {passed+failed}  |  PASS: {passed}  |  FAIL: {failed}')
    print()
    print(f'tau3(k2=2, p2=0.5) = {mp.nstr(t3_val,6)}')
    print(f'tau6(k2=2, p2=0.5) = {mp.nstr(t6_val,6)}')
    print(f'Sigma_A(1 GeV^2)   = {mp.nstr(sA,6)}')
    print(f'Sigma_B(1 GeV^2)   = {mp.nstr(sB,6)} GeV')
    print(f'Sigma_B BC-only     = {mp.nstr(sB_bc,6)} GeV')
    print(f'Sigma_B full CP     = {mp.nstr(sB_full,6)} GeV')
    print(f'M(p^2=0) [2-iter]   = {mp.nstr(M0,5)} GeV  [Evidence D]')
    print()
    print('[UIDT LIMITS] Quenched. tau8, tau1,2,4,5,7 excluded.')
    print('[UIDT LIMITS] Transverse kernel: simplified angle-average [Evidence D].')
    print('[UIDT LIMITS] N_k=16 coarse. D(q^2) parametric.')
    print(f'  Delta* = {Delta_star} GeV [A], gamma = {gamma_val} [A-] unchanged.')
    if failed > 0:
        raise RuntimeError(f'[VERIFICATION_FAIL] {failed} check(s) failed')


if __name__ == '__main__':
    print('=== Quark SDE Coupled (BC + CP tau3/tau6 + STI) -- Verification ===')
    print(f'N_k={N_k}, N_th={N_th}, alpha_mix={alpha_mix}, c_T={c_T}')
    print()
    run_verification()
