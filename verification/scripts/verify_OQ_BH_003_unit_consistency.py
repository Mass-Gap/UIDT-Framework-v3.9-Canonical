import mpmath as mp
import sys

mp.dps = 80

def verify_oq_bh_003():
    print("--- OQ-BH-003 Unit Consistency Check ---")
    
    # Constants
    xi_S = mp.mpf('1') / mp.mpf('6')
    m_S = mp.mpf('1.710')  # GeV
    M_Pl = mp.mpf('1.220910e19')  # GeV
    
    # Pre-factor: (96 xi_S)^(1/6) / 2
    factor1 = (mp.mpf('96') * xi_S)**(mp.mpf('1')/mp.mpf('6')) / mp.mpf('2')
    
    # Mass hierarchy factor: (M_Pl / m_S)^(1/3)
    factor2 = (M_Pl / m_S)**(mp.mpf('1')/mp.mpf('3'))
    
    hierarchy_val = factor1 * factor2
    
    print(f"Hierarchy constant C = {mp.nstr(hierarchy_val, 6)}")
    
    # Check for Astrophysical Black Hole
    # M_sun in GeV ~ 1.115e57 GeV
    M_sun_GeV = mp.mpf('1.115e57')
    M_astrophysical = mp.mpf('10') * M_sun_GeV
    
    mu_astro = M_astrophysical / M_Pl
    ratio_astro = hierarchy_val * (mu_astro)**(mp.mpf('-2')/mp.mpf('3'))
    
    print(f"For 10 Solar Mass BH (mu = {mp.nstr(mu_astro, 6)}):")
    print(f"rc / rS = {mp.nstr(ratio_astro, 6)}")
    
    if ratio_astro < 1:
        print("=> rc << rS. Condensation happens FAR INSIDE the horizon.")
        print("=> Natural units confirm C-070 constraint holds.")
    else:
        print("=> rc >> rS. Condensation happens OUTSIDE the horizon.")
        print("=> C-070 scope widens.")

if __name__ == '__main__':
    verify_oq_bh_003()
