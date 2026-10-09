# Review brief — amplitudes from ordering (SIM-SPEC-02 / RESULTS-03)

*Written 9 October 2026 for an independent reviewer. You have not seen the work being done; that is the point. Judge the documents and the code as they stand.*

## Context in one paragraph

This repository develops an interpretation of quantum mechanics (the "resolution-front framework", RFF). One of its open problems is why alternative histories combine like clock hands, which add and can cancel, rather than like chances, which only add. [SIM-SPEC-02](SIM-SPEC-02-amplitudes.md) proposes an answer. From five assumptions (A1–A5, spec §4), Herglotz's theorem is claimed to force the rule "each link of a history turns its hand by a fixed angle; hands add; the result is squared". Three numerical tests were then run ([RESULTS-03](RESULTS-03-amplitudes.md); code in [sim/amplitudes/](sim/amplitudes/)). All three passed against conditions written before any code ran. The author's own assessment is that the tests check the argument's ingredients, not the argument itself. Your job is the part the tests cannot do.

## What to read

1. [SIM-SPEC-02-amplitudes.md](SIM-SPEC-02-amplitudes.md) — especially §4 (assumptions, derivation, self-review for circularity) and §6 (kill conditions).
2. [RESULTS-03-amplitudes.md](RESULTS-03-amplitudes.md) — results and the "what this establishes" section.
3. [sim/amplitudes/](sim/amplitudes/) — code and committed output. See its README for what each file does.

You do not need the rest of the repository. The framework's wider claims are out of scope.

## Questions, in order of importance

### 1. Is there a phase rule hidden in A1–A5? *(decides everything else)*

The spec's first kill condition: if any assumption already contains the clock-hand rule, the derivation is circular and fails. Please judge each assumption separately.

- **A3, positivity under composition.** The cited justification is Boes & Navascués (PRA 95, 022114, 2017): strongly positive decoherence functionals are the largest set closed under composition *that contains the quantum ones*. If the argument needs quantum systems to exist elsewhere in the world, the derivation borrows quantum theory to explain quantum theory. Dowker & Wilkes (arXiv:2011.06120) claim strong positivity is the *unique* maximal set closed under tensor product, which may remove that dependence. **What exactly did each prove, and can A3 be justified without presupposing quantum systems?** A hint from the tests: in Test 2, composing a bad rule with a copy of itself exposed it only once in 22 cases, while composing with a qubit exposed it every time. This is the sharpest question.
- **A2, comparison by difference of clock readings.** Herglotz applies because the integers under addition form a group whose characters are e^{inθ}. Is "D depends only on n − n′" already equivalent to assuming each history carries a phase e^{iθn}, or is it genuinely weaker? Note that a constant f (no cancellation at all) also satisfies A2.
- **A5, one sharp rate.** This turns a mixture of rotations into a single rotation. Is it an independent physical statement, or the conclusion restated?
- **Hidden extras.** A2 gives every history equal weight, so histories differ only in their clock readings. Quantum mechanics has path-dependent magnitudes as well as phases. Does the restriction to equal weights matter for the claim?

**Verdict wanted:** for each of A2, A3, A5 — *no hidden phase rule* / *hidden phase rule (say where)* / *cannot tell (say what would settle it)*.

### 2. Is the mathematics right?

- Does Herglotz's theorem apply as used in spec §4? Positive semidefiniteness of every matrix f(nᵢ − nⱼ) ⇔ f is the Fourier transform of a positive measure on the circle.
- Is the step from A1 (pairs) + Herglotz to P(A) = ∫ dμ(θ) |Σ_{h∈A} e^{iθn(h)}|² correct?
- Is the claim right that a real kernel (symmetric μ, giving cosines) and a complex one (single angle) give identical one-particle probabilities, differing only in multi-party settings?

### 3. Is it already published?

The author found no published derivation of this form, but the search was short. Please check the decoherence-functional and quantum-measure literature (Sorkin; Dowker, Johnston & Sorkin; Gudder; Anastopoulos; Hartle) and the Goyal–Knuth–Skilling line for a derivation of the e^{iS} weighting from positive-definiteness plus dependence on action differences, via Bochner or Herglotz. If it exists, give the reference. That is not a failure: the project adopts the published version.

### 4. Is Test 1 a fair test?

Test 1 counts links along the longest chain through each slit on random discrete spacetime, uses the count as the clock reading, and compares the resulting double-slit pattern with the exact continuum one.

- The clock is calibrated on **straight** histories and used on **bent** ones (through a slit). Is that a fair separation, or could the calibration still absorb something it shouldn't?
- Is the continuum reference (maximum proper time through each slit) the right comparison?
- Only the longest chain per slit is used, not a sum over all chains. Does that limit what can be claimed? (The author says the scope is "two stationary histories, 1+1 dimensions".)
- A residual fringe-spacing bias (2% at ρ = 10⁷, 1% at 3 × 10⁷) is attributed, without a check, to finite-size corrections in chain length. Plausible?

### 5. Does the write-up claim more than the evidence supports?

- Check each line under "Established, by test" in RESULTS-03 against the committed output in `sim/amplitudes/results/`.
- Two things changed after a first launch: Test 1 dropped its lowest density (a slit held no elements); Test 2's search was strengthened after it missed two rules, and its kernels were given their own random stream. Both are recorded in the scripts' docstrings and in RESULTS-03. Were they handled honestly, and could either have biased a verdict?
- Test 3 is described as a known identity that could not fail. Agree?

## What a useful review looks like

- **Lead with the verdict on question 1.** If a hidden phase rule is found, the rest matters much less.
- Then questions 2–5, each with *agree* / *disagree* / *cannot tell*, and one or two sentences of reasons.
- Point to specific lines (spec section, file and line number) where possible.
- Plain language is welcome; the author prefers it.

## Reproducing anything

```bash
cd sim/amplitudes
pip install numpy scipy numba matplotlib
python check_cs.py           # brute-force check of the chain code (~1 min)
python test2_positivity.py   # ~10 min
python test3_spread_rate.py  # seconds
python test1_link_clock.py   # ~8 min on 2 cores
```
