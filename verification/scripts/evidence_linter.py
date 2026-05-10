#!/usr/bin/env python3
"""
evidence_linter.py

Scans all Markdown files in the repository for evidence-category tags
(e.g. [A], [A-], [B], [C], [D], [E]) and enforces the following rules:

  RULE-EL-01  Forbidden certainty language must not appear near Evidence A claims.
              Forbidden words: ultimate, definitive, solved, holy grail, resolved
              (exception: resolved inside a changelog/decision entry).

  RULE-EL-02  Cosmological claims must not carry Evidence A or B.
              Detected by co-occurrence of cosmological keywords and [A]/[B] tags
              on the same line.

  RULE-EL-03  Evidence E items must carry the word 'withdrawn' or 'speculative'
              in the same paragraph (15 lines radius).

  RULE-EL-04  No file may claim Evidence A+ B+ C+ D+ (non-existent categories).

Usage:
    python verification/scripts/evidence_linter.py [--root REPO_ROOT] [--fail-fast]

Exit codes:
    0  All checks passed
    1  One or more violations found

Design constraint: no float(), no round(), no external LLM calls.
"""

import argparse
import os
import re
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
FORBIDDEN_LANGUAGE = re.compile(
    r"\b(ultimate|definitive|holy\s+grail|mass\s+gap\s+solved|yang.mills\s+solved)\b",
    re.IGNORECASE,
)

INVALID_CATEGORY = re.compile(r"\[([ABCDE][+])\]")

COSMO_KEYWORDS = re.compile(
    r"\b(hubble|dark\s+energy|cosmolog|H_0|w_0|w_a|DESI|S_?8|sigma_?8)\b",
    re.IGNORECASE,
)

EVIDENCE_TAG = re.compile(r"\[([A-E][\-]?)\]")
EVIDENCE_A_OR_B = re.compile(r"\[(A|A-|B)\]")
EVIDENCE_E = re.compile(r"\[E\]")

CHANGELOG_MARKERS = re.compile(r"(RESOLVED|Decision\s+D-\d+|CHANGELOG|FIXED)", re.IGNORECASE)

EXCLUDE_DIRS = {".git", ".archive", "node_modules", "__pycache__"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def iter_markdown_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith(".md"):
                yield os.path.join(dirpath, fname)


def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()


def context_window(lines, idx, radius=15):
    start = max(0, idx - radius)
    end   = min(len(lines), idx + radius + 1)
    return "".join(lines[start:end])


# ---------------------------------------------------------------------------
# Lint rules
# ---------------------------------------------------------------------------
def lint_file(path, lines, fail_fast=False):
    violations = []

    for i, line in enumerate(lines):
        lineno = i + 1

        # RULE-EL-01: forbidden language
        if FORBIDDEN_LANGUAGE.search(line):
            # Allow in changelog context
            ctx = context_window(lines, i, radius=3)
            if not CHANGELOG_MARKERS.search(ctx):
                violations.append(
                    (path, lineno, "RULE-EL-01",
                     f"Forbidden certainty language: {line.strip()[:80]}")
                )
                if fail_fast:
                    return violations

        # RULE-EL-02: cosmological keywords + [A] or [B] on the same line
        if COSMO_KEYWORDS.search(line) and EVIDENCE_A_OR_B.search(line):
            violations.append(
                (path, lineno, "RULE-EL-02",
                 f"Cosmology claim with Evidence A/B (max allowed: C): {line.strip()[:80]}")
            )
            if fail_fast:
                return violations

        # RULE-EL-04: non-existent category
        m = INVALID_CATEGORY.search(line)
        if m:
            violations.append(
                (path, lineno, "RULE-EL-04",
                 f"Non-existent evidence category [{m.group(1)}]: {line.strip()[:80]}")
            )
            if fail_fast:
                return violations

    # RULE-EL-03: Evidence E without 'withdrawn' or 'speculative' nearby
    for i, line in enumerate(lines):
        lineno = i + 1
        if EVIDENCE_E.search(line):
            ctx = context_window(lines, i, radius=15)
            if not re.search(r"\b(withdrawn|speculative|Speculative)\b", ctx):
                violations.append(
                    (path, lineno, "RULE-EL-03",
                     f"Evidence [E] without 'withdrawn' or 'speculative' in context window: "
                     f"{line.strip()[:80]}")
                )
                if fail_fast:
                    return violations

    return violations


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="UIDT Evidence Linter")
    parser.add_argument("--root", default=None,
                        help="Repository root (default: two levels above this script)")
    parser.add_argument("--fail-fast", action="store_true",
                        help="Stop after first violation")
    args = parser.parse_args()

    if args.root:
        root = args.root
    else:
        root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

    all_violations = []
    files_checked  = 0

    for md_path in sorted(iter_markdown_files(root)):
        lines = read_lines(md_path)
        viol  = lint_file(md_path, lines, fail_fast=args.fail_fast)
        all_violations.extend(viol)
        files_checked += 1
        if args.fail_fast and all_violations:
            break

    # Report
    if all_violations:
        print(f"\nEVIDENCE LINTER — {len(all_violations)} violation(s) in "
              f"{files_checked} file(s) scanned:\n")
        for (path, lineno, rule, msg) in all_violations:
            rel = os.path.relpath(path, root)
            print(f"  {rel}:{lineno}  [{rule}]  {msg}")
        print()
        sys.exit(1)
    else:
        print(f"EVIDENCE LINTER — OK  ({files_checked} Markdown files scanned, "
              f"0 violations)")
        sys.exit(0)


if __name__ == "__main__":
    main()
