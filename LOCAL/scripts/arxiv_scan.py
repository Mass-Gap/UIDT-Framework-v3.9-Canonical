import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re

def search_arxiv(query):
    query_url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending"
    try:
        response = urllib.request.urlopen(query_url)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        results = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title')
            summary = entry.find('{http://www.w3.org/2005/Atom}summary')
            link = entry.find('{http://www.w3.org/2005/Atom}id')
            if title is not None and summary is not None and link is not None:
                results.append({'title': title.text, 'summary': summary.text, 'link': link.text})
        return results
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

def main():
    queries = {
        "Lattice QCD glueball spectrum continuum limit": "Lattice QCD",
        "DESI dark energy equation of state": "DESI",
        "Casimir effect anomaly precision measurement": "Casimir"
    }

    triggers = []

    for query, source in queries.items():
        results = search_arxiv(query)
        for res in results:
            summary = res['summary']

            if source == "DESI":
                # Check for w = -1.00 \pm 0.01 (handling possible LaTeX formatting)
                if re.search(r'w\s*(?:\(z\))?\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', summary, re.IGNORECASE):
                    triggers.append(
                        f"🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{res['link']}]. "
                        f"Data implies $w = -1.00 \\pm 0.01$. This challenges the holographic scale factor mechanism. "
                        f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn]."
                    )

            if source == "Lattice QCD":
                # Check for mass gap \neq 1.710 GeV at >3\sigma
                if re.search(r'(?:\\neq|!=|≠|not equal to)\s*1\.710', summary) and re.search(r'>\s*3\s*(?:\\sigma|σ)', summary, re.IGNORECASE):
                    triggers.append(
                        f"🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{res['link']}]. "
                        f"Data implies Lattice QCD confirms mass gap $\\neq 1.710$ GeV at >3$\\sigma$. "
                        f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn]."
                    )

    if triggers:
        for t in triggers:
            print(t)
    else:
        print("No falsification triggers detected in real ArXiv data.")

if __name__ == "__main__":
    main()
