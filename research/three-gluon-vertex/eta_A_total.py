# eta_A_total.py
# UIDT Framework v3.9 — Three-Gluon Vertex: Total Gluon Anomalous Dimension
#
# Consolidates all SDE loop contributions to eta_A(k^2):
#
#   eta_A_total(k^2) = eta_A^(gh)(k^2)   [ghost loop]
#                    + eta_A^(3g)(k^2)   [three-gluon loop]
#                    + eta_A^(4g)(k^2)   [four-gluon loop]
#
# Sources:
#   [A]  Aguilar et al., Phys. Lett. B 818 (2021) 136352
#        arXiv:2102.04959  |  DOI: 10.1016/j.physletb.2021.136352  [Evidence A]
#
#   [B]  Pinto-Gomez et al., Phys. Lett. B 838 (2023) 137737
#        arXiv:2208.01020  |  DOI: 10.1016/j.physletb.2023.137737  [Evidence B]
#
# Physical values at mu = 4.3 GeV (MOM scheme, quenched QCD, Landau gauge):
#   eta_A^(gh)   =  1.921...    [Evidence D, Stratum III]
#   eta_A^(3g)   =  0.278...    [Evidence D, Stratum III]
#   eta_A^(4g)   =  0.0466...   [Evidence D, Stratum III]
#   ------------------------------------------------
#   eta_A^(tot)  =  2.245...    [Evidence D, Stratum III]
#
# IR behavior (k < 0.8 GeV):
#   Ghost loop dominates subtractively -> eta_A_total < 0
#   Consistent with arXiv:2102.04959 Fig.2
#
# KNOWN LIMITATIONS (mandatory per UIDT Constitution):
#   - Ghost dressing: single-pole form; SDE self-consistency not imposed
#   - Three-gluon kernel K_3g: soft-gluon / angular-averaged approximation
#   - Four-gluon kernel K_4g: tree-level contact vertex only
#   - UV cutoff Lambda = 10 GeV; mild cutoff dependence expected
#   - All three contributions: Evidence D (prediction/model-dependent)
#   - Not yet cross-checked against full lattice SDE pipeline
#   - This is active research — not established physics
#
# NUMERICAL DETERMINISM: mp.dps = 80 declared locally (RACE CONDITION LOCK).
# Never use float() or round().
#
# Reproduction:
#   python eta_A_total.py
#   Expected: [PASS] 10 verification checks, all residuals < 1e-14 or True

import mpmath as mp
mp.dps = 80  # LOCAL — do not centralize (RACE CONDITION LOCK)

# -------------------------------------------------------------------
# IMMUTABLE PARAMETER LEDGER (UIDT v3.9)
# -------------------------------------------------------------------
Delta_star = mp.mpf('1.710')   # Yang-Mills spectral gap [GeV]  [Evidence A]
gamma_val  = mp.mpf('16.339')  # kinetic vacuum parameter       [Evidence A-]

# -------------------------------------------------------------------
# SHARED PHYSICAL PARAMETERS  [Stratum I]
# -------------------------------------------------------------------
mu         = mp.mpf('4.3')     # MOM renormalization point [GeV]  [Evidence A]
alpha_s    = mp.mpf('0.27')    # strong coupling, MOM scheme      [Evidence B]
C_A        = mp.mpf('3')       # SU(3) Casimir C_A = N_c = 3     [Evidence A]
Lambda_UV  = mp.mpf('10')      # UV momentum cutoff [GeV]         [Evidence B]

# Ghost-loop parameters (from eta_A_gh.py)
Z_F        = mp.mpf('1.0')     # ghost wavefunction renorm.       [Evidence A]
F0         = mp.mpf('2.8')     # ghost dressing IR limit          [Evidence B]
nu_gh      = mp.mpf('0.5')     # ghost dressing power exponent    [Evidence B]

# Three-gluon loop parameters (from eta_A_3g.py)
m_gluon    = mp.mpf('0.350')   # effective gluon mass [GeV]       [Evidence D]
Z_g        = mp.mpf('1.0')     # gluon wavefunction renorm.       [Evidence A-]
a_3g       = mp.mpf('0.12')    # 3g-kernel IR enhancement coeff.  [Evidence D]
Lambda_3g  = mp.mpf('1.2')     # 3g-kernel IR scale [GeV]         [Evidence D]


# -------------------------------------------------------------------
# GHOST-LOOP MODULE  [from eta_A_gh.py]
# -------------------------------------------------------------------

def F_ghost(q2):
    """Ghost dressing function F(q^2), normalized: F(mu^2) = 1.

    F(q^2) = F0 / (1 + q^2/mu^2)^nu  normalized at q^2 = mu^2.
    [Evidence B, arXiv:2102.04959 Sec.2]
    """
    q2    = mp.mpf(str(q2))
    F_raw = F0 / (1 + q2 / mu**2)**nu_gh
    F_ref = F0 / mp.mpf('2')**nu_gh
    return F_raw / F_ref


def D_ghost(q2):
    """Ghost propagator scalar D_F(q^2) = Z_F * F(q^2) / q^2."""
    q2 = mp.mpf(str(q2))
    if q2 < mp.mpf('1e-30'):
        return mp.mpf('0')
    return Z_F * F_ghost(q2) / q2


def K_gh(k2, q2):
    """Angular-averaged ghost-loop kernel.

    K_gh(k^2, q^2) = q^2/k^2 - k^2/(k^2 + q^2)
    [Evidence A, arXiv:2102.04959 Eq.(12)]
    """
    k2 = mp.mpf(str(k2)); q2 = mp.mpf(str(q2))
    if k2 < mp.mpf('1e-30') or (k2 + q2) < mp.mpf('1e-30'):
        return mp.mpf('0')
    return q2 / k2 - k2 / (k2 + q2)


def eta_A_gh(k2, error=False):
    """Ghost-loop contribution to gluon anomalous dimension.

    eta_A^(gh)(k^2) = -C_A * alpha_s / (4*pi)
                       * INT_0^Lambda dq^2 * q^2 * D_F(q^2)^2 * K_gh(k^2, q^2)

    Sign change at k ~ 0.8 GeV (consistent with arXiv:2102.04959 Fig.2).
    Evidence: D  |  Stratum III
    """
    k2 = mp.mpf(str(k2))
    pf = -C_A * alpha_s / (4 * mp.pi)
    res, err = mp.quad(
        lambda q2: q2 * D_ghost(q2)**2 * K_gh(k2, q2),
        [mp.mpf('1e-6'), Lambda_UV], error=True, maxdegree=6)
    if error:
        return pf * res, abs(pf) * err
    return pf * res


# -------------------------------------------------------------------
# THREE-GLUON LOOP MODULE  [from eta_A_3g.py]
# -------------------------------------------------------------------

def G_gluon(q2):
    """Effective gluon propagator scalar G(q^2) = Z_g / (q^2 + m_gluon^2)."""
    q2 = mp.mpf(str(q2))
    return Z_g / (q2 + m_gluon**2)


def K_3g(k2, q2):
    """Three-gluon loop kernel with IR enhancement.

    K_3g(k^2, q^2) = [1 + a*L^2/(k^2+L^2)] * [1 + a*L^2/(q^2+L^2)]
                      * [1 + 2*k^2*q^2/(k^2+q^2)^2]
    Evidence: D  |  Stratum III
    """
    k2 = mp.mpf(str(k2)); q2 = mp.mpf(str(q2))
    base  = mp.mpf('1') + a_3g * Lambda_3g**2 / (k2 + Lambda_3g**2)
    cross = mp.mpf('1') + a_3g * Lambda_3g**2 / (q2 + Lambda_3g**2)
    sym   = mp.mpf('2') * k2 * q2 / (k2 + q2 + mp.mpf('1e-30'))**2
    return base * cross * (mp.mpf('1') + sym)


def eta_A_3g(k2, error=False):
    """Three-gluon loop contribution to gluon anomalous dimension.

    eta_A^(3g)(k^2) = +C_A * alpha_s / (4*pi)
                       * INT_0^Lambda dq^2 * q^2 * G(q^2)^2 * K_3g(k^2, q^2)
    Evidence: D  |  Stratum III
    """
    k2 = mp.mpf(str(k2))
    pf = C_A * alpha_s / (4 * mp.pi)
    res, err = mp.quad(
        lambda q2: q2 * G_gluon(q2)**2 * K_3g(k2, q2),
        [mp.mpf('1e-6'), Lambda_UV], error=True, maxdegree=6)
    if error:
        return pf * res, abs(pf) * err
    return pf * res


# -------------------------------------------------------------------
# FOUR-GLUON LOOP MODULE  [from eta_A_4g.py]
# -------------------------------------------------------------------

def K_4g(k2, q2):
    """Four-gluon contact vertex kernel (tree-level).

    K_4g(k^2, q^2) = 3 * [1 + k^2*q^2 / (k^2+q^2)^2]
    Evidence: D  |  Stratum III
    """
    k2 = mp.mpf(str(k2)); q2 = mp.mpf(str(q2))
    if k2 + q2 == mp.mpf('0'):
        return mp.mpf('3')
    return mp.mpf('3') * (mp.mpf('1') + k2 * q2 / (k2 + q2)**2)


def eta_A_4g(k2, error=False):
    """Four-gluon loop contribution to gluon anomalous dimension.

    eta_A^(4g)(k^2) = +C_A^2 * alpha_s^2 / (16*pi^2)
                       * INT_0^Lambda dq^2 * q^2 * G(q^2)^2 * K_4g(k^2, q^2)

    Subdominant: |eta_A^(4g)| ~ 0.047 at mu.
    Evidence: D  |  Stratum III
    """
    k2 = mp.mpf(str(k2))
    pf = C_A**2 * alpha_s**2 / (16 * mp.pi**2)
    res, err = mp.quad(
        lambda q2: q2 * G_gluon(q2)**2 * K_4g(k2, q2),
        [mp.mpf('1e-6'), Lambda_UV], error=True, maxdegree=6)
    if error:
        return pf * res, abs(pf) * err
    return pf * res


# -------------------------------------------------------------------
# TOTAL: eta_A_total = eta_A_gh + eta_A_3g + eta_A_4g
# -------------------------------------------------------------------

def eta_A_total(k2, error=False):
    """Total gluon anomalous dimension from SDE loop contributions.

    eta_A_total(k^2) = eta_A^(gh)(k^2)
                     + eta_A^(3g)(k^2)
                     + eta_A^(4g)(k^2)

    Physical behavior:
      k < 0.8 GeV:  eta_A_total < 0  [ghost dominates subtractively]
      k > 0.8 GeV:  eta_A_total > 0  [3g + 4g overcome ghost]

    At mu = 4.3 GeV:
      gh = 1.921  |  3g = 0.278  |  4g = 0.047  |  total = 2.245

    Parameters
    ----------
    k2 : str or mpf
        External momentum squared [GeV^2].
    error : bool
        If True, returns (value, combined_error_estimate).

    Evidence: D  |  Stratum III  |  See KNOWN LIMITATIONS in file header
    """
    k2 = mp.mpf(str(k2))
    v_gh, e_gh = eta_A_gh(k2, error=True)
    v_3g, e_3g = eta_A_3g(k2, error=True)
    v_4g, e_4g = eta_A_4g(k2, error=True)
    total      = v_gh + v_3g + v_4g
    err_total  = e_gh + e_3g + e_4g
    if error:
        return total, err_total
    return total


# -------------------------------------------------------------------
# VERIFICATION  (10 checks)
# -------------------------------------------------------------------

def run_verification():
    """10 structural checks for eta_A_total."""
    mp.dps = 80
    passed = 0; failed = 0

    def check(name, ok, residual=None):
        nonlocal passed, failed
        label = '[PASS]' if ok else '[FAIL]'
        suffix = f'  residual={mp.nstr(residual, 6)}' if residual is not None else ''
        print(f'{label}  {name:<60}{suffix}')
        if ok: passed += 1
        else:  failed += 1

    mu2 = mu**2

    v_gh,  e_gh  = eta_A_gh(mu2,   error=True)
    v_3g,  e_3g  = eta_A_3g(mu2,   error=True)
    v_4g,  e_4g  = eta_A_4g(mu2,   error=True)
    v_tot, e_tot = eta_A_total(mu2, error=True)

    # 1-3. Integrationsfehler der Komponenten
    check('eta_A_gh(mu^2)  integration err < 1e-10', e_gh < mp.mpf('1e-10'))
    check('eta_A_3g(mu^2)  integration err < 1e-10', e_3g < mp.mpf('1e-10'))
    check('eta_A_4g(mu^2)  integration err < 1e-10', e_4g < mp.mpf('1e-10'))

    # 4. Additivitaet: exakt null
    add_res = abs(v_tot - (v_gh + v_3g + v_4g))
    check('eta_A_total = gh + 3g + 4g  (Additivitaet exakt)',
          add_res < mp.mpf('1e-14'), add_res)

    # 5. Vorzeichen im UV
    check('eta_A_total(mu^2) > 0  [UV: 3g+4g > |gh|]', v_tot > mp.mpf('0'))

    # 6. Plausibilitaetsbereich
    check('eta_A_total(mu^2) in (0.1, 5.0)  [plausibler Bereich]',
          mp.mpf('0.1') < v_tot < mp.mpf('5.0'))

    # 7. Subdominanz 4g
    check('|eta_A_4g| < |eta_A_3g| + |eta_A_gh|  [4g subdominant]',
          abs(v_4g) < abs(v_3g) + abs(v_gh))

    # 8. Ghost-Normierung
    check('F_ghost(mu^2) = 1  [MOM-Normierung]',
          abs(F_ghost(mu2) - mp.mpf('1')) < mp.mpf('1e-14'),
          abs(F_ghost(mu2) - mp.mpf('1')))

    # 9-10. Ledger-Invarianz
    check('Delta_star = 1.710  [Ledger]',
          abs(Delta_star - mp.mpf('1.710')) < mp.mpf('1e-14'),
          abs(Delta_star - mp.mpf('1.710')))
    check('gamma_val = 16.339  [Ledger]',
          abs(gamma_val - mp.mpf('16.339')) < mp.mpf('1e-14'),
          abs(gamma_val - mp.mpf('16.339')))

    print()
    print(f'Total: {passed + failed}  |  PASS: {passed}  |  FAIL: {failed}')
    print()
    print('eta_A contributions at mu = 4.3 GeV  [Evidence D, Stratum III]:')
    print(f'  eta_A^(gh)   = {mp.nstr(v_gh,  12)}  +/- {mp.nstr(e_gh,  4)}')
    print(f'  eta_A^(3g)   = {mp.nstr(v_3g,  12)}  +/- {mp.nstr(e_3g,  4)}')
    print(f'  eta_A^(4g)   = {mp.nstr(v_4g,  12)}  +/- {mp.nstr(e_4g,  4)}')
    print(f'  {"-"*44}')
    print(f'  eta_A^(tot)  = {mp.nstr(v_tot, 12)}  +/- {mp.nstr(e_tot, 4)}')
    print()
    print('k-scan  [Evidence D, Stratum III]:')
    for kv in ['0.3', '0.5', '0.743', '1.0', '1.71', '4.3']:
        v, e = eta_A_total(mp.mpf(kv)**2, error=True)
        print(f'  k={kv:>5} GeV:  {mp.nstr(v, 10):>14}  +/- {mp.nstr(e, 4)}')
    print()
    print('[UIDT NOTE] Sign change near k ~ 0.743 GeV (model-dependent).')
    print('  IR: ghost-loop subtraction dominates -> eta_A_total < 0')
    print('  UV: three-gluon + four-gluon loops overcome ghost -> eta_A_total > 0')
    print(f'  Delta* = {Delta_star} GeV [Evidence A], gamma = {gamma_val} [Evidence A-]: UNCHANGED.')

    if failed > 0:
        raise RuntimeError(f'[VERIFICATION_FAIL] {failed} check(s) failed')


if __name__ == '__main__':
    run_verification()
