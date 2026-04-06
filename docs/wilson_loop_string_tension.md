# Wilson Loop and String Tension in UIDT

**UIDT Framework v3.9** | Evidence Category: B (lattice string tension), D (UIDT connection)  
**Author:** P. Rietz | **Last updated:** 2026-03-25  
**DOI cross-reference:** 10.5281/zenodo.18003018 (v3.7.1, Theorem G.3)

---

## Purpose

This document addresses the Area Law for Wilson loops within the UIDT framework.
It collects the empirical lattice values for the string tension $\sigma$, maps them
to the canonical UIDT parameter $\Delta^* = 1.710 \pm 0.015$ GeV [A], and
explicitly flags where the legacy paper argument (v3.7.1, Appendix G.3) is
qualitative rather than quantitative.

---

## Stratum I — Empirical Baseline

The string tension $\sigma$ is measured from the slope of the static quark–antiquark
potential $V(r) = \sigma r - \pi/(12r) + \text{const}$ (Luscher term) on the lattice.

| Study | $\sqrt{\sigma}$ | Method | DOI / arXiv |
|---|---|---|---|
| Bali & Schilling (1993) | $440 \pm 20$ MeV | SU(3) quenched, Wilson | 10.1103/PhysRevD.47.661 |
| Necco & Sommer (2002) | $465 \pm 5$ MeV | Continuum extrapolation | arXiv:hep-lat/0108008 |
| Boucaud et al. (2003) | $445 \pm 15$ MeV | Improved Wilson fermions | arXiv:hep-ph/0310006 |
| FLAG 2024 average | $440$–$470$ MeV | Review (quenched) | arXiv:2411.04268 |

Conventionally: $\sigma \approx (440\,\text{MeV})^2 \approx 0.193\,\text{GeV}^2$.

---

## Stratum II — Field Consensus

The Wilson loop for a planar rectangular loop $C$ of area $A = R \times T$ satisfies
the Area Law in the confining phase:

$$\langle W(C) \rangle \sim \exp(-\sigma \cdot A)\quad (R,\, T \to \infty)$$

This is a well-established non-perturbative result, confirmed numerically by lattice
Monte Carlo for all compact non-Abelian gauge groups. The Area Law is equivalent to
linear confinement of colour charges at large separations.

The Luscher–Weisz proof (2002, arXiv:hep-lat/0207003) establishes the Area Law
for SU(N) at strong coupling; extension to the physical weak-coupling continuum limit
remains a subject of ongoing rigorous work.

---

## Stratum III — UIDT Mapping

### What v3.7.1 Claims

Appendix G.3 (Theorem G.3, Corollary G.4) asserts:

> *"In a confining phase with mass gap $\Delta^* > 0$, the Wilson loop satisfies
> $W(C) \sim \exp(-\sigma\,\text{Area}(C))$ for large loops, where $\sigma > 0$
> is the string tension."*

This claim is **qualitatively correct** — a mass gap and exponential clustering
imply confinement in the sense of an area law (Seiler, 1982; Fredenhagen & Marcu,
1986). However, the argument in v3.7.1 provides **no numerical value for $\sigma$**
and no derivation connecting $\sigma$ to $\Delta^*$ quantitatively.

### Proposed Dimensional Relation (Category D — Prediction)

A natural dimensional estimate for the string tension from the spectral gap is:

$$\sigma \sim \frac{(\Delta^*)^2}{C_{\text{geom}}}$$

where $C_{\text{geom}}$ is a dimensionless geometric factor. With
$\Delta^* = 1.710$ GeV and the empirical $\sqrt{\sigma} \approx 0.44$ GeV:

$$C_{\text{geom}} = \frac{(\Delta^*)^2}{\sigma} = \frac{(1.710)^2}{(0.440)^2} \approx 15.1$$

This factor is **not derived** from UIDT first principles. Its value is noted here
for future work.

**Evidence category: D.** This is a dimensional estimate only. No derivation from
the UIDT gap equation or the Banach fixed-point theorem yields $\sigma$ analytically.

### Relation to Kugo–Ojima / Gribov Horizon

Confinement in UIDT is argued via the Kugo–Ojima mechanism (v3.7.1, Section 5.3
and Appendix C.3): physical states lie in the BRST cohomology $H_{\text{phys}} =
\ker Q / \text{im}\, Q$ and all colour-non-singlet states are BRST-exact.
This is an **algebraic** confinement criterion, distinct from the
**dynamical** string-tension confinement measured by the Wilson loop. The
connection between the two criteria is non-trivial and is an open problem.

---

## Known Inconsistencies in Legacy Papers

| Document | Location | Issue | Status |
|---|---|---|---|
| `UIDT-v3.7.1-Complete.pdf` | Theorem G.3 | States $\sigma > 0$ without computing $\sigma$ from UIDT parameters | **Incomplete** |
| `UIDT_Main_Paper_Ultra.pdf` | Section 8.1 | Claims Area Law "confirmed in 2D lattice simulations with nonlinear $N_{\text{dof}}$ jump" — no DOI, no quantitative result | **[POTENTIAL ARTIFACT]** |
| `UIDT_Main_Paper_Ultra.pdf` | Section 7.4 | Introduces a lattice UIDT action without demonstrating continuum limit or Area Law recovery | **Incomplete / Category D** |

---

## Open Tasks

- [ ] Derive an analytic expression for $\sigma$ from the UIDT effective action
      (post-auxiliary-field elimination).
- [ ] Perform quenched lattice simulation of the UIDT-discretised action and
      measure $\langle W(C) \rangle$ to extract $\sigma$ (target: Category B).
- [ ] Prove or disprove the equivalence between BRST-algebraic confinement
      and Area-Law confinement within the UIDT framework.

---

## References

- G. S. Bali & K. Schilling, *Running coupling and the $\Lambda$-parameter from
  SU(3) lattice simulations*, Phys. Rev. D 47 (1993) 661.
  DOI: 10.1103/PhysRevD.47.661
- S. Necco & R. Sommer, *The $N_f = 0$ heavy quark potential from short to
  intermediate distances*, Nucl. Phys. B 622 (2002) 328. arXiv:hep-lat/0108008
- M. Luscher & P. Weisz, *Quark confinement and the bosonic string*,
  JHEP 07 (2002) 049. arXiv:hep-lat/0207003
- FLAG Collaboration (2024), arXiv:2411.04268
- E. Seiler, *Gauge theories as a problem of constructive quantum field theory
  and statistical mechanics*, Lecture Notes Phys. 159 (1982).
- K. Fredenhagen & M. Marcu, *Dual interpretation of order parameters for
  lattice gauge theories*, Commun. Math. Phys. 92 (1983) 81.
