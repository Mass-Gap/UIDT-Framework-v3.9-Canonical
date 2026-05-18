import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import os
import time

def generate_emergency_report(paper_id, threshold, claim_mechanism):
    report_content = f"""🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {paper_id}. Data implies {threshold}. This challenges {claim_mechanism}. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn]."""

    logs_dir = "LOCAL/logs"
    os.makedirs(logs_dir, exist_ok=True)
    report_path = os.path.join(logs_dir, f"Emergency_Epistemic_Report_{int(time.time())}.md")
    with open(report_path, "w") as f:
        f.write(report_content)
    print(f"Generated Emergency Epistemic Report at {report_path}")

def search_arxiv(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f'http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results=10'
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req).read()
            root = ET.fromstring(data)

            results = []
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                paper_id = entry.find('{http://www.w3.org/2005/Atom}id').text
                results.append({'title': title, 'summary': summary, 'id': paper_id})
            return results
        except Exception as e:
            print(f"Error fetching from arXiv: {e}")
            time.sleep(5)
    return []

def scan():
    print("Running arXiv Monitor (Rule 4.1 & 4.2)...")

    queries = {
        "desi": "DESI dark energy equation of state",
        "lattice": "Lattice QCD glueball spectrum continuum limit",
        "casimir": "Casimir effect anomaly precision measurement"
    }

    desi_pattern = re.compile(r'w\s*=\s*-1\.00\s*(?:\+/-|\\pm)\s*0\.01')
    lattice_pattern = re.compile(r'mass gap.*!=.*1\.710.*>3\\sigma|mass gap.*\neq.*1\.710.*>3\\sigma')
    casimir_pattern = re.compile(r'\\Delta F/F.*<.*0\.1%|anomaly.*<.*0\.1%')

    for key, q in queries.items():
        print(f"Querying: {q}")
        papers = search_arxiv(q)
        for p in papers:
            summary = p['summary'].replace('\n', ' ')

            if key == "desi":
                if desi_pattern.search(summary):
                    print(f"Trigger found in DESI paper: {p['id']}")
                    generate_emergency_report(p['id'], r"w = -1.00 \pm 0.01", "the holographic scale factor mechanism")

            elif key == "lattice":
                if lattice_pattern.search(summary):
                    print(f"Trigger found in Lattice paper: {p['id']}")
                    generate_emergency_report(p['id'], r"mass gap != 1.710 GeV at >3\sigma", "Pillar I mass gap theorem")

            elif key == "casimir":
                if casimir_pattern.search(summary):
                    print(f"Trigger found in Casimir paper: {p['id']}")
                    generate_emergency_report(p['id'], r"|\Delta F/F| < 0.1%", "Casimir prediction")
        time.sleep(3) # respectful to API rate limits

if __name__ == "__main__":
    scan()
