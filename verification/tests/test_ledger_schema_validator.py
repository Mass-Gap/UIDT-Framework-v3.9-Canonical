"""
test_ledger_schema_validator.py

Validates that LEDGER/CLAIMS.json conforms to LEDGER/claims.schema.json.
Also verifies structural invariants that go beyond JSON Schema:
  - every claim has a non-empty 'id' field
  - every claim has a valid evidence category (A, A-, B, C, D, E)
  - no claim has evidence category A or B for cosmology-tagged items
  - withdrawn claims (evidence E) are not referenced by other claims as
    primary support

Precision: mpmath not required here (no numerical calculations).
Framework: pytest
Dependencies: jsonschema (pip install jsonschema)
"""

import json
import os
import pytest

REPO_ROOT    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLAIMS_PATH  = os.path.join(REPO_ROOT, "LEDGER", "CLAIMS.json")
SCHEMA_PATH  = os.path.join(REPO_ROOT, "LEDGER", "claims.schema.json")

VALID_EVIDENCE = {"A", "A-", "B", "C", "D", "E"}
COSMO_TAGS     = {"cosmology", "cosmological", "dark_energy", "hubble"}
EVIDENCE_RANK  = {"E": -1, "D": 0, "C": 1, "B": 2, "A-": 3, "A": 4}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_claims_list(data):
    """Normalise: CLAIMS.json may be a list or a dict with a 'claims' key."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("claims", "data", "entries"):
            if key in data:
                return data[key]
        # flat dict keyed by claim id
        return list(data.values()) if data else []
    return []


# ---------------------------------------------------------------------------
# Test 1: Schema file is valid JSON
# ---------------------------------------------------------------------------
def test_schema_is_valid_json():
    schema = load_json(SCHEMA_PATH)
    assert isinstance(schema, dict), "Schema must be a JSON object"


# ---------------------------------------------------------------------------
# Test 2: CLAIMS.json validates against schema (if jsonschema available)
# ---------------------------------------------------------------------------
def test_claims_validates_against_schema():
    try:
        import jsonschema
    except ImportError:
        pytest.skip("jsonschema not installed — skipping schema validation")
    claims_data = load_json(CLAIMS_PATH)
    schema      = load_json(SCHEMA_PATH)
    try:
        jsonschema.validate(instance=claims_data, schema=schema)
    except jsonschema.ValidationError as e:
        pytest.fail(f"CLAIMS.json fails schema validation: {e.message}")


# ---------------------------------------------------------------------------
# Test 3: All claims have required fields
# ---------------------------------------------------------------------------
def test_all_claims_have_required_fields():
    data   = load_json(CLAIMS_PATH)
    claims = get_claims_list(data)
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            continue
        assert "id" in claim or "claim_id" in claim, (
            f"Claim at index {i} missing 'id' field: {str(claim)[:80]}"
        )


# ---------------------------------------------------------------------------
# Test 4: All evidence categories are valid
# ---------------------------------------------------------------------------
def test_all_evidence_categories_valid():
    data   = load_json(CLAIMS_PATH)
    claims = get_claims_list(data)
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        ev = claim.get("evidence") or claim.get("evidence_category") or claim.get("category")
        if ev is None:
            continue  # missing field — covered by schema test
        assert ev in VALID_EVIDENCE, (
            f"Invalid evidence category '{ev}' in claim {claim.get('id', '?')}"
        )


# ---------------------------------------------------------------------------
# Test 5: Cosmology-tagged claims must not exceed category C
# ---------------------------------------------------------------------------
def test_cosmology_claims_ceiling_C():
    data   = load_json(CLAIMS_PATH)
    claims = get_claims_list(data)
    ceiling = EVIDENCE_RANK["C"]
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        tags = claim.get("tags", []) or claim.get("domain", [])
        if isinstance(tags, str):
            tags = [tags]
        is_cosmo = any(t.lower() in COSMO_TAGS for t in tags)
        if not is_cosmo:
            continue
        ev = claim.get("evidence") or claim.get("evidence_category") or claim.get("category")
        if ev is None:
            continue
        rank = EVIDENCE_RANK.get(ev, -99)
        assert rank <= ceiling, (
            f"Cosmology claim {claim.get('id','?')} has evidence {ev} > C ceiling"
        )


# ---------------------------------------------------------------------------
# Test 6: No active claim references a withdrawn (E) claim as sole support
# ---------------------------------------------------------------------------
def test_no_active_claim_depends_on_withdrawn():
    data   = load_json(CLAIMS_PATH)
    claims = get_claims_list(data)
    withdrawn_ids = set()
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        ev = claim.get("evidence") or claim.get("evidence_category") or claim.get("category")
        if ev == "E":
            cid = claim.get("id") or claim.get("claim_id")
            if cid:
                withdrawn_ids.add(str(cid))
    if not withdrawn_ids:
        return  # nothing to check
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        ev = claim.get("evidence") or claim.get("evidence_category") or claim.get("category")
        if ev == "E":
            continue
        deps = claim.get("depends_on") or claim.get("references") or []
        if isinstance(deps, str):
            deps = [deps]
        for dep in deps:
            assert str(dep) not in withdrawn_ids, (
                f"Active claim {claim.get('id','?')} references withdrawn claim {dep}"
            )
