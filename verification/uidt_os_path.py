from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class UIDTOsLayout:
    root: Path
    canonical: Path
    ledger: Path
    db_path: Path


def resolve_uidt_os_path(explicit: Optional[str | Path] = None) -> Path:
    preferred = Path(
        r"C:\Users\badbu\Documents\UIDT-Framework-V3.2-Canonical-main\UIDT-Framework-V3.6.1\UIDT-OS"
    )
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    env = os.getenv("UIDT_OS_PATH")
    if env:
        candidates.append(Path(env))
    candidates.append(preferred)

    repo_root = Path(__file__).resolve().parents[1]
    candidates.append(repo_root / "UIDT-OS")
    candidates.append(repo_root / "uidt-os")

    for c in candidates:
        try:
            if c.exists() and c.is_dir():
                return c.resolve()
        except Exception:
            continue
    return preferred


def validate_uidt_os_layout(uidt_os_path: str | Path) -> UIDTOsLayout:
    root = Path(uidt_os_path).resolve()
    canonical = root / "CANONICAL"
    ledger = root / "LEDGER"
    db_path = root / "LOCAL" / "database" / "uidt_os.db"
    missing: list[str] = []
    if not canonical.exists():
        missing.append("CANONICAL")
    if not ledger.exists():
        missing.append("LEDGER")
    if not db_path.exists():
        missing.append("LOCAL/database/uidt_os.db")
    if missing:
        raise FileNotFoundError(f"UIDT-OS layout missing: {', '.join(missing)} (root={root})")
    return UIDTOsLayout(root=root, canonical=canonical, ledger=ledger, db_path=db_path)


def ensure_uidt_os_on_syspath(uidt_os_path: str | Path) -> Path:
    root = Path(uidt_os_path).resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


try:
    UIDT_OS_PATH = resolve_uidt_os_path()
except Exception:
    UIDT_OS_PATH = Path(
        r"C:\Users\badbu\Documents\UIDT-Framework-V3.2-Canonical-main\UIDT-Framework-V3.6.1\UIDT-OS"
    )

