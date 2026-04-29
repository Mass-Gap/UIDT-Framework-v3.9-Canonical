import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    LINK_PATTERN = r"\[.+?\]\(\.{0,2}/(.+?\.md)\)"

    file_deps = {}

    for root, dirs, files in os.walk(repo_root):
        if any(skip in root for skip in [".git", "UIDT-OS", "venv", "clay-submission"]):
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, repo_root)
                file_deps[rel_path] = []
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    for match in re.finditer(LINK_PATTERN, content):
                        target = match.group(1)
                        # Clean target
                        target = target.split('#')[0]
                        file_deps[rel_path].append(target)
                except Exception:
                    pass

    # Check cycles (naive depth 2 check)
    for f, deps in file_deps.items():
        if os.path.basename(f) in [os.path.basename(d) for d in deps]:
            messages.append(f"FAIL: File self-references non-trivially: {f}")
            status = "FAIL"

        for d in deps:
            # if d refers back to f
            target_key = next((k for k in file_deps.keys() if os.path.basename(k) == os.path.basename(d)), None)
            if target_key and target_key != f:
                if os.path.basename(f) in [os.path.basename(x) for x in file_deps.get(target_key, [])]:
                    messages.append(f"FAIL: Cyclic dependency between {f} and {target_key}")
                    status = "FAIL"

    return status, messages
