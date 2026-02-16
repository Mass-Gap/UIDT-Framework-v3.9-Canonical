from __future__ import annotations

import json

from verification.uidt_os_path import UIDT_OS_PATH, ensure_uidt_os_on_syspath, resolve_uidt_os_path, validate_uidt_os_layout


def run() -> dict:
    root = resolve_uidt_os_path(UIDT_OS_PATH)
    ensure_uidt_os_on_syspath(root)
    layout = validate_uidt_os_layout(root)
    import uidt_os  # noqa: F401
    from uidt_os.orchestration.ralph_wiggum_loop import RalphWiggumLoop  # noqa: F401
    from uidt_os.verification.chain_of_verification import ChainOfVerification  # noqa: F401
    from uidt_os.orchestration.ralph_cove_hybrid import RalphCoVeHybridLoop  # noqa: F401

    return {
        "status": "ok",
        "uidt_os_root": str(layout.root),
        "canonical": str(layout.canonical),
        "ledger": str(layout.ledger),
        "db_path": str(layout.db_path),
    }


def as_dict() -> dict:
    return run()


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))

