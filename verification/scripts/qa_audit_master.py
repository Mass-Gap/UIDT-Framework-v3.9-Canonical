#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

def run_module(module_name):
    print(f"\n--- Running {module_name} ---")
    script_path = Path("verification/scripts/qa_modules") / f"{module_name}.py"
    if not script_path.exists():
        print(f"Error: {script_path} not found.")
        return 2 # System Error

    try:
        result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {module_name} PASSED.")
            return 0
        else:
            print(f"❌ {module_name} FAILED.")
            print(result.stdout)
            print(result.stderr)
            return 1 # Check Failed
    except Exception as e:
        print(f"System Error running {module_name}: {e}")
        return 2

def main():
    print("========================================")
    print(" UIDT QA Audit Master - Initialization")
    print("========================================\n")

    modules = [
        "qa_wording",
        "qa_numerical",
        "qa_evidence"
    ]

    overall_status = 0

    for mod in modules:
        status = run_module(mod)
        if status == 1:
            overall_status = 1
        elif status == 2 and overall_status == 0:
            overall_status = 2

    print("\n========================================")
    if overall_status == 0:
        print("🎉 ALL QA CHECKS PASSED. EXIT CODE 0.")
        sys.exit(0)
    elif overall_status == 1:
        print("🛑 QA AUDIT FAILED. EXIT CODE 1.")
        sys.exit(1)
    else:
        print("⚠️ QA AUDIT ENCOUNTERED SYSTEM ERRORS. EXIT CODE 2.")
        sys.exit(2)

if __name__ == "__main__":
    main()
