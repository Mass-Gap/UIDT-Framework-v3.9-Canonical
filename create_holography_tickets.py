import json
import os
import subprocess
import time

# Configuration
BASE_PATH = r"C:\Users\badbu\Documents\github\UIDT-Framework-V3.9"
PLANS_DIR = os.path.join(BASE_PATH, "UIDT-OS", "PLANS", "UIDT-UPDATES", "2026-03-09_LLM_holography_gamma")
LEDGER_DIR = os.path.join(BASE_PATH, "LEDGER")

# ID Mapping based on file analysis
ID_MAP = {
    "Holographic Gamma Literature Survey": "005",
    "UIDT-RT Holographic Prototype": "007",
    "Proton-Horizon Information Ratio": "009",
    "Gamma Derivation Research Claims Registry": "011",
    "KS MC-FSS Kinetic VEV Reproduction": "013",
    "AdS-QCD Holographic PR Preparation": "015",
    "Lattice QCD Ratio Falsification Test": "016",
    "Gamma-12 Torsion Bridge Derivation": "017",
    "L4 Audit Protocol Perturbative RG Gap": "018",
    "L5 N99 Cascade Audit and N9405 Tension": "019"
}

BATCH_FILES = [
    "batch_holographic_gamma_t1.json",
    "batch_holographic_gamma_t2.json",
    "batch_holographic_gamma_t3.json"
]

def run_cmd(cmd):
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=BASE_PATH)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        # Don't exit, try to continue

def create_ticket_file(ticket_id, data):
    filename = f"TKT-2026-03-09-{ticket_id}.md"
    filepath = os.path.join(LEDGER_DIR, filename)
    
    content = f"# Ticket {ticket_id}: {data['title']}\n\n"
    content += f"**Type:** {data['plan_type']}\n"
    content += f"**Objective:** {data['objective']}\n\n"
    content += "## Observations\n" + data['observations'] + "\n\n"
    content += "## Approach\n" + data['approach'] + "\n\n"
    content += "## Steps\n"
    for step in data['steps']:
        content += f"### {step['title']}\n"
        content += f"{step['description']}\n"
        content += f"- **Target:** {', '.join(step['file_targets'])}\n"
        content += f"- **Evidence:** {step.get('evidence_category', 'N/A')}\n\n"
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created ticket: {filepath}")
    return filepath

def create_placeholders(files):
    for fpath in files:
        full_path = os.path.join(BASE_PATH, fpath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                f.write(f"# Placeholder for {fpath}\n\nThis file is part of the Holographic Gamma research plan.")
            print(f"Created placeholder: {fpath}")

def process_item(data):
    title = data['title']
    if title not in ID_MAP:
        print(f"Skipping unknown title: {title}")
        return

    tid = ID_MAP[title]
    tkt_name = f"TKT-2026-03-09-{tid}"
    branch_name = f"feature/{tkt_name}-{title.replace(' ', '-').replace('/', '').replace(',', '')}"[:50] # Limit length
    
    print(f"\n--- Processing {tkt_name} ---")
    
    # 1. Create Ticket File
    create_ticket_file(tid, data)
    
    # 2. Git Operations
    run_cmd("git checkout main")
    run_cmd("git pull origin main")
    
    # Create/Reset Branch
    try:
        run_cmd(f"git branch -D {branch_name}")
    except:
        pass
    run_cmd(f"git checkout -b {branch_name}")
    
    # 3. Create Target Files (Placeholders)
    all_targets = []
    for step in data['steps']:
        all_targets.extend(step['file_targets'])
    create_placeholders(all_targets)
    
    # 4. Commit and Push
    run_cmd("git add .")
    run_cmd(f'git commit -m "[UIDT-v3.9] {title} ({tkt_name})" -m "Implements structure for {tkt_name}"')
    run_cmd(f"git push -u origin {branch_name} --force")
    
    # 5. Create PR
    body = f"## Summary\n{data['objective']}\n\n## Evidence\n- Category: [D] (Research/Documentation)\n- Ticket: {tkt_name}\n\n## Plan\nSee LEDGER/{tkt_name}.md"
    run_cmd(f'gh pr create --title "[UIDT-v3.9] {title} ({tkt_name})" --body "{body}"')

def main():
    for batch_file in BATCH_FILES:
        fpath = os.path.join(PLANS_DIR, batch_file)
        with open(fpath, 'r') as f:
            items = json.load(f)
            for item in items:
                process_item(item)
                time.sleep(2) # rate limit

if __name__ == "__main__":
    main()
