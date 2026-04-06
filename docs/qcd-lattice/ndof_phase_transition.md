# Ndof Phase Transition Mechanism

> **Evidence Category:** [B] Lattice compatible  
> **Version:** v3.9 | **Source:** UIDT I, UIDT II, Master Report 2

---

## 1. Conceptual Foundation

In UIDT, **mass generation** is not continuous. It occurs only when a critical
information density (equivalently: entropy gradient or thermal parameter)
is exceeded. Below the threshold, the effective number of active degrees of
freedom $N_{\text{dof}} = 0$ and hence $m_{\text{eff}} = 0$.

This discontinuity is the UIDT interpretation of the Yang-Mills mass gap.

## 2. Activation Function

### Standard Form

$$N_{\text{dof}}(u) = N_{\text{max}} \cdot \frac{1}{2}\left(1 + \tanh\left(\frac{u - u_c}{\sigma}\right)\right)$$

with:
- $u_c = 3.0$ — critical control parameter [B]
- $\sigma$ — transition width (lattice-dependent)
- $N_{\text{max}}$ — maximum degrees of freedom

### Higgs-VEV Coupled Form

When coupled to the Higgs sector (Evidence [C]):

$$N_{\text{dof}} = N_{\text{max}} \left(1 - \frac{1}{2}\left(1 + \tanh\left(\beta_c - \beta \cdot \frac{H^2}{H_{\text{VEV}}^2}\right)\right)\right)$$

where $H_{\text{VEV}} = 246$ GeV is the Higgs vacuum expectation value.

> **Limitation L-Ndof:** The Higgs-coupled form is a theoretical extension [C].
> The standard form is lattice-compatible [B] and constitutes the primary claim.

## 3. Connection to Effective Mass

The effective mass field is:

$$m_{\text{eff}}^2(x) = m_0^2 + \frac{k_B^2}{c^4} (\nabla S)^2 \cdot \frac{N_{\text{dof}}(u)}{N_{\text{max}}}$$

Below $u_c$: $N_{\text{dof}} \approx 0 \Rightarrow m_{\text{eff}} \approx m_0$ (bare mass only)  
Above $u_c$: $N_{\text{dof}} \rightarrow N_{\text{max}} \Rightarrow$ full mass activation

## 4. Lattice Simulation Results

The 2D lattice simulation (UIDT Master Report 2) demonstrated:
- Sharp nonlinear jump in $N_{\text{dof}}$ at $u = u_c = 3.0$
- Behaviour consistent with QCD confinement analogy
- Phase transition order: second-order (continuous in $N_{\text{dof}}$,
  discontinuous in $\partial N_{\text{dof}}/\partial u$)

```python
import mpmath as mp
import numpy as np

mp.dps = 80

def ndof_activation(u, u_c=3.0, sigma=0.5, N_max=100):
    """
    UIDT Ndof activation function.
    mp.dps = 80 is set locally per RACE CONDITION LOCK.
    """
    mp.dps = 80
    u_mp  = mp.mpf(str(u))
    uc_mp = mp.mpf(str(u_c))
    sig   = mp.mpf(str(sigma))
    return mp.mpf(str(N_max)) * mp.mpf('0.5') * (1 + mp.tanh((u_mp - uc_mp) / sig))

# Verification: at u = u_c the activation should equal N_max / 2
u_test = mp.mpf('3.0')
result = ndof_activation(u_test)
expected = mp.mpf('50')  # N_max / 2
residual = abs(result - expected)
print(f"Ndof(u_c) = {mp.nstr(result, 20)}")
print(f"Residual  = {mp.nstr(residual, 10)}")
assert residual < mp.mpf('1e-14'), "[NDOF_SYMMETRY_FAIL]"
```

## 5. Cross-References

- `modules/ndof/` — (to be created) full implementation
- `simulation/` — lattice simulation code
- `FORMALISM.md` — Lagrangian context
- `docs/CE8_derivation.md` — CE8 in emergent-time context
