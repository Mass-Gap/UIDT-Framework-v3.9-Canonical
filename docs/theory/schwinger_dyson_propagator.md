# Schwinger–Dyson Equations: Gluon and Ghost Propagators

**UIDT Framework v3.9** | Evidence Category: A (gap equation derivation), D (full SD closure)  
**Author:** P. Rietz | **Last updated:** 2026-03-25  
**DOI cross-reference:** 10.5281/zenodo.18003018 (v3.7.1 source paper)

---

## Purpose

This document derives and contextualises the Schwinger–Dyson (SD) equations for the
gluon and ghost propagators as they appear in the UIDT framework. It clarifies the
relationship between the effective gap equation used in the Banach proof (Theorem 8.3
of v3.7.1) and the full, non-perturbative SD system, and explicitly flags where the
legacy papers made unjustified approximations.

---

## Stratum I — Empirical Baseline

The dressed gluon propagator in Landau gauge has been studied extensively via
lattice QCD and functional methods. The key empirical findings are:

- **Infrared suppression:** The gluon dressing function $Z(p^2) = p^2 D(p^2)$
  saturates at a finite, non-zero value in the deep infrared, consistent with a
  dynamically generated gluon mass scale. Lattice results in four dimensions
  (quenched SU(3)) place the saturation scale near $p \approx 0.4$–$0.6$ GeV
  (Bogolubsky et al., 2009, arXiv:0901.0736; Ayala et al., 2012, arXiv:1208.0795).
- **Ghost dressing:** The ghost dressing function $G(p^2) = p^2 \Delta_c(p^2)$
  remains IR-enhanced but finite, consistent with the decoupling (massive) solution
  rather than the scaling solution (Boucaud et al., 2011, arXiv:1109.1936).
- **Gluon mass scale:** Phenomenological fits to lattice data yield an effective
  gluon mass $m_g \approx 0.5$–$0.7$ GeV (Cornwall, 1982; Aguilar & Papavassiliou,
  arXiv:0802.1870). This is **not** the same quantity as the Yang–Mills spectral
  gap $\Delta^* = 1.710 \pm 0.015$ GeV [A]; see the distinction note below.

---

## Stratum II — Field Consensus

The SD system for pure SU(N) Yang–Mills in Landau gauge reads (schematically):

$$\left[D^{-1}(p^2)\right]^{ab}_{\mu\nu} = \left[D_0^{-1}(p^2)\right]^{ab}_{\mu\nu} + \Pi^{ab}_{\mu\nu}(p^2)$$

$$\left[\Delta_c^{-1}(p^2)\right]^{ab} = \left[\Delta_{c,0}^{-1}(p^2)\right]^{ab} + \Sigma_c^{ab}(p^2)$$

where $\Pi_{\mu\nu}$ is the gluon self-energy and $\Sigma_c$ the ghost self-energy.
Both equations are **coupled** and require a truncation scheme to close. The two
leading truncation families are:

1. **Scaling solution** (Fischer, Alkofer, 2003): $D(p^2) \sim (p^2)^{2\kappa-1}$,
   $G(p^2) \sim (p^2)^{-\kappa}$ with $\kappa \approx 0.595$ in 4D. Implies $D(0) = 0$.
2. **Decoupling / massive solution** (Boucaud et al., Aguilar et al.): $D(0)$ finite
   and non-zero; $G(0)$ finite. Preferred by most recent lattice data.

The current field consensus (as of 2025) leans towards the decoupling solution.
**Neither solution constitutes a proof of the mass gap**; both are truncation-dependent
numerical results.

---

## Stratum III — UIDT Mapping

### Gap Equation in UIDT v3.7.1

The effective gap equation used in the Banach proof (v3.7.1, Proposition 8.1) is:

$$\Delta^2 = m_S^2 + \Sigma(\Delta^2)$$

with

$$\Sigma(0) = \frac{\kappa^2 \langle C \rangle}{4\pi^2}\left(1 - \ln\frac{\Delta^2}{\mu^2}\right)\frac{1}{16\pi^2}$$

where $\langle C \rangle = 0.277\,\text{GeV}^4$ is the gluon condensate (SVZ sum rules,
Shifman–Vainshtein–Zakharov, Nucl. Phys. B 147, 1979).

**Evidence category for this equation: D (predicted, not derived from closed SD system).**

This self-energy is **not** derived from the full coupled SD system. It is an
effective, one-loop level approximation using the background-field value of the
gluon condensate. The full SD closure — coupling gluon, ghost, and scalar-field
dressing functions self-consistently — has not been carried out within UIDT.

### Distinction: $\Delta^*$ vs. Gluon Dressing Mass

| Quantity | Symbol | Value | Category | Note |
|---|---|---|---|---|
| Yang–Mills spectral gap | $\Delta^*$ | $1.710 \pm 0.015$ GeV | A | Hamiltonian spectrum; NOT a particle mass |
| Effective gluon mass (phenomenological) | $m_g$ | $\approx 0.5$–$0.7$ GeV | B | From SD / lattice propagator fits; distinct quantity |
| Scalar field mass | $m_S$ | $1.705 \pm 0.015$ GeV | D | UIDT prediction; unverified |

**These are three distinct quantities.** Conflating $\Delta^*$ with $m_g$ (as was
implicitly done in some passages of `UIDT_Main_Paper_Ultra.pdf`, Section 12.3 and
Corollary 13.5) constitutes an epistemic error. The Ultra paper's value of
"$1580 \pm 120$ MeV" for the mass gap is inconsistent with the canonical ledger
value $\Delta^* = 1710 \pm 15$ MeV and reflects an earlier, superseded calibration.

---

## Known Inconsistencies in Legacy Papers

| Document | Location | Issue | Status |
|---|---|---|---|
| `UIDT_Main_Paper_Ultra.pdf` | Section 12.3, Corollary 13.5 | States gap = $1580 \pm 120$ MeV, inconsistent with canonical $1710 \pm 15$ MeV | **Superseded** |
| `UIDT_Main_Paper_Ultra.pdf` | Section 12.3 | Derives mass gap from $\langle SS \rangle_{\text{vacuum}}$ without closed SD derivation | **Incomplete** |
| `UIDT-v3.7.1-Complete.pdf` | Prop. 8.1 | Gap equation is an effective 1-loop approximation, not a closed SD result | **Acknowledged, L4** |
| `UIDT_Main_Paper_Ultra.pdf` | Section 14.5 | Claims "99.98% pion mass agreement" — no derivation given, no DOI cited | **[POTENTIAL ARTIFACT]** |

---

## Open Tasks

- [ ] Derive the full UIDT-coupled SD system including the $S$-field dressing correction
      to the gluon self-energy $\Pi_{\mu\nu}$.
- [ ] Verify decoupling-solution compatibility numerically (Category B target).
- [ ] Resolve the $\Delta^*$ vs. $m_g$ mapping: is $\Delta^*$ recoverable as a
      pole in the full SD propagator or only as a Hamiltonian spectral quantity?

---

## References

- I. L. Bogolubsky et al., *Lattice gluodynamics computation of Landau gauge Green's
  functions in the deep infrared*, Phys. Lett. B 676 (2009) 69–73.
  DOI: 10.1016/j.physletb.2009.04.076 | arXiv:0901.0736
- A. Ayala et al., *Quenching the quark propagator: Lattice vs. Dyson–Schwinger*,
  Phys. Rev. D 86 (2012) 074512. arXiv:1208.0795
- P. Boucaud et al., *The infrared behaviour of the pure Yang–Mills Green functions*,
  Few-Body Syst. 53 (2012) 387–436. arXiv:1109.1936
- A. C. Aguilar & J. Papavassiliou, *Gluon mass generation without seagull
  divergences*, Phys. Rev. D 81 (2010) 034003. arXiv:0802.1870
- M. A. Shifman, A. I. Vainshtein, V. I. Zakharov, Nucl. Phys. B 147 (1979) 385.
  DOI: 10.1016/0550-3213(79)90022-1
