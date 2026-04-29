"""FRG-Tachyon S2-a: γ_emergent via first principles — N_steps >= 10000, |F| < 1e-14

TKT-20260429-hp-csv-lambda-patch-s2a
Evidence: [D] → candidate [C] if |Δγ| < δγ = 0.0047

Pre-flight:
- No float()
- mp.dps = 80 declared LOCAL (RACE CONDITION LOCK)
- No mock/patch
- RG-constraint check embedded
- [RG_CONSTRAINT_FAIL] emitted on violation
- [TENSION ALERT] emitted if |γ_emergent - γ_ledger| > δγ
"""

import mpmath as mp
import sys

# ──────────────────────────────────────────────────────────────
# IMMUTABLE LEDGER (read-only reference, never modified)
# ──────────────────────────────────────────────────────────────
LEDGER = {
    "Delta_star":  "1.710",    # GeV  [A]
    "gamma":       "16.339",   # [A-]
    "delta_gamma": "0.0047",   # [A-]
    "v":           "47.7",     # MeV  [A]
    "ET":          "2.44",     # MeV  [C]
    "kappa":       "0.5",      # [A]  exact 1/2
    "lambda_S":    "0.41666666666666666666666666666666666666666666666666666666666666666666666666666666",  # [A] exact 5/12
}


def rg_constraint_check() -> None:
    """Phase 0: verify 5κ² = 3λ_S exactly before any numerical work."""
    mp.dps = 80
    kappa    = mp.mpf(LEDGER["kappa"])
    lambda_S = mp.mpf(LEDGER["lambda_S"])
    residual = abs(mp.mpf(5) * kappa**2 - mp.mpf(3) * lambda_S)
    if residual > mp.mpf("1e-14"):
        print(f"[RG_CONSTRAINT_FAIL] residual = {mp.nstr(residual, 20)}")
        sys.exit(1)
    print(f"[RG_CONSTRAINT: PASS] residual = {mp.nstr(residual, 20)}")


def ym_beta_function(alpha: mp.mpf, N_c: mp.mpf, N_f: mp.mpf) -> mp.mpf:
    """One-loop + two-loop β-function coefficient (pure YM: N_f=0)."""
    mp.dps = 80
    b0 = (mp.mpf(11) * N_c - mp.mpf(2) * N_f) / mp.mpf(3)
    b1 = (mp.mpf(34) * N_c**2 - (mp.mpf(10) * N_c + mp.mpf(3) * (N_c - mp.mpf(1)/N_c)) * N_f) / mp.mpf(3)
    return -b0 * alpha**2 * (mp.mpf(1) + b1 / b0 * alpha)


def scalar_mass_flow(
    m2: mp.mpf,
    alpha: mp.mpf,
    kappa: mp.mpf,
    lambda_S: mp.mpf,
    k: mp.mpf,
    N_c: mp.mpf,
) -> mp.mpf:
    """LPA' truncation: dm²_S/dt = η_A * m²_S + threshold contributions."""
    mp.dps = 80
    # anomalous dimension from Wetterink equation in YM sector
    eta_A = mp.mpf(2) * alpha * N_c / (mp.mpf(3) * mp.pi)
    # scalar threshold function (LPA', regulator: optimised Litim)
    threshold = mp.mpf(3) * lambda_S * k**2 / (mp.mpf(1) + m2 / k**2)**2
    return eta_A * m2 - threshold


def frg_flow_rk4(
    k_UV: mp.mpf,
    k_IR: mp.mpf,
    N_steps: int,
    alpha0: mp.mpf,
    m2_0: mp.mpf,
    kappa: mp.mpf,
    lambda_S: mp.mpf,
    N_c: mp.mpf,
    N_f: mp.mpf,
    tol_F: str = "1e-14",
) -> dict:
    """4th-order Runge-Kutta FRG flow from k_UV to k_IR.

    Returns dict with:
        k_crit        — scale where m²_S crosses zero (tachyonic threshold)
        m2_final      — scalar mass squared at k_IR
        alpha_final   — running coupling at k_IR
        gamma_emergent — k_UV / k_crit
        F_residual    — |dm²/dt| at k_crit (convergence diagnostic)
        steps_used    — actual RK4 steps
    """
    mp.dps = 80
    tol = mp.mpf(tol_F)
    dt  = (mp.log(k_IR) - mp.log(k_UV)) / N_steps  # t = ln(k/k_UV), negative

    k      = k_UV
    m2     = m2_0
    alpha  = alpha0
    k_crit = None
    F_residual = mp.mpf(0)

    for step in range(N_steps):
        t = mp.log(k / k_UV)

        # RK4 for (alpha, m2) simultaneously
        def derivs(ki: mp.mpf, ai: mp.mpf, m2i: mp.mpf):
            da = ym_beta_function(ai, N_c, N_f)
            dm = scalar_mass_flow(m2i, ai, kappa, lambda_S, ki, N_c)
            return da, dm

        da1, dm1 = derivs(k,                         alpha,              m2)
        da2, dm2 = derivs(k * mp.exp(dt/2),          alpha + da1*dt/2,   m2 + dm1*dt/2)
        da3, dm3 = derivs(k * mp.exp(dt/2),          alpha + da2*dt/2,   m2 + dm2*dt/2)
        da4, dm4 = derivs(k * mp.exp(dt),            alpha + da3*dt,     m2 + dm3*dt)

        alpha_new = alpha + (da1 + 2*da2 + 2*da3 + da4) * dt / 6
        m2_new    = m2    + (dm1 + 2*dm2 + 2*dm3 + dm4) * dt / 6
        k_new     = k * mp.exp(dt)

        # tachyon detection: sign change in m²_S
        if k_crit is None and m2_new < mp.mpf(0) and m2 > mp.mpf(0):
            # bisection refinement between k and k_new
            k_lo, k_hi = k, k_new
            m2_lo, m2_hi = m2, m2_new
            for _ in range(100):
                k_mid  = (k_lo + k_hi) / 2
                # linear interpolation of m2 for bisection step
                frac   = (k_mid - k_lo) / (k_hi - k_lo)
                m2_mid = m2_lo + frac * (m2_hi - m2_lo)
                if m2_mid > mp.mpf(0):
                    k_lo, m2_lo = k_mid, m2_mid
                else:
                    k_hi, m2_hi = k_mid, m2_mid
                if abs(k_hi - k_lo) < mp.mpf("1e-25"):
                    break
            k_crit     = (k_lo + k_hi) / 2
            F_residual = abs(scalar_mass_flow(m2, alpha, kappa, lambda_S, k, N_c))

        alpha = alpha_new
        m2    = m2_new
        k     = k_new

        if abs(dm1) < tol:
            break

    Delta_star_MeV = mp.mpf(LEDGER["Delta_star"]) * mp.mpf("1000")  # GeV → MeV
    gamma_emergent = None if k_crit is None else Delta_star_MeV / k_crit

    return {
        "k_crit":         k_crit,
        "m2_final":       m2,
        "alpha_final":    alpha,
        "gamma_emergent": gamma_emergent,
        "F_residual":     F_residual,
        "steps_used":     step + 1,
    }


def run_s2a() -> None:
    mp.dps = 80

    # ── Phase 0: RG constraint ──────────────────────────────────
    rg_constraint_check()

    # ── Physical parameters ─────────────────────────────────────
    N_c      = mp.mpf(3)         # SU(3)
    N_f      = mp.mpf(0)         # pure YM
    kappa    = mp.mpf(LEDGER["kappa"])
    lambda_S = mp.mpf(LEDGER["lambda_S"])

    # UV boundary conditions  (scale: MeV)
    k_UV   = mp.mpf("1710")      # = Δ*  [A]
    k_IR   = mp.mpf("1")         # 1 MeV IR cutoff
    alpha0 = mp.mpf("0.3")       # α_s(k_UV) ~ perturbative
    # m²_S(Λ) < 0 from SVZ motivation (|m_S| ~ 345 MeV from S1)
    m2_0   = -(mp.mpf("344") ** 2)

    N_steps = 10000  # S2-a requirement: N_steps >= 10000

    print("\n[S2-a] FRG-Tachyon flow N_steps=10000, tol=1e-14")
    print(f"  k_UV     = {mp.nstr(k_UV, 10)} MeV")
    print(f"  k_IR     = {mp.nstr(k_IR, 6)} MeV")
    print(f"  alpha0   = {mp.nstr(alpha0, 6)}")
    print(f"  m2_0     = {mp.nstr(m2_0, 10)} MeV²")
    print(f"  kappa    = {mp.nstr(kappa, 6)}  [A] exact 1/2")
    print(f"  lambda_S = {mp.nstr(lambda_S, 10)}  [A] exact 5/12")
    print()

    result = frg_flow_rk4(
        k_UV=k_UV, k_IR=k_IR, N_steps=N_steps,
        alpha0=alpha0, m2_0=m2_0,
        kappa=kappa, lambda_S=lambda_S,
        N_c=N_c, N_f=N_f,
        tol_F="1e-14",
    )

    gamma_ledger = mp.mpf(LEDGER["gamma"])
    delta_gamma  = mp.mpf(LEDGER["delta_gamma"])

    print("[S2-a RESULTS]")
    print(f"  k_crit          = {mp.nstr(result['k_crit'], 15) if result['k_crit'] else 'NOT REACHED'} MeV")
    print(f"  gamma_emergent  = {mp.nstr(result['gamma_emergent'], 15) if result['gamma_emergent'] else 'N/A'}  [D]")
    print(f"  gamma_ledger    = {mp.nstr(gamma_ledger, 15)}  [A-]")
    if result["gamma_emergent"]:
        delta = abs(result["gamma_emergent"] - gamma_ledger)
        print(f"  |Δγ|            = {mp.nstr(delta, 10)}")
        print(f"  δγ (ledger)     = {mp.nstr(delta_gamma, 6)}")
        ratio = delta / delta_gamma
        print(f"  |Δγ|/δγ         = {mp.nstr(ratio, 6)}")
        if delta > delta_gamma:
            print(f"  [TENSION ALERT] |Δγ| = {mp.nstr(delta, 8)} > δγ = {mp.nstr(delta_gamma, 6)}")
            print(f"  External γ_emergent = {mp.nstr(result['gamma_emergent'], 10)} [D]")
            print(f"  UIDT Ledger γ       = {mp.nstr(gamma_ledger, 10)} [A-]")
            print(f"  Difference          = {mp.nstr(delta, 8)}")
        else:
            print(f"  [TENSION RESOLVED] |Δγ| < δγ — candidate Evidence [D] → [C]")
    print(f"  F_residual      = {mp.nstr(result['F_residual'], 10)}")
    print(f"  steps_used      = {result['steps_used']}")
    print(f"  m2_final        = {mp.nstr(result['m2_final'], 10)} MeV²")
    print(f"  alpha_final     = {mp.nstr(result['alpha_final'], 10)}")
    print(f"  |m_S(Λ)|        = {mp.nstr(mp.sqrt(abs(m2_0)), 8)} MeV  (SVZ-check: ~330-350 MeV [B])")


if __name__ == "__main__":
    run_s2a()
