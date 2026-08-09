# Sim Spec 01 — Does coherence behave as thickness?

*The first computational task. Purpose: verify or kill the variable assignment made 25 Jul before anything else is built on it. Failure here is a good outcome — it's cheap and it's early.*

> **STATUS: executed in full, 6 August 2026.** Code in [sim/](sim/), results in [RESULTS-01.md](RESULTS-01.md).
>
> | Test | Outcome |
> |---|---|
> | 1 | **PASS** — endpoints, monotonicity, inversion; measures agree along any resolution history, disagree across unrelated states above d=2 |
> | 2 | **PASS**, more strongly than asked — the which-path basis is the *maximising* basis, so thinness is not basis-tuned |
> | 2 (Watch) | **PASS exactly** — non-distinguishing coupling produces literally zero thinning; #9 survives its internal check |
> | 3 | **FAIL** — coherence lifetime does not track L. Exponent 0.00 where 1.00 was required |
> | 4 | **PASS** to machine precision; found one error in the SOURCES §6 wording |
>
> The spec below is left as written so the pass/fail conditions can be checked against what was actually run. Nothing here should be re-run to get a different answer.

**Stack:** Python + QuTiP. Small Hilbert spaces throughout; nothing here needs to be big.

**What this spec is for.** It tests posit **#4** (thickness = coherence) in [FRAMEWORK.md §11](FRAMEWORK.md), checks **#9** (Test 2), carries the framework's only distinguishing prediction (Test 3, the L-sweep), and keeps a code-correctness check (Test 4).

**Where it sits in the order of attack** ([FRAMEWORK.md §14](FRAMEWORK.md)): the **Test 3 design section below is step 1** and blocks all code. **Tests 1–2 are step 2.** **Test 3 itself is step 4.** The dimensionality decision (step 3) should be settled before Tests 1–2 are run, since it determines what they are simulating.

The definitions computed here come from the coherence papers in [SOURCES.md](SOURCES.md), **all read 5 August 2026** — implement the measures from the papers in `papers/`, not from these summaries.

---

## Test 1 — Endpoint behaviour

**Claim:** coherence is high for a live superposition, zero for a resolved outcome.

Two-level system in the which-path basis. Compute both relative entropy of coherence and l₁-norm for:

| State | Expected |
|---|---|
| (\|0⟩ + \|1⟩)/√2, isolated | maximum |
| after full dephasing | 0 |
| partially dephased, swept | monotone between |

**Pass:** monotone decrease, correct endpoints, both measures agreeing on ordering.
**Fail:** non-monotonicity, or the two measures disagreeing on ordering — the latter would mean the choice of measure carries physical content, which is a problem for the ontology.

**Compare orderings, not values.** The two measures have different maxima in general (l₁-norm → d−1, relative entropy → log d). They coincide at 1 for a qubit, which will make them look interchangeable in this test and stop being true the moment Test 2 goes to larger d. Normalise before plotting them on one axis, and never read the agreement of *magnitudes* as evidence. *(Confirmed against Baumgratz–Cramer–Plenio, 5 Aug.)*

**Do not use the sum of squared off-diagonals.** It is the measure most people reach for first, and it is **not a valid coherence monotone** — Baumgratz–Cramer–Plenio give an explicit counterexample where it *increases* under an incoherent operation. Only the l₁-norm and the relative entropy are established here. A third valid option, if a fidelity-based measure is ever wanted, is the geometric measure of coherence: for a qubit, C_g = ½(1 − √(1 − 4|ρ₀₁|²)).

Also compute entanglement entropy of the reduced state across the same sweep, to confirm it runs the *other* way. That's the inversion argument, made numerically.

---

## Test 2 — Does a chair come out thin?

**Claim:** macroscopic objects have negligible coherence without hand-waving about basis choice.

Spin-boson or central-spin model. System coupled to N environment modes; sweep N upward and track coherence decay.

**What to extract:** the scaling of residual coherence with N, and how fast it collapses.

**Pass:** coherence falls off steeply enough that a macroscopic N gives an effectively zero value, *without* tuning the basis to make it happen.
**Fail:** thinness requires a hand-picked basis. That would mean the classical world's thinness is an artefact of bookkeeping, not a fact — and #3's interpolation claim is decoration.

**Watch:** whether the answer depends on the coupling being which-path-distinguishing. It should. If a non-distinguishing coupling also thins the system, #9 is in trouble — and #9 is the framework's only *internal* falsification condition, the one that can fail before any experiment gets to it. (The external one is Test 3.)

---

## Test 3 — The L-sweep *(design incomplete — nothing runs until this section is finished)*

**This is the framework's only distinguishing prediction** ([FRAMEWORK.md §7](FRAMEWORK.md), Reading B). Everything else is prior art or explanation. **Designing this test is step 1 of the order of attack; running it is step 4.** Write the design before any code at all, including Test 1's.

**Claim:** at fixed local coupling and temperature, coherence lifetime tracks the distance L to the absorber, ~L/c.

**The knob:** absorber distance L. **Held fixed:** coupling strength, temperature, system dimension, everything else.

---

### What this test replaced, and why *(6 Aug — do not restore)*

The original Test 3 compared the coherence decay timescale τ_C against the standard decoherence timescale τ_D in a spin-boson model, and counted **τ_C = τ_D as a pass that unifies #4 and #14**. Both halves were wrong:

1. **The model contains no L.** A spin-boson or central-spin model has no absorber at a distance, so the L/c claim cannot appear in the result either way. Whatever came back said nothing about #14.
2. **The pass condition was inverted.** τ_D is set by coupling and temperature — local physics. #14's window is set by a distance. τ_C = τ_D *in a model with no L* is evidence that coherence is governed by local coupling rather than by distance to an absorber: **a point against #14.**
3. **The unification it was chasing is already done.** Under Reading B, thickness *is* open-transaction depth ([FRAMEWORK.md §7](FRAMEWORK.md)) — #4 and #14 are one quantity structurally. No numerical result is needed for the merge, and none is available for it.

The old pass/partial/fail block is deleted rather than archived, because its structure does not survive: it graded a comparison this test no longer makes.

---

### Design requirements — all six must be written down before code

**1. Model class.** "Absorber at distance L" has to be an actual object. A structureless bath will not do it. The candidate class is **time-delayed coherent feedback / waveguide QED**: a two-level system coupled to a 1D continuum with a mirror or second emitter at distance L, giving a delay-differential master equation with memory time 2L/c. This is standard, implementable, and non-Markovian by construction. Fix the class, and record what was rejected.

**2. How L enters.** L must enter through **propagation** — the delay in the feedback term — and must not appear in any rate, coupling constant, or decay parameter. **If the implementation encodes "transaction complete iff signal returns from L," the result is L/c by construction and the test is worthless.** This is the single largest risk in the spec. Write down, explicitly, the line of the model where L appears and why that placement is not question-begging.

**3. The null, and it is not trivially L-independent.** ⚠️ **The obvious null is wrong.** "Standard decoherence has no L-dependence" holds for a Markovian bath — it is false of open-system physics generally. An emitter in front of a mirror has an L-dependent decay rate (Purcell/interference); delayed feedback is non-Markovian with memory time 2L/c. **A standard model can produce L/c scaling with no #14 in it.** So the null must be a specific, implemented, conventional dynamics run through the same pipeline — not an assertion of flatness. Two nulls are wanted:

   - **Null A (flat):** Markovian amplitude damping / spin-boson at matched coupling. Expect no L-dependence. Confirms the pipeline can see flatness.
   - **Null B (hard):** the *same* delayed-feedback model interpreted conventionally, with no transactional structure added. **If Null B already reproduces the predicted scaling, the L-sweep does not distinguish #14 from standard physics and the paper has no empirical section.** Establish this before running anything else in Test 3 — it is cheaper to find here than in review.

   The framework only has content if there is a measurable difference between #14's prediction and Null B. **State in advance what that difference is.** If none can be stated, say so in the write-up and drop the claim to an interpretive one.

**4. Observable.** Define "coherence lifetime" precisely: which measure (l₁-norm or relative entropy, per Test 1), what fit form (single exponential? stretched? the delayed-feedback case is generically non-exponential), what threshold defines the lifetime, and over what ensemble. Fix this before seeing data.

**5. Parameter ranges and units.** L in units of the emitter wavelength and of the Markovian decay length; enough decades of L to distinguish a linear scaling from a weak one; coupling held at a value where Null A's lifetime is well inside the measurable window. State the figure of merit: fitted exponent of lifetime vs L, with a confidence interval.

**6. Pass / fail, stated before the run.**

   - **Supports #14:** lifetime scales monotonically with L (exponent consistent with 1), Null A flat, and **a stated, observed difference from Null B**.
   - **Against #14:** lifetime L-independent at fixed coupling. Reading B then has no content left and the range limit is all that remains — revisit **Reading A** ([FRAMEWORK.md §7](FRAMEWORK.md)).
   - **Evidence for Reading A specifically:** a **cutoff** — scaling that stops beyond some L. Under Reading B there is no range beyond which transactions fail, so a clean scaling is expected and a break point is not.
   - **Null result for the programme (the quiet failure mode):** scaling present but indistinguishable from Null B. Record this outcome explicitly; it is the most likely one and the easiest to not notice.

---

## Test 4 — Does the conversion saturate? *(demoted 5 Aug — the question is answered on paper)*

> **Read this before running it.** The Tier-2 papers settle both bounds analytically ([SOURCES.md](SOURCES.md) §2–3):
>
> - **Englert:** V² + K² = 2 Tr(ρ²) − 1 exactly. The gap *is* the which-way marker's impurity. Measured to the percent level in 1999.
> - **Streltsov:** the bound is attainable via an explicit generalised CNOT. A gap in any real evolution measures how far the coupling is from optimal, not a shortfall in the theory.
>
> **So this is no longer a discovery test.** Keep it as a **code-correctness check** — if your implementation doesn't reproduce 2 Tr(ρ²) − 1, the bug is yours, and better to find it here than in Test 3. Drop the "characterise the gap" framing entirely; there is nothing to characterise.
>
> Run it last, cheaply, and don't spend a week on it.

**Claim (fork, not prediction):** coherence lost = entanglement gained, or is there a gap?

Track coherence lost by the system and entanglement generated with the environment through the same evolution. Compute both sides of the Streltsov bound and of V² + D² ≤ 1.

**Design warning — this test will return a false "always saturates" if run naively.** Englert's relation saturates for pure states, and a unitary evolution of system + environment from a pure initial state stays globally pure. Run it that way and saturation is a property of the setup, not a result. The test only has content on **mixed** states: mixed initial system state, thermal or finite-temperature environment, or an environment sector that is traced out and stays inaccessible. Decide which of those three before writing code — they are different physical claims about what the front does and does not have access to, and the third is the one that actually corresponds to the framework's picture.

Same caution on the Streltsov side: the bound saturates only under a specific class of operations. **A gap found outside that class is not a discovery** — it's the theorem's own precondition being violated. Get the class from the paper first ([SOURCES.md](SOURCES.md)).

**Expected result: it saturates**, and that is now the known answer rather than a finding. If your numbers disagree with 2 Tr(ρ²) − 1 on the Englert side, or exceed the Streltsov bound, you have a bug — that is the entire value of running this.

---

## Order and stopping rule

**Design Test 3 → run 1 → 2 → 3 → 4.** The Test 3 design section is written first and blocks all code, including Test 1's. The **dimensionality decision** ([FRAMEWORK.md §3](FRAMEWORK.md), §14 step 3) is settled before Test 1 runs — it determines what Tests 1–2 are simulating.

Stop and re-think if Test 1 or Test 2 fails: those are the variable assignment itself, and there's no point running 3 and 4 on a dead variable. Stop and re-think if **Null B** in Test 3 reproduces the predicted scaling: the prediction is then not distinguishing, and that is a result about the framework, not about the code.

**Where results go.** Each test writes back to exactly one place, so the documents don't drift:

| Test | Updates |
|---|---|
| 1, 2 | **#4's verdict** in [FRAMEWORK.md §11](FRAMEWORK.md) — currently KEEP-provisional, and this is what makes it final or kills it |
| 2 (the "Watch" clause) | **#9** in [FRAMEWORK.md §8](FRAMEWORK.md) |
| 3 | **#14 and the Reading A/B fork** in [FRAMEWORK.md §7](FRAMEWORK.md), and **§3 "still owed", item 2**. Note it does **not** merge #4 and #14 — Reading B already did that structurally. This test asks only whether coherence lifetime tracks L, and whether that is distinguishable from a conventional delayed-feedback model |
| 4 | **§4** in [FRAMEWORK.md](FRAMEWORK.md) — code-correctness only, nothing to discover |

Record the outcome even when it's boring. A test that ran and found nothing is a different state from a test that hasn't run, and only one of them is progress.

**Do not extend to:** field-theoretic area-law verification, cosmological anything, gravitational decoherence models. Out of scope per the charter — and Test 2's environment sweep will make the first of those look tempting.
