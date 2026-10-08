# Project Review: Q-Physics (Resolution-Front Framework)

**Version:** 4
**Date:** 8 October 2026
**Scope:** External read of branch `gravity-area-law` at `db507c8` (PR 2). Full read of [FRAMEWORK.md](FRAMEWORK.md), [RESULTS-01.md](RESULTS-01.md), [RESULTS-02-gravity.md](RESULTS-02-gravity.md), [README.md](README.md), review v3, and the gravity scripts plus their committed output. [Framework-Summary-Plain.md](Framework-Summary-Plain.md) and [SOURCES.md](SOURCES.md) were checked for drift and for whether named debts are still open. The August sims were not re-read line by line; this review does not reopen them. **The October sims were not re-run.** Numbers below are the committed console output and JSON.

This is a research-workspace review, not a software PR review. It supersedes v3.

---

## Why v4 exists

**Review v3 was written on 9 August, before the October scope change.** It is stale in a way worth stating plainly, because October did the thing v3 had marked closed.

| v3 said (9 Aug) | State at `db507c8` (8 Oct) |
|---|---|
| Do not reopen gravity-origin | Reopened on 7 Oct through the area-law route; four tests claimed passed |
| The only empirical content left is #9 vs Strubbe | #9 is now grounded by averaged gravity and carries a BMV prediction; a second prediction (no primordial gravitational waves of quantum origin) is stated as co-equal |
| Cut or one-line the area law; it contributes nothing to #9 | The area law is the gravity route. §6's "call this locality, never gravity" line is lifted |
| No git, no README | Both exist. This review is of a clone of [PR 2](https://github.com/Neil-A/Q-Physics/pull/2) |
| Write the paper around #9; specify the experiment; re-derive Strubbe from his equations | None of the three is done |
| Lay summary was the last drift, and it was fixed | The lay summary is drift again: it still says gravity-origin was cut and should not come back |

v3's account of the August sims stands. #14 failed cleanly. Thickness = coherence holds, with the cross-system restriction. #9's internal check is arithmetic and was reported as arithmetic. Those are not relitigated here.

---

## Overall assessment

**The August standard is the part worth trusting. The October gravity claim is a real choice about semiclassical gravity, written up as a derivation the notes do not contain.**

The project is still unusually good at killing its own ideas and leaving the body where a later reader can find it. Posit #14 was specified in advance, run three ways, and failed: fitted exponent about 0.00 where 1.00 was required, wrong-signed on the mirror's node branch, and causally excluded past L\* = v/γ. That result is written back into §7 and the posit ledger. The sentence in RESULTS-01 that the framework supplies no dynamics of its own is still the sharpest self-description in the repo, and it still belongs in any public write-up, said once, by the author.

October did two different things and the headline treats them as one.

The first is sound. "Settling load causes time dilation" fails reach, universality, and light bending. GPS, Galileo eccentric orbits, MICROSCOPE, and Cassini already say so. That mechanism is correctly in the dead-end list. `tests_2_4.py` reproduces the textbook contrasts: gravitational share of the GPS offset 45.7 µs/day, and solar-limb deflection 1.751″ against the time-only 0.876″ (committed JSON: 1.751196 and 0.875596). Those numbers show the rejected mechanism disagrees with measurements. They do not show that the area-law route is true. Anything that yields Einstein's equations passes the same checks.

The second is a compatibility argument with Jacobson, plus one new commitment. Step 0 of RESULTS-02 already says the framework supplies the ingredients only in part: the area law partly, G an input, local equilibrium a story. The lattice work confirms the entanglement first law for a free scalar, including the Wald term §6's area-law sentence did not contain. That is a real numerical check, and it is the best new result in the October code. It is not a derivation of gravity from the resolution front.

**Verdict:** Keep the August measurement claim at the size v3 left it. Treat October as a decision to source gravity with the average energy of an unsettled mass, updated to the settled outcome when records can meet. That decision is coherent, it is not yet a theory, and it has a kill condition that is already named and not yet done. Do not describe the current notes as gravity derived from the area law and tested four ways.

---

## What October actually settled

### Settled, and the conclusion is right

**Settling-load as the cause of time dilation is dead.** Direction, reach, and universality each fail for that mechanism, for the reasons in the RESULTS-02 test table. The cause, if the framework keeps gravitational time dilation at all, is the place: the front and everything on it slow by the same factor. Dense matter can still settle many records per slow tick. That distinction is the useful October conceptual result, and it does not require the lattice.

**#9's original wording was too weak, and the notes now say so.** "Both slit paths have the same mass" does not stop a quantum metric from distinguishing their locations. That is the content of a BMV experiment. Averaged gravity does remove which-path information from the source. §8's 8 Oct paragraph is the right repair. The price is that #9 is no longer an interpretation of unmodified quantum mechanics plus ordinary gravity. It is a claim about how gravity couples.

### The lattice check — real, and narrower than the headline

Committed output in `sim/gravity/results/`:

| Check | What the output shows |
|---|---|
| Pipeline sanity (`first_law_console.txt`) | Against the lattice's own modular operator, dS/dK = 0.999998 and 0.9975. The comparison pipeline is sound |
| 1D interval | Ratios 1.013 down to 0.983 from 8 to 256 sites, as RESULTS-02 states |
| 3D ball, plain energy density | Median ratio about −0.016 at R = 16.5, 32.5, 64.5. The bulk area-law comparison fails |
| 3D ball, free fit (`ball3d_fit_console.txt`) | Three coefficients on (Laplacian term, volume integral, surface integral): **−0.168, −0.00009, 1.056**, against theory −1/6 ≈ −0.167, 0, and 2π/6 ≈ 1.047. Max relative residual 0.0033 |
| 3D ball, ratio using the theoretical coefficients | Median 0.978, 0.984, 0.985. The floor of the same sample is 0.72, 0.66, 0.64 |

The fit is on the same 54 configurations that are then scored. The volume coefficient landing on zero is the impressive part: the lattice asks for the two corrections the conformal/Wald analysis already contains, and does not ask for a third. RESULTS-02 calls this "two correction terms." The console shows three, with the third negligible. Say it that way.

The summary table's "PASS — 0.97–1.01" quotes the median neighbourhood. The body is more honest: ratios fall to 0.64 where the wave sits mostly inside the ball and dS is tiny. The table should match the body.

What this licenses: a free scalar on a lattice obeys the known entanglement first law once the improved energy density and the Wald surface term are included. What it does not license: that the resolution front produces Einstein's equation, that G is explained, or that the check extends past the free-field states Srednicki's hypotheses already named. A 3D horizon was not run; RESULTS-02's wave-by-wave argument for covering it by the 1D scan is plausible and unexecuted.

### The four tests — two of them are not tests of the new route

| Test | In the notes | In the code | What a pass means |
|---|---|---|---|
| 1 Direction | Argument | No script | Internal consistency with "dense matter settles fast," plus Pikovski et al. on the sign of gravitational time dilation |
| 2 Reach | `tests_2_4.py` | GR clock profile of a uniform ball against a step function that is zero outside the Earth | The rejected local-load rule disagrees with the Newtonian/GR potential. Galileo is cited, not computed |
| 3 Universality | "Pass by construction" | No script | The new route couples only to energy, so it cannot fail this test. MICROSCOPE and JILA constrain the rejected rule. The 7 Oct correction is right: JILA does not test "unsettled things don't slow clocks," because every atom in the comparison is equally unsettled |
| 4 Light bending | `tests_2_4.py` | Ray trace of n = 1 + (1+γ)GM/(c²r) | Numerical deflection matches 4GM/c²b and 2GM/c²b. Cassini is cited, not fitted |

Tests 1 and 3 are prose. Tests 2 and 4 are a 33-line reproduction of standard formulas. Killing the old mechanism with them is fair. Counting them as four passed tests of "gravity via the area law" overstates the file.

---

## The two predictions are one commitment, and the second is a further leap

**Prediction 1** — BMV-type experiments see no entanglement through gravity — follows from sourcing the metric with ⟨Tμν⟩, and from the further rule that a settled outcome replaces the average only once records can meet. The first half is a known semiclassical position. RESULTS-02 cites Struyve (2025) and Page & Geilker (1981) for it. Aziz & Howl's indirect classical channel is acknowledged and set aside as too small for near-term experiments. That is the right shape for the claim. It is not a signature unique to the resolution front. The front's addition is the update rule.

**Prediction 2** — no primordial gravitational waves of quantum origin — does not follow from prediction 1. Inflationary tensor modes are not the Newtonian field of a laboratory mass in superposition. Krauss & Wilczek argue one direction: a detection would be evidence that gravity is quantized. A non-detection at σ(r) ~ 10⁻³, which is the target RESULTS-02 quotes, leaves both quantum gravity and this framework standing. Many inflationary models sit below that line. "Gravity is never quantum" is a slogan stretched over two different claims. Keep prediction 1 in the ledger. Park prediction 2 until a derivation inside the framework produces it.

**Newton–Schrödinger** is named as a small side effect. It is the place the departure from ordinary quantum mechanics becomes a number, and "small" has not been calculated for any system the framework cares about. Price it for one concrete case, or stop calling it small.

---

## The kill condition for §15

§14 item 7 already asks whether averaged gravity sourced locally holds together, "mainly the moment a distant pull updates." That item is not a leftover. It is the condition under which the October reopening survives.

Einstein's equation, through the Bianchi identities, requires a conserved source. An expectation value can be conserved. A source that jumps from the average to one outcome has to say where the difference sits at events that have not yet received the record. The three readings are different theories:

1. The source stays ⟨T⟩ until the record's light cone arrives, then jumps.
2. The source was always the eventual outcome, and ⟨T⟩ is only what a distant observer is entitled to compute in the meantime.
3. Some other structure carries the difference until the records meet.

Reading 1 spends energy that was not in the stress tensor, unless the jump is arranged so that ∇·T = 0 at every event. Reading 2 puts the outcome into the gravitational field before the record exists, which is the thing §15 says gravity never carries, and it reopens signalling unless the field is forbidden from being read. Reading 3 is the one that might work, and it is not written down. "Until the records can meet, a distant mass keeps pulling from its average" is a rule for observers. It is not yet a stress tensor.

This is the same seam that hits objective collapse plus semiclassical gravity. If no conserved source can be written, the gravity reopening should be parked again, and #9 should be kept only as the semiclassical bet it actually is. Do not write the black-hole account (§14 item 8) or extend the balloon analogy while this is open. Both will inherit a source that has not been shown to exist.

---

## #9 and Strubbe

The disagreement in the §8 table is still the sharpest named contrast in the measurement half of the project: this framework says gravity cannot distinguish which-path; Strubbe says it can. Gravitationally induced entanglement is now "no" on both sides of that table, so BMV-entanglement is no longer the experiment that separates them. The separating experiment is a gravitational which-path measurement that, on his account, leaves the interference pattern intact.

Two August debts are still open, and both are now more important because the claim is public-shaped:

- **His prediction has not been re-derived from his equations in this repo.** §8 and SOURCES record a reading. Naming him in an abstract requires the derivation.
- **No experiment is specified.** Mass scale, separation, coherence time, what is measured, and which current or proposed apparatus could see it. "Checkable" is still doing the work a methods paragraph should do. The Diósi–Penrose apparatus and a BMV apparatus are not the same test, and the notes sometimes talk as though one disagreement covers all three (collapse, which-path, entanglement).

The internal α = 0 check remains exactly what v3 said it was: thinning is environment distinguishability, as arithmetic. It cannot confirm averaged gravity. Nothing in `sim/` evolves a metric.

---

## Documentation

The repo's own discipline is that the ledger matches the last run. Three entry points currently disagree with §15.

| File | What a new reader is told | What §15 says |
|---|---|---|
| [Framework-Summary-Plain.md](Framework-Summary-Plain.md) | Gravity-as-origin was cut and should not come back. The only live bet is that gravity never collapses a wavefunction | Gravity-origin is reopened. The live bets are averaged gravity, no BMV entanglement, and (as written) no primordial gravitational waves of quantum origin |
| REVIEW v3, which this file replaces | Do not reopen gravity-origin. Write the #9 paper | Superseded |
| [FRAMEWORK.md](FRAMEWORK.md) §14, closing paragraph | The only empirical content is #9 vs Strubbe, plus an interpretation of open-system quantum mechanics | §15, immediately after, widens the claim |

[README.md](README.md) is the right front door. Its review row points here. The lay summary should not be handed to anyone until it is rewritten. A one-line banner at the top is the minimum if a rewrite waits on the questions below.

§15's stress map and the "Gravity via the Area Law" findings note are private claude.ai links. RESULTS-02 is enough to audit the gravity numbers. It is not enough to audit the phenomenon-by-phenomenon map §14 item 10 says is being merged and rechecked. A claim that lives only at a private URL is not in the ledger.

Cramer (1986) is still marked unread in [SOURCES.md](SOURCES.md). The selection-problem paragraph still dates the open question to that paper via Strubbe's silence. If the paper asserts "open since 1986," read the paper.

Code notes in [sim/gravity/README.md](sim/gravity/README.md) are up to the August standard: four real traps, discarded runs labelled, stack pinned. That file is in better shape than the headline it serves.

---

## Questions

These decide what the next document is allowed to say. Recommendations that depend on an answer are marked.

1. **Scope.** On 5 Oct the mission moved from the double slit and the measurement problem to "how much known physics fits." Is that the charter now? If the conserved-source check fails, does gravity park again, or does the widened project stay open around it?
2. **What "gravity is never quantum" means.** (a) There is no quantized metric, so there are no vacuum tensor modes of quantum origin, cosmological or otherwise. (b) An unsettled mass gravitates by its average, and a settled mass gravitates by the outcome. Prediction 1 needs (b). Prediction 2 needs (a). Which one was decided on 8 Oct?
3. **The update rule.** When a fold closes, which of the three readings in the kill-condition section is intended? If none of them, what is the stress tensor at an event outside the record's light cone?
4. **Strubbe.** Has the gravitational which-path claim been re-derived from his equations, outside this repo? If yes, where does that derivation live? If no, §8 should say the column is a reading.
5. **The private record.** Should the stress map and the findings note come into the repo in some form a later reader can open? If not, §15 should stop citing them as the phenomenon-by-phenomenon record.
6. **What gets written first.** The measurement note (resolution rule, thickness, the L-sweep as a negative result, #9 as the semiclassical bet), or a gravity note? Recommendation 4 below assumes the measurement note until question 3 has an answer.

---

## Recommendations

Ordered by leverage. Items 4 and 6 wait on the questions.

1. **Rewrite the RESULTS-02 headline to the strength of the evidence.** Suggested replacement, in the file's own voice: the old settling-load mechanism is dead on reach, universality, and light bending; the free-scalar first law reproduces on the lattice, including the Wald term, and fails without it; G is not derived; equilibrium is not proved; the framework's addition is that gravity follows the settled outcome once records can meet, and follows the average until then. Change the summary table's 3D line from "PASS — 0.97–1.01" to the median and the floor, and call the fit a three-coefficient fit whose volume term is zero.
2. **Make the conserved source the next piece of work, and the park condition for the reopening.** A short note is enough: the proposed Tμν, the event at which it changes, and a check that ∇·T = 0. If it cannot be written, park gravity-origin again with a closing note, and leave #9 as the semiclassical bet. Do not start §14 item 8 (black holes) or further balloon geometry before that.
3. **Split prediction 2 out of the co-equal pair** in §15, the README status line, and the RESULTS-02 decision list, unless question 2 is answered "(a)" and a derivation exists. Until then the ledger should carry one prediction.
4. **Write the measurement note, not the gravity paper.** Structure carried over from v3, updated for 8 Oct: the resolution rule (thinning = distinguishability, verified exactly); thickness = coherence, with the d > 2 restriction; the L-sweep in its own section; #9 as a semiclassical coupling claim against Strubbe's which-path claim, with the BMV prediction stated as that coupling and not as a derivation of Einstein's equations. The area-law material is an appendix titled as a compatibility check. Promote this to the main paper only if recommendation 2 succeeds. *Waits on question 6.*
5. **Specify the separating experiment** before Strubbe is named in an abstract. One paragraph: what is prepared, what is measured, what his equations predict, what averaged gravity predicts, and whether any proposed apparatus is in range. Re-derive his claim from his equations in the same note. *The derivation half waits on question 4 only if it already exists somewhere.*
6. **Price the Newton–Schrödinger side effect for one system** already in the sources (a molecule above 25 kDa, or a BMV mass pair). Report the fractional shift. If it is not small, §15's "small departure" has to change.
7. **Stop the remaining entry-point drift.** Rewrite [Framework-Summary-Plain.md](Framework-Summary-Plain.md), or put a dated banner on line 1 that it predates October and contradicts §15. Soften §14's closing paragraph so it does not say the only empirical content is #9 vs Strubbe while §15 says more. Bring the stress map into the repo, or stop citing it. The README review row already points here. *The lay rewrite waits on questions 2 and 3 for the gravity paragraphs. The banner does not.*
8. **Read Cramer (1986)** before the selection section dates an open problem to him. He is still `[ ]` in SOURCES.
9. **Do not:** re-open #14 or either reading of the front; re-run the lattice looking for a closer ratio; treat tests 2 and 4 as evidence for Jacobson; write primordial gravitational waves into an abstract on the current derivation.

---

## Where it stands

| | |
|---|---|
| **As a lab notebook** | Still the project's strongest asset, August and October both. Discarded runs are labelled. The failure of #14 is fully written back |
| **As a theory of measurement** | The size v3 described. An interpretation of open-system quantum mechanics, plus one coupling claim that is now explicitly semiclassical |
| **As a theory of gravity** | A decision to use Jacobson's route and ⟨Tμν⟩, with a light-cone update rule that has no stress tensor yet. G is an input. The four-test headline is ahead of the code |
| **As an empirical programme** | August: executed, and the distinguishing prediction failed. October: standard results reproduced; the new predictions are not yet at the stage #14 was on the morning it was killed |
| **Biggest change since v3** | Gravity-origin reopened. The weak form of #9 was replaced by averaged gravity. The record at the front door went stale |
| **Biggest remaining risk** | Writing, or citing, "gravity comes out of the framework" before a conserved source exists |
| **Biggest asset** | The same one as in August: the willingness to build the check that can kill the idea. The next check is already named |

**One line:** October killed a bad mechanism and adopted semiclassical gravity; it did not derive gravity, and the update rule is now the whole question.

---

## Response, 8 October 2026

*Added after reading v4. Records what was accepted and acted on in the same commit, what was added, and what waits on Neil.*

**Acted on in this commit:** recommendation 1 (RESULTS-02 headline, summary table, three-coefficient fit, tests 1 and 3 marked as argument), 2 (conserved source made the gate for the reopening; §14 items 8 and balloon geometry held), 3 (prediction 2 parked, one prediction in the ledger), 7 in part (dated banner on the lay summary; §14 closing paragraph softened; README status line), and the date on the selection problem softened until Cramer is read (8). §8's Strubbe column is marked as a reading until a re-derivation exists in the repo.

**Added to the review's kill condition.** Reading 3 has published, worked-out examples, so the conserved-source check starts from them rather than from a blank page:

- Tilloy & Diósi (2016) source the Newtonian field from the record of a spontaneous-localization process. The source is noisy, consistent, and does not signal.
- Oppenheim's postquantum classical gravity (2023) couples a classical metric to quantum matter consistently. It predicts no gravitationally induced entanglement, and it fixes a trade-off between decoherence of the matter and diffusion of the metric that experiments can bound (Oppenheim et al. 2023).

The question for §14 item 7 becomes: is the light-cone update rule one of these, a variant of one, or something that fails where they succeed? If it maps onto Oppenheim, the framework inherits a consistent theory and a real kill condition, and prediction 1 stops being distinctive to the framework.

**Note on recommendation 6.** "Small" is likely right for the 25 kDa molecule. It is not obviously right for a BMV mass pair: the averaged self-pull between the two branches of one mass is tiny as a displacement, but whether it is tiny as a visibility or phase effect depends on the wave-packet width. Not priced yet.

**Answered by Neil, 8 Oct:** question 1 — the charter is updated to "an interpretation of quantum mechanics plus one semiclassical claim about gravity" (README, FRAMEWORK §15). Question 4 — no re-derivation of Strubbe exists; §8 says so.

Question 2 — **(a)**, the broad meaning: no quantized metric anywhere. Prediction 2 is restored in a sharper form (tensor modes strongly suppressed, second order only, after the inflaton settles), with its derivation owed (FRAMEWORK §14 item 13). Published precedent: León, Sudarsky and colleagues. Question 5 — the Stress Map is exported to [stress-map/](stress-map/); nothing on it is done until all of it is done. Question 6 — the measurement note comes first.

Neil also stated (8 Oct) that there is no empty space in RFF: everything is primed for a resolution event. Recorded in §15 as a refinement of the vacuum bullet.

**Still waiting:** question 3 (the update rule — this is the §14 item 7 work itself), and the lay-summary rewrite.
