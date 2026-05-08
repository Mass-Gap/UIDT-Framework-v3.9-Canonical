"""
UIDT MODULE: GAUGE-CONSISTENT MANIFOLD TRANSPORT (Phase 0)
==========================================================
Version: 3.9.2
Author: P. Rietz (ORCID: 0009-0007-4307-1609)
DOI: 10.5281/zenodo.17835200
Evidence Category: A (mathematical core)
Stratum: I (empirical/algebraic)

Purpose:
    This module is the formal foundation ("Gatekeeper") for any heuristic
    proposal engine (tensor networks, normalizing flows, ML accelerators)
    that interfaces with the UIDT lattice HMC simulation.

    It implements gauge-consistent manifold transport between a low-dimensional
    latent proposal space and the physical SU(3) gauge group, guaranteeing:

    1. Lie algebra closure: all perturbations lie in su(3) by construction
    2. SU(3) group membership: exact reprojection via polar decomposition
    3. Haar measure conservation: numerical drift bounded to < 10^{-10}
    4. Detailed balance: symmetrized Metropolis kernel with backward
       proposal correction Q(U' -> U) / Q(U -> U')
    5. SVD condition monitoring: kill-switch for entanglement volume
       law explosion (kappa_SVD > 10^{12} -> reject before HMC)

    Tensor networks are NOT part of the mass-gap proof (Cat. A/B).
    They are exclusively a sampling/ergodicity tool (Cat. D).
    This separation is Clay-critical.

Architecture:
    - GellMannBasis:       8 generators T^a of su(3) at 80-digit precision
    - lie_algebra_inject:  U' = exp(i*a*g * delta_A^a T^a) . U
    - project_to_su3:      Newton-Schulz polar decomposition + det normalization
    - svd_condition_check: sigma_max / sigma_min monitoring
    - MetropolisDetailedBalanceGuard: P_acc = min(1, e^{-dS} Q(U'->U)/Q(U->U'))
    - haar_measure_drift:  ||U^dag U - I|| ensemble tracking
    - topological_charge_bias: Q_top via clover discretization

References:
    - Luscher, M. (2010). Properties and uses of the Wilson flow in lattice QCD.
      JHEP 08 (2010) 071. arXiv:1006.4518
    - Luscher, M. (2010). Trivializing maps, the Wilson flow and the HMC algorithm.
      Comm. Math. Phys. 293, 899-919.
    - Duane, S. et al. (1987). Hybrid Monte Carlo. Phys. Lett. B 195, 216.
"""

from mpmath import mp, mpf, matrix, eye, sqrt, log, pi, det, fabs

# Precision MUST remain locally declared — Race Condition Lock (AGENTS.md §1)
mp.dps = 80


# =============================================================================
# 1. GELL-MANN GENERATOR BASIS
# =============================================================================

class GellMannBasis:
    """
    The 8 Gell-Mann matrices T^a = lambda^a / 2 as mpmath matrices
    at 80-digit precision.

    Normalization: Tr(T^a T^b) = delta^{ab} / 2
    Property: Each T^a is traceless and Hermitian; i*T^a is in su(3).

    Evidence Category: A (algebraic identity, exact)
    """

    def __init__(self):
        mp.dps = 80
        self._generators = self._build_generators()

    def _build_generators(self):
        """Construct the 8 Gell-Mann generators T^a = lambda^a / 2."""
        mp.dps = 80
        zero = mpf('0')
        one = mpf('1')
        half = mpf('0.5')
        inv_sqrt3 = one / sqrt(mpf('3'))

        # lambda_1
        l1 = matrix([
            [zero, one,  zero],
            [one,  zero, zero],
            [zero, zero, zero]
        ])
        # lambda_2
        l2 = matrix([
            [zero,       mpf('-1j') if False else zero, zero],
            [zero,       zero,                          zero],
            [zero,       zero,                          zero]
        ])
        # Build lambda_2 explicitly with imaginary parts
        l2 = matrix(3, 3)
        l2[0, 1] = mpf('-1') * mpf('1')  # -i -> handled below
        l2[1, 0] = mpf('1')              # +i -> handled below

        # For mpmath: we need complex matrices. mpmath handles mpc natively.
        from mpmath import mpc
        j = mpc(0, 1)

        # Rebuild all 8 generators properly with complex entries
        # lambda_1
        l1 = matrix(3, 3)
        l1[0, 1] = one
        l1[1, 0] = one

        # lambda_2
        l2 = matrix(3, 3)
        l2[0, 1] = -j
        l2[1, 0] = j

        # lambda_3
        l3 = matrix(3, 3)
        l3[0, 0] = one
        l3[1, 1] = -one

        # lambda_4
        l4 = matrix(3, 3)
        l4[0, 2] = one
        l4[2, 0] = one

        # lambda_5
        l5 = matrix(3, 3)
        l5[0, 2] = -j
        l5[2, 0] = j

        # lambda_6
        l6 = matrix(3, 3)
        l6[1, 2] = one
        l6[2, 1] = one

        # lambda_7
        l7 = matrix(3, 3)
        l7[1, 2] = -j
        l7[2, 1] = j

        # lambda_8
        l8 = matrix(3, 3)
        l8[0, 0] = inv_sqrt3
        l8[1, 1] = inv_sqrt3
        l8[2, 2] = -mpf('2') * inv_sqrt3

        # T^a = lambda^a / 2
        generators = []
        for lam in [l1, l2, l3, l4, l5, l6, l7, l8]:
            generators.append(lam * half)

        return generators

    def get(self, a):
        """
        Return generator T^a (0-indexed: a = 0..7).

        Returns:
            mpmath.matrix: 3x3 complex matrix T^a = lambda^{a+1} / 2
        """
        if not (0 <= a <= 7):
            raise IndexError(f"Generator index must be 0-7, got {a}")
        return self._generators[a]

    @property
    def all(self):
        """Return list of all 8 generators."""
        return list(self._generators)

    def verify_orthonormality(self):
        """
        Verify Tr(T^a T^b) = delta^{ab} / 2 for all pairs.

        Returns:
            mpf: Maximum residual across all 64 pairs.
        """
        mp.dps = 80
        max_residual = mpf('0')
        for a in range(8):
            for b in range(8):
                product = self._generators[a] * self._generators[b]
                trace = _trace(product)
                expected = mpf('0.5') if a == b else mpf('0')
                residual = fabs(trace - expected)
                if residual > max_residual:
                    max_residual = residual
        return max_residual

    def verify_tracelessness(self):
        """
        Verify Tr(T^a) = 0 for all generators.

        Returns:
            mpf: Maximum |Tr(T^a)| across all 8 generators.
        """
        mp.dps = 80
        max_residual = mpf('0')
        for a in range(8):
            trace = _trace(self._generators[a])
            residual = fabs(trace)
            if residual > max_residual:
                max_residual = residual
        return max_residual


# =============================================================================
# 2. LIE ALGEBRA INJECTION
# =============================================================================

def lie_algebra_inject(U, delta_coeffs, coupling_ag=None):
    """
    Inject a Lie algebra perturbation into a link variable.

    Constructs delta_A = sum_a delta_coeffs[a] * T^a in su(3),
    then returns U' = exp(i * ag * delta_A) . U.

    This guarantees delta_A is in the algebra by construction (algebraic closure).

    Args:
        U (mpmath.matrix): Current 3x3 link variable in SU(3).
        delta_coeffs (list/tuple of mpf): 8 real coefficients for
            the Gell-Mann basis expansion.
        coupling_ag (mpf or None): The product a*g (lattice spacing times
            gauge coupling). Defaults to 1 if None.

    Returns:
        mpmath.matrix: U' = exp(i * ag * delta_A^a T^a) . U

    Evidence Category: A (algebraic construction, exact by definition)
    """
    mp.dps = 80
    from mpmath import mpc

    if coupling_ag is None:
        coupling_ag = mpf('1')

    if len(delta_coeffs) != 8:
        raise ValueError(f"Expected 8 algebra coefficients, got {len(delta_coeffs)}")

    basis = GellMannBasis()
    j = mpc(0, 1)

    # Construct delta_A = sum_a delta_coeffs[a] * T^a
    delta_A = matrix(3, 3)
    for a in range(8):
        delta_A = delta_A + mpf(str(delta_coeffs[a])) * basis.get(a)

    # Construct the exponent: i * ag * delta_A
    exponent = j * coupling_ag * delta_A

    # Matrix exponential: exp(i * ag * delta_A)
    exp_matrix = mp.expm(exponent)

    # U' = exp(...) . U
    U_prime = exp_matrix * U

    return U_prime


# =============================================================================
# 3. SU(3) REPROJECTION VIA POLAR DECOMPOSITION (Newton-Schulz)
# =============================================================================

def project_to_su3(W, max_iter=200, tol=None):
    """
    Project a general GL(3,C) matrix W to the nearest SU(3) element
    via iterative Newton-Schulz polar decomposition.

    Algorithm:
        X_0 = W
        X_{n+1} = (1/2) * (X_n + X_n^{-dagger})
        Converge until ||X^dag X - I|| < tol

    Then normalize determinant:
        U = X / det(X)^{1/3}

    Post-conditions (verified internally):
        ||U^dag U - I|| < 10^{-70}
        |det(U) - 1|   < 10^{-70}

    Args:
        W (mpmath.matrix): 3x3 complex matrix to project.
        max_iter (int): Maximum Newton-Schulz iterations.
        tol (mpf or None): Convergence tolerance. Defaults to 10^{-75}.

    Returns:
        mpmath.matrix: U in SU(3)

    Raises:
        RuntimeError: If convergence fails after max_iter iterations.
        RuntimeError: If post-conditions are violated.

    Evidence Category: A (constructive, residual < 10^{-70})
    """
    mp.dps = 80
    if tol is None:
        tol = mpf('1e-75')

    X = W.copy()

    for iteration in range(max_iter):
        # X_inv_dagger = (X^{-1})^dagger = (X^dagger)^{-1}
        X_dag = _dagger(X)
        try:
            X_inv_dag = X_dag ** (-1)
        except ZeroDivisionError:
            raise RuntimeError(
                f"[GAUGE-PROJ-FAIL] Singular matrix at Newton-Schulz iteration {iteration}"
            )

        X_new = (X + X_inv_dag) * mpf('0.5')

        # Check convergence: ||X^dag X - I||
        unitarity_residual = _frobenius_norm(_dagger(X_new) * X_new - eye(3))

        if unitarity_residual < tol:
            X = X_new
            break
        X = X_new
    else:
        raise RuntimeError(
            f"[GAUGE-PROJ-FAIL] Newton-Schulz did not converge after {max_iter} "
            f"iterations. Residual: {unitarity_residual}"
        )

    # Determinant normalization: U = X / det(X)^{1/3}
    d = det(X)
    # Cube root of complex determinant
    d_abs = fabs(d)
    if d_abs < mpf('1e-60'):
        raise RuntimeError(
            f"[GAUGE-PROJ-FAIL] Near-zero determinant: {d}"
        )
    # det(X) should be close to e^{i*theta} after unitarization
    # Normalize: U = X / det(X)^{1/3}
    from mpmath import cbrt, arg, mpc, exp as mp_exp
    phase = arg(d) / mpf('3')
    scale = cbrt(d_abs)
    correction = mpc(1, 0) / (scale * mp_exp(mpc(0, phase)))
    U = X * correction

    # === POST-CONDITION VERIFICATION ===
    post_tol = mpf('1e-70')

    # Check unitarity: ||U^dag U - I||
    unitarity_check = _frobenius_norm(_dagger(U) * U - eye(3))
    if unitarity_check >= post_tol:
        raise RuntimeError(
            f"[SU3-UNITARITY-FAIL] ||U^dag U - I|| = {unitarity_check} >= {post_tol}"
        )

    # Check det(U) = 1
    det_check = fabs(det(U) - mpf('1'))
    if det_check >= post_tol:
        raise RuntimeError(
            f"[SU3-DET-FAIL] |det(U) - 1| = {det_check} >= {post_tol}"
        )

    return U


# =============================================================================
# 4. SVD CONDITION MONITOR
# =============================================================================

def svd_condition_check(perturbation_matrix, threshold=None):
    """
    Check the SVD condition number of a proposal perturbation.

    Tensor networks in 4D gauge theories suffer from entanglement volume
    law explosion, which manifests as catastrophic condition numbers:
        sigma_max / sigma_min >> 10^{16}

    Kill condition: kappa_SVD > threshold -> proposal REJECTED before HMC.

    Args:
        perturbation_matrix (mpmath.matrix): The perturbation matrix to check.
        threshold (mpf or None): Kill threshold. Defaults to 10^{12}.

    Returns:
        tuple: (passed: bool, kappa: mpf, sigmas: list[mpf])
            - passed: True if kappa < threshold
            - kappa: The condition number sigma_max / sigma_min
            - sigmas: Sorted list of singular values (descending)

    Evidence Category: A (numerical diagnostic, exact computation)
    """
    mp.dps = 80
    if threshold is None:
        threshold = mpf('1e12')

    # Compute singular values via eigenvalues of W^dag W
    WdW = _dagger(perturbation_matrix) * perturbation_matrix
    eigenvalues = mp.eighe(WdW)

    # eigenvalues are real and non-negative for Hermitian positive semi-definite
    # mp.eighe returns (eigenvalues, eigenvectors) — extract eigenvalues
    if isinstance(eigenvalues, tuple):
        evals = eigenvalues[0]
    else:
        evals = eigenvalues

    sigmas = sorted([sqrt(fabs(e)) for e in evals], reverse=True)

    sigma_max = sigmas[0]
    sigma_min = sigmas[-1]

    if sigma_min < mpf('1e-75'):
        # Effectively singular — automatic reject
        kappa = mpf('inf')
        return False, kappa, sigmas

    kappa = sigma_max / sigma_min

    passed = kappa < threshold

    if not passed:
        # Log diagnostic but do not raise — caller decides
        pass

    return passed, kappa, sigmas


# =============================================================================
# 5. METROPOLIS DETAILED BALANCE GUARD
# =============================================================================

class MetropolisDetailedBalanceGuard:
    """
    Symmetrized Metropolis acceptance kernel that corrects for asymmetric
    proposal distributions.

    Standard HMC uses: P_acc = min(1, exp(-Delta_H))

    This is INSUFFICIENT when the proposal kernel is asymmetric (which is
    almost always the case for TN/ML-enhanced proposals).

    Correct form:
        P_acc = min(1, exp(-Delta_S) * Q(U' -> U) / Q(U -> U'))

    where Q is the proposal probability density.

    For symmetric proposals (standard HMC with Gaussian momenta),
    Q(U->U') = Q(U'->U) and this reduces to the standard form.

    Evidence Category: A (mathematical identity)
    """

    def __init__(self):
        mp.dps = 80
        self._violation_history = []

    def acceptance_probability(self, delta_S, log_Q_backward, log_Q_forward):
        """
        Compute corrected Metropolis acceptance probability.

        Args:
            delta_S (mpf): Action difference S[U'] - S[U].
            log_Q_backward (mpf): log Q(U' -> U) (backward proposal log-density).
            log_Q_forward (mpf): log Q(U -> U') (forward proposal log-density).

        Returns:
            mpf: P_acc = min(1, exp(-delta_S + log_Q_backward - log_Q_forward))
        """
        mp.dps = 80
        log_ratio = -delta_S + log_Q_backward - log_Q_forward

        if log_ratio >= mpf('0'):
            return mpf('1')

        from mpmath import exp as mp_exp
        return mp_exp(log_ratio)

    def check_detailed_balance(self, delta_S, log_Q_backward, log_Q_forward,
                                action_U, action_U_prime):
        """
        Verify that detailed balance is satisfied within tolerance.

        Tests: |P(U->U') * exp(-S[U]) - P(U'->U) * exp(-S[U'])| < 10^{-8}

        Args:
            delta_S (mpf): S[U'] - S[U]
            log_Q_backward (mpf): log Q(U' -> U)
            log_Q_forward (mpf): log Q(U -> U')
            action_U (mpf): S[U]
            action_U_prime (mpf): S[U']

        Returns:
            tuple: (passed: bool, violation: mpf)

        Evidence Category: A (mathematical verification)
        """
        mp.dps = 80
        from mpmath import exp as mp_exp

        tolerance = mpf('1e-8')

        # Forward transition rate: Q(U->U') * P_acc(U->U')
        p_acc_forward = self.acceptance_probability(
            delta_S, log_Q_backward, log_Q_forward
        )
        # Backward: delta_S changes sign, Q roles swap
        p_acc_backward = self.acceptance_probability(
            -delta_S, log_Q_forward, log_Q_backward
        )

        # Detailed balance: P(U->U') e^{-S[U]} = P(U'->U) e^{-S[U']}
        # Where P(U->U') = Q(U->U') * P_acc(U->U')
        from mpmath import exp as mp_exp

        # Use log-space to avoid overflow
        log_lhs = log_Q_forward + mp.log(p_acc_forward) - action_U
        log_rhs = log_Q_backward + mp.log(p_acc_backward) - action_U_prime

        violation = fabs(log_lhs - log_rhs)

        self._violation_history.append(violation)

        passed = violation < tolerance

        if not passed:
            pass  # Caller handles the halt

        return passed, violation

    @property
    def max_violation(self):
        """Return maximum detailed balance violation observed."""
        if not self._violation_history:
            return mpf('0')
        return max(self._violation_history)


# =============================================================================
# 6. HAAR MEASURE DRIFT MONITOR
# =============================================================================

def haar_measure_drift(link_matrices):
    """
    Monitor the cumulative unitarity drift across an ensemble of link variables.

    Computes max_i ||U_i^dag U_i - I||_F for a collection of SU(3) matrices.

    Threshold: max drift > 10^{-10} -> [HAAR-DRIFT] Invalid ensemble.

    Args:
        link_matrices (list of mpmath.matrix): Collection of 3x3 link variables.

    Returns:
        tuple: (passed: bool, max_drift: mpf, mean_drift: mpf)

    Evidence Category: A (numerical diagnostic)
    """
    mp.dps = 80
    threshold = mpf('1e-10')

    if not link_matrices:
        return True, mpf('0'), mpf('0')

    max_drift = mpf('0')
    total_drift = mpf('0')

    for U in link_matrices:
        drift = _frobenius_norm(_dagger(U) * U - eye(3))
        if drift > max_drift:
            max_drift = drift
        total_drift = total_drift + drift

    mean_drift = total_drift / mpf(str(len(link_matrices)))

    passed = max_drift < threshold

    return passed, max_drift, mean_drift


# =============================================================================
# 7. TOPOLOGICAL CHARGE MONITOR
# =============================================================================

def topological_charge_clover(plaquettes_munu, plaquettes_munu_dual):
    """
    Compute the topological charge Q_top via clover discretization.

    Q_top = (1 / 32 pi^2) * sum_x Tr(F_munu * F_tilde_munu)

    where F_munu is approximated by the clover (four-plaquette average)
    and F_tilde_munu is its dual.

    NOTE: This is the 1x1 clover approximation. For improved definitions,
    see Luscher (2010).

    Args:
        plaquettes_munu (list): Field strength tensor components
            F_{mu,nu}(x) as 3x3 mpmath matrices.
        plaquettes_munu_dual (list): Dual field strength tensor components
            F_tilde_{mu,nu}(x) as 3x3 mpmath matrices.

    Returns:
        mpf: Q_top (should be near-integer for smooth configurations)

    Evidence Category: B (lattice discretization artifact)
    """
    mp.dps = 80

    if len(plaquettes_munu) != len(plaquettes_munu_dual):
        raise ValueError("F and F_tilde must have same number of components")

    prefactor = mpf('1') / (mpf('32') * pi ** 2)

    q_sum = mpf('0')
    for F, F_tilde in zip(plaquettes_munu, plaquettes_munu_dual):
        q_sum = q_sum + _trace_real(F * F_tilde)

    return prefactor * q_sum


def topological_charge_bias(q_history):
    """
    Check for topological charge bias in the Monte Carlo history.

    A healthy ensemble should have <Q> / sigma_Q < 2.
    Violation indicates topological freezing or biased proposal dynamics.

    Args:
        q_history (list of mpf): History of Q_top measurements.

    Returns:
        tuple: (passed: bool, mean_Q: mpf, sigma_Q: mpf, ratio: mpf)

    Evidence Category: B (statistical test)
    """
    mp.dps = 80

    if len(q_history) < 2:
        return True, mpf('0'), mpf('0'), mpf('0')

    n = len(q_history)
    mean_Q = sum(q_history) / mpf(str(n))
    variance = sum((q - mean_Q) ** 2 for q in q_history) / mpf(str(n - 1))
    sigma_Q = sqrt(variance) if variance > mpf('0') else mpf('1e-30')

    ratio = fabs(mean_Q) / sigma_Q

    passed = ratio < mpf('2')

    return passed, mean_Q, sigma_Q, ratio


# =============================================================================
# INTERNAL UTILITIES (NOT EXPORTED)
# =============================================================================

def _trace(M):
    """Compute trace of 3x3 mpmath matrix."""
    mp.dps = 80
    return M[0, 0] + M[1, 1] + M[2, 2]


def _trace_real(M):
    """Compute real part of trace of 3x3 mpmath matrix."""
    mp.dps = 80
    t = _trace(M)
    if hasattr(t, 'real'):
        return t.real
    return t


def _dagger(M):
    """Compute Hermitian conjugate (conjugate transpose) of mpmath matrix."""
    mp.dps = 80
    n = M.rows
    m = M.cols
    result = matrix(m, n)
    for i in range(n):
        for k in range(m):
            val = M[i, k]
            if hasattr(val, 'conjugate'):
                result[k, i] = val.conjugate()
            else:
                result[k, i] = val
    return result


def _frobenius_norm(M):
    """Compute Frobenius norm ||M||_F = sqrt(sum |M_ij|^2)."""
    mp.dps = 80
    total = mpf('0')
    for i in range(M.rows):
        for k in range(M.cols):
            val = M[i, k]
            total = total + fabs(val) ** 2
    return sqrt(total)


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    mp.dps = 80
    print("=" * 70)
    print("  UIDT GAUGE-CONSISTENT MANIFOLD TRANSPORT v3.9.2")
    print("  Evidence Category: A (mathematical core)")
    print("=" * 70)

    # Test 1: Gell-Mann basis
    basis = GellMannBasis()
    ortho_res = basis.verify_orthonormality()
    trace_res = basis.verify_tracelessness()
    print(f"\n[TEST 1] Gell-Mann orthonormality residual: {mp.nstr(ortho_res, 6)}")
    print(f"[TEST 1] Gell-Mann tracelessness residual:  {mp.nstr(trace_res, 6)}")
    assert ortho_res < mpf('1e-14'), f"ORTHONORMALITY FAIL: {ortho_res}"
    assert trace_res < mpf('1e-14'), f"TRACELESSNESS FAIL: {trace_res}"
    print("[TEST 1] PASS")

    # Test 2: Reprojection
    # Start with identity (already in SU(3))
    I3 = eye(3)
    U_proj = project_to_su3(I3)
    id_residual = _frobenius_norm(U_proj - I3)
    print(f"\n[TEST 2] Identity reprojection residual: {mp.nstr(id_residual, 6)}")
    assert id_residual < mpf('1e-70'), f"REPROJECTION FAIL: {id_residual}"
    print("[TEST 2] PASS")

    # Test 3: SVD condition check on identity
    passed, kappa, sigmas = svd_condition_check(I3)
    print(f"\n[TEST 3] SVD condition(I): kappa = {mp.nstr(kappa, 6)}, passed = {passed}")
    assert passed, "SVD FAIL on identity"
    print("[TEST 3] PASS")

    # Test 4: Lie algebra injection from identity
    coeffs = [mpf('0.01')] * 8
    U_injected = lie_algebra_inject(I3, coeffs, coupling_ag=mpf('0.1'))
    U_reproj = project_to_su3(U_injected)
    unit_res = _frobenius_norm(_dagger(U_reproj) * U_reproj - eye(3))
    print(f"\n[TEST 4] Lie algebra injection -> reprojection unitarity: {mp.nstr(unit_res, 6)}")
    assert unit_res < mpf('1e-70'), f"INJECTION FAIL: {unit_res}"
    print("[TEST 4] PASS")

    # Test 5: Haar measure drift
    matrices = [project_to_su3(eye(3))] * 10
    passed_h, max_d, mean_d = haar_measure_drift(matrices)
    print(f"\n[TEST 5] Haar drift: max={mp.nstr(max_d, 6)}, mean={mp.nstr(mean_d, 6)}, passed={passed_h}")
    assert passed_h, "HAAR DRIFT FAIL"
    print("[TEST 5] PASS")

    print("\n" + "=" * 70)
    print("  ALL SELF-TESTS PASSED")
    print("  DOI: 10.5281/zenodo.17835200")
    print("=" * 70)
