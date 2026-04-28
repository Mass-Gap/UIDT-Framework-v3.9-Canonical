---
alwaysApply: false
description: Apply when creating new files, directories, or verification scripts.
---
# File Architecture (Intelligent)

- All verification scripts/tests live in `verification/tests/` or `verification/scripts/`.
- Never create a root-level `tests/` directory.
- Do not write into protected/publication paths unless explicitly authorized.
- Treat `UIDT-OS/`, `.kiro/`, and `LOCAL/` as internal runtime support: never publish or commit their contents.
