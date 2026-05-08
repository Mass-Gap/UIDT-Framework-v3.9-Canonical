import mpmath as mp

def main():
    mp.mp.dps = 80

    # Glueball mass from UIDT: m_G ~ 2*Δ*
    m_G_UIDT = 2 * mp.mpf('1.710')  # = 3.420 GeV [D]
    m_G_lattice = mp.mpf('2.56')    # lightest scalar glueball lattice prediction

    # Compare to experimental candidates
    m_X2370 = mp.mpf('2.370')       # GeV
    m_f2100 = mp.mpf('2.100')       # GeV

    for m_exp, name in [(m_X2370, 'X(2370)'), (m_f2100, 'f₀(2100)')]:
        diff = abs(m_G_UIDT - m_exp)
        print(f"{name}: |m_UIDT - m_exp| = {mp.nstr(diff, 6)} GeV")

if __name__ == '__main__':
    main()
