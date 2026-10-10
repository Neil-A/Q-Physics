# sim/selection — code for SIM-SPEC-03 (selection)

This folder holds the code for [SIM-SPEC-03](../../SIM-SPEC-03-selection.md). The spec fixes every pass condition before any run. Each script repeats the rules it uses at the top of the file.

| File | What it does | Test |
|---|---|---|
| `box2d.py` | Rule W1 (pilot-wave guidance) in the 2D box of Towler, Russell & Valentini 2012 | 1a, and the W1 part of 2 |
| `analyse_box.py` | H̄, TV, noise floors, fits and verdicts for the box runs | 1a, 2 (W1) |
| `nelson1d.py` | Rule W2 (Nelson) in the double slit of Hardel, Hervieux & Manfredi 2023, with its analysis | 1b, and the W2 part of 2 |
| `signal2p.py` | Two entangled particles; a local pulse at A; B's statistics | 3 |
| `rng.py` | One random stream for each seed, inside numba loops | used by W2 |
| `run_box.sh` | All W1 runs in order, checks first | 1a, 2 |

## How to run

Install the packages in [../requirements.txt](../requirements.txt) (numpy, scipy, numba). Then, from this folder:

1. Run `./run_box.sh`. It takes some hours on two cores.
2. Run `python3 nelson1d.py equiv`, then `step`, then `main`, then `analyse`.
3. Run `python3 signal2p.py`.

Each run writes its raw output to `results/` as `.npz` files. Each analysis writes a `.json` file and a `_console.txt` file with the verdicts.

## Rules that apply to every run

- Each test has set-up checks from known physics (equivariance, step size, closed forms). If a check fails, the code is wrong, and the pass condition is not valid.
- The random seeds are fixed in the code, so each run gives the same numbers again.
- A change after a run started is written in the docstring of the script, with its reason. A run that a change replaced stays in `results/` with `FAILED` in its name.
