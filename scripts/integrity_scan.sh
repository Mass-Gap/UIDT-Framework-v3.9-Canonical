#!/usr/bin/env bash
# =============================================================================
# scripts/integrity_scan.sh  UIDT v3.9 Scientific Integrity Scanner
# Scans for prestige/overclaim phrasing without theorem/citation refs.
# Evidence category: B (governance tooling) | Limitation: none
# DOI: 10.5281/zenodo.17835200
# =============================================================================
set -euo pipefail

VIOLATIONS=0
REVIEW_LOG="AUDIT_TRAIL/integrity_violations.txt"
mkdir -p AUDIT_TRAIL
> "$REVIEW_LOG"

echo "[INTEGRITY] UIDT v3.9 scientific integrity scan - $(date -u)"

# Rule 1: 'proof' without Theorem/Lemma/Banach ref
echo "[INTEGRITY] Rule 1: 'proof' without Theorem reference..."
while IFS= read -r match; do
  FILE=$(echo "$match" | cut -d: -f1)
  LNUM=$(echo "$match" | cut -d: -f2)
  echo "REVIEW-REQUIRED | Rule-1 proof-without-Theorem | ${FILE}:${LNUM}" | tee -a "$REVIEW_LOG"
  VIOLATIONS=$((VIOLATIONS + 1))
done < <(grep -rn --include='*.md' --include='*.tex' --include='*.py' \
  -iE '\bproof\b' . \
  | grep -ivE 'theorem|banach|fixed.point|lemma|proposition|corollary|proof of|proof sketch|proof-of-concept' \
  | grep -vE '\.git/|integrity_scan|CHANGELOG|AUDIT_TRAIL' || true)

# Rule 2: 'confirmed' without citation
echo "[INTEGRITY] Rule 2: 'confirmed' without citation..."
while IFS= read -r match; do
  FILE=$(echo "$match" | cut -d: -f1)
  LNUM=$(echo "$match" | cut -d: -f2)
  echo "REVIEW-REQUIRED | Rule-2 confirmed-without-citation | ${FILE}:${LNUM}" | tee -a "$REVIEW_LOG"
  VIOLATIONS=$((VIOLATIONS + 1))
done < <(grep -rn --include='*.md' --include='*.tex' --include='*.rst' \
  -iE '\bconfirmed\b' . \
  | grep -ivE '\[.*\]|arxiv|doi|zenodo|lattice|experimentally|observationally' \
  | grep -vE '\.git/|integrity_scan|CHANGELOG|AUDIT_TRAIL' || true)

# Rule 3: 'resolved' without A/A- evidence tag
echo "[INTEGRITY] Rule 3: 'resolved' without evidence tag..."
while IFS= read -r match; do
  FILE=$(echo "$match" | cut -d: -f1)
  LNUM=$(echo "$match" | cut -d: -f2)
  echo "REVIEW-REQUIRED | Rule-3 resolved-without-evidence-tag | ${FILE}:${LNUM}" | tee -a "$REVIEW_LOG"
  VIOLATIONS=$((VIOLATIONS + 1))
done < <(grep -rn --include='*.md' --include='*.tex' --include='*.rst' \
  -iE '\bresolved\b' . \
  | grep -ivE '\[A\]|\[A-\]|issue.*resolved|PR #|merge|conflict|TODO' \
  | grep -vE '\.git/|integrity_scan|CHANGELOG|AUDIT_TRAIL' || true)

# Rule 4: prestige closure language
echo "[INTEGRITY] Rule 4: prestige closure language..."
while IFS= read -r match; do
  FILE=$(echo "$match" | cut -d: -f1)
  LNUM=$(echo "$match" | cut -d: -f2)
  echo "REVIEW-REQUIRED | Rule-4 prestige-closure | ${FILE}:${LNUM}" | tee -a "$REVIEW_LOG"
  VIOLATIONS=$((VIOLATIONS + 1))
done < <(grep -rn --include='*.md' --include='*.tex' --include='*.rst' \
  -iE '\bdefinitively\b|\bdefinitive proof\b|\bsolves the.*problem\b|\bproves the mass gap\b' . \
  | grep -vE '\.git/|integrity_scan|CHANGELOG|AUDIT_TRAIL' || true)

# Rule 5: sigma-claims without appendix
echo "[INTEGRITY] Rule 5: sigma-claims without statistical note..."
while IFS= read -r match; do
  FILE=$(echo "$match" | cut -d: -f1)
  LNUM=$(echo "$match" | cut -d: -f2)
  echo "REVIEW-REQUIRED | Rule-5 sigma-claim-no-appendix | ${FILE}:${LNUM}" | tee -a "$REVIEW_LOG"
  VIOLATIONS=$((VIOLATIONS + 1))
done < <(grep -rn --include='*.md' --include='*.tex' --include='*.rst' \
  -E '[0-9]+-?sigma|[0-9]+[[:space:]]*sigma' . \
  | grep -ivE 'appendix|table|heuristic|statistical note|see.*section|\[heuristic\]' \
  | grep -vE '\.git/|integrity_scan|CHANGELOG|AUDIT_TRAIL' || true)

echo "[INTEGRITY] Scan complete. Violations: $VIOLATIONS"
if [ "$VIOLATIONS" -gt 0 ]; then
  echo "[INTEGRITY] === Scientific Integrity Violation ==="
  cat "$REVIEW_LOG"
  exit 1
fi
echo "[INTEGRITY] PASS - no prestige/overclaim phrasing detected."
exit 0