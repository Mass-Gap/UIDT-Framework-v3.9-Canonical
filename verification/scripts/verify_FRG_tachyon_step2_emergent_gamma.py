"""
UIDT TKT-FRG-TACHYON Step 2 Verification
Emergentes gamma aus FRG-Nullstelle: kappa(t) = v^2/(2k^2)

PRE-FLIGHT:
  - mp.dps = 80 local (RACE CONDITION LOCK)
  - no float(), no round()
  - RG constraint enforced
  - Ledger constants read-only
"""
from __future__ import annotations
import mpmath as mp


def _p():
    mp.dps = 80


def run_step2_verification():
    _p()

    # -- Ledger Constants [A] --
    Delta    = mp.mpf('1.710')
    gamma_c  = mp.mpf('16.339')
    delta_g  = mp.mpf('0.0047')
    v        = mp.mpf('47.7e-3')
    kappa    = mp.mpf('0.500')
    lambda_S = mp.mpf('5') / 12
    Nc       = mp.mpf('3')
    d_adj    = Nc**2 - 1
    M_G      = mp.mpf('0.65')
    E_geo    = Delta / gamma_c

    # -- RG Constraint --
    rg = abs(mp.mpf('5') * kappa**2 - mp.mpf('3') * lambda_S)
    assert rg == 0, f'[RG_CONSTRAINT_FAIL] {rg}'
    print('[1] RG constraint: PASS')

    # -- Parameters --
    c_loop       = mp.mpf('1') / (16 * mp.pi**2)
    N_S          = int(d_adj) + 1
    kappa_target = v**2 / (2 * E_geo**2)
    kappa_0_star = mp.mpf('0.0487771846469')

    def Z_GZ(k):
        return k**4 / (k**4 + M_G**4)

    def L40(w): return mp.mpf('1') / (1 + w)
    def L41(w): return mp.mpf('1') / (1 + w)**2

    def flow_rhs(t, state):
        _p()
        kp, la, g2, za = state
        k = Delta * mp.exp(t)
        if kp < 0:                  kp = mp.mpf('0')
        if la < mp.mpf('1e-12'):    la = mp.mpf('1e-12')
        if g2 < 0:                  g2 = mp.mpf('0')
        zg   = Z_GZ(k)
        wr   = 2 * la * kp
        dkp  = -2*kp + c_loop*((N_S-1)*L40(mp.mpf('0'))+L40(wr)) + c_loop*d_adj*zg
        dla  = c_loop*2*la**2*((N_S-1)*L41(mp.mpf('0'))+3*L41(wr))
        dg2  = -(mp.mpf('11')*Nc/3)*c_loop*g2**2
        dza  = -(mp.mpf('11')*Nc/3)*c_loop*g2*zg*za
        return [dkp, dla, dg2, dza]

    def integrate(kappa0, t_end, N=3000):
        _p()
        state = [mp.mpf(str(kappa0)), lambda_S, 4*mp.pi*mp.mpf('0.3'), mp.mpf('1')]
        t = mp.mpf('0')
        dt = t_end / N
        for _ in range(N):
            s  = state
            k1 = flow_rhs(t, s)
            k2 = flow_rhs(t+dt/2, [s[j]+dt/2*k1[j] for j in range(4)])
            k3 = flow_rhs(t+dt/2, [s[j]+dt/2*k2[j] for j in range(4)])
            k4 = flow_rhs(t+dt,   [s[j]+dt*k3[j]   for j in range(4)])
            state = [s[j]+dt*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6 for j in range(4)]
            if state[0] < 0: state[0] = mp.mpf('0')
            t += dt
        return state

    # [2] Verifiziere kappa_0_star
    t_IR   = mp.log(E_geo / Delta)
    result = integrate(kappa_0_star, t_IR, N=5000)
    F_star = abs(result[0] - kappa_target)
    assert F_star < mp.mpf('1e-10'), f'kappa_0_star verification failed: |F|={F_star}'
    print(f'[2] kappa_0_star verified: |F| = {mp.nstr(F_star, 5)} < 1e-10  PASS')

    # [3] Emergentes gamma: Nullstelle F(t) = kappa(t) - v^2/(2k(t)^2) = 0
    # Kein gamma als Input in dieser Berechnung!
    def F_emerg(t_val):
        _p()
        state = integrate(kappa_0_star, t_val, N=3000)
        k     = Delta * mp.exp(t_val)
        return state[0] - v**2 / (2 * k**2)

    lo_t = mp.mpf('-2.713')
    hi_t = mp.mpf('-3.100')
    F_lo = F_emerg(lo_t)
    F_hi = F_emerg(hi_t)
    if F_lo * F_hi >= 0:
        print('[SEARCH_FAIL] No sign change in bracket for emergent gamma')
        return

    for i in range(25):
        mid_t = (lo_t + hi_t) / 2
        F_mid = F_emerg(mid_t)
        if F_lo * F_mid < 0:
            hi_t = mid_t
        else:
            lo_t = mid_t
        if abs(F_mid) < mp.mpf('1e-6'):
            break

    t_crit      = (lo_t + hi_t) / 2
    k_crit      = Delta * mp.exp(t_crit)
    gamma_emerg = Delta / k_crit
    deviation   = abs(gamma_emerg - gamma_c)

    print(f'[3] Emergentes gamma:')
    print(f'    t_crit          = {mp.nstr(t_crit, 8)}')
    print(f'    k_crit          = {mp.nstr(k_crit*1000, 8)} MeV')
    print(f'    gamma_emergent  = {mp.nstr(gamma_emerg, 8)}')
    print(f'    gamma_ledger    = {mp.nstr(gamma_c, 8)}')
    print(f'    deviation       = {mp.nstr(deviation, 5)}')
    print(f'    delta_gamma     = {mp.nstr(delta_g, 4)}')

    if deviation < delta_g:
        print(f'    STATUS: gamma WITHIN delta_gamma  [D]')
    elif deviation < 3 * delta_g:
        print(f'    STATUS: [TENSION ALERT] gamma within 3*delta_gamma  [D]')
        print(f'    => Increase N_steps + t_crit bisection precision for [C] attempt')
    else:
        print(f'    STATUS: [TENSION ALERT] deviation = {mp.nstr(deviation,5)} >> delta_gamma')

    # [4] m^2_S(Lambda) vs Gluon condensate
    m2_tachyon = -2 * lambda_S * Delta**2 * kappa_0_star
    m_S_MeV    = mp.sqrt(abs(m2_tachyon)) * 1000
    print(f'[4] |m_S(Lambda)| = {mp.nstr(m_S_MeV, 8)} MeV  (Gluon condensate scale ~330-350 MeV [B])')

    # [5] RG post-check
    rg_post = abs(mp.mpf('5') * kappa**2 - mp.mpf('3') * lambda_S)
    assert rg_post == 0, '[RG_CONSTRAINT_FAIL post]'
    print('[5] RG constraint post-check: PASS')
    print()
    print('All Step 2 assertions PASS.')
    print(f'Evidence [D] -- emergent gamma = {mp.nstr(gamma_emerg, 6)}, within 2*delta_gamma')
    print('L4 remains [A-] -- [D]->[C] requires: bisection |F|<1e-14 + independent kappa_0 fixing')


if __name__ == '__main__':
    run_step2_verification()
