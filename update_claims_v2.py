import json
import os
from datetime import datetime

ledger_path = 'LEDGER/CLAIMS.json'

with open(ledger_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

claims = data.get('claims', [])

# Remove existing C-070, C-072, C-073 just in case they miraculously appeared
claims = [c for c in claims if c['id'] not in ['UIDT-C-070', 'UIDT-C-072', 'UIDT-C-073']]

# Data to append
c070 = {
    "id": "UIDT-C-070",
    "statement": "FRG-Run (2026-04-06): Nontrivial FP not found in unconstrained Z_S-extended Litim truncation.",
    "type": "diagnostic",
    "status": "verified",
    "evidence": "C",
    "confidence": 0.9,
    "dependencies": [],
    "since": "v3.9.6",
    "notes": "FRG-Run (2026-04-06): Nontrivial FP not found in unconstrained Z_S-extended Litim truncation. Gribov pole at \u03ba\u00b2=1 confirmed. Evidence C confirmed for YM-sector mass gap generation; scalar extension requires Gribov-Zwanziger modification and Trace Anomaly."
}

c072 = {
    "id": "UIDT-C-072",
    "statement": "Identifikation von S als Dilaton-Feld zur Aufl\u00f6sung des Z_2-Kollapses",
    "type": "canonical_definition",
    "status": "verified",
    "evidence": "B",
    "confidence": 0.85,
    "dependencies": ["Gatekeeper-Run 3x3-System (2026-04-06)"],
    "since": "v3.9.7",
    "notes": "In der strikten \u27e8S\u27e9=0 Phase kollabiert der S-F^2 Operator in den Ursprung (deterministisch verifiziert). Die Identifikation von S als Dilaton koppelt das Feld an die Spuranomalie der SU(3). Das Gluon-Kondensat generiert einen nicht-verschwindenden Quellterm, der den Fixpunkt jenseits von kappa=0 stabilisiert."
}

c073 = {
    "id": "UIDT-C-073",
    "statement": "Analytische Vorhersage des geometrischen Skalars aus der RG-Projektion unter GZ-Abschirmung",
    "type": "predictive",
    "status": "predicted",
    "evidence": "D",
    "confidence": 0.9,
    "dependencies": ["verification/scripts/solve_gz_projected_2x2.py (Midpoint Rule 80-dps)"],
    "since": "v3.9.7",
    "notes": "kappa2_star = pi^2, lam_SF_star = 16.449340668482264505, deviation_to_gamma = 0.67%. L7: Fixpunkt erfordert kinematische Evaluierung jenseits des Gribov-Horizonts. Evidenz C erfordert dynamische Gribov-Zwanziger (GZ) Erweiterung ohne externen Scan-Parameter."
}

# Append the new claims
claims.extend([c070, c072, c073])

data['claims'] = claims

# Recalculate statistics
stats = {
    "by_evidence": {"A": 0, "A-": 0, "B": 0, "C": 0, "D": 0, "E": 0},
    "by_status": {}
}

for c in claims:
    ev = c.get('evidence', '')
    if ev in stats["by_evidence"]:
        stats["by_evidence"][ev] += 1
    
    status = c.get('status', '')
    if status not in stats["by_status"]:
        stats["by_status"][status] = 0
    stats["by_status"][status] += 1

data['statistics'] = stats

# Update total count
data['metadata']['total_claims'] = len(claims)

# Write back
with open(ledger_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Successfully updated {ledger_path}. New total claims: {len(claims)}")
