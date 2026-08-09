# Results 01 — SIM-SPEC-01 executed

*All four tests designed, run and recorded 6 August 2026. Code in [sim/](sim/), raw output in `sim/results/`. Stack: Python 3.13, QuTiP 5.3.1, NumPy 2.5.1, SciPy 1.18.0 — pinned in [sim/requirements.txt](sim/requirements.txt).*

**Headline:** Tests 1, 2 and 4 pass. **Test 3 — the L-sweep — fails, and fails cleanly.** Coherence lifetime does not track absorber distance. The framework's single distinguishing prediction is not merely unsupported; in the regime where it was stated it is causally excluded.

---

## Summary table

| Test | Question | Result |
|---|---|---|
| 1 | Is coherence high for a superposition, zero for an outcome? | **PASS**, with a documented restriction on cross-system comparison |
| 2 | Does a chair come out thin without a hand-picked basis? | **PASS**, and more strongly than asked |
| 2 (Watch) | Does thinning require distinguishing coupling? (#9) | **PASS** — exactly, analytically |
| 3 | Does coherence lifetime track L? (#14) | **FAIL** — exponent 0.00 where 1.00 was required |
| 4 | Do the two analytic bounds reproduce? | **PASS** to machine precision |

---

## Test 1 — endpoint behaviour

**Pass conditions met.** Monotone decrease, correct endpoints, three valid measures agreeing on ordering along the dephasing sweep (Spearman = 1.000).

- Endpoints exactly as required: l₁ and relative entropy both 1 → 0; geometric measure 0.5 → 0.
- **The inversion argument, numerically.** Coherence and entanglement entropy anticorrelate perfectly (Spearman = −1.000) across the record-strength sweep. Coherence = |⟨E₀|E₁⟩| to 4×10⁻¹⁶ — the environment-state overlap, exactly.
- **Maxima differ as the spec warned** — l₁ → d−1, relative entropy → log₂d, verified for d = 2…8.
- **l₂ is not a monotone — counterexample reproduced.** Found an incoherent operation on d=3 that *increases* the summed squared off-diagonals by 0.089 while both valid measures decrease. The trap in the spec is real and it is easy to hit.

### One flag, and it is not fatal

Test 1's stated fail condition includes "the two measures disagreeing on ordering." They do — but only where it does not matter, and the boundary is sharp:

| States compared | Pair disagreement | Spearman |
|---|---|---|
| Along a single dephasing trajectory, any d | **0.0%** | **1.000** |
| Pooled across different trajectories | 2–4% | 0.99 |
| Unrelated random full-rank states, d = 8 | 13.5% | 0.91 |

**Reading.** Resolution moves a state *along* a dephasing trajectory, and there the two measures agree perfectly in every dimension. The disagreement appears only when comparing unrelated states.

> **Consequence for the framework.** It may say "this cell thinned" without choosing a measure. It may **not** say "cell A is thicker than cell B" for unrelated A and B without choosing one. Thickness is a well-defined monotone along a resolution history, and not a well-defined absolute cross-system quantity above d = 2. State this in the write-up before a referee finds it.

---

## Test 2 — does a chair come out thin?

**Pass, and the basis worry dissolves rather than being argued away.**

- **Exponential suppression in N.** Central-spin pure dephasing, disorder-averaged: log C falls linearly in N with slope −0.81. Coherence at N = 10³ is already below double-precision floor. Extrapolated to N = 6×10²³ the coherence is **10^(−2.1×10²³)**.
- **Generic couplings too.** Random non-dephasing Hamiltonians, full QuTiP evolution, N = 1…10: the basis-free Bloch length falls with N (log-slope −0.18).

### The basis question, made decidable

The spec worried that thinness might require "a hand-picked basis." That worry can be settled rather than argued, because for a qubit the l₁ coherence in the basis with axis n̂ is √(|r|² − (r·n̂)²), so **the maximum over every possible basis is the Bloch-vector length |r|** — a basis-independent quantity.

**Result: on the dephasing trajectory the which-path basis *is* the maximising basis** (agreement to 1×10⁻¹⁶). No other basis shows more coherence. So thinness is not an artefact of bookkeeping: the state is thin in every basis, and the framework's chosen basis is the most generous one available.

**This is a stronger result than Test 2 asked for**, and it retires the "decoration" failure mode. Zurek/einselection is no longer load-bearing as a defence of #4 — it remains the explanation of *why* the pointer basis is selected, but #4 no longer needs it to avoid a charge of basis-tuning.

### The #9 Watch clause — passes exactly

Sweeping the distinguishing fraction α of the system–environment coupling:

- **α = 0** (coupling proportional to the identity on the which-path DOF — gravity's case, since both slit-paths carry identical mass): coherence = **1.000000000000** at every N and every t. No thinning whatsoever.
- Coherence equals the environment-branch overlap |⟨E₀|E₁⟩| **exactly** (max deviation 0.0).
- Small-α decay rate exponent **2.009** against a predicted 2.

> **#9 survives its internal check.** Thinning is *exactly* the distinguishability of the environment record — not approximately, not typically. A non-distinguishing coupling cannot resolve. #9 can now only be killed from outside, by experiment, which is where the Strubbe disagreement lives.

---

## Test 3 — the L-sweep

**This is the result the project was waiting for, and it is negative.**

Model, per the design requirements: 1D tight-binding waveguide, finite bandwidth, emitter coupled at one site with fixed strength g, absorber at L lattice sites. L appears **only** in the position of the absorber — not in any rate, coupling, or spectral density. Nothing in the model says "a transaction completes when a signal returns from L."

Three independent absorber implementations were run, to be sure the answer was not an artefact of one:

| Configuration | Exponent of T vs L | T dynamic range | L dynamic range |
|---|---|---|---|
| Absorbing detector at L | **+0.00003** | 1.0004 | 200× |
| Real absorbing atom at L, irreversible record | **−0.004 to −0.078** | 1.15–3.4 | 200× |
| Perfect mirror at L (antinode branch) | saturating crossover | 2.00 | 200× |
| **Required by #14** | **+1.0** | **200×** | 200× |

Null A (Markovian amplitude damping) is exactly flat, confirming the pipeline reports flatness when flatness is true.

### What actually happens

1. **The detector configuration is flat.** Lifetime = 2/γ = 2J/g² for every L from 4 to 1500 sites, to four decimal places. It is set by the local coupling and nothing else. Verified across couplings g = 0.05–0.3 and bandwidths J = 0.5–2.0; in every case the value tracks 2J/g² and the spread over L stays below 0.07%.

2. **The mirror configuration does depend on L — in the wrong way, on the wrong scale.** Sweeping L site by site reveals a **period-2 alternation**, which is the standing-wave phase φ = 2k₀L: a *wavelength*-scale effect (this is Purcell, known since 1946), not a *delay*-scale one. Splitting the branches:
   - **Antinode (even L):** lifetime rises from 1/γ to 2/γ and then saturates. A factor of **2**, spanning a 200-fold change in L, and flat thereafter.
   - **Node (odd L):** the emitter forms a bound state and *stops decaying* at a residue. The residue falls from 0.97 at L=5 to 0.33 at L=401. **A closer absorber preserves more coherence** — the opposite sign to #14.

3. **The maximum local slope anywhere is 0.64**, at the crossover shoulder, and it flattens immediately. Over 91% of the swept window the slope is below 0.5. #14 requires a sustained 1.0.

### Why this is not a parameter choice — the causal bound

The one regime where the absorber distance affects the lifetime at all is bounded, and the bound is quantitative:

> **L\* = v/γ.** Measured across four couplings, the saturation distance scales as γ^(−0.994) against a predicted −1, with observed/predicted ratios of 0.95, 1.09, 1.13, 1.04.

The reasoning is general, not model-specific. Coherence decays at the local rate γ. Information about the absorber's existence cannot return faster than 2L/c. So once 2L/c exceeds the decoherence time, the absorber's distance **cannot** influence the decay — the source has already decohered before any confirmation could arrive.

> **A coherence lifetime proportional to L is therefore not merely absent from this model. It is causally excluded in any theory with a finite signal speed.** And the distance at which it is excluded is itself set by the local coupling — so even the range over which L matters is a coupling-controlled quantity.

### The observable that *does* scale as L

Record-formation time at the absorber scales as L^1.09 with r² = 0.999. That is real, and it is the L/c timescale #14 correctly identifies.

**But it is time of flight.** It is present in every theory with a finite signal speed, it is not a decoherence timescale, and it distinguishes nothing. The distinction the framework needs and does not have is between *when the record forms somewhere else* and *how fast the source loses coherence*. The absorber determines **where** the record forms. The local coupling determines **how fast** the source decoheres. These are different quantities and only the first depends on L.

### Verdict against the pass conditions fixed before the run

- ❌ **Supports #14** — required monotone scaling with exponent ≈ 1. Observed ≈ 0.
- ✅ **Against #14** — "lifetime L-independent at fixed coupling." This is what was observed.
- ❌ **Evidence for Reading A** — required a cutoff, a scaling that stops. There is no scaling to stop.
- ⚠️ **Null-B indistinguishability** — moot, and worse than moot. The concern was that #14's prediction might be reproduced by conventional physics. Instead conventional physics reproduces neither, because the effect is not there in either reading. Note also that Null B and the signal were always going to be the same numbers: **the framework supplies no dynamics of its own.** There was only ever one model to run.

---

## Test 4 — code correctness

Both analytic bounds reproduce, so the Test 3 pipeline is trustworthy.

- **Streltsov:** entanglement generated = coherence consumed to **1.8×10⁻¹⁵** under the generalised CNOT, across d = 2…5. Zero bound violations in 2400 samples. Under non-injective (suboptimal) incoherent operations a gap opens, and the gap is exactly the branches the ancilla fails to resolve — coupling suboptimality, as the paper says.
- **Englert:** V² + D² ≤ 1 with zero violations in 20 000 samples (max excess 3.6×10⁻⁸, numerical). 26% of samples within 1% of saturation.

### A correction for SOURCES

SOURCES §6 records the duality identity as **V² + K² = 2 Tr(ρ²) − 1, "where ρ is the state of the which-way marker."** That attribution is wrong in general:

| Joint state | Identity against **path** purity | Identity against **marker** purity |
|---|---|---|
| Pure | holds (1.2×10⁻¹⁵) | holds (1.3×10⁻¹⁵) |
| Mixed | **holds (7.2×10⁻¹⁶)** | **fails (deviation 0.61)** |

The relation is an identity for the **interfering system's** reduced state. It appears to hold for the marker only because a *pure* joint state has equal Schmidt purities on both sides. Cite it against the path state, or a referee who tries a mixed marker will find the error.

---

## What this does to the framework

**Discharged:**
- #4 (thickness = coherence) is no longer provisional. Tests 1–2 pass. Promote to **KEEP**.
- #9's internal check passes exactly. Still **KEEP + RISK** — the risk is external and unchanged.
- §4's bounds are verified; nothing there needs revisiting.

**Killed:**
- **#14's L/c claim, as a claim about coherence lifetime.** The prediction is false in the detector configuration, wrong-signed in the node configuration, and bounded to a factor of 2 in the most favourable one.
- **Reading B has no testable content left.** Its own text: "What remains testable is the L-sweep." The L-sweep has run. The range limit, which Reading B traded away as vacuous, is not recoverable from this result either — Reading A predicted a *cutoff*, and there is no scaling to cut off. **Neither reading survives as an empirical claim.** The fork is not "revisit Reading A"; it is that the fork was never empirical.

**What survives, honestly stated:**
- The framework is a coherent *interpretation* of standard open-system quantum mechanics. Tests 1, 2 and 4 confirm its internal machinery works and is not basis-tuned.
- #9 is a genuine, sharp, falsifiable disagreement with Strubbe on a checkable point, and it is now internally verified. **It is the only empirical content the project has left.**
- The L/c timescale is real as *time of flight to the absorber*. It is not a decoherence timescale and it is not distinguishing.

**Recommended reframing.** The paper that can be written from this is *not* "front thickness is derived from L/c and here is the test." It is: **#9 versus Strubbe, on gravitationally extracted which-path information**, with the resolution rule (thinning = environment distinguishability, verified exactly) as its machinery. That is one clean bet against a named opponent on one experiment. The L/c story should be reported as a negative result — it is a real contribution to have closed it, and closing it took four hours rather than a referee's rejection.

---

## Reproduction

```bash
python -m pip install -r sim/requirements.txt
cd sim && python test1_endpoints.py && python test1b_ordering.py && python test2_chair.py && python test3_lsweep.py && python test3b_followup.py && python test3c_atom.py && python test4_bounds.py && python make_figures.py
```

Figures: `sim/results/fig3_lsweep.png` is the one that matters.

**Known numerical caveat.** In the Test 3e convergence block, `cap_len=600` combined with `left_pad=400` puts the emitter inside the left absorbing ramp and shifts the absolute lifetime by 1.6% (199.96 → 196.70). It does not affect the L-independence — the spread over L *falls* to 1.000008 in that run. Keep `cap_len < left_pad`.
