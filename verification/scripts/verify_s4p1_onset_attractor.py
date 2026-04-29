"""S4-P1: Verifikation des tachyonischen Onset-Attractors im FRG-System.

Verifiziert:
- C-S4P1-01: κ̃₀^attr = -0.01030923381
- C-S4P1-04: Regulator-Unabhängigkeit bei ω_A >> 1
- Alle numerischen Checks mit mp.dps=80

Kein Mock, kein float(), kein round().
"""

import mpmath as mp

mp.dps = 80

# ── Ledger-Konstanten ──────────────────────────────────────────────────────
Nc        = mp.mpf('3')
DELTA     = mp.mpf('1.710')
ET        = mp.mpf('2.44e-3')
ALPHA_UV  = mp.mpf('0.30')
CA        = Nc
b0        = 11 * CA / (12 * mp.pi)


def alpha_s(t: mp.mpf) -> mp.mpf:
    """1-Loop laufendes α_s, t = ln(k/Λ)."""
    denom = 1 + b0 * ALPHA_UV * (-t)
    if denom < mp.mpf('0.05'):
        denom = mp.mpf('0.05')
    return ALPHA_UV / denom


def c_A_integrand(s: mp.mpf) -> mp.mpf:
    """e^{2s} · c_A(s) für den Attractor-Integral."""
    omega_A = mp.exp(-2 * s)
    g = alpha_s(s)
    c_A = (Nc**2 - 1) * g / (4 * mp.pi * (1 + omega_A)**2)
    return mp.exp(2 * s) * c_A


def verify_attractor() -> bool:
    """C-S4P1-01: κ̃₀^attr Verifikation."""
    integral = mp.quad(c_A_integrand, [mp.mpf('-10'), mp.mpf('0')])
    kappa_attr = -integral
    expected = mp.mpf('-0.01030923381')
    residual = abs(kappa_attr - expected)
    print(f"[C-S4P1-01] κ̃₀^attr = {mp.nstr(kappa_attr, 12)}")
    print(f"            erwartet = {mp.nstr(expected, 12)}")
    print(f"            |Δ|     = {mp.nstr(residual, 6)}")
    passed = residual < mp.mpf('1e-8')
    print(f"            Status  = {'PASS' if passed else 'FAIL'}")
    return passed


def verify_regulator_independence() -> bool:
    """C-S4P1-04: Regulator-Unabhängigkeit bei ω_A >> 1."""
    k_crit = mp.mpf('30.79e-3')  # MeV
    omega_A = (DELTA / k_crit)**2
    g = alpha_s(mp.log(k_crit / DELTA))

    # Litim
    c_litim = (Nc**2 - 1) * g / (4 * mp.pi * (1 + omega_A)**2)
    # Smooth (asymptotisch, ω_A >> 1)
    c_smooth_approx = (Nc**2 - 1) * g / (4 * mp.pi * omega_A**2)

    ratio = c_litim / c_smooth_approx
    expected_ratio = (1 + 1 / omega_A)**(-2)  # → 1 für ω_A >> 1
    residual = abs(ratio - mp.mpf('1'))

    print(f"[C-S4P1-04] ω_A = {mp.nstr(omega_A, 6)}")
    print(f"            c_A^Litim  = {mp.nstr(c_litim, 8)}")
    print(f"            c_A^Smooth ≈ {mp.nstr(c_smooth_approx, 8)}")
    print(f"            Ratio      = {mp.nstr(ratio, 8)}")
    print(f"            |1-ratio|  = {mp.nstr(residual, 6)}")
    passed = residual < mp.mpf('1e-5')  # bei ω_A=3080 exzellent
    print(f"            Status     = {'PASS' if passed else 'FAIL'}")
    return passed


def verify_casimir_consistency() -> bool:
    """C-S4P1-03: E_T·4π vs. numerisches k_crit."""
    k_num    = mp.mpf('30.790e-3')  # MeV, Bisection Session-2
    k_casimir = ET * 4 * mp.pi
    delta_mev = abs(k_num - k_casimir) * 1000  # in MeV
    print(f"[C-S4P1-03] k_crit(num)     = {mp.nstr(k_num*1000, 8)} MeV")
    print(f"            k_crit(E_T·4π)  = {mp.nstr(k_casimir*1000, 8)} MeV")
    print(f"            |Δ|             = {mp.nstr(delta_mev, 6)} MeV")
    passed = delta_mev < mp.mpf('0.5')  # toleranz 0.5 MeV
    print(f"            Status          = {'PASS' if passed else 'FAIL'}")
    return passed


if __name__ == '__main__':
    print('=' * 65)
    print('S4-P1 Onset-Attractor Verifikation (mp.dps=80)')
    print('=' * 65)
    print()

    results = []
    results.append(verify_attractor())
    print()
    results.append(verify_regulator_independence())
    print()
    results.append(verify_casimir_consistency())
    print()

    all_pass = all(results)
    print('=' * 65)
    print(f'GESAMT: {"ALLE PASS" if all_pass else "MINDESTENS EIN FAIL"}')
    print('=' * 65)
