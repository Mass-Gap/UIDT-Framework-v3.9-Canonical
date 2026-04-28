"""
UIDT v3.9 — Gitignore Leakage Prevention Test
DOI: 10.5281/zenodo.17835200

Ensures that internal/sensitive files are properly excluded from version control.
This test prevents accidental exposure of:
- UIDT-OS operational system
- Agent configuration files
- Environment variables and API keys
- Internal governance documents
"""
import os
import subprocess
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Files that MUST be in .gitignore and NOT tracked
MUST_NOT_BE_TRACKED = [
    'UIDT-OS/',
    'AGENTS.md',
    '.env',
    '.claude/',
    '.mcp.json',
    'CLAUDE.md',
    '.trae/',
    '.kiro/',
    '.antigravity/',
]


def get_tracked_files():
    """Get list of all git-tracked files."""
    try:
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        return set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
    except FileNotFoundError:
        pytest.skip("git not available")
        return set()


class TestGitignoreLeakage:
    """Verify no internal files leak into version control."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.tracked = get_tracked_files()

    def test_uidt_os_not_tracked(self):
        """UIDT-OS/ directory must not be in version control."""
        uidt_os_files = [f for f in self.tracked if f.startswith('UIDT-OS/')]
        assert len(uidt_os_files) == 0, \
            f"UIDT-OS files are tracked (CRITICAL LEAK): {uidt_os_files[:5]}"

    def test_agents_md_not_tracked(self):
        """AGENTS.md must not be tracked (internal governance)."""
        assert 'AGENTS.md' not in self.tracked, \
            "AGENTS.md is tracked — contains internal agent rules"

    def test_security_md_is_tracked(self):
        """Public SECURITY.md (vulnerability disclosure) must be tracked."""
        assert 'SECURITY.md' in self.tracked, \
            "SECURITY.md (public vulnerability policy) must be tracked for GitHub Security tab"

    def test_no_env_files_tracked(self):
        """No .env files should be tracked."""
        env_files = [f for f in self.tracked if '.env' in os.path.basename(f)]
        assert len(env_files) == 0, \
            f".env files are tracked (CRITICAL LEAK): {env_files}"

    def test_no_claude_config_tracked(self):
        """No Claude/AI configuration directories should be tracked."""
        ai_dirs = ['.claude/', '.mcp.json', 'CLAUDE.md']
        leaked = [d for d in ai_dirs if any(f.startswith(d.rstrip('/')) for f in self.tracked)]
        assert len(leaked) == 0, \
            f"AI configuration files are tracked: {leaked}"

    def test_gitignore_has_critical_entries(self):
        """Verify .gitignore contains all critical exclusion patterns."""
        gitignore_path = os.path.join(REPO_ROOT, '.gitignore')
        assert os.path.isfile(gitignore_path), ".gitignore missing"

        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()

        critical_patterns = ['UIDT-OS/', 'AGENTS.md', '.env', '.claude/']
        missing = [p for p in critical_patterns if p not in content]
        assert len(missing) == 0, \
            f"Critical patterns missing from .gitignore: {missing}"

    def test_gitignore_not_self_referencing(self):
        """Gitignore must not ignore itself."""
        gitignore_path = os.path.join(REPO_ROOT, '.gitignore')
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if not line.startswith('#') and line.strip()]

        # Check that .gitignore is not listed as a pattern
        self_refs = [l for l in lines if l == '.gitignore']
        assert len(self_refs) == 0, \
            ".gitignore contains self-referencing entry (ignoring itself!)"
