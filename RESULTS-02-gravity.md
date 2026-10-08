# Results 02 — Gravity via the area law

*Run 7–8 October 2026; re-run inside this repository on 8 October to confirm the numbers. Code in [sim/gravity/](sim/gravity/), raw output in `sim/gravity/results/`. Stack: Python 3.13, NumPy, SciPy (pinned in [sim/requirements.txt](sim/requirements.txt)); no QuTiP needed.*

**Headline:** Gravity can come out of the framework's area law. The key ingredient, empty space's entanglement responding to energy with the 2π (Unruh) factor, checks out on a lattice, in 1D and in 3D. The route passes all four tests set for it. The original mechanism, "mass slows time because resolution takes time to process," fails three of them. What the framework adds beyond Jacobson is a reason gravity follows the outcome that actually happened.

**Context.** Gravity-origin was cut in July (§12 of [FRAMEWORK.md](FRAMEWORK.md)). On 5 October the scope widened to "how much known physics fits," and on 7 October Neil reopened gravity-origin through the area-law route, with four tests set in advance: direction, reach, universality, light bending.

---

## Summary table

| What ran | Question | Result |
|---|---|---|
| Step 0 | Does the framework supply Jacobson's ingredients? | Four of six outright; the area law in part; a story for the equilibrium assumption |
| Lattice, 1D horizon | Does a region's entanglement change by 2π × distance-weighted energy change? | **PASS** — within 1% in 28 of 34 cases (3 masses, 2 kinds of nudge) |
| Lattice, 1D small ball | Same, for a short interval of a massless field | **PASS** — 0.98–1.01, sizes 8 to 256 sites |
| Lattice, 3D small ball | Same, in three dimensions | **PASS with a surface term** — 0.97–1.01 when the wave straddles the edge; plain energy density fails completely |
| Test 1, direction | Does mass slow clocks without contradicting "dense matter settles fast"? | **PASS** |
| Test 2, reach | Does slowing reach through empty space? | **PASS**; a local-load rule fails |
| Test 3, universality | Do all clocks slow identically? | **PASS** by construction; a local-load rule fails |
| Test 4, light bending | Full bending, not half? | **PASS** — 1.751″ at the Sun's edge; time-slowing alone gives 0.876″ |

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

A free fit of the two correction terms over 54 configurations returns −0.168 and 1.056, against theory's −1/6 (−0.167) and 2π/6 (1.047), residual 0.3%. In words: **dS(lattice) = 2π × (improved energy change) + 2πξ ∮ d⟨φ²⟩**, with ξ = 1/6. The surface term is the Wald entropy term for this field, the same kind that appears in black-hole entropy, and it is exactly what Jacobson 2016's "conformal fields only" caveat is about. Ratios drop (to 0.64) only where the wave sits mostly inside the ball and dS is tiny.

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
- **Prediction 2:** **no primordial gravitational waves of quantum origin**. Krauss & Wilczek (2014) argued their detection would establish quantum gravity. None detected; Simons Observatory, LiteBIRD and CMB-S4 aim for σ(r) ~ 10⁻³.
- **Side effect:** a spread-out heavy mass feels its own averaged pull (Newton–Schrödinger). Not collapse, but a small departure from plain quantum mechanics.

**The signalling worry, and its answer.** Averaged gravity plus real settling could let a distant observer see a pull jump from "middle" to "side" when someone elsewhere looks. Neil (8 Oct): until the records can meet, the system has not truly resolved. Recorded as: **results become facts across regions only when records can meet, at light speed or slower.** A distant mass keeps pulling from its average until news of a look could arrive. This also explains why entanglement can't signal. Remaining: check the published work on locally sourced averaged gravity, mainly the moment a distant pull updates.

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
- Tolman (1930); Tolman & Ehrenfest (1930)
