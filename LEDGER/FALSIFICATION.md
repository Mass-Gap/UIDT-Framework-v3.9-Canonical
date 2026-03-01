# UIDT Falsification Criteria v3.7.2

> **PURPOSE:** Define hard limits that would falsify UIDT
> **PRINCIPLE:** A theory that cannot be wrong cannot be science

---

## Active Falsification Tests

### F1: Lattice QCD Mass Gap
**Prediction:** $\Delta = 1.710 \pm 0.015$ GeV

**Falsification Condition:**
$$|\Delta_{\text{Lattice}} - 1.710| > 3\sigma_{\text{combined}}$$

**Current Status:** ✅ CONSISTENT
- Lattice value: 1.710 ± 0.040 GeV (Morningstar et al. 2024)
- z-score: 0.37σ (well within tolerance)

**Timeline:** Continuous monitoring of lattice updates

---

### F2: Casimir Force Anomaly
**Prediction:** $\Delta F/F = +0.59\%$ at $d = 0.66$ nm [D]

**Falsification Condition:**
$$|\Delta F/F| < 0.1\% \quad \text{at} \quad d \approx 0.66 \text{ nm}$$

**Current Status:** ⏳ PENDING
- No precision Casimir measurement at sub-nm scale available
- Requires: AFM or molecular force spectroscopy

**Timeline:** Awaiting experimental capability

---

### F3: DESI Dark Energy
**Prediction:** $w_0 = -0.99$ [C] (Canonical per Decision D-002)

**Falsification Condition:**
$$w = -1.00 \pm 0.01 \quad \text{(exact } \Lambda\text{CDM)}$$

**Current Status:** ⏳ AMBIGUOUS
- DESI DR2: w = -0.99 ± 0.05
- Within UIDT range but also ΛCDM consistent
- Needs: DR3+ for decisive test

**Timeline:** DESI DR3 (expected 2026)

---

### F4: LHC Scalar Search
**Prediction:** $m_S = 1.705 \pm 0.015$ GeV [D]

**Falsification Condition:**
- Scalar resonance excluded in 1.5-1.9 GeV window at >5σ
- OR diphoton/dimuon anomaly clearly attributed to other physics

**Current Status:** ⏳ PENDING
- Low-mass scalar searches challenging at LHC
- Belle II or future lepton colliders may be better

**Timeline:** Long-term (2030+)


---

### F5: Lepton Flavor Universality (LFU) R_K
**Prediction:** Topological scaling shift of $\gamma^{-2} - \gamma^{-3} pprox +0.35\%$

**Falsification Condition:**
Wenn zukünftige LHCb Run 3/4 Daten die Unsicherheit von $R_K$ auf $< 0.1\%$ reduzieren und das Residuum exakt $0.000$ (SM-Limit) statt $\approx 0.0035$ (UIDT-Limit) beträgt, ist die topologische $\mu/e$-Skalierungshypothese falsifiziert.

**Current Status:** ⏳ PENDING
- Current LHCb precision for $R_K$ is $\approx 5\%$, masking the $\sim 0.35\%$ effect.
- Anomaly currently measured as $0 \pm 0.05$.

**Timeline:** LHCb Run 3/4 high-statistics updates.

---

### F6: RG Cascade Steps N_bare
**Prediction:** $N_{\text{bare}} = 99$ [D] (Lattice topology, Decision D-001)

**Physical Basis:**
N_bare = 99 represents the unrenormalized discrete lattice limit. The effective renormalized value N_eff = 94.05 [E] is conjectured via fractal damping (5%). Neither value has first-principles derivation.

**Falsification Condition:**
$$N_{\text{derived}} \neq 99 \pm 5 \quad \text{from non-perturbative RG calculation}$$

Specifically: If a first-principles derivation of the RG cascade step count from SU(3) vacuum structure, holographic duality, or \u03b2-function zeros yields $N \neq 99 \pm 5$, the lattice topology claim is refuted.

**Current Status:** \u23f3 PENDING
- No first-principles derivation exists for N=99
- N=99 is phenomenologically chosen to match $\rho_{\text{vac}} = \rho_{\text{obs}}$
- See Limitation L5 and Decision D-001

**Timeline:** Requires analytic progress on vacuum structure
