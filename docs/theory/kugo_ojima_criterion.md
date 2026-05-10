# Kugo–Ojima Confinement Criterion in UIDT

**UIDT Framework v3.9** | Evidence Category: B (lattice KO coefficient), D (UIDT KO derivation)  
**Author:** P. Rietz | **Last updated:** 2026-03-25  
**DOI cross-reference:** 10.5281/zenodo.18003018 (v3.7.1, Section 5, Appendix C.3)

---

## Purpose

This document states and contextualises the Kugo–Ojima (KO) confinement criterion
within the UIDT framework. It distinguishes the BRST-algebraic confinement argument
used in v3.7.1 from the quantitative KO coefficient criterion, and flags where the
connection to the canonical parameters has not yet been established.

---

## Stratum I — Empirical Baseline

The Kugo–Ojima confinement criterion (Kugo & Ojima, 1979, Prog. Theor. Phys. Suppl. 66)
requires the KO function $u(p^2)$ to satisfy:

$$u(0) = -1$$

in the infrared limit. Here $u(p^2)$ is defined via the ghost–gluon two-point function
in Landau gauge:

$$\langle c^a(p)\, \bar{A}^b_\nu(-p)\rangle = \delta^{ab}\left(g_{\mu\nu} -
\frac{p_\mu p_\nu}{p^2}\right)\frac{u(p^2)}{p^2}$$

Lattice measurements in quenched SU(3) Landau gauge yield:

| Study | $u(0)$ | Method |
|---|---|---|
| Furui & Nakajima (2004) | $-0.713 \pm 0.014$ | $16^4$ lattice | 
| Boucaud et al. (2001) | $-0.78 \pm 0.02$ | $16^4$ lattice |
| Sternbeck et al. (2012) | $-0.82 \pm 0.03$ | $32^4$ lattice |

All lattice results give $u(0)$ **significantly above $-1$**, suggesting the
KO criterion in its strict form is **not satisfied** on the lattice in Landau gauge.
This is consistent with the observation that the lattice favours the *decoupling
solution* rather than the *scaling solution* (see `schwinger_dyson_propagator.md`).

**The Kugo–Ojima criterion $u(0) = -1$ is thus a contested, potentially gauge-artefact
sensitive criterion. It is not confirmed by current lattice data.**

---

## Stratum II — Field Consensus

The original Kugo–Ojima paper (1979) proves colour confinement in the BRST-quartet
mechanism under the assumption that the KO function satisfies $u(0) = -1$ **and**
that the Faddeev–Popov operator has no zero modes (i.e., no Gribov problem). Both
conditions are algebraic requirements in the continuum formulation.

The Gribov–Zwanziger approach (Zwanziger, 2003) provides an alternative mechanism
where confinement arises from restriction of the path integral to the Gribov region,
leading to the *horizon condition* $h(0) = d(N^2-1)$ (ghost enhancement). This is
distinct from the KO criterion but numerically consistent with the scaling solution.

Current field status: the decoupling vs. scaling dichotomy remains **unresolved**.
Both scenarios are consistent with confinement but via different mechanisms.

---

## Stratum III — UIDT Mapping

### BRST Cohomology Argument in v3.7.1

The confinement argument in v3.7.1 (Section 5.3, Appendix C.3) is purely
algebraic: physical states satisfy $Q_B |\text{phys}\rangle = 0$ and states
not in the BRST cohomology decouple. This is the **quartet mechanism** argument,
which is equivalent to the KO criterion in the continuum.

However, v3.7.1 does **not** compute the KO coefficient $u(0)$ from the UIDT
propagator equations. The Kugo–Ojima mechanism is invoked as a formal argument
only. **Evidence category: D.**

### Connection to $\Delta^*$ and $\gamma$

The canonical parameters $\Delta^* = 1.710 \pm 0.015$ GeV [A] and
$\gamma = 16.339$ [A−] appear in the kinetic vacuum structure of UIDT.
Neither is directly related to the KO coefficient $u(0)$ by any
currently derived equation within UIDT.

**A formal mapping between $u(0)$ and $\kappa$, $\Delta^*$, or $\gamma$
does not yet exist. This is an open problem [Category D].**

### Gribov Suppression in UIDT (v3.7.1, Section 12)

The Gribov copy contribution is estimated in v3.7.1 (Equation 66) as:

$$\frac{V_{\text{Gribov}}}{V_{\text{total}}} \sim \mathcal{O}\left(e^{-2\pi^2/\alpha_s}\right)
\sim \mathcal{O}(10^{-11})$$

using $\alpha_s \approx 0.34$. This estimate is **order-of-magnitude only** and
relies on the assumption that $\Delta^* \approx 1.710$ GeV provides the relevant
cutoff. The calculation is not a rigorous Gribov-region restriction but a
phenomenological suppression argument. **Evidence category: D.**

---

## Known Inconsistencies in Legacy Papers

| Document | Location | Issue | Status |
|---|---|---|---|
| `UIDT-v3.7.1-Complete.pdf` | Sec. 5.3, App. C.3 | KO mechanism invoked formally; $u(0)$ not computed | **Incomplete** |
| `UIDT-v3.7.1-Complete.pdf` | Remark 12.3 | Claims KO criterion coincides with UIDT fixed point in Landau gauge — no derivation given | **[TENSION ALERT]: lattice $u(0) \approx -0.8$, not $-1$** |
| `UIDT_Main_Paper_Ultra.pdf` | Sec. 4.3 | States modified Ward identities but does not verify KO condition | **Incomplete** |

**[TENSION ALERT]:**  
- Lattice value: $u(0) \approx -0.78$ to $-0.82$ (Sternbeck et al. 2012)  
- KO criterion requirement: $u(0) = -1$  
- UIDT v3.7.1 claim (Remark 12.3): KO satisfied at UIDT fixed point  
- Difference: $|{-1} - (-0.80)| = 0.20$ — significantly above zero  

This tension does not invalidate the BRST-quartet argument but means the
*quantitative* KO criterion is not satisfied on the lattice, and UIDT has not
yet provided a derivation that resolves this.

---

## Open Tasks

- [ ] Derive $u(p^2)$ from the UIDT ghost–gluon vertex at one loop, including
      the $\kappa$-dependent scalar-field correction.
- [ ] Check whether the UIDT fixed point $\kappa = 0.500$ [A] shifts $u(0)$
      towards $-1$ relative to pure Yang–Mills.
- [ ] Reconcile the algebraic BRST-quartet argument with the numerical lattice
      evidence for $u(0) \neq -1$.

---

## References

- T. Kugo & I. Ojima, *Local covariant operator formalism of non-Abelian
  gauge theories and quark confinement problem*, Prog. Theor. Phys. Suppl.
  66 (1979) 1–130. DOI: 10.1143/PTPS.66.1
- S. Furui & H. Nakajima, *Infrared features of unquenched lattice Landau
  gauge QCD*, Phys. Rev. D 73 (2006) 074503. arXiv:hep-lat/0511045
- A. Sternbeck et al., *Lattice evidence for the decoupling scenario of
  dynamical chiral symmetry breaking*, arXiv:1203.3557
- P. Boucaud et al., *Testing Landau gauge OPE on the lattice with a
  $\langle A^2 \rangle$ condensate*, Phys. Rev. D 63 (2001) 114003.
  arXiv:hep-ph/0101302
- D. Zwanziger, *No confinement without Coulomb confinement*,
  Phys. Rev. Lett. 90 (2003) 102001. arXiv:hep-lat/0209105
