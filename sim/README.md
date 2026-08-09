# sim/ — SIM-SPEC-01 implementation

Executes [SIM-SPEC-01-coherence.md](../SIM-SPEC-01-coherence.md). Results and interpretation in [RESULTS-01.md](../RESULTS-01.md).

## Setup

```bash
python -m venv .venv && .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Verified on Python 3.13 with the pinned versions in `requirements.txt`.

## Run

```bash
python test1_endpoints.py && python test1b_ordering.py && python test2_chair.py && python test3_lsweep.py && python test3b_followup.py && python test3c_atom.py && python test4_bounds.py && python make_figures.py
```

Whole suite is a few minutes. Everything writes JSON to `results/`.

## Files

| File | What it does |
|---|---|
| `common.py` | Coherence measures, entropies, lifetime extraction, power-law fits. `c_l2_INVALID` exists only to demonstrate the BCP counterexample — never use it as a measure. |
| `waveguide.py` | The Test 3 model: 1D tight-binding waveguide, emitter at one site, terminator at L sites. Three terminator types (absorbing potential, mirror, real absorbing atom). |
| `test1_endpoints.py` | Endpoints, monotonicity, the inversion, dimension scaling, l₂ counterexample |
| `test1b_ordering.py` | Follow-up: do the two valid measures agree on ordering, and where |
| `test2_chair.py` | Coherence vs environment size; the basis question; the #9 watch clause |
| `test3_lsweep.py` | The L-sweep proper, plus nulls, record-formation time, convergence |
| `test3b_followup.py` | Fine L scan, node branch, max local slope, the causal bound L\* = v/γ |
| `test3c_atom.py` | Third absorber implementation: a real absorbing atom with an irreversible record |
| `test4_bounds.py` | Englert and Streltsov, as code-correctness checks |
| `make_figures.py` | Figures. `results/fig3_lsweep.png` is the one that matters. |

## Two things to know before changing anything

**Coherence in the waveguide model is `|c_e(t)|`** — the amplitude still on the emitter. Once the photon is in the field, that branch is orthogonal to the un-emitted branch in the field sector, so it contributes to the ground-state population and not to coherence. Getting this wrong makes the whole L-sweep meaningless.

**Do not extract lifetimes with a late-window log-linear fit.** The mirror configuration produces a two-stage curve — free decay, then a frozen residue from the bound state — so a late fit measures the plateau and returns spurious infinities. It was tried, it gave nonsense (`max_local_slope` of 3.7 that vanished on inspection), and it was replaced. Use `lifetime_1e` for the decay and report the plateau separately.

**Keep `cap_len < left_pad`** in the waveguide, or the emitter sits inside the left absorbing ramp and the absolute lifetime shifts by ~1.6%.
