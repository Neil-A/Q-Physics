# Review 04 — the repaired amplitude argument (independent)

*Received 9 October 2026, in response to [REVIEW-BRIEF-04-amplitudes-repair.md](REVIEW-BRIEF-04-amplitudes-repair.md). Reproduced as received. The project's response: [SIM-SPEC-02 §9](SIM-SPEC-02-amplitudes.md), "Review outcome".*

---

The repair holds. Theorem 4 is used correctly, and a dark fringe does not put the phase rule back in by hand.

1. Theorem 4 — applied correctly

Dowker and Wilkes, Theorem 4, says exactly what §9 says: a tensor-closed set of systems lies wholly in the strongly positive set S, or wholly in the positive-entry set R⁺. No Galois self-duality, and no need for a quantum system to be in the set already. Their Corollary 3 is the other half: anything outside both S and R⁺ eventually produces a negative probability when copied enough times, so it cannot sit in a tensor-closed set.

A dark fringe means Re D(A, B) < 0 for some disjoint pair, so that system is not in R⁺. One member outside R⁺ means the whole set is not inside R⁺. Theorem 4 then puts every physical system in S, including a free particle compared by clock differences. Putting the fringe and the free particle in one set is just A3′. That is the right hypothesis for the theorem.

The free-particle kernel counts as one of their systems only once it is Hermitian, weakly positive, and normalised, D(Ω, Ω) = 1, on an event algebra. For a finite set of histories that is easy: scale the matrix. §9 never checks it. For every chain at once, the sum over histories need not be finite, so that object is not yet one of their systems. The argument as written covers finite experiments. The infinite history space is still open.

2. E1 — observation, and not circular

One negative interference term is weaker than a quantum system. It does not supply amplitudes, a Gram matrix, or a turn per link. The old failure was composing against a qubit that already had those. A dark fringe does not.

The original target asked why histories cancel at all. E1 makes that existence an input, and the argument derives only the form. That is what §9 claims, and it does not trip the kill condition, which was about adding the phase rule by hand. The line "no theory attached" is a little strong: reading the fringe as Re D < 0 uses the pair formula, which is A1, already a named input. It still does not assume the clock-hand rule.

3. A3′ — agree, not a borrowing

"Any two independent systems combine, and the joint probabilities stay non-negative" is a physical requirement of its own. The product rule D₁₂ = D₁ ⊗ D₂ is the ordinary rule for independent systems, and classical probability uses it too. It does not hide phases. It is a real assumption: some other combination rule would put the systems outside the theorem.

4. Steps 3–4 — agree

Strong positivity on single histories makes every matrix f(nᵢ − nⱼ) positive semidefinite, for readings that actually occur. A finite positive semidefinite Toeplitz matrix is the moment sequence of a positive measure on the circle. That measure is not unique; A5 is what picks one angle. Herglotz covers the case where every difference occurs.

5. The claim — agree, with two omissions

The claim matches the argument: if something somewhere cancels, and all systems combine, then every clock-difference comparison is clock hands squared. It does not explain why anything cancels.

The named inputs are short A4, that readings are whole numbers. Normalisation, above, should be stated as a limit. The limits carried over from REVIEW-03 are stated correctly: equal weights only, and one particle cannot tell a real kernel from a complex one.

6. Published — not this combination

Dowker and Wilkes stop at strong positivity. They do not mention Herglotz, Bochner, or a phase per link. I did not find anyone else joining their Theorem 4 to an observed fringe and then to e^{inθ}. Same limit as last time: this was a search of that combination, not a page-by-page read of the whole histories literature.

This still does not derive amplitudes from ordering. Ordering remains the clock. What is new, and what the repair actually shows, is that the form of the phase follows from cancellation existing somewhere, plus combinability, plus comparison by clock differences.
