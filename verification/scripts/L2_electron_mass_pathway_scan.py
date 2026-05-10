#!/usr/bin/env python3
"""
L2 Electron Mass Residual — Numerical Pathway Scan
UIDT Framework v3.9 | Evidence: [E] speculative

Scans Pathways A (Yukawa-S(x)), B (Koide/SU(3)), C (E_T mixing)
All calculations: mpmath, mp.dps=80, no float(), no round().

Author: P. Rietz | DOI: 10.5281/zenodo.17835200
"""

import mpmath as mp
mp.dps = 80

# ---------------------------------------------------------------------------
# IMMUTABLE LEDGER CONSTANTS (must not be modified)
# ---------------------------------------------------------------------------
Delta   = mp.mpf('1.710')          # GeV  [A]  Yang-Mills spectral gap
gamma   = mp.mpf('16.339')         # [A-] phenomenological vacuum parameter
v       = mp.mpf('47.7')           # MeV  [A]  scalar VEV
ET      = mp.mpf('2.44')           # MeV  [C]  torsion binding energy
kappa   = mp.mpf('0.500')          # [A]  scalar-gluon coupling
lambda_S = mp.mpf('5') / mp.mpf('12')  # [A-] exact rational

# ---------------------------------------------------------------------------
# EXPERIMENTAL REFERENCE VALUES (CODATA 2022 / PDG 2024)
# ---------------------------------------------------------------------------
m_e_codata = mp.mpf('0.51099895000')   # MeV  electron mass
m_mu       = mp.mpf('105.6583755')     # MeV  muon mass
m_tau      = mp.mpf('1776.86')         # MeV  tau mass
m_u_pdg    = mp.mpf('2.16')            # MeV  up quark (PDG 2024 central)
m_d_pdg    = mp.mpf('4.67')            # MeV  down quark (PDG 2024 central)
sin2_tW    = mp.mpf('0.23122')         # Weinberg angle sin^2(theta_W)
Nc         = mp.mpf('3')               # SU(3) colour

Delta_MeV  = Delta * mp.mpf('1000')

# ---------------------------------------------------------------------------
# RG CONSTRAINT CHECK (mandatory)
# ---------------------------------------------------------------------------
rg_lhs = mp.mpf('5') * kappa**2
rg_rhs = mp.mpf('3') * lambda_S
rg_residual = abs(rg_lhs - rg_rhs)
assert rg_residual < mp.mpf('1e-14'), f"[RG_CONSTRAINT_FAIL] residual={rg_residual}"
print(f"RG constraint 5*kappa^2 = 3*lambda_S: residual = {mp.nstr(rg_residual, 6)} [PASS]")
print()

# ---------------------------------------------------------------------------
# PATHWAY A: Yukawa-S(x) coupling  [E]
# m_e = y_e * v  =>  y_e = m_e / v
# ---------------------------------------------------------------------------
print("=" * 60)
print("PATHWAY A: Yukawa-S(x) coupling [E]")
print("=" * 60)

y_e = m_e_codata / v
print(f"y_e = m_e / v = {mp.nstr(y_e, 20)}")
print()
print("Structural candidates for y_e from UIDT parameters:")
candidates_A = {
    "kappa/gamma^2":         kappa / gamma**2,
    "ET/(gamma*v)":          ET / (gamma * v),
    "v/(gamma*Delta_MeV)":   v / (gamma * Delta_MeV),
    "1/(gamma*sqrt(Nc))": mp.mpf('1') / (gamma * mp.sqrt(Nc)),
    "sqrt(ET/Delta_MeV)/gamma": mp.sqrt(ET / Delta_MeV) / gamma,
    "kappa/(gamma*sqrt(Nc))": kappa / (gamma * mp.sqrt(Nc)),
}
for name, val in candidates_A.items():
    ratio = val / y_e
    print(f"  {name:35s} = {mp.nstr(val, 10)}  |  ratio/y_e = {mp.nstr(ratio, 8)}")

print()
print("RESULT A: No candidate reproduces y_e within 10%. [E] status confirmed.")
print("Open action L2-A1: derive y_e from (kappa, lambda_S) without free parameter.")
print()

# ---------------------------------------------------------------------------
# PATHWAY B: Koide relation and SU(3) algebra  [E]
# ---------------------------------------------------------------------------
print("=" * 60)
print("PATHWAY B: Koide relation and SU(3) algebra [E]")
print("=" * 60)

koide_num = m_e_codata + m_mu + m_tau
koide_den = (mp.sqrt(m_e_codata) + mp.sqrt(m_mu) + mp.sqrt(m_tau))**2
Q_koide   = koide_num / koide_den
Q_exact   = mp.mpf('2') / mp.mpf('3')

print(f"Koide Q (experimental) = {mp.nstr(Q_koide, 20)}")
print(f"2/3 exact              = {mp.nstr(Q_exact,  20)}")
print(f"|Q - 2/3|              = {mp.nstr(abs(Q_koide - Q_exact), 6)}")
print()

# SU(3) colour candidates for 2/3
C2_fund   = (Nc**2 - mp.mpf('1')) / (mp.mpf('2') * Nc)  # = 4/3
print("SU(3) candidates for Koide 2/3:")
print(f"  2/N_c                = {mp.nstr(mp.mpf('2')/Nc, 20)}  <- EXACT MATCH")
print(f"  1 - 1/N_c           = {mp.nstr(mp.mpf('1') - mp.mpf('1')/Nc, 20)}  <- SAME")
print(f"  C2(fund) = 4/3      = {mp.nstr(C2_fund, 10)}  (differs)")
print(f"  gamma_bare = 49/3   = {mp.nstr(mp.mpf('49')/mp.mpf('3'), 10)}")
print(f"  gamma_bare/gamma    = {mp.nstr(mp.mpf('49')/(mp.mpf('3')*gamma), 10)}")
print()
print("KEY FINDING [E]:")
print("  Koide Q = 2/3 = 2/N_c (SU(3) democratic weight).")
print("  This equals 1 - 1/N_c = colour suppression residual.")
print("  Interpretation: Koide constraint may arise from colour-democratic")
print("  lepton vacuum coupling where each generation carries weight 1/N_c")
print("  of the total sqrt-mass. Physical basis: unknown. Status: [E].")
print()
print("Open action L2-B1: prove/disprove 2/3 = 2/N_c from S(x)-vacuum geometry.")
print()

# ---------------------------------------------------------------------------
# PATHWAY C: E_T mixing angle  [E]
# ---------------------------------------------------------------------------
print("=" * 60)
print("PATHWAY C: E_T mixing angle [E]")
print("=" * 60)

# E_T quark coincidences (confirmed [C])
print("E_T quark sector coincidences [C]:")
print(f"  E_T       = {mp.nstr(ET, 6)} MeV    m_u = {mp.nstr(m_u_pdg, 6)} MeV")
print(f"  E_T/m_u   = {mp.nstr(ET/m_u_pdg, 8)}   (13% off)")
print(f"  E_T,iso   = {mp.nstr(2*ET, 6)} MeV    m_d = {mp.nstr(m_d_pdg, 6)} MeV")
print(f"  E_T,iso/m_d = {mp.nstr(2*ET/m_d_pdg, 8)}   (4.5% off)")
print()

# Lepton sector: m_e = E_T * sin^2(theta_l)
ratio_e_ET = m_e_codata / ET
theta_l    = mp.asin(mp.sqrt(ratio_e_ET))   # radians
theta_W    = mp.asin(mp.sqrt(sin2_tW))       # Weinberg angle

print("Lepton mixing hypothesis: m_e = E_T * sin^2(theta_l)")
print(f"  sin^2(theta_l) = m_e/E_T = {mp.nstr(ratio_e_ET, 12)}")
print(f"  theta_l        = {mp.nstr(theta_l * 180 / mp.pi, 10)} degrees")
print(f"  theta_W        = {mp.nstr(theta_W * 180 / mp.pi, 10)} degrees")
print(f"  theta_l/theta_W = {mp.nstr(theta_l / theta_W, 10)}  (5.2% below theta_W)")
print()

# Additional candidates
print("Additional m_e candidates from E_T:")
m_e_cand1 = ET * sin2_tW
m_e_cand2 = ET * (mp.mpf('2') / Nc)            # E_T * Koide
m_e_cand3 = ET * kappa / gamma                  # E_T * kappa / gamma
m_e_cand4 = ET * mp.mpf('1') / (gamma * kappa) # E_T / (gamma*kappa)

for label, val in [
    ("E_T * sin^2(theta_W)",   m_e_cand1),
    ("E_T * (2/N_c)",          m_e_cand2),
    ("E_T * kappa/gamma",      m_e_cand3),
    ("E_T / (gamma*kappa)",    m_e_cand4),
]:
    res = (val - m_e_codata) / m_e_codata * mp.mpf('100')
    print(f"  {label:30s} = {mp.nstr(val, 8)} MeV  | residual = {mp.nstr(res, 6)}%")

print()
print("RESULT C: No candidate <1% residual found. [E] status confirmed.")
print("Open action L2-C1: derive theta_l from UIDT torsion geometry.")
print()

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print()
print("Pathway A (Yukawa-S(x)):")
print("  y_e = m_e/v = 0.01071 not reproduced by UIDT parameters. [E]")
print("  Structural: lepton-Yukawa needs separate derivation.")
print()
print("Pathway B (Koide):")
print("  KEY: Koide 2/3 = 2/N_c = colour-democratic SU(3) weight. [E]")
print("  This is a non-trivial algebraic coincidence warranting investigation.")
print()
print("Pathway C (E_T mixing):")
print("  theta_l = 27.23 deg vs theta_W = 28.74 deg: 5.2% proximity. [E]")
print("  E_T * sin^2(theta_W) gives 10.4% residual: not sufficient.")
print()
print("OVERALL: L2 remains [E/open]. No pathway closed. Honest status: [E].")
print("Recommendation: Pathway B (Koide/SU(3)) is highest-priority research.")
print("Action: Derive 2/N_c from S(x)-vacuum configuration (L2-B1).")
print()
print(f"mpmath precision: mp.dps = {mp.dps}")
print(f"RG constraint residual: {mp.nstr(rg_residual, 6)} < 1e-14 [PASS]")
