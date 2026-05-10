# Spectral Function and Positivity Violations in UIDT

**UIDT Framework v3.9** | Evidence Category: A (OS4 proof for scalar sector), B (gluon positivity violation)  
**Author:** P. Rietz | **Last updated:** 2026-03-25  
**DOI cross-reference:** 10.5281/zenodo.18003018 (v3.7.1, Sections 3.5 and Appendix B.5)

---

## Purpose

This document analyses the Källén–Lehmann spectral function $\rho(\mu^2)$ for the
gluon propagator and the UIDT scalar field $S(x)$, with particular attention to
positivity violations as a confinement signal. It distinguishes where OS4 is
rigorously established within UIDT from where positivity violations are expected
but not yet derived.

---

## Stratum I — Empirical Baseline

Positivity violation of the gluon Schwinger function is a well-established
numerical result:

- The gluon Schwinger function $\Delta(t) = \int_{-\infty}^{+\infty}\frac{dp_4}{2\pi}
  e^{ip_4 t} D(p_4^2)$ exhibits a **zero crossing** at $t \approx 1$–$1.5$ fm and
  turns negative, signalling that the spectral density $\rho(\mu^2)$ is **not
  positive semi-definite**.
- This has been observed on the lattice (Cucchieri & Mendes, 2004, arXiv:hep-lat/0311019;
  Bowman et al., 2007, arXiv:hep-lat/0703022) and in truncated SD studies
  (Alkofer et al., 2004, arXiv:hep-ph/0301062).
- The ghost propagator does **not** show positivity violation and does not
  correspond to a physical asymptotic state — consistent with the BRST-quartet
  confinement mechanism.

---

## Stratum II — Field Consensus

The Källén–Lehmann representation for a physical scalar field states:

$$D(p^2) = \int_0^\infty d\mu^2\, \frac{\rho(\mu^2)}{p^2 + \mu^2}$$

with $\rho(\mu^2) \geq 0$ required for a physical particle (OS4 / positivity).

For confined degrees of freedom (gluons), $\rho(\mu^2)$ is **not** required to
be non-negative; its violation is a *sufficient* condition for confinement in
the sense that the corresponding excitation cannot appear as an asymptotic state
(Oehme & Zimmermann, 1980; Strocchi, 1978).

In the decoupling scenario (field consensus), the gluon propagator takes the
form:

$$D(p^2) = \frac{Z}{p^2 + m_g^2} + \text{(negative-spectral contributions)}$$

The negative-spectral tail ensures that the propagator is **not** of
Källén–Lehmann form with $\rho \geq 0$.

---

## Stratum III — UIDT Mapping

### OS4 for the Scalar Sector $S(x)$

The proof in v3.7.1 (Theorem 3.5, Appendix B.5) establishes OS4 (Reflection
Positivity) for the **scalar field** $S(x)$ and the **combined** UIDT path
integral. This is a **rigorous result [Category A]** within the UIDT framework.

The scalar propagator $G_S(p^2)$ is positive-definite and has a Källén–Lehmann
representation with $\rho_S(\mu^2) \geq 0$, consistent with $S(x)$ creating a
physical excitation with mass $m_S \approx \Delta^* = 1.710$ GeV [A].

### Gluon Positivity Violation

For the gauge field $A^a_\mu$, OS4 is satisfied by the **combined** measure
(ghost sector included, v3.7.1 Section 13 and Proposition 13.1). However,
this does **not** imply that the *gluon propagator alone* has a positive
spectral function. The expected situation — consistent with field consensus —
is that:

$$\rho_{\text{gluon}}(\mu^2) \not\geq 0$$

This is a **confinement signal** and is physically expected, but it has **not
been explicitly derived** from the UIDT effective action or verified numerically
within the framework.

**Evidence category: B (lattice-compatible expectation), D (UIDT-specific derivation absent).**

### Inconsistency Alert — Ultra Paper

The `UIDT_Main_Paper_Ultra.pdf` (Section 14.5) claims the spectral condition
implies $\Delta^* > 0$ from "vacuum gradients" $\langle S^2 \rangle$. This
derivation conflates the *scalar* spectral condition (well-defined) with the
*gluon* spectral gap (which requires a separate argument). The claim is
**incomplete** and does not constitute a derivation of the Yang–Mills mass gap
in the sense required by the Clay formulation.

---

## Summary Table

| Field | $\rho(\mu^2) \geq 0$? | Status in UIDT | Category |
|---|---|---|---|
| Scalar $S(x)$ | Yes (by construction) | Proven via OS4 | A |
| Gluon $A^a_\mu$ | No (expected, confinement signal) | Lattice-compatible; not derived in UIDT | B/D |
| Ghost $c^a$ | Not applicable (Grassmann) | BRST-quartet; decouples | A |

---

## Known Inconsistencies in Legacy Papers

| Document | Location | Issue | Status |
|---|---|---|---|
| `UIDT_Main_Paper_Ultra.pdf` | Sec. 14.5 | Conflates scalar and gluon spectral conditions | **Incomplete** |
| `UIDT_Main_Paper_Ultra.pdf` | Sec. 15.1 | Mass gap formula $\Delta^2 \sim k_B^2 c^4 \langle SS \rangle$ has wrong dimensions in SI units vs. natural units; no mpmath verification | **[POTENTIAL ARTIFACT]** |
| `UIDT-v3.7.1-Complete.pdf` | Sec. 13 | OS4 proof covers combined measure; gluon positivity violation not explicitly addressed | **Acknowledged (incomplete), L4** |

---

## Open Tasks

- [ ] Compute the UIDT gluon Schwinger function from the Banach fixed-point
      propagator and verify the zero crossing (Category B target).
- [ ] Derive an analytic condition on the UIDT coupling $\kappa$ for which
      the gluon spectral function acquires negative support.
- [ ] Verify whether the scalar pole at $m_S \approx \Delta^*$ is gauge-independent
      (Nielsen identity check for the scalar sector).

---

## References

- A. Cucchieri & T. Mendes, *What's up with IR gluon and ghost propagators in
  Landau gauge? A puzzling answer from huge lattices*, arXiv:hep-lat/0311019
- P. O. Bowman et al., *Unquenched quark propagator in Landau gauge*,
  Phys. Rev. D 71 (2005) 054507. arXiv:hep-lat/0703022
- R. Alkofer et al., *Quark confinement and the analyticity of the quark
  propagator*, arXiv:hep-ph/0301062
- R. Oehme & W. Zimmermann, *Quark and gluon propagators in quantum
  chromodynamics*, Phys. Rev. D 21 (1980) 471.
  DOI: 10.1103/PhysRevD.21.471
- F. Strocchi, *Locality and covariant operations in QFT*,
  Phys. Rev. D 17 (1978) 2010. DOI: 10.1103/PhysRevD.17.2010
