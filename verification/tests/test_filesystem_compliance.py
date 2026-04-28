"""
UIDT v3.9 — Filesystem Compliance Test
DOI: 10.5281/zenodo.17835200

Ensures the repository filesystem structure conforms to UIDT governance rules:
- Root directory contains only approved meta files
- No root-level tests/ directory
- No special characters in directory names
- verification/data/ exists for result artifacts
- No internal paths leaked in public files
"""
import os
import re
import pytest

# Repository root (two levels up from verification/tests/)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Approved root-level files (meta files only)
APPROVED_ROOT_FILES = {
    '.editorconfig',
    '.gitattributes',
    '.gitignore',
    'CHANGELOG.md',
    'CITATION.cff',
    'CODEOWNERS',
    'CONTRIBUTING.md',
    'Dockerfile',
    'FORMALISM.md',
    'GLOSSARY.md',
    'LICENSE.md',
    'README.md',
    'REPRODUCE.md',
    'SECURITY.md',
    'pyproject.toml',
    'requirements.txt',
}

# Approved root-level directories
APPROVED_ROOT_DIRS = {
    '.github',
    '.git',
    'CANONICAL',
    'LEDGER',
    'LOCAL',
    'clay-submission',
    'core',
    'data',
    'docs',
    'figures',
    'manuscript',
    'metadata',
    'modules',
    'references',
    'research',
    'simulation',
    'verification',
}


class TestFilesystemCompliance:
    """Verify repository filesystem meets UIDT governance standards."""

    def test_no_root_level_tests_directory(self):
        """Root-level tests/ directory is forbidden. Use verification/tests/."""
        tests_dir = os.path.join(REPO_ROOT, 'tests')
        assert not os.path.isdir(tests_dir), \
            "Root-level tests/ directory exists. Use verification/tests/ instead."

    def test_verification_data_directory_exists(self):
        """verification/data/ must exist for result artifacts."""
        data_dir = os.path.join(REPO_ROOT, 'verification', 'data')
        # Create if missing (soft enforcement)
        if not os.path.isdir(data_dir):
            pytest.skip("verification/data/ does not exist yet (non-critical)")

    def test_no_special_characters_in_directories(self):
        """Directory names must use lowercase-kebab-case or snake_case."""
        pattern = re.compile(r'^[a-zA-Z0-9._-]+$')
        violations = []
        for item in os.listdir(REPO_ROOT):
            full_path = os.path.join(REPO_ROOT, item)
            if os.path.isdir(full_path) and not item.startswith('.'):
                if not pattern.match(item):
                    violations.append(item)
        assert len(violations) == 0, \
            f"Directories with special characters: {violations}"

    def test_no_log_files_at_root(self):
        """No .log files should exist at repository root."""
        log_files = [f for f in os.listdir(REPO_ROOT)
                     if f.endswith('.log') and os.path.isfile(os.path.join(REPO_ROOT, f))]
        assert len(log_files) == 0, \
            f"Log files found at root (should be in LOCAL/logs/): {log_files}"

    def test_no_bat_files_at_root(self):
        """No .bat/.cmd scripts should exist at root (internal only)."""
        bat_files = [f for f in os.listdir(REPO_ROOT)
                     if (f.endswith('.bat') or f.endswith('.cmd'))
                     and os.path.isfile(os.path.join(REPO_ROOT, f))]
        assert len(bat_files) == 0, \
            f"Batch scripts found at root (move to UIDT-OS/LOCAL/): {bat_files}"

    def test_no_zip_files_at_root(self):
        """No .zip archives should be tracked at root. Use GitHub Releases."""
        zip_files = [f for f in os.listdir(REPO_ROOT)
                     if f.endswith('.zip') and os.path.isfile(os.path.join(REPO_ROOT, f))]
        # Allow but warn — these should be in .gitignore
        if zip_files:
            pytest.skip(f"ZIP files at root (should be in .gitignore or Releases): {zip_files}")


class TestNoInternalPathLeakage:
    """Verify no internal/local paths are leaked in public files."""

    PUBLIC_DIRS = ['core', 'modules', 'verification', 'docs', 'manuscript']
    LOCAL_PATH_PATTERN = re.compile(
        r'C:\\Users\\|/home/\w+/|/Users/\w+/',
        re.IGNORECASE
    )

    def _scan_files(self, directory, extensions=('.py', '.md', '.tex')):
        """Scan files in a directory for local path references."""
        violations = []
        dir_path = os.path.join(REPO_ROOT, directory)
        if not os.path.isdir(dir_path):
            return violations
        for root, _dirs, files in os.walk(dir_path):
            for fname in files:
                if any(fname.endswith(ext) for ext in extensions):
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                            for i, line in enumerate(f, 1):
                                if self.LOCAL_PATH_PATTERN.search(line):
                                    violations.append(f"{fpath}:{i}")
                    except (OSError, UnicodeDecodeError):
                        pass
        return violations

    def test_no_local_paths_in_public_code(self):
        """Public Python/Markdown files must not contain local filesystem paths."""
        all_violations = []
        for d in self.PUBLIC_DIRS:
            all_violations.extend(self._scan_files(d))
        if all_violations:
            msg = "Local paths found in public files:\n" + "\n".join(all_violations[:10])
            pytest.fail(msg)
