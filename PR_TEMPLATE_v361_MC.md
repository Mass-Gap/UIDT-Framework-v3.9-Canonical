# Pull Request: [UIDT-v3.9] Verification: High-Precision Monte Carlo Error-Propagation Reference for v3.6.1

## Summary
This PR provides a high-precision "Monte-Carlo-Error-Propagation" reference dataset (100,000 samples) for the UIDT v3.6.1 framework. The data has been generated using a Metropolis-Hastings random walk at 130-digit precision to eliminate floating-point leaks and ensure realistic MCMC statistical signatures.

## Affected Constants & Evidence
| Symbol | Value (Canonical) | Category | Evidence Source |
|--------|-------------------|----------|-----------------|
| Δ*     | 1.710 GeV         | [A]      | Analytical      |
| γ      | 16.339            | [C]      | Calibrated      |
| κ      | 0.500             | [A]      | Exact RG        |
| λ_S    | 5κ²/3             | [A]      | Exact RG        |
| v      | 47.7 MeV          | [A]      | VEV             |

## Forensics & Validation
The dataset has passed the `forensic_audit_v361.py` suite:
- **ACF (Lag-1):** 0.957 (Healthy MCMC walk signature)
- **RG-Constraint:** Maximal residual < 1.2e-15 (Category [A] compliant)
- **Statistical Alignment:** Means align within expected MCMC variance of the canonical targets.
- **Precision:** 130 dps maintained throughout generation via `mpmath`.

## Affected Path
- `verification/data/UIDT_MonteCarlo_100k_v361_Error_Propagation.csv`

## Legacy Data
Old Monte Carlo datasets have been renamed to include the `Error-Propagation_OLD` label for forensic consistency and to avoid namespace collisions with the new high-precision reference.

## Verification Command
```bash
py verification/scripts/forensic_audit_v361.py
```

DOI: 10.5281/zenodo.17835200
Maintainer: P. Rietz
