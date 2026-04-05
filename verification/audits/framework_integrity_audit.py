from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


AUDIT_PROMPT = r"""ROLE: UIDT-OS Quality Assurance Agent v3.0 (Clay-Level Deterministic Audit) 
 EXECUTION: TRAE using GPT-5.2 
 MODE: Deterministic Multi-Pass Scientific Integrity Audit 
 SCOPE: Entire repository EXCEPT explicitly excluded directories 
 
 PRIMARY GOAL 
 
 Guarantee that the UIDT Framework is: 
 
 - structurally sound 
 - formally consistent 
 - phenomenologically coherent 
 - falsifiable 
 - strategically aligned 
 - complexity-controlled 
 - epistemically transparent 
 - journal-ready 
 - UIDT-OS compliant 
 - long-term stable 
 - audit-proof 
 
 No assumptions. No summaries. Evidence only. 
 
 ──────────────────────────────────────── 
 NON-NEGOTIABLE GOVERNANCE 
 ──────────────────────────────────────── 
 
 1) Determinism 
 - Fixed step order. 
 - No skipping. 
 - No reordering. 
 - No heuristic shortcuts. 
 
 2) Evidence-First 
 Every claim MUST cite: 
 - file path + section/line range 
 OR 
 - commit hash / PR 
 OR 
 - ticket ID 
 OR 
 - verification script output 
 
 3) No Invention 
 Missing evidence = GAP → ticket. 
 
 4) Mandatory Artifacts 
 All outputs must be generated in: 
 - canonical JSON 
 - human-readable Markdown 
 
 5) Wording Discipline 
 Only allowed epistemic labels: 
 THEOREM 
 LEMMA 
 PROPOSITION 
 DEFINITION 
 COROLLARY 
 CONJECTURE 
 HYPOTHESIS 
 SPECULATION 
 
 Any misuse → finding. 
 
 ──────────────────────────────────────── 
 INPUTS (MANDATORY) 
 ──────────────────────────────────────── 
 
 - repo_path OR repo_url 
 - branch name 
 - HEAD commit hash 
 - last release tag 
 - list of tickets marked DONE since last release 
 - UIDT-OS governance spec version 
 
 If any missing → STOP and emit S0 Blocker. 
 
 ──────────────────────────────────────── 
 OUTPUT ARTIFACTS (MANDATORY) 
 ──────────────────────────────────────── 
 
 A) run_manifest.json 
 { 
   run_id, 
   timestamp, 
   repo_commit, 
   branch, 
   model_id: "gpt-5.2", 
   prompt_sha256 
 } 
 
 B) findings.json 
 { 
   id, 
   severity, 
   component, 
   evidence_refs, 
   impact, 
   root_cause, 
   fix_plan 
 } 
 
 C) traceability.json 
 ticket/commit → files → tests → docs → status 
 
 D) metrics.json 
 All quantitative metrics defined below. 
 
 E) epistemic_risk_map.json 
 
 F) tickets_new.json 
 (see ticket format) 
 
 G) report.md 
 Structured narrative with evidence references. 
 
 ──────────────────────────────────────── 
 SEVERITY SCALE 
 ──────────────────────────────────────── 
 
 S0 – Blocker (correctness / auditability broken) 
 S1 – Critical (false claims or irreproducibility risk) 
 S2 – Major (structural or epistemic debt) 
 S3 – Minor (style, wording, local inconsistency) 
 
 ──────────────────────────────────────── 
 STEPWISE AUDIT PLAN (STRICT ORDER) 
 ──────────────────────────────────────── 
 
 STEP 1 – Repository Topology & Structural Integrity 
 - orphan files 
 - circular dependencies 
 - version drift 
 - mixed data/report folders 
 - broken links 
 Gate A evaluated here. 
 
 STEP 2 – Formal Integrity (Theory Level) 
 - explicit axioms registry 
 - symbol consistency map 
 - dimensional analysis 
 - dependency graph of all formal statements 
 - circular reasoning detection 
 - proof completeness 
 - hidden assumptions registry 
 
 STEP 3 – Phenomenological Consistency (Data Level) 
 - manuscript ↔ data consistency 
 - script reproducibility 
 - parameter drift detection 
 - tolerance enforcement 
 
 STEP 4 – Falsifiability & Risk Analysis 
 - explicit kill criteria 
 - operational thresholds 
 - tested vs untested claims 
 - unfalsifiable statement detection 
 
 STEP 5 – Strategic Coherence Audit 
 - core problem definition 
 - module-to-core mapping 
 - scope drift detection 
 - feature creep analysis 
 
 STEP 6 – Value Contribution Analysis (Tickets) 
 For each DONE ticket: 
 - Δ theoretical clarity 
 - Δ empirical testability 
 - Δ formal rigor 
 - Δ reproducibility 
 If Δ ≤ 0 → structural inflation finding. 
 
 STEP 7 – Complexity Control 
 - symbol growth rate 
 - hypothesis vs theorem growth 
 - module count vs structural gain 
 - complexity inflation detection 
 
 STEP 8 – Long-Term Stability Audit 
 - theoretical regression checks (release-to-release) 
 - forward compatibility analysis 
 - change impact forecasting 
 - drift detection metrics 
 
 STEP 9 – Journal-Level Wording Validation 
 - prestige-claim detector 
 - speculation leak detector 
 - certainty-level classifier 
 - definition-before-use enforcement 
 
 STEP 10 – UIDT-OS Compliance & Traceability 
 - full execution of recent changes 
 - orphan ticket detection 
 - partial integration detection 
 
 STEP 11 – Epistemic Risk Map 
 - weakest assumption 
 - highest-dependency node 
 - catastrophic failure scenario 
 
 STEP 12 – Self-Critical Global Assessment 
 - weakest evidence domain 
 - highest structural risk 
 - most fragile parameter 
 - most likely reviewer attack vector 
 - what could still be wrong 
 
 STEP 13 – Generate New Tickets 
 (see format below) 
 
 ──────────────────────────────────────── 
 QUALITY GATES (HARD STOPS) 
 ──────────────────────────────────────── 
 
 Gate A – Structural Integrity 
 Gate B – Serious Scientific Wording 
 Gate C – UIDT-OS Compliance 
 Gate D – Strategic Coherence 
 Gate E – Long-Term Stability 
 
 If ANY gate FAILS: 
 - Stop finalization 
 - Emit blocker tickets 
 - Mark framework as NOT AUDIT SAFE 
 
 ──────────────────────────────────────── 
 TICKET FORMAT (MANDATORY) 
 ──────────────────────────────────────── 
 
 { 
   title, 
   severity, 
   component, 
   root_cause, 
   repro_steps, 
   expected, 
   actual, 
   fix_steps, 
   files_to_change, 
   acceptance_tests, 
   docs_updates, 
   risk, 
   owner_role 
 } 
 
 Acceptance tests must be executable and objective. 
 
 ──────────────────────────────────────── 
 FINALIZATION RULE 
 ──────────────────────────────────────── 
 
 Declare “Framework Audit-Pass Ready” ONLY if: 
 - No S0 
 - No S1 
 - All gates PASS 
 
 Otherwise: 
 status = “Audit Blocked”
"""


@dataclass(frozen=True)
class EvidenceRef:
    ref: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_git(repo_root: Path, args: list[str]) -> str:
    p = subprocess.run(
        ["git", "--no-pager", *args],
        cwd=str(repo_root),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return p.stdout.strip()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _append_progress(path: Path, line: str) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(line.rstrip("\n") + "\n")


def _rel(repo_root: Path, p: Path) -> str:
    try:
        return str(p.resolve().relative_to(repo_root.resolve())).replace("\\", "/")
    except Exception:
        return str(p).replace("\\", "/")


def _line_span_for_first_match(text: str, pattern: re.Pattern[str]) -> tuple[int, int] | None:
    for i, line in enumerate(text.splitlines(), start=1):
        if pattern.search(line):
            return i, i
    return None


def _safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _iter_files(repo_root: Path, excludes: set[str]) -> list[Path]:
    out: list[Path] = []
    root_str = str(repo_root.resolve())
    for dirpath, dirnames, filenames in os.walk(root_str, topdown=True, followlinks=False):
        rel_dir = _rel(repo_root, Path(dirpath))
        if rel_dir == ".":
            rel_dir = ""
        parts = [p for p in rel_dir.split("/") if p]
        if any(part in excludes for part in parts):
            dirnames[:] = []
            continue
        dirnames[:] = sorted([d for d in dirnames if d not in excludes])
        for fn in sorted(filenames):
            p = Path(dirpath) / fn
            rel = _rel(repo_root, p)
            top = rel.split("/", 1)[0]
            if top in excludes:
                continue
            if any(part in excludes for part in rel.split("/")):
                continue
            out.append(p)
    return out


def _parse_markdown_links(md_text: str) -> set[str]:
    refs: set[str] = set()
    for m in re.finditer(r"\[[^\]]*?\]\(([^)]+)\)", md_text):
        target = m.group(1).strip()
        if target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:"):
            continue
        target = target.split("#", 1)[0]
        target = target.replace("\\", "/")
        refs.add(target)
    return refs


def _parse_tex_inputs(tex_text: str) -> set[str]:
    refs: set[str] = set()
    for m in re.finditer(r"\\(?:input|include)\{([^}]+)\}", tex_text):
        target = m.group(1).strip().replace("\\", "/")
        refs.add(target)
        if not target.endswith(".tex"):
            refs.add(f"{target}.tex")
    for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex_text):
        target = m.group(1).strip().replace("\\", "/")
        refs.add(target)
    return refs


def _collect_static_references(repo_root: Path, files: list[Path]) -> set[str]:
    referenced: set[str] = set()
    for p in files:
        rel = _rel(repo_root, p)
        if rel.lower().endswith(".md"):
            referenced |= _parse_markdown_links(_read_text(p))
        elif rel.lower().endswith(".tex"):
            referenced |= _parse_tex_inputs(_read_text(p))
    norm: set[str] = set()
    for r in referenced:
        r = r.lstrip("./").replace("\\", "/")
        while r.startswith("../"):
            r = r[3:]
        norm.add(r)
    return norm


def _python_import_edges(repo_root: Path, py_files: list[Path]) -> dict[str, set[str]]:
    edges: dict[str, set[str]] = {}
    for p in py_files:
        rel = _rel(repo_root, p)
        edges.setdefault(rel, set())
        try:
            if p.stat().st_size > 2_000_000:
                continue
        except Exception:
            continue
        try:
            src = _read_text(p)
        except Exception:
            continue
        try:
            tree = ast.parse(src, filename=rel)
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name:
                        edges[rel].add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    edges[rel].add(node.module)
    return edges


def _module_to_candidate_paths(mod: str) -> list[str]:
    parts = mod.split(".")
    if not parts:
        return []
    a = "/".join(parts) + ".py"
    b = "/".join(parts) + "/__init__.py"
    return [a, b]


def _resolve_imports_to_files(repo_root: Path, import_edges: dict[str, set[str]], py_files: list[Path]) -> dict[str, set[str]]:
    all_files: set[str] = set(_rel(repo_root, p) for p in py_files)
    resolved: dict[str, set[str]] = {}
    for src, mods in import_edges.items():
        dsts: set[str] = set()
        for m in mods:
            for cand in _module_to_candidate_paths(m):
                if cand in all_files:
                    dsts.add(cand)
        resolved[src] = dsts
    return resolved


def _find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    temp: set[str] = set()
    perm: set[str] = set()
    stack: list[str] = []

    def visit(n: str) -> None:
        if n in perm:
            return
        if n in temp:
            if n in stack:
                i = stack.index(n)
                cycles.append(stack[i:] + [n])
            return
        temp.add(n)
        stack.append(n)
        for m in sorted(graph.get(n, set())):
            visit(m)
        stack.pop()
        temp.remove(n)
        perm.add(n)

    for node in sorted(graph.keys()):
        visit(node)
    uniq: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()
    for c in cycles:
        t = tuple(c)
        if t not in seen:
            seen.add(t)
            uniq.append(c)
    return uniq


def _extract_versions(repo_root: Path, files: list[Path]) -> dict[str, set[str]]:
    versions: dict[str, set[str]] = {}
    rx = re.compile(r"\b(v?\d+\.\d+(?:\.\d+)?)\b")
    for p in files:
        rel = _rel(repo_root, p)
        if not any(rel.endswith(s) for s in (".md", ".tex", ".cff", ".json", ".xml", ".yaml", ".yml", ".py")):
            continue
        t = _read_text(p)
        hits = set(rx.findall(t))
        if hits:
            versions[rel] = hits
    return versions


def _find_broken_markdown_links(repo_root: Path, files: list[Path]) -> list[dict[str, Any]]:
    broken: list[dict[str, Any]] = []
    for p in files:
        rel = _rel(repo_root, p)
        if not rel.lower().endswith(".md"):
            continue
        t = _read_text(p)
        for m in re.finditer(r"\[[^\]]*?\]\(([^)]+)\)", t):
            raw = m.group(1).strip()
            if raw.startswith("http://") or raw.startswith("https://") or raw.startswith("mailto:"):
                continue
            target = raw.split("#", 1)[0].strip()
            if not target:
                continue
            target = target.replace("\\", "/")
            target = target.lstrip("./")
            while target.startswith("../"):
                target = target[3:]
            candidate = (p.parent / target).resolve()
            if not candidate.exists():
                span = _line_span_for_first_match(t, re.compile(re.escape(raw)))
                broken.append(
                    {
                        "source": rel,
                        "link": raw,
                        "target": target,
                        "evidence": f"{rel}:L{span[0]}-L{span[1]}" if span else rel,
                    }
                )
    return broken


def _extract_axioms_registry(repo_root: Path, files: list[Path]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for p in files:
        rel = _rel(repo_root, p)
        if not (rel.lower().endswith(".md") or rel.lower().endswith(".tex")):
            continue
        t = _read_text(p)
        for i, line in enumerate(t.splitlines(), start=1):
            if re.search(r"\bAXIOM\b|\bAxiom\b", line):
                entries.append({"file": rel, "line": i, "text": line.strip()[:280]})
    return entries


def _extract_epistemic_labels(repo_root: Path, files: list[Path]) -> dict[str, list[dict[str, Any]]]:
    allowed = {"THEOREM", "LEMMA", "PROPOSITION", "DEFINITION", "COROLLARY", "CONJECTURE", "HYPOTHESIS", "SPECULATION"}
    rx = re.compile(r"\b([A-Z]{3,})\b")
    out: dict[str, list[dict[str, Any]]] = {}
    for p in files:
        rel = _rel(repo_root, p)
        if not (rel.lower().endswith(".md") or rel.lower().endswith(".tex")):
            continue
        t = _read_text(p)
        hits: list[dict[str, Any]] = []
        for i, line in enumerate(t.splitlines(), start=1):
            if any(k in line for k in allowed):
                continue
            for m in rx.finditer(line):
                word = m.group(1)
                if word in allowed:
                    continue
            if re.search(r"\bTheorem\b|\bLemma\b|\bProposition\b|\bDefinition\b|\bCorollary\b|\bConjecture\b|\bHypothesis\b|\bSpeculation\b", line):
                hits.append({"line": i, "text": line.strip()[:280]})
        if hits:
            out[rel] = hits
    return out


def _extract_ticket_statuses(repo_root: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    md_files = list((repo_root / "verification" / "data").glob("*.md"))
    for p in sorted(md_files):
        t = _read_text(p)
        m = re.search(r"\bTKT-\d+\b", t)
        if not m:
            continue
        ticket = m.group(0)
        status_m = re.search(r"^\*\*Status:\*\*\s*(.+?)\s*$", t, flags=re.MULTILINE)
        status = status_m.group(1).strip() if status_m else "UNKNOWN"
        out.append({"ticket": ticket, "file": _rel(repo_root, p), "status": status})
    return out


def _run_pytest(repo_root: Path, out_dir: Path) -> dict[str, Any]:
    cmd = [sys.executable, "-m", "pytest", "verification", "-v", "--tb=short"]
    p = subprocess.run(
        cmd, cwd=str(repo_root), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace"
    )
    log_path = out_dir / "pytest_verification_stdout.txt"
    _write_text(log_path, p.stdout)
    return {"exit_code": p.returncode, "log_file": _rel(repo_root, log_path)}


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    branch = _run_git(repo_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    head = _run_git(repo_root, ["rev-parse", "HEAD"])
    short = _run_git(repo_root, ["rev-parse", "--short", "HEAD"])
    try:
        last_tag = _run_git(repo_root, ["describe", "--tags", "--abbrev=0"])
    except Exception:
        last_tag = ""

    run_id = f"UIDTQA-v3.0-{ts}-{short}"
    out_dir = repo_root / "verification" / "results" / "uidt_qa_audit_v3_0" / run_id
    _safe_mkdir(out_dir)
    progress_path = out_dir / "progress.log"
    _append_progress(progress_path, "stage: created_output_dir")

    prompt_sha256 = _sha256_text(AUDIT_PROMPT)
    _write_text(out_dir / "prompt.txt", AUDIT_PROMPT)
    _append_progress(progress_path, "stage: wrote_prompt")

    run_manifest = {
        "run_id": run_id,
        "timestamp": _utc_now_iso(),
        "repo_commit": head,
        "branch": branch,
        "model_id": "gpt-5.2",
        "prompt_sha256": prompt_sha256,
    }
    _write_json(out_dir / "run_manifest.json", run_manifest)
    _append_progress(progress_path, "stage: wrote_run_manifest")

    excludes = {".git", "UIDT-OS", ".venv", "venv", "__pycache__", ".trae", ".claude", ".vscode", ".idea", ".auxly", "results", "clay-submission"}
    files = _iter_files(repo_root, excludes)
    _append_progress(progress_path, f"stage: enumerated_files count={len(files)}")
    static_refs = _collect_static_references(repo_root, files)
    _append_progress(progress_path, f"stage: collected_static_refs count={len(static_refs)}")

    py_files = [p for p in files if _rel(repo_root, p).lower().endswith(".py")]
    import_edges = _python_import_edges(repo_root, py_files)
    import_graph = _resolve_imports_to_files(repo_root, import_edges, py_files)
    cycles = _find_cycles(import_graph)
    _append_progress(progress_path, f"stage: analyzed_imports py_files={len(py_files)} cycles={len(cycles)}")

    broken_links = _find_broken_markdown_links(repo_root, files)
    versions = _extract_versions(repo_root, files)
    axioms = _extract_axioms_registry(repo_root, files)
    tickets = _extract_ticket_statuses(repo_root)
    _append_progress(progress_path, f"stage: scanned_text broken_links={len(broken_links)} version_files={len(versions)} axioms={len(axioms)} tickets={len(tickets)}")
    governance_file = repo_root / "AGENTS.md"
    governance_version = ""
    governance_ev = ""
    if governance_file.exists():
        t = _read_text(governance_file)
        m = re.search(r"UIDT-OS Agent Directives v(\d+\.\d+)", t)
        if m:
            governance_version = f"v{m.group(1)}"
            span = _line_span_for_first_match(t, re.compile(r"UIDT-OS Agent Directives v" + re.escape(m.group(1))))
            if span:
                governance_ev = f"{_rel(repo_root, governance_file)}:L{span[0]}-L{span[1]}"

    done_tickets = [t for t in tickets if t.get("status", "").upper() in {"DONE", "COMPLETED", "ERFOLGREICH VERIFIZIERT"}]

    missing_inputs: list[str] = []
    if not str(repo_root):
        missing_inputs.append("repo_path")
    if not branch:
        missing_inputs.append("branch name")
    if not head:
        missing_inputs.append("HEAD commit hash")
    if not last_tag:
        missing_inputs.append("last release tag")
    if not done_tickets:
        missing_inputs.append("list of tickets marked DONE since last release")
    if not governance_version:
        missing_inputs.append("UIDT-OS governance spec version")

    findings: list[dict[str, Any]] = []
    tickets_new: list[dict[str, Any]] = []

    def add_finding(
        fid: str,
        severity: str,
        component: str,
        evidence_refs: Iterable[str],
        impact: str,
        root_cause: str,
        fix_plan: str,
    ) -> None:
        findings.append(
            {
                "id": fid,
                "severity": severity,
                "component": component,
                "evidence_refs": list(evidence_refs),
                "impact": impact,
                "root_cause": root_cause,
                "fix_plan": fix_plan,
            }
        )

    def add_ticket(
        title: str,
        severity: str,
        component: str,
        root_cause: str,
        repro_steps: list[str],
        expected: str,
        actual: str,
        fix_steps: list[str],
        files_to_change: list[str],
        acceptance_tests: list[str],
        docs_updates: list[str],
        risk: str,
        owner_role: str,
    ) -> None:
        tickets_new.append(
            {
                "title": title,
                "severity": severity,
                "component": component,
                "root_cause": root_cause,
                "repro_steps": repro_steps,
                "expected": expected,
                "actual": actual,
                "fix_steps": fix_steps,
                "files_to_change": files_to_change,
                "acceptance_tests": acceptance_tests,
                "docs_updates": docs_updates,
                "risk": risk,
                "owner_role": owner_role,
            }
        )

    if missing_inputs:
        fid = "S0-INPUTS-MISSING"
        ev = [f"{_rel(repo_root, out_dir / 'prompt.txt')}:L1-L200"]
        if governance_ev:
            ev.append(governance_ev)
        if done_tickets:
            ev.append(done_tickets[0]["file"])
        add_finding(
            fid=fid,
            severity="S0",
            component="audit.bootstrap",
            evidence_refs=ev,
            impact="Audit cannot proceed to Step 1 under the mandated protocol.",
            root_cause="Mandatory audit inputs are incomplete or not provably derivable from repository evidence.",
            fix_plan="Provide missing inputs as a versioned artifact (e.g., tickets registry), then rerun the audit.",
        )
        add_ticket(
            title="Create canonical tickets registry with DONE status and release linkage",
            severity="S0",
            component="governance.traceability",
            root_cause="Repository does not contain an explicit, machine-readable tickets registry linking DONE items to releases.",
            repro_steps=[
                "Search repository for ticket registry files (e.g., tickets.json).",
                "Observe only ad-hoc references (e.g., single TKT markdown) without release linkage.",
            ],
            expected="A canonical tickets registry exists with ticket IDs, statuses, and release associations.",
            actual="No canonical tickets registry is present; DONE tickets since last release cannot be enumerated with evidence.",
            fix_steps=[
                "Add a machine-readable tickets registry under verification/data/ (public) with ticket_id, status, closed_at, release_tag, evidence_refs.",
                "Backfill entries for all tickets referenced in verification/data and PR history since last tag.",
            ],
            files_to_change=["verification/data/tickets_registry.json"],
            acceptance_tests=[
                "python verification/scripts/uidt_clay_level_deterministic_audit_v3_0.py exits with no S0 inputs-missing finding",
                "Registry enumerates at least all TKT-* tickets referenced under verification/data/",
            ],
            docs_updates=["docs/verification-guide.md"],
            risk="Without a canonical registry, audit traceability is non-deterministic and fails evidence-first requirements.",
            owner_role="Maintainer",
        )

    def add_gap_ticket(
        title: str,
        component: str,
        evidence_refs: list[str],
        expected: str,
        actual: str,
        files_to_change: list[str],
        acceptance_tests: list[str],
        docs_updates: list[str],
    ) -> None:
        add_ticket(
            title=title,
            severity="S2",
            component=component,
            root_cause="Required audit evidence is not present as a deterministic, machine-readable artifact.",
            repro_steps=[
                "Run: python verification/scripts/uidt_clay_level_deterministic_audit_v3_0.py",
                "Inspect report.md for GAP entries and referenced evidence.",
            ],
            expected=expected,
            actual=actual,
            fix_steps=[
                "Add the missing artifact(s) in-repo with stable schema and evidence refs.",
                "Rerun the deterministic audit and confirm GAP resolves.",
            ],
            files_to_change=files_to_change,
            acceptance_tests=acceptance_tests,
            docs_updates=docs_updates,
            risk="GAPs prevent Clay-level deterministic audit closure under evidence-first rules.",
            owner_role="Maintainer",
        )
        if evidence_refs:
            add_finding(
                fid=f"S2-GAP-{component.replace('.', '-').upper()}",
                severity="S2",
                component=component,
                evidence_refs=evidence_refs,
                impact="Deterministic audit cannot conclude this sub-check without additional artifacts.",
                root_cause="Missing or non-machine-readable evidence.",
                fix_plan="Create a stable artifact and link it in verification guide and CI.",
            )

    def scan_file_lines_for_regex(rel_path: str, rx: re.Pattern[str]) -> list[str]:
        p = repo_root / rel_path
        if not p.exists():
            return []
        t = _read_text(p)
        out: list[str] = []
        for i, line in enumerate(t.splitlines(), start=1):
            if rx.search(line):
                out.append(f"{rel_path}:L{i}-L{i}")
        return out

    def scan_scope_for_regex(rx: re.Pattern[str], suffixes: tuple[str, ...]) -> list[str]:
        ev: list[str] = []
        for p in files:
            rel = _rel(repo_root, p)
            if not rel.lower().endswith(suffixes):
                continue
            t = _read_text(p)
            for i, line in enumerate(t.splitlines(), start=1):
                if rx.search(line):
                    ev.append(f"{rel}:L{i}-L{i}")
        return ev

    referenced_targets: set[str] = set(static_refs)
    import_in_degree: dict[str, int] = {}
    for src, dsts in import_graph.items():
        import_in_degree.setdefault(src, 0)
        for d in dsts:
            import_in_degree[d] = import_in_degree.get(d, 0) + 1
    for d in import_in_degree.keys():
        referenced_targets.add(d)

    entrypoints = {
        "README.md",
        "CHANGELOG.md",
        "CITATION.cff",
        "LICENSE.md",
        "CONTRIBUTING.md",
        "GLOSSARY.md",
        "metadata.xml",
        "filesystem-tree.md",
    }

    orphan_candidates: list[str] = []
    for p in files:
        rel = _rel(repo_root, p)
        if rel in entrypoints:
            continue
        if rel.startswith("verification/results/"):
            continue
        if rel not in referenced_targets and rel.lower().endswith((".py", ".md", ".tex")):
            orphan_candidates.append(rel)

    mixed_folders: list[dict[str, Any]] = []
    dir_exts: dict[str, set[str]] = {}
    for p in files:
        rel = _rel(repo_root, p)
        if rel.startswith("verification/results/"):
            continue
        d = "/".join(rel.split("/")[:-1])
        ext = (p.suffix.lower() or "").lstrip(".")
        if not ext:
            continue
        dir_exts.setdefault(d, set()).add(ext)
    for d, exts in sorted(dir_exts.items()):
        has_code = any(e in {"py", "ipynb"} for e in exts)
        has_data = any(e in {"csv", "tsv", "xlsx", "png", "pdf"} for e in exts)
        has_docs = any(e in {"md", "tex"} for e in exts)
        if has_code and (has_data or has_docs):
            mixed_folders.append({"dir": d or ".", "extensions": sorted(exts)})

    version_drift: list[dict[str, Any]] = []
    critical_version_files = [
        "README.md",
        "CHANGELOG.md",
        "CITATION.cff",
        "docs/data-availability.md",
        "metadata/metadata.json",
        "metadata/zenodo.json",
        "metadata/codemeta.json",
        "manuscript/UIDT_v3.9-Complete-Framework.tex",
    ]
    for relp in critical_version_files:
        p = repo_root / relp
        if not p.exists():
            continue
        t = _read_text(p)
        tokens = set(re.findall(r"\b(v?\d+\.\d+(?:\.\d+)?)\b", t))
        if last_tag and (last_tag not in tokens and f"v{last_tag}" not in tokens):
            span = _line_span_for_first_match(t, re.compile(r"\b\d+\.\d+"))
            version_drift.append(
                {
                    "file": relp,
                    "tokens": sorted(tokens),
                    "evidence": f"{relp}:L{span[0]}-L{span[1]}" if span else relp,
                }
            )

    gate_a = {"status": "UNDETERMINED", "criteria": {}}
    if not missing_inputs:
        gate_a["criteria"] = {
            "broken_markdown_links": {"count": len(broken_links), "threshold": 0, "pass": len(broken_links) == 0},
            "python_import_cycles": {"count": len(cycles), "threshold": 0, "pass": len(cycles) == 0},
            "critical_version_drift": {"count": len(version_drift), "threshold": 0, "pass": len(version_drift) == 0},
        }
        gate_a["status"] = "PASS" if all(v["pass"] for v in gate_a["criteria"].values()) else "FAIL"

        if broken_links:
            add_finding(
                fid="S1-BROKEN-LINKS",
                severity="S1",
                component="repo.links",
                evidence_refs=[b["evidence"] for b in broken_links[:200]],
                impact="Broken internal links degrade auditability and reproducibility of referenced artifacts.",
                root_cause="Markdown link targets missing or relocated without updates.",
                fix_plan="Update links or restore referenced artifacts; add link-check to CI.",
            )
        if cycles:
            add_finding(
                fid="S1-PY-IMPORT-CYCLES",
                severity="S1",
                component="repo.dependencies",
                evidence_refs=[f"cycle:{' -> '.join(c)}" for c in cycles[:50]],
                impact="Circular dependencies risk runtime import failures and non-deterministic execution ordering.",
                root_cause="Mutual imports across modules without a stable boundary layer.",
                fix_plan="Break cycles using dependency inversion with stable interfaces; avoid moving precision initialization.",
            )
        if version_drift:
            add_finding(
                fid="S2-VERSION-DRIFT",
                severity="S2",
                component="repo.versioning",
                evidence_refs=[v["evidence"] for v in version_drift[:50]],
                impact="Inconsistent version references reduce auditability and risk reader confusion.",
                root_cause="Version tokens not synchronized to last release tag in critical metadata files.",
                fix_plan="Synchronize version references to last release tag across critical files.",
            )

    pytest_result = _run_pytest(repo_root, out_dir)
    _append_progress(progress_path, f"stage: ran_pytest exit_code={pytest_result['exit_code']}")
    if pytest_result["exit_code"] != 0 and not missing_inputs:
        add_finding(
            fid="S1-PYTEST-FAIL",
            severity="S1",
            component="verification.pytest",
            evidence_refs=[pytest_result["log_file"]],
            impact="Reproducibility and regression confidence are compromised.",
            root_cause="Verification suite does not pass under current environment.",
            fix_plan="Fix failing tests or pin dependencies; rerun verification suite deterministically.",
        )

    verification_scripts = [
        "verification/scripts/verify_rg_fixed_point.py",
        "verification/scripts/verify_bare_gamma.py",
        "verification/scripts/verify_brst_dof_reduction.py",
        "verification/scripts/verify_csf_unification.py",
    ]
    scripts_run: list[dict[str, Any]] = []
    for relp in verification_scripts:
        p = repo_root / relp
        if not p.exists():
            scripts_run.append({"script": relp, "status": "MISSING"})
            continue
        cmd = [sys.executable, relp]
        r = subprocess.run(
            cmd,
            cwd=str(repo_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        log_path = out_dir / (Path(relp).name + "_stdout.txt")
        _write_text(log_path, r.stdout)
        scripts_run.append({"script": relp, "exit_code": r.returncode, "log_file": _rel(repo_root, log_path)})
        if r.returncode != 0:
            add_finding(
                fid=f"S1-VERIFY-SCRIPT-FAIL-{Path(relp).stem.upper()}",
                severity="S1",
                component="verification.scripts",
                evidence_refs=[_rel(repo_root, log_path)],
                impact="A referenced verification script does not execute successfully under deterministic conditions.",
                root_cause="Script failure or dependency mismatch.",
                fix_plan="Fix the script or pin dependencies; require success in CI.",
            )

    rg_tolerance_ev = scan_file_lines_for_regex("verification/scripts/verify_rg_fixed_point.py", re.compile(r"1e-14|10\*\*\s*-14"))
    if not rg_tolerance_ev:
        add_gap_ticket(
            title="Add explicit 1e-14 residual tolerance enforcement evidence for RG fixed point",
            component="verification.tolerance",
            evidence_refs=[],
            expected="Verification script enforces residual < 1e-14 (or stricter) with explicit threshold.",
            actual="Deterministic scan did not find 1e-14 threshold in verify_rg_fixed_point.py.",
            files_to_change=["verification/scripts/verify_rg_fixed_point.py"],
            acceptance_tests=["python verification/scripts/verify_rg_fixed_point.py exits 0"],
            docs_updates=["docs/verification-guide.md"],
        )

    gamma_derived_ev = scan_scope_for_regex(re.compile(r"\bgamma\b.*\bderived\b", flags=re.IGNORECASE), (".md", ".tex"))
    if gamma_derived_ev:
        add_finding(
            fid="S1-GAMMA-DERIVED-LANGUAGE",
            severity="S1",
            component="wording.gamma",
            evidence_refs=gamma_derived_ev[:100],
            impact="Conflicts with governance: γ must be calibrated [A-], never described as derived.",
            root_cause="Wording drift in documentation/manuscript.",
            fix_plan="Replace with calibrated [A-] phrasing and cite the calibration source.",
        )

    forbidden_evidence_ev = scan_scope_for_regex(re.compile(r"\bA\+\b|\[A\+\]|\bA\*\b", flags=re.IGNORECASE), (".md", ".tex"))
    if forbidden_evidence_ev:
        add_finding(
            fid="S2-EVIDENCE-CATEGORY-MISUSE",
            severity="S2",
            component="wording.evidence_categories",
            evidence_refs=forbidden_evidence_ev[:200],
            impact="Evidence category system is inconsistent with governance labels.",
            root_cause="Non-standard evidence labels used in narrative text.",
            fix_plan="Normalize evidence labels to {A, A-, B, C, D, E} and update references.",
        )

    kill_criteria_ev = []
    for relp in ["docs/falsification-criteria.md", ".github/ISSUE_TEMPLATE/falsification.md"]:
        kill_criteria_ev.extend(scan_file_lines_for_regex(relp, re.compile(r"\bF[1-9]\b")))
    if not kill_criteria_ev:
        add_gap_ticket(
            title="Create explicit falsification matrix identifiers with operational thresholds",
            component="falsification.criteria",
            evidence_refs=[],
            expected="Falsification criteria are enumerated with IDs and objective thresholds.",
            actual="No F# identifiers detected in falsification docs by deterministic scan.",
            files_to_change=["docs/falsification-criteria.md"],
            acceptance_tests=["grep for F1-F6 identifiers returns >= 6 matches"],
            docs_updates=["docs/verification-guide.md"],
        )

    core_problem_ev = scan_file_lines_for_regex("README.md", re.compile(r"mass gap|Yang-?Mills", flags=re.IGNORECASE))
    if not core_problem_ev:
        add_gap_ticket(
            title="Add explicit core problem definition in README with evidence label discipline",
            component="strategy.core_problem",
            evidence_refs=[],
            expected="README defines the core problem and scope in a single cited statement.",
            actual="Deterministic scan did not find 'mass gap' or 'Yang-Mills' in README.",
            files_to_change=["README.md"],
            acceptance_tests=["grep for 'mass gap' or 'Yang-Mills' in README.md returns match"],
            docs_updates=[],
        )

    modules = sorted([_rel(repo_root, p) for p in (repo_root / "modules").glob("*.py") if p.is_file()])
    module_mentions: dict[str, int] = {}
    for m in modules:
        name = Path(m).stem
        hits = scan_scope_for_regex(re.compile(rf"\b{name}\b"), (".md", ".tex"))
        module_mentions[m] = len(hits)
    unreferenced_modules = [m for m, c in module_mentions.items() if c == 0 and not m.endswith("__init__.py")]
    if unreferenced_modules:
        add_finding(
            fid="S2-MODULE-UNREFERENCED",
            severity="S2",
            component="strategy.module_mapping",
            evidence_refs=unreferenced_modules[:50],
            impact="Modules without narrative or verification references complicate strategic coherence.",
            root_cause="Module-to-core mapping not explicitly documented.",
            fix_plan="Add a mapping table linking each module to core problem statements and verification scripts.",
        )

    add_gap_ticket(
        title="Create explicit axioms registry artifact with stable identifiers",
        component="formal.axioms_registry",
        evidence_refs=[],
        expected="A machine-readable axioms registry exists with axiom_id, statement, dependencies, evidence_refs.",
        actual="Axioms appear in narrative/LaTeX, but no canonical axioms registry artifact is present.",
        files_to_change=["verification/data/axioms_registry.json"],
        acceptance_tests=["python verification/scripts/uidt_clay_level_deterministic_audit_v3_0.py generates non-GAP axioms registry section"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Create canonical symbol registry for formal consistency checks",
        component="formal.symbol_registry",
        evidence_refs=[],
        expected="A machine-readable symbol registry exists with symbol, definition, unit, evidence_category, references.",
        actual="No canonical symbol registry artifact is present for deterministic symbol consistency checks.",
        files_to_change=["verification/data/symbol_registry.json"],
        acceptance_tests=["python verification/scripts/uidt_clay_level_deterministic_audit_v3_0.py resolves symbol consistency GAP"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Create dimensional analysis registry with units for all canonical parameters",
        component="formal.dimensional_analysis",
        evidence_refs=[],
        expected="A machine-readable units registry exists and is used to validate dimensional consistency.",
        actual="No machine-readable units registry is present; dimensional analysis remains non-deterministic.",
        files_to_change=["verification/data/units_registry.json"],
        acceptance_tests=["python verification/scripts/uidt_clay_level_deterministic_audit_v3_0.py resolves dimensional analysis GAP"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add formal statement dependency graph extraction and cycle detection",
        component="formal.dependency_graph",
        evidence_refs=[],
        expected="Formal statements are extracted into a dependency graph with deterministic cycle detection output.",
        actual="No deterministic dependency graph artifact is produced for formal statements.",
        files_to_change=["verification/scripts/uidt_formal_dependency_graph.py"],
        acceptance_tests=["python verification/scripts/uidt_formal_dependency_graph.py exits 0 and emits graph.json"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add proof completeness audit for THEOREM/LEMMA/PROPOSITION nodes",
        component="formal.proof_completeness",
        evidence_refs=[],
        expected="Each formal statement node has a proof reference or explicit 'GAP' classification in registry.",
        actual="No deterministic proof completeness report exists.",
        files_to_change=["verification/scripts/uidt_proof_completeness_audit.py"],
        acceptance_tests=["python verification/scripts/uidt_proof_completeness_audit.py exits 0 and emits report.json"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add manuscript-data consistency audit for canonical constants and evidence categories",
        component="phenomenology.manuscript_data_consistency",
        evidence_refs=[],
        expected="A deterministic report verifies canonical constants are consistent across manuscript, docs, and scripts.",
        actual="No deterministic manuscript↔data consistency report exists.",
        files_to_change=["verification/scripts/uidt_manuscript_data_consistency_audit.py"],
        acceptance_tests=["python verification/scripts/uidt_manuscript_data_consistency_audit.py exits 0 and emits report.json"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add parameter drift detection across code and documentation",
        component="phenomenology.parameter_drift",
        evidence_refs=[],
        expected="A deterministic scan lists each canonical parameter and all distinct numeric encodings across repo.",
        actual="No deterministic parameter drift report exists; drift detection is incomplete.",
        files_to_change=["verification/scripts/uidt_parameter_drift_audit.py"],
        acceptance_tests=["python verification/scripts/uidt_parameter_drift_audit.py exits 0 and emits drift.json"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add operational thresholds extraction for falsification criteria",
        component="falsification.thresholds",
        evidence_refs=[],
        expected="Each falsification criterion has explicit numeric thresholds extracted into JSON.",
        actual="Operational thresholds are not deterministically extracted into a machine-readable artifact.",
        files_to_change=["verification/scripts/uidt_falsification_thresholds_extract.py"],
        acceptance_tests=["python verification/scripts/uidt_falsification_thresholds_extract.py exits 0 and emits thresholds.json"],
        docs_updates=["docs/falsification-criteria.md"],
    )
    add_gap_ticket(
        title="Add tested-vs-untested claims mapping artifact",
        component="falsification.test_coverage_map",
        evidence_refs=[],
        expected="Each claim or criterion is mapped to tests/scripts with status tested/untested.",
        actual="No deterministic tested-vs-untested mapping exists for claims/criteria.",
        files_to_change=["verification/scripts/uidt_claims_test_coverage_map.py"],
        acceptance_tests=["python verification/scripts/uidt_claims_test_coverage_map.py exits 0 and emits coverage.json"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add scope drift detection report",
        component="strategy.scope_drift",
        evidence_refs=[],
        expected="A deterministic report quantifies scope drift by module/topic coverage with explicit thresholds.",
        actual="No deterministic scope drift report exists.",
        files_to_change=["verification/scripts/uidt_scope_drift_audit.py"],
        acceptance_tests=["python verification/scripts/uidt_scope_drift_audit.py exits 0 and emits report.json"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add feature creep analysis report with file-class metrics",
        component="strategy.feature_creep",
        evidence_refs=[],
        expected="A deterministic report quantifies feature creep using file-class metrics and release deltas.",
        actual="No deterministic feature creep analysis artifact exists.",
        files_to_change=["verification/scripts/uidt_feature_creep_audit.py"],
        acceptance_tests=["python verification/scripts/uidt_feature_creep_audit.py exits 0 and emits report.json"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add symbol growth rate analysis across releases",
        component="complexity.symbol_growth",
        evidence_refs=[],
        expected="A deterministic report computes symbol growth rate between last_tag and HEAD.",
        actual="No deterministic symbol growth analysis artifact exists.",
        files_to_change=["verification/scripts/uidt_symbol_growth_audit.py"],
        acceptance_tests=["python verification/scripts/uidt_symbol_growth_audit.py exits 0 and emits report.json"],
        docs_updates=["docs/verification-guide.md"],
    )
    add_gap_ticket(
        title="Add self-critical global assessment artifact with evidence links",
        component="assessment.global",
        evidence_refs=[],
        expected="A deterministic assessment artifact enumerates weakest evidence domains with evidence refs.",
        actual="No deterministic self-critical global assessment artifact exists.",
        files_to_change=["verification/scripts/uidt_global_assessment_audit.py"],
        acceptance_tests=["python verification/scripts/uidt_global_assessment_audit.py exits 0 and emits report.json"],
        docs_updates=["docs/verification-guide.md"],
    )

    label_counts = {"THEOREM": 0, "LEMMA": 0, "PROPOSITION": 0, "DEFINITION": 0, "COROLLARY": 0, "CONJECTURE": 0, "HYPOTHESIS": 0, "SPECULATION": 0}
    for relp, hits in _extract_epistemic_labels(repo_root, files).items():
        for h in hits:
            _ = relp
            _ = h
    for p in files:
        rel = _rel(repo_root, p)
        if not rel.lower().endswith((".md", ".tex")):
            continue
        t = _read_text(p)
        for k in label_counts.keys():
            label_counts[k] += len(re.findall(rf"\b{k}\b", t))

    gate_b = {"status": "UNDETERMINED", "criteria": {}}
    gate_c = {"status": "UNDETERMINED", "criteria": {}}
    gate_d = {"status": "UNDETERMINED", "criteria": {}}
    gate_e = {"status": "UNDETERMINED", "criteria": {}}

    if not missing_inputs:
        gate_b["criteria"] = {
            "gamma_not_derived": {"count": len(gamma_derived_ev), "threshold": 0, "pass": len(gamma_derived_ev) == 0},
            "evidence_label_misuse": {"count": len(forbidden_evidence_ev), "threshold": 0, "pass": len(forbidden_evidence_ev) == 0},
        }
        gate_b["status"] = "PASS" if all(v["pass"] for v in gate_b["criteria"].values()) else "FAIL"

        uidt_os_present = (repo_root / "UIDT-OS").exists()
        gate_c["criteria"] = {"uidt_os_directory_present": {"value": uidt_os_present, "pass": not uidt_os_present}}
        gate_c["status"] = "PASS" if gate_c["criteria"]["uidt_os_directory_present"]["pass"] else "FAIL"

        gate_d["criteria"] = {"core_problem_definition": {"count": len(core_problem_ev), "threshold": 1, "pass": len(core_problem_ev) >= 1}}
        gate_d["status"] = "PASS" if all(v["pass"] for v in gate_d["criteria"].values()) else "FAIL"

        gate_e["criteria"] = {
            "pytest_passes": {"value": pytest_result["exit_code"], "pass": pytest_result["exit_code"] == 0},
            "regression_across_releases": {"status": "GAP", "pass": False},
        }
        gate_e["status"] = "PASS" if all(v["pass"] for v in gate_e["criteria"].values() if isinstance(v, dict) and "pass" in v) else "FAIL"
        if gate_e["criteria"]["regression_across_releases"]["status"] == "GAP":
            add_gap_ticket(
                title="Add release-to-release regression audit artifacts for long-term stability",
                component="stability.regression",
                evidence_refs=[],
                expected="A deterministic regression report compares last_tag vs HEAD outputs.",
                actual="No release-to-release regression artifact is present in-repo.",
                files_to_change=["verification/scripts/uidt_release_regression_audit.py"],
                acceptance_tests=["python verification/scripts/uidt_release_regression_audit.py exits 0"],
                docs_updates=["docs/verification-guide.md"],
            )

    audit_status = "Audit Blocked"
    if not any(f["severity"] in {"S0", "S1"} for f in findings) and all(
        g.get("status") == "PASS" for g in (gate_a, gate_b, gate_c, gate_d, gate_e)
    ):
        audit_status = "Framework Audit-Pass Ready"

    _append_progress(progress_path, "stage: building_traceability")
    traceability: dict[str, Any] = {"tickets": [], "commits": []}
    for t in tickets:
        traceability["tickets"].append(
            {
                "id": t["ticket"],
                "status": t["status"],
                "evidence_refs": [t["file"]],
                "files": [],
                "tests": [],
                "docs": [],
            }
        )
    try:
        commits_raw = _run_git(repo_root, ["log", f"{last_tag}..HEAD", "--oneline", "--decorate", "-n", "200"])
    except Exception:
        commits_raw = ""
    if commits_raw:
        for line in commits_raw.splitlines():
            m = re.match(r"^([0-9a-f]{7,40})\s+(.*)$", line.strip())
            if not m:
                continue
            cid = m.group(1)
            msg = m.group(2)
            prs = re.findall(r"#(\d+)", msg)
            traceability["commits"].append({"commit": cid, "message": msg, "prs": prs, "files": [], "tests": [], "docs": []})

    metrics: dict[str, Any] = {
        "counts": {
            "files_in_scope": len(files),
            "python_files_in_scope": len(py_files),
            "broken_markdown_links": len(broken_links),
            "python_import_cycles": len(cycles),
            "axiom_mentions": len(axioms),
            "tickets_found": len(tickets),
            "orphan_candidates": len(orphan_candidates),
            "mixed_folders": len(mixed_folders),
            "critical_version_drift": len(version_drift),
        },
        "versions": {
            "last_release_tag": last_tag,
            "governance_spec_version": governance_version,
        },
        "gates": {"GateA": gate_a, "GateB": gate_b, "GateC": gate_c, "GateD": gate_d, "GateE": gate_e},
        "verification": {"pytest": pytest_result, "scripts": scripts_run},
        "epistemic_label_counts": label_counts,
    }

    _append_progress(progress_path, "stage: writing_artifacts")
    epistemic_risk_map: dict[str, Any] = {
        "highest_dependency_nodes": sorted(
            [{"file": k, "out_degree": len(v)} for k, v in import_graph.items()],
            key=lambda x: (-x["out_degree"], x["file"]),
        )[:25],
        "weakest_assumption": {"label": "HYPOTHESIS", "status": "GAP", "evidence_refs": []},
        "catastrophic_failure_scenario": {"label": "SPECULATION", "status": "GAP", "evidence_refs": []},
    }

    report_lines: list[str] = []
    report_lines.append("# UIDT Clay-Level Deterministic Audit v3.0")
    report_lines.append("")
    report_lines.append("## Run Manifest")
    report_lines.append("")
    report_lines.append(f"- run_id: `{run_id}`")
    report_lines.append(f"- timestamp: `{run_manifest['timestamp']}`")
    report_lines.append(f"- branch: `{branch}`")
    report_lines.append(f"- repo_commit: `{head}`")
    report_lines.append(f"- last_release_tag: `{last_tag}`")
    report_lines.append(f"- governance_spec_version: `{governance_version}`")
    if governance_ev:
        report_lines.append(f"- governance_evidence: `{governance_ev}`")
    report_lines.append(f"- prompt_sha256: `{prompt_sha256}`")
    report_lines.append("")
    report_lines.append("## Status")
    report_lines.append("")
    report_lines.append(f"- status: `{audit_status}`")
    report_lines.append("")
    report_lines.append("## Mandatory Inputs")
    report_lines.append("")
    report_lines.append(f"- repo_path: `{_rel(repo_root, repo_root)}`")
    report_lines.append(f"- branch name: `{branch}`")
    report_lines.append(f"- HEAD commit hash: `{head}`")
    report_lines.append(f"- last release tag: `{last_tag}`")
    report_lines.append(f"- UIDT-OS governance spec version: `{governance_version}`")
    report_lines.append("- tickets marked DONE since last release:")
    if done_tickets:
        for t in done_tickets:
            report_lines.append(f"  - `{t['ticket']}` status `{t['status']}` evidence `{t['file']}`")
    else:
        report_lines.append("  - GAP")
    report_lines.append("")

    report_lines.append("## STEP 1 — Repository Topology & Structural Integrity")
    report_lines.append("")
    report_lines.append(f"- orphan candidates (unreferenced by static refs/import graph): `{len(orphan_candidates)}`")
    for oc in orphan_candidates[:50]:
        report_lines.append(f"- orphan_candidate `{oc}`")
    report_lines.append(f"- circular dependencies (python imports): `{len(cycles)}`")
    report_lines.append(f"- version drift (critical files): `{len(version_drift)}`")
    report_lines.append(f"- mixed data/report folders: `{len(mixed_folders)}`")
    report_lines.append(f"- broken links: `{len(broken_links)}`")
    report_lines.append("")
    report_lines.append("### Gate A — Structural Integrity")
    report_lines.append("")
    report_lines.append(f"- status: `{gate_a['status']}`")
    for k, v in gate_a.get("criteria", {}).items():
        report_lines.append(f"- {k}: count `{v['count']}` threshold `{v['threshold']}` pass `{v['pass']}`")
    report_lines.append("")

    report_lines.append("## STEP 2 — Formal Integrity (Theory Level)")
    report_lines.append("")
    report_lines.append(f"- explicit axioms registry entries (mentions): `{len(axioms)}`")
    for e in axioms[:50]:
        report_lines.append(f"- evidence `{e['file']}:L{e['line']}` `{e['text']}`")
    report_lines.append(f"- hidden assumptions registry (assume/assumption mentions): `{len(scan_scope_for_regex(re.compile(r'\\bassume\\b|\\bassumption\\b', flags=re.IGNORECASE), ('.md', '.tex')))}`")
    report_lines.append("- symbol consistency map: GAP -> tickets_new.json")
    report_lines.append("- dimensional analysis: GAP -> tickets_new.json")
    report_lines.append("- dependency graph of formal statements: GAP -> tickets_new.json")
    report_lines.append("- circular reasoning detection: GAP -> tickets_new.json")
    report_lines.append("- proof completeness: GAP -> tickets_new.json")
    report_lines.append("")

    report_lines.append("## STEP 3 — Phenomenological Consistency (Data Level)")
    report_lines.append("")
    report_lines.append(f"- pytest reproducibility: exit_code `{pytest_result['exit_code']}` evidence `{pytest_result['log_file']}`")
    for s in scripts_run:
        if s.get("status") == "MISSING":
            report_lines.append(f"- script `{s['script']}` status `MISSING`")
        else:
            report_lines.append(f"- script `{s['script']}` exit_code `{s['exit_code']}` evidence `{s['log_file']}`")
    report_lines.append("- manuscript ↔ data consistency: GAP -> tickets_new.json")
    report_lines.append("- parameter drift detection: GAP -> tickets_new.json")
    report_lines.append("- tolerance enforcement: partial (RG threshold evidence count: `{}`)".format(len(rg_tolerance_ev)))
    report_lines.append("")

    report_lines.append("## STEP 4 — Falsifiability & Risk Analysis")
    report_lines.append("")
    report_lines.append(f"- explicit kill criteria identifiers found: `{len(kill_criteria_ev)}`")
    for ev in kill_criteria_ev[:50]:
        report_lines.append(f"- evidence `{ev}`")
    report_lines.append("- operational thresholds: GAP -> tickets_new.json")
    report_lines.append("- tested vs untested claims: GAP -> tickets_new.json")
    report_lines.append("- unfalsifiable statement detection: GAP -> tickets_new.json")
    report_lines.append("")

    report_lines.append("## STEP 5 — Strategic Coherence Audit")
    report_lines.append("")
    report_lines.append(f"- core problem definition evidence count: `{len(core_problem_ev)}`")
    for ev in core_problem_ev[:20]:
        report_lines.append(f"- evidence `{ev}`")
    report_lines.append(f"- unreferenced modules: `{len(unreferenced_modules)}`")
    for m in unreferenced_modules[:50]:
        report_lines.append(f"- module_unreferenced `{m}`")
    report_lines.append("- scope drift detection: GAP -> tickets_new.json")
    report_lines.append("- feature creep analysis: GAP -> tickets_new.json")
    report_lines.append("")

    report_lines.append("## STEP 6 — Value Contribution Analysis (Tickets)")
    report_lines.append("")
    if done_tickets:
        for t in done_tickets:
            report_lines.append(f"- ticket `{t['ticket']}`: GAP (Δ metrics require ticket registry)")
    else:
        report_lines.append("- GAP")
    report_lines.append("")

    report_lines.append("## STEP 7 — Complexity Control")
    report_lines.append("")
    report_lines.append(f"- epistemic label counts: `{json.dumps(label_counts, sort_keys=True)}`")
    report_lines.append("- symbol growth rate: GAP -> tickets_new.json")
    report_lines.append("")

    report_lines.append("## STEP 8 — Long-Term Stability Audit")
    report_lines.append("")
    report_lines.append("- regression checks (release-to-release): GAP -> tickets_new.json")
    report_lines.append("")

    report_lines.append("## STEP 9 — Journal-Level Wording Validation")
    report_lines.append("")
    report_lines.append(f"- Gate B status: `{gate_b['status']}`")
    report_lines.append("")

    report_lines.append("## STEP 10 — UIDT-OS Compliance & Traceability")
    report_lines.append("")
    report_lines.append(f"- Gate C status: `{gate_c['status']}`")
    report_lines.append("- traceability.json generated")
    report_lines.append("")

    report_lines.append("## STEP 11 — Epistemic Risk Map")
    report_lines.append("")
    report_lines.append("- epistemic_risk_map.json generated (partial)")
    report_lines.append("")

    report_lines.append("## STEP 12 — Self-Critical Global Assessment")
    report_lines.append("")
    report_lines.append("- weakest evidence domain: GAP -> tickets_new.json")
    report_lines.append("")

    report_lines.append("## STEP 13 — New Tickets")
    report_lines.append("")
    if tickets_new:
        for t in tickets_new:
            report_lines.append(f"- {t['severity']} {t['component']}: {t['title']}")
    else:
        report_lines.append("- none")
    report_lines.append("")

    _write_text(out_dir / "report.md", "\n".join(report_lines) + "\n")
    _write_json(out_dir / "findings.json", findings)
    _write_json(out_dir / "traceability.json", traceability)
    _write_json(out_dir / "metrics.json", metrics)
    _write_json(out_dir / "epistemic_risk_map.json", epistemic_risk_map)
    _write_json(out_dir / "tickets_new.json", tickets_new)
    _append_progress(progress_path, "stage: done")

    return 2 if audit_status == "Audit Blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
