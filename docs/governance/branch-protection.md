# Branch Protection Configuration — UIDT v3.9

> This document specifies the required GitHub branch protection rules for the `main` branch.
> These settings must be configured by the repository owner (PI) via GitHub Settings.

## Required Settings for `main`

### 1. Require Pull Request Reviews

- **Required approving reviews:** 1
- **Dismiss stale pull request approvals when new commits are pushed:** ✅
- **Require review from Code Owners:** ✅ (defined in `CODEOWNERS`)

### 2. Require Status Checks

- **Require status checks to pass before merging:** ✅
- **Required checks:**
  - `Check Commit Message Format`
  - `Check Protected Paths`
  - `Run UIDT Verification Suite`
  - `PR Review Summary`

### 3. Branch Restrictions

- **Restrict who can push to matching branches:** ✅
  - Only `@Mass-Gap/P-Rietz`
- **Do not allow force pushes:** ✅
- **Do not allow deletions:** ✅

### 4. Enforce for Administrators

- **Include administrators:** ✅

## Merge Authority

Per the UIDT Constitutional Amendment (2026-04-25):

> **Antigravity (Lead Research Assistant):** PERMANENTLY FORBIDDEN from merging to `main`.
> **Opus 4.7 Desktop:** SOLE authority for merging PRs into `main`.

## How to Configure

1. Go to **Settings** → **Branches** → **Branch protection rules**
2. Click **Add rule**
3. Set **Branch name pattern** to `main`
4. Enable all settings listed above
5. Click **Create**

---

*Configuration guide: 2026-04-26 | DOI: 10.5281/zenodo.17835200*
