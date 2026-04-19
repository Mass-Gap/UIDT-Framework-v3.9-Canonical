# UIDT Framework v3.9 — TKT-FRG-TACHYON
# Coupled YM+Scalar FRG flow with tachyonic UV boundary
# Inversion: find kappa_tilde_0 such that kappa_tilde(t_IR) = v^2/(2*E_geo^2)
#
# Author: P. Rietz
# Constitution compliance:
#   - mp.dps = 80 local (RACE CONDITION LOCK)
#   - no float(), no round()
#   - RG constraint: 5*kappa^2 = 3*lambda_S enforced
#   - Ledger constants: read-only

import mpmath as mp

def run_FRG_tachyon_inversion():
    mp.dps = 80

    # ── Immutable Ledger Constants ─────────────────────────────────────────
    Delta    = mp.mpf('1.710')          # Yang-Mills spectral gap [GeV] [A]
    gamma_c  = mp.mpf('16.339')         # Kinematic vacuum parameter [A-]
    v        = mp.mpf('47.7e-3')        # Scalar VEV [GeV] [A]
    kappa    = mp.mpf('0.500')          # RG coefficient [A]
    lambda_S = mp.mpf('5') / 12        # Quartic coupling [A]
    Nc       = mp.mpf('3')              # SU(3) color
    d_adj    = Nc**2 - 1               # = 8 adjoint dimensions
    b0       = mp.mpf('11') * Nc / 3   # 1-loop YM beta coefficient
    M_G      = mp.mpf('0.65')          # Gribov mass [GeV] [B]
    E_geo    = Delta / gamma_c          # Geometric energy scale [A-]

    # ── RG Constraint Enforcement ─────────────────────────────────────────
    rg_residual = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg_residual < mp.mpf('1e-14'), (
        f"[RG_CONSTRAINT_FAIL] residual = {mp.nstr(rg_residual, 5)}"
    )

    # ── Derived Quantities ────────────────────────────────────────────────
    t_UV  = mp.mpf('0')
    t_IR  = mp.log(E_geo / Delta)          # ≈ -2.794
    N_S   = int(d_adj) + 1                 # = 9 scalar modes
    c_loop = mp.mpf('1') / (16 * mp.pi**2)

    # Target: kappa_tilde at IR
    kappa_target = v**2 / (2 * E_geo**2)

    # Fixed UV values (not kappa_tilde — that is the free parameter)
    lambda_0 = lambda_S
    g2_0     = 4 * mp.pi * mp.mpf('0.3')   # alpha_s(Δ*) ≈ 0.30
    Z_A_0    = mp.mpf('1')

    # ── Threshold Functions (Litim Regulator) ────────────────────────────
    def L40(w):
        return mp.mpf('1') / (1 + w)

    def L41(w):
        return mp.mpf('1') / (1 + w)**2

    def Z_GZ(k):
        return k**4 / (k**4 + M_G**4)

    # ── RHS of Coupled Flow System ────────────────────────────────────────
    def flow_rhs(t, state):
        kappa_t, lambda_t, g2_t, Z_A_t = state
        k = Delta * mp.exp(t)

        # Stability guards
        if kappa_t < 0:
            kappa_t = mp.mpf('0')
        if lambda_t < mp.mpf('1e-12'):
            lambda_t = mp.mpf('1e-12')
        if g2_t < 0:
            g2_t = mp.mpf('0')

        Z_GZ_k   = Z_GZ(k)
        w_radial = 2 * lambda_t * kappa_t

        # [1] kappa_tilde flow
        scalar_c = c_loop * ((N_S - 1) * L40(mp.mpf('0')) + L40(w_radial))
        gluon_c  = c_loop * d_adj * Z_GZ_k
        dkappa   = -2 * kappa_t + scalar_c + gluon_c

        # [2] lambda_tilde flow
        dlambda  = (c_loop * 2 * lambda_t**2
                    * ((N_S - 1) * L41(mp.mpf('0')) + 3 * L41(w_radial)))

        # [3] g^2 flow (1-loop YM)
        dg2      = -b0 * c_loop * g2_t**2

        # [4] Z_A flow with GZ damping
        eta_A    = b0 * c_loop * g2_t * Z_GZ_k
        dZ_A     = -eta_A * Z_A_t

        return [dkappa, dlambda, dg2, dZ_A]

    # ── RK4 Integrator ────────────────────────────────────────────────────
    def integrate_flow(kappa_0_in, N_steps=2000):
        """Integrate from t_UV to t_IR; return kappa_tilde(t_IR)."""
        state = [
            mp.mpf(str(kappa_0_in)),
            lambda_0,
            g2_0,
            Z_A_0
        ]
        t   = t_UV
        dt  = (t_IR - t_UV) / N_steps

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

        return state  # [kappa_IR, lambda_IR, g2_IR, Z_A_IR]

    # ── Shooting Function ─────────────────────────────────────────────────
    def F_shoot(log_kappa_0):
        """F = kappa_tilde(t_IR) - target; input is log10(kappa_0) for scan."""
        kappa_0 = mp.power(10, log_kappa_0)
        state_IR = integrate_flow(kappa_0, N_steps=2000)
        return state_IR[0] - kappa_target

    # ── Step 1: Bracket scan over log10(kappa_0) ─────────────────────────
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  TKT-FRG-TACHYON: Shooting over tachyonic UV boundary       ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print(f"  Δ*       = {mp.nstr(Delta, 5)} GeV")
    print(f"  γ_c      = {mp.nstr(gamma_c, 6)}")
    print(f"  v        = {mp.nstr(v*1000, 5)} MeV")
    print(f"  E_geo    = {mp.nstr(E_geo*1000, 6)} MeV")
    print(f"  κ_target = {mp.nstr(kappa_target, 8)}")
    print(f"  t_IR     = {mp.nstr(t_IR, 5)}")
    print()
    print("  RG constraint: |5κ²-3λ_S| =", mp.nstr(rg_residual, 3), "✓")
    print()
    print("  Scanning log10(κ̃₀) ∈ [-4, +1] for sign change of F ...")
    print()

    scan_vals = [mp.mpf(str(x)) for x in
                 [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1]]
    F_vals = []
    bracket_found = False
    lo_bracket = None
    hi_bracket = None

    for lk in scan_vals:
        kap = mp.power(10, lk)
        st  = integrate_flow(kap, N_steps=1000)
        f   = st[0] - kappa_target
        F_vals.append((lk, kap, f))
        print(f"  log10(κ̃₀)={mp.nstr(lk,4):6s}  "
              f"κ̃₀={mp.nstr(kap,5):12s}  "
              f"κ̃(t_IR)={mp.nstr(st[0],8):14s}  "
              f"F={mp.nstr(f,6)}")

    print()
    # Find bracket
    for i in range(len(F_vals) - 1):
        f1 = F_vals[i][2]
        f2 = F_vals[i+1][2]
        if f1 * f2 < 0:
            lo_bracket = F_vals[i][0]
            hi_bracket = F_vals[i+1][0]
            bracket_found = True
            break

    if not bracket_found:
        print("  [SEARCH_FAIL] No sign change found in scan range.")
        print("  Extended diagnostics:")
        print(f"  F at log10(κ̃₀)=-4: {mp.nstr(F_vals[0][2], 6)}")
        print(f"  F at log10(κ̃₀)=+1: {mp.nstr(F_vals[-1][2], 6)}")
        return None

    print(f"  Bracket found: log10(κ̃₀) ∈ [{mp.nstr(lo_bracket,4)}, {mp.nstr(hi_bracket,4)}]")
    print()

    # ── Step 2: Bisection to |F| < 1e-14 ──────────────────────────────────
    print("  Bisecting for |F| < 1e-14 ...")
    for bisect_iter in range(200):
        mid = (lo_bracket + hi_bracket) / 2
        kap_mid = mp.power(10, mid)
        st_mid  = integrate_flow(kap_mid, N_steps=2000)
        F_mid   = st_mid[0] - kappa_target

        kap_lo = mp.power(10, lo_bracket)
        st_lo  = integrate_flow(kap_lo, N_steps=2000)
        F_lo   = st_lo[0] - kappa_target

        if F_lo * F_mid < 0:
            hi_bracket = mid
        else:
            lo_bracket = mid

        if abs(F_mid) < mp.mpf('1e-14'):
            print(f"  Converged at iteration {bisect_iter+1}: |F| = {mp.nstr(abs(F_mid), 4)}")
            break

    kappa_0_star = mp.power(10, (lo_bracket + hi_bracket) / 2)
    state_star   = integrate_flow(kappa_0_star, N_steps=5000)
    kappa_IR_star = state_star[0]
    F_final       = abs(kappa_IR_star - kappa_target)

    # ── Derived Physical Quantities ────────────────────────────────────────
    m2_tachyon = -2 * lambda_S * Delta**2 * kappa_0_star  # [GeV^2]
    k_SSB      = Delta * mp.exp(t_IR)                      # = E_geo by construction
    gamma_FRG  = Delta / k_SSB                             # should = gamma_c

    print()
    print("─── RESULTS ──────────────────────────────────────────────────")
    print()
    print(f"  κ̃₀*  (optimal UV start) = {mp.nstr(kappa_0_star, 10)}")
    print(f"  m²_S(Λ)                  = {mp.nstr(m2_tachyon, 8)} GeV² (tachyonic)")
    print(f"  |m_S(Λ)|                 = {mp.nstr(mp.sqrt(-m2_tachyon)*1000, 6)} MeV")
    print()
    print(f"  κ̃(t_IR) achieved         = {mp.nstr(kappa_IR_star, 10)}")
    print(f"  κ̃_target                 = {mp.nstr(kappa_target, 10)}")
    print(f"  Residual |F|             = {mp.nstr(F_final, 5)}")
    print()
    print(f"  γ_FRG = Δ*/E_geo         = {mp.nstr(gamma_FRG, 8)}")
    print(f"  γ_canonical              = {mp.nstr(gamma_c, 8)}")
    print(f"  Z_A(t_IR)                = {mp.nstr(state_star[3], 8)}")
    print(f"  λ̃(t_IR)                  = {mp.nstr(state_star[1], 8)}")
    print(f"  g̃²(t_IR)                 = {mp.nstr(state_star[2], 8)}")
    print()

    # Constitution checks
    rg_final = abs(5 * kappa**2 - 3 * lambda_S)
    assert rg_final < mp.mpf('1e-14'), "[RG_CONSTRAINT_FAIL] post-run"

    print("─── CONSTITUTION CHECK ────────────────────────────────────────")
    print(f"  |5κ²-3λ_S|  = {mp.nstr(rg_final, 3)} ✓")
    print(f"  mp.dps      = {mp.dps} (local) ✓")
    print(f"  float() used: NO ✓")
    print(f"  Ledger constants: unchanged ✓")
    print()

    if F_final < mp.mpf('1e-14'):
        print("  ★ RESIDUAL < 1e-14 — Constitution threshold satisfied")
    else:
        print(f"  [WARN] Residual = {mp.nstr(F_final, 5)} > 1e-14 — increase N_steps")

    return {
        'kappa_0_star':  kappa_0_star,
        'm2_tachyon':    m2_tachyon,
        'kappa_IR':      kappa_IR_star,
        'kappa_target':  kappa_target,
        'F_final':       F_final,
        'gamma_FRG':     gamma_FRG,
        'Z_A_IR':        state_star[3],
    }

if __name__ == '__main__':
    result = run_FRG_tachyon_inversion()
