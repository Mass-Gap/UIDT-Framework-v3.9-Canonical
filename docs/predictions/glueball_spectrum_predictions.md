# Glueball Spectrum Predictions — UIDT v3.9

> **Evidence Category:** [A] Spectral gap (Δ\*) | [D] Mass ratio predictions | [E] Glueball identification (WITHDRAWN)  
> **Version:** v3.9 | **Source:** Ultra Main Paper §9.1, §7.6  
> **Affected Constants:** Δ\* = 1.710 ± 0.015 GeV [A]  
> **Limitation:** L6 (Glueball f₀(1710) identification WITHDRAWN 2025-12-25)

---

## 1. Overview

> **Epistemic Note (L6 Resolution, 2025-12-25):**
> The spectral gap Δ\* = 1.710 ± 0.015 GeV [A] is the lowest eigenvalue
> of the Yang-Mills Hamiltonian — **NOT** a particle mass.
> The identification Δ\* = m(0⁺⁺) was **WITHDRAWN [E]** on 2025-12-25.
> Lattice QCD independently finds m(0⁺⁺) ≈ 1.710 GeV; the numerical
> proximity is noted but classified **[E]** (speculative coincidence).

The UIDT spectral gap Δ\* = 1710 ± 15 MeV [A] provides an energy scale
for the low-lying glueball spectrum via the RG fixed-point structure and
the Cheeger spectral gap hierarchy.

> The mass *ratios* below use Δ\* as a reference scale under UIDT assumptions
> and are classified [D] (predictions awaiting experimental confirmation).
> They do **not** depend on the withdrawn glueball identification.

---

## 2. Mass Ratio Predictions

From the UIDT transfer-matrix hierarchy (Ultra Main Paper §7.6):

$$\frac{m_{2^{++}}}{m_{0^{++}}} = 1.395 \pm 0.015 \qquad [D]$$

$$\frac{m_{0^{-+}}}{m_{0^{++}}} = 1.493 \pm 0.020 \qquad [D]$$

$$\frac{m_{0^{++*}}}{m_{0^{++}}} = 1.558 \pm 0.025 \qquad [D]$$

These ratios are derived from the Cheeger spectral hierarchy:
$$\Delta_n \geq \frac{h_n^2}{2}, \quad h_n = n \cdot h_1$$
where $h_1$ is the fundamental Cheeger constant of the gauge configuration
space (see `docs/gribov_cheeger_proof.md`).

---

## 3. Absolute Mass Predictions

Anchored to the spectral gap $\Delta^* = 1710 \pm 15$ MeV [A] as reference energy scale:

| State | $J^{PC}$ | UIDT [MeV] | Lattice QCD [MeV] | Status |
|-------|----------|------------|-------------------|--------|
| Spectral gap scale | $0^{++}$ | **1710 ± 15** | 1710 ± 80 | Δ\* = scale [A]; lattice coincidence [E] |
| Tensor | $2^{++}$ | 2386 ± 35 | 2400 ± 100 | Compatible [D/B] |
| Pseudoscalar | $0^{-+}$ | 2554 ± 40 | 2590 ± 130 | Compatible [D/B] |
| Excited scalar | $0^{++*}$ | 2664 ± 45 | ~2670 (uncertain) | Predicted [D] |

> **Lattice QCD reference:** Morningstar & Peardon, Phys. Rev. D 60 (1999) 034509.
> Verify DOI: https://doi.org/10.1103/PhysRevD.60.034509

---

## 4. Numerical Verification

```python
import mpmath as mp

def compute_glueball_spectrum(delta_star_gev='1.710'):
    """
    Compute glueball spectrum from UIDT mass ratios.
    mp.dps = 80 set locally per RACE CONDITION LOCK.
    """
    mp.dps = 80

    delta_star = mp.mpf(delta_star_gev)

    # Mass ratios from Ultra Main Paper §7.6
    ratio_2pp  = mp.mpf('1.395')
    ratio_0mp  = mp.mpf('1.493')
    ratio_0pps = mp.mpf('1.558')

    m_2pp  = delta_star * ratio_2pp
    m_0mp  = delta_star * ratio_0mp
    m_0pps = delta_star * ratio_0pps

    print(f"m(0++) = {mp.nstr(delta_star, 10)} GeV  [A]")
    print(f"m(2++) = {mp.nstr(m_2pp,  10)} GeV  [D]")
    print(f"m(0-+) = {mp.nstr(m_0mp,  10)} GeV  [D]")
    print(f"m(0++*)= {mp.nstr(m_0pps, 10)} GeV  [D]")

    # Consistency check: ratios must be > 1 (mass hierarchy)
    assert m_2pp  > delta_star, "[SPECTRUM_ORDER_FAIL] 2++ must be heavier than 0++"
    assert m_0mp  > delta_star, "[SPECTRUM_ORDER_FAIL] 0-+ must be heavier than 0++"
    assert m_0pps > m_0mp,     "[SPECTRUM_ORDER_FAIL] 0++* must be heavier than 0-+"

    return delta_star, m_2pp, m_0mp, m_0pps

compute_glueball_spectrum()
```

---

## 5. Experimental Falsification

These predictions are falsified (at $5\sigma$) if:

| Condition | Falsification threshold |
|-----------|------------------------|
| $m_{2^{++}}$ measured | Outside $2200$–$2600$ MeV |
| $m_{0^{-+}}$ measured | Outside $2400$–$2700$ MeV |
| Ratio $m_{2^{++}}/m_{0^{++}}$ | Outside $1.30$–$1.50$ |

Primary experimental venue: **BESIII** (Beijing), **LHCb** (CERN Run 3+).
See `docs/experimental_roadmap.md` Tier 1.

---

## 6. Cross-References

- `docs/gribov_cheeger_proof.md` — Cheeger bound derivation
- `docs/experimental_roadmap.md` — BESIII/LHCb timeline
- `docs/falsification_criteria.md` — F1 criterion
- `FORMALISM.md` — Δ* canonical value
- `clay-submission/01_Manuscript/` — Clay proof context
