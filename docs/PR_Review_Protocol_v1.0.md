# UIDT v3.9 — Formalized Pull Request Review Protocol v1.0

**Effective:** 2026-02-28
**Scope:** All PRs into `Mass-Gap/UIDT-Framework-v3.9-Canonical`
**Authority:** Supersedes ad-hoc merge decisions. Binding for all merge agents (human, Claude, Jules).
**Baseline:** UIDT-OS v3.7.3 `data/canonical/` + `data/ledger/` as single source of truth.

---

## 0. MANDATORY PRE-MERGE INITIALIZATION

Before evaluating ANY Pull Request, the reviewing agent MUST execute:

```
1. uidt-os:get_project_instructions()    → Load evidence system, rules, limitations
2. uidt-os:get_canonical_values()         → Load Δ*, γ, κ, λ_S, v, m_S, H₀
3. uidt-os:get_limitations()              → Load L1–L7 + falsification criteria F1–F4
4. uidt-os:get_claims(limit=100)          → Load all 42+ canonical claims
```

If ANY of these calls fail → PR review CANNOT proceed. Log as S0 Blocker.

---

## 1. STRUCTURAL TRIAGE (Automated, ≤ 30 seconds)

For each PR, determine:

| Check | Action |
|-------|--------|
| Files changed = 0 | → CLOSE as empty scaffolding |
| Contains `UIDT-OS/` files | → Flag 🔴 UIDT-OS contamination. Cherry-pick only non-OS content. |
| Only new files (`status: added`) | → Flag 🟢 safe for auto-merge consideration |
| Modifies `theoretical_notes.md` | → Flag 🟡 append-conflict risk, manual merge |
| Modifies `modules/*.py` or `verification/*.py` | → Flag ⚪ code review required |
| Modifies `manuscript/*.tex` or `clay-submission/` | → Flag 🔵 publication-grade review |

---

## 2. PARAMETER CONSISTENCY CHECK (Gate A — Hard Stop)

Every numeric value in the PR diff MUST be cross-referenced against CANONICAL/CONSTANTS.md:

| Parameter | Canonical Value | Tolerance | Evidence |
|-----------|----------------|-----------|----------|
| Δ* | 1.710 ± 0.015 GeV | exact match | [A] |
| γ (kinetic) | 16.339 | exact match | [A-] |
| γ (MC) | 16.374 ± 1.005 | within stated σ | [A-] |
| κ | 0.500 ± 0.008 | exact match | [A] |
| λ_S | 0.417 ± 0.007 | exact match | [A] |
| v | 47.7 MeV | exact match | [A] |
| m_S | 1.705 ± 0.015 GeV | exact match | [D] |
| H₀ | 70.4 ± 0.16 km/s/Mpc | exact match | [C] |
| 5κ² = 3λ_S | 1.250 ≈ 1.251 | |Δ| < 0.01 | [A] |

**FAIL conditions:**
- Any parameter value that deviates from canonical without explicit justification → REJECT
- Any parameter tagged with a HIGHER evidence category than canonical → REJECT
- Any new parameter NOT present in `data/canonical/CONSTANTS.md` used without [D] or [E] tag → FLAG

**Known tension parameters requiring special attention:**
- N (RG steps): CLAIMS.json says N=99 [E/open]. theoretical_notes §12 says N=94.05. Code uses N=99. → Any PR touching N MUST explicitly state which value and why.
- w₀: Canonical w₀ = −0.99 [C] (Decision D-002). UIDT-C-037 updated. Any PR using w₀ must use −0.99.
- w_a: Not in CLAIMS.json. Two derivations exist (-1.183 with L=8, -1.300 with L=8.2). → PR MUST state which L and why.
- L (holographic length): NOT a canonical parameter. Any use requires [C/D] tag.

---

## 3. EVIDENCE CATEGORY VALIDATION (Gate B — Hard Stop)

### 3.1 Category Assignment Rules

| Rule | Violation = |
|------|-------------|
| Cosmology claim tagged [A] or [B] | S1 — REJECT |
| γ tagged anything other than [A-] | S1 — REJECT |
| H₀ described as "predicted" or "derived" | S1 — REJECT |
| Prediction without falsification criterion | S1 — REJECT |
| [B] claim without z-score < 1σ verification | S1 — REJECT |
| [A] claim without residual < 10⁻¹⁴ | S1 — REJECT |
| Glueball = particle mass (withdrawn [E]) | S0 — REJECT |
| [A+] category used (does not exist) | S2 — flag for correction |

### 3.2 Evidence Stratification (Required for all scientific PRs)

Every PR that introduces or modifies a scientific claim MUST separate content into three strata:

**Stratum I — Empirical:**
- Direct measurements with stated uncertainties
- Citation with DOI or arXiv ID
- Example: "Lattice QCD: Δ = 1.710 ± 0.040 GeV (Morningstar et al. 2024, doi:10.xxxx)"

**Stratum II — Consensus:**
- Field-level status with appropriate hedging
- Example: "Hubble tension persists at 4-6σ between early- and late-universe methods (Verde et al. 2024)"

**Stratum III — UIDT:**
- Interpretive mapping to UIDT parameters
- MUST be labeled as "UIDT interpretation" or "model-dependent" if not externally validated
- Example: "UIDT proposes [C] H₀ = 70.4 ± 0.16 km/s/Mpc, calibrated to DESI DR2"

**Missing stratification for any claim → S2 finding, PR requires revision before merge.**

---

## 4. LANGUAGE AUDIT (Gate C)

### 4.1 Forbidden Language (unless conditions met)

| Phrase | Allowed only if | Otherwise |
|--------|----------------|-----------|
| "proves" / "beweist" | Theorem + formal proof + [A] residual | S2 — replace with "demonstrates consistency" |
| "resolves" / "löst" | Only for mathematical contradictions with [A] evidence | S2 — replace with "addresses" or "proposes resolution" |
| "complete solution" | Never for UIDT as a whole | S1 — remove |
| "definitive" / "endgültig" | Only for [A] claims with residual < 10⁻¹⁴ | S2 — replace with "consistent" |
| "holy grail" / "ultimate" | Never | S2 — remove |
| "parameter-free" | Only if ALL inputs are from QCD constants, no fitting | S1 — remove (L1 violation) |
| "solves Hubble tension" | Never (cosmology ≤ [C]) | S1 — replace with "calibrated to DESI" |
| "derived" for γ | Never in OUTPUT-MODE (L4) | S1 — replace with "calibrated [A-]" |

### 4.2 Required Epistemic Labels

Every non-trivial scientific claim must carry one of:
THEOREM, LEMMA, PROPOSITION, DEFINITION, COROLLARY, CONJECTURE, HYPOTHESIS, SPECULATION

Unlabeled strong claims → S2 finding.

---

## 5. NUMERICAL INTEGRITY (Gate D)

### 5.1 Uncertainty Requirements

Every quantitative value MUST include:
- ± uncertainty (stat, sys, or combined — specify which)
- Evidence category tag [A–E]
- Unit

**Missing uncertainty → S2 finding.** Exception: exact mathematical identities (e.g., 5κ² = 3λ_S).

### 5.2 Z-Score / σ-Agreement Requirements

Any statement of the form "agrees at Xσ" MUST specify:
1. The two quantities being compared (name, value, source for each)
2. How combined uncertainty was constructed (quadrature, correlated, etc.)
3. Whether correlations are included (if not: mark as "heuristic")

### 5.3 Internal vs External Ground Truth

UIDT-calibrated values (e.g., H₀ = 70.4) are NEVER treated as empirical ground truth for σ-comparisons. They are model outputs [C].

---

## 6. CITATION & DOI REQUIREMENTS (Gate E)

Every external numeric value requires at least one of:
- DOI resolvable via doi.org
- arXiv ID + arXiv DOI (10.48550/arXiv.xxxxx)
- Publisher URL (only if DOI unavailable)

**Additional rules:**
- The cited paper must actually contain the stated value in the stated context
- No "nearby" or "similar" paper substitution
- Bibliography entries must include resolvable identifiers, not placeholders
- Broken LaTeX delimiters in citations → S3 finding

---

## 7. UIDT-OS COMPLIANCE (Gate F)

### 7.1 File Containment

| Rule | Action |
|------|--------|
| PR adds files under `UIDT-OS/` | Cherry-pick only non-OS files. Remove OS files post-merge if leaked. |
| PR modifies `UIDT-OS/CANONICAL/` | REJECT — canonical files are immutable within the v3.9 repo |
| PR modifies `UIDT-OS/LEDGER/` | REJECT — ledger managed separately |

### 7.2 Claims Registry Sync

After merge, check if PR introduces claims NOT present in CLAIMS.json:
- New parameter values → propose CLAIMS.json entry
- New predictions → require falsification criterion
- New evidence categories → validate against EVIDENCE_SYSTEM.md rules

### 7.3 Limitation Acknowledgment

If PR content touches any of L1–L7, the relevant limitation MUST be explicitly acknowledged in the PR text. Failure → S2 finding.

---

## 8. POST-MERGE ACTIONS (Mandatory)

After every successful merge:

```
1. Verify no UIDT-OS/ files leaked:
   git ls-files | grep "UIDT-OS/" → must be empty

2. Update UIDT-OS claims for new discoveries:
   - New parameters → uidt-os claims update
   - New predictions → with falsification criteria
   - Evidence category changes → with justification
   
3. Clean stale branches:
   Delete merged feature branches (preserve main + any active draft PRs)

4. Log merge in session transcript:
   PR#, commit hash, files changed, findings, evidence updates
```

---

## 9. SEVERITY CLASSIFICATION

| Level | Name | Meaning | PR Action |
|-------|------|---------|-----------|
| S0 | Blocker | Correctness broken, canonical violation | REJECT — cannot merge |
| S1 | Critical | False claims, evidence inflation, reproducibility | REJECT — requires revision |
| S2 | Major | Structural debt, missing labels, wording | MERGE with mandatory follow-up ticket |
| S3 | Minor | Style, local inconsistency | MERGE — note for future cleanup |

---

## 10. PR GATE CHECKLIST (Summary)

Before approving ANY PR for merge, verify ALL gates pass:

- [ ] **Gate A** — Parameter Consistency: All values match CANONICAL/CONSTANTS.md
- [ ] **Gate B** — Evidence Categories: No inflation, cosmology ≤ [C], γ = [A-]
- [ ] **Gate C** — Language: No prestige claims, proper epistemic labels
- [ ] **Gate D** — Numerics: All values have ±, z-scores properly constructed
- [ ] **Gate E** — Citations: DOI/arXiv resolvable, values actually in cited source
- [ ] **Gate F** — UIDT-OS: No OS files in repo, claims registry synced
- [ ] **Gate G** — Strata: Empirical / Consensus / UIDT clearly separated

**ALL gates PASS → Merge approved.**
**ANY S0/S1 → REJECT.**
**S2 only → Merge with follow-up ticket.**

---

## APPENDIX: Known Inconsistencies Requiring Resolution (as of 2026-02-28)

These items MUST be checked against any PR that touches related content:

| ID | Issue | Files Affected | Required Action |
|----|-------|---------------|-----------------|
| KI-01 | w_a = -1.183 vs -1.300 | theoretical_notes.md, DESI_DR2_alignment_report.md | Define canonical L |
| KI-02 | N=99 vs N=94.05 | limitations.md, covariant_unification.py, theoretical_notes.md | Reconcile or version |
| KI-03 | w₀ = −0.99 [C] | **RESOLVED** per Decision D-002 | Canonical w₀ = −0.99 |
| KI-04 | γ tagged [C] in quark_mass doc | quark_mass_hierarchy_prediction.md | Enforce [A-] |
| KI-05 | [A+] category used | quark_mass_hierarchy_prediction.md | Remove (non-existent) |
| KI-06 | Duplicate §9 numbering | theoretical_notes.md | Renumber |
| KI-07 | Broken LaTeX delimiters (1814) | DESI_DR2_alignment_report.md | Fix to $$ |

---

**Protocol Version:** 1.0
**Author:** Philipp Rietz / Claude Opus 4.6
**Effective Date:** 2026-02-28
**Review Cycle:** After every 20 PRs or major framework version change
