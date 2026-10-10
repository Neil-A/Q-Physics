# Sim Spec 03 — Selection: does the loom relax to Born?

*Written 10 October 2026, before any code. Purpose: start work on the selection problem, which is the last fully open item in the quantum column of the Stress Map ("Measurement: why one outcome"). The start point is the new position in [FRAMEWORK.md §9](FRAMEWORK.md).*

> **STATUS: specified, not run.** Neil decided the §4 choices on 10 October: **test both rules**, and **choice (a)** for the conflict. The pass conditions in §5 still need his sign-off before any test runs.

---

## 1. The target

Plainly: **what picks which outcome?**

The §9 position (10 October) gives the shape of the answer:

- A **seed** comes from the fluctuations of the primed substrate at the front.
- The **immediate conditions** resolve the seed into one outcome, as a loom weaves a thread. Above the seed level, everything is conditional.
- The **Born weights come from relaxation**: any spread of seeds settles to the Born spread before the record forms.

This spec asks one question: **can a weave rule do this without help?** The rule must:

1. pick one outcome for each seed, with no further randomness at the record;
2. move any spread of seeds to the exact Born spread;
3. do this fast, before the record forms;
4. not permit signals faster than light once relaxation is complete;
5. sample the interference pattern that SIM-SPEC-02 §9 derives, and not change it.

---

## 2. What is already established

- **The form of interference** (clock hands, the Born square) follows from pairs, combinability, comparison by clock difference and one observed dark fringe ([SIM-SPEC-02 §9](SIM-SPEC-02-amplitudes.md); passed [REVIEW-04](REVIEW-04-amplitudes-repair.md)). Selection only picks a point inside this pattern.
- **A record needs the update to spread past the point of return** (FRAMEWORK §15, "Isolation"; [sim/amplitudes/revivals.py](sim/amplitudes/revivals.py)).
- **Relaxation is known physics in two published dynamics.** In pilot-wave theory, the relaxation time falls roughly as 1/M, where M is the number of superposed modes (Towler, Russell & Valentini 2012). In Nelson's stochastic dynamics, trajectories that start at one point reach the Born spread; in a double slit they do this before the fringes appear (Hardel, Hervieux & Manfredi 2023).
- **Without relaxation, signals are possible.** A spread of hidden values that is not Born permits signals faster than light (Valentini). So relaxation must be complete wherever we can test.

---

## 3. Prior art for this spec

*Abstract-level reads on 10 October unless marked. Each entry needs a full read before a write-up uses it.*

| Work | What it does | What it means here |
|---|---|---|
| Bohm, Phys. Rev. 85, 166 (1952) | Pilot-wave theory: a definite position, steered by the wave | Weave rule W1 (§4) |
| Valentini, Phys. Lett. A 156, 5 (1991) | Relaxation to the Born spread; non-Born spreads permit signals | The relaxation account in §9 |
| Towler, Russell & Valentini, Proc. R. Soc. A (2012), arXiv:1103.1589 | Relaxation time ∝ 1/M in a 2D box, robust across coarse-grainings | Benchmark for W1 |
| Dürr, Goldstein & Zanghì, J. Stat. Phys. 67, 843 (1992) | Born from typicality, with no need for relaxation | A rival account; noted, not used |
| Nelson, Phys. Rev. 150, 1079 (1966) | Stochastic mechanics: random kicks plus a drift give the Born spread | Weave rule W2 (§4) |
| Wallstrom, Phys. Rev. A 49, 1613 (1994) | Nelson's theory needs an extra quantization condition, put in by hand | A known cost of W2 |
| Petroni & Guerra (1995) | Quantum states act as attractors for Nelson processes *(not read)* | Relaxation in W2 |
| Hardel, Hervieux & Manfredi, Found. Phys. (2023), arXiv:2305.04084 | Nelson trajectories relax to Born; in free fall, fringes appear before relaxation is complete | Benchmark for W2; a case where the race of §5 Test 2 matters |
| Colin & Valentini, Phys. Rev. D 92, 043520 (2015), arXiv:1407.8262 | Relaxation that does not finish at long wavelengths gives a large-scale CMB power deficit | The possible test in §9 |
| Strubbe (2025), arXiv:2505.10383 | Outcome picked by a uniform random number against a threshold | The trap: a rule chosen to give Born is fiat |

---

## 4. Two candidate weave rules (the loom)

Both rules exist in the literature. If one works, RFF adopts that published dynamics and reads it in its own terms. This spec does not claim a new dynamics.

- **W1 — steered seed** (pilot-wave type). The seed is a point. It moves in the direction that the summed clock hands set (the gradient of the phase). There is no randomness after the seed. The nodes of the pattern mix the seeds, and that mix gives relaxation. *In RFF terms:* the immediate conditions steer each thread. This matches "above the seed level, everything is conditional" most closely.
- **W2 — thread with kicks** (Nelson type). The seed point moves in the same steered direction. It also gets small random kicks from the primed substrate all the time. The kick size is ħ/2m. The kicks and the steered motion together give relaxation. *In RFF terms:* the substrate continues to feed fluctuations into the loom. This matches "the front carries fresh seeds all the time" most closely.

**Decided 10 Oct (Neil): test both.** The two rules agree with quantum mechanics once relaxation is complete. They differ only before it is complete.

### A conflict to settle first *(found on the map recheck, 10 Oct; decided: choice (a))*

Both rules give the seed a definite value (a position) before the record forms. Relaxation needs this: a spread of values can only settle if the values exist and move. But the map item "No values before measurement" says: *nothing has a value until it is anchored*.

The two cannot both stand as written. There are two consistent choices:

- **(a) Keep relaxation.** The seed has a value from the start, but only for position. Every other quantity gets its value at the record, and that value depends on what else is measured (it is contextual). The Kochen–Specker theorem forbids values that do not depend on context; it permits this. Pilot-wave theory works in this way. The map item changes from "no values before measurement" to "**no context-free values** before measurement".
- **(b) Keep "no values before the record".** Then nothing can relax before the record, because no value exists to move. The seed must then pick the outcome at the record with the Born weights put in directly. That is the fiat this spec must avoid (Strubbe, §3).

Choice (a) is the only one that keeps relaxation and the possible CMB test. It needs the map change above. Section 9 of the framework already places RFF in the hidden-variable family, so (a) also removes an older conflict between §9 and the map item.

---

## 5. Tests — specified in advance

### Test 1 — Do the rules relax? *(benchmark against published results)*

**Model.** (a) For W1, the 2D box of Towler, Russell & Valentini, with M = 4 to 64 superposed modes. (b) For W2, the double slit of Hardel, Hervieux & Manfredi. In both, start the seeds far from the Born spread: all seeds near one point, or spread evenly.

**Measure.** The coarse-grained H-function, H = ∫ ρ ln(ρ / |ψ|²), against time. Also the distance between the seed spread and the Born spread at the screen.

**Pass:** W1 gives a relaxation time ∝ M^(−1 ± 0.2). W2 reaches the Born spread in the double slit before the fringes form, as published.
**Fail:** either rule does not reproduce its published result. That is a code error until shown otherwise.

*This test reproduces prior art. It checks the code. It is not new physics.*

### Test 2 — The race between relaxation and the record *(the RFF test)*

**Question.** RFF says the Born weights hold only if relaxation finishes before the record forms. How large is the difference from Born when the record forms first?

**Model.** The double slit again. Add a record at a set time t_rec: the position couples to N partners, as in the August central-spin model, so the record forms at a known rate. Vary t_rec from far below to far above the relaxation time τ.

**Measure.** The outcome statistics at the record, compared with the Born weights, as a function of t_rec / τ.

**Pass:** the difference from Born is large for t_rec ≪ τ and falls to zero for t_rec ≫ τ, with a clear transition near t_rec ≈ τ. This gives RFF a quantitative rule: *where records form faster than relaxation, statistics are not Born.*
**Fail:** no transition, or the difference does not fall to zero. Then "relaxation before the record" does not describe the dynamics, and §9 point 3 needs revision.

### Test 3 — Equilibrium forbids signals *(a check of Valentini's theorem)*

**Model.** Two entangled particles. One side changes its measurement choice. The other side looks at its own statistics.

**Pass:** with seeds in the Born spread, the far side sees no change. With seeds far from the Born spread, the far side sees a change.
*This is a check of a known theorem. It cannot fail the position, but it confirms that the code treats signals correctly.*

---

## 6. Kill conditions — set in advance

- **A rule needs a start spread that already equals Born.** That is fiat, as with Strubbe. That rule fails.
- **Test 2 shows no transition.** Then the "race" view of §9 fails, and point 3 of §9 must change.
- **Already published:** not a kill. The pilot-wave literature possibly contains the race of Test 2 already. If so, RFF adopts and cites it.
- **W2 needs Wallstrom's extra condition:** not a kill. It is a known cost of W2, and the write-up must state it.

---

## 7. What it would change on the map

| Item | Now | If Tests 1 and 2 pass |
|---|---|---|
| Measurement: why one outcome | Fits with work | Fits with work: selection named (seed plus loom, with relaxation) |
| Born rule | Fits with work | Fits with work: the form comes from SIM-SPEC-02; the sample comes from relaxation |
| Quantum seeds of galaxies | Fits with work | Possible test added: relic statistics that are not Born |

---

## 8. Out of scope

Which rule nature uses: the two rules differ only out of equilibrium, and laboratory systems are already in equilibrium. The CMB calculation itself (Colin & Valentini did it in pilot-wave theory; RFF would need its own version). Gravity. Many particles beyond the two in Test 3.

## Sources

Listed in §3.
