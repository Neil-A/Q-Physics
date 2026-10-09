# Q-Physics — The Resolution-Front Framework

A working research repository. It started on the double slit and the measurement problem; since
October 2026 it tests how much known physics, small and large, the framework can fit.

**Status as of 8 October 2026:** the scope has widened from the double slit to "how much known
physics fits." Gravity-origin was reopened on 7 October through the area-law route. The old
"settling load slows time" mechanism is dead; the free-field entanglement first law checks out
on a lattice. Gravity is not derived: G is an input, and the route is a compatibility argument
with Jacobson. The framework's addition is a coupling rule — an unsettled mass gravitates by its
average, and there is no quantized metric anywhere. Two predictions: no gravity-mediated
entanglement in BMV-type experiments, and strongly suppressed primordial gravitational waves of
quantum origin (derivation owed). **Open, and the gate for the reopening:** a conserved source for that rule (FRAMEWORK.md §14 item 7). See
[RESULTS-02-gravity.md](RESULTS-02-gravity.md), FRAMEWORK.md §15, and [REVIEW.md](REVIEW.md) v4.

**Earlier (9 August 2026):** the framework's single distinguishing prediction — coherence
lifetime tracking absorber distance *L* — was tested on 6 August and **failed**. Posit #9
passed its internal check exactly. See [RESULTS-01.md](RESULTS-01.md).

**Charter (updated 8 October 2026):** RFF is an interpretation of quantum mechanics plus one
physical claim about gravity. Everywhere else it follows standard quantum mechanics and adds a
story, not dynamics. For the gravity of unsettled masses it departs: such a mass gravitates by
its average. There RFF is a semiclassical theory, and it can be proved wrong by experiment.

## Where to start

| If you want | Read |
|---|---|
| The idea, no jargon | [Framework-Summary-Plain.md](Framework-Summary-Plain.md) — predates October and contradicts §15 on gravity |
| The full argument and all sixteen posits (canonical) | [FRAMEWORK.md](FRAMEWORK.md) |
| How known physics fits, item by item (provisional until all items are done) | [stress-map/STRESS-MAP.md](stress-map/STRESS-MAP.md) |
| What the simulations actually returned | [RESULTS-01.md](RESULTS-01.md) (coherence), [RESULTS-02-gravity.md](RESULTS-02-gravity.md) (gravity), [RESULTS-03-amplitudes.md](RESULTS-03-amplitudes.md) (amplitudes) |
| Current status, risks, next actions | [REVIEW.md](REVIEW.md) — v4, 8 October, with a response section |
| The independent review of the amplitude work, and its brief | [REVIEW-03-amplitudes.md](REVIEW-03-amplitudes.md) (verdict: kill condition 1 met), [REVIEW-BRIEF-03-amplitudes.md](REVIEW-BRIEF-03-amplitudes.md) |
| The literature, and what each paper was read for | [SOURCES.md](SOURCES.md) |
| The computational specs | [SIM-SPEC-01-coherence.md](SIM-SPEC-01-coherence.md) (coherence), [SIM-SPEC-02-amplitudes.md](SIM-SPEC-02-amplitudes.md) (amplitudes from ordering) |
| The code | [sim/](sim/) |

## Reproducing the simulations

```bash
cd sim
python -m venv .venv && .venv/Scripts/activate   # Windows; use .venv/bin/activate elsewhere
python -m pip install -r requirements.txt
python test1_endpoints.py && python test1b_ordering.py && python test2_chair.py \
  && python test3_lsweep.py && python test3b_followup.py && python test3c_atom.py \
  && python test4_bounds.py && python make_figures.py
```

Verified on Python 3.13 with the pinned versions in [sim/requirements.txt](sim/requirements.txt).
Runs in a few minutes. Raw JSON and figures are committed under `sim/results/` so the recorded
outcome can be compared against a fresh run.

See [sim/README.md](sim/README.md) for what each test does.

The gravity checks (October) live in [sim/gravity/](sim/gravity/) and need only NumPy and SciPy:

```bash
cd sim/gravity
python first_law.py && python rindler_scan.py && python ball3d_squeeze.py && python ball3d_fit.py && python tests_2_4.py
```

About a minute. See [sim/gravity/README.md](sim/gravity/README.md).

## A note on `papers/`

The `papers/` directory holds PDFs of published journal articles and is **excluded from this
repository** — they are copyrighted and not mine to redistribute. Full citations for every one
of them are in [SOURCES.md](SOURCES.md). Links to `papers/` elsewhere in these documents will
not resolve on GitHub; they work in a local checkout if you supply the PDFs yourself.
