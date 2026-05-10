# Invitation for Adversarial Review

**Maintainer: P. Rietz**  
**Last reviewed: 2026-05-10**

---

## To Critical Physicists and Mathematicians

UIDT v3.9 is an active, single-author research framework.  It claims a constructive candidate
proof of the SU(3) Yang–Mills mass gap and a set of cosmological and photonic predictions.
**These claims need adversarial scrutiny, not only supportive review.**

We explicitly invite critics to:

1. **Attack the mass-gap proof architecture.**  
   Find a logical gap in the Banach fixed-point construction, the OS-axiom verification,
   or the homotopy argument.  The Falsification Matrix in `FALSIFICATION_MATRIX.md` lists
   the known kill-switches; we are equally interested in kill-switches we have not yet
   identified.

2. **Reproduce the core numerics independently.**  
   Use the `INDEPENDENT_REPRODUCTION_PROTOCOL.md`.  We expect discrepancies to be
   reported as Issues, not suppressed.

3. **Challenge the Evidence categorisation.**  
   If you believe a claim rated Evidence A should be Evidence D, open an Issue with the
   label `evidence-dispute` and provide your reasoning.

4. **Identify missing phenomena.**  
   If UIDT should explain X and does not, open an Issue with label `scope-gap`.

---

## What We Do Not Want

- Rubber-stamp reviews that find no problems.
- Reviews that only check internal consistency (which LLMs already do).
- Engagement that avoids stating a clear verdict.

---

## Contact

Open a GitHub Issue in this repository, or contact P. Rietz directly via the email listed
in CITATION.cff.

---

## Red-Team PR Procedure

A contributor who finds a genuine error or gap should:

1. Open an Issue with label `red-team` describing the problem.
2. If a patch is proposed, open a PR with title `[RED-TEAM] <description>`.
3. The PR body must include: the specific claim attacked, the evidence for the attack,
   and the proposed resolution or downgrade of Evidence category.

All red-team Issues and PRs are treated with the highest priority.
