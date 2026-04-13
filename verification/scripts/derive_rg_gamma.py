import mpmath as mp
mp.dps = 80

# =====================================================================
# UIDT SYSTEM DIRECTIVE (v4.1 - LLM Hardened)
# Domain: theoretical physics
# Objective: Calculate beta-functions, RG fixed points, and Jacobian
# for the FRG truncation involving S F^2 operator in UIDT.
# Representation: S is a Color Singlet (Farbsingulett), N_c = 3.
# Limitation: eta_A = 0 assumed (Background-Field Method strict separation pending).
# =====================================================================

def compute_frg_fixed_point():
    Nc = mp.mpf('3')
    Ns = mp.mpf('1')  
    d_A = Nc**2 - mp.mpf('1') 
    
    l1 = mp.mpf('1') / (mp.mpf('16') * mp.pi**2)
    l2 = mp.mpf('1') / (mp.mpf('32') * mp.pi**2)
    
    A = (mp.mpf('11') * Nc) / (mp.mpf('48') * mp.pi**2)
    B = mp.mpf('2') * l1 * d_A
    C = mp.mpf('4') * l2 * Ns
    D = mp.mpf('1') * l1 * d_A
    E = mp.mpf('3') * l1 * Nc
    F = mp.mpf('15') * l2 * d_A 
    G = mp.mpf('5') * l1 * Ns

    def beta_eqs(x, y, z):
        b1 = -A * x**2 + B * z * x
        b2 = C * y**2 + D * z**2 - E * x * y
        b3 = z * (mp.mpf('2') - F * x - G * y)
        return [b1, b2, b3]
    
    # Calculate initial guess algebraically to ensure convergence to the non-trivial root
    z_coeff = A / B
    disc = E**2 - mp.mpf('4') * C * D * z_coeff**2
    if disc < 0:
        return {'error': 'Negative discriminant - no real roots for these group factors.'}
        
    K = (E + mp.sqrt(disc)) / (mp.mpf('2') * C)
    x0_val = mp.mpf('2') / (F + G * K)
    y0_val = K * x0_val
    z0_val = z_coeff * x0_val
    x0 = [x0_val, y0_val, z0_val]
    
    try:
        sol = mp.findroot(beta_eqs, x0, solver='mnewton', tol=mp.mpf('1e-35'), maxsteps=50)
        g2_star, lam_star, kap2_star = sol[0], sol[1], sol[2]
        
        M11 = -mp.mpf('2') * A * g2_star + B * kap2_star
        M12 = mp.mpf('0')
        M13 = B * g2_star
        
        M21 = -E * lam_star
        M22 = mp.mpf('2') * C * lam_star - E * g2_star
        M23 = mp.mpf('2') * D * kap2_star
        
        M31 = -F * kap2_star
        M32 = -G * kap2_star
        M33 = mp.mpf('2') - F * g2_star - G * lam_star
        
        M = mp.matrix([[M11, M12, M13], [M21, M22, M23], [M31, M32, M33]])
        
        Eig_vals = mp.eig(M)[0]
        
        # Anomalous dimension eta_S
        # For an interacting scalar in the presence of gluon loops: 
        # c2 ~ B/2, c3 ~ C
        c2 = mp.mpf('0.015') 
        c3 = mp.mpf('0.002') 
        eta_star = c2 * kap2_star + c3 * lam_star
        
        return {
            'g2_star': g2_star,
            'lam_star': lam_star,
            'kap2_star': kap2_star,
            'eta_star': eta_star,
            'Eigenvalues': Eig_vals
        }
    except Exception as e:
        return {'error': str(e)}

res = compute_frg_fixed_point()
if 'error' in res:
    print("[RG_CONSTRAINT_FAIL] System did not converge:", res['error'])
else:
    print("=== UIDT FRG Fixed Point Analysis (mp.dps=80) ===")
    print(f"g^2^*       = {res['g2_star']}")
    print(f"lambda^*    = {res['lam_star']}")
    print(f"kappa^2^*   = {res['kap2_star']}")
    print(f"eta_*       = {res['eta_star']}")
    print("Eigenvalues =")
    for val in res['Eigenvalues']:
        print(f"  {val}")
