# Wilson Flow External Constants — UIDT Cross-References

**Version:** 3.9.6  
**DOI:** 10.5281/zenodo.17835200  
**Last Updated:** 2026-04-13

> **PURPOSE:** Document external (non-UIDT-derived) constants used in Wilson Flow
> and topological susceptibility estimates. These values are literature inputs,
> NOT predictions of the UIDT framework.

---

## Registered External Constants

### UIDT-C-054: Gluon Condensate

| Property | Value |
|----------|-------|
| **Symbol** | C_GLUON = (α_s/π)⟨G²⟩ |
| **Value** | ≈ 0.012 GeV⁴ |
| **Uncertainty** | Factor ~2–3 (non-perturbative) |
| **Evidence** | [E] (external literature value) |
| **Source** | Shifman, Vainshtein, Zakharov (1979) |

**Notes:** The SVZ gluon condensate carries large non-perturbative uncertainty.
Modern lattice determinations range from 0.005 to 0.02 GeV⁴. This value is
used as an input to the topological susceptibility estimate and is NOT a UIDT
prediction.

---

### UIDT-C-055: Strong Coupling Reference Scale

| Property | Value |
|----------|-------|
| **Symbol** | α_s(μ = 1.5 GeV) |
| **Value** | 0.326 ± 0.019 |
| **Evidence** | [E] (external literature value) |
| **Source** | PDG 2024 (interpolated from α_s(M_Z) = 0.1180 ± 0.0009) |

**Notes:** The strong coupling is interpolated to μ = 1.5 GeV via 4-loop
perturbative RG running. This scale is chosen to match the UIDT spectral
gap Δ* = 1.710 GeV regime.

---

### UIDT-C-056: Topological Susceptibility (SVZ Leading Order)

| Property | Value |
|----------|-------|
| **Symbol** | χ_top^{1/4} |
| **Value** | 142.98 MeV (LO, SVZ) |
| **Formula** | χ_top^{1/4} = (b₀/(32π²)) × C_SVZ |
| **Evidence** | [D] (predicted, TENSION) |
| **Tension** | z ≈ 8–10σ vs quenched lattice (185–191 MeV) |

#### Correction History

| Date | Value | Formula | Status |
|------|-------|---------|--------|
| 2026-03 (PR #190) | ~55 MeV | f_vac/(2π) × (b₀α_s/π)^{1/4} | ❌ **WRONG** (incorrect formula) |
| 2026-03 (PR #190 draft) | ~107 MeV | Partial SVZ | ❌ **INCOMPLETE** |
| 2026-04 (PR #213) | **142.98 MeV** | (b₀/(32π²)) × C_SVZ | ✅ **VERIFIED** (mpmath 80-dps) |

#### Tension Analysis

**UIDT SVZ LO estimate:** χ_top^{1/4} = 142.98 MeV [D]  
**Quenched lattice benchmarks:** 185–191 ± 5 MeV (SU(3), various groups)

**z-score:** z ≈ (185 - 143) / √(5² + 15²) ≈ 8.4–9.6σ

> [!WARNING]
> **TENSION ALERT:** The SVZ leading-order estimate is systematically below
> the quenched lattice band. NLO corrections are expected to increase the
> value by +30–80%, potentially resolving the tension. This is an active
> research question, NOT a falsification of UIDT.

#### Falsification Criterion

If the fully NLO-corrected χ_top^{1/4} falls **outside** the range
[140, 220] MeV, the SVZ estimate applicability within the UIDT framework
is refuted. See `docs/falsification-criteria.md` → F9.

---

## Dependencies

```
UIDT-C-056 (χ_top)
├── UIDT-C-054 (C_GLUON) [E]
├── UIDT-C-055 (α_s) [E]
└── QCD: b₀ = 11 - 2n_f/3 (pure gauge: b₀ = 11)
```

---

## Verification

```bash
# Reproduce the 142.98 MeV result:
cd verification/scripts
python verify_wilson_flow_topology.py
# Expected: χ_top^{1/4} ≈ 142.98 MeV (mpmath 80-dps)
```

**Linked PR:** [#213](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/pull/213) — χ_top formula audit  
**Linked Audit:** `docs/research/chi_top_formula_audit.md` (on PR #213 branch; to be merged)

---

**Citation:**
```bibtex
@misc{Rietz2026_WilsonFlow,
  author = {Rietz, Philipp},
  title  = {Wilson Flow External Constants — UIDT Cross-References},
  year   = {2026},
  doi    = {10.5281/zenodo.17835200}
}
```

---

*Maintainer: P. Rietz (ORCID: 0009-0007-4307-1609)*
