"""FRG-Tachyon S2-a: γ_emergent via first principles — N_steps >= 10000, |F| < 1e-14

TKT-20260429-hp-csv-lambda-patch-s2a  (Fix v2)

BUG FIX gegenüber v1:
  m2_0 war -(344 MeV)² (bereits tachyonisch) → kein Vorzeichenwechsel detektierbar.
  Korrekt: m2_0 > 0 an UV-Skala k_UV; der FRG-Flow treibt m² auf negativ bei k_crit.
  Physikalische Begründung:
    - Bei k = k_UV = Δ* ist das Skalarfeld massiv (m²_S > 0).
    - Die Threshold-Funktion (∝ 3λ_S k²) dominiert bei großen k und reduziert m²_S.
    - Bei k_crit unterschreitet m²_S Null → tachyonische Instabilität → γ_emergent = Δ*/k_crit.
    - |m_S(Λ)_UV| ~ 344 MeV aus SVZ ist die IR-Skala (Vakuum-Kondensat), nicht die UV-Masse.
  Neuer UV-Startwert: m2_0 = +(κ̃₀* · k_UV)² basierend auf S1-Bisection-Ergebnis:
    κ̃₀* = 0.04877718 (S1, N=4000) → m2_UV = (0.04877718 · 1710)² ≈ (83.4 MeV)²

Evidence: [D] → candidate [C] wenn |Δγ| < δγ = 0.0047

Pre-flight:
- Kein float()
- mp.dps = 80 LOCAL (RACE CONDITION LOCK)
- Kein mock/patch
- RG-Constraint in Phase 0
- [RG_CONSTRAINT_FAIL] bei Verletzung
- [TENSION ALERT] wenn |γ_emergent − γ_ledger| > δγ
"""

import mpmath as mp
import sys

# ────────────────────────────────────────────────────────────────────────────
# IMMUTABLE LEDGER (read-only, never modified)
# ────────────────────────────────────────────────────────────────────────────
LEDGER = {
    "Delta_star":  "1.710",    # GeV  [A]
    "gamma":       "16.339",   # [A-]
    "delta_gamma": "0.0047",   # [A-]
    "v":           "47.7",     # MeV  [A]
    "ET":          "2.44",     # MeV  [C]
    "kappa":       "0.5",      # [A]  exact 1/2
    "lambda_S":    "5",        # [A]  numerator of 5/12
    "lambda_S_den":"12",       # [A]  denominator
    # S1-Bisection result (N=4000, tol=1e-5) — used for UV boundary m2_0
    "kappa_tilde_s1": "0.04877718",  # [D]  κ̃₀* from S1
}


def rg_constraint_check() -> bool:
    """Phase 0: verify 5κ² = 3λ_S exactly."""
    mp.dps = 80
    kappa    = mp.mpf("1") / mp.mpf("2")
    lambda_S = mp.mpf(LEDGER["lambda_S"]) / mp.mpf(LEDGER["lambda_S_den"])
    residual = abs(mp.mpf(5) * kappa**2 - mp.mpf(3) * lambda_S)
    if residual > mp.mpf("1e-14"):
        print(f"[RG_CONSTRAINT_FAIL] residual = {mp.nstr(residual, 20)}")
        sys.exit(1)
    print(f"[RG_CONSTRAINT: PASS] residual = {mp.nstr(residual, 20)}")
    return True


def ym_beta_one_loop(alpha: mp.mpf, N_c: mp.mpf) -> mp.mpf:
    """One-loop β-function, pure YM (N_f=0)."""
    mp.dps = 80
    b0 = mp.mpf(11) * N_c / mp.mpf(3)
    return -b0 * alpha**2


def scalar_mass_flow(
    m2: mp.mpf, alpha: mp.mpf, lambda_S: mp.mpf, k: mp.mpf, N_c: mp.mpf
) -> mp.mpf:
    """LPA' truncation: dm²_S/dt = η_A·m²_S − threshold(k,m²_S)."""
    mp.dps = 80
    eta_A     = mp.mpf(2) * alpha * N_c / (mp.mpf(3) * mp.pi)
    denom     = (mp.mpf(1) + m2 / k**2) ** 2
    threshold = mp.mpf(3) * lambda_S * k**2 / denom
    return eta_A * m2 - threshold


def frg_flow_rk4(
    k_UV: mp.mpf,
    k_IR: mp.mpf,
    N_steps: int,
    alpha0: mp.mpf,
    m2_0: mp.mpf,
    lambda_S: mp.mpf,
    N_c: mp.mpf,
    tol_F: str = "1e-14",
) -> dict:
    """
    4th-order Runge-Kutta FRG flow from k_UV to k_IR.
    m2_0 MUST be positive at k_UV (UV massive phase).
    k_crit is detected when m²_S crosses zero from above.
    """
    mp.dps = 80
    assert m2_0 > mp.mpf(0), "m2_0 must be positive at UV scale (UV massive phase)"

    tol = mp.mpf(tol_F)
    dt  = (mp.log(k_IR) - mp.log(k_UV)) / N_steps  # negative: flow to IR

    k, m2, alpha = k_UV, m2_0, alpha0
    k_crit     = None
    F_residual = mp.mpf(0)
    steps_used = N_steps

    for step in range(N_steps):
        def derivs(ki, ai, m2i):
            da = ym_beta_one_loop(ai, N_c)
            dm = scalar_mass_flow(m2i, ai, lambda_S, ki, N_c)
            return da, dm

        da1, dm1 = derivs(k,                  alpha,            m2)
        da2, dm2 = derivs(k*mp.exp(dt/2),     alpha+da1*dt/2,   m2+dm1*dt/2)
        da3, dm3 = derivs(k*mp.exp(dt/2),     alpha+da2*dt/2,   m2+dm2*dt/2)
        da4, dm4 = derivs(k*mp.exp(dt),       alpha+da3*dt,     m2+dm3*dt)

        alpha_new = alpha + (da1+2*da2+2*da3+da4)*dt/6
        m2_new    = m2    + (dm1+2*dm2+2*dm3+dm4)*dt/6
        k_new     = k * mp.exp(dt)

        # k_crit: first zero crossing m² > 0 → m² < 0
        if k_crit is None and m2_new < mp.mpf(0) and m2 > mp.mpf(0):
            k_lo, k_hi = k_new, k   # k flows downward, k_new < k
            m2_lo, m2_hi = m2_new, m2
            for _ in range(100):
                k_mid  = (k_lo + k_hi) / 2
                frac   = (k_mid - k_lo) / (k_hi - k_lo)
                m2_mid = m2_lo + frac * (m2_hi - m2_lo)
                if m2_mid < mp.mpf(0):
                    k_lo, m2_lo = k_mid, m2_mid
                else:
                    k_hi, m2_hi = k_mid, m2_mid
                if abs(k_hi - k_lo) < mp.mpf("1e-25"):
                    break
            k_crit     = (k_lo + k_hi) / 2
            F_residual = abs(scalar_mass_flow(m2, alpha, lambda_S, k, N_c))

        alpha, m2, k = alpha_new, m2_new, k_new
        steps_used   = step + 1

        if abs(dm1) < tol:
            break

    Delta_star_MeV = mp.mpf(LEDGER["Delta_star"]) * mp.mpf("1000")
    gamma_emergent = None if k_crit is None else Delta_star_MeV / k_crit

    return {
        "k_crit":          k_crit,
        "m2_final":        m2,
        "alpha_final":     alpha,
        "gamma_emergent":  gamma_emergent,
        "F_residual":      F_residual,
        "steps_used":      steps_used,
    }


def run_s2a() -> None:
    mp.dps = 80

    # Phase 0: RG constraint
    rg_constraint_check()

    # Physical parameters
    N_c      = mp.mpf(3)
    lambda_S = mp.mpf(LEDGER["lambda_S"]) / mp.mpf(LEDGER["lambda_S_den"])  # 5/12
    k_UV     = mp.mpf("1710")   # MeV = Δ*
    k_IR     = mp.mpf("1")      # MeV
    alpha0   = mp.mpf("0.3")

    # UV boundary: m2_0 > 0 (scalar is massive at UV scale)
    # From S1 bisection: κ̃₀* = 0.04877718 → m_S(k_UV) = κ̃₀* · k_UV
    kappa_tilde = mp.mpf(LEDGER["kappa_tilde_s1"])
    m_UV    = kappa_tilde * k_UV           # ~ 83.4 MeV
    m2_0    = m_UV ** 2                    # > 0  (UV massive phase)

    N_steps = 10000

    print(f"\n[S2-a] FRG-Tachyon flow  N_steps={N_steps}, mp.dps=80")
    print(f"  k_UV          = {mp.nstr(k_UV, 10)} MeV")
    print(f"  k_IR          = {mp.nstr(k_IR, 6)} MeV")
    print(f"  alpha_s(k_UV) = {mp.nstr(alpha0, 6)}")
    print(f"  κ̃₀* (S1)     = {mp.nstr(kappa_tilde, 10)}  [D]")
    print(f"  m_UV          = {mp.nstr(m_UV, 10)} MeV  (= κ̃₀* · k_UV)")
    print(f"  m2_0          = +{mp.nstr(m2_0, 10)} MeV²  [UV massive phase, > 0]")
    print(f"  λ_S           = {mp.nstr(lambda_S, 10)}  [A] exact 5/12")
    print()

    result = frg_flow_rk4(
        k_UV=k_UV, k_IR=k_IR, N_steps=N_steps,
        alpha0=alpha0, m2_0=m2_0,
        lambda_S=lambda_S, N_c=N_c,
        tol_F="1e-14",
    )

    gamma_ledger = mp.mpf(LEDGER["gamma"])
    delta_gamma  = mp.mpf(LEDGER["delta_gamma"])

    print("[S2-a RESULTS]")
    if result["k_crit"]:
        g_em  = result["gamma_emergent"]
        delta = abs(g_em - gamma_ledger)
        ratio = delta / delta_gamma
        print(f"  k_crit          = {mp.nstr(result['k_crit'], 20)} MeV")
        print(f"  gamma_emergent  = {mp.nstr(g_em, 20)}  [D]")
        print(f"  gamma_ledger    = {mp.nstr(gamma_ledger, 20)}  [A-]")
        print(f"  |Δγ|            = {mp.nstr(delta, 15)}")
        print(f"  δγ (ledger)     = {mp.nstr(delta_gamma, 6)}")
        print(f"  |Δγ|/δγ         = {mp.nstr(ratio, 8)}")
        if delta > delta_gamma:
            print(f"  [TENSION ALERT]")
            print(f"    External γ_emergent = {mp.nstr(g_em, 12)}  [D]")
            print(f"    UIDT Ledger γ       = {mp.nstr(gamma_ledger, 12)}  [A-]")
            print(f"    Differenz           = {mp.nstr(delta, 10)}")
            print(f"    Ursache prüfen: κ̃₀*-Präzision, NLO-Korrekturen (S2-b)")
        else:
            print(f"  [TENSION RESOLVED] |Δγ| < δγ — γ_emergent kandidiert [D]→[C]")
    else:
        print("  k_crit: NOT REACHED")
        print("  Diagnose: kein m²_S-Vorzeichenwechsel im Flow-Fenster [k_UV→k_IR]")
        print("  Prüfen: m2_0, α_s(k_UV), Trunkierungs-Vollständigkeit")

    print(f"  F_residual      = {mp.nstr(result['F_residual'], 10)}")
    print(f"  steps_used      = {result['steps_used']} / {N_steps}")
    print(f"  m2_final        = {mp.nstr(result['m2_final'], 15)} MeV²")
    print(f"  alpha_final     = {mp.nstr(result['alpha_final'], 15)}")
    print(f"  |m_UV|          = {mp.nstr(mp.sqrt(m2_0), 8)} MeV  (UV-Startwert)")


if __name__ == "__main__":
    run_s2a()
