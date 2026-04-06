# CE8 Coupling Constant — Complete Derivation

> **Evidence Category:** [A-] Phenomenological parameter  
> **Version:** v3.9 | **Author:** P. Rietz  
> **Source:** UIDT I (Foundations), UIDT IV (Field Theory), Ultra Main Paper

---

## Definition (SI-Canonical Form)

The CE8 coupling constant is defined as the ratio of the E8 symmetry dimension
to the vacuum information-density normalisation scale, expressed in SI units:

$$C_{E8} = \frac{\sqrt{G \cdot \hbar}}{c^{5/2}} \cdot \frac{N_{E8}}{f_{E8}}$$

where:
- $N_{E8} = 248$ — dimension of the exceptional Lie algebra $E_8$
- $f_{E8}$ — E8 information-density normalisation factor (calibrated from $\rho_{\text{vac}}$)
- $G = 6.674 \times 10^{-11}$ m³ kg⁻¹ s⁻² — Newton's gravitational constant
- $\hbar = 1.055 \times 10^{-34}$ J·s — reduced Planck constant
- $c = 2.998 \times 10^{8}$ m/s — speed of light

> **Dimensional note:** $\sqrt{G \hbar}/c^{5/2}$ has units of m s⁻¹, consistent
> with CE8 governing the emergent-time relation $dt = C_{E8} |\nabla S|$
> where $|\nabla S|$ carries units of (m)⁻¹.

---

## Connection to the Abstract Form

An earlier abstract form appeared in UIDT I–III:

$$C_{E8}^{\text{(abstract)}} = \frac{N_{E8}}{D_S} \cdot \sqrt{\frac{G}{c^4}} \qquad \text{[SUPERSEDED BY SI FORM]}$$

This is **not dimensionally equivalent** to the SI-canonical form above.
The two expressions coincide only under the identification
$D_S \equiv f_{E8} / \sqrt{\hbar}$, which is implied but not made explicit
in UIDT I. The SI-canonical form (with explicit $\hbar$) is the operative
definition in v3.9 and must be used for all numerical calculations.
The abstract form is retained here for historical traceability only and
must **not** be used in derivations or code.

---

## Numerical Value

Substituting SI constants:

$$C_{E8} = \frac{\sqrt{G \cdot \hbar}}{c^{5/2}} \cdot \frac{N_{E8}}{f_{E8}} \approx 8.1 \times 10^{-60} \text{ m/s}$$

with calibrated uncertainty $\delta C_{E8} = \pm 2.8 \times 10^{-60}$ m/s [A-].

> **Limitation L-CE8:** The CE8 value depends on the calibration of $f_{E8}$
> (equivalently $D_S$) from the vacuum energy density $\rho_{\text{vac}}$.
> This introduces an indirect dependence on cosmological calibration
> (Evidence Category [C]).

---

## Physical Role

CE8 governs the emergent-time relation in UIDT:

$$dt = C_{E8} \cdot |\nabla S|$$

This resolves the Wheeler-DeWitt frozen-time problem by defining time as the
irreversible flow of information entropy, not as an external parameter.

It also appears in the high-Q resonator prediction:

$$\frac{\delta f}{f_0} = C_{E8} \cdot |\nabla S|$$

with required precision $\delta f / f_0 \sim 10^{-18}$ for detection.

---

## E8 Symmetry Justification

The E8 Lie algebra (dimension 248) is the maximal exceptional simple Lie algebra.
In UIDT it serves as the symmetry group of the information-theoretic
ground state. The coupling to Yang-Mills occurs via the branching
$E_8 \supset SU(3) \times SU(2) \times U(1) \times \ldots$,
where the SU(3) sector produces the mass gap.

> **Epistemic Note:** The E8 embedding is a theoretical conjecture [E].
> The numerical CE8 value is phenomenologically calibrated [A-].
> These two layers MUST NOT be conflated.

---

## Version History

| Version | CE8 Value | Formula Form | Status |
|---------|-----------|--------------|--------|
| UIDT I  | $8.1 \times 10^{-60}$ m/s | Abstract ($N_{E8}/D_S \cdot \sqrt{G/c^4}$) | Introduced, $\hbar$ implicit |
| UIDT IV | $8.1 \times 10^{-60}$ m/s | SI-corrected ($\sqrt{G\hbar}/c^{5/2}$) | SI form canonical |
| UIDT VI | $8.1 \pm 2.8 \times 10^{-60}$ m/s | SI-canonical | Uncertainty added |
| v3.9    | $8.1 \pm 2.8 \times 10^{-60}$ m/s | SI-canonical | **Operative definition** |

---

## Cross-References

- `FORMALISM.md` — canonical Lagrangian context
- `GLOSSARY.md` — CE8 entry
- `modules/emergent_time/` — implementation
- `clay-submission/08_Documentation/` — Clay proof context
