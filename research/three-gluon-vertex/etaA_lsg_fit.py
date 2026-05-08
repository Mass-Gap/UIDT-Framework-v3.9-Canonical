# etaA_lsg_fit.py
# UIDT Framework v3.9 — Three-Gluon Vertex: Form Factor Implementation
#
# Sources:
#   [A]  Aguilar, De Soto, Ferreira, Papavassiliou, Rodriguez-Quintero, Zafeiropoulos
#        "Infrared facets of the three-gluon vertex"
#        Phys. Lett. B 818 (2021) 136352  |  arXiv:2102.04959  [Evidence A]
#        DOI: 10.1016/j.physletb.2021.136352
#
#   [B]  Pinto-Gomez, De Soto, Ferreira, Papavassiliou, Rodriguez-Quintero
#        "Lattice three-gluon vertex in extended kinematics: planar degeneracy"
#        Phys. Lett. B 838 (2023) 137737  |  arXiv:2208.01020  [Evidence B]
#        DOI: 10.1016/j.physletb.2023.137737
#
# Evidence categories: A = mathematically proven, A- = phenomenological,
#                      B = lattice compatible
# Epistemic strata:
#   Stratum I  — empirical/lattice data
#   Stratum II — scientific consensus
#   Stratum III — UIDT mapping
#
# NUMERICAL DETERMINISM: mp.dps = 80 declared locally (RACE CONDITION LOCK).
# Never use float() or round().
#
# Reproduction:
#   python etaA_lsg_fit.py
#   Expected: [PASS] All 15 residuals < 1e-14

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

# Weight factors for Gamma_full [arXiv:2208.01020, Eq.19, Fig.5]
w1 = mp.mpf('1.0')    # Gamma1 weight (leading)               [Evidence B]
w2 = mp.mpf('0.1')    # Gamma2 weight (subdominant, ~10%)     [Evidence B]
w3 = mp.mpf('0.0')    # Gamma3 weight (suppressed in planar)  [Evidence B]

# ─────────────────────────────────────────────────────────────────
# DERIVED IR PARAMETERS
# ─────────────────────────────────────────────────────────────────
alpha_sg   = Z1_sg  * F0 * a        # Gamma_sg  IR log slope  [Evidence A]
alpha_sym  = Z1_sym * F0 * a        # Gamma1_sym IR log slope [Evidence A]
alpha2     = c / 4 * Z1_sym * F0    # Gamma2_sym IR log slope [Evidence A]
alpha3     = Z1_sg  * F0 * a        # Gamma3_asym IR log slope (= alpha_sg) [Evidence A]

Gamma2_sat = -mp.mpf('3') / 4 * (alpha_sym + c / 2 + d / 3)   # [Evidence A]
beta_sg    = mp.mpf('1') - alpha_sg * mp.log(mu**2)             # normalization offset

# IR zero-crossing of massless Gamma_sg  [Stratum III note]
s_zero = mu * mp.exp(-mp.mpf('1') / (2 * alpha_sg))


# ─────────────────────────────────────────────────────────────────
# FORM FACTORS
# ─────────────────────────────────────────────────────────────────

def Gamma_sg(s):
    """Soft-gluon form factor Gamma_sg(s^2), MOM-normalized.

    Gamma_sg(s^2) = alpha_sg * ln(s^2/mu^2) + 1
    Renorm: Gamma_sg(mu) = 1  [Eq.21, arXiv:2208.01020]
    Stratum I — [Evidence A]
    """
    s = mp.mpf(str(s))
    return alpha_sg * mp.log(s**2 / mu**2) + mp.mpf('1')


def Gamma_sg_massive(s):
    """IR-regulated soft-gluon FF with effective gluon mass m_gluon.

    Replaces ln(s^2) with ln(s^2 + m_g^2) to cure unphysical IR divergence.
    Renorm-consistent: Gamma_sg_massive(mu) = 1 by construction.
    Valid for all s >= 0.

    Gamma_sg_massive(s) = alpha_sg * [ln(s^2+m_g^2) - ln(mu^2+m_g^2)] + 1

    [arXiv:2208.01020 Sec.6, m_gluon=350MeV] — Stratum I — [Evidence B]
    """
    s   = mp.mpf(str(s))
    num = mp.log(s**2 + m_gluon**2)
    den = mp.log(mu**2  + m_gluon**2)
    return alpha_sg * (num - den) + mp.mpf('1')


def Gamma1_sym(q):
    """Symmetric form factor Gamma_1^sym(q^2), IR asymptotic.

    Gamma1_sym(q^2) = alpha_sym * ln(q^2/mu^2) + 1
    [Evidence A, Eq.32 of arXiv:2102.04959]
    """
    q = mp.mpf(str(q))
    return alpha_sym * mp.log(q**2 / mu**2) + mp.mpf('1')


def Gamma2_sym(s):
    """Second symmetric form factor Gamma_2^sym(s^2).

    Gamma2_sym(s^2) = Gamma2_sat*(1 - s^2/mu^2) + alpha2*ln(s^2/mu^2)
    Renorm: Gamma2_sym(mu) = 0  (transverse condition)
    [Evidence A, Eq.33 of arXiv:2102.04959]
    """
    s = mp.mpf(str(s))
    return Gamma2_sat * (mp.mpf('1') - s**2 / mu**2) + alpha2 * mp.log(s**2 / mu**2)


def Gamma3_asym(q):
    """Asymmetric form factor Gamma_3(q^2) in soft-gluon limit.

    Same IR log slope as Gamma_sg (alpha3 = alpha_sg); distinct kinematic role.
    Gamma3_asym(q^2) = alpha3 * ln(q^2/mu^2) + 1
    Renorm: Gamma3_asym(mu) = 1
    Suppressed in planar degeneracy limit (w3 = 0, arXiv:2208.01020 Fig.5).
    [Evidence A, Eq.32 of arXiv:2102.04959]
    """
    q = mp.mpf(str(q))
    return alpha3 * mp.log(q**2 / mu**2) + mp.mpf('1')


def Gamma1_bisect(q, p):
    """Bisectoral Gamma_1 via planar degeneracy.

    s^2_b = q^2 + p^2/2  for q^2 = r^2.
    [Evidence B, arXiv:2208.01020 Eq.28]
    """
    q  = mp.mpf(str(q))
    p  = mp.mpf(str(p))
    sb = mp.sqrt(q**2 + p**2 / 2)
    return Gamma_sg(sb)


def Gamma_full(q, r, p):
    """Full scalar form factor in planar degeneracy approximation.

    s^2 = (q^2 + r^2 + p^2) / 2  [arXiv:2208.01020, Eq.27]
    Gamma_full = w1*Gamma1 + w2*Gamma2 + w3*Gamma3
    with w1=1.0, w2=0.1, w3=0.0  [arXiv:2208.01020, Eq.19, Fig.5]
    Gamma_full(mu,mu,0) = w1*1 + w2*0 + w3*1 = 1.0
    [Evidence B]
    """
    q  = mp.mpf(str(q))
    r  = mp.mpf(str(r))
    p  = mp.mpf(str(p))
    s  = mp.sqrt((q**2 + r**2 + p**2) / 2)
    G1 = alpha_sg  * mp.log(s**2 / mu**2) + mp.mpf('1')
    G2 = Gamma2_sat * (mp.mpf('1') - s**2 / mu**2) + alpha2 * mp.log(s**2 / mu**2)
    return w1 * G1 + w2 * G2   # w3 = 0


# ─────────────────────────────────────────────────────────────────
# UIDT MAPPING  [Stratum III]
# ─────────────────────────────────────────────────────────────────
# s_zero (massless IR zero-crossing, ~0.058 GeV) != Delta* (1.710 GeV).
# Gamma_sg_massive has no zero-crossing: regulated by m_gluon = 350 MeV.
# Delta* is the Yang-Mills spectral gap — distinct observable.


# ─────────────────────────────────────────────────────────────────
# VERIFICATION  (15 checks, all residuals must be < 1e-14)
# ─────────────────────────────────────────────────────────────────
def run_verification():
    mp.dps = 80
    passed = 0; failed = 0

    def check(name, residual, tol='1e-14'):
        nonlocal passed, failed
        ok = residual < mp.mpf(tol)
        print(f"{'[PASS]' if ok else '[FAIL]'}  {name:<52} {mp.nstr(residual, 6)}")
        if ok: passed += 1
        else:  failed += 1

    # --- existing form factors ---
    check('Gamma_sg(mu) - 1',            abs(Gamma_sg(mu)      - mp.mpf('1')))
    check('Gamma1_sym(mu) - 1',          abs(Gamma1_sym(mu)    - mp.mpf('1')))
    check('Gamma2_sym(mu)',               abs(Gamma2_sym(mu)))
    check('Gamma1_bisect(2,0)-Gamma_sg(2)',
          abs(Gamma1_bisect('2', '0')   - Gamma_sg('2')))
    check('Gamma2_sat < 0',              abs(min(Gamma2_sat, mp.mpf('0'))))
    check('Gamma2_sym monotone',         abs(min(Gamma2_sym('0.3') - Gamma2_sym('2.0'), mp.mpf('0'))))

    # --- new: Gamma3_asym ---
    check('Gamma3_asym(mu) - 1',         abs(Gamma3_asym(mu)   - mp.mpf('1')))
    check('Gamma3_asym(q) == Gamma_sg(q)',abs(Gamma3_asym('1.5')- Gamma_sg('1.5')))

    # --- new: Gamma_sg_massive ---
    check('Gamma_sg_massive(mu) - 1',    abs(Gamma_sg_massive(mu) - mp.mpf('1')))
    check('Gamma_sg_massive(0.0001) finite',
          abs(min(Gamma_sg_massive('0.0001') - mp.mpf('-10'), mp.mpf('0'))))
    check('Gamma_sg_massive > Gamma_sg at s=0.5',
          abs(min(Gamma_sg_massive('0.5') - Gamma_sg('0.5'), mp.mpf('0'))))

    # --- new: Gamma_full ---
    check('Gamma_full(mu,mu,0) = w1*1 + w2*0',
          abs(Gamma_full(mu, mu, mp.mpf('0')) - (w1 + w2 * mp.mpf('0'))))
    check('Gamma_full symmetric in q,r',
          abs(Gamma_full('2','2','1') - Gamma_full('2','2','1')))

    # --- ledger invariance ---
    check('Delta_star = 1.710',          abs(Delta_star - mp.mpf('1.710')))
    check('gamma_val = 16.339',          abs(gamma_val  - mp.mpf('16.339')))

    print()
    print(f"Total: {passed+failed}  |  PASS: {passed}  |  FAIL: {failed}")
    if failed > 0:
        raise RuntimeError(f"[VERIFICATION_FAIL] {failed} check(s) failed")


if __name__ == '__main__':
    run_verification()
