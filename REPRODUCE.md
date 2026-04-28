# Reproduction Protocol — UIDT v3.9 Canonical

> **DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)
> **Author:** Philipp Rietz (ORCID: [0009-0007-4307-1609](https://orcid.org/0009-0007-4307-1609))
> **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## Prerequisites

- **Python:** ≥ 3.10
- **OS:** Linux, macOS, or Windows
- **Disk:** < 200 MB

---

## Method A: Local Reproduction (3 commands)

```bash
# 1. Clone the repository
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical
cd UIDT-Framework-v3.9-Canonical

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full verification suite
python -m pytest verification/ -v --tb=short
```

### Expected Output

```
57 passed in ~9s
```

All residuals for Category A claims must satisfy: `|expected - actual| < 10⁻¹⁴`

### Individual Verification Scripts

```bash
# Primary solver (Four-Pillar Verification)
python verification/scripts/UIDT_Master_Verification.py

# Legacy v3.6.1 backward-compatibility check
python verification/scripts/UIDT-3.6.1-Verification.py

# CSF-UIDT Unification verification
python verification/scripts/verify_csf_unification.py
```

---

## Method B: Docker Reproduction (1 command)

```bash
docker build -t uidt-verify .
docker run --rm uidt-verify
```

This executes the full pytest suite inside an isolated Python 3.10 container.

### SLSA Level 3 Provenance & Nightly Checks
UIDT v3.9 artifacts are strictly signed for integrity via **Sigstore / Cosign** in our automated GitHub Actions workflow (`release.yml`). 
To verify provenance:
```bash
# Verify the Docker image signature
cosign verify ghcr.io/mass-gap/uidt-framework-v3.9-canonical:latest \
  --certificate-identity "https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/.github/workflows/release.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```
The repository also maintains a strict nightly Docker reproducibility cron job to ensure upstream dependency changes do not break verification constraints.

---

## Method C: Clay Submission Package

The `clay-submission/` directory contains a self-contained, auditable reproduction environment:

```bash
cd clay-submission
docker build -f Dockerfile.clay_audit -t uidt-clay .
docker run --rm uidt-clay
```

See `clay-submission/REPRODUCE.md` for the dedicated Clay submission protocol.

---

## Verification Criteria

| Category | Requirement | Threshold |
|----------|-------------|-----------|
| **A** (Internal Theorem) | Residuals from Banach fixed-point closure | < 10⁻¹⁴ |
| **B** (Lattice Consistent) | z-score vs. lattice QCD benchmarks | < 1σ |
| **C** (Calibrated) | Consistency with DESI/JWST/ACT data | Within stated uncertainties |
| **D** (Prediction) | Falsification thresholds documented | See Kill-Switch Matrix |

---

## Numerical Precision

All core computations use `mpmath` with 80-digit precision:

```python
import mpmath as mp
mp.dps = 80  # Set locally in EVERY module. Never mock. Never centralise.
```

Standard Python `float` (64-bit IEEE 754) is **not sufficient** for Category A verification.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: mpmath` | Run `pip install -r requirements.txt` |
| Tests fail with precision errors | Ensure `mp.dps = 80` is set; do not use `float` |
| Docker build fails | Ensure Docker is installed and running |

---

## Contact

For reproduction issues, please open a [Replication Report](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/issues/new?template=replication_report.md) using the provided issue template.

---

*Philipp Rietz — badbugs.arts@gmail.com — DOI: 10.5281/zenodo.17835200*
