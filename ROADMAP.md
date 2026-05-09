# UIDT Framework v3.9 — Research Roadmap

**Maintainer:** P. Rietz  
**Status:** Active Research  
**Last updated:** 2026-05-09  
**Evidence categories:** A · A- · B · C · D · E  
**Epistemic strata:** Stratum I (empirical) · Stratum II (consensus) · Stratum III (UIDT model)

> This roadmap integrates a structured critical review of the UIDT Framework.  
> Each open flank is documented with its current status, the corresponding epistemic  
> stratum, the assigned evidence category, and a concrete work programme.  
> Language rules apply: no forbidden words (`ultimate`, `solved`, `resolved`, etc.).  
> All open items are tracked as GitHub Issues; issue links are added upon creation.

---

## Open Flank 1 — Calibration vs. First Principles (γ)

**Status:** ACTIVE — in progress (Pull Request open)  
**Evidence category:** A- (phenomenological parameter)  
**Epistemic stratum:** Stratum III (UIDT model)

### Problem statement

The central kinetic vacuum parameter γ = 16.339 [A-] is currently obtained via
calibration against cosmological observational data (DESI DR2, JWST).
A framework that derives a fundamental parameter by fitting the data it intends to
explain risks circular reasoning. The observed agreement at the Yang–Mills spectral
gap may be a reparametrisation of known physics rather than an independent prediction.

Furthermore, the specific numerical value of γ lacks a derivation from logical or
topological necessity. Until such a derivation exists, UIDT contains one fewer free
parameter than the Standard Model, which is a quantitative improvement but not a
qualitative step to a fully first-principles theory.

### Work programme

- [ ] **RG-1** Derive γ from the RG fixed-point constraint `5κ² = 3λS` without
      reference to cosmological observables. Document the algebraic chain. [Evidence A]
- [ ] **RG-2** If exact derivation is not yet achievable, establish an explicit
      inequality bounding γ from topological data (e.g. instanton number, Pontryagin
      class). [Evidence B]
- [ ] **RG-3** Add a dedicated section to the manuscript that makes the calibration
      status of γ explicit, distinguishes prediction from parametric fit, and lists
      the observables that constrain γ at Stratum I. [Evidence A-]
- [ ] **RG-4** Open a separate GitHub Issue: `[TENSION ALERT] γ derivation status`.

**Affected constants:** γ = 16.339 [A-], γ∞ = 16.3437 [A-], δγ = 0.0047

---

## Open Flank 2 — Operational Definition of S(x)

**Status:** ACTIVE — in progress (Pull Request open)  
**Evidence category:** D (prediction) → target A (mathematically proven)  
**Epistemic stratum:** Stratum III (UIDT model) → must bridge to Stratum I

### Problem statement

The information density field S(x) is the central object of UIDT. Its physical
status is currently unclear: there is no measurement prescription that would allow
an experimenter to determine S(x) at a spacetime point x from an independent
observable. A physical field requires an operational definition.

Equally important is the connection to the Bekenstein–Hawking entropy relation.
If S(x) is a volume density, the holographic area-proportionality of black-hole
entropy must emerge as a limiting case. Without this correspondence, S(x) stands
in tension with one of the best-tested results in quantum gravity research.

### Work programme

- [ ] **OP-1** Formulate an operational definition: identify the observable quantity
      (lattice correlator, vacuum condensate, energy-momentum trace anomaly, or other)
      that S(x) maps onto. Assign a Stratum I measurement protocol. [Evidence A]
- [ ] **OP-2** Derive or demonstrate compatibility with the Bekenstein–Hawking
      relation `S_BH = A / (4 G ℏ)` in the appropriate limit. Document the
      dimensional reduction step from volume to area. [Evidence A / B]
- [ ] **OP-3** If full derivation is not yet achievable, classify the
      Bekenstein–Hawking correspondence as an open conjecture at Evidence D and
      track it explicitly. Note: "compatible with" must not imply "equivalent to"
      without proof.
- [ ] **OP-4** Cross-check against the holographic Factor 2.3 suppression already
      documented in `Factor_2_3_Derivation.md`.

---

## Open Flank 3 — Classical Limit: General Relativity and Time Emergence

**Status:** OPEN — not yet formally demonstrated  
**Evidence category:** D (prediction)  
**Epistemic stratum:** Stratum III (UIDT model)

### Problem statement

Every candidate theory of quantum gravity must reproduce General Relativity (GR)
as its effective low-energy, low-curvature limit. In UIDT, spacetime geometry
emerges from information density — a top-down construction. However, a formal
demonstration that the Einstein field equations

    G_μν = (8π G / c⁴) T_μν

emerge exactly in the weak-field, low-information-density regime has not yet been
provided in a standalone derivation.

A related open item is the emergence of coordinate time: the claim that time is
"rendered" from logical causality must be elevated from a conceptual picture to a
mathematical statement. Loop Quantum Gravity (LQG) provides a candidate framework
(Wheeler–DeWitt equation, spin-network boundary conditions) with which UIDT's
time-emergence mechanism could be compared.

### Work programme

- [ ] **GR-1** Provide a formal derivation of the GR limit. Specify the expansion
      parameter (e.g. `S(x) → S_background + δS` for small δS) and show that
      linearised UIDT reproduces the linearised Einstein equations. [Evidence A]
- [ ] **GR-2** Map the UIDT logical-causality structure onto the LQG spin-network
      formalism. Identify whether UIDT's information-density nodes correspond to
      spin-network vertices. Structural isomorphism → [Evidence B]; schematic
      correspondence only → [Evidence E].
- [ ] **GR-3** Wheeler–DeWitt equation: show that the UIDT wave-functional Ψ[S]
      satisfies Ĥ Ψ = 0 in the appropriate sector. [Evidence D → target A]
- [ ] **GR-4** Document the GR-limit section in the manuscript with explicit
      evidence category stated in the heading.

---

## Open Flank 4 — Yang–Mills Mass Gap: Physical Model vs. Mathematical Proof

**Status:** PARTIAL — numerical calculation complete; Clay-level proof separate  
**Evidence category:** B (lattice compatible) for physical model;
                      D (prediction) for mathematical proof claim  
**Epistemic stratum:** Stratum II (Clay problem definition) vs. Stratum III (UIDT approach)

### Problem statement

The UIDT framework produces a numerically precise result for the Yang–Mills
spectral gap Δ* = 1.710 ± 0.015 GeV [A], derived from the calibrated parameter
γ [A-] via the Banach fixed-point structure. This constitutes a physical model of
the mass gap.

The Clay Mathematics Institute requires a complete mathematical proof that for every
compact, simple gauge group a strictly positive mass gap exists — independent of
any particular parameter choice. The UIDT numerical result, though consistent with
lattice QCD data, is not a proof in this sense. This distinction is critical and
must be stated unambiguously in all public-facing documents.

The approximation structure (Banach iteration, torsion lattice corrections,
ET = 2.44 MeV [C]) carries convergence obligations: it must be demonstrated that
the series is controlled and that deviations from exact results are bounded.

### Work programme

- [ ] **YM-1** Add an explicit disclaimer paragraph to the manuscript and to all
      files under `clay-submission/` that distinguishes the physical model
      calculation from the mathematical existence proof. [Documentation — mandatory]
- [ ] **YM-2** Provide a convergence certificate: for each approximation step in
      the Banach iteration, bound the truncation error. Express bounds in mpmath
      mpf arithmetic at `mp.dps = 80` (local scope). [Evidence A]
- [ ] **YM-3** Identify the minimal mathematical conditions under which the UIDT
      fixed-point argument constitutes a rigorous existence proof. Consult the
      literature on Banach-space Yang–Mills (e.g. Uhlenbeck compactness theorem)
      to determine the gap between current UIDT formalism and the Clay
      requirement. [Evidence D]
- [ ] **YM-4** The Clay submission must be framed as a "physically motivated
      conjecture with numerical support" — never as a completed proof.
      Forbidden words: `solved`, `definitive`, `resolved`.

**Affected constants:** Δ* = 1.710 ± 0.015 GeV [A], ET = 2.44 MeV [C]

---

## Open Flank 5 — External Critique and Independent Verification

**Status:** PARTIALLY ADDRESSED — UIDT-Research founded; submissions received;
            GitHub collaboration open  
**Evidence category:** n/a (process criterion)  
**Epistemic stratum:** meta-scientific (scientific method)

### Problem statement

A single-author research programme carries the structural risk of hidden assumptions
that become visible only through adversarial external review. A mathematically
self-consistent framework can be internally precise yet fail to correspond to
physical reality — historical precedents for this class of failure are well documented.

The scientific method's core error-correction mechanism is collective, independent
peer scrutiny. Bypassing formal peer review removes the principal safeguard against
unconscious systematic bias.

### Current state

- UIDT-Research organisation founded; external submissions received.
- GitHub repository is public; collaboration openly invited via `CONTRIBUTING.md`.
- Falsification criteria documented in `falsification-criteria.md`
  (experimental thresholds: lattice QCD, LHC, DESI, Casimir, KATRIN).
- Evidence classification system (`evidence-classification.md`) provides
  a transparent epistemic ledger accessible to external reviewers.

### Work programme

- [ ] **EXT-1** Identify 3–5 external theoretical physicists (QFT / lattice QCD / GR)
      and issue direct review invitations via GitHub Discussions or email.
      Target expertise: Yang–Mills theory (Open Flank 4), holography (Open Flank 2),
      cosmological perturbation theory (Open Flank 1). [Process]
- [ ] **EXT-2** Submit a preprint to arXiv (hep-th or gr-qc) to expose the work
      to the community's standard scrutiny mechanism. [Process]
- [ ] **EXT-3** For each Open Flank above, create a corresponding GitHub Issue
      labelled `open-critique` and `help-wanted` to invite focused external
      contributions. [Process]
- [ ] **EXT-4** Document all received external criticism in `CRITIQUE_LOG.md`,
      recording: date, reviewer (anonymous if preferred), critique content,
      UIDT response, and evidence-category update if applicable. [Documentation]

---

## Roadmap Status Overview

| # | Open Flank | Current Status | Evidence Cat. | Priority |
|---|---|---|---|---|
| 1 | γ derivation from first principles | Active / PR open | A- | High |
| 2 | Operational definition of S(x) | Active / PR open | D → A | High |
| 3 | GR limit and time emergence | Open | D | High |
| 4 | Mass gap: physical model vs. Clay proof | Partial | B / D | Medium |
| 5 | External critique and peer review | Partial | n/a | High |

---

## Compliance Notes

- All numerical claims must use `mpmath` at `mp.dps = 80` (local scope only —
  never centralised in `config.py` or global variables).
- Constants listed above must not be modified without explicit ledger audit.
- PRs addressing this roadmap must follow the format:
  `[UIDT-v3.9] <Component>: <Description>`  
  and list all affected constants with their evidence category in the PR body.
- Cosmological tensions (H₀, S₈) must not be declared resolved in any PR
  that references this roadmap.
- Forbidden words in all associated documents:
  `ultimate`, `definitive`, `solved`, `holy grail`, `resolved`.
