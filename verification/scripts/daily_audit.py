import json
import sys
import os

def load_claims(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data['claims']
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        sys.exit(1)

def build_graph(claims):
    graph = {}
    claim_map = {c['id']: c for c in claims}

    for claim in claims:
        claim_id = claim['id']
        deps = claim.get('dependencies', [])
        # Only add dependencies that are also claims in the list
        # This focuses the graph on internal claim interdependencies
        valid_deps = [d for d in deps if d in claim_map]
        graph[claim_id] = valid_deps

    return graph, claim_map

def find_cycles(graph):
    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                cycle_start_index = path.index(neighbor)
                cycle = path[cycle_start_index:] + [neighbor]
                cycles.append(cycle)

        rec_stack.remove(node)
        path.pop()

    for node in graph:
        if node not in visited:
            dfs(node, [])

    return cycles

def check_epistemic_violations(graph, claim_map):
    violations = []

    # Memoization for reachable categories
    reachable_categories = {}

    def get_reachable_categories(node, visited_path):
        if node in reachable_categories:
            return reachable_categories[node]

        cats = set()

        # Add current node's category if known and valid
        if node in claim_map:
            ev = claim_map[node].get('evidence')
            if ev:
                cats.add((node, ev))

        visited_path.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited_path:
                neighbor_cats = get_reachable_categories(neighbor, visited_path)
                cats.update(neighbor_cats)

        visited_path.remove(node)
        reachable_categories[node] = cats
        return cats

    for node in graph:
        claim = claim_map.get(node)
        if not claim: continue

        # Check only Claims of Category [A]
        # Violations: A depending on C or D
        if claim.get('evidence') == 'A':
            # Get all reachable nodes (dependencies)
            # Note: We check immediate and transitive dependencies
            # But wait, get_reachable_categories includes the node itself.
            # We must filter out the node itself for the check.
            reachable = get_reachable_categories(node, set())

            for dep_node, dep_ev in reachable:
                if dep_node == node:
                    continue

                if dep_ev in ['C', 'D']:
                    violations.append({
                        'source': node,
                        'source_ev': 'A',
                        'dependency': dep_node,
                        'dependency_ev': dep_ev
                    })

    return violations

def main():
    filepath = 'UIDT-OS/LEDGER/CLAIMS.json'
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        sys.exit(1)

    claims = load_claims(filepath)
    graph, claim_map = build_graph(claims)

    cycles = find_cycles(graph)

    if cycles:
        print("CRITICAL: Circular Dependencies Found!")
        for cycle in cycles:
            print(f"Cycle: {' -> '.join(cycle)}")
        sys.exit(1)

    violations = check_epistemic_violations(graph, claim_map)

    if violations:
        print("CRITICAL: Epistemic Constitution Violation!")
        for v in violations:
            source = v['source']
            target = v['dependency']
            # Find path from source to target
            path = find_path(graph, source, target)
            path_str = " -> ".join(path) if path else "Path not found"
            print(f"Claim {source} [A] depends on {target} [{v['dependency_ev']}] via path: {path_str}")
        sys.exit(1)

    print("Epistemic Graph Acyclic & Secure")

def find_path(graph, start, end, path=None):
    if path is None:
        path = []
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None

if __name__ == '__main__':
    main()
