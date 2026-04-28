# ============================================================================
# UIDT v3.9 Canonical — Reproducible Verification Environment
# DOI: 10.5281/zenodo.17835200
# Author: P. Rietz (ORCID: 0009-0007-4307-1609)
# ============================================================================
# This Dockerfile provides a minimal, isolated environment to reproduce
# all UIDT verification results. Usage:
#   docker build -t uidt-verify .
#   docker run --rm uidt-verify
# ============================================================================

FROM python:3.10-slim

LABEL maintainer="P. Rietz <badbugs.arts@gmail.com>"
LABEL description="UIDT v3.9 Canonical Verification Environment"
LABEL org.opencontainers.image.source="https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical"
LABEL org.opencontainers.image.licenses="CC-BY-4.0"
LABEL doi="10.5281/zenodo.17835200"

WORKDIR /uidt

# Install dependencies first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy repository contents (respects .dockerignore if present)
COPY core/ core/
COPY modules/ modules/
COPY verification/ verification/
COPY CANONICAL/ CANONICAL/
COPY LEDGER/ LEDGER/

# Run full verification suite as default command
CMD ["python", "-m", "pytest", "verification/", "-v", "--tb=short"]
