"""W2 tail measurement (11 Oct). A measurement, not a test.

Written after the W2 second test failed its floor condition (RESULTS-04):
at t_rec = 1.5, the record's error (TV over 20 bins) was 0.0054, about twice
the noise floor (0.0027). This script asks one question: does the W2 tail
reach Born later, and how fast? It cannot change any verdict.

Set-up: as nelson_rerun.py at sigma = 0.4 (N = 4e5, dt = 1e-4, start at x = +-a),
run to t = 6. A Born start runs over the same time as a control, so that
integrator drift over the longer run would show.
Fresh streams: default_rng([2026, 10, 11, 40, 3]) for the main run,
[2026, 10, 11, 40, 4] for the control kicks, [2026, 10, 11, 40, 5] for the
control start points.
Output at t = 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6: TV over 20 bins and L1 over
100 bins, each with equal Born weight, and their noise floors (TV is half the
sum over bins).

Usage:  python nelson_tail.py
"""
import json
import time

import numpy as np

import nelson1d as n1
import rng as rs

N, DT, S, A = n1.N, n1.DT, 0.4, n1.A
TIMES = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
OUT = "results/"


def metrics(X, t):
    c100 = np.bincount(np.searchsorted(n1.edges(t, S, 100), X), minlength=100) / N
    c20 = np.bincount(np.searchsorted(n1.edges(t, S, 20), X), minlength=20) / N
    return float(np.abs(c100 - 0.01).sum()), float(0.5 * np.abs(c20 - 0.05).sum())


def run(X, st, label):
    rows = []
    t0 = time.time()
    for k, t in enumerate(TIMES):
        if k > 0:
            n1.advance(X, st, TIMES[k - 1], int(round((t - TIMES[k - 1]) / DT)), DT, S)
        L, T = metrics(X, t)
        rows.append(dict(t=t, L1=L, TV=T))
        print(f"{label} t={t}: L1 {L:.4f}  TV {T:.5f}  ({time.time() - t0:.0f}s)", flush=True)
    return rows


def main():
    g = np.random.default_rng(20261013)
    d100 = g.multinomial(N, np.full(100, 0.01), size=200) / N
    d20 = g.multinomial(N, np.full(20, 0.05), size=200) / N
    L1f = np.abs(d100 - 0.01).sum(1)
    TVf = 0.5 * np.abs(d20 - 0.05).sum(1)
    floors = dict(L1=(float(L1f.mean()), float(L1f.std())), TV=(float(TVf.mean()), float(TVf.std())))
    print("floors", floors, flush=True)
    X = np.where(np.arange(N) % 2 == 0, A, -A).astype(float)
    main_rows = run(X, rs.states(N, [2026, 10, 11, 40, 3]), "main")
    Xc = n1.sample_born(N, 0.0, S, np.random.default_rng([2026, 10, 11, 40, 5]))
    ctrl_rows = run(Xc, rs.states(N, [2026, 10, 11, 40, 4]), "control")
    json.dump(dict(floors=floors, main=main_rows, control=ctrl_rows), open(OUT + "tail_w2.json", "w"), indent=1)


if __name__ == "__main__":
    main()
