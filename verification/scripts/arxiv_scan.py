import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import os

def search_arxiv(query, max_results=5):
    params = urllib.parse.urlencode({
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'desc'
    })
    url = f'http://export.arxiv.org/api/query?{params}'
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return data
    except Exception as e:
        print(f"Error connecting to arXiv API: {e}")
        return None

def parse_arxiv_xml(xml_data):
    if not xml_data:
        return []
    
    root = ET.fromstring(xml_data)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    
    entries = []
    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace).text.strip()
        summary = entry.find('atom:summary', namespace).text.strip()
        published = entry.find('atom:published', namespace).text.strip()
        link = entry.find('atom:id', namespace).text.strip()
        entries.append({
            'title': title,
            'summary': summary,
            'published': published,
            'link': link
        })
    return entries

def main():
    print("--- UIDT arXiv Compatibility Scan ---")
    
    queries = {
        "Fully Heavy Tetraquarks (cccc)": "all:cccc+AND+all:tetraquark",
        "Omega_bbb Baryon": "all:Omega_bbb+OR+all:%22triply+heavy+baryon%22"
    }
    
    results_map = {}
    
    for category, q in queries.items():
        print(f"Querying arXiv for: {category}...")
        xml_data = search_arxiv(q)
        results = parse_arxiv_xml(xml_data)
        results_map[category] = results
        print(f"Found {len(results)} recent papers.")
        
    # Generate Markdown Report
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_name = f"Verification_Report_arXiv_{timestamp}.md"
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    report_path = os.path.join(base_dir, 'verification', 'data', report_name)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# UIDT-v3.9 arXiv Compatibility Report\n\n")
        f.write(f"**Generated:** {timestamp}\n")
        f.write("**Evidence Category:** [C/D] Monitoring\n\n")
        f.write("This report tracks experimental and theoretical developments in hadronic physics that could falsify or calibrate UIDT constants.\n\n")
        
        for category, papers in results_map.items():
            f.write(f"## {category}\n")
            if not papers:
                f.write("*No recent papers found.*\n\n")
            for p in papers:
                f.write(f"### [{p['title']}]({p['link']})\n")
                f.write(f"**Published:** {p['published']}\n\n")
                f.write(f"> {p['summary'][:300]}...\n\n")
                
    print(f"\n[PASS] Report generated at: {report_path}")

if __name__ == "__main__":
    main()
