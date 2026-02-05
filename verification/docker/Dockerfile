# --- UIDT v3.6.1 Master Container (Clean State) ---
# Base Image: Python 3.10 Slim (Scientific Standard for Reproducibility)
FROM python:3.10-slim

# ==============================================================================
# SCIENTIFIC METADATA (OCI ANNOTATIONS)
# ==============================================================================
LABEL maintainer="Philipp Rietz <badbugs.arts@gmail.com>"
LABEL org.opencontainers.image.title="UIDT Verification Suite"
LABEL org.opencontainers.image.description="Official verification container for UIDT v3.6.1 (Canonical Clean State)"
LABEL org.opencontainers.image.version="3.6.1"
LABEL org.opencontainers.image.licenses="CC-BY-4.0"
LABEL org.opencontainers.image.url="https://doi.org/10.5281/zenodo.17835200"
LABEL org.opencontainers.image.source="https://github.com/badbugsarts-hue/UIDT-Framework-V3.2-Canonical"

# ==============================================================================
# ENVIRONMENT CONFIGURATION
# ==============================================================================
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr (faster logs)
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# ==============================================================================
# DEPENDENCIES
# ==============================================================================
# Install system dependencies required for numerical libraries (numpy/scipy)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Utilizing Docker cache layers for efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==============================================================================
# SOURCE CODE INJECTION
# ==============================================================================
# Copy the entire project context into the container
COPY . .

# ==============================================================================
# RUNTIME EXECUTION
# ==============================================================================
# Default Command: Executes the v3.6.1 Verification Suite
# Ensures that every container start performs a fresh audit of the 3-Equation System.
CMD ["python", "UIDT-3.6.1-Verification.py"]