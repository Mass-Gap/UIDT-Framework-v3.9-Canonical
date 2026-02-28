import json
import sys

def load_claims(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data['claims']
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        sys.exit(1)

def build_graph(claims):
    claim_map = {c['id']: c for c in claims}
    adj = {c['id']: [] for c in claims}

    for c in claims:
        deps = c.get('dependencies', [])
        for dep in deps:
            if dep in claim_map:
                adj[c['id']].append(dep)
            else:
                # External dependency
                pass
    return claim_map, adj

def find_cycles(adj):
    visited = set()
    recursion_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        recursion_stack.add(node)
        path.append(node)

        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in recursion_stack:
                cycle_start_index = path.index(neighbor)
                cycles.append(path[cycle_start_index:] + [neighbor])

        recursion_stack.remove(node)
        path.pop()

    for node in adj:
        if node not in visited:
            dfs(node, [])

    return cycles

def check_epistemic_breach(claim_map, adj):
    breaches = []
    memo = {}
    visiting = set()

    def get_cd_dependencies(node):
        if node in memo:
            return memo[node]
        if node in visiting:
            return set()

        visiting.add(node)
        risky = set()

        claim = claim_map.get(node)
        if claim:
            cat = claim.get('evidence', '?')
            if cat in ['C', 'D']:
                risky.add((node, cat))

        if node in adj:
            for child in adj[node]:
                risky.update(get_cd_dependencies(child))

        visiting.remove(node)
        memo[node] = risky
        return risky

    for cid, claim in claim_map.items():
        if claim.get('evidence') == 'A':
            risky = get_cd_dependencies(cid)
            if risky:
                breaches.append((cid, list(risky)))

    return breaches

def main():
    filepath = 'UIDT-OS/LEDGER/CLAIMS.json'
    print(f"Reading {filepath}...")
    claims = load_claims(filepath)
    claim_map, adj = build_graph(claims)

    cycles = find_cycles(adj)
    has_cycles = False
    if cycles:
        print("CRITICAL: Circular Dependencies Detected!")
        for cycle in cycles:
            print(f"Cycle: {' -> '.join(cycle)}")
        has_cycles = True
    else:
        print("Graph is Acyclic.")

    breaches = check_epistemic_breach(claim_map, adj)
    has_breaches = False
    if breaches:
        print("CRITICAL: Epistemic Constitutional Breach Detected!")
        for cid, risky_list in breaches:
            print(f"Claim {cid} (Category A) depends on:")
            for r_id, r_cat in risky_list:
                print(f"  - {r_id} (Category {r_cat})")
        has_breaches = True
    else:
        print("No Epistemic Breaches found.")

    if not has_cycles and not has_breaches:
        print("Epistemic Graph Acyclic & Secure")

if __name__ == "__main__":
    main()
