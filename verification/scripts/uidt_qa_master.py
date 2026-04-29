import os
import sys
import json
import importlib.util
from datetime import datetime, timezone
import mpmath as mp

# Enforce local mp.dps as per Constitution
mp.mp.dps = 80

def get_repo_root():
    # Assuming script is run from anywhere, find root by looking for .git or specific folders
    current = os.path.abspath(__file__)
    while True:
        parent = os.path.dirname(current)
        if os.path.exists(os.path.join(parent, '.git')) or os.path.exists(os.path.join(parent, 'verification')):
            return parent
        if parent == current:
            # Fallback to current working dir
            return os.getcwd()
        current = parent

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def run_all_checks():
    repo_root = get_repo_root()
    checks_dir = os.path.join(repo_root, "verification", "scripts", "checks")

    if not os.path.exists(checks_dir):
        print(f"Error: Checks directory {checks_dir} not found.")
        sys.exit(3)

    check_files = sorted([f for f in os.listdir(checks_dir) if f.startswith("chk") and f.endswith(".py")])

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "repo_root": repo_root,
        "results": [],
        "overall_status": "PASS"
    }

    global_status_code = 0

    status_priority = {"PASS": 0, "WARN": 1, "FAIL": 2, "CRITICAL": 3}
    max_status_seen = 0

    for check_file in check_files:
        module_name = check_file[:-3]
        file_path = os.path.join(checks_dir, check_file)

        try:
            module = load_module_from_path(module_name, file_path)
            if hasattr(module, 'run_check'):
                print(f"Running {module_name}...")
                status, messages = module.run_check(repo_root)

                report["results"].append({
                    "check": module_name,
                    "status": status,
                    "messages": messages
                })

                # Update global status
                if status_priority.get(status, 0) > max_status_seen:
                    max_status_seen = status_priority.get(status, 0)

                if status != "PASS":
                    for msg in messages:
                        print(f"  [{status}] {msg}")
                else:
                    print("  [PASS]")

            else:
                print(f"  [ERROR] {module_name} missing run_check function")
        except Exception as e:
            print(f"  [ERROR] Failed to run {module_name}: {str(e)}")
            report["results"].append({
                "check": module_name,
                "status": "FAIL",
                "messages": [f"Execution error: {str(e)}"]
            })
            max_status_seen = max(max_status_seen, 2)

    # Determine overall status string
    for status_str, code in status_priority.items():
        if code == max_status_seen:
            report["overall_status"] = status_str
            break

    # Generate output
    timestamp_clean = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = os.path.join(repo_root, "verification", "data", f"qa_report_{timestamp_clean}.json")

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n" + "="*50)
    print(f"QA Master Run Complete.")
    print(f"Overall Status: {report['overall_status']}")
    print(f"Report saved to: {report_path}")
    print("="*50)

    sys.exit(max_status_seen)

if __name__ == "__main__":
    run_all_checks()
