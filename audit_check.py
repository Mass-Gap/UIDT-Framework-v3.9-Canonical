import os
import re

directories = [
    'core',
    'modules',
    'verification/scripts'
]

# Patterns to search for (Forbidden)
forbidden_patterns = {
    'float_call': re.compile(r'float\('),
    'numpy_float64': re.compile(r'numpy\.float64'),
    'import_math': re.compile(r'import math'),
    'from_math': re.compile(r'from math'),
}

# Patterns to search for (Required)
required_patterns = {
    'mp_dps_80': re.compile(r'(?:mp|mpmath\.mp)\.dps\s*=\s*80'),
}

findings = []
files_checked = 0

for directory in directories:
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        continue

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                filepath = os.path.join(root, file)
                files_checked += 1

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    content = "".join(lines)

                    # Check for forbidden patterns
                    for issue_name, pattern in forbidden_patterns.items():
                        for i, line in enumerate(lines):
                            if pattern.search(line):
                                # Context check: ignore if in comment
                                if line.strip().startswith('#'):
                                    continue

                                findings.append({
                                    'file': filepath,
                                    'line': i + 1,
                                    'issue': f"Forbidden: {issue_name}",
                                    'code': line.strip()
                                })

                    # Check for required patterns
                    # We assume these are mathematical files.
                    # If mpmath is imported, it likely needs mp.dps = 80
                    if 'import mpmath' in content or 'from mpmath' in content:
                        has_dps = False
                        for line in lines:
                            if required_patterns['mp_dps_80'].search(line):
                                has_dps = True
                                break
                        if not has_dps:
                            findings.append({
                                'file': filepath,
                                'line': 0, # Whole file issue
                                'issue': "Missing: mp.dps = 80",
                                'code': "N/A"
                            })

                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

if findings:
    print(f"Found {len(findings)} issues in {files_checked} files:")
    for f in findings:
        print(f"{f['file']}:{f['line']} - {f['issue']} -> {f['code']}")
else:
    print(f"System 100% mpmath-compliant (Checked {files_checked} files)")
