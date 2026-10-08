# The Resolution-Front Framework

*Working document. Last substantive revision **8 October 2026** — scope widened (5 Oct), gravity-origin reopened and tested ([RESULTS-02-gravity.md](RESULTS-02-gravity.md)), new commitments and predictions collected in **§15** (scaled back the same day after [REVIEW.md](REVIEW.md) v4: one prediction, conserved source as the gate); targeted edits in §6, §8, §11, §12, §13, §14. Previous revision 6 August 2026 (evening) — **SIM-SPEC-01 executed in full; results written back into §3, §4, §7, §8, §11, §14.** #4 confirmed, #9 internally verified, **#14's L/c prediction failed**. See [RESULTS-01.md](RESULTS-01.md). Earlier the same day: Reading B adopted (§7), handshake confined to the front (§7, §9), #1 marked idle, τ-adoption reversed. Seven blocking papers read 5 August 2026 ([SOURCES.md](SOURCES.md)).*

> **Read this first (October 2026).** **Charter (updated 8 Oct):** an interpretation of quantum mechanics plus one semiclassical claim about gravity — an unsettled mass gravitates by its average. Everywhere else the framework adds a story, not dynamics; for that one claim it is a physical theory that can fail. It carries **two predictions**: BMV-type experiments will see no entanglement through gravity, and primordial gravitational waves of quantum origin are strongly suppressed (derivation owed). Gravity is taken from the area law (Jacobson's route) as a compatibility argument, not derived; the free-field first law is checked on a lattice, and the old settling-load mechanism is dead. **The reopening stands only if a conserved source can be written (§14 item 7).** Start with §15, then [RESULTS-02-gravity.md](RESULTS-02-gravity.md).
>
> **August status, kept as history.** The framework's single distinguishing prediction — coherence lifetime tracking absorber distance L — was tested on 6 August and **does not hold**. Sections written before that run still argue for it; they are marked where they stand. The live claim is #9 (§8), which passed its internal check exactly and remains a sharp disagreement with Strubbe on a checkable experiment.

**Scope (widened 5 October 2026):** how much of known physics, small and large, fits the framework, tracked phenomenon by phenomenon on the RFF Stress Map (§15). Gravity-origin, cut in July, was reopened on 7 October through the area-law route and tested. *The July scope line, kept as history: "the double slit and the measurement problem; gravity-as-origin and cosmology were cut — they fed nothing back into the measurement story and carried all the empirical exposure."*

| File | Role |
|---|---|
| **This one** | The whole argument and all sixteen posits. Canonical. |
| [SOURCES.md](SOURCES.md) | Every paper, the question it was read for, and the answer. |
| [SIM-SPEC-01-coherence.md](SIM-SPEC-01-coherence.md) | The computational task that verifies or kills §3. **Executed 6 Aug.** |
| [RESULTS-01.md](RESULTS-01.md) | What the simulations returned, and what it does to the posits. |
| [RESULTS-02-gravity.md](RESULTS-02-gravity.md) | **Oct 2026.** The area-law route to gravity: lattice checks, the tests that killed the settling-load mechanism, the decisions, and the open source question. |
| [sim/](sim/) | The code. Python + QuTiP, pinned. Gravity checks in [sim/gravity/](sim/gravity/). |
| RFF Stress Map (private link in §15) | **Oct 2026.** Known physics mapped fundamental → abstract, each item marked fits / fits with work / strains / breaks / outside an interpretation. |
| [REVIEW.md](REVIEW.md) | External project review (status, risks, next actions). **v4, 8 Oct** — reviews the October gravity work; response section at the end. |
| [Framework-Summary-Plain.md](Framework-Summary-Plain.md) | Lay summary, no jargon. Rewritten 9 Aug; **predates October, not yet refreshed.** |
| [papers/](papers/) | PDFs. |

---

## 1. The claim

The universe is a **block** — past and future both real — with two modifications:

1. The future exists as **potential**, not as definite fact.
2. The "now" is not a flat slice but a **slab with thickness**, and that thickness is **informational**: it measures how much is still undecided in a region. Near-resolved regions are thin; highly superposed regions are thick.

The universe advances by **resolving** undecided conditions within the slab.

**Terms.** *Cell* — a local unresolved region; mathematically this is the wavefunction. *Front* — the advancing slab where resolution happens. *Wake* — the resolved region behind it.

**The core claim, in one line:**

> **The front advances by converting coherence into entanglement.**

Everything below either supports that sentence, prices it, or says what it still owes.

---

## 2. Prior art — the map

Almost nothing in the original notes was unclaimed. Cite these or lose the room.

- **Ellis & Rothman, "Time and spacetime: the crystallizing block universe"** (IJTP 49, 988–1003, 2010; arXiv:0912.0808). Future quantum-indeterminate, past classically definite, reduction as the transition — and explicitly **non-uniform**: delayed choice leaves patches of indeterminacy persisting. That last part is #13, and it is squarely his.
  **But he is not a block-universe theorist** — see §9. His future genuinely does not exist. Ours does. Different ontologies, not variants.
- **Strubbe, "Crystallizing spacetime"** (arXiv:2505.10383, 2025). Crystallisation front Σ(τ), explicit evolution parameter τ, deterministic and realist, reproduces double-slit interference and EPR via Costa de Beauregard zigzag, claims to resolve the measurement problem. **The closest work in existence to this framework.** He does not solve the selection problem (§10), he contradicts #9 head-on (§7), and his analogue of #14 is set by free constants rather than a physical distance (§8).
- **Cramer (1986); Kastner, PTI (2010–13).** Offer wave ψ, confirmation ψ*, transaction as collapse. Kastner adds a dynamic ontology where spacetime is created out of the present.
- **Zurek, decoherence and einselection.** The resolution rule of §6. Well established, and famously does *not* deliver single outcomes — it gives an improper mixture. The rule inherits that gap exactly.
- **Bohm (1952); Sutherland's causally symmetric Bohmian mechanics; Valentini (1991–).** The determinism story of §9.
- **Jaeger, Shimony & Vaidman (PRA 51, 54, 1995); Englert (PRL 77, 2154, 1996).** The duality relation V² + D² ≤ 1. *Cite Jaeger–Shimony–Vaidman first — they have priority, and citing Englert alone gets it wrong.*
- **Baumgratz, Cramer & Plenio (2014); Streltsov et al. (2015).** The coherence resource theory and the coherence→entanglement bound. §3 rests entirely on these.

**Independent reconstruction is a real signal about the intuitions. It is not a contribution.**

---

## 3. The thickness variable: coherence

### What died

Thickness was originally λ = h/p. It fails on three counts:

1. **Frame-dependent.** p isn't invariant, so the slab has no invariant thickness.
2. **Divergent in the rest frame.** Every massive particle has one; there p = 0 and λ → ∞. So *everything* is maximally thick somewhere, including a screen dot after resolution. The variable loses all discriminating power.
3. **The wrong quantity.** h/p tracks fringe *spacing* — a property of the wave, already handled by phase. Spatial extent is not undecidedness.

**Diagnosis:** undecidedness is a *relation* between a system and everything it hasn't coupled to yet. It was never a property of the particle alone. For a free particle the only invariant is rest mass, which isn't state-dependent — so the search for a kinematic invariant was structurally doomed, not merely unlucky.

### The four criteria

A thickness variable must be:

1. **Invariant** — same in every frame. *(h/p fails.)*
2. **Finite everywhere** — no divergence in any frame. *(h/p fails.)*
3. **A measure of undecidedness, not of extent or phase** — those are accounted for elsewhere. *(h/p fails.)*
4. **Correctly signed at the endpoints** — maximal for a live superposition, zero for a resolved dot.

### Why not entanglement entropy

It points backwards. Run the test cases:

| | Superposed electron in flight | Dot on the screen |
|---|---|---|
| Thickness should be | high | zero |
| Entanglement entropy is | **0** (isolated, pure) | **large** (entangled with ~10²³ DOF) |

Entanglement entropy measures how much which-path information has *escaped*. That is a measure of resolution, not of undecidedness. Exactly inverted. **So swap the slots:** resolution = growth of entanglement entropy; thickness = coherence.

### Coherence

The resource theory of coherence (Baumgratz–Cramer–Plenio 2014) quantifies exactly "how much superposition is present" relative to a basis. Fix a basis; states diagonal in it are incoherent; a valid measure never increases under operations that cannot create coherence. Two measures qualify:

- **Relative entropy of coherence:** C = S(ρ_diag) − S(ρ). Maximum log d.
- **l₁-norm:** the sum of the off-diagonal magnitudes. Maximum d − 1.

High for a live superposition, zero for a dot, no rest-frame divergence, no momentum dependence. Passes all four criteria.

**Traps, all confirmed in the source:**
- The **squared** off-diagonals (l₂) are *not* a valid measure — monotonicity fails, with an explicit counterexample. It is the measure most people reach for first.
- The two valid maxima differ and coincide only for a qubit. Compare orderings, never magnitudes.
- The maximally coherent state is the *uniform* superposition, so a 50/50 superposition is thicker than a 70/30 one. **Thickness tracks amplitude balance, not just branch count.** That is a commitment; make it deliberately.

### The two costs

**Basis-dependence.** Arguably a feature: the basis is the which-path basis, and einselection already explains why the environment selects it. We inherit a solved problem rather than an open one.

**Finite-dimensionality — the larger cost, and it is unresolved.** Baumgratz–Cramer–Plenio build the theory for a d-dimensional Hilbert space and flag the infinite-dimensional case as not yet constructed; Streltsov et al. state "finite-dimensional" in their theorem. **A particle's position is neither.** Two honest options:

1. **Restrict to the discrete which-path degree of freedom** — treat the slit choice as a qubit and say so. Legitimate, standard, keeps every cited result valid. Cost: thickness becomes a property of a chosen two-level abstraction rather than of the electron, which weakens the claim to be *the* continuous quantum↔classical parameter.
2. **Take on continuous-variable coherence.** A separate project.

**Decide before the write-up. Leaving it unstated is the kind of thing a referee finds first.**

### What thickness is, after §7

Under Reading B, thickness has two descriptions that must agree:

- **Informational:** coherence, as defined above.
- **Structural:** the depth of still-open transactions — how far back into the wake tails remain unclosed, i.e. ~L/c.

**The framework's central quantitative claim is that these are the same quantity.** Coherence persists exactly as long as the transaction stays open. That is not circular — the two are defined independently, one in Hilbert space and one in spacetime — and it is exactly what makes it testable.

### Still owed

1. Does a chair come out thin without hand-waving about basis choice?
2. ~~**Does coherence lifetime track L, or coupling strength?**~~ **Answered 6 August: coupling strength.** The L-sweep ran and #14's prediction failed — exponent 0.00 against the required 1.00, and beyond L\* = v/γ the absorber's distance is causally barred from mattering at all. See §7 and [RESULTS-01.md](RESULTS-01.md).

Item 1 was [SIM-SPEC-01](SIM-SPEC-01-coherence.md) Test 2: **passed 6 Aug**, and passed more strongly than asked — on the dephasing trajectory the which-path basis is the *maximising* basis over all bases, so thinness is not basis-tuned and cannot be called bookkeeping. Item 2 was Test 3: **failed**.

---

## 4. Coherence into entanglement — and why there's no gap to exploit

Coherence lost by a system converts into entanglement generated with its environment. Streltsov et al. make this exact: a state can be converted to an entangled one **if and only if** it is coherent, and the entanglement generated is bounded by the coherence consumed.

For the double slit the relevant form is the duality relation **V² + D² ≤ 1** (visibility versus which-path distinguishability).

**The hope was that the gap in these inequalities was where the framework could have content. It isn't. Both were checked and both are closed:**

- **Duality:** the gap has a closed form — **V² + K² = 2 Tr(ρ²) − 1**. It is exactly the *impurity of the which-way marker*, and nothing else. Known since 1996, measured to the percent level in 1999.
- **Streltsov:** the bound is **attainable**, via an explicit generalised CNOT. So a gap in any real evolution says only that the actual system–environment coupling isn't the optimal entangling operation — which it never is. The gap measures suboptimality of the coupling, not a shortfall in the theory.

**Both verified numerically 6 Aug** ([RESULTS-01.md](RESULTS-01.md), Test 4): entanglement generated equals coherence consumed to 1.8×10⁻¹⁵ under the generalised CNOT, zero bound violations in 2400 samples; V² + D² ≤ 1 with zero violations in 20 000 samples. The gap under other incoherent operations is exactly the branches the ancilla fails to resolve. Nothing here needs revisiting. *(One correction for the ledger: the duality identity holds against the **interfering system's** purity, not the marker's — see [SOURCES.md](SOURCES.md) §6.)*

**Consequence.** The core claim of §1 is now visibly a theorem someone else proved, in standard quantum information theory, with no ontology attached. To recover content here the framework would have to claim something about *which* operations nature uses — a dynamical claim needing its own argument. **Original content lived in #14 and #9. #14 failed its test on 6 August (§7), so it lives in #9 alone.**

---

## 5. The cell

- A cell is a continuous blob. Inside it, states are in superposition and oscillate; the oscillation carries **phase**, which sets fringe spacing.
- The cell's thickness is set by the **dynamical state** of what's inside, not by material identity.
- The cell can deform and stretch: part runs ahead into the front, part stays in the wake. It **straddles time**.
- Its **root stays connected** — an entangled pair is one deformed blob, not two things signalling.

*Cut: fractal structure. It survived deletion; nothing used it.*

---

## 6. The resolution rule

**A cell resolves when its coupling to the environment creates a which-branch record** — when something ends up *different* depending on which branch is real. That is which-path-distinguishing coupling, and physically it is entanglement.

- **Distinguishing coupling** → creates a record → **resolves** the cell (thins it).
- **Non-distinguishing coupling** → does **not** resolve → superposition survives.

Falls out cleanly:
- **Double slit.** Electron leaves as a thick cell, stays thick through both slits (nothing distinguishes the paths), thins to a dot at the screen.
- **Which-path detector kills fringes.** Predicted, not bolted on.
- **Resolution is nonlocal.** A record forming anywhere, irreversibly, resolves the cell — justified because the pair is one blob, so EPR correlations need no message. *(Refined 8 Oct 2026: a record settles the cell on its own side first; the result becomes a fact across regions only when records can meet, at light speed or slower. The correlation is still one blob's; what is local is when it becomes a shared fact. §15.)*

**Quantified:** resolution = growth of entanglement entropy. This is Zurek's, and it inherits his gap — decoherence gives an improper mixture, not one outcome. So the rule buys the which-path result but not definite outcomes. Do not count those as two separate wins.

### The area law

Vacuum entanglement across a spatial cut scales with boundary **area**, not volume (Srednicki 1993). The argument is short and good: tracing out the inside and tracing out the outside give the same eigenvalues, hence the same entropy — so the answer can only depend on what the two regions share, their common boundary. If the front is a surface and resolution proceeds by entanglement forming across it, **resolution rate scales with front area**.

**Conditions, all of them:** free field, vacuum ground state, flat space, static region, **d = 3** for the R² law (d = 2 gives S ∝ R; d = 1 goes logarithmic and is the only case where the infrared cutoff enters; d ≥ 4 was not computed), and a **coefficient that depends on the UV cutoff and is not universal**. Nothing licenses extending it to excited or thermal states — which is every case this framework cares about.

*Note: the field is massless, i.e. gapless, and the law is clean anyway. Earlier notes hedged this against "gapped ground states"; that was wrong.*

~~**Call this locality, never "gravitational propensity"** — that would contradict #9.~~ **Lifted 7 Oct 2026.** The area law is now the framework's route to gravity (Jacobson; §15, [RESULTS-02-gravity.md](RESULTS-02-gravity.md)). It does not contradict #9: gravity built this way is sourced by energy, and for an unsettled mass by its average, which carries no which-path information. On a 3D lattice the 2π rule needs a surface (Wald) term alongside the bulk linking; keep that in mind when talking about thickness at a boundary.

---

## 7. The handshake, and the one original claim

The pattern on the screen has two features:
- **Fringe spacing** ← set by phase ← handled by the cell's oscillation. ✅
- **Fringe brightness** ← set by |amplitude|² ← **the open debt.**

**The mechanism (transactional):** resolution is a two-sided handshake, not a one-way arrival. The emitter sends an **offer wave** ψ forward; each potential absorber sends a **confirmation wave** ψ* back; the completed link is ψ·ψ* = |ψ|².

**This does not pay the debt, and it is important to say so plainly.** ψ* is *defined* as the conjugate of ψ, so ψ·ψ* = |ψ|² is arithmetic, not physics. The square appears because we put it there. *(Strubbe makes exactly the same move — coupling coefficient applied once out and once back around a loop — and does not notice.)*

### #14 — the confirmation closes the tail

**The returning confirmation is what closes the tail of the blob**, on a timescale **~L/c** set by the distance to the absorber.

- Open tail = superposed and thick; confirmation returns = tail closes = resolution = thinning.
- Explains why macroscopic matter is thin: its tails were sealed by completed transactions long ago.
- Commits us to a wake that isn't uniformly solid — right behind the front, tails dangle open. Delayed-choice experiments behave this way.

### The handshake is confined to the front

**The offer and confirmation both happen inside the slab. Neither reaches into the far future block.**

Stated as a restriction on #11/#14 — though under Reading B it turns out to be forced rather than chosen (see the note below) — it pays for itself three times:

**It answers Ellis's objection.** He rejects transactional accounts because you cannot integrate over a future that does not exist. If the round trip never leaves the front, the objection does not apply — the absorber the offer transacts with is inside the slab, and the slab is real on any account. **We no longer need the far future to be accessible, so we no longer need to defend accessing it.**

**It makes #1 idle — see §9.** If nothing in the mechanism reaches past the front, no physics here depends on the far future existing. The full block stops being the substrate and becomes a preference.

**Under Reading B this stops being a restriction and becomes a consequence — say so.** Once the front is *defined* as the region where transactions are still open (below), nothing can be outside it, so the handshake cannot leave it. That is not a weakening: the objections still dissolve, and the answer is cheaper for being forced rather than postulated. But it means confinement and derived thickness are **one move with three payoffs, not two independent wins.** Do not bill them separately in the write-up; a referee who spots the double-count will discount both.

### Where the tail actually is — and what the front therefore is

Three regions, and they have to be kept apart:

- **Ahead of the front** — unresolved.
- **The front** — where resolution is happening.
- **Behind the front** — mostly resolved, but with tails still dangling open. Ellis's pockets of residue. The glowing margin.

**The tail that #14 closes sits behind the front, not in it.** The emitter is in the wake, the absorber is at or near the front, and the confirmation travels *backward* into the wake to close the tail. So the extent that matters is not the resolving surface — it is **how far back into the wake tails remain open**.

That leaves a choice about what the word "front" names, and it is a real fork.

### Reading B — adopted

**The front is the whole partially-resolved slab, glowing margin included.** Its leading edge is where resolution begins; its trailing edge is simply **where the last tail closes**.

> **Front thickness is not a free parameter. It is set by how long transactions stay open — that is, by L/c.**

This is the reading the framework wants, and it earns its place five times:

1. **It answers what sets the thickness.** Nothing external does. The front is thick *because* tails take L/c to close. Derived, not postulated — and that question had no answer before.
2. **Thickness becomes local and variable automatically.** Dense matter with absorbers everywhere: transactions complete fast, front is thin. Isolated particle heading for a distant screen: transaction stays open, front is locally thick. That is exactly what #3 and #4 require, and it is the same statement as "macroscopic matter is thin because its tails were sealed long ago."
3. **It merges #4 and #14.** Thickness *is* open-transaction depth. That is the unification the **old** Test 3 was chasing, reached structurally rather than numerically — and the reason the redesigned Test 3 no longer chases it.
4. **It dissolves the long-baseline problem.** Delayed-choice and erasure experiments over long baselines — Jacques et al. at tens of metres, Ma et al. (PNAS 110, 1221, 2013) over a hundred-kilometre-scale link — do not falsify anything. They simply have a locally thick front. No ad-hockery, because thickness was never global to begin with.
5. **It renders the wake non-uniform geometrically.** The advancing slab is bumpy: thick where long transactions are open, thin where everything has settled. That is Ellis's non-uniform crystallisation, drawn rather than asserted.

**The first cost, and it is real.** Under Reading B there is no range limit. "An absorber outside the front cannot close a tail" becomes vacuous, because the front's extent is *defined* by where transactions are still open — nothing is outside it by construction. **We trade a prohibition for an explanation.**

**The second cost, not previously priced: thickness has no upper bound.** If thickness = L/c with no cutoff, then a photon in flight from a distant source leaves the front locally thick over that whole baseline. The cosmic-source Bell tests (Handsteiner et al. 2017; Rauch et al. 2018, quasar-seeded settings) then imply a front locally *gigayears* deep. Nothing falsifies that — thickness is local and unbounded by construction — but two things follow and both belong in the write-up:

1. **"Now" is no longer a thin slab in any recognisable sense.** The word "slab" carries a picture that Reading B does not license. Audit it in §13 terms before using it in prose.
2. **The contrast that does the work is local, not global.** "Macroscopic matter is thin" survives — dense matter closes its transactions immediately. Do not defend a global thickness; there isn't one.

What remains testable is the **L-sweep**: does coherence lifetime track distance to the absorber rather than local coupling strength? #14 says it tracks L/c.

**The null is not as clean as it looks, and this is the most likely way the paper dies.** "Standard decoherence says the decay time is set by coupling and temperature and does not move with L" is true for a *Markovian* bath — it is not true of open-system physics generally. An emitter in front of a mirror at distance L has an L-dependent decay rate (Purcell/interference), and time-delayed coherent feedback in waveguide QED is explicitly non-Markovian with memory time 2L/c. **So a standard model can produce L/c scaling with no #14 in it.** The prediction only distinguishes if the null model is stated as a specific implementable dynamics and *fails* to reproduce the observed scaling. Fixing this is a design requirement on [SIM-SPEC-01](SIM-SPEC-01-coherence.md) Test 3, not a caveat to add later.

**Subject to that, this is the framework's single distinguishing prediction, and the paper should be built on it.** *(Written 6 Aug, before the run. It was run the same day and it failed — see below. Left in place because the reasoning that led here was sound; the prediction was simply wrong.)*

### Reading A — recorded, not taken

*The front is the resolving surface only; the glowing margin is a separate structure behind it.*

Then front thickness and margin depth are different quantities, and the range limit survives as a genuine prohibition: some extent exists beyond which a transaction cannot complete, and that forbids something observable.

**Why not taken:** it leaves front thickness unexplained, and it puts the long-baseline experiments back as a live constraint — a fixed thickness looks falsified by the hundred-kilometre results, and a thickness that adapts to the apparatus is a patch with no mechanism.

| | Reading A | **Reading B (adopted)** |
|---|---|---|
| Front thickness | independent, unexplained | **derived from L/c** |
| Long-baseline experiments | live constraint, possibly fatal | **dissolved** |
| Range limit as prediction | sharp prohibition | **vacuous** |
| #4 and #14 | separate posits | **one quantity** |
| Testable content | prohibition + L-sweep | **L-sweep** |

### The L-sweep ran on 6 August. It failed. *(Result written back here per the SIM-SPEC routing table — full detail in [RESULTS-01.md](RESULTS-01.md).)*

**Coherence lifetime does not track L.** Fitted exponent ≈ 0.00 against the 1.00 #14 requires, in three independent absorber implementations (absorbing detector, real absorbing atom with an irreversible record, perfect mirror). The mirror case does depend on L, but as a period-2 **standing-wave phase** alternation — Purcell, wavelength-scale — and on the node branch a *closer* absorber preserves *more* coherence, the opposite sign to #14.

**And the claim is not merely unsupported, it is causally excluded.** Coherence decays at the local rate γ; nothing about the absorber can return faster than 2L/c; so beyond L\* = v/γ the absorber's distance cannot affect the decay at all. Measured: L\* scales as γ^(−0.994) against a predicted −1. **Even the range over which L matters is set by the local coupling.**

**What this does to the fork.** Reading B's own text said "what remains testable is the L-sweep." It has run. Reading A predicted a *cutoff* — a scaling that stops — and there is no scaling to stop, so Reading A is not recovered either. **The A/B fork was never empirical.** Do not revisit A; do not rewrite B. Record that front thickness has no measured consequence and move the paper to #9.

**What survives, and it is real:** record-formation time at the absorber does scale as L (exponent 1.09, r² = 0.999). #14 correctly identified an L/c timescale. It is time of flight — present in any theory with a finite signal speed, not a decoherence timescale, and distinguishing nothing.

**The wake being non-uniform is Ellis's** (#13). His wording: a crystallizing molten mixture in which "some molten bits remain in the interstices to become fixed only later," with pockets persisting "for a time after the main resolution front has passed."

**What closes a pocket, and on what timescale, is not.** Ellis never says. Cramer never says.

**Strubbe has the structure but not the number.** His dynamics also persist in a finite region behind the front — milliseconds deep in his EPR run. But that depth is set by free relaxation constants he says outright can be "tuned to make this dynamic region arbitrarily small." **Ours is set by L/c — a physical distance, not a fitting parameter.**

> **This is the delta. It survived all seven papers. It is the paper.**

**What it still owes:** find something that differs *inside* the L/c window from what decoherence alone predicts — against a null model that is itself allowed to be L-dependent (above).

*(Struck 6 Aug. This paragraph used to add: "the claim partly dissolves if §3's Test 3 passes — if coherence decay time equals decoherence time, the window and thickness are one quantity." That was the **old** Test 3 and it had the logic backwards on both halves. The merge of #4 and #14 is already done structurally under Reading B — no numerical result is needed for it. And τ_C = τ_D in a model that contains no L would show coherence is governed by local coupling rather than by distance to an absorber: evidence **against** #14. See [SIM-SPEC-01](SIM-SPEC-01-coherence.md) Test 3.)*

---

## 8. Gravity does not resolve — #9

**No gravitationally induced collapse, at any mass scale.** Both slit-paths have identical mass, so gravity sees the same thing either way: non-distinguishing coupling, therefore no resolution. This directly contradicts the Diósi–Penrose family, which is under active experimental test.

**It now has a named opponent on the same experiment.** Strubbe predicts you could extract **which-slit information gravitationally without destroying the interference pattern**, because in his model only the single momentum-carrying worldline gravitates. That makes gravity *distinguishing* — and by §6's own rule, a distinguishing coupling **resolves**. #9 and Strubbe's model cannot both be right, and they differ on a checkable point rather than on interpretation.

| | This framework | Strubbe |
|---|---|---|
| Gravitational collapse (Diósi–Penrose) | **No** | No |
| Gravitationally induced entanglement | **No** — decided 8 Oct 2026 (averaged gravity, §15) | **No** |
| Gravity can distinguish which-path | **No** | **Yes** |

**The Strubbe column is a reading of his paper, not a re-derivation** *(noted 8 Oct, [REVIEW.md](REVIEW.md) v4; Neil confirmed the same day that no re-derivation exists anywhere)*. With entanglement now "No" on both sides, BMV does not separate us; the separating experiment is a gravitational which-path measurement that, on his account, leaves the pattern intact. Collapse (Diósi–Penrose), which-path, and entanglement are three different apparatuses, not one disagreement.

**State it loudly, and name him** — once two debts are paid: his prediction re-derived from his equations, and the separating experiment specified (mass, separation, coherence time, what is measured, which apparatus could reach it). A bet against a named opponent on one experiment is worth more than a bet against a research programme. Then it belongs in the abstract.

**Its internal check has now run, and #9 passed it exactly** *(6 Aug, [RESULTS-01.md](RESULTS-01.md); result routed here per the SIM-SPEC table).* Sweeping the distinguishing fraction α of the system–environment coupling: at α = 0 — a coupling proportional to the identity on the which-path degree of freedom, which is gravity's case since both slit-paths carry identical mass — coherence stays at **1.000000000000** at every N and every t. No thinning whatsoever. Coherence equals the environment-branch overlap |⟨E₀|E₁⟩| to zero deviation, and the small-α decay rate carries exponent 2.009 against a predicted 2.

**So thinning is *exactly* the distinguishability of the environment record** — not approximately, not generically. A non-distinguishing coupling cannot resolve, as a matter of arithmetic rather than of modelling choice.

**#9 can now only be killed from outside.** That raises the stakes on the Strubbe disagreement rather than lowering them, and since the L-sweep failed (§7), **this is the only empirical content the framework has left.** Build the paper here.

### 8 October 2026 — #9 grounded rather than asserted

The original argument, "both slit-paths have identical mass, so gravity sees the same thing," is weak: a mass in superposition sits in different places, and a quantum gravitational field would distinguish them. That is why an August review session retired #9 on BMV grounds (recorded in project notes, never written back here). **The averaged-gravity decision (§15) restores it on firmer footing:** an unsettled mass gravitates by its average, which carries no which-path information, so gravity cannot resolve. The price is a definite prediction, now the framework's first: **BMV-type experiments will see no entanglement through gravity.** The disagreement with Strubbe stands: he lets gravity distinguish which-path; we do not.

---

## 9. Determinism, Born, and the ontology debt

**Position: nothing is random.** Outcomes are fixed by the net conditions in the nonlocal, root-connected blob. This is legitimate — it puts the framework in the **nonlocal hidden-variable** family, and Bell only forbids *local* determinism.

**The two debts are one debt, and it's a theorem.** Valentini: quantum non-equilibrium (ρ ≠ |ψ|²) permits signal nonlocality; equilibrium forbids it. So exact Born ⟺ no-signalling ⟺ empirically identical to QM, forever.

### The Born fork is settled — by the scope cut, not on the merits

Towler, Russell & Valentini establish that relaxation to the Born rule is **real and demonstrated**: the coarse-grained H-function decays exponentially, **τ ∝ M⁻¹** in the number of superposed modes, robust across coarse-grainings. In physical units, **~10⁻²¹–10⁻¹⁸ s** for an electron. Driven by wave-function nodes generating vorticity and stirring the two densities together.

So Born-by-relaxation can be adopted honestly. **But it buys nothing observable inside our scope.** Relaxation completes long before anything measurable; the only surviving non-equilibrium is *relic* — early universe, super-Hubble modes, CMB imprints. **We cut cosmology.**

> **Adopt relaxation as the account of Born-rule origin. State plainly that within this scope it is observationally identical to postulation, and that the distinguishing regime is cosmological and out of scope.**

Getting teeth back means bringing cosmology back, and §12 lists good reasons not to.

*(If citing a relaxation timescale, use τ ∝ M⁻¹ from this paper — Valentini's own earlier τ ∝ M⁻³ estimate is superseded and the numerics kill it.)*

### The ontology debt — currently the largest conceptual hole

**Ellis & Rothman are arguing *against* the block universe.** *"Our claim, by contrast, is that the future does not yet exist; at present the future is merely a set of possibilities."* Their whole arrow-of-time argument depends on it. They are also non-deterministic, and they explicitly reject integrating over the future — which cuts directly at the confirmation wave in §7.

So **#1 is unclaimed**. Nobody in the literature holds *full block + resolution as a real process* — Ellis escapes the tension by denying the future, Strubbe by adding τ.

### But confining the handshake to the front makes #1 idle

Once the offer and confirmation both stay inside the slab (§7), **nothing in the mechanism depends on the far future existing.** The absorber is in the front. The record forms in the front. The tail closes in the front. Delete the far block and no equation changes.

That is a large simplification and it should be treated as one:

- **The debt is discharged rather than paid.** We no longer owe an account of what resolution "does" to an already-existing future, because resolution never touches it.
- **Ellis's objection dissolves.** He rejects transactional accounts for needing a future to integrate over. We don't need one.
- **Strubbe's objection dissolves too.** He faults the transactional interpretation for not saying how bidirectional signals work in ordinary spacetime without an extra parameter. Confined to a slab of finite thickness, they are ordinary two-way propagation across a finite region — no parameter required.

**So τ is no longer needed, and should not be adopted.** Adopting it would import prior art, add a postulate, and buy something we now get for free. *This reverses the earlier recommendation in this section, which was written before the handshake was confined.*

### What #1 is now

**A preference, not a substrate.** Keep the full block if it is the ontology you believe; it costs nothing and contradicts nothing. But it is no longer load-bearing, and the paper should not present it as the foundation — a referee will ask what work it does, and the honest answer is none.

**The live question underneath it is different and smaller:** what is ahead of the front? If nothing reaches into it and nothing comes out of it, the framework is silent on it by construction. That is a defensible position — say it plainly rather than filling it with structure.

**One usable option if you want the future to be *something*:** it exists, it is ψ, and ψ has high coherence there. One entity, one property, varying along the axis. That needs no graded existence and no *potentia*, and it is §3's relational answer applied to the block. It is also close to Ellis's coarse-first/fine-later picture — cite him if you use it.

*(Ellis offers one further patch worth a paragraph if the handshake is ever un-confined: keep the transactional formalism but impose the "final condition" at the present time rather than at the end of the universe. The mathematics does not care where the final state sits.)*

---

## 10. The selection problem

> **What makes exactly one confirmation win — and why are the winners distributed as |ψ|² rather than some other way?**

This is the one thing that is fully, genuinely open. It is posits #10 and #16 in §11.

Candidate pictures for how competing tails resolve to one:
- **Racing** — first tail to close wins.
- **Matching** — the absorber whose local conditions best fit the offer wins.
- **Something else.**

Whichever is picked must cough up the Born weighting. That is the test everything else has been building toward.

**Status: unmoved, as far as we know.** Cramer (1986) appears never to have answered it — *inferred from Strubbe's silence; Cramer's paper is still unread ([SOURCES.md](SOURCES.md)). Read it before dating the problem to him.* **Strubbe does not answer it either** — his outcome is decided by comparing an intensity to a hidden variable he postulates *uniform on [0,1]*, and the Born weights appear precisely because he chose that distribution. That is fiat wearing a hidden variable's clothes.

**Two things follow.** The problem is not scooped — good. And nobody has a route through it — so attack it last, not first. It is constrained by everything above, and it *dissolves* rather than resolves if a definite beable gets added (Bohm's move: the particle always had one position, so nothing ever needed selecting).

**A warning taken from Strubbe.** He brands his framework "fundamentally deterministic" and then uses random numbers in both his models. That is exactly the gap between our #15 and #16. He got it past a referee. Don't count on the same.

---

## 11. The posit ledger

**Verdicts:** KEEP (load-bearing, ours) · PRIOR (load-bearing, someone else's — cite) · OPEN (load-bearing, unconstrained — declare) · RISK (in contact with a live experiment)

*October 2026 commitments are collected in §15. They extend this ledger rather than renumber it.*

### Structure

| # | Posit | Work it does | Verdict |
|---|---|---|---|
| 1 | Block universe; future exists as unresolved potential | ~~Substrate~~ — **none, since §7** | **IDLE** — keep as preference; not load-bearing; see §9 |
| 2 | "Now" is a slab with thickness; wake = resolved past | Makes resolution an event | **PRIOR** |
| 3 | Thickness is **informational** — measures undecidedness | One continuous parameter interpolating quantum↔classical | **KEEP** |
| 4 | Thickness = **coherence** | Makes #3 a number, not a metaphor | **KEEP** — provisional status discharged 6 Aug, Tests 1–2 passed ([RESULTS-01.md](RESULTS-01.md)). One restriction: well defined as a monotone along a resolution history, not as a cross-system absolute above d = 2 |

### The cell

| # | Posit | Work it does | Verdict |
|---|---|---|---|
| 5 | Cell = continuous blob, mathematically ψ; oscillates, carries phase | Fringe spacing | **PRIOR** — this *is* the wavefunction |
| 6 | Root stays connected | EPR without signalling: one blob, never two | **KEEP** |
| 7 | Cell straddles time — part in front, part in wake | Delayed choice, quantum eraser | **KEEP** |

### Resolution rule

| # | Posit | Work it does | Verdict |
|---|---|---|---|
| 8 | Resolution ⟸ which-path record (= entanglement); nonlocal. Quantified as growth of entanglement entropy | Which-path detector kills fringes | **PRIOR** — Zurek |
| 9 | Non-distinguishing coupling does **not** resolve — gravity included | Superposition survives the slits; gravity never collapses anything | **KEEP + RISK** — contested by Strubbe, §8. **8 Oct 2026: grounded by averaged gravity; carries the BMV prediction (§15).** |
| 10 | Exactly one tail closes per trial | Definite outcomes | **OPEN** — the selection problem, §10 |

### Handshake

| # | Posit | Work it does | Verdict |
|---|---|---|---|
| 11 | Offer wave ψ forward, confirmation ψ* back | Round trip | **PRIOR** — Cramer 1986 |
| 12 | Round trip ⟹ \|ψ\|² | The Born *square* | **PRIOR — and circular.** ψ* is defined as the conjugate |
| 13 | Wake not uniformly solid; tails dangle open | Delayed choice as a feature | **PRIOR** — Ellis, wording in §7 |
| 14 | ~~The returning confirmation closes the tail — timescale ~L/c~~ | ~~Resolution = thinning; explains what sets the slab's depth~~ | **FAILED 6 Aug.** The L-sweep ran ([RESULTS-01.md](RESULTS-01.md)): coherence lifetime does not track L. Exponent 0.00 where 1.00 was required, across three absorber implementations. Wrong-signed on the node branch. What does scale as L is record-formation time — time of flight, present in every theory. See §7 |

### Determinism

| # | Posit | Work it does | Verdict |
|---|---|---|---|
| 15 | Nothing is random; net conditions fix outcomes | Determinism, nonlocal HV | **PRIOR** — Bohmian family |
| 16 | Selection reproduces \|ψ\|² exactly; hidden conditions permanently unreadable | Empirical adequacy + no-signalling | **OPEN** — §10 |

### Summary

**October 2026:** #9 is now grounded by averaged gravity and carries the framework's one prediction (§15): no gravitational entanglement in BMV-type experiments. *(A second, on primordial gravitational waves, was parked 8 Oct: it does not follow from the first.)*

**Ours, load-bearing — 6 Aug, after the sims:** #3 informational thickness · #4 thickness = coherence, now confirmed (*the use* is ours; the measure is standard quantum information theory) · **#9 gravity never resolves — internally verified, and now the only empirical claim the framework carries.** ~~#14 confirmation closes the tail, ~L/c~~ **failed its test**; it survives only as the observation that record formation at a distant absorber takes L/c, which is time of flight and belongs to everyone.

**Ours, structurally (2):** #6 root connection · #7 time-straddling. Both do real work on EPR and delayed choice, though neither is far from what a nonlocal HV theory gives you anyway.

**Prior art — cite, don't claim (7):** #2, #5, #8, #11, #12, #13, #15.

**Unconstrained — declare openly (2):** #10, #16. Listing these is a strength; their omission is what draws the sharpest criticism of the transactional programme.

**Special case (1):** #1 — unclaimed, and now **idle**. Confining the handshake to the front removed its job. Keep it as a preference; don't build on it. §9.

---

## 12. Dead ends — recorded so they aren't re-walked

- **Fifth dimension as real substrate.** Nothing breaks if deleted. "Never static" is already free in 4D — four-velocity has invariant magnitude c, so a particle at rest moves through time at c.
- **Fifth dimension as mental model.** Fine, but then it can't ground the rest-frame patch. Can't be free and load-bearing at once.
- **Time as non-dimensional / emergent.** If the remaining ordered axis is what the front sweeps and the past sits behind, it *is* time renamed — deriving time from time. Also costs the block, the light cone, and Lorentz invariance. Genuine timeless programmes derive ordering rather than laying it down, and recovering Lorentz invariance is unsolved in every one.
- **Front encodes the past ⇒ holography.** That's determinism plus reversibility — true in Newtonian mechanics, needs no brane. Real holography is dimension-directional, not time-directional.
- **Volume burst driving expansion.** Arithmetic works (saturate and differentiate → de Sitter). Dies on: unitary evolution accumulates no records at all; it's an inequality with no saturation argument; we sit ~18 orders below the bound (10¹⁰⁴ vs ~10¹²²); and three expansion epochs can't come from one constant ratio.
- **Branching tree / graph instead of a front.** Dies on the sign: it predicts record-rich regions expand fastest, whereas dense regions expand slowest and collapse while near-empty voids expand fastest. Also, a branching graph isn't a manifold — no tangent space at nodes, so no metric and no Lorentz invariance.
- ~~**The entire gravity-origin story.** Front curvature = metric, resolution lag as time dilation. Cut: fed nothing back into measurement, carried all the empirical exposure.~~ **Reopened 7 Oct 2026** through the area-law route and tested ([RESULTS-02-gravity.md](RESULTS-02-gravity.md), §15). What stays dead is the next entry.
- **Settling load as the *cause* of time dilation** (7 Oct 2026). "More mass slows time because resolution takes time to process" fails three tests: reach (clock slowing extends through empty space: GPS, Galileo), universality (all clocks slow identically: MICROSCOPE), and direction (dense matter settles fast). Survives only as "the place slows everything, settling included."
- **Observer–observed clock-rate difference as the source of quantum behaviour** (4 Oct 2026 simulations). With realistic rates across 10⁻²⁰ to 10, no version produced interference or Bell correlations; the observer's clock drops out. Clock differences do the work *between a particle's alternative histories* instead, which is Feynman's sum over histories.
- **The vacuum as the future / the front advancing into vacuum** (7 Oct 2026). Empty space is rubber with no patterns; ahead of the front is the unsettled future. The balloon's "outside" is not space.

*Closing note, superseded 7 Oct 2026: "the front's variable advance rate suggests a connection to gravitational time dilation; say it in one sentence and do not pursue it." It was pursued, through the area law rather than through advance rate, and it passed its tests.*

---

## 13. Metaphor audit

Metaphors are not decorative here — they have repeatedly become commitments. "Slab" produced thickness. "Wavelength" produced h/p and cost several sessions. So they get audited like posits.

| Metaphor | Gave | Verdict |
|---|---|---|
| **Ember burning through paper** — front as flame, wake as ash | The **glowing margin**: ash isn't uniformly cold right behind the flame. That's #14 — a record exists but isn't final. Best picture yet of the L/c window. | **Keep.** The old objection — "paper never un-burns, but the eraser recovers coherence" — is **withdrawn**: the eraser doesn't un-burn anything either (below). |
| **Gap-wave** — vacancy propagating outward, not structure accreting | **Resolution as subtraction**: a superposition has more terms than its outcome, so resolution *removes*. More honest than "crystallizing," which is additive. Nearest real physics: Dirac hole theory, and Coleman–De Luccia false-vacuum decay (bubble wall converts false→true, resolved behind, undecided ahead — closest existing formalism). | **Keep the mechanism, drop the shells.** The hollow centre reintroduces a singular boundary at t=0. And the "refillable vacancy" payoff is **dead** — see the eraser note below. Watch the r² dilution problem: an outward wave on a sphere weakens as it spreads, predicting the universe becomes *less* classical with age. |
| **Entanglement as re-established prior unity** | — | **DEAD.** Entanglement swapping: two particles that never interacted and share no common origin can be entangled by a Bell measurement on their partners. Entanglement is created fresh between strangers, so it cannot be a record of prior contact. Also fails monogamy. The legitimate restricted version already exists as #6; keep that, do not generalise it. |
| **Entanglement propensity across the gap** | The area law (§6). Propensity isn't memory, so swapping doesn't touch it. | **Keep, renamed.** ~~It's locality, not gravity.~~ Since 7 Oct 2026 it is also the route to gravity. |
| **Balloon / vase** (Oct 2026) — rubber = 3D space, outward = time | Age = radius (cosmic time); the rubber's size at each age is separate, so it flares like a vase; dark energy shapes the flare. One time dimension falls out of the shape. | **Keep, as an analogy only.** Its "outside" is not space, and the vacuum is not the future. No fifth dimension unless it pays off. |
| **Fold** (Oct 2026) — unsettled past trailing behind the front | Quantum eraser, delayed choice, Wigner's friend (nested folds), black holes (a fold sealed by geometry). Change keeps ticking inside a fold; only the record lags. | **Keep.** Say "nested," not "fractal" — fractal structure was cut in §5. |
| **"The universe wants to smooth out folds"** (Oct 2026) | — | **Reworded.** Purpose language. Say "folds always close eventually, because links always spread." |

**The eraser does not work the way we assumed.** Englert's own experiment demonstrates *non-erasing quantum erasure*: interference is recovered from a **completely mixed** input, where there was no which-path information to erase in the first place. The mechanism is **sorting the run into sub-ensembles** — one showing fringes, one anti-fringes, summing to nothing — and keeping one. It does not undo a record; nothing gets backfilled. This removes the framework's embarrassment about the eraser, but by dissolving the question: post-selection needs no ontology.

---

## 14. Order of attack

*Steps 1–4 were executed on 6 August 2026. [RESULTS-01.md](RESULTS-01.md) has the numbers; the outcomes are written back into §3, §4, §7, §8 and §11.*

1. ~~Redesign Test 3 as the L-sweep.~~ **Done.** Six design requirements, model class fixed as waveguide QED, nulls specified in advance.
2. ~~Run Tests 1–2.~~ **Done — both pass.** Test 2 passes more strongly than asked: on the dephasing trajectory the which-path basis is the *maximising* basis over all bases, so thinness cannot be called an artefact of bookkeeping. #3 does not drop to decoration.
3. ~~Decide the dimensionality question.~~ **Decided: discrete which-path DOF for paper v1.** Test 1's follow-up settles the terms — the two valid measures agree perfectly along any resolution history in any dimension, and disagree on 13% of pairs when comparing unrelated states. So thickness is a monotone along a history, not a cross-system absolute. Continuous-variable coherence remains a separate project.
4. ~~Run the L-sweep.~~ **Done. It failed** (§7). Exponent 0.00 against the required 1.00, across three absorber implementations, with the effect causally excluded beyond L\* = v/γ.

**The remaining work, re-derived from the results:**

5. **Write the paper around #9 versus Strubbe** — **decided 8 Oct: the measurement note comes first; a gravity note only after item 7 passes.** *(Oct 2026: now with #9 grounded by averaged gravity, a semiclassical coupling claim with one prediction attached, §15)*. In August this was the only empirical content the framework had. Write it as a measurement note; the area-law material goes in an appendix titled as a compatibility check unless item 7 passes. The machinery to present with it is the resolution rule — thinning = environment distinguishability, verified exactly (§8) — and the thickness variable, verified (§3). Report the L-sweep as a negative result in its own section: it is a real contribution to have closed it.
6. **The selection problem** (§10). Last, and unmoved.

*Discharged, and recorded so they aren't re-opened:*
- *~~Fix the ontology.~~ Confining the handshake made #1 idle and removed the need for τ (§9).*
- *~~What sets front thickness?~~ Reading B derived it from L/c — and the L/c claim then failed its test. **Front thickness has no measured consequence.** Do not re-open either reading (§7).*
- *~~Long-baseline delayed choice may be fatal.~~ Dissolved by Reading B, and moot now that Reading B carries no empirical claim.*
- *~~Is thinness basis-tuned?~~ No. Settled numerically, not argued (§3, Test 2).*

**October 2026 — the remaining work, re-derived again:**

7. **Write the conserved source — the gate for the gravity reopening** *(promoted 8 Oct, [REVIEW.md](REVIEW.md) v4)*. A short note: the proposed Tμν, the event at which it changes from the average to the outcome, and a check that ∇·T = 0 everywhere, including at events the record has not reached. Start by asking whether the light-cone update rule is Tilloy & Diósi (2016), Oppenheim's postquantum classical gravity (2023), a variant of one, or something that fails where they succeed. **If no conserved source can be written, park gravity-origin again with a closing note, and keep #9 as a semiclassical bet.**
8. **Write the framework's own account of information leaving an evaporating black hole.** The recent Page-curve results lean on quantum gravity, which the framework no longer has. **Held until item 7 passes**, together with further balloon geometry: both would inherit a source not yet shown to exist.
9. **What sources the front's thickness?** Still open. The vacuum was ruled out as the source on 7 Oct.
10. **Work through the remaining Stress Map drafts**, rechecking every agreed item after each merge.
11. ~~Refresh [REVIEW.md](REVIEW.md).~~ **Done 8 Oct (v4).** [Framework-Summary-Plain.md](Framework-Summary-Plain.md) has a dated banner; the rewrite waits on item 7 (the charter was decided 8 Oct).
12. **Price the Newton–Schrödinger side effect** for one system already in the sources (a 25 kDa molecule, or a BMV mass pair), as a fractional effect on what the experiment measures. Until then, do not call it small.
13. **Derive prediction 2 inside RFF** (no quantized metric → tensor modes only at second order, after the inflaton settles), and check that the same settling gives the observed scalar spectrum. Start from León et al. (2015, 2017) and Perez, Sahlmann & Sudarsky (2006). Waits on item 7.

**Worth holding, and it has changed.** The framework's problems were all downstream of one vacant variable. The variable was filled, and it turned out to be a good variable — Tests 1, 2 and 4 all pass. What it does not have is a distinguishing prediction from front thickness; that was tested and it is gone. **What remained in August was one sharp bet against a named opponent (#9 vs Strubbe) and a coherent interpretation of standard open-system quantum mechanics.** That is a smaller claim than the project set out to make, and it is one that survived contact with a computer. *(8 Oct: §15 adds one coupling claim — an unsettled mass gravitates by its average — and its prediction of no gravitational entanglement in BMV-type experiments. That claim is semiclassical, and it stands only if item 7 passes.)*

---

## 15. October 2026 — the balloon, folds, and gravity

*Written 8 October 2026. Collects the commitments agreed between 4 and 8 October. The phenomenon-by-phenomenon record is the **RFF Stress Map**, exported to [stress-map/STRESS-MAP.md](stress-map/STRESS-MAP.md) (the live map is a private artifact: https://claude.ai/artifact/EvGt54gPa6abYXUgFogfrn; re-export after each merge). **Nothing on the map is done until all of it is done:** every status is provisional until every item is examined and the whole map rechecked; the gravity work is in [RESULTS-02-gravity.md](RESULTS-02-gravity.md) and the overnight findings doc "Gravity via the Area Law" (private: https://claude.ai/code/artifact/722ae576-bdd5-4803-8791-0ecc5ad8ef2e). Rule since 8 Oct: after every merge into the map, recheck every agreed item for anything the merge breaks.*

### Position

- **Charter (updated 8 Oct, replacing "a narrative around quantum mechanics, never a challenge to it").** RFF is an interpretation of quantum mechanics plus one semiclassical claim: an unsettled mass gravitates by its average. Everywhere else it adds a story, not dynamics. For gravity it is a physical theory, and it can be proved wrong by a BMV-type experiment. If the conserved source fails (§14 item 7), the claim is parked and RFF returns to an interpretation.
- **What can't be verified is left open, not explained.** A free interpretive choice is made where no experiment can tell the options apart, and recorded as a choice.

### Geometry — the balloon (an analogy)

- The rubber is 3D space; "outward" is time. No extra dimension unless it pays off. **The balloon's outside is not space.**
- The balloon's radius is the **age of the universe** (cosmic time). Local clocks run fast, slow or appear stuck: that is each region's own time.
- The rubber's size at each age is separate from the age: the balloon **flares like a vase**. Dark energy shapes the flare (the stretching), not the age.
- **c is the rubber's rate of change** and the boundary that makes order possible. Settling never spreads faster than c, and isn't timed by it (the #14 lesson).
- The **seed** is a point in spacetime, taken as a starting condition; it gives the beginning, and outward gives the arrow. A singularity is where an equation of state stops applying: bulk physics run back to where nothing had settled.
- One time dimension follows from the shape; three space dimensions are an input.

### Settling and folds

- The rubber is the front, the "now". **The front advances by settling.** Change and settling differ: inside a fold, change keeps ticking at the normal rate; what lags is the record.
- **Past ≠ settled.** The past holds the interaction (the link); it need not hold the outcome.
- **Folds:** where a system is shielded, the front leaves a fold of unsettled past behind it. A fold holds the whole linked region. Folds can be very long and **nest**. A fold closes by unfolding into its parent, and finally into the smooth rubber; only then is its result a fact for everyone.
- **A fold closes when undoing becomes impossible** (practical impossibility, no hidden size threshold), and it **really closes**. Every fold eventually closes: that is entropy rising. A reversal is recorded as an act, never as an outcome.
- **Results become facts across regions only when records can meet,** at light speed or slower. Until then, what is settled on one side is still open from the other. This is why entanglement can't signal. It refines §6's "resolution is nonlocal": the correlation is one blob's; when it becomes a shared fact is local. Closest prior art: Rovelli's relational QM, which differs in never making the facts shared.
- **Quantum at the rubber's leading edge, classical in its bulk;** least action shapes the bulk (it picks the path, not the outcome). Gravity is the exception: it is never quantum.

### The two-ended picture

- Both ends of a history are fixed; nothing is chosen at the slit. Probability belongs to a **pair of histories**, compared by their clock readings where they meet. Consistent with higher-order interference experiments: one particle, pairs only; M particles, order 2M.
- **Uncertainty:** settling anchors one quantity and solves the rest ("force x, y grows"). Not hidden values. What sets Planck's constant is open.
- **Particles are stable patterns in the rubber** (ripples, standing waves, vortices). Waviness comes from paired histories; the dot comes from settling.
- **The vacuum is not the future.** **There is no empty space** (Neil, 8 Oct): rubber with no settled patterns is still primed for a resolution event. Its linking is that priming — texture, not thickness, until something couples to it. Priming is readiness, not resolving: nothing settles in the vacuum on its own. It is what gravity keeps in balance.

### Gravity

- **Route:** the area law (Jacobson). Vacuum linking across any small surface scales with its area; an accelerating observer finds it warm (Unruh); energy crossing a surface changes the linking, and spacetime curves to keep it balanced, which gives Einstein's equations. G is an input; Λ is a free constant. **This is a compatibility argument, not a derivation from the front:** the framework supplies the area law only in part, and local equilibrium as a story. Lattice checks of the free-field first law (including the Wald term), and the tests that killed the settling-load mechanism: [RESULTS-02-gravity.md](RESULTS-02-gravity.md).
- **Resolution rate has two meanings:** (a) how fast the front advances (local clock rate) and (b) how much settles per tick. Near mass the rubber's shape slows the front and everything on it by the same factor; the cause is the place, not the settling load. **At balance, settling measured on a far-away clock is the same everywhere** (gravitational redshift; Tolman–Ehrenfest).
- **Settled mass:** gravity follows the outcome, because folds really close (consistent with Page & Geilker 1981).
- **Unsettled mass gravitates by its average** (decided 8 Oct). **Gravity is never quantum:** it is the rubber's equation of state. Side effect: a spread-out heavy mass feels its own averaged pull (Newton–Schrödinger), a departure from plain QM, not yet priced (§14 item 12).
- **Open — the source.** "A distant mass keeps pulling from its average until records can meet" is a rule for observers, not yet a conserved stress tensor. §14 item 7 is the gate: no conserved source, no reopening.
- **"Never quantum" in the broad sense** (Neil, 8 Oct): no quantized metric anywhere, not only for lab masses.
- **Two predictions:** (1) BMV-type experiments will see no entanglement through gravity; (2) primordial gravitational waves of quantum origin are **strongly suppressed** — with no quantum metric, tensor modes arise only at second order, after the inflaton's fluctuations settle (León, Sudarsky and colleagues get this in semiclassical gravity with collapse). Prediction 1 follows from averaged gravity; prediction 2 needs the broad sense, and its derivation inside RFF is owed (§14 item 13). [RESULTS-02-gravity.md](RESULTS-02-gravity.md).
- **Black holes** *(held until §14 item 7 passes)*: no clock stops anywhere. Near the horizon, churn per tick grows without limit and ticks slow without limit, seen from far away. The cause is the place (hovering takes ever-larger acceleration), not density. A black hole is a fold sealed by geometry, closed by evaporation.

### Consistency notes against §1–§14

- **#1** (block, future as potential) stays idle. The October geometry doesn't lean on it.
- **#9** is grounded by averaged gravity (§8) and carries prediction 1.
- **#14** stays failed. Nothing in this section times settling by L/c.
- **§6 "resolution is nonlocal"** is refined, not reversed (above).
- **§9's Born-by-relaxation:** its distinguishing regime was cosmological and set aside by the July scope cut. The scope is wider now; that regime has not been re-examined.
- **§3 front thickness:** still unsourced. The vacuum was ruled out as the source on 7 Oct. Open.
