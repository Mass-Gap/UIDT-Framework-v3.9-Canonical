# Torsion Self-Energy (E_T)

> **Evidence Category:** [C] — Phenomenological calibration  
> **Value:** E_T = 2.44 MeV  
> **Source:** v3.9 Constructive Synthesis (Missing Link Integration)  
> **Module:** [`lattice_topology.py`](../modules/lattice_topology.py)

---

## Definition

The **Torsion Self-Energy** (E_T) represents the binding energy contribution from the discrete torsion lattice structure to the vacuum frequency f_vac. It quantifies the energy difference between the pure geometric vacuum mode and the torsion-corrected lattice resonance.

### Physical Interpretation

In the UIDT torsion lattice framework (based on Nathen Miranda's Torsion Lattice Theory), the vacuum is modeled as a discrete 4D lattice with non-trivial torsion. The torsion introduces a small binding energy that shifts the vacuum frequency upward from its purely geometric value.

---

## How E_T Enters the Vacuum Frequency

The dynamically derived vacuum frequency f_vac is computed as:

$$f_{\text{vac}} = \frac{\Delta^*}{\gamma} + E_T$$

where:
- Δ* = 1.710 GeV — the Yang-Mills spectral gap [Category A]
- γ = 16.339 — the universal scaling invariant [Category A-]
- E_T = 2.44 MeV — the torsion self-energy [Category C]

### Numerical Result

```
f_vac = (1710 MeV / 16.339) + 2.44 MeV
      = 104.66 MeV + 2.44 MeV
      = 107.10 MeV
```

This 107.10 MeV vacuum frequency serves as the fundamental resonance scale for hadronic harmonic predictions (see `harmonic_predictions.py`).

---

## Code Reference

In [`modules/lattice_topology.py`](../modules/lattice_topology.py):

```python
self.TORSION_ENERGY_GEV = mpf('0.00244')  # 2.44 MeV [Category C]
```

Used in `TorsionLattice.calculate_vacuum_frequency()`:

```python
corrected_freq = base_freq + self.TORSION_ENERGY_GEV
```

---

## Limitations

- **[Category C]:** E_T = 2.44 MeV is phenomenologically determined — it is the observed difference between the geometric frequency (Δ/γ ≈ 104.66 MeV) and the lattice resonance frequency (≈ 107.10 MeV).
- **Not derived from first principles:** No analytic derivation from the torsion lattice Hamiltonian currently exists.
- **Upgrade path:** A first-principles derivation from torsion lattice dynamics would upgrade E_T from [C] to [A-].

---

## Related Documents

- [`CONSTANTS.md`](../CANONICAL/CONSTANTS.md) — Canonical parameter table
- [`limitations.md`](limitations.md) — Framework limitations (L1, L4)
- [`topological_quantization.tex`](../manuscript/topological_quantization.tex) — Vacuum topology manuscript
- [`lattice_topology.py`](../modules/lattice_topology.py) — Implementation
- [`harmonic_predictions.py`](../modules/harmonic_predictions.py) — Downstream usage in hadronic spectrum

---

**Citation:** Rietz, P. (2026). UIDT v3.9. DOI: 10.5281/zenodo.17835200
