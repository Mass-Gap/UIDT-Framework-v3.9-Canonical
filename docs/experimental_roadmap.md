# Experimental Roadmap — UIDT v3.9

> **Evidence Categories:** [D] Predictions | [B] Lattice compatible  
> **Version:** v3.9 | **Source:** Ultra Main Paper §9.5, §11.4; Master Report 2 §12–13

---

## Tier 1 — Near-Term (1–3 Years, 2026–2028)

| Experiment | Observable | UIDT Prediction | Current Sensitivity | Required |
|------------|-----------|----------------|---------------------|----------|
| BESIII (Beijing) | Glueball spectrum $0^{++}$ | $1710 \pm 15$ MeV [A] | ±30 MeV | ±10 MeV |
| LHC Run 3 (ATLAS/CMS) | W/Z boson mass shift | $\delta m_{W/Z} \sim 1.2 \times 10^{-6}$ GeV | ±12 MeV | ±0.1 MeV |
| Cryogenic Resonator | Entropy gradient coupling | $\delta f/f_0 \sim 10^{-18}$ | $10^{-15}$ | $10^{-18}$ |
| Lattice QCD (Collaboration) | $0^{++}$ glueball / $2^{++}$ ratio | UIDT: 1.04 ± 0.02 | 1.0 ± 0.1 | ±0.02 |

## Tier 2 — Medium-Term (3–7 Years, 2028–2032)

| Experiment | Observable | UIDT Prediction | Facility |
|------------|-----------|----------------|----------|
| Electron-Ion Collider (EIC) | Gluon polarization structure | Modified $\Delta G$ | BNL |
| FCC-ee (Z-pole) | Z boson mass precision | $\delta m_Z \sim 10^{-4}$ GeV | CERN |
| CMB Spectral Distortions | Information-theoretic corrections | $\delta n_s \sim 0.001$ | PIXIE 2030 |
| Atomic Interferometry | Entropy gradient: $a/g$ | $10^{-12}$ | Various |
| DESI DR3+ | Dark energy EOS $w_a$ | $w_a = +0.03$ (UIDT CSF) [C] | DESI |

## Tier 3 — Long-Term (>7 Years, post-2033)

| Experiment | Observable | UIDT Prediction | Facility |
|------------|-----------|----------------|----------|
| FCC-hh | High-energy glueball production | Direct $0^{++}$ discovery | CERN |
| Gravitational Wave Detectors | Modified dispersion relations | $\delta v_{\text{GW}}/c \sim 10^{-20}$ | LISA, ET |
| Quantum Gravity Experiments | Information field quantization | QUIDTs | TBD |

## Falsification Criteria

UIDT is falsified if **any** of the following hold:

1. Glueball $0^{++}$ mass measured at $< 1650$ MeV or $> 1780$ MeV with $5\sigma$ confidence
2. No entropy gradient coupling detected at resonator sensitivity $\delta f/f_0 = 10^{-18}$
3. $w_a$ measured as $0.00 \pm 0.005$ (i.e., perfectly consistent with $\Lambda$CDM)
4. RG fixed point $5\kappa^2 = 3\lambda_S$ violated in lattice simulation at $> 3\sigma$

> **Limitation Acknowledgement:** Several Tier 1 predictions (especially the
> resonator experiment) require next-generation experimental capabilities not
> yet available. Current data are compatible with UIDT but do not constitute
> confirmation.

## Cross-References

- `docs/falsification_criteria.md` — complete falsification matrix
- `FORMALISM.md` — canonical predictions
- `clay-submission/08_Documentation/` — Clay submission experimental section
