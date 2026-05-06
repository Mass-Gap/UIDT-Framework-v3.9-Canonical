[VERIFICATION_FAIL] ALPHA-01 2026-05-02: verify_mass_gap_core.py

**Error output:**
```
/home/jules/.pyenv/versions/3.12.13/bin/python: can't open file '/app/verification/scripts/verify_mass_gap_core.py': [Errno 2] No such file or directory
```

**Last known good commit SHA:** 30ee0be

The script `verify_mass_gap_core.py` is listed in the AGENTS.md instructions for ALPHA-01, but the file does not exist in the repository under `verification/scripts/`.
