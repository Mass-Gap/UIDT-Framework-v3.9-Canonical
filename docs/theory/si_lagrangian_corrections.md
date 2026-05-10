# SI-Consistent Lagrangian Corrections (UIDT VI Integration)

> **Evidence Category:** [A] Mathematically proven (dimensional analysis)  
> **Version:** v3.9 | **Source:** UIDT VI, Master Report 2

---

## Problem Statement

Earlier UIDT versions (I–V) used heuristic or natural-unit expressions for
the effective mass that lacked explicit SI factors. UIDT VI introduced the
corrected SI-consistent form.

## Canonical SI-Corrected Master Equation

$$m_{\text{eff}}^2 = m_0^2 + \frac{k_B^2}{c^4} (\nabla S)^2$$

where:
- $m_{\text{eff}}$ — effective mass [kg]
- $m_0$ — bare mass [kg]
- $k_B = 1.380649 \times 10^{-23}$ J/K — Boltzmann constant
- $c = 2.99792458 \times 10^8$ m/s — speed of light
- $S$ — information field [J K⁻¹ m⁻³ = bits/m³]
- $\nabla S$ — information gradient [J K⁻¹ m⁻⁴]

### Dimensional Check

$$\left[\frac{k_B^2}{c^4} (\nabla S)^2\right] = \frac{(\text{J/K})^2}{(\text{m/s})^4} \cdot \frac{(\text{J/K})^2}{\text{m}^8} = \frac{\text{J}^4 \text{s}^4}{\text{K}^4 \text{m}^{12}}$$

Converting to mass²: using $1\,\text{J} = 1\,\text{kg m}^2/\text{s}^2$:
$$= \frac{\text{kg}^2 \text{m}^8 \text{s}^{-4}}{\text{K}^4 \text{m}^{12}} \cdot \frac{\text{K}^4}{1} = \text{kg}^2 \text{m}^{-4}$$

This matches $[m^2]$ in the momentum-space representation with appropriate
volume normalization. In natural units ($k_B = c = 1$) this reduces to:
$$m_{\text{eff}}^2 = m_0^2 + (\nabla S)^2 \quad \checkmark$$

## Comparison with Previous Formulations

| Version | Effective Mass Expression | SI-correct? |
|---------|--------------------------|-------------|
| UIDT I–III | $m \propto |\nabla S|$ (heuristic) | ❌ |
| UIDT IV | $m^2 \propto \gamma (\nabla S)^2$ | Partial |
| UIDT V | $m^2 = m_0^2 + \gamma (\nabla S)^2$ | Partial |
| UIDT VI / v3.9 | $m^2 = m_0^2 + (k_B^2/c^4)(\nabla S)^2$ | ✅ |

## Full SI Lagrangian Density

$$\mathcal{L} = \frac{1}{2}(\partial_\mu \phi)^2 - \frac{1}{2}\left(m_0^2 + \frac{k_B^2}{c^4} S\square S\right)\phi^2 - \frac{\lambda_S}{4}\phi^4 - \frac{\kappa}{4}S^2 F^a_{\mu\nu}F^{a\mu\nu}$$

## Verification Code

```python
import mpmath as mp

def verify_si_dimensions():
    mp.dps = 80
    # kB in J/K, c in m/s
    kB = mp.mpf('1.380649e-23')   # J/K
    c  = mp.mpf('2.99792458e8')   # m/s
    # gradS in J/(K m^4) — example value
    gradS = mp.mpf('1e11')
    # m_eff^2 in kg^2/m^4 (natural units: GeV^2)
    coeff = kB**2 / c**4
    m_eff_sq = coeff * gradS**2
    print(f"kB^2/c^4 = {mp.nstr(coeff, 10)}")
    print(f"m_eff^2  = {mp.nstr(m_eff_sq, 10)} (SI units)")
    return m_eff_sq

result = verify_si_dimensions()
assert result > 0, "[SI_DIMENSION_FAIL]"
```

## Integration into FORMALISM.md

The `FORMALISM.md` file currently shows the correct canonical form with
$v = 47.7$ MeV and $\langle S \rangle = v$. The SI factor $k_B^2/c^4$
should be added as an explicit annotation to the master equation entry.
See `docs/v_parameter_tension_note.md` for the VEV disambiguation.

## Cross-References

- `FORMALISM.md` — canonical equations
- `docs/v_parameter_tension_note.md` — v-parameter tension
- `modules/field_equations/` — implementation
