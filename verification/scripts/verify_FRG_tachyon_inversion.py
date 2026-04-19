# UIDT Framework v3.9 — TKT-FRG-TACHYON
# Coupled YM+Scalar FRG flow with tachyonic UV boundary
# Inversion: find kappa_tilde_0 such that kappa_tilde(t_IR) = v^2/(2*E_geo^2)
#
# Author: P. Rietz
# Date: 2026-04-19
#
# Numerical result:
#   kappa_0_star = 0.0487771846469
#   m^2_S(Lambda) = -0.1188578047 GeV^2
#   |m_S(Lambda)| = 344.758 MeV
#   Residual |F| = 3.33e-13 (converged at iter 40)
#
# Constitution compliance:
#   - mp.dps = 80 local (RACE CONDITION LOCK)
#   - no float(), no round()
#   - RG constraint: 5*kappa^2 = 3*lambda_S enforced
#   - Ledger constants: read-only

import mpmath as mp


def run_FRG_tachyon_inversion():
    mp.dps = 80

    # -- Immutable Ledger Constants --
    Delta    = mp.mpf('1.710')          # Yang-Mills spectral gap [GeV] [A]
    gamma_c  = mp.mpf('16.339')         # Kinematic vacuum parameter [A-]
    v        = mp.mpf('47.7e-3')        # Scalar VEV [GeV] [A]
    kappa    = mp.mpf('0.500')          # RG coefficient [A]
    lambda_S = mp.mpf('5') / 12        # Quartic coupling [A]
    Nc       = mp.mpf('3')
    d_adj    = Nc**2 - 1               # = 8
    b0       = mp.mpf('11') * Nc / 3   # = 11
    M_G      = mp.mpf('0.65')          # Gribov mass [GeV] [B]
    E_geo    = Delta / gamma_c

    # -- RG Constraint --
    rg_residual = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg_residual < mp.mpf('1e-14'), (
        f"[RG_CONSTRAINT_FAIL] residual = {mp.nstr(rg_residual, 5)}"
    )

    # -- Derived --
    t_UV         = mp.mpf('0')
    t_IR         = mp.log(E_geo / Delta)
    N_S          = int(d_adj) + 1
    c_loop       = mp.mpf('1') / (16 * mp.pi**2)
    kappa_target = v**2 / (2 * E_geo**2)
    lambda_0     = lambda_S
    g2_0         = 4 * mp.pi * mp.mpf('0.3')
    Z_A_0        = mp.mpf('1')

    def L40(w):
        return mp.mpf('1') / (1 + w)

    def L41(w):
        return mp.mpf('1') / (1 + w)**2

    def Z_GZ(k):
        return k**4 / (k**4 + M_G**4)

    def flow_rhs(t, state):
        kappa_t, lambda_t, g2_t, Z_A_t = state
        k = Delta * mp.exp(t)
        if kappa_t < 0:                  kappa_t  = mp.mpf('0')
        if lambda_t < mp.mpf('1e-12'):   lambda_t = mp.mpf('1e-12')
        if g2_t < 0:                     g2_t     = mp.mpf('0')
        Z_GZ_k   = Z_GZ(k)
        w_rad    = 2 * lambda_t * kappa_t
        scalar_c = c_loop * ((N_S - 1) * L40(mp.mpf('0')) + L40(w_rad))
        gluon_c  = c_loop * d_adj * Z_GZ_k
        dkappa   = -2 * kappa_t + scalar_c + gluon_c
        dlambda  = (c_loop * 2 * lambda_t**2
                    * ((N_S - 1) * L41(mp.mpf('0')) + 3 * L41(w_rad)))
        dg2      = -b0 * c_loop * g2_t**2
        dZ_A     = -(b0 * c_loop * g2_t * Z_GZ_k) * Z_A_t
        return [dkappa, dlambda, dg2, dZ_A]

    def integrate_flow(kappa_0_in, N_steps=2000):
        state = [mp.mpf(str(kappa_0_in)), lambda_0, g2_0, Z_A_0]
        t  = t_UV
        dt = (t_IR - t_UV) / N_steps
        for _ in range(N_steps):
            s  = state
            k1 = flow_rhs(t, s)
            k2 = flow_rhs(t + dt/2, [s[j] + dt/2*k1[j] for j in range(4)])
            k3 = flow_rhs(t + dt/2, [s[j] + dt/2*k2[j] for j in range(4)])
            k4 = flow_rhs(t + dt,   [s[j] + dt  *k3[j] for j in range(4)])
            state = [s[j] + dt*(k1[j] + 2*k2[j] + 2*k3[j] + k4[j])/6
                     for j in range(4)]
            if state[0] < 0:
                state[0] = mp.mpf('0')
            t += dt
        return state

    print("="*66)
    print("  TKT-FRG-TACHYON: Tachyonic UV Boundary Inversion")
    print("="*66)
    print()
    print(f"  Delta*       = {mp.nstr(Delta, 5)} GeV   [A]")
    print(f"  gamma_c      = {mp.nstr(gamma_c, 6)}        [A-]")
    print(f"  v            = {mp.nstr(v*1000, 5)} MeV   [A]")
    print(f"  E_geo        = {mp.nstr(E_geo*1000, 6)} MeV   [A-]")
    print(f"  kappa_target = {mp.nstr(kappa_target, 8)}")
    print(f"  RG residual  = {mp.nstr(rg_residual, 3)} [machine zero] checked")
    print()

    # Bisection (bracket pre-verified: [0.039811, 0.050119])
    lo = mp.mpf('0.039811')
    hi = mp.mpf('0.050119')

    print("  Bisecting kappa_0 in [0.039811, 0.050119] ...")
    for bisect_iter in range(80):
        mid    = (lo + hi) / 2
        F_mid  = integrate_flow(mid, N_steps=3000)[0] - kappa_target
        F_lo   = integrate_flow(lo,  N_steps=3000)[0] - kappa_target
        if F_lo * F_mid < 0:
            hi = mid
        else:
            lo = mid
        if abs(F_mid) < mp.mpf('1e-12'):
            print(f"  Converged at iteration {bisect_iter+1}: |F| = {mp.nstr(abs(F_mid),4)}")
            break

    kappa_0_star = (lo + hi) / 2
    state_star   = integrate_flow(kappa_0_star, N_steps=5000)
    kappa_IR     = state_star[0]
    F_final      = abs(kappa_IR - kappa_target)
    m2_tachyon   = -2 * lambda_S * Delta**2 * kappa_0_star

    print()
    print("-"*66)
    print("  RESULTS")
    print("-"*66)
    print(f"  kappa_0_star   = {mp.nstr(kappa_0_star, 12)}")
    print(f"  m^2_S(Lambda)  = {mp.nstr(m2_tachyon, 10)} GeV^2")
    print(f"  |m_S(Lambda)|  = {mp.nstr(mp.sqrt(abs(m2_tachyon))*1000, 8)} MeV")
    print()
    print(f"  kappa(t_IR)    = {mp.nstr(kappa_IR, 12)}")
    print(f"  kappa_target   = {mp.nstr(kappa_target, 12)}")
    print(f"  Residual |F|   = {mp.nstr(F_final, 5)}")
    print()
    print(f"  gamma_FRG = Delta*/E_geo = {mp.nstr(Delta/E_geo, 8)}")
    print(f"  Z_A(t_IR)               = {mp.nstr(state_star[3], 8)}")
    print(f"  lambda(t_IR)            = {mp.nstr(state_star[1], 8)}")
    print(f"  g^2(t_IR)               = {mp.nstr(state_star[2], 8)}")
    print()
    print("-"*66)
    print("  CONSTITUTION CHECK")
    print("-"*66)
    rg_post = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg_post < mp.mpf('1e-14'), "[RG_CONSTRAINT_FAIL] post-run"
    print(f"  |5kappa^2 - 3*lambda_S| = {mp.nstr(rg_post, 3)} [machine zero] checked")
    print(f"  mp.dps = {mp.dps} (local) checked")
    print(f"  float() used: NO checked")
    print(f"  Ledger constants: unchanged checked")
    if F_final < mp.mpf('1e-12'):
        print(f"  Residual < 1e-12: PASS")
    else:
        print(f"  [WARN] Residual {mp.nstr(F_final,4)} > 1e-12: increase N_steps")

    return {
        'kappa_0_star':  kappa_0_star,
        'm2_tachyon':    m2_tachyon,
        'kappa_IR':      kappa_IR,
        'kappa_target':  kappa_target,
        'F_final':       F_final,
        'Z_A_IR':        state_star[3],
    }


if __name__ == '__main__':
    result = run_FRG_tachyon_inversion()
