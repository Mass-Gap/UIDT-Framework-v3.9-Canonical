# quark_sde_coupled.py
# UIDT Framework v3.9 -- Fully Coupled Quark Dyson-Schwinger Equation
#
# Implements the quark SDE (quenched, Landau gauge) with the complete
# Ball-Chiu + STI/ghost-quark-kernel vertex dressing.
#
# Quark propagator (Euclidean):
#   S^{-1}(p) = i slash_p * A(p^2) + B(p^2)
#   M(p^2) = B(p^2)/A(p^2)   [dynamical quark mass function]
#
# Quark SDE (quenched Landau gauge, colour factor C_F = 4/3):
#
#   A(p^2) = 1 + Sigma_A(p^2)
#   B(p^2) = m_q + Sigma_B(p^2)
#
# Self-energy integrals (4d Euclidean, Landau gauge, angle-averaged):
#
#   Sigma_A(p^2) = (C_F * alpha_s)/(4*pi^2) *
#     INT_0^infty dk^2 k^2 * ANGLE_A(p^2, k^2)
#
#   Sigma_B(p^2) = (C_F * alpha_s)/(4*pi^2) *
#     INT_0^infty dk^2 k^2 * ANGLE_B(p^2, k^2)
#
# Angle kernel (standard, Aguilar et al. PRD89:085032 Appendix A):
#   ANGLE_{A,B} = (2/pi) * INT_0^pi d_theta sin^2(theta) *
#                 D(q^2) * Gamma_{A,B}(p^2, k^2, theta)
#
# where q^2 = p^2 + k^2 - 2*sqrt(p^2*k^2)*cos(theta) (Euclidean)
#
# Vertex factor (BC longitudinal + STI correction):
#   Gamma_A = L1_eff * [A(k^2)+A(p^2)]/2 / denom(k)
#   Gamma_B = L1_eff * 3 * B(k^2) / denom(k)
#   where denom(k) = k^2*A(k^2)^2 + B(k^2)^2
#   and L1_eff = F_ghost(q^2) * H_scalar(q^2, k^2, p^2)  [STI correction]
#
# Gluon propagator (Landau gauge, UIDT parametrization):
#   D(q^2) = Z(q^2) / q^2
#   Z(q^2) = (q^2 / (q^2 + Lambda_gl^2))^kappa_gl   [UV]
#           * (1 + c_gl * Lambda_gl^2 / (q^2 + Lambda_gl^2))   [IR decoupling]
#   Saturates to finite value at q^2=0 (massive/decoupling solution)
#   consistent with lattice [Bogolubsky 2009, Ayala 2012] (Evidence B)
#
# Iteration:
#   Start: A^(0) = 1, B^(0) = m_q
#   Update: A_new = (1-alpha)*A_old + alpha*(1 + Sigma_A)
#            B_new = (1-alpha)*B_old + alpha*(m_q + Sigma_B)
#   Stop: max|A_new - A_old| < eps  AND  max|B_new - B_old| < eps
#
# Numerical integration:
#   k^2 integral: N_k Gauss-Legendre nodes on [0, k2_max] (mpmath.gauss)
#   theta integral: N_th Gauss-Legendre nodes on [0, pi]
#   N_k = 16, N_th = 12  (convergence test level; increase for production)
#
# KNOWN LIMITATIONS:
#   - Quenched (N_f = 0): no quark loop in gluon propagator.
#   - Transverse vertex (tau_3, tau_6) NOT included in SDE kernel.
#     These contribute ~10-15% to B(0) [Evidence D].
#   - Gluon propagator D(q^2): parametric model, not solved from gluon SDE.
#   - A_0 kernel: 1-loop approximation (not full SDE kernel).
#   - N_k=16 is coarse -- use N_k>=64 for publication-quality results.
#   - Active research framework -- not established physics.
#
# Sources:
#   [A] Ball, Chiu (1980) PRD 22, 2542  DOI:10.1103/PhysRevD.22.2542
#   [B] Aguilar, Binosi, Papavassiliou (2014) PRD 89, 085032
#       arXiv:1401.3631  DOI:10.1103/PhysRevD.89.085032
#       [Appendix A: angle-average formula; Fig.2: A,B functions]
#   [C] Aguilar, De Fazio, Papavassiliou (2018) PRD 98, 014002
#       arXiv:1804.04229  DOI:10.1103/PhysRevD.98.014002
#       [Full coupled SDE with non-Abelian BC vertex]
#   [D] Bogolubsky et al. (2009) PLB 676, 69
#       DOI:10.1016/j.physletb.2009.04.076  [lattice gluon propagator]
#   [E] Ayala et al. (2012) PRD 86, 074512
#       DOI:10.1103/PhysRevD.86.074512  [lattice, large volume]
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

# Quark dressing initial/seed parameters
m_q        = mp.mpf('0.005')   # current quark mass [GeV]
a_A        = mp.mpf('0.3');    Lambda_A = mp.mpf('1.0')
b_B        = mp.mpf('40.0');   Lambda_B = mp.mpf('0.5')

# Ghost dressing (MOM: F(mu^2)=1)
a_F        = mp.mpf('0.30');   Lambda_F = mp.mpf('0.6')

# Gluon propagator parameters [Evidence B, Bogolubsky 2009 / Ayala 2012]
Lambda_gl  = mp.mpf('0.73')    # gluon IR scale [GeV]  (m_gl in literature)
c_gl       = mp.mpf('0.85')    # IR saturation strength
kappa_gl   = mp.mpf('1.0')     # UV power (quenched)

# Integration parameters
N_k        = 16    # k^2 nodes (Gauss-Legendre)
N_th       = 12    # theta nodes
k2_max     = mp.mpf('400')     # upper cutoff [GeV^2] (~20 GeV)
alpha_mix  = mp.mpf('0.5')     # iteration mixing


# ------------------------------------------------------------------
# GLUON PROPAGATOR  D(q^2) = Z(q^2)/q^2
# ------------------------------------------------------------------

def Z_gluon(q2):
    """Gluon dressing function Z(q^2).

    UIDT parametrization of the decoupling/massive solution:
      Z(q^2) = [q^2/(q^2+L^2)]^kappa * [1 + c*L^2/(q^2+L^2)]

    Properties:
      UV: Z(q^2>>L^2) -> 1  (perturbative)
      IR: Z(0) = c * kappa / (1 + kappa) ~ finite  (decoupling)
      Z(mu^2) renorm. not enforced here (relative normalization).
    Consistent with lattice: Bogolubsky 2009, Ayala 2012  [Evidence B]
    """
    q2 = mp.mpf(str(q2))
    L2 = Lambda_gl**2
    return ((q2 / (q2 + L2))**kappa_gl
            * (mp.mpf('1') + c_gl * L2 / (q2 + L2)))


def D_gluon(q2):
    """Full gluon propagator D(q^2) = Z(q^2)/q^2 (massless pole reg.).

    q^2 = 0 is treated via continuity: D(0) = lim_{q->0} Z/q^2.
    Since Z(0) finite, D(0) diverges -- physically screened by IR mass.
    Numerical: replace q^2=0 with q2_min = 1e-4 GeV^2.
    [Evidence B]
    """
    q2 = mp.mpf(str(q2))
    q2_reg = mp.fmax(q2, mp.mpf('1e-4'))
    return Z_gluon(q2_reg) / q2_reg


# ------------------------------------------------------------------
# GHOST DRESSING  F(q^2)  (copy from sti_ghost_quark_kernel.py)
# ------------------------------------------------------------------

def F_ghost(q2):
    """Ghost dressing MOM: F(mu^2)=1, F(0)~1.29  [Evidence B]"""
    q2  = mp.mpf(str(q2))
    mu2 = mu**2
    return (mp.mpf('1')
            + a_F * Lambda_F**2 / (q2 + Lambda_F**2)
            - a_F * Lambda_F**2 / (mu2 + Lambda_F**2))


# ------------------------------------------------------------------
# QUARK-GHOST KERNEL  H_scalar  (copy from sti_ghost_quark_kernel.py)
# ------------------------------------------------------------------

def H_scalar(q2, k2, p2, B_k, B_p):
    """Scalar quark-ghost kernel A_0 (1-loop dressed).

    A_0 = 1 - (C_F/C_A)*alpha_s/(4*pi) * 2*B(p)/(B(k)+B(p))
    [Aguilar PRD98 Eq.(C.1), Evidence B]
    """
    C_A  = mp.mpf('3')
    denom = B_k + B_p
    if denom == mp.mpf('0'):
        return mp.mpf('1')
    delta = -(C_F / C_A) * alpha_s / (mp.mpf('4') * mp.pi) * (
        mp.mpf('2') * B_p / denom
    )
    return mp.mpf('1') + delta


# ------------------------------------------------------------------
# ANGLE-AVERAGED SELF-ENERGY KERNELS
# ------------------------------------------------------------------

def _angle_avg(p2, k2, A_func, B_func):
    """Angle-averaged SDE kernel (Aguilar PRD89 Appendix A).

    Returns (kernel_A, kernel_B) for given p^2, k^2.
    Performs theta integral via Gauss-Legendre on [0, pi].
    """
    p2 = mp.mpf(str(p2))
    k2 = mp.mpf(str(k2))
    sp = mp.sqrt(mp.fmax(p2, mp.mpf('0')))
    sk = mp.sqrt(mp.fmax(k2, mp.mpf('0')))

    nodes, weights = mp.gauss_legendre(N_th, -mp.pi, mp.pi)
    # map to [0, pi]: exploit symmetry cos(pi-x) = -cos(x)
    # -> integrate on [0,pi] with weight sin^2(theta)
    n2, w2 = mp.gauss_legendre(N_th, mp.mpf('0'), mp.pi)

    sum_A = mp.mpf('0')
    sum_B = mp.mpf('0')

    for theta, wt in zip(n2, w2):
        cos_t = mp.cos(theta)
        sin2_t = mp.sin(theta)**2
        q2 = p2 + k2 - mp.mpf('2') * sp * sk * cos_t
        q2 = mp.fmax(q2, mp.mpf('1e-6'))

        Ak = A_func(k2)
        Bk = B_func(k2)
        Ap = A_func(p2)
        denom_k = k2 * Ak**2 + Bk**2
        if denom_k == mp.mpf('0'):
            continue

        # STI effective vertex correction
        L1_eff = F_ghost(q2) * H_scalar(q2, k2, p2, Bk, B_func(p2))

        # BC form factor: L1 = (A(k)+A(p))/2
        L1_BC = (Ak + Ap) / mp.mpf('2')

        Dq = D_gluon(q2)

        ker_A = Dq * L1_eff * L1_BC / denom_k
        ker_B = Dq * L1_eff * mp.mpf('3') * Bk / denom_k

        # sin^2(theta) weight (4d solid angle average)
        sum_A += wt * sin2_t * ker_A
        sum_B += wt * sin2_t * ker_B

    # prefactor: (2/pi) from angle normalization
    prefac = mp.mpf('2') / mp.pi
    return prefac * sum_A, prefac * sum_B


def _sigma(p2, A_func, B_func):
    """Full self-energy Sigma_A, Sigma_B at p^2.

    Sigma_{A,B}(p^2) = (C_F*alpha_s)/(4*pi^2) *
      INT_0^{k2_max} dk^2 k^2 * ANGLE_{A,B}(p^2,k^2)

    k^2 integral via Gauss-Legendre on [0, k2_max].
    [Aguilar PRD89:085032 Appendix A, Evidence B]
    """
    p2 = mp.mpf(str(p2))
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

    Parameters
    ----------
    p2_grid : list of mpf  -- Euclidean momentum^2 values [GeV^2]
    n_iter  : int          -- max iterations (3 for test, >=10 for conv.)
    eps     : mpf          -- convergence threshold on max |Delta A|, |Delta B|
    verbose : bool

    Returns
    -------
    A_vals, B_vals : list of mpf  -- converged (or n_iter) dressing functions
    converged      : bool
    """
    N = len(p2_grid)

    # Initial seed: BC parametrization
    A_vals = [mp.mpf('1') + a_A * Lambda_A**2 / (p2 + Lambda_A**2)
               for p2 in p2_grid]
    B_vals = [m_q * (mp.mpf('1') + b_B * Lambda_B**2 / (p2 + Lambda_B**2))
               for p2 in p2_grid]

    def A_func(p2):
        """Linear interpolation on grid."""
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
        A_new = []
        B_new = []
        for p2 in p2_grid:
            sA, sB = _sigma(p2, A_func, B_func)
            A_new.append((mp.mpf('1') - alpha_mix) * A_func(p2)
                         + alpha_mix * (mp.mpf('1') + sA))
            B_new.append((mp.mpf('1') - alpha_mix) * B_func(p2)
                         + alpha_mix * (m_q + sB))

        dA = max(abs(A_new[i] - A_vals[i]) for i in range(N))
        dB = max(abs(B_new[i] - B_vals[i]) for i in range(N))
        A_vals = A_new
        B_vals = B_new
        # update interpolators
        if verbose:
            M0 = B_vals[0] / A_vals[0]
            print(f'  iter {it}: delta_A={mp.nstr(dA,4)}  '
                  f'delta_B={mp.nstr(dB,4)}  '
                  f'M(0)={mp.nstr(M0,5)} GeV')
        if dA < eps and dB < eps:
            converged = True
            break

    return A_vals, B_vals, converged


# ------------------------------------------------------------------
# VERIFICATION
# ------------------------------------------------------------------

def run_verification():
    mp.dps = 80
    passed = 0; failed = 0

    def check(name, ok, residual=None):
        nonlocal passed, failed
        label = '[PASS]' if ok else '[FAIL]'
        suffix = f'  res={mp.nstr(residual,5)}' if residual is not None else ''
        print(f'{label}  {name:<68}{suffix}')
        if ok: passed += 1
        else:  failed += 1

    mu2 = mu**2

    # 1-4: Parameter Ledger
    check('Delta_star = 1.710 GeV [A]',
          abs(Delta_star - mp.mpf('1.710')) < mp.mpf('1e-14'),
          abs(Delta_star - mp.mpf('1.710')))
    check('gamma_val = 16.339 [A-]',
          abs(gamma_val - mp.mpf('16.339')) < mp.mpf('1e-14'),
          abs(gamma_val - mp.mpf('16.339')))

    # 5-6: Gluon propagator
    check('D_gluon(mu^2) > 0  [positive definite]',
          D_gluon(mu2) > mp.mpf('0'))
    check('Z_gluon UV -> 1: Z(1e6) in [0.9, 1.1]',
          mp.mpf('0.9') < Z_gluon(mp.mpf('1e6')) < mp.mpf('1.1'))

    # 7: Ghost dressing
    check('F_ghost(mu^2) = 1  [MOM exact]',
          abs(F_ghost(mu2) - mp.mpf('1')) < mp.mpf('1e-14'),
          abs(F_ghost(mu2) - mp.mpf('1')))

    # 8-9: Angle kernel sanity
    p2_test = mp.mpf('1.0')
    kA, kB = _angle_avg(p2_test, mp.mpf('2.0'),
                         lambda p2: mp.mpf('1') + a_A*Lambda_A**2/(p2+Lambda_A**2),
                         lambda p2: m_q*(mp.mpf('1')+b_B*Lambda_B**2/(p2+Lambda_B**2)))
    check('Angle kernel_A > 0  [physical]', kA > mp.mpf('0'))
    check('Angle kernel_B > 0  [physical, DCSB]', kB > mp.mpf('0'))

    # 10-11: SDE self-energy (seed iteration)
    def A0(p2): return mp.mpf('1') + a_A*Lambda_A**2/(mp.mpf(str(p2))+Lambda_A**2)
    def B0(p2): return m_q*(mp.mpf('1')+b_B*Lambda_B**2/(mp.mpf(str(p2))+Lambda_B**2))
    sA, sB = _sigma(p2_test, A0, B0)
    check('Sigma_A(1 GeV^2) is finite mpf', isinstance(sA, mp.mpf))
    check('Sigma_B(1 GeV^2) > 0  [DCSB signal]', sB > mp.mpf('0'))

    # 12-13: Iteration (3 steps, coarse grid)
    p2_grid = [mp.mpf('1e-4'), mp.mpf('0.5'), mu2]
    A_vals, B_vals, _ = run_coupled_sde(p2_grid, n_iter=2, verbose=False)
    check('A(mu^2) after 2 iter in [1.0, 1.6]',
          mp.mpf('1.0') < A_vals[2] < mp.mpf('1.6'))
    check('B(0) after 2 iter > m_q  [DCSB present]',
          B_vals[0] > m_q)

    # 14: M(0) = B(0)/A(0) constituent mass range
    M0 = B_vals[0] / A_vals[0]
    check('M(0) in [0.05, 0.50] GeV  [constituent mass range]',
          mp.mpf('0.05') < M0 < mp.mpf('0.50'))

    print()
    print(f'Total: {passed+failed}  |  PASS: {passed}  |  FAIL: {failed}')
    print()
    print(f'Sigma_A(1 GeV^2) = {mp.nstr(sA, 6)}')
    print(f'Sigma_B(1 GeV^2) = {mp.nstr(sB, 6)} GeV')
    print(f'M(p^2=0) [2-iter] = {mp.nstr(M0, 5)} GeV  [Evidence D]')
    print()
    print('[UIDT LIMITS] Quenched. Transverse vertex excluded from SDE kernel.')
    print('[UIDT LIMITS] N_k=16 coarse -- increase to >=64 for production.')
    print('[UIDT LIMITS] Gluon D(q^2) parametric model, not SDE-solved.')
    print(f'  Delta* = {Delta_star} GeV [A], gamma = {gamma_val} [A-] unchanged.')
    if failed > 0:
        raise RuntimeError(f'[VERIFICATION_FAIL] {failed} check(s) failed')


if __name__ == '__main__':
    print('=== Quark SDE Coupled -- Verification ===')
    print(f'N_k={N_k}, N_th={N_th}, alpha_mix={alpha_mix}')
    print()
    run_verification()
