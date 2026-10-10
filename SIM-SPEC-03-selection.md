# Sim Spec 03 — Selection: does the loom relax to Born?

*Written 10 October 2026, before any code. Purpose: start work on the selection problem, which is the last fully open item in the quantum column of the Stress Map ("Measurement: why one outcome"). The start point is the new position in [FRAMEWORK.md §9](FRAMEWORK.md).*

> **STATUS: run 10 October 2026; results in [RESULTS-04-selection.md](RESULTS-04-selection.md).** W1 passes Tests 1a, 2 and 3. The W2 verdicts (Tests 1b and 2) are pending under §6, because the W2 step check failed. It failed on the fitted τ_q, which this run shows to be fragile. Neil decides how to fix it before a W2 rerun (RESULTS-04, "Decisions"). Neil approved the pass conditions on 10 October, on the condition that each matches known physics; §5.5 lists what changed and why.

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
- **Relaxation is known physics in two published dynamics.** In pilot-wave theory, the relaxation time τ scales as M^p, where M is the number of superposed modes, with p = −1.05 ± 0.03 to −1.09 ± 0.18 across grains (Towler, Russell & Valentini 2012, Table I). With only a few modes, a residue can stay (Abraham, Colin & Valentini 2014). In Nelson's stochastic dynamics, trajectories that start at one point reach the Born spread; in a double slit they do this before the fringes appear (Hardel, Hervieux & Manfredi 2023).
- **Without relaxation, signals are possible.** A spread of hidden values that is not Born permits signals faster than light (Valentini). So relaxation must be complete wherever we can test.

---

## 3. Prior art for this spec

*Abstract-level reads on 10 October unless marked. Each entry needs a full read before a write-up uses it. For TRV and Hardel et al., Claude checked the set-up, the equations, the tables and the figure captions in the full text on 10 October.*

| Work | What it does | What it means here |
|---|---|---|
| Bohm, Phys. Rev. 85, 166 (1952) | Pilot-wave theory: a definite position, steered by the wave | Weave rule W1 (§4) |
| Valentini, Phys. Lett. A 156, 5 (1991) | Relaxation to the Born spread; non-Born spreads permit signals | The relaxation account in §9 |
| Towler, Russell & Valentini, Proc. R. Soc. A 468, 990 (2012), arXiv:1103.1589 *(set-up and Tables I–II checked)* | τ ∝ M^p in a 2D box, p = −1.05 ± 0.03 at the coarsest grain; 6 phase sets per point; M = 4 left out of the fit | Benchmark for W1 (Test 1a) |
| Abraham, Colin & Valentini, J. Phys. A 47, 395306 (2014), arXiv:1310.1899 | With 4 modes, H̄ can keep a residue above 10% of its start value; with 25 modes, decay is close to exponential | Why M = 4 is only reported, and why Test 2 uses the median |
| Dürr, Goldstein & Zanghì, J. Stat. Phys. 67, 843 (1992) | Born from typicality, with no need for relaxation | A rival account; noted, not used |
| Nelson, Phys. Rev. 150, 1079 (1966) | Stochastic mechanics: random kicks plus a drift give the Born spread | Weave rule W2 (§4) |
| Wallstrom, Phys. Rev. A 49, 1613 (1994) | Nelson's theory needs an extra quantization condition, put in by hand | A known cost of W2 |
| Petroni & Guerra (1995) | Quantum states act as attractors for Nelson processes *(not read)* | Relaxation in W2 |
| Hardel, Hervieux & Manfredi, Found. Phys. (2023), arXiv:2305.04084 *(§4.1, Eqs. 10–14 and Figs. 4–5 checked)* | Nelson trajectories relax to Born; in the double slit, before the fringes appear; in free fall, fringes appear before relaxation is complete | Benchmark for W2 (Test 1b); a case where the race of Test 2 matters |
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

*Rewritten 10 October, before any code, to match each condition to the published set-up. The old text of this section is in git (commit dbdf434). The changes and their reasons are in §5.5.*

**Words used in this section.**

- **Spread** (ρ): how the seeds are distributed in position.
- **Born spread**: |ψ|².
- **H̄**: the coarse-grained H-function, H̄ = Σ ρ̄ ln(ρ̄ / |ψ|²‾), summed over cells. It is zero only when the spread equals the Born spread at the scale of the cells.
- **L1**: the sum over bins of |ρ̄ − |ψ|²‾|. It is 2 at the start (all seeds at two points) and 0 at Born.
- **TV**: half of L1, for the outcome regions of a record. It is the largest error in the probability of any outcome.
- **Noise floor**: the value that a metric has when the seeds are a finite sample from the exact Born spread. For H̄ with K cells and N seeds, it is about (K − 1)/(2N). Each test computes its own floor.

### Test 1a — W1 relaxes as published *(Towler, Russell & Valentini 2012)*

**Model.** The 2D box of TRV.

- Box side π; ħ = m = 1.
- ψ = (2/(π√M)) Σ sin(nx) sin(my) exp(i(θ_nm − E_nm t)), with n, m = 1 … √M and E_nm = (n² + m²)/2. The period of ψ is 4π.
- M ∈ {4, 9, 16, 25, 36, 49, 64}. For each M, use 6 sets of random phases θ_nm with fixed seeds (TRV also used 6).
- Start spread: the ground state, ρ = (4/π²) sin²x sin²y.

**Method.**

- Sample N = 5 × 10⁴ seeds from the start spread. Move each seed with the guidance equation v = Im(∇ψ/ψ).
- Integrator: RK4. The step is h = min(0.05, 0.005/|v|), so that no step moves a seed more than 0.005.
- If a step puts a seed outside the box, reflect it back into the box. Count these events.
- Coarse cells: 16 × 16. This is the coarsest grain in TRV (ε = 64 on their 1024 lattice).
- Compute H̄ every π/8 from t = 0 to 4π. Compute |ψ|²‾ in each cell by Gauss–Legendre quadrature.
- TRV computed H̄ by backtracking from a lattice. This test samples forward. The quantity is the same; the noise differs.

**Fit.** For each run, fit a straight line to ln H̄ against t, as TRV did. Use only the points where H̄ is more than 10 times the noise floor. The slope gives −1/τ. For each M, τ(M) is the mean over the 6 runs, and its error is their standard deviation. Fit τ = A·M^p by weighted least squares over M = 9 … 64. TRV left out M = 4, because its spread of τ is very large. This test also leaves it out and only reports it.

**Checks to do before the pass condition** (each one is a code check from known physics):

1. *Equivariance.* Start 10⁵ seeds from the exact Born spread (M = 64, phase set 0). The larger N makes this the stricter check. H̄ must stay below the noise floor plus 5 standard deviations of the floor at every output time.
2. *Step size.* Run M = 64, phase set 0 again with the step limit 0.0025. The two values of τ must agree within 5%.

**Pass:** p lies in −1.05 ± 0.20. TRV found p = −1.05 ± 0.03 at this grain, and p from −1.05 to −1.09 at the other grains. Their largest error bar is 0.18; this test rounds it to 0.20.
**Fail:** p outside that band. That is a code error until shown otherwise.

*This test reproduces prior art. It checks the code. It is not new physics.*

### Test 1b — W2 relaxes as published *(Hardel, Hervieux & Manfredi 2023)*

**Model.** The 1D double slit of Hardel et al. (their §4.1).

- ħ = m = a = 1.
- ψ(x, 0) ∝ exp(−(x + a)²/2σ²) + exp(−(x − a)²/2σ²), with free motion after t = 0. Their Eq. 10 prints the normalisation as [2√(πσ)(1 + e^(−a²/σ²))]^(−1/2). The overlap factor e^(−a²/σ²) agrees with this form of the Gaussian only if √(πσ) means √π·σ. This test uses √π·σ.
- σ ∈ {0.2, 0.3, 0.4, 0.5, 0.6, 0.7}. Hardel et al. studied σ/a from 0.2 to 0.7.
- Start: all seeds at x = ±a, half at each point (their Eq. 11).

**Method.**

- Dynamics: dX = b dt + √(2D) dW, with D = ħ/2m = 1/2 and drift b = Im(ψ′/ψ) + Re(ψ′/ψ). This is their Eq. 4 with ħ = m = 1.
- Integrator: Euler–Maruyama with dt = 10⁻⁴. Hardel et al. used a second-order scheme. The step check below covers this difference.
- N = 4 × 10⁵ seeds. Run to t = 1.5.
- Output every 10⁻³ up to t = 0.1, and every 10⁻² after that.
- L1: use 100 bins, each with Born weight 1/100 at that time.

**Fit.** Fit L1(t) = α₁ exp(−α₂ e^(α₃ t)) to ln L1 (their Eq. 14). Use only the points where L1 is more than 3 times its noise floor. The relaxation time is τ_q = 1/(α₂α₃), the point where the tangent at t = 0 meets the time axis (their definition).

**Interference time τ_int.** Hardel et al. define it in words: "the time when the first maximum appears in between the two original wavepackets". This test uses the literal definition: the first time that |ψ|² has a local maximum at x = 0. For this ψ, that time is τ_int = σ² √((a² − σ²)/(a² + σ²)). This definition gives the earliest time, so it gives the hardest test. The test also reports a second definition, for a peak that is visible: the first time that the peak at x = 0 stands at least 10% of the highest peak above the next minimum.

**Checks to do before the pass condition:**

1. *Figure check.* For σ = 0.09, |ψ|² at t = 0.12 must have a local maximum at x = 0, as their Fig. 4 shows. This value of σ is outside their range; the figure only shows that the peak exists by t = 0.12. It does not fix the exact time.
2. *Equivariance.* Start N seeds from the exact Born spread (σ = 0.4). L1 must stay below its noise floor plus 5 standard deviations at every output time.
3. *Step size.* Run σ = 0.2 and σ = 0.7 again with dt = 5 × 10⁻⁵. Each value of τ_q must agree within 5%.

**Pass:** τ_q < τ_int for every σ, with the literal definition of τ_int. This is their published result ("for every value of σ … quantum equilibrium is reached before the appearance of quantum interferences").
**Partial:** τ_q < τ_int only with the second definition. Record that this result depends on the definition. It is not a pass, and it is not a code error, because the paper does not give a formula for τ_int.
**Fail:** τ_q ≥ τ_int with both definitions, for any σ. That is a code error until shown otherwise.

*This test also reproduces prior art.*

### Test 2 — The race between relaxation and the record *(the RFF test)*

**Question.** RFF says that the Born weights hold only if relaxation finishes before the record forms. How large is the difference from Born when the record forms first?

**The record.** An ideal record at time t_rec: it reads which outcome region holds the seed, at that instant. After the record, the outcome is fixed. So the outcome frequencies are the coarse-grained spread at t_rec. A record that forms at a finite rate (the N-partner model of August) is out of scope (§8).

**Systems.** Each rule runs in its own Test 1 system, because each published benchmark exists only there. W1 cannot use the double slit: in 1D, pilot-wave paths cannot cross, so a 1D spread that is not Born never relaxes.

- **W1:** the Test 1a box, M = 64, all 6 phase sets. Continue these runs to t = 12π (3 periods). Outcome regions: 4 × 4 squares.
- **W2:** the Test 1b double slit, σ = 0.4, the same run. Outcome regions: 20 bins, each with Born weight 1/20 at t_rec.

**Measure.** TV between the outcome frequencies and the Born weights, as a function of t_rec. Also the noise floor of TV: its mean and standard deviation for N seeds sampled from the Born spread.

**Pass (W1):**

1. Fit ln TV against t over [0, 4π], with the window rule of Test 1a (TV more than 3 times its floor). The e-fold time T_TV lies between 0.5τ and 4τ, where τ is the Test 1a value at M = 64. *Reason:* for a small difference, TV scales as √H̄, so T_TV ≈ 2τ. Coarser regions relax faster: TRV found τ ∝ ε^q with q from −0.20 to −0.37, so 4 × 4 regions can lower T_TV to about 1.2τ. The band covers both effects.
2. At t_rec = 12π, the median TV over the 6 phase sets lies below the floor mean plus 3 standard deviations.

**Pass (W2):**

1. The time at which TV falls to half its start value lies between 0.25τ_q and 4τ_q, where τ_q is the Test 1b value at σ = 0.4.
2. At t_rec = 1.5, TV lies below the floor mean plus 3 standard deviations.

**Fail:** for either rule, TV does not fall to the floor, or it falls on a time scale outside the band. Then "relaxation before the record" does not describe the dynamics, and §9 point 3 needs revision.

*Note.* In both published dynamics, Test 2 follows closely from Test 1. Its value for RFF is the number it gives: how far from Born a record is, as a function of t_rec/τ. That is the quantitative form of "where records form faster than relaxation, statistics are not Born".

### Test 3 — Equilibrium forbids signals *(Valentini's theorem)*

**Model.** Two particles, each in a 1D harmonic trap with ω = 1 (ħ = m = 1). Entangled state: ψ₀ = [φ₀(x₁)φ₁(x₂) + φ₁(x₁)φ₀(x₂)]/√2, with φ₀ and φ₁ the two lowest trap states.

**The choice at A.** At t = 0, A either does nothing, or applies a local pulse exp(iκx₁²) with κ = 1 to particle 1. The pulse is a short, strong change of A's own trap. B looks only at particle 2.

*Why a pulse in x₁², not a kick in x₁.* A kick exp(ipx₁) cannot show a signal in this state. It only moves particle 1 along a classical path and adds a phase that depends on x₁ alone. So it leaves the guidance of particle 2 unchanged, in every spread. The pulse in x₁² does change that guidance. Claude found this on 10 October, in the set-up check.

**Exact evolution.** After the pulse, each trap state stays a Gaussian, or x times a Gaussian, with a width parameter A(t) = (A₀ cos t + i sin t)/(cos t + iA₀ sin t), where A₀ = 1 − 2iκ. The amplitudes scale as (cos t + iA₀ sin t)^(−1/2) and ^(−3/2). The code checks these closed forms against a direct numerical evolution.

**Ensembles.**

- *Equilibrium:* N = 10⁵ seeds sampled from |ψ₀|².
- *Not equilibrium:* N = 10⁵ seeds sampled from |φ₀(x₁)φ₀(x₂)|².
- Both choices at A use the same start points. W2 also uses the same random kicks for both choices.

**Measure.** B's histogram of x₂: 40 bins on [−4, 4], at t = 0.5, 1, 2 and 3. Compute TV between B's histograms for the two choices. The null band is the mean plus 3 standard deviations of TV between two independent samples of N seeds from B's Born marginal (200 pairs). With the same start points, the true noise is smaller than this band, so the band is cautious for the equilibrium check.

**Pass (W1):** with equilibrium seeds, TV stays inside the null band at all four times. With seeds not in equilibrium, TV goes above the band at one time or more.
**Pass (W2), equilibrium part only:** with equilibrium seeds, TV stays inside the band at all four times. Nelson's dynamics also keeps |ψ|² as |ψ|² (equivariance), so equilibrium forbids signals in W2 as well.
**Report only (W2), seeds not in equilibrium:** Valentini's signal theorem is a result for pilot-wave theory. For W2, the test records what happens and sets no pass condition.

*This test checks known theorems. It cannot fail the position. A failure of the equilibrium part is a code error.*

### 5.5 What changed on 10 October, and why

| Change | Reason (published source) |
|---|---|
| Test 1a band for p: from −1 ± 0.2 to −1.05 ± 0.20 | TRV Table I gives p = −1.05 ± 0.03 at the grain this test uses |
| Test 1a: M = 4 reported, not fitted | TRV left it out; Abraham, Colin & Valentini 2014 show that a few modes can leave a residue that does not relax |
| Test 1b: τ_int defined by a formula | The paper defines it in words only; the literal definition gives the hardest test |
| Test 1b: second definition of τ_int changed (code check, before any run) | The first version (centre at half the highest peak) is already true at t = 0 for σ = 0.7, because the packets overlap |
| Test 2: W1 moved from the double slit to the box | 1D pilot-wave paths cannot cross, so W1 cannot relax in a 1D double slit |
| Test 2: ideal record, not the N-partner model | The ideal record is the limit case; a finite-rate record needs many particles (§8) |
| Test 2: a band for the time scale of TV, set from τ | For a small difference, TV ∝ √H̄ (Pinsker's inequality gives the bound TV ≤ √(H̄/2)); coarser regions relax faster (TRV Table II) |
| Test 3: a pulse in x₁², not a kick in x₁ | A kick in x₁ leaves particle 2's guidance unchanged in this state |
| Test 3: W2 equilibrium given a pass condition | Equivariance holds for Nelson's dynamics too (Nelson 1966) |
| Test 1a: step limit 0.02 → 0.01 → 0.005, step check 0.01 → 0.0025 (code checks, before any main run) | The equivariance check failed at 0.02 (H̄ of the Born start rose from 0.0012 to a maximum of 0.0035) and, by a small margin, at 0.01 (on average 2.4 floor deviations high, maximum 5.1 against the limit 5). The drift falls fast with the step |
| Test 1a: N = 10⁵ → 5 × 10⁴ for the main runs | Compute time at the shorter step. The equivariance check keeps 10⁵. The fit window changes little, because H̄ stays far above the floor for most runs |
| All tests: set-up checks added | Equivariance and step size are known properties; a code that fails them is wrong |

---

## 6. Kill conditions — set in advance

- **A rule needs a start spread that already equals Born.** That is fiat, as with Strubbe. That rule fails.
- **A set-up check fails** (equivariance, step size, the figure check, the closed forms). That is a code error. Fix the code before you read any pass condition.
- **Test 2 fails for a rule** (TV does not fall to the floor, or the time scale is outside the band). Then the "race" view of §9 fails for that rule, and point 3 of §9 must change.
- **Test 1b gives only a partial result.** Not a kill. Record that the published claim depends on the definition of τ_int.
- **One W1 phase set in Test 2 keeps a residue.** Not a kill, because the pass uses the median. Abraham, Colin & Valentini found such residues for a few modes. Report it.
- **Test 3, W1 seeds not in equilibrium, show no signal.** Not a kill. It is a code error or a pulse that is too weak. Check the code first.
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

Which rule nature uses: the two rules differ only out of equilibrium, and laboratory systems are already in equilibrium. A record that forms at a finite rate (the N-partner model): Test 2 uses an ideal, instant record, which is the limit case. The CMB calculation itself (Colin & Valentini did it in pilot-wave theory; RFF would need its own version). Gravity. Many particles beyond the two in Test 3.

## Sources

Listed in §3.
