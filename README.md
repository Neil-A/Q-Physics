# Q-Physics — The Resolution-Front Framework

A working research repository on the double slit and the measurement problem.

**Status as of 9 August 2026:** the framework's single distinguishing prediction — coherence
lifetime tracking absorber distance *L* — was tested on 6 August and **failed**. The live
claim is posit #9, which passed its internal check exactly. See
[RESULTS-01.md](RESULTS-01.md) before reading anything else.

**Scope:** the double slit and the measurement problem. Gravity-as-origin and cosmology were
cut in July and are out of scope.

## Where to start

| If you want | Read |
|---|---|
| The idea, no jargon | [Framework-Summary-Plain.md](Framework-Summary-Plain.md) |
| The full argument and all sixteen posits (canonical) | [FRAMEWORK.md](FRAMEWORK.md) |
| What the simulations actually returned | [RESULTS-01.md](RESULTS-01.md) |
| Current status, risks, next actions | [REVIEW.md](REVIEW.md) |
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

## A note on `papers/`

The `papers/` directory holds PDFs of published journal articles and is **excluded from this
repository** — they are copyrighted and not mine to redistribute. Full citations for every one
of them are in [SOURCES.md](SOURCES.md). Links to `papers/` elsewhere in these documents will
not resolve on GitHub; they work in a local checkout if you supply the PDFs yourself.
