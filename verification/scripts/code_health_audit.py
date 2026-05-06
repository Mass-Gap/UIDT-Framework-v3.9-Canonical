import os
import ast
import sys

def audit_directory(target_dir):
    violations = []
    
    for root, _, files in os.walk(target_dir):
        for file in files:
            if not file.endswith('.py'):
                continue
                
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 1. Check for mp.dps = 80
            if "mp.dps = 80" not in content and "mp.dps=80" not in content:
                # We only enforce this for mathematical modules. Let's flag it if mpmath is imported.
                if "import mpmath" in content or "from mpmath" in content:
                    violations.append(f"[{filepath}] Missing local precision declaration 'mp.dps = 80'")
                    
            # 2. Check for float() leaks using AST
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == 'float':
                            violations.append(f"[{filepath}:{node.lineno}] UNAUTHORIZED USE OF float(). Must use mpf().")
            except SyntaxError as e:
                violations.append(f"[{filepath}] Syntax error during AST parsing: {e}")
                
    return violations

def main():
    print("--- UIDT Code Health & Epistemic Audit ---")
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    modules_dir = os.path.join(base_dir, 'modules')
    sim_dir = os.path.join(base_dir, 'simulation')
    
    dirs_to_audit = []
    if os.path.exists(modules_dir): dirs_to_audit.append(modules_dir)
    if os.path.exists(sim_dir): dirs_to_audit.append(sim_dir)
    
    all_violations = []
    for d in dirs_to_audit:
        print(f"Auditing directory: {d}")
        all_violations.extend(audit_directory(d))
        
    if all_violations:
        print("\n[FAILED] Epistemic Violations Detected:")
        for v in all_violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("\n[PASS] No float() leaks detected. Precision constraints are healthy.")
        sys.exit(0)

if __name__ == "__main__":
    main()
