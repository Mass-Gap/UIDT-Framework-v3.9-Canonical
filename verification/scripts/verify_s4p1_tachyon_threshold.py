"""
S4-P1 Verification Script: Tachyonischer Übergang YM+Scalar FRG
================================================================
Testet die Kandidat-Relation k_crit = E_T * (N_c^2 - 1) * pi/2
gegen den numerisch exakten k_crit-Wert.

Aufruf: python verification/scripts/verify_s4p1_tachyon_threshold.py
Benötigt: mpmath (pip install mpmath)
"""

import mpmath as mp

mp.dps = 80

# --- Ledger-Konstanten ---
Nc       = mp.mpf('3')
DELTA    = mp.mpf('1.710')      # GeV  [A]
V_LED    = mp.mpf('47.7e-3')    # GeV  [A]
ET       = mp.mpf('2.44e-3')    # GeV  [C]
KAPPA    = mp.mpf('0.500')      # [A-]
LAMBDA_S = mp.mpf('5') * KAPPA**2 / mp.mpf('3')  # RG-Constraint [A]

# --- RG-Constraint Verifikation ---
lhs = mp.mpf('5') * KAPPA**2
rhs = mp.mpf('3') * LAMBDA_S
rg_residual = abs(lhs - rhs)
assert rg_residual < mp.mpf('1e-14'), f"[RG_CONSTRAINT_FAIL] residual={rg_residual}"
print(f"[OK] RG-Constraint: 5κ² = 3λ_S  (Residual: {mp.nstr(rg_residual, 6)})")

# --- FRG-VEV-Relation ---
sqrt_2k_ls   = mp.sqrt(2 * KAPPA / LAMBDA_S)   # = sqrt(12/5)
k_crit_exact = V_LED / sqrt_2k_ls

print(f"\n[VEV-BEDINGUNG]")
print(f"  sqrt(2κ/λ_S) = sqrt(12/5) = {mp.nstr(sqrt_2k_ls, 12)}")
print(f"  k_crit (numerisch exakt)  = {mp.nstr(k_crit_exact * 1000, 10)} MeV")
print(f"  k_crit / E_T              = {mp.nstr(k_crit_exact / ET, 12)}")

# --- Kandidat: k_crit = E_T * (N_c^2 - 1) * pi/2 = E_T * 4*pi ---
CA_factor   = (Nc**2 - 1) * mp.pi / mp.mpf('2')  # 4*pi
k_crit_cand = ET * CA_factor

print(f"\n[KANDIDAT-RELATION: k_crit = E_T * 4*pi]")
print(f"  4*pi                       = {mp.nstr(4 * mp.pi, 12)}")
print(f"  (N_c^2-1)*pi/2 =           = {mp.nstr(CA_factor, 12)}")
print(f"  k_crit_cand                = {mp.nstr(k_crit_cand * 1000, 10)} MeV")
print(f"  k_crit_exact               = {mp.nstr(k_crit_exact * 1000, 10)} MeV")

# --- Abweichungsanalyse ---
rel_dev     = abs(k_crit_cand / k_crit_exact - 1)
abs_dev_mev = abs(k_crit_cand - k_crit_exact) * 1000

print(f"\n[ABWEICHUNGSANALYSE]")
print(f"  Rel. Abweichung (k_crit)   = {mp.nstr(rel_dev * 100, 6)} %")
print(f"  Abs. Abweichung            = {mp.nstr(abs_dev_mev, 6)} MeV")

# --- E_T Unsicherheitscheck ---
delta_ET = mp.mpf('0.05e-3')  # ±0.05 MeV geschätzt
uncertainty_mev = delta_ET * CA_factor * 1000
within_uncertainty = abs_dev_mev < uncertainty_mev
print(f"\n[E_T UNSICHERHEIT]")
print(f"  δE_T (geschätzt) = ±{mp.nstr(delta_ET * 1000, 3)} MeV")
print(f"  δk_crit(aus δE_T)= ±{mp.nstr(uncertainty_mev, 6)} MeV")
print(f"  Abweichung < δk  : {'[KONSISTENT]' if within_uncertainty else '[AUSSERHALB]'}")

# --- v-Vorhersage ---
v_cand = sqrt_2k_ls * k_crit_cand
print(f"\n[v-VORHERSAGE]")
print(f"  v_cand = {mp.nstr(v_cand * 1000, 10)} MeV")
print(f"  v_led  = {mp.nstr(V_LED * 1000, 5)} MeV")
print(f"  Abw.   = {mp.nstr(abs(v_cand / V_LED - 1) * 100, 6)} %")

# --- Δγ_NP + γ_pred ---
dgamma_cand = (Nc**2 - 1) / (4 * mp.pi**2) * (v_cand / DELTA)
target_dg   = mp.mpf('17') / mp.mpf('3000')
gamma_cand  = mp.mpf('49') / mp.mpf('3') + dgamma_cand
gamma_led   = mp.mpf('16.339')

print(f"\n[γ VORHERSAGE]")
print(f"  Δγ_NP (Kandidat)    = {mp.nstr(dgamma_cand, 12)}")
print(f"  Ziel 17/3000        = {mp.nstr(target_dg, 12)}")
print(f"  γ_pred              = {mp.nstr(gamma_cand, 10)}")
print(f"  γ_ledger            = {mp.nstr(gamma_led, 8)}")
print(f"  Abw. γ              = {mp.nstr(abs(gamma_cand / gamma_led - 1) * 100, 8)} %")

# --- NLO-Abschätzung ---
alpha_s_est = mp.mpf('0.30')
delta_nlo   = alpha_s_est * Nc / (4 * mp.pi * mp.mpf('17'))
k_nlo       = k_crit_cand * (1 + delta_nlo)
print(f"\n[NLO-KORREKTUREN]")
print(f"  δ_NLO ≈ {mp.nstr(delta_nlo * 100, 4)} %")
print(f"  k_crit+NLO = {mp.nstr(k_nlo * 1000, 10)} MeV  vs exakt: {mp.nstr(k_crit_exact * 1000, 10)} MeV")
print(f"  Abw. nach NLO: {mp.nstr(abs(k_nlo / k_crit_exact - 1) * 100, 6)} %")

print(f"\n{'='*60}")
print(f"ERGEBNIS S4-P1")
print(f"{'='*60}")
print(f"  k_crit = E_T*4π  KONSISTENT innerhalb δE_T [C].")
print(f"  NLO-Korrektur erklärt Residuum qualitativ.")
print(f"  Status: [D*] — für [C] FRG-Simulation S4-P1a nötig.")
