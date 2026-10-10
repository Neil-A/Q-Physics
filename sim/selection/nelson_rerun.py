"""SIM-SPEC-03 section 5.6: the W2 second test (Test 1b report and Test 2 for W2).

Why: in the first W2 run (RESULTS-04) the step check failed on tau_q, the
fitted relaxation time of Hardel et al., whose fit was degenerate. Neil
approved (10 Oct) a rerun on fresh seeds with a relaxation time that needs no
fitted curve. This is a second test: Claude saw the first run before writing it.

Unchanged from nelson1d.py: the double slit, the dynamics (drift, Euler-
Maruyama), s in {0.2, ..., 0.7}, N = 4e5, dt = 1e-4, start at x = +-a, t to 1.5,
100 and 20 bins of equal Born weight, multinomial noise floors.

Changes (fixed before any run, SIM-SPEC-03 section 5.6):
  fresh streams: kicks default_rng([2026, 10, 11, round(100 s), 0]);
                 Born start (equivariance) [2026, 10, 11, 40, 1];
  output every 1e-4 to t = 0.01, every 1e-3 to 0.1, every 1e-2 to 1.5;
  t_half = first time L1 <= L1(0)/2, linear interpolation between outputs;
  t_3 = first output time with L1 <= 3 x floor (report only).
Checks: equivariance (L1 of the Born start <= floor + 5 sd at every output);
  step size (t_half at dt 1e-4 and 5e-5 agree within 5%, s = 0.2 and 0.7;
  report the largest L1 difference too).
Test 1b (second test): report only: t_half, t_3, tau_int (literal and visible
  peak), L1 at the literal tau_int.
Test 2 (second test, W2, s = 0.4): PASS if the half time of TV (20 bins) lies
  between 0.25 t_half and 4 t_half, and TV(1.5) < floor + 3 sd.

Usage:  python nelson_rerun.py equiv|step|main|analyse
"""
import json
import sys
import time

import numpy as np

import nelson1d as n1
import rng as rs

N = n1.N
DT = n1.DT
SIGMAS = n1.SIGMAS
A = n1.A
KL1, KTV = 100, 20
TIMES = np.unique(np.round(np.concatenate([np.arange(0, 101) * 1e-4,
                                           0.01 + np.arange(1, 91) * 1e-3,
                                           0.1 + np.arange(1, 141) * 1e-2]), 10))
OUT = "results/"


def run(s, kind):
    dt = 5e-5 if kind == "step" else DT
    st = rs.states(N, [2026, 10, 11, round(100 * s), 0])
    if kind == "equiv":
        X = n1.sample_born(N, 0.0, s, np.random.default_rng([2026, 10, 11, 40, 1]))
    else:
        X = np.where(np.arange(N) % 2 == 0, A, -A).astype(float)
    C1 = np.zeros((len(TIMES), KL1), np.int64)
    C2 = np.zeros((len(TIMES), KTV), np.int64)
    t0 = time.time()
    for k, t in enumerate(TIMES):
        if k > 0:
            m = int(round((t - TIMES[k - 1]) / dt))
            n1.advance(X, st, TIMES[k - 1], m, dt, s)
        C1[k] = np.bincount(np.searchsorted(n1.edges(t, s, KL1), X), minlength=KL1)
        C2[k] = np.bincount(np.searchsorted(n1.edges(t, s, KTV), X), minlength=KTV)
    el = time.time() - t0
    name = f"{OUT}rerun_{kind}_s{round(100 * s):02d}.npz"
    np.savez_compressed(name, times=TIMES, c100=C1, c20=C2, sigma=s, N=N, dt=dt,
                        nonfinite=int(np.sum(~np.isfinite(X))), seconds=el)
    print(f"{kind} sigma={s}: {el:.0f}s -> {name}", flush=True)


# ---------------------------------------------------------------- analysis
gen = np.random.default_rng(20261012)


def floor(K):
    d = gen.multinomial(N, np.full(K, 1.0 / K), size=200) / N
    m = np.abs(d - 1.0 / K).sum(axis=1)
    return float(m.mean()), float(m.std())


def half_time(t, y):
    """First time y falls to y(0)/2, by linear interpolation between outputs."""
    j = int(np.argmax(y <= y[0] / 2))
    assert j > 0 and y[j] <= y[0] / 2, "never reaches half"
    return float(t[j - 1] + (y[0] / 2 - y[j - 1]) * (t[j] - t[j - 1]) / (y[j] - y[j - 1]))


def curves(name):
    d = np.load(name)
    L = np.abs(d["c100"] / N - 1 / KL1).sum(axis=1)
    TV = 0.5 * np.abs(d["c20"] / N - 1 / KTV).sum(axis=1)
    return d["times"], L, TV, d


def analyse():
    log = []
    say = lambda x: (print(x, flush=True), log.append(x))
    fl1, sd1 = floor(KL1)
    fl2, sd2 = floor(KTV)
    say(f"Floors (N = {N}): L1 {fl1:.4f} ± {sd1:.4f}; TV over 20 bins {fl2:.4f} ± {sd2:.4f}")
    res = dict(floors=dict(L1=(fl1, sd1), TV20=(fl2, sd2)), checks={}, sigma={}, test2_w2={})

    t, L, _, _ = curves(OUT + "rerun_equiv_s40.npz")
    ok_eq = bool(np.all(L <= fl1 + 5 * sd1))
    say(f"Check, equivariance (sigma=0.4, Born start): max L1 {L.max():.4f}, limit {fl1 + 5 * sd1:.4f} "
        f"-> {'OK' if ok_eq else 'FAILED'}")
    step = {}
    for s in (0.2, 0.7):
        ta, La, _, _ = curves(f"{OUT}rerun_main_s{round(100 * s):02d}.npz")
        tb, Lb, _, _ = curves(f"{OUT}rerun_step_s{round(100 * s):02d}.npz")
        ha, hb = half_time(ta, La), half_time(tb, Lb)
        m = La > 3 * fl1
        dmax = float(np.abs(La - Lb)[m].max())
        step[str(s)] = dict(t_half_dt1e4=ha, t_half_dt5e5=hb, rel=abs(ha - hb) / ha, max_L1_diff=dmax)
        say(f"Check, step size (sigma={s}): t_half {ha:.5f} at dt 1e-4, {hb:.5f} at 5e-5, "
            f"difference {100 * abs(ha - hb) / ha:.2f}%; largest L1 difference {dmax:.4f}")
    ok_st = all(v["rel"] < 0.05 for v in step.values())
    say(f"Check, step size -> {'OK' if ok_st else 'FAILED'}")
    valid = ok_eq and ok_st
    res["checks"] = dict(equivariance=ok_eq, equiv_max_L1=float(L.max()), step=ok_st, step_detail=step)

    say("Test 1b, second test (report only):")
    store = {}
    for s in SIGMAS:
        t, L, TV, d = curves(f"{OUT}rerun_main_s{round(100 * s):02d}.npz")
        th = half_time(t, L)
        t3 = float(t[np.argmax(L <= 3 * fl1)]) if np.any(L <= 3 * fl1) else None
        lit, num, vis = n1.tau_int(s)
        Llit = float(np.exp(np.interp(lit, t, np.log(L))))
        res["sigma"][str(s)] = dict(t_half=th, t_3=t3, tau_int_literal=lit, tau_int_visible=vis,
                                    L1_at_literal=Llit, L1_start=float(L[0]), L1_end=float(L[-1]),
                                    L1_tail_over_floor=float(L[t >= 1].mean() / fl1),
                                    nonfinite=int(d["nonfinite"]), seconds=float(d["seconds"]))
        store[str(s)] = dict(t=t.tolist(), L1=L.tolist(), TV=TV.tolist())
        say(f"  sigma={s}: t_half {th:.4f}; t_3 {t3}; tau_int literal {lit:.4f}, visible {vis:.4f}; "
            f"tau_int/t_half {lit / th:.1f}; t_3/tau_int {t3 / lit if t3 else float('nan'):.2f}; "
            f"L1 at literal tau_int {Llit:.4f} ({100 * Llit / L[0]:.1f}% of start)")

    t, L, TV, _ = curves(OUT + "rerun_main_s40.npz")
    thL, thT = half_time(t, L), half_time(t, TV)
    ratio = thT / thL
    p1 = bool(0.25 <= ratio <= 4.0)
    band = fl2 + 3 * sd2
    p2 = bool(TV[-1] < band)
    say(f"Test 2 W2 (sigma=0.4), second test: TV {TV[0]:.3f} -> {TV[-1]:.4f} at t = 1.5 (band {band:.4f}) -> {p2}")
    say(f"  TV half time {thT:.5f}; L1 half time {thL:.5f}; ratio {ratio:.2f} (band 0.25 to 4) -> {p1}")
    say(f"TEST 2 (W2), second test: {'PASS' if (p1 and p2) else 'FAIL'}"
        + ("" if valid else "  -- PENDING: a check failed (spec section 6)"))
    res["test2_w2"] = dict(t_half_TV=thT, t_half_L1=thL, ratio=ratio, pass_timescale=p1, tv_end=float(TV[-1]),
                           band=band, pass_floor=p2, passed=bool(p1 and p2), valid=valid)
    res["curves"] = store
    with open(OUT + "rerun_w2.json", "w") as f:
        json.dump(res, f)
    with open(OUT + "rerun_w2_console.txt", "w") as f:
        f.write("\n".join(log) + "\n")


def main():
    kind = sys.argv[1]
    if kind == "main":
        for s in SIGMAS:
            run(s, "main")
    elif kind == "step":
        for s in (0.2, 0.7):
            run(s, "step")
    elif kind == "equiv":
        run(0.4, "equiv")
    elif kind == "analyse":
        analyse()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
