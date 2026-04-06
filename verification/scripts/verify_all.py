import subprocess
import sys
import os

def run_script(script_path):
    print(f"========================================")
    print(f"Running {script_path}...")
    print(f"========================================")
    try:
        # Resolve python executable
        result = subprocess.run([sys.executable, script_path], check=True)
        print(f"[SUCCESS] {script_path} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {script_path} failed with exit code {e.returncode}.\n")
        sys.exit(1)

def run_pytest():
    print(f"========================================")
    print(f"Running full pytest suite...")
    print(f"========================================")
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "verification/tests/", "-v"], check=True)
        print(f"[SUCCESS] Pytest suite completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Pytest suite failed with exit code {e.returncode}.\n")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure working directory is the repository root
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(repo_root)

    print("Starting UIDT Framework Verification Suite...\n")

    scripts = [
        "verification/scripts/verify_spectral_gap.py",
        "verification/scripts/verify_rg_fixed_point.py",
        "verification/scripts/verify_cosmology.py",
        "verification/scripts/verify_light_quark_masses.py"
    ]

    for script in scripts:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f"[WARNING] Script not found: {script}. Skipping...")

    run_pytest()

    print("========================================")
    print("[ALL PASSED] Unified verification completed successfully.")
    print("========================================")
