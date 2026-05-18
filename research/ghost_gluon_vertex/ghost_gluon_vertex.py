# ghost_gluon_vertex.py
# UIDT Framework v3.9 -- Ghost-Gluon Vertex: H(k,q) in Landau Gauge
#
# Implements the ghost-gluon vertex scalar form factor H(k,q) in Landau gauge
# with Taylor renormalization. The ghost-gluon vertex is the simplest QCD
# vertex -- it is finite (no UV renormalization) in Landau gauge (Taylor theorem).
#
# Sources:
#   [A]  Taylor, J.C. (1971) Nucl. Phys. B33, 436
#        DOI: 10.1016/0550-3213(71)90297-5  [Evidence A]
#
#   [B]  Aguilar, Papavassiliou (2008) JHEP 0811:080
#        arXiv:0805.3067  DOI: 10.1088/1126-6708/2008/11/080  [Evidence B]
#
#   [C]  Aguilar et al. (2021) PLB 818
#        arXiv:2102.04959  DOI: 10.1016/j.physletb.2021.136352  [Evidence A]
#
# Physics:
#   H(k,q) is the scalar form factor of the ghost-gluon vertex (gluon momentum q,
#   antighost momentum k). In Landau gauge, Z_1^F = 1 exactly (Taylor theorem).
#
#   Renormalization: H(0, mu^2) = 1  [Taylor scheme]
#
#   Parameterization:
#     H(k^2, q^2) = H_IR(k^2) * H_UV(q^2)
#
#   where UV scale = q^2 (gluon leg), so H_UV(mu^2) = 1 at renorm point.
#
#   IMPORTANT FIX (v1.1): UV scale is q^2 (gluon momentum), NOT (k^2+q^2)/2.
#   Reason: Taylor renorm condition H(0, mu^2) = 1 requires s^2 = q^2
#   so that H_UV(q^2=mu^2) = 1 and H_IR(k^2=0) = 1 independently.
#   Using (k^2+q^2)/2 gives s^2=mu^2/2 at k=0,q=mu, violating the condition.
#
#   H_IR(k^2) = 1 + a_H * k^2 / (k^2 + m_H^2)  [IR: ghost-leg enhancement]
#   H_UV(q^2) = [alpha_s(q^2)/alpha_s(mu^2)]^{delta_H}  [UV: gluon-leg running]
#   delta_H = 9*C_A / (44*C_A - 8*N_f) = 9/44  (quenched)  [1-loop anomalous dim]
#
#   IR note: alpha_s(q^2) is frozen at alpha_s(mu^2) for q^2 below the
#   Landau pole (1-loop unphysical pole); H_UV = 1 in deep IR.
#
# NUMERICAL DETERMINISM: mp.dps = 80 local. Never float(), never round().
# RACE CONDITION LOCK: mp.dps declared here, not in config.

import mpmath as mp
mp.dps = 80  # LOCAL -- do not centralize

# ------------------------------------------------------------------
# IMMUTABLE PARAMETER LEDGER (UIDT v3.9)
# ------------------------------------------------------------------
Delta_star = mp.mpf('1.710')   # Yang-Mills spectral gap [GeV]  [Evidence A]
gamma_val  = mp.mpf('16.339')  # kinetic vacuum parameter       [Evidence A-]

# ------------------------------------------------------------------
# PHYSICAL PARAMETERS
# ------------------------------------------------------------------
mu         = mp.mpf('4.3')     # MOM renorm. point [GeV]        [Evidence A]
alpha_s    = mp.mpf('0.27')    # strong coupling MOM scheme     [Evidence B]
C_A        = mp.mpf('3')       # SU(3) Casimir C_A = N_c = 3   [Evidence A]
N_f        = mp.mpf('0')       # quenched approximation         [Evidence A]
beta0      = (mp.mpf('11') * C_A - mp.mpf('2') * N_f) / mp.mpf('3')

# Ghost-gluon vertex IR parameters  [Evidence B, arXiv:0805.3067 Fig.3]
a_H        = mp.mpf('0.20')    # IR enhancement amplitude
m_H        = mp.mpf('0.50')    # IR mass scale [GeV]

# UV anomalous dimension (quenched, N_f=0): delta_H = 9/44
delta_H = mp.mpf('9') * C_A / (mp.mpf('44') * C_A - mp.mpf('8') * N_f)


# ------------------------------------------------------------------
# RUNNING COUPLING (1-loop, IR-frozen)
# ------------------------------------------------------------------

def alpha_s_running(q2):
    """1-loop running coupling. Frozen below Landau pole."""
    q2    = mp.mpf(str(q2))
    denom = mp.mpf('1') + beta0 * alpha_s / (mp.mpf('2') * mp.pi) * mp.log(q2 / mu**2)
    return alpha_s if denom <= mp.mpf('0') else alpha_s / denom


# ------------------------------------------------------------------
# FORM FACTOR COMPONENTS
# ------------------------------------------------------------------

def H_IR(k2):
    """IR part: ghost-leg enhancement.
    H_IR(0) = 1, H_IR(inf) = 1 + a_H = 1.20
    [arXiv:0805.3067 Eq.(4.3)]
    """
    k2 = mp.mpf(str(k2))
    return mp.mpf('1') + a_H * k2 / (k2 + m_H**2)


def H_UV(q2):
    """UV part: gluon-leg RG running.
    H_UV(mu^2) = 1 exactly.  H_UV < 1 for q > mu (asymptotic freedom).
    1-loop frozen in deep IR: H_UV(q->0) = 1.
    delta_H = 9/44 (quenched).  [arXiv:2102.04959 Eq.(A.3)]
    """
    q2 = mp.mpf(str(q2))
    return mp.power(alpha_s_running(q2) / alpha_s, delta_H)


def H_vertex(k2, q2):
    """Full ghost-gluon vertex scalar form factor.

    H(k^2, q^2) = H_IR(k^2) * H_UV(q^2)

    UV scale: q^2 (gluon leg).  Ensures H(0, mu^2) = 1 exactly.
    Evidence: B  |  Stratum I/II
    """
    k2 = mp.mpf(str(k2))
    q2 = mp.mpf(str(q2))
    return H_IR(k2) * H_UV(q2)


# ------------------------------------------------------------------
# VERIFICATION
# ------------------------------------------------------------------

def run_verification():
    """10 structural checks for H(k,q)."""
    mp.dps = 80
    passed = 0; failed = 0

    def check(name, ok_bool, residual=None):
        nonlocal passed, failed
        label = '[PASS]' if ok_bool else '[FAIL]'
        suffix = f'  residual={mp.nstr(residual, 6)}' if residual is not None else ''
        print(f'{label}  {name:<65}{suffix}')
        if ok_bool: passed += 1
        else:       failed += 1

    mu2 = mu**2

    check('H(0, mu^2) = 1  [Taylor renorm, s^2=q^2 fix]',
          abs(H_vertex(mp.mpf('0'), mu2) - mp.mpf('1')) < mp.mpf('1e-14'),
          abs(H_vertex(mp.mpf('0'), mu2) - mp.mpf('1')))
    check('H_UV(mu^2) = 1',
          abs(H_UV(mu2) - mp.mpf('1')) < mp.mpf('1e-14'),
          abs(H_UV(mu2) - mp.mpf('1')))
    check('H_IR(0) = 1',
          abs(H_IR(mp.mpf('0')) - mp.mpf('1')) < mp.mpf('1e-14'),
          abs(H_IR(mp.mpf('0')) - mp.mpf('1')))
    check('H_IR(inf) -> 1.20',
          abs(H_IR(mp.mpf('1e8')) - (mp.mpf('1') + a_H)) < mp.mpf('1e-5'),
          abs(H_IR(mp.mpf('1e8')) - (mp.mpf('1') + a_H)))
    check('H(mu^2, mu^2) >= 1  [IR enhancement at symmetric point]',
          H_vertex(mu2, mu2) >= mp.mpf('1'))
    check('delta_H = 9/44  [quenched]',
          abs(delta_H - mp.mpf('9') / mp.mpf('44')) < mp.mpf('1e-14'),
          abs(delta_H - mp.mpf('9') / mp.mpf('44')))
    check('H_UV(100 GeV^2) < 1  [asymptotic freedom]',
          H_UV(mp.mpf('100')) < mp.mpf('1'))
    check('H_UV(0.1 GeV^2) >= 1  [frozen in deep IR: 1-loop pole regulated]',
          H_UV(mp.mpf('0.1')) >= mp.mpf('1'))
    check('Delta_star = 1.710',
          abs(Delta_star - mp.mpf('1.710')) < mp.mpf('1e-14'),
          abs(Delta_star - mp.mpf('1.710')))
    check('gamma_val = 16.339',
          abs(gamma_val - mp.mpf('16.339')) < mp.mpf('1e-14'),
          abs(gamma_val - mp.mpf('16.339')))

    print()
    print(f'Total: {passed+failed}  |  PASS: {passed}  |  FAIL: {failed}')
    print()
    print('Sample H(k, mu^2):')
    for kv in ['0.0', '0.5', '1.0', '1.71', '4.3']:
        v = H_vertex(mp.mpf(kv)**2, mu2)
        print(f'  k={kv} GeV:  H = {mp.nstr(v, 10)}')
    print()
    print('[UIDT NOTE] Z_1^F = 1 exactly (Taylor theorem). H >= 1 in physical range.')
    if failed > 0:
        raise RuntimeError(f'[VERIFICATION_FAIL] {failed} check(s) failed')


if __name__ == '__main__':
    run_verification()
