# Project Review: Q-Physics (Resolution-Front Framework)

**Version:** 3
**Date:** 9 August 2026
**Scope of review:** Full re-read of [FRAMEWORK.md](FRAMEWORK.md), [SOURCES.md](SOURCES.md), [SIM-SPEC-01-coherence.md](SIM-SPEC-01-coherence.md), [RESULTS-01.md](RESULTS-01.md), `sim/` (code, results, figures), and prior review v2.

This is a research-workspace review, not a software PR review.

---

## Why v3 exists

**Review v2 was written on 6 August, before the simulations ran that same day.** It is stale in a way worth stating plainly, because it recorded the opposite of what happened:

| v2 said | Actually |
|---|---|
| "Zero computational results (unchanged, still fatal)" | Four tests designed, run and recorded, with pinned deps and reproducible output |
| "L-sweep is named but not designed" | Designed to all six requirements, then run in three independent absorber implementations |
| "The project is closer to a paper outline and still at zero runs" | The runs happened and settled the central question |
| "Verdict: do not write more ontology prose. Design and run the L-sweep." | Done — and it failed |
| Bottleneck: design → run → write | Bottleneck is now: write |

v2's recommended-actions list is discharged or moot. Items 1–6 are done; item 9 ("do not re-open") still stands. **This file supersedes it.** v2 is not preserved — its findings are captured in the table above, and keeping a review that asserts zero results alongside a results file is exactly the drift the project is otherwise good at avoiding.

---

## Overall assessment

**The project did the hard thing: it built the falsifier it had been promising, ran it, and lost.**

That is the headline and it should be read as a success of method. The framework's single distinguishing prediction — coherence lifetime tracking absorber distance L — was specified with pass/fail conditions fixed in advance, implemented in a model class chosen so the answer could not be smuggled in, run against a stated null, and reported negative. Exponent 0.00 against a required 1.00, in three independent absorber implementations, wrong-signed in one, and causally excluded beyond L\* = v/γ on an argument that is general rather than model-specific.

**Equally important: the machinery around it passed.** Thickness = coherence is no longer provisional. The basis worry didn't need to be argued away — it was decided, and decided favourably (the which-path basis is the *maximising* basis). #9's internal check passed exactly rather than approximately. The two analytic bounds reproduce to machine precision, which is what licenses trusting the Test 3 pipeline at all.

**The project is now correctly sized.** It set out to derive front thickness from physical distance and produce a new prediction. It ends with one falsifiable disagreement against a named opponent plus a verified interpretation of standard open-system QM. Smaller, and real.

**Verdict:** The empirical phase is complete. The remaining work is writing, and the writing is now blocked on nothing. **Do not run more simulations looking for a better answer, and do not re-open either reading of the front.**

---

## Project inventory

| Piece | Role | Status |
|---|---|---|
| [FRAMEWORK.md](FRAMEWORK.md) | Canonical argument + 16 posits | Current as of 6 Aug; results written back into §3, §4, §7, §8, §11, §14 |
| [RESULTS-01.md](RESULTS-01.md) | What the sims returned | Complete, with reproduction command and a known numerical caveat recorded |
| [SIM-SPEC-01-coherence.md](SIM-SPEC-01-coherence.md) | The computational gate | Executed; spec deliberately left as written so pass/fail can be audited against it. Correct call |
| [SOURCES.md](SOURCES.md) | Paper Q&A ledger | 7/7 blocking read; τ entry reversed in place; §6 misattribution corrected after Test 4 |
| [Framework-Summary-Plain.md](Framework-Summary-Plain.md) | Lay summary | **Rewritten 9 Aug** — was badly stale (contained the July-cut gravity story and the failed #14 as live) |
| [sim/](sim/) | Code | 10 scripts, JSON results, 4 figures, pinned requirements, README with three real gotchas |
| [REVIEW.md](REVIEW.md) | This file | v3 |
| [papers/](papers/) | Local PDFs | 8 files, consistent naming |
| Git | — | **Still absent** |

---

## What the simulations actually settled

### Passed

**#4 — thickness = coherence.** Promote from KEEP-provisional to **KEEP**. Endpoints exact, monotone, three valid measures agreeing (Spearman 1.000 along a resolution trajectory). The inversion argument is now numerical, not rhetorical: coherence and entanglement entropy anticorrelate at −1.000, and coherence equals the environment-branch overlap to 4×10⁻¹⁶.

**The basis question — settled, not argued.** For a qubit the maximum l₁ coherence over all bases is the Bloch-vector length, a basis-independent quantity, and the which-path basis attains it to 1×10⁻¹⁶. This retires the "decoration" failure mode and, usefully, demotes Zurek from load-bearing defence to explanatory citation.

**#9's internal check — passed exactly.** At α = 0 coherence sits at 1.000000000000 at every N and every t. Thinning *is* environment distinguishability, arithmetically. #9 can now only be killed from outside.

**Code correctness.** Streltsov reproduced to 1.8×10⁻¹⁵, zero violations in 2400 samples; Englert zero violations in 20 000. This test was demoted from discovery to correctness check on 5 August and then earned its keep by finding a real error in SOURCES §6 — the duality identity holds against the *interfering system's* purity, not the marker's, and fails by up to 0.61 on mixed states. That is exactly the error a referee finds.

### Failed

**#14, and cleanly.** The detector configuration is flat to four decimal places across a 200× range in L, at every coupling and bandwidth tried. The mirror configuration does depend on L but as a period-2 standing-wave alternation — Purcell, wavelength-scale, known since 1946 — and on the node branch a closer absorber preserves *more* coherence. Maximum local slope anywhere is 0.64, at a crossover shoulder, flattening immediately.

**The causal-exclusion argument is the part that makes this final.** Coherence decays at local rate γ; news from the absorber cannot return faster than 2L/c; so beyond L\* = v/γ the distance cannot matter — in any theory with a finite signal speed. Measured L\* scales as γ^(−0.994) against a predicted −1. This is not a parameter choice and it will not be rescued by a different model.

**Neither reading of the front survives.** Reading B's own text said the L-sweep was all that remained testable. Reading A predicted a cutoff, and there is no scaling to cut off. RESULTS-01 draws the right conclusion — the A/B fork was never empirical — and FRAMEWORK §14 correctly marks it as not to be re-opened.

### The honest note buried in Test 3, and it deserves promotion

> "Null B and the signal were always going to be the same numbers: **the framework supplies no dynamics of its own.** There was only ever one model to run."

This is the sharpest self-criticism in the project and it is sitting in a bullet under a pass/fail table. It belongs in the paper's discussion section, stated once, in the author's own voice. A referee who notices it independently will make it fatal; an author who states it first makes it a limit on scope.

---

## Critical issues

### Blocking

**1. No paper draft exists.** Everything upstream is done. §14 step 5 is "write the paper around #9 versus Strubbe" and there is no file for it. This is now the only thing between the project and an output. Missing: abstract, figure plan, and a decision on where the negative result sits (recommendation: its own short section, not an appendix — it is a contribution and burying it looks evasive).

**2. #9 needs its external falsifier specified.** The framework's whole remaining empirical claim is "gravity cannot distinguish which-path, Strubbe says it can." The disagreement is stated qualitatively and the table in §8 is clear, but there is no worked account of **what experiment would decide it** — mass scale, coherence times, what an actual gravitational which-path measurement would consist of, and whether current or near-term Diósi–Penrose test apparatus could see it. Without that, "checkable in principle" is doing a lot of work. This is the one place where more technical effort is still warranted.

**3. Strubbe's model needs a closer read before the bet is placed publicly.** The whole paper rests on characterising his prediction correctly. SOURCES §1 is good, but the claim being contradicted — that only the momentum-carrying worldline gravitates, so which-slit information is gravitationally extractable without destroying interference — is being taken from a summary of one reading. Re-derive it from his equations before naming him in an abstract.

### Worth fixing

**4. Cramer (1986) is still unread and now matters more than it did.** The handshake is no longer load-bearing (it failed), but §10's claim that the selection problem has been open since 1986 is currently sourced to *Strubbe implying* Cramer doesn't answer it. If the paper asserts a 40-year-open problem, read the paper it's been open since.

**5. Finite-dimensionality — decided, but the decision needs to appear in the write-up.** §14 step 3 fixes it: discrete which-path DOF for paper v1, justified by Test 1b (measures agree perfectly along a history, disagree on 13% of unrelated pairs at d=8). The reasoning is sound and the restriction is honest. It just has to be stated in the paper rather than in the notes, and the phrase "the continuous quantum↔classical parameter" avoided.

**6. The area law (§6) still overreaches.** Unchanged from v2 and unaffected by the sims. Srednicki's conditions are narrow — free field, vacuum, flat, static, d=3, non-universal UV-dependent coefficient — and none of the states this framework cares about satisfy them. For a measurement paper: one sentence on locality, or cut it. It contributes nothing to #9.

**7. Posit ledger has one stale entry.** §11's table lists #4's verdict as "KEEP — provisional status discharged 6 Aug," which is correct, but the appendix-style summary language elsewhere still reads as though the provisional status is live in places. Minor, but this project's value is partly that its ledger can be trusted at a glance.

### Hygiene

**8. Still no git.** Raised in v1 and v2. It matters more now than it did, because there is code with pinned dependencies and a results set that claims reproducibility — and the only copy is in OneDrive. `git init`, one commit, done in two minutes.

**9. No README.** FRAMEWORK.md is the entry point and says so in its file table, which is nearly sufficient. A four-line README stating the claim, the file map, and "L-sweep ran and failed 6 Aug; project is in write-up" would prevent the next reader from starting where v2 started.

---

## Scientific coherence check

| Claim | Status | Risk |
|---|---|---|
| Core: front converts coherence → entanglement | Streltsov Thm 2, verified numerically | Fine as interpretation; carries no originality and the docs say so |
| Thickness = coherence (#4) | **Verified** | Restricted to monotone-along-history above d=2. Stated |
| Thickness = open-transaction depth (#14) | **Dead** | Closed. Do not re-open |
| Resolution = distinguishing entanglement (#8) | Zurek; verified exactly | Improper-mixture gap owned — still owned |
| Gravity never resolves (#9) | **KEEP + RISK**, internally verified | External only. Needs a specified experiment — issue 2 |
| Born from relaxation | Adopted; teeth are cosmological, out of scope | Honest |
| Full block (#1) | IDLE | Correct. Not a foundation |
| Selection (#10/#16) | OPEN | Unmoved since 1986. Correctly deferred, correctly declared |

**Internal consistency is now good.** The 6 August write-back was thorough — §3's "still owed" item struck, §7's stale dissolve-note struck with the reasoning preserved, SOURCES' τ recommendation reversed in place, the §6 misattribution corrected from a test result. The one remaining drift was the plain-language summary, fixed 9 August.

---

## Documentation quality

| Dimension | Rating | Notes |
|---|---|---|
| Clarity | Excellent | The A/B table and the posit ledger are both models of the form |
| Honesty | **Outstanding** | Failed prediction reported in full detail, in the same file as the passes, with the causal argument for why it can't be rescued |
| Cross-linking | Excellent | Result-routing table meant results landed where they were meant to land |
| Internal consistency | **Good** | Drift fixed; only the lay summary had escaped |
| Reproducibility | **Good** | Pinned deps, one-line repro command, README documenting three real traps and one known 1.6% caveat |
| Completeness for a paper | **Medium** | Content is there; no draft, no abstract, no figure plan |
| Maintainability | Excellent | Dead-ends list, "not to read" list, "do not re-open" markers |

Tone remains working-doc sharp — "don't count on the same," "the paper" — which is right for notes and will need flattening for a journal.

---

## Recommended next actions

Ordered by leverage. The theory phase is over; do not restart it.

1. **`git init` and commit.** Two minutes. Currently one OneDrive folder holds the only copy of a reproducible result set.
2. **Specify the #9 experiment** (issue 2). Mass scale, coherence requirement, what a gravitational which-path measurement is, and whether any current DP-test apparatus is in range. This is the paper's empirical section and it is the last piece of real work.
3. **Re-derive Strubbe's gravitational which-path prediction from his equations** (issue 3) before naming him.
4. **Draft the paper.** Structure suggested by the results: #9 vs Strubbe as the claim; the resolution rule (thinning = environment distinguishability, verified exactly) as the machinery; thickness = coherence as the variable, with the d>2 restriction stated; the L-sweep as a self-contained negative-result section; selection declared open.
5. **Say the "no dynamics of its own" line yourself**, in the discussion. Once, plainly.
6. **Skim Cramer 1986** (issue 4) — needed to source the 1986 claim honestly.
7. **Cut or one-line the area law** (issue 6).
8. **Do not:** re-open gravity-origin, cosmology, τ-adoption, Reading A, or the L-sweep. All are marked closed in FRAMEWORK §12 and §14 and all of those closures are sound.

---

## Bottom line

| | |
|---|---|
| **As a lab notebook** | Outstanding. Continues to be the project's strongest asset |
| **As a theory** | Coherent, internally verified, and now correctly sized |
| **As an empirical programme** | **Executed.** One prediction, tested, failed, reported |
| **As a contribution** | One falsifiable disagreement with a named opponent, plus a closed question |
| **Biggest change since v2** | The sims ran. The distinguishing prediction died. The machinery around it held |
| **Biggest remaining risk** | Never writing it up — or writing it around a claim that no longer exists |
| **Biggest asset** | Willingness to build the thing that could kill the idea, and then publish the result |

**One line:** The framework spent an afternoon proving itself smaller than it hoped, which is more than most foundations programmes manage in a decade — now write the paper that's left.
