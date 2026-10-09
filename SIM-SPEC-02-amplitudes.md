# Sim Spec 02 — Do amplitudes come out of ordering?

*Written 9 October 2026, before any code. Purpose: attack the open problem behind the map items "Why amplitudes cancel" and "Born rule" (both marked **strains**), and the "granular spacetime" question of whether pairwise ordering connects to pairwise interference. Failure is a good outcome if it is clean.*

> **STATUS: assumptions A1–A5 accepted by Neil, 9 October 2026.** Test 1 code committed before its run: [sim/amplitudes/](sim/amplitudes/). Results in RESULTS-03 when run.

---

## 1. The target

Plainly: **why do alternative histories combine like clock hands, so that they can cancel, rather than like chances, which only add?**

It has two parts, and they have different status.

- **(a) What each hand carries.** Already answered on 4 October: each history's own clock reading, with both ends of the history fixed. Arrows built from those readings reproduce the double slit exactly (5.4 µm against the real 5.36 µm at 50 keV, correct scaling at 25/50/100 keV). This is Feynman's sum over histories (1948) seen through clocks. On a discrete front, the clock reading has a discrete counterpart: the number of links along a chain, which tracks proper time (§3).
- **(b) Why hands add and the result is squared.** Put in by hand on 4 October. Positive weights never made a dark band, at any rate and with any clock arrangement. **This is the open problem.**

The August version of the question — "what discrete feature of a causal order carries the phase?" — assumed the cancellation had to come from a count that comes in opposing flavours. §4 proposes a different answer: the count (links along a chain) supplies only the clock reading, and the cancellation is forced by comparing histories in pairs under positivity.

---

## 2. What is already established in the project

- Positive weights never make dark bands (4 Oct). With three particles, about a third of the weight had to be negative.
- Clock-reading arrows reproduce the double slit exactly; the observer's clock drops out (4 Oct).
- **Probability belongs to a pair of histories, scored by comparing their clocks where they meet; comparing readings means subtracting them** (two-ended picture, 4 Oct; FRAMEWORK §15).
- Interference only ever in pairs: no third-order interference for one particle (Sinha et al. 2010; Kauten et al. 2017); maximum order 2M for M particles (Pleinert et al. 2021). On the map as **fits**.
- Thickness = coherence, set by local coupling (August; sourced 9 Oct).

---

## 3. Prior art read for this spec

*Read at abstract level on 9 Oct unless marked. Every entry needs a full read before anything here is claimed in a write-up.*

| Work | What it does | What it means here |
|---|---|---|
| Sorkin, "Quantum mechanics as quantum measure theory" (1994), gr-qc/9401003 | A hierarchy of sum rules: level 1 is classical probability; level 2 contains quantum mechanics. The square follows from level 2 | RFF's "probability belongs to pairs" **is** level 2. The square is what pairs mean |
| Goyal, Knuth & Skilling, PRA 81, 022109 (2010), arXiv:0907.0909 | Assume each process is described by a **pair of real numbers**; symmetry rules then force complex arithmetic, Feynman's sum and product rules, and modulus-squared probability | A rival route to (b). Its "pair" is two numbers per history, not two histories per probability. Worth comparing, not merging |
| Dowker, Johnston & Sorkin, "Hilbert spaces from path integrals", J. Phys. A 43, 275302 (2010), arXiv:1002.0589 | Builds a Hilbert space from a decoherence functional. Requires **strong positivity**: every matrix D(αᵢ, αⱼ) positive semidefinite *(confirmed in the text, not only the abstract)* | Amplitudes exist if probabilities are pairwise and strongly positive |
| Boes & Navascués, PRA 95, 022114 (2017), arXiv:1609.09723 | Strongly positive decoherence functionals form a set that cannot be enlarged while staying closed under composition | Strong positivity = probabilities stay non-negative when a system is combined with any other independent system |
| Dowker & Wilkes, "An argument for strong positivity of the decoherence functional" (2022), arXiv:2011.06120 | Extends Boes–Navascués to infinite systems; strong positivity is the unique maximal set closed under tensor product | Same, more general |
| Joshi, Srikanth & Sinha (2016), arXiv:1308.6065 | Violating the higher-order sum rules permits signalling, under stated assumptions *(assumptions not yet read)* | A possible reason for pairs: no signalling. RFF already commits to "nothing signals" |
| Johnston, CQG 25, 202001 (2008), arXiv:0806.3083; PRL 103, 180401 (2009), arXiv:0909.0944 | Propagators on a causal set from sums over chains and paths, with a "hop" weight per link and a "stop" weight per element; agrees with the continuum retarded propagator | Prior art for counting along chains as the discrete carrier. Whether his weights are real, and where *i* enters, not yet read |
| Myrheim (1978); Brightwell & Gregory, PRL 66 (1991) | Proper time between two events is recovered from the longest chain between them | The discrete clock reading in §1(a) |
| Renou et al., Nature 600, 625 (2021), arXiv:2101.10873 | Real-number quantum theory is experimentally distinguishable from complex, and fails | Constrains §4's last step (complex vs real) |
| Anastopoulos (2003), gr-qc/0208031 | Argues complex phases are an irreducible ingredient of quantum probability | Opposing view: the phase cannot be derived |

**Not found:** a published derivation of the clock-hand rule from pairs + positivity + clock differences, as in §4. A short search turned up nothing. That is weak evidence; the Sorkin-school literature must be read before claiming novelty.

---

## 4. The candidate derivation

### Assumptions

- **A1 — Pairs.** Probability is built from pairs of histories: P(A) = Σ D(h, h′) over pairs h, h′ in A. *(RFF commitment, 4 Oct; Sorkin level 2; supported by the higher-order interference experiments.)*
- **A2 — Compare by subtracting.** For histories of one free particle, D(h, h′) depends only on the difference of their clock readings: D = f(n − n′), where n is the number of links along the history. The absolute reading never matters. *(RFF commitment, 4 Oct: "comparing readings = subtracting them". The observer's clock dropping out on 4 Oct is this condition.)*
- **A3 — Positivity survives composition.** Probabilities stay non-negative when the system is combined with any other independent system. By Boes–Navascués and Dowker–Wilkes this is strong positivity: every matrix f(nᵢ − nⱼ) is positive semidefinite.
- **A4 — Discreteness.** Clock readings are whole numbers of links.
- **A5 — One rate.** A particle of definite mass has a clock of definite rate.

### Result

A function on the whole numbers that is positive semidefinite in this sense must, by **Herglotz's theorem**, be a positive mixture of pure rotations:

  f(n) = ∫ e^{inθ} dμ(θ), with μ a positive measure on the circle.

(The continuous version is Bochner's theorem.) Substituting into A1:

  **P(A) = ∫ dμ(θ) |Σ_{h∈A} e^{iθ n(h)}|²**

With A5, μ is concentrated at one angle θ, and this is exactly **"each link turns the hand by θ; hands add; the result is squared."** θ is set by the mass (θ = m × link length / ħ in natural units).

### How to read it

- **The cancellation is not put in.** It is what a sharp clock rate means, once probabilities come in pairs and stay positive under composition.
- **μ is a dial from quantum to classical.** One angle: full interference. Angles spread evenly around the circle: f(n) = 0 for n ≠ 0, so histories with different readings never interfere — classical, additive probability. In between: partial fringe visibility, equal to |f(Δn)|. This reads decoherence as a spreading of the clock rate, which should connect to "thickness = coherence, set by local coupling" (to be checked, Test 3).
- **The square is the pairing.** A1 is where the Born square comes from. What remains put in is A1 itself — why pairs and not triples — and A3.
- **The August question changes shape.** No count has to come in opposing flavours. The count (links along a chain) gives the clock reading; positivity over pairs supplies the turning.

### Possible circularity — to be checked before claiming anything

- Does A3 smuggle in a Hilbert space? Strong positivity is what *permits* one (Dowker–Johnston–Sorkin), and is justified independently by composition. It does not mention phases, and real-valued and classical theories satisfy it. Judged not circular, but this is the first thing a referee would press.
- Does A2 smuggle in the phase? It says only that comparison depends on the difference of clock readings. A constant f (no cancellation) satisfies it. Judged not circular.
- Complex or real? A real f (μ symmetric, giving cos θn) and a complex f (one angle) give identical single-particle probabilities. They differ only in multi-party networks, where experiment (Renou et al. 2021) favours complex. Out of scope here; flagged.

---

## 5. Tests — specified in advance

### Test 1 — Are link counts good enough clocks? *(the real test)*

**Question:** On a random discrete spacetime, does the link count along each history carry the phase well enough to give the right double-slit pattern?

**Model.** Poisson sprinkling at density ρ in a 1+1 region. Source event at the bottom; two slit regions at a fixed later time, separated by d; a row of screen events at a later time. For each screen point and each slit, the clock reading n is the longest chain from source to screen through that slit. Probability per screen point: |e^{iθn₁} + e^{iθn₂}|², with one θ set by the mass. This is the discrete version of the 4 October calculation (two stationary histories, both ends fixed).

**Prediction from the continuum.** The longest chain in a 2D causal interval of volume V is about 2√(ρV), so the clock estimate is τ̂ = n / √(2ρ). The pattern should converge to the continuum one, |e^{imτ₁} + e^{imτ₂}|² with proper times τ, as ρ grows. Chain-length fluctuations grow as N^{1/6} (N = number of elements), so phase error should fall as ρ^{−1/3}.

*Checked 9 Oct (scratch run, 40 sprinklings each):* longest chain / √N = 1.85, 1.91, 1.96 at N = 10³, 10⁴, 10⁵, approaching 2 slowly; spread / N^{1/6} ≈ 0.9 at all three. The slow approach biases the clock scale by a few per cent at accessible densities, which would shift fringe spacing by the same amount. **So the clock scale is calibrated on independent sprinklings at each density before spacing is scored**, the way a real clock is calibrated before use.

**Metrics.** For each sprinkling (one sprinkling is one actual spacetime, so no averaging inside a run): correlation between the discrete and continuum patterns; fringe spacing; RMS phase error. Then trends over ρ, with 20 sprinklings per density.

**Pass:** correlation rises toward 1 with density; fringe spacing converges to the continuum value within 2% at the highest density; RMS phase error falls with exponent −1/3 ± 0.08.
**Fail:** correlation does not improve with density, or spacing converges to a wrong value. Then link counts are not the clock, and §1(a) has no discrete carrier.

### Test 2 — Is positivity doing the work?

**Question:** Does a comparison rule that depends only on clock differences, but is not positive semidefinite, produce negative probabilities, and only in composition when not alone?

**Model.** Random families of f on the integers (finite Fourier series with some negative coefficients, and short-range kernels such as f(0) = 1, f(±1) = a). For each, search random sets of histories alone, then composed with an independent second copy, for P < 0.

**Pass:** every non-positive-semidefinite f yields a negative probability somewhere, at least once composed; every positive semidefinite f never does. Records which kernels fail only under composition; that is the case where A3 is the deciding assumption.
**Fail:** a non-positive-semidefinite f survives composition with no negative probability. Then A3 is not justified by composition alone.

*This is a check of the theorem and of the composition argument, not new physics. It costs little.*

### Test 3 — Spread rate = decoherence?

**Question:** Does spreading μ reproduce the dephasing behaviour already measured in RESULTS-01?

**Model.** Take the RESULTS-01 dephasing results: the Test 1 dephasing sweep, and the Test 2 central-spin model where log-coherence falls linearly with the number of coupled environment parts (slope −0.81). Fit a μ of width σ whose visibility |f(Δn)| matches the measured coherence at each point.

**Pass:** a single family of μ fits both, with σ growing monotonically as coupling accumulates.
**Fail:** no such family exists. Then "decoherence = spreading of the clock rate" is a slogan, not a reading.

*Consistency check only; it cannot fail the derivation.*

---

## 6. Kill conditions — set in advance

- **The original null (set 9 Oct): every candidate needs the phase rule added by hand.** §4 passes this only if A1–A5 contain no phase rule in disguise. If review finds one, the derivation is circular: **fail.**
- **Test 1 fails:** link counts cannot carry the phase. The derivation may survive, but its discrete carrier does not, and "what in the ordering is the clock" reopens.
- **Already published:** not a kill. RFF adopts the published version and cites it; the map item moves without a novelty claim.
- **A1 stays unexplained:** not a kill. It becomes the single named input of the quantum column, with Joshi–Srikanth–Sinha (no signalling) as the lead to check.

---

## 7. What it would change on the map

| Item | Now | If §4 holds and Test 1 passes |
|---|---|---|
| Why amplitudes cancel | Strains | Fits with work: cancellation derived from pairs + positivity + one clock rate |
| Born rule | Strains | Fits with work: the square is the pairing (A1); why pairs remains |
| Interference only in pairs | Fits | Fits; becomes the load-bearing input (A1) |
| Granular spacetime | Fits with work | Fits with work: link count is the clock; pairwise comparison carries the phase |

---

## 8. Out of scope

Selection (#10, #16); complex vs real in networks; spin and the Dirac equation (the checkerboard's domain); many particles; gravity. Nothing here depends on the conserved-source gate.

## Sources

Listed in §3. Abstract-level reads only, except Dowker–Johnston–Sorkin's positivity condition, which was checked in the text.
