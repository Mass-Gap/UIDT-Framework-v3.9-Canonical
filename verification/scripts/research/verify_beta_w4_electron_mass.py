import mpmath as mp

# Ensure local precision
mp.mp.dps = 80

def analyze_electron_mass_residual():
    # Ledger constants [A] and [A-]
    m_e_PDG = mp.mpf('0.51099895')  # MeV [A, PDG]
    delta_star = mp.mpf('1710')     # MeV [A]
    gamma = mp.mpf('16.339')        # [A-]

    # 1. Baseline Calculation
    m_e_UIDT = delta_star / (gamma**3)

    residual_abs = abs(m_e_UIDT - m_e_PDG)
    residual_rel = (residual_abs / m_e_PDG) * mp.mpf('100')

    print(f"UIDT Predicted m_e: {mp.nstr(m_e_UIDT, 8)} MeV")
    print(f"PDG Observed m_e:   {mp.nstr(m_e_PDG, 8)} MeV")
    print(f"Baseline Residual:  {mp.nstr(residual_rel, 6)} %\n")

    # 2. QED Radiative Correction
    alpha_em = mp.mpf('1') / mp.mpf('137.036')
    lambda_UV = delta_star

    # Leading QED self-energy correction (multiplicative)
    delta_m_QED = m_e_UIDT * (mp.mpf('3') * alpha_em / (mp.mpf('4') * mp.pi)) * mp.log(lambda_UV / m_e_PDG)
    m_e_QED_corr = m_e_UIDT + delta_m_QED

    residual_QED_abs = abs(m_e_QED_corr - m_e_PDG)
    residual_QED_rel = (residual_QED_abs / m_e_PDG) * mp.mpf('100')

    print(f"delta_m_QED:        {mp.nstr(delta_m_QED, 8)} MeV")
    print(f"QED Corrected m_e:  {mp.nstr(m_e_QED_corr, 8)} MeV")
    print(f"QED Residual:       {mp.nstr(residual_QED_rel, 6)} %\n")

    # 3. Weak Isospin Projection (from verify_electroweak_mixing.py)
    # The framework hints at m_e^UIDT = m_e^obs * cos^2(theta_W) or similar
    sin2_theta_w = mp.mpf('0.23122')
    cos2_theta_w = mp.mpf('1') - sin2_theta_w

    # m_e_UIDT is the "bare" vacuum projection. The physical mass includes the weak mixing.
    m_e_EW = m_e_UIDT / cos2_theta_w

    residual_EW_abs = abs(m_e_EW - m_e_PDG)
    residual_EW_rel = (residual_EW_abs / m_e_PDG) * mp.mpf('100')

    print(f"EW Corrected m_e:   {mp.nstr(m_e_EW, 8)} MeV")
    print(f"EW Residual:        {mp.nstr(residual_EW_rel, 6)} %\n")

if __name__ == "__main__":
    analyze_electron_mass_residual()
