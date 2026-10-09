# Review 03 — amplitudes from ordering (independent)

*Received 9 October 2026, in response to [REVIEW-BRIEF-03-amplitudes.md](REVIEW-BRIEF-03-amplitudes.md). Reproduced as received. The project's response is in [RESULTS-03-amplitudes.md](RESULTS-03-amplitudes.md), "Review outcome".*

---

The derivation fails the brief's first kill condition. The failure is in the justification of A3, which borrows a quantum system. A2 and A5 do not hide the clock-hand rule, and the Herglotz step itself is right. The three tests are honest and stay inside what they can show.

1. Is a phase rule hidden in A1–A5?

A3 — the justification borrows quantum theory. Spec §4, line 67, says that probabilities staying non-negative under composition with any other independent system is strong positivity, "by Boes–Navascués and Dowker–Wilkes." That is stronger than either paper.

Boes and Navascués (PRA 95, 022114, 2017) prove two different things. The set of strongly positive decoherence functionals cannot be enlarged and stay closed under composition. Separately, any composition-closed set that already contains all quantum decoherence functionals can contain only strongly positive ones. The second theorem is the one that forces strong positivity on a theory, and its witness is a quantum system: their Lemma 3 builds, for any functional that is not strongly positive, a quantum functional with two settings whose composition gives a negative probability. A copy of the system itself is not enough. They also show that for every n there is a functional that survives n−1 copies of itself and fails at the next copy.

Dowker and Wilkes (arXiv:2011.06120) do not remove that dependence. After proving that strong positivity is closed under tensor product, the paper says that closure is not enough to pick it out: positive-entry functionals (real and non-negative) and classical functionals are also closed. Their uniqueness theorem (Theorem 3) is that the strongly positive systems are the only set that is both tensor-closed and Galois self-dual. The proof that the dual of the strongly positive set is itself composes against quantum Gram matrices. The spec's prior-art table (§3) quotes the abstract's "unique maximal set" and misses that condition.

Test 2 is this theorem in numbers. Of 22 non-positive rules caught only under composition, the qubit with amplitudes (1, −1) caught all 22 and a second copy caught 1 (test2_positivity.py lines 14–17; test2_console.txt, the copy column; K3 #13 is the one copy catch). A rule such as f(±1) = 0.8 has every term positive when counts are non-negative, so it looks harmless alone and under a copy, and it breaks only on meeting a system that already interferes. Strong positivity is what lets Dowker, Johnston and Sorkin build a history Hilbert space (arXiv:1002.0589). Justifying it by composition with a qubit assumes a quantum system in order to explain the phase structure of a quantum system.

A2 — no hidden phase rule. "D depends only on n − n′" (spec §4, line 66) is invariance under a shift of the zero of the clock. A constant satisfies it, and so does a kernel with no cancellation. The phases appear later, as the characters of the integers, once positive-definiteness is added. That is the content of Herglotz, not a phase already sitting in A2.

Equal weights are a real limit on the claim. Because D is a function of the difference alone, every history has the same magnitude and histories differ only by an integer reading. Ordinary quantum mechanics also has path-dependent magnitudes. For two stationary histories of one free particle the magnitudes are nearly equal, which is the scope the spec and Test 1 actually use. The argument does not deliver the general path-integral weight.

A5 — no hidden phase rule. Herglotz already gives a mixture, P(A) = ∫ dμ(θ) |Σ e^{iθ n(h)}|², before A5 is used (spec lines 73–81). A5 sets μ to a single angle. A spread-out μ, which the same assumptions allow, washes the fringes out. Sharpness is what keeps the cancellation, and it is a statement about a particle of definite mass, not the addition rule typed in again. For one particle a single angle θ and the real pair ±θ give the same probabilities, so A5 is stronger than one-particle data. The spec already says they come apart only for several parties (line 94).

2. Is the mathematics right?

Agree.

Herglotz applies as used. A function on the integers whose matrices f(n_i − n_j) are all positive semidefinite is the Fourier transform of a positive measure on the circle. Substituting into A1 gives the modulus-squared formula, for histories counted with equal weight. A real kernel, from a measure symmetric under θ → −θ, and a single complex angle give the same one-particle probabilities, because |Σ e^{iθ n}|² = |Σ e^{−iθ n}|². They differ when several parties are composed. Test 2 checks real symmetric kernels only (test2_positivity.py line 4), so the complex half of the theorem is not in the numerical evidence.

3. Is it already published?

Not this argument. I did not find a derivation that starts from a difference of clock readings plus strong positivity and arrives at e^{inθ} per link through Herglotz or Bochner, in Sorkin, Dowker–Johnston–Sorkin, Gudder, Anastopoulos, or Hartle, or under a search for that combination.

The nearest published derivation of complex amplitudes, addition, and the square is Goyal, Knuth and Skilling, PRA 81, 022109 (2010). It assumes a pair of real numbers per sequence of outcomes and gets Feynman's rules from symmetry. The spec already lists it as a rival route (§3). Dowker, Johnston and Sorkin (2010) go from strong positivity to a Hilbert space, which is amplitudes existing as vectors, and they do not derive the clock phase. Sorkin's level-2 sum rule is the square for pairs, which is A1, not the phase. If a later full read of Gudder or Hartle turns up this Herglotz argument, the spec's own rule applies: adopt that version and cite it.

4. Is Test 1 a fair test?

Agree.

The calibration is a single monotone map, n = aτ + bτ^{1/3} + c, fitted on straight chains along the axis and applied to chains that bend at a slit (test1_link_clock.py lines 53–70, cs.py lines 149–168). It cannot absorb the slit geometry. The raw clock τ̂ = n/√(2ρ), with no fit, gives correlation 0.945 and spacing 0.980 at ρ = 10⁷, against 0.946 and 0.981 for the calibrated clock (test1_console.txt). The pass does not depend on the fit.

The continuum reference, the maximum of τ(source, p) + τ(p, screen) over the slit slab, is the right comparison for two stationary histories. Using only the longest chain, in 1+1, is exactly the scope the results claim, and it does not test a sum over all chains.

The spacing bias is plausible and unchecked, as RESULTS-03 says (the paragraph after the follow-up table). The ratio moves from about 0.96 at ρ = 10⁶ to 0.981 at 10⁷ and 0.991 at 3×10⁷, and a ρ^{−1/3} finite-size correction to chain length would move it that way. The follow-up's own repeat at 3×10⁶ landed at 0.971 against 0.980 in the main run, so the fitted exponent ρ^{−0.42±0.08} is rough. The direction, toward 1 at higher density, is what the committed output shows.

5. Does the write-up claim more than the evidence?

Agree on Tests 1 and 2. Disagree on one Test 3 bullet.

The committed consoles match the summary table. Test 1: correlation rises at every density, spacing 0.9811 at ρ = 10⁷, RMS exponent −0.287 ± 0.012 inside the pre-registered −1/3 ± 0.08. The table's ± values are standard errors; the console prints standard deviations. Test 2: 83 kernels, 52 not positive semidefinite, 52 caught, 22 only under composition, 0 of 31 positive semidefinite kernels ever negative.

Both post-launch changes are recorded and point the right way. Dropping ρ = 10⁴ happened because a slit was empty, before any metric (test1_link_clock.py lines 30–34). Strengthening Test 2's search, and giving kernels their own random stream, made a miss harder to keep; the two kernels the first run missed were put back in and are now caught (K3x in test2_console.txt).

Test 3 could not fail. Part A sets g = arccos(1−p), so |cos g| equals the target visibility by algebra (test3_spread_rate.py lines 14–16). Part B regenerates the August central-spin draws and checks that a product of cosines equals the characteristic function of a sum of random signs, to 10⁻¹⁶. The slope −0.8097 is that regeneration. The sentence in RESULTS-03 that calls this a known identity is right. The bullet "Decoherence is exactly a spread of clock rates" under "Established, by test" states the reading as if the test had been able to refuse it.

The rest of "What this establishes" matches the evidence, including the explicit statement that circularity and novelty are still open. The proposed map move to "fits with work" waits on a justification of A3 that does not compose against a qubit.