# Review brief 04 — the repaired amplitude argument

*Written 9 October 2026 for an independent reviewer. A fresh reviewer is preferred; if you also wrote REVIEW-03, say so. Judge the documents as they stand.*

## Context in one paragraph

This repository develops an interpretation of quantum mechanics (the "resolution-front framework", RFF). [SIM-SPEC-02](SIM-SPEC-02-amplitudes.md) proposed deriving the clock-hand rule (each link of a history turns its hand by a fixed angle; hands add; the result is squared) from five assumptions via Herglotz's theorem. An independent review ([REVIEW-03](REVIEW-03-amplitudes.md)) found that one assumption, A3 (strong positivity), had been justified by composing with **quantum** systems. That borrows quantum theory to explain quantum structure, so the derivation failed its own first kill condition. The review also found that A2, A5 and the Herglotz step were sound. **[SIM-SPEC-02 §9](SIM-SPEC-02-amplitudes.md) replaces only the justification of A3**, using Dowker & Wilkes's Theorem 4 together with the observed existence of dark fringes. The project's lead adopted the repair. Your job is to judge it.

## What to read

1. **[SIM-SPEC-02 §9](SIM-SPEC-02-amplitudes.md)** — the repair. Short; this is the main object of review.
2. SIM-SPEC-02 §4 — the original assumptions A1–A5 and the Herglotz step, which §9 builds on.
3. [REVIEW-03](REVIEW-03-amplitudes.md) — the review that found the problem.
4. **Dowker & Wilkes, "An argument for strong positivity of the decoherence functional", arXiv:2011.06120** — Definitions 1 and 4, Theorems 3 and 4.

The test results ([RESULTS-03](RESULTS-03-amplitudes.md)) are background only. No new tests were run, and none are claimed.

## The repair in four lines

- **A3′:** the set of physical systems is tensor-closed. Any two independent systems form a joint system whose probabilities are non-negative.
- **E1:** some physical system shows destructive interference, P(A ∪ B) < P(A) + P(B), so Re D(A, B) < 0 for some pair of events: it is not a positive-entry system.
- **Dowker–Wilkes Theorem 4:** a tensor-closed set of systems lies wholly in the strongly positive set S or wholly in the positive-entry set R⁺.
- **Hence** every physical system is strongly positive, and §4's Herglotz argument goes through (Carathéodory–Toeplitz if only a finite range of readings occurs).

## Questions, in order of importance

### 1. Is Theorem 4 stated and applied correctly? *(decides everything else)*

- Is §9's statement of Theorem 4 faithful, hypotheses included? Note how the paper defines a system (Hermitian, additive, normalised, weakly positive) and "tensor-closed".
- Does "the set of physical systems" in A3′ meet those definitions? In particular: does the free-particle clock-comparison system of §4, with D(h, h′) = f(n_h − n_{h′}), count as a system in their sense (normalisation, event algebra, possibly infinite history spaces)?
- Is it legitimate to put the system that shows the dark fringe and the free-particle system in the same tensor-closed set?

**Verdict wanted:** *applied correctly* / *misapplied (say where)* / *cannot tell (say what would settle it)*.

### 2. Does E1 sneak quantum theory back in?

E1 says only that a dark fringe is observed somewhere: one negative interference term. REVIEW-03's objection was that the old justification needed a full quantum system (amplitudes, a Gram matrix) to exist.

- Is a single observed negative interference term genuinely weaker than "a quantum system exists", or equivalent to it in disguise?
- The original target (spec §1(b)) was to explain why histories combine like clock hands, which can cancel, rather than like chances. With E1, the **existence** of cancellation becomes an input and only its **form** is derived. Is that still a non-circular result, or has the target simply been assumed? Spec §6's first kill condition reads: "every candidate needs the phase rule added by hand". Does E1 count as adding the phase rule by hand?

**Verdict wanted:** *E1 is observation-only and not circular* / *circular (say why)* / *cannot tell*.

### 3. Is A3′ itself a borrowing?

Is "all physical systems can be combined, with non-negative joint probabilities" a reasonable physical requirement in its own right? Or does it carry hidden quantum structure, for example through the specific tensor-product rule D₁₂ = D₁ ⊗ D₂ for independent systems?

### 4. Do steps 3–4 of §9 hold?

- Does strong positivity on atomic events (single histories) give positive semidefiniteness of every matrix f(nᵢ − nⱼ)?
- Is the Carathéodory–Toeplitz step right: a finite positive semidefinite Toeplitz matrix is the moment sequence of a positive measure on the circle?

### 5. Is the claim sized honestly?

§9 claims: *if something somewhere cancels, and all systems can be combined, then every system compared by clock-reading differences uses clock hands with the Born square.* It explicitly does not claim to explain why anything cancels.

- Does that match what the argument delivers?
- Are the named inputs (A1, A2, A3′, A5, E1) complete, or is something else being used silently?
- Are the limits carried over from REVIEW-03 (equal weights only; real versus complex kernels) still stated correctly?

### 6. Is it already published?

Dowker & Wilkes do not draw this conclusion themselves, and do not connect strong positivity to phases via Herglotz or Bochner (checked against their text). Has anyone combined a "tensor-closed implies S or R⁺" result with observed interference to force strong positivity, and then derived the e^{iθn} form? If so, give the reference; the project would adopt it.

## What a useful review looks like

- **Lead with verdicts on questions 1 and 2.** If either fails, the repair fails.
- Then 3–6, each with *agree* / *disagree* / *cannot tell* and a sentence or two of reasons.
- Point to specific places: §9 step numbers, theorem or definition numbers in Dowker & Wilkes.
- Plain language is welcome; the project's lead prefers it.
