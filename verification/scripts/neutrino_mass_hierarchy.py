import mpmath
from mpmath import mp

# Set precision
mp.dps = 80

def calculate_neutrino_masses():
    # Constants (eV^2)
    delta_m21_sq = mp.mpf('7.53e-5')
    delta_m32_sq_NH = mp.mpf('2.453e-3')
    delta_m32_sq_IH = mp.mpf('2.546e-3')  # Magnitude

    print("--- Neutrino Mass Hierarchy Analysis ---")
    print(f"Delta m21^2: {delta_m21_sq}")
    print(f"|Delta m32^2| (NH): {delta_m32_sq_NH}")
    print(f"|Delta m32^2| (IH): {delta_m32_sq_IH}")
    print("-" * 40)

    # Target sum range
    sum_min = mp.mpf('0.12')
    sum_max = mp.mpf('0.16')

    # Normal Hierarchy (NH)
    # m1 < m2 < m3
    # m2 = sqrt(m1^2 + delta_m21^2)
    # m3 = sqrt(m2^2 + delta_m32^2)

    print("\n--- Normal Hierarchy (NH) ---")
    print(f"Checking for sum in [{sum_min}, {sum_max}] eV")

    found_nh = False
    m_lightest_nh = mp.mpf('0.0')
    step = mp.mpf('0.0001')

    while m_lightest_nh < 0.1:
        m1 = m_lightest_nh
        m2 = mp.sqrt(m1**2 + delta_m21_sq)
        m3 = mp.sqrt(m2**2 + delta_m32_sq_NH)
        total_mass = m1 + m2 + m3

        if sum_min <= total_mass <= sum_max:
            if not found_nh:
                print(f"Match found! m_lightest: {m1} eV -> Sum: {total_mass} eV")
                found_nh = True
            # Keep searching to find the upper bound of m_lightest
            max_m_lightest_nh = m1
            max_sum_nh = total_mass

        m_lightest_nh += step

    if found_nh:
        print(f"Range of m_lightest compatible: ... to {max_m_lightest_nh} eV")
    else:
        print("No match found in search range.")


    # Inverted Hierarchy (IH)
    # m3 < m1 < m2
    # m1 = sqrt(m3^2 + delta_m32^2)  (approx, actually |Delta m32^2| = m2^2 - m3^2 ? No, usually |Delta m32| refers to large splitting)
    # Let's use standard convention:
    # m3 is lightest.
    # m1 = sqrt(m3^2 + delta_m32_sq_IH)  (large splitting)
    # m2 = sqrt(m1^2 + delta_m21_sq)

    print("\n--- Inverted Hierarchy (IH) ---")
    print(f"Checking for sum in [{sum_min}, {sum_max}] eV")

    found_ih = False
    m_lightest_ih = mp.mpf('0.0')

    while m_lightest_ih < 0.1:
        m3 = m_lightest_ih
        m1 = mp.sqrt(m3**2 + delta_m32_sq_IH) # Using delta_m32 as the atmospheric splitting
        m2 = mp.sqrt(m1**2 + delta_m21_sq)
        total_mass = m1 + m2 + m3

        if sum_min <= total_mass <= sum_max:
            if not found_ih:
                print(f"Match found! m_lightest: {m3} eV -> Sum: {total_mass} eV")
                found_ih = True
            max_m_lightest_ih = m3
            max_sum_ih = total_mass

        m_lightest_ih += step

    if found_ih:
        print(f"Range of m_lightest compatible: ... to {max_m_lightest_ih} eV")
    else:
        print("No match found in search range.")

if __name__ == "__main__":
    calculate_neutrino_masses()
