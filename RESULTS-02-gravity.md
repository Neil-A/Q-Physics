# Results 02 — Gravity via the area law

*Run 7–8 October 2026; re-run inside this repository on 8 October to confirm the numbers. Code in [sim/gravity/](sim/gravity/), raw output in `sim/gravity/results/`. Stack: Python 3.13, NumPy, SciPy (pinned in [sim/requirements.txt](sim/requirements.txt)); no QuTiP needed.*

**Headline** *(rewritten 8 Oct after [REVIEW.md](REVIEW.md) v4)*: The old mechanism, "mass slows time because resolution takes time to process," is dead: it fails reach, universality and light bending. On a lattice, a free scalar field obeys the known entanglement first law (dS = 2π × weighted energy change) in 1D, and in 3D once the improved energy density and the Wald surface term are included; without them it fails. This is a check of Jacobson's ingredient for a free field, not a derivation of gravity from the resolution front. **G is not derived. Local equilibrium is not proved.** Tests 2 and 4 reproduce textbook formulas that kill the old mechanism; any route that yields Einstein's equations passes them. The framework's own addition is a coupling rule: gravity follows the average energy of an unsettled mass, and the settled outcome once records can meet. That rule does not yet have a conserved stress tensor ([FRAMEWORK.md](FRAMEWORK.md) §14 item 7), and the gravity reopening stands or falls on it.

**Context.** Gravity-origin was cut in July (§12 of [FRAMEWORK.md](FRAMEWORK.md)). On 5 October the scope widened to "how much known physics fits," and on 7 October Neil reopened gravity-origin through the area-law route, with four tests set in advance: direction, reach, universality, light bending.

---

## Summary table

| What ran | Question | Result |
|---|---|---|
| Step 0 | Does the framework supply Jacobson's ingredients? | Four of six outright; the area law in part; a story for the equilibrium assumption |
| Lattice, 1D horizon | Does a region's entanglement change by 2π × distance-weighted energy change? | **PASS** — within 1% in 28 of 34 cases (3 masses, 2 kinds of nudge) |
| Lattice, 1D small ball | Same, for a short interval of a massless field | **PASS** — 0.98–1.01, sizes 8 to 256 sites |
| Lattice, 3D small ball | Same, in three dimensions | **PASS with improved energy + Wald surface term** — median 0.978–0.985, floor 0.64–0.72 (where the wave sits mostly inside the ball and dS is tiny); plain energy density fails completely (median ≈ −0.016) |
| Test 1, direction | Does mass slow clocks without contradicting "dense matter settles fast"? | Argument, no script. Consistent |
| Test 2, reach | Does slowing reach through empty space? | Textbook GR profile vs a local-load step function: **the local-load rule fails**. Galileo cited, not computed |
| Test 3, universality | Do all clocks slow identically? | Argument, no script. Passes by construction (couples only to energy); **the local-load rule fails** |
| Test 4, light bending | Full bending, not half? | Ray trace reproduces 1.751″ vs time-only 0.876″: **the local-load rule fails**. Cassini cited, not fitted |

*Tests 1–4 kill the old mechanism. They are not evidence for the area-law route over any other route to Einstein's equations.*

---

## Step 0 — Jacobson's argument, ingredient by ingredient

Jacobson (1995) derives Einstein's equations from two assumptions: entanglement entropy across any small horizon is proportional to its area, and energy crossing it changes that entropy like heat at the Unruh temperature (δQ = T dS). Demand this for every local horizon and spacetime must obey Einstein's equations, with Λ as a free constant and G = 1/(4ħη), where η is the area law's strength. The 2016 version ("entanglement equilibrium") uses small balls instead of horizons; it is fully worked out for conformal fields and rests on a conjecture otherwise.

| Ingredient | Does the framework supply it? | Note |
|---|---|---|
| Local horizons everywhere | Yes | From c as the rubber's rate |
| Area law | Partly | §6; established for empty space; η is not universal, so **G is an input** |
| Unruh warmth (Bisognano–Wichmann) | Yes, by inheritance | Checked on a lattice below |
| Local equilibrium | A story, not a proof | Every fold eventually closes, so settled rubber relaxes to balance |
| Energy in the rubber | Yes | Particles as patterns carry energy |
| Area change from focusing (Raychaudhuri) | Yes, by inheritance | Geometry of light rays |

---

## The lattice — the 2π rule in empty space

**Model.** A chain of coupled oscillators (lattice free scalar field), ground state as the vacuum. A region is either everything beyond a cut (a horizon) or a short stretch (a small ball). Nudge the field locally, recompute the ground state, and compare the change in the region's entanglement entropy, dS, with dK = Σ β(x) d⟨h(x)⟩, where β is the Bisognano–Wichmann weight: 2π × distance from the cut for a horizon, 2π (x−a)(b−x)/(b−a) for an interval.

**Sanity check.** Against the lattice's exact modular operator (not the 2π formula), dS/dK = 1.0000 and 0.9975 for the two reference cases. The pipeline is sound.

### 1D horizon — `rindler_scan.py`

| Mass (lattice units) | On-site nudge: ratio, out to 2.4 correlation lengths | Stiffness nudge: ratio |
|---|---|---|
| 0.05 | 0.9934–0.9998 | 0.9957–0.9996 to 0.8 ξ; 0.82 at 2.4 ξ |
| 0.10 | 0.9930–0.9994 | 0.9959–0.9993 to 1.2 ξ; 0.95 at 2.4 ξ |
| 0.20 | 0.9911–0.9975 | 0.9849–0.9974 |

On-site nudges stay within 0.9% everywhere. Stiffness nudges stay within 0.5% out to 0.8 correlation lengths, then drift. **The drift is lattice error, not physics:** deep inside the region the true entanglement change is exponentially small, and the lattice's discretised energy density dominates once both numbers shrink. Jacobson's argument works at the horizon, where the rule holds.

### 1D small ball — `first_law.py`

Massless chain, stiffness nudge scaled with the interval: ratio 1.013, 1.010, 1.009, 1.008, 1.003, 0.983 for sizes 8, 16, 32, 64, 128, 256. dS is the same at every size (4.0 × 10⁻⁵), as a scale-free field should give. The slight drift at the largest size grows with chain length, pointing to the massless 2D field's known long-wavelength quirk.

### 3D small ball — `ball3d_squeeze.py`, `ball3d_fit.py`

Partial waves (Srednicki's method); one smooth spherical wave squeezed, straddling the ball's edge.

| Ball radius (sites) | Plain energy density: median ratio | Improved energy + Wald surface term: median ratio |
|---|---|---|
| 16.5 | −0.015 | 0.978 |
| 32.5 | −0.016 | 0.984 |
| 64.5 | −0.016 | 0.985 |

A free three-coefficient fit over 54 configurations (Laplacian term, volume integral, surface integral) returns −0.168, −0.00009 and 1.056, against theory's −1/6 (−0.167), 0 and 2π/6 (1.047), max residual 0.33%. The volume coefficient landing on zero is the strong part: the lattice asks for the two corrections the conformal/Wald analysis already contains, and no third. The fit is scored on the same 54 configurations it was fitted to. In words: **dS(lattice) = 2π × (improved energy change) + 2πξ ∮ d⟨φ²⟩**, with ξ = 1/6. The surface term is the Wald entropy term for this field, the same kind that appears in black-hole entropy, and it is exactly what Jacobson 2016's "conformal fields only" caveat is about. Ratios drop (to 0.64) only where the wave sits mostly inside the ball and dS is tiny.

**Two discarded first attempts, recorded.** (1) Mass nudges on a massless 1D chain are swamped by the longest-wavelength modes. (2) A mass-term nudge in 3D changes short-distance structure; its energy response grew with the cutoff (`ball3d.py`'s own run). Both replaced as described.

---

## Tests 1–4 — `tests_2_4.py`

| Test | Area-law route | Resolution-load mechanism | Measured |
|---|---|---|---|
| 1. Direction | Pass: gravity sourced by energy, not settledness | Fail: predicts slow settling near mass; the framework says dense matter settles fast | Gravity's time dilation speeds settling (Pikovski et al. 2015), the same direction |
| 2. Reach | Pass: slowing falls off as 1/distance through empty space | Fail: stops at the surface | Galileo eccentric orbits: redshift matches GR to (0.19 ± 2.48) × 10⁻⁵ |
| 3. Universality | Pass by construction: couples only to energy | Fail: depends on what is being resolved | MICROSCOPE: η = (−1.5 ± 2.3 ± 1.5) × 10⁻¹⁵; JILA: redshift across a 1 mm cloud of clock atoms |
| 4. Light bending | Pass: 1.751″ | Half only: 0.876″ | Cassini: γ = 1 + (2.1 ± 2.3) × 10⁻⁵ |

Gravity's share of the GPS clock offset comes out at 45.7 µs/day. A hollow shell with Earth's mass at Earth's radius slows clocks inside by 7.0 parts in 10¹⁰ with no pull.

**Correction recorded 7 Oct.** The first draft of test 3 argued from the JILA cloud that "unsettled things don't slow clocks." Neil pointed out that every atom in the cloud is equally unsettled, so that effect would cancel in the comparison. He was right: JILA does not test it directly. The universality argument stands on the other measurements.

---

## What the framework adds, and the decisions taken (7–8 Oct)

**Resolution rate has two meanings.** (a) How fast the front advances: the local clock rate. (b) How much settles per tick. Neil: the front advances by settling. Near mass, the rubber's shape slows the front and everything on it by the same factor, settling included; the cause is the place, not the settling load. Dense matter: many records per tick, slow ticks. At balance the product is fixed (gravitational redshift; Tolman–Ehrenfest).

**Gravity follows the settled outcome.** Applied to quantum states, Jacobson's route gives Einstein's equations sourced by the average energy (Dorau & Much 2025). Because folds really close, once a record forms only one outcome exists, so gravity follows it, consistent with Page & Geilker (1981).

**Decided 8 Oct: an unsettled mass gravitates by its average.** Neil's reasoning: a system forced to an interim value returns the net. Consequences, all accepted:

- **Gravity is never quantum** in this framework: it is the rubber's equation of state.
- **Prediction 1:** BMV-type experiments will see **no entanglement through gravity**. Wavefunction-sourced gravity produces none (Struyve 2025). Aziz & Howl (Nature 2025) argue classical gravity could still entangle indirectly, but expect it far too small for near-future experiments. None has been done.
- **Prediction 2 — committed 8 Oct, derivation owed.** Neil chose the broad meaning of "gravity is never quantum": there is no quantized metric anywhere. Then there are no vacuum ripples of spacetime, and the inflaton's fluctuations gravitate only by their average, which is uniform, until they settle. Tensor modes (primordial gravitational waves) appear only at second order, after settling, and are **strongly suppressed** relative to standard inflation. This is the published result of semiclassical gravity with wavefunction collapse: León, Kraiselburd & Landau (2015) and León, Majhi, Okon & Sudarsky (arXiv:1712.02435); Perez, Sahlmann & Sudarsky (2006) for the scalar seeds. **Owed:** the derivation inside RFF, and a check that settling of the inflaton gives the observed scalar spectrum (otherwise the commitment removes the seeds of galaxies). **What can kill it:** a detection of primordial tensor modes at the level standard inflation predicts for the same inflaton. A non-detection at σ(r) ~ 10⁻³ settles nothing. León et al. note their estimate depends on a UV cutoff. *(Parked earlier on 8 Oct after [REVIEW.md](REVIEW.md) v4, because it does not follow from prediction 1 alone; restored once the broad meaning was chosen.)*
- **Side effect:** a spread-out heavy mass feels its own averaged pull (Newton–Schrödinger). Not collapse, but a departure from plain quantum mechanics. **Not yet priced for any system;** "small" is unverified, and for a BMV mass pair it depends on the wave-packet width.

**The signalling worry, and its answer.** Averaged gravity plus real settling could let a distant observer see a pull jump from "middle" to "side" when someone elsewhere looks. Neil (8 Oct): until the records can meet, the system has not truly resolved. Recorded as: **results become facts across regions only when records can meet, at light speed or slower.** A distant mass keeps pulling from its average until news of a look could arrive. This also explains why entanglement can't signal. Remaining: check the published work on locally sourced averaged gravity, mainly the moment a distant pull updates.

**Open, and the gate for the reopening (8 Oct).** The rule above is a rule for observers, not yet a stress tensor. Einstein's equations need a conserved source (∇·T = 0). A source that jumps from the average to one outcome must say what it is at events the record has not yet reached. Three readings: (1) ⟨T⟩ until the record's light cone arrives, then a jump — conservation must be shown; (2) the outcome all along — puts the result in the field before the record exists, and lets a test mass read it early (signalling); (3) some other structure carries the difference. Reading 3 has worked examples to start from: Tilloy & Diósi (2016) and Oppenheim's postquantum classical gravity (2023). If no conserved source can be written, gravity-origin is parked again and #9 stays as a semiclassical bet.

---

## Caveats

- The 1D results are one space dimension; the 3D result covers a small ball. A 3D horizon splits into independent 1D waves (one per sideways momentum, each a 1D field with a larger mass), so it is covered wave by wave by the 1D horizon runs; it was not run separately.
- G is not predicted. Λ is a free constant in this route.
- Not opened during the work, so treat as approximate: Srednicki 1993 (rate-limited), Page & Geilker 1981 (blocked), the BMV mass scale.

## Reproduce

```bash
cd sim/gravity
python first_law.py && python rindler_scan.py && python ball3d_squeeze.py && python ball3d_fit.py && python tests_2_4.py
```

About a minute. See [sim/gravity/README.md](sim/gravity/README.md) for the four things to know before changing anything.

## Sources

- Jacobson, "Thermodynamics of Spacetime: The Einstein Equation of State," PRL 75, 1260 (1995)
- Jacobson, "Entanglement Equilibrium and the Einstein Equation," PRL 116, 201101 (2016), arXiv:1505.04753
- Dorau & Much, "From Quantum Relative Entropy to the Semiclassical Einstein Equations" (2025), arXiv:2510.24491
- Touboul et al., MICROSCOPE final results, PRL 129, 121102 (2022), arXiv:2209.15487
- Delva et al., "A gravitational redshift test using eccentric Galileo satellites," PRL 121, 231101 (2018), arXiv:1812.03711
- Bothwell et al., "Resolving the gravitational redshift within a millimeter atomic sample," Nature 602, 420 (2022), arXiv:2109.12238
- Bertotti, Iess & Tortora, Cassini test of general relativity, Nature 425, 374 (2003)
- Fein et al., "Quantum superposition of molecules beyond 25 kDa," Nature Physics 15, 1242 (2019)
- Pikovski et al., universal decoherence from gravitational time dilation, Nature Physics 11, 668 (2015), arXiv:1311.1095
- Struyve, "Absence of gravitationally induced entanglement in certain semi-classical theories of gravity," arXiv:2510.20991
- Aziz & Howl, Nature (2025), reported in Physics World, 11 Nov 2025
- Krauss & Wilczek, "Using Cosmology to Establish the Quantization of Gravity," PRD 89, 047501 (2014), arXiv:1309.5343
- León, Kraiselburd & Landau, "Primordial gravitational waves and the collapse of the wave function," PRD 92, 083516 (2015), arXiv:1509.08399 *(abstract only)*
- León, Majhi, Okon & Sudarsky, "On the expectation of primordial gravity waves generated during inflation," arXiv:1712.02435 *(abstract only)*
- Perez, Sahlmann & Sudarsky, "On the quantum origin of the seeds of cosmic structure," CQG 23, 2317 (2006) *(not read; cited on the Stress Map)*
- Tolman (1930); Tolman & Ehrenfest (1930)
- Tilloy & Diósi, "Sourcing semiclassical gravity from spontaneously localized quantum matter," PRD 93, 024026 (2016), arXiv:1509.08705 *(not yet read; added 8 Oct)*
- Oppenheim, "A postquantum theory of classical gravity?" (PRX 2023), arXiv:1811.03116 *(not yet read; added 8 Oct)*
- Oppenheim, Sparaciari, Šoda & Weller-Davies, "Gravitationally induced decoherence vs space-time diffusion: testing the quantum nature of gravity," Nature Communications (2023), arXiv:2203.01982 *(not yet read; added 8 Oct)*
