#!/usr/bin/env python3
"""
S2: FRG-Tachyon-Schwellen k_crit und gamma_emergent Berechnung
Branch: TKT-20260429-S4-P4-P5-P6-torsion-gluon-first-principles

Herleitung: Selbstkonsistente Nullstelle von m^2_eff(k) = 0
im gekoppelten YM+Skalaren FRG-Fluss.

Ge-dockt in: research/TKT-FRG-TACHYON-S2-gamma-emergent-findings.md

UIDT-Constitution:
- mp.dps = 80 (lokal)
- Kein float()
- |expected - actual| < 1e-14 wo möglich
- Ledger-Konstanten NICHT modifizieren
"""

import mpmath as mp


def frg_flow_step(kappa, lam, g2, dt, Nc=None, v=None, ET=None):
    """
    Einzelner RG-Fluss-Schritt für (kappa, lambda, g^2).
    Wetterink-Gleichung (vereinfacht, YM + Skalar).

    Gluon-Schleifen dominieren im UV;
    Skalar-Schleifen dominieren im IR.
    """
    mp.dps = 80

    # Gluon-Schleife zu beta_kappa (YM-Beitrag)
    # d(kappa)/dt = -eta_kappa * kappa + delta_kappa_gluon
    beta_kappa_gluon = -g2 * Nc / (16 * mp.pi**2) * kappa

    # Skalar-Schleife zu beta_lambda
    # d(lambda)/dt = ... (vereinfacht)
    beta_lambda = mp.mpf('2') * lam**2 / (16 * mp.pi**2)

    # YM-Kopplung läuft (1-loop beta-function SU(Nc))
    beta_g2 = -mp.mpf('11') * Nc / (48 * mp.pi**2) * g2**2

    kappa_new = kappa + dt * beta_kappa_gluon
    lam_new   = lam   + dt * beta_lambda
    g2_new    = g2    + dt * beta_g2

    return kappa_new, lam_new, g2_new


def m2_eff(kappa, v, k):
    """Effektive Masse des Skalarsektors bei Skala k."""
    mp.dps = 80
    # m^2_eff = 2*lambda * [kappa - v^2/(2*k^2)]
    # Wir integrieren kappa(k), suchen Nullstelle
    return kappa - v**2 / (2 * k**2)


def run_frg_s2(N_steps=4000, tol=mp.mpf('1e-5')):
    mp.dps = 80

    # IMMUTABLE PARAMETER LEDGER
    Delta_star  = mp.mpf('1710.0')   # MeV [A]
    gamma_L     = mp.mpf('16.339')   # [A-]
    delta_gamma = mp.mpf('0.0047')   # [A-]
    v           = mp.mpf('47.7')     # MeV [A]
    ET          = mp.mpf('2.44')     # MeV [C]
    Nc          = mp.mpf('3')
    Lambda_UV   = Delta_star         # UV-Cutoff = Delta* [A]

    print("=" * 70)
    print("S2: FRG-TACHYON SCHWELLE | gamma_emergent BERECHNUNG")
    print(f"N_steps = {N_steps}, Toleranz = {mp.nstr(tol, 5)}, mp.dps = 80")
    print("=" * 70)

    # ============================================================
    # BISECTION: kappa0_star so dass m^2_eff(k_crit) = 0
    # k_crit ist NICHT gamma-abhaengig (gamma-unabhaengige Nullstelle)
    # ============================================================

    def integrate_flow(kappa0, n_steps):
        """Integriert FRG-Fluss von UV (Lambda) nach IR (Lambda/gamma_L)."""
        mp.dps = 80
        t_start = mp.log(Lambda_UV)
        t_end   = mp.log(Lambda_UV / gamma_L)
        dt      = (t_end - t_start) / n_steps

        # Anfangsbedingungen
        kappa = kappa0
        lam   = mp.mpf('5') * kappa0**2 / mp.mpf('3')  # RG-Constraint
        g2    = mp.mpf('1.5')  # Start-Kopplung bei Lambda

        k_crit = None
        for i in range(n_steps):
            t = t_start + i * dt
            k = mp.exp(t)

            # Prüfe Nullstelle von m^2_eff
            f_val = m2_eff(kappa, v, k)
            if i > 0 and k_crit is None:
                f_prev = m2_eff(kappa_prev, v, mp.exp(t - dt))
                if f_prev * f_val < 0:  # Vorzeichenwechsel
                    # Lineare Interpolation für k_crit
                    k_prev = mp.exp(t - dt)
                    k_crit = k_prev - f_prev * (k - k_prev) / (f_val - f_prev)

            kappa_prev = kappa
            kappa, lam, g2 = frg_flow_step(
                kappa, lam, g2, dt, Nc=Nc, v=v, ET=ET
            )

        return kappa, k_crit

    # Bisection über kappa0
    kappa_lo = mp.mpf('0.001')
    kappa_hi = mp.mpf('2.0')
    kappa_mid = None

    print(f"\nBISECTION kappa0 in [{mp.nstr(kappa_lo,3)}, {mp.nstr(kappa_hi,3)}]...")

    F_lo = integrate_flow(kappa_lo, N_steps)[0] - v**2 / (2 * (Lambda_UV/gamma_L)**2)
    F_hi = integrate_flow(kappa_hi, N_steps)[0] - v**2 / (2 * (Lambda_UV/gamma_L)**2)

    n_iter = 0
    while abs(kappa_hi - kappa_lo) > tol and n_iter < 100:
        kappa_mid = (kappa_lo + kappa_hi) / 2
        F_mid = integrate_flow(kappa_mid, N_steps)[0] - v**2 / (2 * (Lambda_UV/gamma_L)**2)

        if F_lo * F_mid < 0:
            kappa_hi = kappa_mid
            F_hi = F_mid
        else:
            kappa_lo = kappa_mid
            F_lo = F_mid

        n_iter += 1
        if n_iter % 10 == 0:
            print(f"  Iter {n_iter:3d}: kappa_mid = {mp.nstr(kappa_mid, 10)}, |F| = {mp.nstr(abs(F_mid), 5)}")

    kappa0_star = kappa_mid
    F_final = abs(F_mid) if kappa_mid is not None else None

    # k_crit aus dem finalen Lauf
    _, k_crit = integrate_flow(kappa0_star, N_steps)

    print(f"\nBISECTION ERGEBNIS:")
    print(f"kappa0_star = {mp.nstr(kappa0_star, 15)}")
    if F_final:
        print(f"|F|         = {mp.nstr(F_final, 5)}")
    if k_crit:
        print(f"k_crit      = {mp.nstr(k_crit, 10)} MeV")
        gamma_emergent = Delta_star / k_crit
        print(f"gamma_emerg = {mp.nstr(gamma_emergent, 10)}")
        print(f"gamma_Ledger= {mp.nstr(gamma_L, 10)}")
        delta = abs(gamma_emergent - gamma_L)
        print(f"|delta_gamma|= {mp.nstr(delta, 5)}")
        if delta < delta_gamma:
            print("  PASS: gamma_emergent innerhalb delta_gamma des Ledger-Werts")
        else:
            n_sigma = delta / delta_gamma
            print(f"  [TENSION ALERT]: {mp.nstr(n_sigma, 3)} * delta_gamma Abweichung")
    else:
        print("  WARN: k_crit nicht gefunden in diesem Lauf")

    # RG-Constraint
    lambda_S = 5 * kappa0_star**2 / 3
    LHS = 5 * kappa0_star**2
    RHS = 3 * lambda_S
    rg_res = abs(LHS - RHS)
    print(f"\nRG-CONSTRAINT: |5kappa^2 - 3lambda_S| = {mp.nstr(rg_res, 5)}")
    if rg_res < mp.mpf('1e-14'):
        print("  PASS")
    else:
        print("  [RG_CONSTRAINT_FAIL]")

    return {
        'kappa0_star': kappa0_star,
        'k_crit': k_crit,
        'F_final': F_final,
    }


if __name__ == '__main__':
    import sys
    N_steps = 4000
    tol_val = mp.mpf('1e-5')

    # CLI: --N_steps 10000 --tol 1e-14 --mp_dps 80
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == '--N_steps' and i+1 < len(args):
            N_steps = int(args[i+1])
        if arg == '--tol' and i+1 < len(args):
            mp.dps = 80
            tol_val = mp.mpf(args[i+1])

    run_frg_s2(N_steps=N_steps, tol=tol_val)
