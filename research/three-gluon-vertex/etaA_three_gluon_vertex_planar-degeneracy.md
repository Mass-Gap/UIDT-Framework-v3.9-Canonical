# Three-Gluon Vertex — Planar Degeneracy

**UIDT Research Note**
**Date:** 2026-05-08
**Author:** P. Rietz (UIDT Framework v3.9)
**Branch:** TKT-2026-05-08-L4-three-gluon-vertex-planar-degeneracy-50801
**Evidence Category:** B (lattice compatible)
**Stratum:** I (Sec. 1–4), II (Sec. 5), III (Sec. 6)

---

## 1. Primary Reference

**Pinto-Gómez, De Soto, Ferreira, Papavassiliou, Rodríguez-Quintero (2022)**
*Lattice three-gluon vertex in extended kinematics: planar degeneracy*
Phys. Lett. B (2022)
arXiv: [2208.01020](https://arxiv.org/abs/2208.01020)
DOI: verified via ar5iv render — full text retrieved 2026-05-08

Quenched SU(3), Landau gauge, four lattice ensembles (β = 5.6, 5.8, 6.0, 6.2),
renormalization point μ = 4.3 GeV, soft-gluon MOM scheme.

---

## 2. Claims Table

| ID | Claim | Category | Source |
|---|---|---|---|
| UIDT-C-016-a | Form factors of the transversely projected three-gluon vertex depend almost exclusively on s² = ½(q²+r²+p²) — "planar degeneracy" | B | arXiv:2208.01020, Sec. 5 |
| UIDT-C-016-b | Dominant compact approximation: Ω̄Γ^αμν ≈ Ω̄Γ^sg(s²) · λ̃₁^αμν (Eq. 28) | B | arXiv:2208.01020, Eq. (28) |
| UIDT-C-016-c | χ²/datum = 3.9 (s² basis) vs. 66.4 (q² basis) — overlap improved by factor 17 | B | arXiv:2208.01020, Sec. 5 |
| UIDT-C-016-d | Collinear divergences at θ→π are cured by effective gluon mass m ≈ 350 MeV | B | arXiv:2208.01020, Sec. 6 |
| UIDT-C-016-e | Deviation from planar degeneracy at θ→π: max. 16% at s = 4 GeV | B | arXiv:2208.01020, Fig. 7 |
| UIDT-C-016-f | Connection to UIDT Δ* = 1.710 ± 0.015 GeV via gluon mass scale m ≈ 350 MeV | D | UIDT mapping (Stratum III) |

---

## 3. Core Results (Stratum I)

### 3.1 Kinematic Variable

All kinematic configurations on a plane ŝ² = const. in (q², r², p²)-space
share — to high accuracy — the same form factors:

```
s² = ½(q² + r² + p²)
```

In bisectoral kinematics (q² = r²):

```
s_b² = q² + p²/2
```

### 3.2 Bose-Symmetric Tensor Basis

The transversely projected vertex is expanded as (Eq. 8):

```
Ω̄Γ^αμν(q,r,p) = Σᵢ Γ̃ᵢ(q²,r²,p²) · λ̃ᵢ^αμν(q,r,p)    i = 1,...,4
```

Bose symmetry enforces (Eq. 9):

```
Γ̃ᵢ(q²,r²,p²) = Γ̃ᵢ(r²,q²,p²) = Γ̃ᵢ(q²,p²,r²)
```

λ̃₁ corresponds to the tree-level transversely projected vertex.

### 3.3 Planar Degeneracy — Approximate Relations (Eqs. 26–28)

**Two-term approximation (Eq. 27):**

```
Ω̄Γ^αμν(q,r,p) = Ω̄Γ^sg(s²) · λ̃₁^αμν(q,r,p)
               + Ω̄Γ₂^sym(2s²/3) · λ̃₂^αμν(q,r,p)
```

**Compact single-term approximation (Eq. 28):**

```
Ω̄Γ^αμν(q,r,p) ≈ Ω̄Γ^sg(s²) · λ̃₁^αμν(q,r,p)
```

where Ω̄Γ^sg is the soft-gluon form factor (single dynamical input).

### 3.4 Special Kinematic Limits

**Soft-gluon limit** (p² → 0, Eq. 19):

```
Ω̄Γ^sg(q²) = lim_{p²→0} [ Ω̄Γ₁(q²,q²,p²) + (3/2) Ω̄Γ₃(q²,q²,p²) ]
```

**Symmetric limit** (q² = r² = p², Eqs. 18a–18b):

```
Ω̄Γ₁^sym(q²) = lim_{p²→q²} [ Ω̄Γ₁(q²,q²,p²) + ½ Ω̄Γ₃(q²,q²,p²) ]
Ω̄Γ₂^sym(q²) = lim_{p²→q²} [ Ω̄Γ₂(q²,q²,p²) - (3/4) Ω̄Γ₃(q²,q²,p²) ]
```

### 3.5 Deviation Function (Eq. 30)

```
d(s²,θ) = [ Ω̄Γ₁(q²,q²,p²) - Ω̄Γ^sg(s²) ] / Ω̄Γ^sg(s²)
```

Vanishes identically under exact planar degeneracy.

---

## 4. One-Loop Analysis with Gluon Mass (Stratum I/II)

One-loop calculation (bisectoral, Eq. 29):

```
Ω̄Γ₁(q²,q²,p²) = 1 + w₁ ln(s²/μ²) + w₂ ln(1 + cosθ) + w₃
```

- Without gluon mass: collinear divergence at θ→π destroys planar degeneracy
- With m = 350 MeV (massive gluon propagator Δ(q²) → (q²+m²)⁻¹):
  - d(s²,θ) remains finite at θ = π
  - Maximum deviation < 5% for s ≤ 4 GeV (except near θ = π: peak 16%)
- Lattice data compatible with massive-gluon calculation; clearly above massless curve near θ = π

---

## 5. Scientific Consensus Context (Stratum II)

- Infrared suppression of three-gluon vertex form factors: established in literature
  [Athenodorou et al. 2016; Duarte et al. 2016; Aguilar et al. 2020, 2021]
- Zero crossing of dominant form factor: confirmed by multiple lattice groups
- Gluon mass scale m ≈ 300–400 MeV: consistent with Schwinger mechanism analyses
  [Aguilar, Papavassiliou et al., multiple works 2011–2022]
- Planar degeneracy: first identified in continuum analysis by Eichmann et al. (2014),
  arXiv:2208.01020 provides first systematic lattice confirmation

---

## 6. UIDT Mapping (Stratum III)

> **UIDT Limitation Notice:** The following constitutes Stratum III interpretation.
> It is not established physics. Transparency has priority over narrative coherence.

### 6.1 Connection to Δ* = 1.710 ± 0.015 GeV

The UIDT Yang–Mills spectral gap Δ* = 1.710 ± 0.015 GeV [Evidence A] represents
the vacuum information density threshold, not a particle mass.

The effective gluon mass scale m ≈ 350 MeV from arXiv:2208.01020 (Evidence B)
is consistent with the infrared end of the Schwinger mechanism mass function m²(q²).
The ratio Δ*/m ≈ 4.9 suggests Δ* operates at a parametrically higher scale
than the perturbative gluon mass threshold — consistent with UIDT's identification
of Δ* with the spectral gap of the full Yang–Mills operator, not with m(0).

**This connection is classified Evidence D (prediction/conjecture).**
No direct numerical identification of Δ* with m is claimed.

### 6.2 Compact Vertex for SDE Input

Eq. (28) provides a practical compression of the three-gluon vertex:

```
Ω̄Γ^αμν(q,r,p) ≈ Ω̄Γ^sg(s²) · λ̃₁^αμν(q,r,p)
```

In UIDT SDE pipelines this reduces the three-gluon vertex kernel to a
single scalar function of one variable, evaluated at the soft-gluon kinematics.
This is the recommended input for UIDT vacuum polarization calculations
until a full bisectoral dataset is integrated.

### 6.3 Parameter γ = 16.339 (Evidence A-)

The phenomenological kinetic vacuum parameter γ enters the vacuum polarization
integral. The planar degeneracy result reduces the integration domain from
a function of three independent kinematic variables to effectively one (s²),
which may simplify future γ-calibration runs. No numerical update to γ is
implied by the present analysis.

---

## 7. Validity Domain and Limitations

| Condition | Validity | Note |
|---|---|---|
| Bisectoral kinematics q²=r² | Confirmed, ~4000 lattice points | Main result of paper |
| General kinematics (q²≠r²) | Preliminary confirmation | Systematic study pending |
| θ < 5π/6 | d(s²,θ) < 5% | Safe domain for Eq. (28) |
| θ → π | d peaks at 16% (s=4 GeV) | Eq. (28) less reliable |
| Quenched approximation | Full QCD: qualitative pattern persists | See Aguilar et al. 2021 |
| Momentum range | 0–5 GeV (lattice ensembles) | Extrapolation beyond 5 GeV: caution |

---

## 8. Reproduction Note

```bash
# Paper data: quenched SU(3) Wilson action, four ensembles
# β = 5.6 (V=32⁴), β = 5.8 (V=48⁴), β = 6.0 (V=64⁴), β = 6.2 (V=80⁴)
# H4-extrapolation applied for hypercubic artifact removal
# Renormalization: μ = 4.3 GeV, soft-gluon MOM scheme, Eq. (21)
# Computing center: C3UPO (Univ. Pablo de Olavide)
# No UIDT numerical code required for Stratum I claims — all from lattice paper
```

---

## 9. Affected UIDT Ledger Parameters

| Parameter | Value | Evidence | Impact of this note |
|---|---|---|---|
| Δ* | 1.710 ± 0.015 GeV | A | Unchanged — Stratum III mapping only |
| γ | 16.339 | A- | Unchanged — simplification potential noted |
| γ∞ | 16.3437 | A- | Unchanged |
| v | 47.7 MeV | A | Unchanged |
| w0 | −0.99 | C | Unchanged |
| ET | 2.44 MeV | C | Unchanged |

**No ledger constants are modified by this note.**

---

*End of Research Note — UIDT-C-016*
