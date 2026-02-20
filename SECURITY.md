# Security Policy

## Data Sensitivity Notice

### Proprietary Research Workflows

The **UIDT-OS/** directory contains proprietary operational systems, local databases, and research workflows that are **NOT included** in this public repository.

**Important:**
- ❌ **DO NOT** request access to UIDT-OS
- ❌ **DO NOT** expect UIDT-OS files in this repository
- ✅ All necessary verification tools are provided in [verification/](verification/)

### What IS Included (Public)

This repository contains:
- ✅ Complete verification suite ([verification/scripts/](verification/scripts/))
- ✅ Clay Mathematics Institute submission ([clay-submission/](clay-submission/))
- ✅ Full documentation ([docs/](docs/))
- ✅ Reproducibility infrastructure (Docker, requirements.txt)

### What is NOT Included (Private)

The following are intentionally excluded via [.gitignore](.gitignore):
- ❌ UIDT-OS/ (427 files) - Proprietary operational system
- ❌ Local databases and configuration files
- ❌ Research strategy and workflow management
- ❌ Large archive files (available via [GitHub Releases](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/releases))

---

## Reporting Security Vulnerabilities

### Scope

Security concerns related to:
- Code execution vulnerabilities in verification scripts
- Dependency vulnerabilities in [verification/requirements.txt](verification/requirements.txt)
- Docker container security issues
- Sensitive data exposure

### How to Report

**Email:** badbugs.arts@gmail.com

**Subject Line:** `[SECURITY] UIDT v3.9 - [Brief Description]`

**Include:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested remediation (if available)

**Response Time:**
- Acknowledgment: Within 48 hours
- Assessment: Within 7 days
- Fix (if applicable): Within 30 days

---

## Supported Versions

| Version | Supported | Status |
|---------|-----------|--------|
| v3.9 | ✅ Yes | Current (Clean State) |
| v3.6.1 | ⚠️ Limited | Superseded by v3.9 |
| v3.3 | ❌ No | Withdrawn (formatting errors) |
| < v3.3 | ❌ No | Archived |

**Recommendation:** Always use the latest version (v3.9) for security and accuracy.

---

## Dependency Security

### Python Dependencies

The project uses standard scientific computing libraries. See [verification/requirements.txt](verification/requirements.txt):

- `numpy>=1.24.0`
- `scipy>=1.10.0`
- `mpmath>=1.3.0`
- `matplotlib>=3.7.0`

**Security Practices:**
- 🔒 Dependencies are pinned to minimum versions
- 🔍 Regular updates for security patches
- ✅ No proprietary or closed-source dependencies

### Docker Security

The [verification/docker/Dockerfile](verification/docker/Dockerfile) uses:
- **Base Image:** `python:3.10-slim` (official Python image)
- **No root execution:** Container runs as non-privileged user
- **Minimal attack surface:** Only scientific computing dependencies

**Best Practices:**
```bash
# Build with security scanning
docker build --no-cache -t uidt-verify verification/docker/

# Run with limited permissions
docker run --read-only --tmpfs /tmp uidt-verify
```

---

## Data Integrity

### Verification Checksums

All verification scripts produce deterministic results. To verify integrity:

```bash
# Run verification
python verification/scripts/UIDT-3.6.1-Verification.py

# Expected output:
# Max Residual: < 1.2e-40
# Overall Consistency: ✅ PASS
```

### Clay Submission Integrity

The complete Clay Mathematics Institute submission package includes SHA256 manifests:

```bash
# Verify checksums
cat clay-submission/04_Certificates/SHA256_MANIFEST.txt
```

---

## License Compliance

### CC BY 4.0 License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

**You are free to:**
- ✅ Share — copy and redistribute
- ✅ Adapt — remix, transform, build upon

**Under the following terms:**
- 📝 **Attribution** — Must give appropriate credit
- 🔗 **Link to license** — Must provide link to CC BY 4.0
- ⚠️ **Indicate changes** — Must indicate if modifications were made
- ❌ **No endorsement** — May not suggest author endorsement

**Commercial Use:** ✅ Allowed (with attribution)

---

## Contact

**Primary Contact:** Philipp Rietz
**Email:** badbugs.arts@gmail.com
**ORCID:** [0009-0007-4307-1609](https://orcid.org/0009-0007-4307-1609)
**DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

For general questions (not security-related), please open a [GitHub Issue](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/issues).

---

**Last Updated:** 2026-02-05
**Version:** UIDT v3.9 Canonical
