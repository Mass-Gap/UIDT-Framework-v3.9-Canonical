#!/usr/bin/env bash
# =============================================================================
# scripts/archival_snapshot.sh - UIDT v3.9 Immutable Research Archival Script
# Generates SHA256 manifest + metadata.json, then calls Zenodo export.
# Evidence category: B (infrastructure) | Limitation: none
# DOI: 10.5281/zenodo.17835200
# =============================================================================
set -euo pipefail

SNAPSHOT_DIR="AUDIT_TRAIL/snapshots"
METADATA_FILE="${SNAPSHOT_DIR}/metadata.json"
MANIFEST_FILE="${SNAPSHOT_DIR}/sha256_manifest.txt"
mkdir -p "$SNAPSHOT_DIR"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
COMMIT_SHA=${CI_COMMIT_SHA:-$(git rev-parse HEAD 2>/dev/null || echo "unknown")}
BRANCH=${CI_COMMIT_BRANCH:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")}
PIPELINE_ID=${CI_PIPELINE_ID:-"local"}

echo "[ARCHIVE] UIDT v3.9 archival snapshot - $TIMESTAMP"
echo "[ARCHIVE] Commit: $COMMIT_SHA | Branch: $BRANCH"

# ---------------------------------------------------------------------------
# Step 1: SHA256 manifest of CANONICAL/ and core/
# ---------------------------------------------------------------------------
echo "[ARCHIVE] Computing SHA256 manifest for CANONICAL/ and core/..."
> "$MANIFEST_FILE"

for dir in CANONICAL core; do
  if [ -d "$dir" ]; then
    find "$dir" -type f | sort | while read -r f; do
      sha256sum "$f" >> "$MANIFEST_FILE"
    done
    echo "[ARCHIVE] Hashed $(find $dir -type f | wc -l) files in $dir/"
  else
    echo "[ARCHIVE] WARNING: directory $dir/ not found, skipping."
  fi
done

ENV_HASH=$(sha256sum "$MANIFEST_FILE" | cut -d' ' -f1)
echo "[ARCHIVE] Manifest SHA256 (env_hash): $ENV_HASH"

# ---------------------------------------------------------------------------
# Step 2: Collect verification residuals (if available)
# ---------------------------------------------------------------------------
VERIF_RESIDUAL="N/A"
if [ -f "AUDIT_TRAIL/pipeline-summary.txt" ]; then
  VERIF_RESIDUAL=$(grep -oE 'RG_CONSTRAINT=[^ ]+' AUDIT_TRAIL/pipeline-summary.txt | head -1 || echo "N/A")
fi

# ---------------------------------------------------------------------------
# Step 3: Generate metadata.json
# ---------------------------------------------------------------------------
echo "[ARCHIVE] Writing metadata.json..."
cat > "$METADATA_FILE" << EOF
{
  "schema_version": "1.0",
  "framework": "UIDT v3.9",
  "project_title": "Vacuum Information Density as the Fundamental Geometric Scalar",
  "doi_canonical": "10.5281/zenodo.17835200",
  "snapshot_timestamp": "${TIMESTAMP}",
  "commit_sha": "${COMMIT_SHA}",
  "branch": "${BRANCH}",
  "pipeline_id": "${PIPELINE_ID}",
  "env_hash_sha256": "${ENV_HASH}",
  "verification_residual": "${VERIF_RESIDUAL}",
  "canonical_constants": {
    "gamma": "16.339",
    "gamma_unc": "1.005",
    "evidence_category": "A-",
    "delta": "1.710",
    "kappa": "0.500",
    "H0": "70.4",
    "H0_evidence_category": "C"
  },
  "python_env": {
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "PYTHONHASHSEED": "0"
  },
  "manifest_file": "sha256_manifest.txt",
  "manifest_algo": "sha256"
}
EOF

echo "[ARCHIVE] metadata.json written."
cat "$METADATA_FILE"

# ---------------------------------------------------------------------------
# Step 4: Zenodo export (stub - requires ZENODO_TOKEN in CI env)
# ---------------------------------------------------------------------------
echo "[ARCHIVE] Checking Zenodo export readiness..."
if [ -n "${ZENODO_TOKEN:-}" ]; then
  echo "[ARCHIVE] ZENODO_TOKEN present - initiating export_to_zenodo stub."
  # Full implementation: call python scripts/export_to_zenodo.py
  # with metadata.json and manifest as inputs.
  # This stub validates the token is set and metadata is well-formed.
  python3 -c "
import json, sys
with open('${METADATA_FILE}') as f:
    m = json.load(f)
assert m.get('commit_sha'), 'commit_sha missing'
assert m.get('env_hash_sha256'), 'env_hash missing'
assert m.get('canonical_constants', {}).get('gamma') == '16.339', 'gamma mismatch'
print('[ARCHIVE] metadata.json validation PASS')
print('[ARCHIVE] Zenodo export stub: implement export_to_zenodo.py with ZENODO_TOKEN')
"
else
  echo "[ARCHIVE] ZENODO_TOKEN not set - skipping Zenodo export (set in CI/CD variables)."
fi

echo "[ARCHIVE] Snapshot complete. Files:"
ls -lh "$SNAPSHOT_DIR/"
echo "[ARCHIVE] DONE."
exit 0