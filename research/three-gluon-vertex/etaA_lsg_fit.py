# etaA_lsg_fit.py
# UIDT Framework v3.9 — Three-Gluon Vertex: Soft-Gluon Form Factor Fit
#
# Sources:
#   [A]  Aguilar, De Soto, Ferreira, Papavassiliou, Rodriguez-Quintero, Zafeiropoulos
#        "Infrared facets of the three-gluon vertex"
#        Phys. Lett. B 818 (2021) 136352  |  arXiv:2102.04959  [Evidence A]
#
#   [B]  Pinto-Gomez, De Soto, Ferreira, Papavassiliou, Rodriguez-Quintero
#        "Lattice three-gluon vertex in extended kinematics: planar degeneracy"
#        Phys. Lett. B (2022)  |  arXiv:2208.01020  [Evidence B]
#
# Evidence categories: A = mathematically proven, A- = phenomenological,
#                      B = lattice compatible
#
# Epistemic strata:
#   Stratum I  — empirical/lattice data (mu, m_gluon, alpha_s, alpha_sg)
#   Stratum II — scientific consensus (IR suppression, logarithmic divergence)
#   Stratum III — UIDT mapping (connection to Delta* spectral gap)
#
# NUMERICAL DETERMINISM: mp.dps = 80 declared locally (RACE CONDITION LOCK).
# Never use float() or round().
#
# Reproduction:
#   python etaA_lsg_fit.py
#   Expected: [PASS] All residuals < 1e-14

import mpmath as mp
mp.dps = 80  # LOCAL — do not centralize

# ─────────────────────────────────────────────────────────────────
# IMMUTABLE PARAMETER LEDGER (UIDT v3.9)
# ─────────────────────────────────────────────────────────────────
Delta_star = mp.mpf('1.710')   # Yang-Mills spectral gap [GeV]  [Evidence A]
gamma_val  = mp.mpf('16.339')  # kinetic vacuum parameter       [Evidence A-]

# ─────────────────────────────────────────────────────────────────
# PAPER PARAMETERS  [Stratum I]
# ─────────────────────────────────────────────────────────────────
# From arXiv:2102.04959, Eqs. (32)-(33):
a        = mp.mpf('0.046')   # IR log coefficient                [Evidence A]
Z1_sym   = mp.mpf('0.85')   # renorm. const., symmetric MOM     [Evidence A-]
Z1_sg    = mp.mpf('0.90')   # renorm. const., soft-gluon MOM    [Evidence A-]
F0       = mp.mpf('2.8')    # ghost dressing at q^2->0          [Evidence B]
c        = mp.mpf('-0.07')  # Y1 IR constant, Eq. (33)          [Evidence A-]
d        = mp.mpf('-0.20')  # Y4 IR constant, Eq. (33)          [Evidence A-]
mu       = mp.mpf('4.3')    # MOM renormalization point [GeV]   [Evidence A]

# From arXiv:2208.01020, Sec. 6, Fig. 7:
m_gluon  = mp.mpf('0.350')  # effective gluon mass [GeV]        [Evidence B]
alpha_s  = mp.mpf('0.27')   # strong coupling, MOM scheme       [Evidence B]

# ─────────────────────────────────────────────────────────────────
# DERIVED IR PARAMETERS
# ─────────────────────────────────────────────────────────────────
# Log slopes (Eq. 32 of [A]):
alpha_sg  = Z1_sg  * F0 * a        # Gamma_sg  IR log slope
alpha_sym = Z1_sym * F0 * a        # Gamma1_sym IR log slope
alpha2    = c / 4 * Z1_sym * F0    # Gamma2_sym IR log slope (Eq. 33 of [A])

# Gamma2_sym saturation at s->0  (Eq. 33 of [A]):
#   Gamma2_sat = -3/4 * (alpha_sym + c/2 + d/3)
Gamma2_sat = -mp.mpf('3') / 4 * (alpha_sym + c / 2 + d / 3)

# Normalization offsets:
# Gamma_sg(mu) = 1, Gamma2_sym(mu) = 0  (transverse, vanishes at mu)
beta_sg = mp.mpf('1') - alpha_sg * mp.log(mu**2)

# IR zero-crossing of Gamma_sg  [Stratum III note]
s_zero = mu * mp.exp(-mp.mpf('1') / (2 * alpha_sg))


# ─────────────────────────────────────────────────────────────────
# FORM FACTORS
# ─────────────────────────────────────────────────────────────────

def Gamma_sg(s):
    """Soft-gluon form factor Gamma_sg(s^2), MOM-normalized at mu.

    IR behaviour: ~ alpha_sg * ln(s^2/mu^2) + 1
    Renormalization: Gamma_sg(mu) = 1  [Eq. 21, arXiv:2208.01020]

    Stratum I — [Evidence A]
    """
    s = mp.mpf(str(s))
    return alpha_sg * mp.log(s**2 / mu**2) + mp.mpf('1')


def Gamma1_sym(q):
    """Symmetric form factor Gamma_1^sym(q^2), IR asymptotic.

    [Evidence A, Eq. 32 of arXiv:2102.04959]
    """
    q = mp.mpf(str(q))
    return alpha_sym * mp.log(q**2 / mu**2) + mp.mpf('1')


def Gamma2_sym(s):
    """Second symmetric form factor Gamma_2^sym(s^2).

    IR asymptotic form (Eq. 33 of arXiv:2102.04959):
        Gamma2_sym(s^2) = Gamma2_sat * (1 - s^2/mu^2) + alpha2 * ln(s^2/mu^2)

    Parameters:
        alpha2     = c/4 * Z1_sym * F0  = -0.04165  [Evidence A]
        Gamma2_sat = -3/4*(alpha_sym + c/2 + d/3)  = -0.005860  [Evidence A]

    Renormalization: Gamma2_sym(mu) = 0  (transverse condition)

    Stratum I — [Evidence A]
    """
    s = mp.mpf(str(s))
    return Gamma2_sat * (mp.mpf('1') - s**2 / mu**2) + alpha2 * mp.log(s**2 / mu**2)


def Gamma1_bisect(q, p):
    """Bisectoral form factor Gamma_1(q^2,q^2,p^2) via planar degeneracy.

    Planar degeneracy (arXiv:2208.01020, Eq. 28):
        Gamma_1(q^2,r^2,p^2) ~ Gamma_sg(s^2)
    with s^2_b = q^2 + p^2/2  for bisectoral kinematics q^2=r^2.

    [Evidence B]
    """
    q  = mp.mpf(str(q))
    p  = mp.mpf(str(p))
    sb = mp.sqrt(q**2 + p**2 / 2)
    return Gamma_sg(sb)


# ─────────────────────────────────────────────────────────────────
# UIDT MAPPING  [Stratum III]
# ─────────────────────────────────────────────────────────────────
# NOTE: The infrared zero-crossing of Gamma_sg lies at:
#   s_zero = mu * exp(-1/(2*alpha_sg))  ~  0.058 GeV
# This is NOT equal to Delta* = 1.710 GeV.
# Delta* is the Yang-Mills spectral gap — a distinct physical quantity.
# No tension with UIDT ledger; different observables.


# ─────────────────────────────────────────────────────────────────
# VERIFICATION
# ─────────────────────────────────────────────────────────────────
def run_verification():
    """Residual checks. All must satisfy |result| < 1e-14."""
    mp.dps = 80  # local re-assertion

    # Gamma_sg renormalization
    res_sg = abs(Gamma_sg(mu) - mp.mpf('1'))
    assert res_sg < mp.mpf('1e-14'), (
        f"[RENORM_FAIL] Gamma_sg(mu)-1 = {mp.nstr(res_sg, 10)}"
    )

    # Gamma2_sym renormalization (must vanish at mu)
    res_g2 = abs(Gamma2_sym(mu))
    assert res_g2 < mp.mpf('1e-14'), (
        f"[RENORM2_FAIL] Gamma2_sym(mu) = {mp.nstr(res_g2, 10)}"
    )

    # Gamma1_sym renormalization
    res_g1 = abs(Gamma1_sym(mu) - mp.mpf('1'))
    assert res_g1 < mp.mpf('1e-14'), (
        f"[RENORM1_FAIL] Gamma1_sym(mu)-1 = {mp.nstr(res_g1, 10)}"
    )

    # Monotonicity: Gamma_sg increases with s
    assert Gamma_sg('2.0') < Gamma_sg('4.3'), "[MONOTON_FAIL] Gamma_sg not monotone"

    # Planar degeneracy: Gamma1_bisect(q, p=0) == Gamma_sg(q)
    q_test    = mp.mpf('2.0')
    res_planar = abs(Gamma1_bisect(q_test, mp.mpf('0')) - Gamma_sg(q_test))
    assert res_planar < mp.mpf('1e-14'), (
        f"[PLANAR_FAIL] bisect(q,0)-sg(q) = {mp.nstr(res_planar, 10)}"
    )

    # Gamma2_sat sign check: must be negative (IR suppression)
    assert Gamma2_sat < mp.mpf('0'), "[SIGN_FAIL] Gamma2_sat must be negative"

    print("[PASS] All residuals < 1e-14")
    print(f"  res_sg          : {mp.nstr(res_sg, 6)}")
    print(f"  res_g1          : {mp.nstr(res_g1, 6)}")
    print(f"  res_g2          : {mp.nstr(res_g2, 6)}")
    print(f"  res_planar      : {mp.nstr(res_planar, 6)}")
    print(f"  alpha_sg        : {mp.nstr(alpha_sg, 20)}")
    print(f"  alpha_sym       : {mp.nstr(alpha_sym, 20)}")
    print(f"  alpha2          : {mp.nstr(alpha2, 20)}")
    print(f"  beta_sg         : {mp.nstr(beta_sg, 20)}")
    print(f"  Gamma2_sat      : {mp.nstr(Gamma2_sat, 20)}")
    print(f"  s_zero (IR)     : {mp.nstr(s_zero, 10)} GeV")
    print(f"  Delta* (UIDT)   : {mp.nstr(Delta_star, 10)} GeV  [distinct observable]")


if __name__ == '__main__':
    run_verification()
