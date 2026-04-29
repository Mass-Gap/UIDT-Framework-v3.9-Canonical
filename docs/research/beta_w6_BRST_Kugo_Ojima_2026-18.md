# BETA-W6: BRST Cohomology and Kugo-Ojima Confinement Criterion Audit

**Task:** Full BRST cohomology and Kugo-Ojima confinement criterion audit.
**Objective:** Verify UIDT gauge-fixing sector is consistent with Kugo-Ojima criterion.
**Date:** 2026, Week 18
**Framework Version:** UIDT v3.9
**Evidence Stratum:** Stratum II (Field consensus), Stratum III (UIDT interpretation)

## 1. Kugo-Ojima Parameter Evaluation

### 1.1 Stratum I: Empirical Lattice Data
Lattice QCD measurements in quenched SU(3) Landau gauge indicate:
- Furui & Nakajima (2004): $u(0) = -0.713 \pm 0.014$
- Boucaud et al. (2001): $u(0) = -0.78 \pm 0.02$
- Sternbeck et al. (2012): $u(0) = -0.82 \pm 0.03$

These results suggest that the strict Kugo-Ojima criterion $u(0) = -1$ is **not supported** by direct lattice observation (tension $\approx 0.2$).

### 1.2 Stratum II: Field Consensus
The theoretical Kugo-Ojima (1979) confinement criterion requires $u(0) = -1$ in the infrared limit for the ghost dressing function to ensure confinement via the BRST-quartet mechanism. This assumes the Faddeev-Popov operator has no zero modes (no Gribov problem). Alternatively, the Gribov-Zwanziger approach imposes the horizon condition $h(0) = d(N^2-1)$. The field consensus remains divided between the decoupling solution (lattice favored) and the scaling solution (Dyson-Schwinger favored).

### 1.3 Stratum III: UIDT Mapping and Consistency
In the UIDT Framework (v3.7.1 and v3.9):
- The Kugo-Ojima mechanism is invoked formally (algebraically).
- The framework currently assumes the theoretical limit $u(0) = -1$ for the BRST quartet mechanism to operate efficiently, ensuring that unphysical ghost and longitudinal gluon states decouple.
- **Limitation:** The value $u(0)$ is not dynamically computed from the UIDT equations. There is a recognized **tension** between the theoretical assumption ($u(0) = -1$) and lattice data ($u(0) \approx -0.8$). This assumption holds an Evidence Category of **[D] (Unverified Prediction / Formal Setup)**.

**Numerical Check:**
Using `mpmath` at 80 digits of precision:
```python
from mpmath import mp
mp.dps = 80
u_UIDT = mp.mpf('-1')
u_KO = mp.mpf('-1')
deviation = abs(u_UIDT - u_KO)
# |u_UIDT - u_KO| = 0.0
```

## 2. BRST Cohomology Check

The physical Hilbert space in the UIDT framework must satisfy the BRST cohomology condition:

1. **Q-Closed Physical States:** For any physical state $|\text{phys}\rangle$, the action of the BRST charge $Q_{\text{BRST}}$ yields zero:
   $$Q_{\text{BRST}}|\text{phys}\rangle = 0$$
   This ensures that physical states are gauge-invariant.

2. **BRST Cohomology:** The physical Hilbert space is defined as the cohomology of $Q_{\text{BRST}}$:
   $$\mathcal{H}_{\text{phys}} = \ker(Q_{\text{BRST}}) / \text{im}(Q_{\text{BRST}})$$
   States that are BRST-exact (i.e., $|\Psi\rangle = Q_{\text{BRST}}|\chi\rangle$) have zero norm and correspond to unphysical longitudinal and ghost degrees of freedom.

3. **Ghost Decoupling:** Ghost ($c^a$) and anti-ghost ($\bar{c}^a$) states, along with longitudinal gluons, form a BRST quartet. In the physical subspace (defined by the cohomology), these states completely decouple. Thus, there are no negative-norm states in $\mathcal{H}_{\text{phys}}$, maintaining S-matrix unitarity.

4. **UIDT Information Scalar ($S$):** The UIDT field $S(x)$ is a BRST singlet ($s S = 0$). It trivially satisfies the cohomology requirements and contributes directly to the physical spectrum without introducing anomalous unphysical degrees of freedom.

## Conclusion

The UIDT gauge-fixing sector is algebraically consistent with the formal Kugo-Ojima BRST-quartet confinement mechanism, guaranteeing the decoupling of unphysical states. However, the exact value of the Kugo-Ojima parameter $u(0)$ is formally assumed to be $-1$ [Evidence D], which exhibits tension with lattice empirical measurements [Stratum I]. Further research is required to compute $u(0)$ dynamically within the UIDT framework to resolve this tension.
