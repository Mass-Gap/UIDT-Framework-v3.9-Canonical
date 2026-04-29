import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    FORBIDDEN_IN_MODULES = ["simulation", "monte_carlo", "lattice_run"]
    FORBIDDEN_IN_VERIFICATION = ["biological", "EFT_bio", "consciousness"]
    ZOMBIE_PATTERN = r"\[.+?\]\(\./(.+?)\)"

    # 1. Check directories
    modules_dir = os.path.join(repo_root, "modules")
    if os.path.exists(modules_dir):
        for root, dirs, files in os.walk(modules_dir):
            for file in files:
                for forbidden in FORBIDDEN_IN_MODULES:
                    if forbidden in file:
                        messages.append(f"FAIL: Forbidden term '{forbidden}' in modules/ file: {file}")
                        status = "FAIL"

    verif_dir = os.path.join(repo_root, "verification")
    if os.path.exists(verif_dir):
        for root, dirs, files in os.walk(verif_dir):
            for file in files:
                for forbidden in FORBIDDEN_IN_VERIFICATION:
                    if forbidden in file:
                        messages.append(f"FAIL: Forbidden term '{forbidden}' in verification/ file: {file}")
                        status = "FAIL"

    # 2. Check broken links
    for root, dirs, files in os.walk(repo_root):
        if any(skip in root for skip in [".git", "UIDT-OS", "venv", "clay-submission"]):
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    for match in re.finditer(ZOMBIE_PATTERN, content):
                        link_target = match.group(1)
                        # Remove anchors
                        link_target = link_target.split('#')[0]
                        if not link_target or link_target.startswith('http'):
                            continue

                        target_path = os.path.join(root, link_target)
                        if not os.path.exists(target_path):
                            messages.append(f"FAIL: Broken markdown link in {os.path.basename(filepath)} -> {link_target}")
                            status = "FAIL"
                except Exception:
                    pass

    return status, messages
