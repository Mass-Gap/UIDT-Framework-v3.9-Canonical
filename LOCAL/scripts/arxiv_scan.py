import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import re

categories = ["cat:hep-ex", "cat:hep-lat", "cat:astro-ph.CO"]
# Construct category part: (cat:hep-ex OR cat:hep-lat OR cat:astro-ph.CO)
cat_str = "(" + " OR ".join(categories) + ")"

keywords = [
    'all:"fully-heavy tetraquark"',
    'all:"X(6900)"',
    'all:Omega_bbb',
    'all:"DESI" AND all:"equation of state"',
    'all:w_0 AND all:w_a'
]

canonical_values = {
    "M_cccc": 4.4982,
    "M_Omega_bbb": 14.4585,
    "w_0": -0.99
}

# 48 hours
recent_cutoff = datetime.now(timezone.utc) - timedelta(days=2)

print("Starting ArXiv scan in RESEARCH-MODE...")

found_relevant = False

def extract_value(text, pattern):
    match = re.search(pattern, text)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def extract_and_compare(text, paper_info):
    global found_relevant

    # Try to find M_cccc
    m_cccc = extract_value(text, r'M_\{cccc\}\s*(?:=|≈)\s*([0-9.]+)')
    if m_cccc is None:
        m_cccc = extract_value(text, r'fully-heavy tetraquark mass\s*(?:of|is)\s*(?:about\s*)?([0-9.]+)')
    if m_cccc is None:
        m_cccc = extract_value(text, r'mass\s*(?:of|is)\s*(?:about\s*)?([0-9.]+)\s*GeV')

    # Try to find M_Omega_bbb
    m_omega = extract_value(text, r'M_\{\\Omega_\{bbb\}\}\s*(?:=|≈)\s*([0-9.]+)')
    if m_omega is None:
         m_omega = extract_value(text, r'\\Omega_\{bbb\}\s*mass\s*(?:of|is)\s*(?:about\s*)?([0-9.]+)')

    # Try to find w_0
    w_0 = extract_value(text, r'w_0\s*(?:=|≈)\s*(-?[0-9.]+)')

    found_anything = False

    if m_cccc is not None:
        diff = m_cccc - canonical_values["M_cccc"]
        print(f"MATCH: {paper_info} -> M_cccc = {m_cccc} GeV (deviation: {diff:+.4f} GeV)")
        found_anything = True

    if m_omega is not None:
        diff = m_omega - canonical_values["M_Omega_bbb"]
        print(f"MATCH: {paper_info} -> M_Omega_bbb = {m_omega} GeV (deviation: {diff:+.4f} GeV)")
        found_anything = True

    if w_0 is not None:
        diff = w_0 - canonical_values["w_0"]
        print(f"MATCH: {paper_info} -> w_0 = {w_0} (deviation: {diff:+.4f})")
        found_anything = True

    if found_anything:
        found_relevant = True

    return found_anything

for kw in keywords:
    query = f"{cat_str} AND ({kw})"
    encoded_query = urllib.parse.quote(query)

    url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&sortBy=submittedDate&sortOrder=descending&max_results=10"

    try:
        req = urllib.request.urlopen(url)
        res = req.read()
        root = ET.fromstring(res)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)

        for entry in entries:
            published_elem = entry.find('atom:published', ns)
            if published_elem is None:
                continue
            published_str = published_elem.text

            try:
                published_date = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except ValueError:
                published_date = datetime.strptime(published_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)

            if published_date >= recent_cutoff:
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')

                paper_info = f"{published_str[:10]} | {title}"
                extract_and_compare(summary, paper_info)

    except Exception as e:
        print(f"Exception querying {kw}: {e}")

if not found_relevant:
    print("Clear — no new relevant publications found.")
