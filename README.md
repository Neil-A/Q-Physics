# Q-Physics — The Resolution-Front Framework

A working research repository. It started on the double slit and the measurement problem; since
October 2026 it tests how much known physics, small and large, the framework can fit.

**Status as of 8 October 2026:** the scope has widened from the double slit to "how much known
physics fits." Gravity-origin was reopened on 7 October through the area-law route and passed
its four tests; an unsettled mass gravitates by its average, so the framework predicts no
gravity-mediated entanglement and no primordial gravitational waves of quantum origin. See
[RESULTS-02-gravity.md](RESULTS-02-gravity.md), and FRAMEWORK.md §15.

**Earlier (9 August 2026):** the framework's single distinguishing prediction — coherence
lifetime tracking absorber distance *L* — was tested on 6 August and **failed**. Posit #9
passed its internal check exactly. See [RESULTS-01.md](RESULTS-01.md).

**Scope:** RFF is a narrative around quantum mechanics, not a challenge to it. It departs from
it only for the gravity of unsettled masses, where experiments haven't yet reached.

## Where to start

| If you want | Read |
|---|---|
| The idea, no jargon | [Framework-Summary-Plain.md](Framework-Summary-Plain.md) — predates October |
| The full argument and all sixteen posits (canonical) | [FRAMEWORK.md](FRAMEWORK.md) |
| What the simulations actually returned | [RESULTS-01.md](RESULTS-01.md) (coherence), [RESULTS-02-gravity.md](RESULTS-02-gravity.md) (gravity) |
| Current status, risks, next actions | [REVIEW.md](REVIEW.md) — predates October; FRAMEWORK.md §14–§15 are current |
| The literature, and what each paper was read for | [SOURCES.md](SOURCES.md) |
| The computational spec | [SIM-SPEC-01-coherence.md](SIM-SPEC-01-coherence.md) |
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
