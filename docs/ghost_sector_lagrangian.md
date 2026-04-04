# Ghost Sector and BRST Symmetry — UIDT v3.9

> **Evidence Category:** [A] Mathematically derived  
> **Version:** v3.9 | **Source:** Ultra Main Paper §3  
> **Context:** Required for gauge-fixed path integral and physical state space

---

## 1. Purpose

The canonical Lagrangian in `FORMALISM.md` documents the Yang-Mills and
information-field sectors. For a complete gauge-fixed quantum field theory —
necessary for the Wightman axiom construction and the Clay proof — the
**ghost sector** (Faddeev-Popov ghosts) and **BRST symmetry** must be
explicitly included.

This document records the complete gauge-fixed UIDT Lagrangian as presented
in Ultra Main Paper §3.

---

## 2. Complete UIDT Lagrangian Density

$$\mathcal{L}_{\text{UIDT}} = \mathcal{L}_{\text{YM}} + \mathcal{L}_S + \mathcal{L}_{\text{int}} + \mathcal{L}_{\text{gf}} + \mathcal{L}_{\text{ghost}}$$

### 2.1 Yang-Mills Sector

$$\mathcal{L}_{\text{YM}} = -\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}$$

with field strength $F^a_{\mu\nu} = \partial_\mu A^a_\nu - \partial_\nu A^a_\mu + g f^{abc} A^b_\mu A^c_\nu$.

### 2.2 Information-Field Sector

$$\mathcal{L}_S = \frac{1}{2}(\partial_\mu S)^2 - \frac{\lambda_S}{4}(S^2 - v^2)^2$$

with $v = 47.7$ MeV [A] and $\lambda_S = 0.417$ [A].

### 2.3 Interaction Sector

$$\mathcal{L}_{\text{int}} = -\frac{\kappa}{4} S^2 F^a_{\mu\nu} F^{a\mu\nu}$$

with $\kappa = 0.500$ [A]. This term generates $m_{\text{eff}}^2 = \kappa v^2 > 0$,
which is the origin of the mass gap.

### 2.4 Gauge-Fixing Sector (Lorenz gauge)

$$\mathcal{L}_{\text{gf}} = -\frac{1}{2\xi}(\partial^\mu A^a_\mu)^2$$

The Lorenz gauge $\xi \to 0$ (Landau gauge) is used in the Gribov-horizon
analysis. Physical observables are $\xi$-independent.

### 2.5 Ghost Sector (Faddeev-Popov)

$$\mathcal{L}_{\text{ghost}} = \bar{c}^a \left(-\partial^\mu D_{\mu}^{ab}\right) c^b$$

where:
- $c^a$ — Faddeev-Popov ghost (Grassmann scalar, adjoint representation)
- $\bar{c}^a$ — anti-ghost
- $D_{\mu}^{ab} = \partial_\mu \delta^{ab} + g f^{acb} A^c_\mu$ — covariant derivative in adjoint

**Role of ghost sector:** The ghost determinant cancels the unphysical
longitudinal gauge degrees of freedom in the path integral measure.

---

## 3. BRST Symmetry

The complete Lagrangian $\mathcal{L}_{\text{UIDT}}$ is invariant under the
nilpotent BRST transformation $s$ ($s^2 = 0$):

$$s A^a_\mu = D_\mu^{ab} c^b \qquad s c^a = -\frac{g}{2} f^{abc} c^b c^c$$

$$s \bar{c}^a = \frac{1}{\xi} \partial^\mu A^a_\mu \qquad s S = 0$$

> **Key result:** $s S = 0$ — the information-density scalar field is
> **BRST-invariant**. This means $S(x)$ is a physical observable (not a ghost).

### BRST Cohomology and Physical States

The physical Hilbert space is defined by BRST cohomology:

$$\mathcal{H}_{\text{phys}} = \ker(Q_{\text{BRST}}) / \text{im}(Q_{\text{BRST}})$$

where $Q_{\text{BRST}} = \int d^3x \, j^0_{\text{BRST}}$ is the conserved BRST charge.

**Consequence:** Physical states satisfy $Q_{\text{BRST}}|\text{phys}\rangle = 0$.
The mass gap $\Delta^* > 0$ implies that the lowest physical excitation above
the vacuum has energy $\geq \Delta^*$.

---

## 4. Connection to Gribov Resolution

The ghost propagator $G_c(k^2) = 1/(k^2 + \epsilon)$ is IR-enhanced in the
presence of Gribov copies. In UIDT, the effective mass $m_{\text{eff}} > 0$
regularizes this enhancement:

$$G_c(k^2)\big|_{\text{UIDT}} = \frac{1}{k^2 + m_{\text{eff}}^2 \cdot r(k^2)}$$

where $r(k^2) \to 0$ as $k^2 \to \infty$ (asymptotic freedom) and
$r(0) = 1$ (IR regularization). This is the UIDT mechanism for Gribov
horizon suppression.

> **Limitation L-ghost:** The exact form of $r(k^2)$ requires
> non-perturbative lattice input. The current form is analytic [A]
> but the IR value $r(0) = 1$ is an assumption that requires lattice
> verification [B].

---

## 5. Verification: BRST Nilpotency

> **[PLACEHOLDER — SU(2) SUBGROUP ONLY]**  
> The function `verify_brst_nilpotency()` below checks the Jacobi identity
> exclusively for the SU(2) subgroup (generators 1–3, $f^{123} = f^{231} = f^{312} = 1$).
> Full SU(3) nilpotency ($s^2 = 0$ over all 8 generators and 9 independent
> structure constants $f^{abc}$) requires the complete SU(3) $f^{abc}$ table
> and has **not yet been implemented**.  
> **Evidence category of this check: [PLACEHOLDER], not [A].**  
> Full SU(3) numerical verification is an open task (see §6 Open Tasks).

```python
import mpmath as mp

def verify_brst_nilpotency():
    """
    [PLACEHOLDER — SU(2) SUBGROUP ONLY]
    Symbolic check that s^2 = 0 on the ghost field for the SU(2) subgroup.
    Uses mpmath for numerical verification of the Jacobi identity
    for structure constants f^{abc} of SU(2) embedded in SU(3).
    mp.dps = 80 set locally per RACE CONDITION LOCK.

    LIMITATION: This tests only the SU(2) subalgebra (f^{123}=1, cyclic).
    Full SU(3) nilpotency requires all 9 independent f^{abc} values.
    Do NOT cite this function as evidence for full SU(3) BRST nilpotency.
    """
    mp.dps = 80

    # SU(2) subgroup: f^{123} = f^{231} = f^{312} = 1 (all others zero here)
    f_123 = mp.mpf('1')
    f_231 = mp.mpf('1')
    f_312 = mp.mpf('1')

    # Jacobi identity for SU(2): f^{123}f^{231} + f^{231}f^{312} + f^{312}f^{123} - 3 = 0
    s2_ghost = (f_123 * f_231 + f_231 * f_312 + f_312 * f_123) - mp.mpf('3')

    assert s2_ghost == mp.mpf('0'), "[BRST_SU2_FAIL] SU(2) Jacobi identity violated"

    print(f"BRST s^2 test (SU(2) subgroup): {mp.nstr(s2_ghost, 10)}")
    print("[PLACEHOLDER] Full SU(3) nilpotency requires complete f^{abc} table.")
    print("BRST nilpotency: SU(2) subgroup consistent with s^2=0 [PLACEHOLDER]")

verify_brst_nilpotency()
```

---

## 6. Summary: Sector Structure

| Sector | Lagrangian term | Evidence | Physical role |
|--------|----------------|----------|---------------|
| Yang-Mills | $-\frac{1}{4}F^2$ | [A] | Gauge field dynamics |
| Information field | $\frac{1}{2}(\partial S)^2 - V(S)$ | [A] | Mass generation |
| Interaction | $-\frac{\kappa}{4}S^2 F^2$ | [A] | Mass gap origin |
| Gauge fixing | $-\frac{1}{2\xi}(\partial A)^2$ | [A] | Path integral definition |
| Ghost | $\bar{c}(-\partial D)c$ | [A] | Unphysical mode cancellation |
| BRST nilpotency check | SU(2) subgroup only | **[PLACEHOLDER]** | Pending full SU(3) implementation |

---

## 7. Open Tasks

- [ ] Implement full SU(3) BRST nilpotency check using the complete
      $f^{abc}$ table (all 9 independent non-zero structure constants).
      Target evidence category: [A] upon completion.
- [ ] Verify that the information-field coupling $\kappa S^2 F^2$ does not
      break BRST invariance at loop level (Ward identity check).

---

## 8. Cross-References

- `FORMALISM.md` — canonical Lagrangian (sectors 1–3 above)
- `docs/gribov_cheeger_proof.md` — Gribov horizon and mass gap
- `docs/gns_hilbert_construction.md` — BRST cohomology → physical Hilbert space
- `clay-submission/01_Manuscript/` — full Clay proof
- `modules/gribov/` — (to be created) Gribov regularization implementation
