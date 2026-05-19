import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys
import json
import os
import datetime

def check_falsification_triggers():
    queries = [
        'all:"Lattice QCD" AND all:"continuum limit" AND all:"mass gap"',
        'all:"DESI" AND all:"dark energy" AND all:"equation of state"',
        'all:"Casimir effect" AND all:"anomaly"'
    ]

    triggers_found = []

    for q in queries:
        url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(q)}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending"
        try:
            response = urllib.request.urlopen(url)
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')

                if title_elem is None or summary_elem is None or id_elem is None:
                    continue

                title = title_elem.text
                summary = summary_elem.text
                id_url = id_elem.text

                # Check for DESI Trigger: w = -1.00 \pm 0.01
                if "DESI" in q:
                    if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\\pm\s+|\+\/\-|\±)\s*0\.01', summary) or \
                       re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\\pm\s+|\+\/\-|\±)\s*0\.01', title):
                       triggers_found.append({
                           'type': 'DESI',
                           'title': title,
                           'id': id_url,
                           'summary': summary,
                           'data_implication': 'w = -1.00 \\pm 0.01',
                           'claim': 'Claim [X]'
                       })

                # Check for Lattice QCD Trigger: mass gap != 1.710 GeV at >3\sigma
                if "Lattice QCD" in q:
                     # MUST meet both conditions to prevent false positives for any paper just saying >3sigma
                     if re.search(r'mass gap.*!=.*1\.710', summary) and \
                        re.search(r'>\s*3\s*(?:\\sigma|sigma)', summary):
                         triggers_found.append({
                             'type': 'Lattice QCD',
                             'title': title,
                             'id': id_url,
                             'summary': summary,
                             'data_implication': 'mass gap \\neq 1.710 GeV at >3\\sigma',
                             'claim': 'Claim [X]'
                         })

        except Exception as e:
            print(f"Error querying {q}: {e}", file=sys.stderr)

    return triggers_found

def generate_emergency_report(trigger):
    report = f"""> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{trigger['id']}]. Data implies ${trigger['data_implication']}$. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of {trigger['claim']} to Category [E-withdrawn].
"""

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"LOCAL/logs/Emergency_Epistemic_Report_{timestamp}.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Generated report at {report_path}")

    trace_entry = {
        "files": [report_path, "LOCAL/scripts/arxiv_scan.py"],
        "tests": [],
        "docs": ["CANONICAL/FALSIFICATION.md", "CANONICAL/LIMITATIONS.md"],
        "status": "emergency_report_generated",
        "timestamp": datetime.datetime.now().isoformat(),
        "author": "P. Rietz"
    }

    traceability_path = "LOCAL/logs/traceability.json"
    trace_data = {}
    if os.path.exists(traceability_path):
        with open(traceability_path, "r") as f:
            try:
                trace_data = json.load(f)
            except json.JSONDecodeError:
                trace_data = {}

    trace_data[f"TKT-{timestamp}"] = trace_entry
    with open(traceability_path, "w") as f:
        json.dump(trace_data, f, indent=2)

if __name__ == "__main__":
    triggers = check_falsification_triggers()

    for t in triggers:
        generate_emergency_report(t)
