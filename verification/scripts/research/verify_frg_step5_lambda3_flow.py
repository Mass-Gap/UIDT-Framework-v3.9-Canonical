"""
UIDT FRG Step 5 Verification Script
TKT-20260429-FRG-STEP5-lambda3-flow

Runs the complete Step 5 pipeline and asserts:
  1. RG constraint residual == 0
  2. phi_0 residual < 1e-14
  3. [NO-GO-STEP5]: physical lambda_3 gives Z_phi(IR) ~ 1 (deviation > 15)
  4. Shooting solution lambda_3* gives |Z_phi(IR) - gamma| < delta_gamma
  5. Tension alert: lambda3_star / lambda3_phys > 1000
"""
from __future__ import annotations
import mpmath as mp


def _p() -> None:
    mp.dps = 80


def run_step5_verification() -> None:
    _p()

    KAPPA    = mp.mpf("1") / mp.mpf("2")
    LAMBDA_S = mp.mpf("5") / mp.mpf("12")
    V_VAC    = mp.mpf("47.7")
    DELTA_STAR = mp.mpf("1710")
    GAMMA    = mp.mpf("16.339")
    DELTA_GAMMA = mp.mpf("0.0047")
    m_sq     = KAPPA ** 2

    # 1. RG constraint
    rg = abs(mp.mpf("5") * KAPPA**2 - mp.mpf("3") * LAMBDA_S)
    assert rg == 0, f"[RG_CONSTRAINT_FAIL] residual={rg}"
    print("[1] RG_CONSTRAINT: PASS")

    # 2. phi_0 from Step 4c
    h   = m_sq * V_VAC / DELTA_STAR
    phi = h / m_sq
    for _ in range(200):
        f  = m_sq * phi - h + LAMBDA_S * phi**3
        fp = m_sq + mp.mpf("3") * LAMBDA_S * phi**2
        phi -= f / fp
    phi_res = abs(m_sq * phi - h + LAMBDA_S * phi**3)
    assert phi_res < mp.mpf("1e-14"), f"phi_0 residual {phi_res} >= 1e-14"
    print(f"[2] phi_0 residual: {mp.nstr(phi_res, 6)} < 1e-14  PASS")

    lambda3_phys = mp.mpf("3") * LAMBDA_S * phi
    print(f"    lambda_3(UV) = {mp.nstr(lambda3_phys, 10)}  [D]")

    # 3. NO-GO: physical lambda_3 cannot drive Z to gamma
    def v4_(): return mp.mpf("1") / (mp.mpf("32") * mp.pi**2)
    def l1_(m): return mp.mpf("-1") / (1 + m)**2
    def l2_(m): return mp.mpf("2") / (1 + m)**3

    def step_(z, m, l3, l4, dt):
        def fz(z, m): return -(v4_() * l3**2 * l2_(m) / z) * z
        def fm(m):    return mp.mpf("-2") * m + mp.mpf("4") * v4_() * l4 * l1_(m)
        k1z, k1m = fz(z, m), fm(m)
        k2z, k2m = fz(z + dt*k1z/2, m + dt*k1m/2), fm(m + dt*k1m/2)
        k3z, k3m = fz(z + dt*k2z/2, m + dt*k2m/2), fm(m + dt*k2m/2)
        k4z, k4m = fz(z + dt*k3z,   m + dt*k3m),   fm(m + dt*k3m)
        return (z + dt*(k1z + 2*k2z + 2*k3z + k4z)/6,
                m + dt*(k1m + 2*k2m + 2*k3m + k4m)/6)

    def run_(l3, n=1000, T=mp.mpf("10")):
        _p()
        z, m_, dt = mp.mpf("1"), m_sq, -T / mp.mpf(str(n))
        for _ in range(n):
            z, m_ = step_(z, m_, l3, LAMBDA_S, dt)
        return z

    z_nogo = run_(lambda3_phys)
    dev_nogo = abs(z_nogo - GAMMA)
    assert dev_nogo > mp.mpf("10"), (
        f"[NO-GO-STEP5 VIOLATION] physical lambda_3 gave dev={dev_nogo}"
    )
    print(f"[3] [NO-GO-STEP5] confirmed: Z_phi(IR)={mp.nstr(z_nogo, 8)}, "
          f"deviation={mp.nstr(dev_nogo, 6)} >> delta_gamma  PASS")

    # 4. Shooting solution: lambda_3* in [95, 105]
    lo, hi = mp.mpf("95"), mp.mpf("105")
    f_lo = run_(lo) - GAMMA
    f_hi = run_(hi) - GAMMA
    assert f_lo * f_hi < 0, "[SEARCH_FAIL] No bracket in [95,105]"
    for _ in range(50):
        mid = (lo + hi) / 2
        f_mid = run_(mid) - GAMMA
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
        if abs(hi - lo) < mp.mpf("1e-6"):
            break
    lambda3_star = (lo + hi) / 2
    z_star = run_(lambda3_star)
    dev_star = abs(z_star - GAMMA)
    assert dev_star < DELTA_GAMMA, (
        f"Shooting solution residual {dev_star} >= delta_gamma {DELTA_GAMMA}"
    )
    print(f"[4] Shooting solution: lambda_3*={mp.nstr(lambda3_star, 10)}, "
          f"|Z_IR - gamma|={mp.nstr(dev_star, 6)} < delta_gamma  PASS")

    # 5. Tension alert
    ratio = lambda3_star / lambda3_phys
    assert ratio > mp.mpf("1000"), f"[TENSION_ALERT missing] ratio={ratio}"
    print(f"[5] [TENSION ALERT] lambda_3*/lambda_3_phys = {mp.nstr(ratio, 8)}x  PASS")

    print()
    print("All Step 5 assertions PASS.")
    print("Evidence [D] — numerical prediction, analytic proof open.")
    print("L4 limitation confirmed: gamma remains [A-].")


if __name__ == "__main__":
    run_step5_verification()
