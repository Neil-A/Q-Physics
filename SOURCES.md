# Sources

*Every paper, the question it was read for, the answer, and what it cost. PDFs in [papers/](papers/). All seven blocking papers read 5 August 2026 — nothing here is second-hand any more.*

**Status marks:** `[x]` read, question answered · `[~]` pulled, not read · `[ ]` unread.

**What the reading changed, in four lines:**
- Two hoped-for openings closed (§3, §4 below).
- One misattribution corrected — #1 is not Ellis's (§5).
- The Born fork settled by the scope cut rather than on the merits (§7).
- ~~**#14 survived everything.** It is the delta.~~ **It did not survive the simulation.** #14 survived all seven papers and then failed the L-sweep on 6 August ([RESULTS-01.md](RESULTS-01.md)). The delta is now #9 alone.

---

## Blocking — read

### 1. `[x]` Strubbe, "Crystallizing spacetime"
**arXiv:2505.10383 (2025)** · `papers/Strubbe-2025-Crystallizing-Spacetime.pdf`

A fixed 4D manifold whose metric and worldlines *relax* as a function of an external parameter τ, via a Ricci-flow-like equation; general relativity is the τ→∞ equilibrium. A crystallization hypersurface Σ(τ) with t_cryst = βτ separates formed worldlines from unformed. Particles are bundles of worldlines with influences running both ways along them. **The closest work in existence to this framework.**

**Q: does he *derive* the double-slit band heights, or fit them?**

**Neither — he assumes them, in the same place we do.** Each worldline loop carries an "excitation intensity" I. For the double slit his Eq. 17 gives

> I_k ≈ Σ_i Σ_j cos(φ_ik − φ_kj)

and he says outright that this **matches the standard path-integral expression |Σ_i e^{iφ_ik}|²**. The Born expression enters as the *definition* of the intensity. What he then genuinely derives (Eqs. 18–21) is that worldline density relaxes until ρ ∝ I — a real dynamical result, but it converts an assumed |ψ|² into a density rather than producing it.

The squaring arrives by the same move as ours: the coupling coefficient applied **once out and once back** around the loop. That is posit #12 in different notation, circular for the same reason. He doesn't notice.

**His EPR model settles it.** The outcome is decided by s_A = sgn(I_A − r_A|P_A|²), with **r_A a random number uniform on [0,1]**. The Born probabilities appear *because r is uniform*. Change the distribution, change the answer. That is Born-by-fiat wearing a hidden variable's clothes — and he selects the momentum-carrying worldline "randomly" in the double-slit model too.

**So the selection problem is not answered.** He walked up to the door and postulated a uniform measure on the other side.

**Q: what does τ do, and why does nothing detect it?**

**He answers this well and the answer is ours to take.** Observers are made of the same worldlines and can only record *equilibrated* configurations — pointer states that have stopped changing with τ. Equilibrium is τ-independent by construction, so **τ is unobservable in principle**, not hidden by a mechanism. And t_cryst = βτ makes clock time indirectly track τ, which is where the felt flow of time comes from.

**Three further takeaways:**
- **He contradicts #9 head-on.** Predicts you could extract which-slit information *gravitationally* without destroying interference, because only the momentum-carrying worldline gravitates. That makes gravity distinguishing; by our own resolution rule it would then resolve. Same experiment, opposite prediction.
- **His analogue of #14 has the structure but not the number.** Dynamics persist in a finite region behind the front — milliseconds deep in his EPR run — but the depth is set by free constants he says can be "tuned to make this dynamic region arbitrarily small." Ours was L/c, a physical distance. *(6 Aug: and ours has now failed its test, so this is no longer an advantage over him. Neither depth has a measured consequence. Do not use this contrast in the paper.)*
- **He criticises the transactional interpretation** for not explaining how bidirectional signals work in ordinary spacetime without an extra parameter. **That objection landed on us too — it no longer does.** *(Updated 6 Aug: this entry previously recommended adopting τ to answer it. **Reversed.** Confining the handshake to the front makes the round trip ordinary two-way propagation across a finite region, so no extra parameter is required — [FRAMEWORK.md §9](FRAMEWORK.md). Adopting τ would import prior art and add a postulate to buy something now free. Do not re-open this.)*

**Warning:** he brands the framework "fundamentally deterministic" and then uses random numbers in both models. That is our #15/#16 gap exactly. He got it past a referee; don't count on the same.

---

### 2. `[x]` Ellis & Rothman, "Time and spacetime: the crystallizing block universe"
**arXiv:0912.0808; IJTP 49, 988–1003 (2010)** · `papers/Ellis-Rothman-2009-Crystallizing-Block-Universe.pdf`

**Q: how precisely does he state the non-uniform crystallisation claim (#13)?**

**Credit confirmed, wording located.** His analogy is a crystallizing molten mixture in which *"some molten bits remain in the interstices to become fixed only later,"* and his Fig. 3 caption describes *"pockets of residue remaining behind for a time after the main resolution front has passed."* Large-scale structure crystallizes first, fine detail later.

**And #14 is not his.** He never says what *closes* a pocket, and gives no timescale. The mechanism and the L/c window are both absent. The two are cleanly distinguishable, which is what this reading was for.

**The bigger finding: posit #1 is misattributed.** Ellis & Rothman are arguing **against** the block universe. Their §5.3: other approaches *"assume that the future already exists... Our claim, by contrast, is that the future does not yet exist; at present the future is merely a set of possibilities."* Their whole arrow-of-time argument rests on it. Theirs is a **growing** block; ours is a **full** block.

Two further mismatches in the same direction: they take collapse to be irreducibly probabilistic (contra #15), and they explicitly reject integrating over the future *because it isn't there* — which cut at #11/#14, where a confirmation returns from an absorber.

*(Updated 6 Aug: the second mismatch is **answered**. Confining the handshake to the front means the absorber is inside the slab and nothing integrates over the far future, so the objection does not apply — [FRAMEWORK.md §7, §9](FRAMEWORK.md). The same move makes **#1 idle**: the misattribution below still stands as a fact about Ellis, but #1 is now a preference rather than a substrate, so nothing load-bearing rests on the disagreement.)*

**Usable patch he does offer — now held in reserve rather than needed:** keep a transactional or two-time formalism but impose the "final condition" at the **present** time rather than at the end of the universe, noting the mathematics doesn't care where the final state sits. *(Confining the handshake does this job already; keep this on record only in case the confinement is ever undone — [FRAMEWORK.md §9](FRAMEWORK.md).)*

**In fairness:** this is a *picture*, not a theory. He says himself there is no satisfactory measurement theory and promises a technical companion paper. Less here to be scooped by than assumed.

---

### 3. `[x]` Towler, Russell & Valentini, "Timescales for dynamical relaxation to the Born rule"
**arXiv:1103.1589** · `papers/Towler-Russell-Valentini-2011-Born-Rule-Relaxation-Timescales.pdf`
*(Author order corrected — earlier notes had "Valentini, Towler & Russell".)*

**Q: how fast does relaxation to |ψ|² go, and what delays or blocks it?**

**Fast.** Pilot-wave dynamics for an electron in a 2D box, started deliberately away from |ψ|². The coarse-grained H-function decays cleanly exponentially, and **τ ∝ M⁻¹** in the number of superposed modes — robust across every coarse-graining tested (indices −1.05 to −1.09). Physically that is **~10⁻²¹ to 10⁻¹⁸ s** for an electron.

**Mechanism:** wave-function nodes move around generating vorticity, making trajectories chaotic and stirring the densities ρ and |ψ|² until they're indistinguishable under coarse-graining. More modes → more nodes → faster.

**What blocks or delays it:**
- **Few modes.** At M=4 the timescale is wildly variable (τ = 980 ± 1600 in one case) — a single node's placement dominates.
- **Fine-grained microstructure in the initial condition.** Required absent, exactly as in classical statistical mechanics. An assumption, not a result.
- **Expanding space** — relaxation is suppressed for super-Hubble modes in the early universe. **The only regime where non-equilibrium survives.**
- **"Extended non-equilibrium"** (p ≠ ∇S, Bohm's second-order dynamics): may be unstable and not relax at all, which the authors take as an argument that de Broglie's first-order version is fundamental.

**Verdict: Born-by-relaxation is live, not a hope.** That was the thing to establish. But relaxation completes before anything measurable, and the only place to look for residue is cosmological — which we cut. **The fork is settled by the scope decision, not on the merits.**

**Citation note:** Valentini's own earlier estimate τ ∝ M⁻³ is superseded — it describes only the first instant, not the exponential tail where relaxation actually happens. Cite this paper's scaling.

---

## Needed for the thickness variable — read

### 4. `[x]` Baumgratz, Cramer & Plenio, "Quantifying Coherence"
**PRL 113, 140401 (2014); arXiv:1311.0275** · `papers/Baumgratz-Cramer-Plenio-2014-Quantifying-Coherence.pdf`

**Q: which measure — relative entropy of coherence, or l₁-norm?**

**Either.** Both are valid, both closed-form. Fix a basis; states diagonal in it are incoherent; a valid measure never increases under operations that cannot create coherence.

Three things that matter for the code:
- **The squared off-diagonals (l₂) are *not* valid** — monotonicity fails, with an explicit counterexample. It's the measure most people reach for first.
- **Maxima differ** (log d vs d−1) and coincide only for a qubit. Compare orderings, never magnitudes.
- **The maximally coherent state is the uniform superposition** — so thickness tracks amplitude balance, not just branch count.

**The catch the notes didn't have: the whole theory is finite-dimensional**, and the authors flag the infinite-dimensional case as not yet constructed. A particle's position isn't finite-dimensional. See [FRAMEWORK.md §3](FRAMEWORK.md).

---

### 5. `[x]` Streltsov et al., "Measuring quantum coherence with entanglement"
**PRL 115, 020403 (2015); arXiv:1502.05876** · `papers/Streltsov-etal-2015-Measuring-Coherence-with-Entanglement.pdf`

**Q: what is the bound on coherence→entanglement conversion, and when does it saturate?**

- **Theorem 1:** entanglement generated ≤ coherence of the input.
- **Theorem 2:** you can make entanglement this way **iff** the input is coherent.
- **The bound is attained** — an explicit generalised CNOT converts coherence into exactly that much entanglement, for relative-entropy and distillable entanglement. Their general measure is *defined* as a supremum, so it saturates by construction.

**Consequence, and it's the unwelcome one.** The hope was that a gap between coherence lost and entanglement gained was where the framework's content lived. The bound is **tight**, so a gap in any real evolution says only that the actual coupling isn't the optimal entangling operation — which it never is. **The gap measures suboptimality, not missing physics.**

**Silver lining:** "the front advances by converting coherence into entanglement" is now literally Theorem 2. Which is also the problem — it's a theorem someone else proved, with no ontology attached.

---

### 6. `[x]` Englert, "Fringe visibility and which-way information: an inequality"
**PRL 77, 2154 (1996)** — *paywalled, not on arXiv.* Two free substitutes pulled instead:
- `papers/Schwindt-Kwiat-Englert-1999-Quantitative-Duality-Experiment.pdf` (arXiv:quant-ph/9908072) — **Englert's own experimental test**, more useful than the original would have been.
- `papers/DeZela-2013-Comment-on-Englert-Inequality.pdf` (arXiv:1305.0861) — patches a technical hole in the 1996 proof. Conclusion unaffected; worth one line if the relation is cited in detail.

**Q: exact conditions for the gap in V² + D² ≤ 1 to be nonzero?**

**Answered completely:**

> **V² + K² = 2 Tr(ρ²) − 1**, where ρ is the state of the **interfering system** (the path degree of freedom).

*(Corrected 6 Aug after Test 4 — this entry previously read "the which-way marker." That is wrong in general. Checked over 8000 states: against the **path** purity the identity holds to 7×10⁻¹⁶ for pure and mixed joint states alike; against the **marker** purity it holds only when the joint state is pure, where the Schmidt decomposition forces the two purities equal, and fails by up to 0.61 otherwise. Cite it against the path state — see [RESULTS-01.md](RESULTS-01.md).)*

The gap is **exactly the impurity of that state**. Pure → saturation. Completely mixed → both sides collapse to zero. Nothing else enters, and it's confirmed to the percent level across pure, mixed and partially-mixed markers.

**So there is no gap to characterise and no mechanism to find.** Second of the two hoped-for openings, closed.

**Priority correction:** the relation is **not Englert's alone**. Jaeger, Shimony & Vaidman derived it first (PRA 51, 54, 1995); Englert independently a year later by a cleaner route. Earlier weaker versions (visibility vs *a priori* predictability) go back to Wootters & Zurek (1979) and Greenberger & Yasin (1988). **Cite Jaeger–Shimony–Vaidman alongside Englert.**

**Two side findings that bear on the framework:**
- **Distinguishability D is an optimum**, not a state property — D = max K over betting strategies. Same shape as Streltsov's supremum: tight by construction, which is why gaps in these quantities carry no content.
- **Non-erasing quantum erasure.** Interference is recovered from a *completely mixed* input, where there was no which-path information to erase. The eraser works by **sorting the run into sub-ensembles** — fringes and anti-fringes summing to nothing — and keeping one. It does not undo a record. This kills the "refillable vacancy" reading of the eraser and withdraws the old objection to the ember metaphor.

---

### 7. `[x]` Srednicki, "Entropy and Area"
**PRL 71, 666 (1993); arXiv:hep-th/9303048** · `papers/Srednicki-1993-Entropy-and-Area.pdf`

**Q: what's required for the area law — gapped, ground state, what else?**

Take a free scalar field in its ground state, trace out everything inside an imaginary sphere of radius R: **S = 0.30 M²R²**, proportional to *area*, not volume. The argument is short and good — tracing out the inside and the outside give the same eigenvalues, so the answer can only depend on the shared boundary.

**The old caveat was wrong.** Earlier notes hedged against "gapped ground states, with log corrections for critical systems." **Srednicki's field is massless — gapless — and the law is clean anyway in 3D.** The log correction is a **one-dimensional** phenomenon, and 1D is also the only case where the infrared cutoff enters the answer at all.

**What is actually required, and it's narrower:**
- Free field, ground state, flat space, static spatial region.
- **d = 3** for the R² law. d = 2 gives S ∝ R. d = 1 breaks the argument entirely. d ≥ 4 wasn't computed — the regularisation doesn't converge.
- **The coefficient depends on the UV cutoff and is not universal.** So "resolution rate scales with front area" comes with a prefactor set by unknown short-distance physics.
- Vacuum only. Nothing licenses excited or thermal states — which is every case the framework cares about.

Out of scope for SIM-SPEC-01 anyway. Don't let it carry weight in a write-up without all of the above stated.

---

## Context — optional

**`[ ]` Cramer (1986), Rev. Mod. Phys. 58, 647** — the transactional interpretation, original.
> Does he anywhere address what makes *one* transaction complete rather than another? If not, confirms the selection problem has been open since 1986. *(Strubbe's paper already implies the answer is no.)*

**`[ ]` Kastner, PTI** — the possibilist version, for the pre-spacetime ontology and how she handles absorbers.

**`[ ]` Zurek, decoherence and einselection** — Rev. Mod. Phys. 75, 715 (2003).
> Why the environment selects the pointer basis. ~~Promote to blocking if SIM-SPEC-01 Test 2 fails on basis choice.~~ **Not promoted — Test 2 passed on 6 Aug**, and passed in a way that removes the dependency: on the dephasing trajectory the which-path basis is the *maximising* basis over all bases, so thinness is basis-independent as a fact rather than as a consequence of einselection. Zurek is still the right citation for *why* that basis is the one nature picks, but he is no longer all that stands between #4 and "decoration." Stays optional.

**`[ ]` Philippidis, Dewdney & Hiley (1979), Nuovo Cimento B 52, 15** — the Bohmian double-slit trajectory computation.
> What does the calculation actually take as input? The benchmark for what "explaining the double slit" means.

---

## October 2026 — blocking for FRAMEWORK §14 item 7 (the conserved source)

**`[ ]` Tilloy & Diósi (2016), PRD 93, 024026; arXiv:1509.08705** — semiclassical gravity sourced by the record of spontaneous localization.
> How is the source written so that it is conserved and does not signal? Is the framework's light-cone update rule a version of it?

**`[ ]` Oppenheim, "A postquantum theory of classical gravity?" (PRX 2023); arXiv:1811.03116** — classical metric coupled consistently to quantum matter.
> Does the framework's rule map onto it? If so, prediction 1 is inherited from it rather than distinctive.

**`[ ]` Oppenheim, Sparaciari, Šoda & Weller-Davies (Nature Communications 2023); arXiv:2203.01982** — the decoherence–diffusion trade-off.
> What bound would an averaged-gravity framework have to meet, and has it been tested?

**`[ ]` León, Kraiselburd & Landau (2015), PRD 92, 083516; arXiv:1509.08399** and **`[ ]` León, Majhi, Okon & Sudarsky, arXiv:1712.02435** — blocking for §14 item 13.
> Semiclassical gravity with collapse suppresses primordial tensor modes. Which assumptions does RFF share, and does the UV-cutoff dependence carry over?

**`[ ]` Perez, Sahlmann & Sudarsky (2006), CQG 23, 2317** — collapse as the source of the scalar seeds.
> Can RFF's settling of the inflaton reproduce the observed scalar spectrum?

Jacobson (1995, 2016) and the gravity papers cited in [RESULTS-02-gravity.md](RESULTS-02-gravity.md) left the "not to read" list below when gravity-origin was reopened on 7 October.

**October 2026 — for SIM-SPEC-02 (amplitudes).** Full list and what each was read for: [SIM-SPEC-02](SIM-SPEC-02-amplitudes.md) §3. Still owed before any novelty claim:

**`[ ]` The Sorkin-school decoherence-functional literature** (Sorkin 1994 onward; Dowker, Johnston & Sorkin 2010; Boes & Navascués 2017; Dowker & Wilkes 2022) — read in full, not at abstract level.
> Has anyone derived the clock-hand rule from pairs + comparison by clock difference + strong positivity, via Herglotz/Bochner?

**`[x]` Joshi, Srikanth & Sinha, "Violation of no signaling in higher order quantum measure theories", Int. J. Quantum Inf. (2016), DOI 10.1142/S0219749916500246; arXiv:1308.6065.** *Read 10 Oct 2026.*
> Under what assumptions do higher-order sum rules permit signalling? If they hold in RFF, A1 (pairs) follows from RFF's no-signalling commitment.

**Answer: the assumptions borrow quantum theory, so this does not give RFF a reason for pairs.** The argument keeps the standard Hilbert-space state space (the theory must match QM for one and two slits, with "only the dynamical part altered") and changes only the probability rule. It then uses Gleason's theorem and the Hughston–Jozsa–Wootters steering result, in a two-party entangled protocol, to show that three-way interference would let one party signal the other. The proof is a sketch built on a worked 3 × 2 example. The authors limit their own claim ("our result does not rule out violation of higher sum rules"), and note that with non-Hilbert (L^p, p ≠ 2) state spaces Gleason fails and the argument does not go through. So: within quantum state space, pairs are forced by no-signalling. From no-signalling alone, they are not. This is the same borrowing REVIEW-03 found in A3's first justification.
> Side note: they also set to zero the small three-way term that standard QM itself predicts in real triple-slit set-ups from looped paths. Blocking a slit changes the boundary conditions, so the measured proxy is not exactly Sorkin's sum. A tiny measured three-way term would not by itself refute pairs.

**October 2026 — for SIM-SPEC-03 (selection).** Full list: [SIM-SPEC-03](SIM-SPEC-03-selection.md) §3.

**`[x]` Towler, Russell & Valentini (2012)** — entry 3 above. *Checked again 10 Oct 2026, for the set-up of Test 1a.* Table I gives p = −1.05 ± 0.03 at the coarsest grain (ε = 64) and −1.06 ± 0.18 to −1.09 ± 0.12 at the finer grains, from 6 phase sets for each point. M = 4 is not in the fit. They compute H̄ by backtracking from a 1024 × 1024 lattice, with Runge–Kutta–Fehlberg steps.

**`[x]` Hardel, Hervieux & Manfredi, Found. Phys. (2023); arXiv:2305.04084.** *Set-up checked 10 Oct 2026 (§4.1, Eqs. 10–14, Figs. 4–5).*
> Do Nelson trajectories that start at one point reach Born before the fringes form?

**Answer: yes, they say so for every σ/a from 0.2 to 0.7, but their τ_int has no formula.** They define τ_int in words ("the time when the first maximum appears in between the two original wavepackets"). Their τ_q is the tangent intercept of a fitted curve. In our run (RESULTS-04), τ_q changes by 2 to 2.5 times with the fit window, so the comparison depends on these definitions. Their Eq. 10 prints √(πσ) in the normalisation; the overlap factor shows that it must be √π·σ.

**`[x]` Abraham, Colin & Valentini, J. Phys. A 47, 395306 (2014); arXiv:1310.1899.** *Abstract read 10 Oct 2026.*
> Does relaxation always complete?

**Answer: not with very few modes.** In a 2D oscillator with 4 states, H̄ can keep a residue above 10% of its start for 50 periods, if the phases confine the paths. With 25 states, the decay is close to exponential.

**`[x]` Valentini, "Subquantum information and computation", Pramana 59, 269 (2002); arXiv:quant-ph/0203049.** *Abstract read 10 Oct 2026.*
> Is the race of Test 2 (a record before relaxation is not Born) already in the literature?

**Answer: in substance, yes.** Matter out of equilibrium gives statistics that are not Born, and it can send instant signals. RFF adopts this. The number that Test 2 gives (how far from Born, as a function of t_rec/τ) is a use of it, not a new result.

---

## Not to read

*(July list. Since 7 October, Jacobson is in use — see above.)* Emergent-gravity literature (Jacobson, Verlinde, Padmanabhan, Van Raamsdonk), holography and AdS/CFT, timeless programmes (Wheeler–DeWitt, Barbour, Page–Wootters), causal sets, eternal inflation.

All were touched during the July sessions and all are out of scope. Listed here so the decision doesn't have to be re-made each time one looks relevant. It will look relevant. It isn't.
