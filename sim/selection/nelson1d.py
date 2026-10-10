"""SIM-SPEC-03 Test 1b (W2 relaxes as published) and the W2 part of Test 2.

The model is the 1D double slit of Hardel, Hervieux & Manfredi 2023, section 4.1:
  hbar = m = a = 1,
  psi(x, 0) = Nrm [exp(-(x+a)^2 / 2 s^2) + exp(-(x-a)^2 / 2 s^2)],
  Nrm = [2 sqrt(pi) s (1 + exp(-a^2/s^2))]^(-1/2), free motion after t = 0.
  (Their Eq. 10 prints sqrt(pi s); the overlap factor fixes it as sqrt(pi) s.)
Free motion of one Gaussian: g(y, t) = sqrt(s^2/S) exp(-y^2 / 2S), S = s^2 + i t.

Rule W2 (Nelson): dX = b dt + sqrt(2D) dW, D = 1/2, b = Im(psi'/psi) + Re(psi'/psi).
Integrator: Euler-Maruyama, dt = 1e-4 (step check: 5e-5). Each seed has its own
random stream (rng.py).
Start: all seeds at x = +a or x = -a, half at each (their Eq. 11).
N = 4e5. Output every 1e-3 to t = 0.1, then every 1e-2 to t = 1.5.
At each output time the code stores counts in 100 bins and in 20 bins. Each bin
has Born weight 1/100 (or 1/20) at that time (edges from the exact |psi|^2).

Runs (fixed before any run, 10 Oct 2026; SIM-SPEC-03 section 5):
  main   s in {0.2, 0.3, 0.4, 0.5, 0.6, 0.7}
  step   s in {0.2, 0.7} with dt = 5e-5
  equiv  s = 0.4, seeds from the exact Born spread (equivariance check)
Random streams: default_rng([2026, 10, 10, round(100 s), k]) with k = 0 for
the noise and k = 1 for the Born start. The step runs use the same noise seed.

Analysis (fixed before any run):
  Floors: 200 multinomial draws of N seeds over equal-weight bins; floor =
  mean of the metric, spread = standard deviation.
  L1 = sum over the 100 bins of |count/N - 1/100|.
  Fit ln L1 = ln a1 - a2 exp(a3 t) (their Eq. 14) to every point with
  L1 > 3 x floor. tau_q = 1/(a2 a3) (their definition).
  tau_int, literal definition: first time |psi|^2 has a local maximum at x = 0,
  = s^2 sqrt((a^2 - s^2)/(a^2 + s^2)) (the code also checks this numerically).
  tau_int, second definition (visible peak): first time the maximum at x = 0
  stands at least 10% of the highest peak above the next minimum.
  Checks: figure (s = 0.09, t = 0.12: local maximum at x = 0); equivariance
  (L1 of the Born start <= floor + 5 sd at every output time); step size
  (tau_q at dt 1e-4 and 5e-5 agree within 5%, s = 0.2 and 0.7).
  TEST 1b PASS: tau_q < tau_int (literal) for every s. PARTIAL: only with the
  second definition. FAIL: tau_q >= tau_int with both, for any s.
  TEST 2 (W2), s = 0.4: TV = half the sum over the 20 bins of |count/N - 1/20|.
  t_half = first time TV <= TV(0)/2 (linear interpolation between outputs).
  PASS: 0.25 tau_q <= t_half <= 4 tau_q, and TV(1.5) < floor + 3 sd.

Usage:  python nelson1d.py main|step|equiv|analyse
"""
import json
import math
import sys
import time

import numba as nb
import numpy as np
from scipy.optimize import curve_fit

import rng as rs

A = 1.0
N = 400_000
DT = 1e-4
SIGMAS = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
TIMES = np.concatenate([np.round(np.arange(0, 101) * 1e-3, 10),
                        np.round(0.1 + np.arange(1, 141) * 1e-2, 10)])
KL1, KTV = 100, 20
OUT = "results/"


@nb.njit(fastmath=True)
def drift(x, t, s):
    """b = Im(r) + Re(r), r = psi'/psi, with one complex exponential (no overflow)."""
    S = complex(s * s, t)
    if x >= 0.0:
        q = np.exp(-2.0 * A * x / S)
        r = -((x - A) + (x + A) * q) / (S * (1.0 + q))
    else:
        q = np.exp(2.0 * A * x / S)
        r = -((x - A) * q + (x + A)) / (S * (q + 1.0))
    return r.imag + r.real


@nb.njit(fastmath=True, parallel=True)
def advance(X, st, t0, nsteps, dt, s):
    sq = math.sqrt(dt)
    for i in nb.prange(X.shape[0]):
        x = X[i]; z = st[i]; t = t0; n2 = 0.0
        for k in range(nsteps):
            if k % 2 == 0:
                z, n1, n2 = rs.normal_pair(z)
                w = n1
            else:
                w = n2
            x += drift(x, t, s) * dt + sq * w
            t += dt
        X[i] = x; st[i] = z


def rho(x, t, s):
    S = s * s + 1j * t
    g = lambda y: np.sqrt(s * s / S) * np.exp(-y * y / (2 * S))
    nrm = 1.0 / (2 * np.sqrt(np.pi) * s * (1 + np.exp(-A * A / (s * s))))
    return nrm * np.abs(g(x - A) + g(x + A)) ** 2


def grid(t, s):
    w = np.sqrt((s ** 4 + t * t) / (2 * s * s))
    return np.linspace(-A - 12 * w, A + 12 * w, 40001)


def edges(t, s, K):
    x = grid(t, s)
    r = rho(x, t, s)
    c = np.concatenate([[0], np.cumsum(0.5 * (r[1:] + r[:-1]) * np.diff(x))])
    assert abs(c[-1] - 1) < 1e-6, c[-1]
    return np.interp(np.arange(1, K) / K, c / c[-1], x)


def sample_born(n, t, s, gen):
    x = grid(t, s)
    r = rho(x, t, s)
    c = np.concatenate([[0], np.cumsum(0.5 * (r[1:] + r[:-1]) * np.diff(x))])
    return np.interp(gen.uniform(0, 1, n), c / c[-1], x)


def run(s, kind):
    dt = 5e-5 if kind == "step" else DT
    st = rs.states(N, [2026, 10, 10, round(100 * s), 0])
    if kind == "equiv":
        X = sample_born(N, 0.0, s, np.random.default_rng([2026, 10, 10, round(100 * s), 1]))
    else:
        X = np.where(np.arange(N) % 2 == 0, A, -A).astype(float)
    C1 = np.zeros((len(TIMES), KL1), np.int64)
    C2 = np.zeros((len(TIMES), KTV), np.int64)
    t0 = time.time()
    for k, t in enumerate(TIMES):
        if k > 0:
            n = int(round((t - TIMES[k - 1]) / dt))
            advance(X, st, TIMES[k - 1], n, dt, s)
        C1[k] = np.bincount(np.searchsorted(edges(t, s, KL1), X), minlength=KL1)
        C2[k] = np.bincount(np.searchsorted(edges(t, s, KTV), X), minlength=KTV)
    el = time.time() - t0
    name = f"{OUT}nelson_{kind}_s{round(100 * s):02d}.npz"
    np.savez_compressed(name, times=TIMES, c100=C1, c20=C2, sigma=s, N=N, dt=dt,
                        nonfinite=int(np.sum(~np.isfinite(X))), seconds=el)
    print(f"{kind} sigma={s}: {el:.0f}s -> {name}", flush=True)


# ---------------------------------------------------------------- analysis
gen = np.random.default_rng(20261011)


def floor(K, n):
    d = gen.multinomial(n, np.full(K, 1.0 / K), size=200) / n
    m = np.abs(d - 1.0 / K).sum(axis=1)
    return float(m.mean()), float(m.std())


def gompertz_tau(t, L, fl):
    m = L > 3 * fl
    tt, yy = t[m], np.log(L[m])
    f = lambda t, la, a2, a3: la - a2 * np.exp(a3 * t)
    best = None
    tw = tt.max()
    for a3 in (1 / tw, 3 / tw, 10 / tw, 30 / tw):
        for a2 in (0.03, 0.3, 1.0, 3.0):
            try:
                p, _ = curve_fit(f, tt, yy, p0=(yy[0] + a2, a2, a3),
                                 bounds=([-np.inf, 1e-9, 1e-9], [np.inf, np.inf, np.inf]), maxfev=20000)
            except RuntimeError:
                continue
            sse = float(np.sum((f(tt, *p) - yy) ** 2))
            if best is None or sse < best[0]:
                best = (sse, p)
    sse, (la, a2, a3) = best
    return float(1 / (a2 * a3)), dict(ln_a1=float(la), a2=float(a2), a3=float(a3), sse=sse,
                                      points=int(m.sum()), t_window=float(tw))


def tau_int(s):
    lit = s * s * math.sqrt((A * A - s * s) / (A * A + s * s))
    ts = np.arange(1, 15001) * 1e-4
    x = np.linspace(0, A + 12 * math.sqrt((s ** 4 + 1.5 ** 2) / (2 * s * s)), 20001)
    # numerical check of the literal formula: sign of the curvature at x = 0
    h = 1e-4
    r0 = rho(np.zeros_like(ts), ts, s)
    rh = rho(np.full_like(ts, h), ts, s)
    num = float(ts[np.argmax(r0 > rh)])
    vis = None
    for t in ts[ts >= num]:
        r = rho(x, t, s)
        if r[1] >= r[0]:
            continue                      # no maximum at x = 0 yet
        j = 0
        while j < len(r) - 1 and r[j + 1] <= r[j]:
            j += 1                        # walk down to the next minimum
        if r[0] - r[j] >= 0.1 * r.max():
            vis = float(t)
            break
    return lit, num, vis


def analyse():
    log = []
    say = lambda s_: (print(s_, flush=True), log.append(s_))
    res = dict(checks={}, sigma={}, test1b={}, test2_w2={})
    fl1, sd1 = floor(KL1, N)
    fl2, sd2 = floor(KTV, N)
    say(f"Floors (N = {N}): L1 over 100 bins {fl1:.4f} ± {sd1:.4f}; TV over 20 bins {fl2:.4f} ± {sd2:.4f}")

    # figure check
    x = np.linspace(-1e-3, 1e-3, 3)
    r = rho(x, 0.12, 0.09)
    ok_fig = bool(r[1] > r[0] and r[1] > r[2])
    say(f"Check, figure (sigma=0.09, t=0.12): |psi|^2 at x = -1e-3, 0, 1e-3 = {r[0]:.5f}, {r[1]:.5f}, "
        f"{r[2]:.5f} -> {'OK' if ok_fig else 'FAILED'}")
    # equivariance check
    d = np.load(OUT + "nelson_equiv_s40.npz")
    L = np.abs(d["c100"] / N - 1 / KL1).sum(axis=1)
    ok_eq = bool(np.all(L <= fl1 + 5 * sd1))
    say(f"Check, equivariance (sigma=0.4, Born start): max L1 {L.max():.4f}, limit {fl1 + 5 * sd1:.4f} "
        f"-> {'OK' if ok_eq else 'FAILED'}")

    def tauq(name):
        d = np.load(name)
        L = np.abs(d["c100"] / N - 1 / KL1).sum(axis=1)
        tq, info = gompertz_tau(d["times"], L, fl1)
        return tq, info, L, d

    step = {}
    for s in (0.2, 0.7):
        a, _, _, _ = tauq(f"{OUT}nelson_main_s{round(100 * s):02d}.npz")
        b, _, _, _ = tauq(f"{OUT}nelson_step_s{round(100 * s):02d}.npz")
        step[s] = (a, b, abs(a - b) / a)
        say(f"Check, step size (sigma={s}): tau_q {a:.4f} at dt 1e-4, {b:.4f} at 5e-5, "
            f"difference {100 * step[s][2]:.2f}%")
    ok_st = all(v[2] < 0.05 for v in step.values())
    say(f"Check, step size -> {'OK' if ok_st else 'FAILED'}")
    res["checks"] = dict(figure=ok_fig, equivariance=ok_eq, equiv_max_L1=float(L.max()),
                         step=ok_st, step_detail={str(k): v for k, v in step.items()})

    lit_ok, half_ok = [], []
    curves = {}
    for s in SIGMAS:
        tq, info, L, d = tauq(f"{OUT}nelson_main_s{round(100 * s):02d}.npz")
        lit, num, half = tau_int(s)
        tq10, _ = gompertz_tau(d["times"], L, 10 * fl1 / 3)   # report only: window L1 > 10 x floor
        lit_ok.append(tq < lit)
        half_ok.append(half is not None and tq < half)
        res["sigma"][str(s)] = dict(tau_q=tq, fit=info, tau_q_window10=tq10, tau_int_literal=lit, tau_int_numeric=num,
                                    tau_int_visible=half, L1_start=float(L[0]), L1_end=float(L[-1]),
                                    nonfinite=int(d["nonfinite"]), seconds=float(d["seconds"]))
        curves[str(s)] = dict(t=d["times"].tolist(), L1=L.tolist())
        say(f"sigma={s}: tau_q = {tq:.4f} (fit on {info['points']} points to t = {info['t_window']:.3f}); "
            f"tau_int literal {lit:.4f} (numerical {num:.4f}), visible peak {half:.4f}; "
            f"L1 {L[0]:.3f} -> {L[-1]:.4f}; tau_q with the 10x window {tq10:.4f} (report only)")
    valid = ok_fig and ok_eq and ok_st
    if all(lit_ok):
        verdict = "PASS"
    elif all(half_ok):
        verdict = "PARTIAL (only with the visible-peak definition)"
    elif any(not a and not b for a, b in zip(lit_ok, half_ok)):
        verdict = "FAIL"
    else:
        verdict = "MIXED (no sigma fails both; some pass neither as a set)"
    say(f"TEST 1b: {verdict}" + ("" if valid else "  -- NOT VALID: a check failed"))
    res["test1b"] = dict(verdict=verdict, literal=lit_ok, half=half_ok, valid=valid)

    # Test 2, W2
    tq = res["sigma"]["0.4"]["tau_q"]
    d = np.load(OUT + "nelson_main_s40.npz")
    t = d["times"]
    TV = 0.5 * np.abs(d["c20"] / N - 1 / KTV).sum(axis=1)
    j = int(np.argmax(TV <= TV[0] / 2))
    th = float(t[j - 1] + (TV[0] / 2 - TV[j - 1]) * (t[j] - t[j - 1]) / (TV[j] - TV[j - 1]))
    p1 = bool(0.25 * tq <= th <= 4 * tq)
    band = fl2 + 3 * sd2
    p2 = bool(TV[-1] < band)
    say(f"Test 2 W2 (sigma=0.4): TV {TV[0]:.3f} -> {TV[-1]:.4f} at t = 1.5 (band {band:.4f}) -> {p2}")
    say(f"t_half = {th:.4f}; tau_q = {tq:.4f}; ratio {th / tq:.2f} (band 0.25 to 4) -> {p1}")
    say(f"TEST 2 (W2): {'PASS' if (p1 and p2) else 'FAIL'}")
    res["test2_w2"] = dict(t_half=th, tau_q=tq, ratio=th / tq, pass_timescale=p1, tv_end=float(TV[-1]),
                           band=band, pass_floor=p2, passed=bool(p1 and p2), t=t.tolist(), TV=TV.tolist())
    res["floors"] = dict(L1=(fl1, sd1), TV20=(fl2, sd2))
    res["curves"] = curves
    with open(OUT + "test1b_test2w2.json", "w") as f:
        json.dump(res, f)
    with open(OUT + "test1b_test2w2_console.txt", "w") as f:
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
