"""SIM-SPEC-03 Test 1a verdict and the W1 part of Test 2, from the box2d.py runs.

Fixed before any run (10 Oct 2026), from SIM-SPEC-03 section 5:

Noise floors. At each output time, draw 200 multinomial samples of N seeds from
the exact Born cell weights. The floor of a metric is the mean of the metric
over these draws; its spread is their standard deviation.

Test 1a.
  H-bar = sum over the 16 x 16 cells of p ln(p/q), p = count/N, q = Born weight.
  For each run, fit ln H-bar = a + b t over t <= 4 pi, using every point where
  H-bar > 10 x floor (the spec's rule, taken literally). tau = -1/b. A run with
  fewer than 4 such points, or with b >= 0, has no tau and is reported.
  tau(M) = mean over the 6 phase sets; its error = their standard deviation.
  Fit tau = A M^p by weighted least squares over M = 9..64 (M = 4 reported only).
  Checks first: equivariance (H-bar of the Born start stays below
  floor + 5 sd at every output time) and step size (tau at step limit 0.005 and
  0.01 agree within 5%, M = 64, phase set 0).
  PASS: p in [-1.25, -0.85].

Test 2, W1 (M = 64, 6 phase sets, runs to 12 pi).
  TV = half the sum over the 4 x 4 regions of |p - q|.
  For each run, fit ln TV = a + b t over t <= 4 pi, using every point where
  TV > 3 x floor. T_TV = -1/b. Take the mean of T_TV over the 6 runs.
  PASS 1: 0.5 tau(64) <= mean T_TV <= 4 tau(64).
  PASS 2: at t = 12 pi, the median TV over the 6 runs < floor + 3 sd.
"""
import glob
import json

import numpy as np
from scipy.optimize import curve_fit

PI = np.pi
OUT = "results/"
NDRAW = 200
rng = np.random.default_rng(20261010)


def regions(a):
    """16 x 16 cells -> 4 x 4 regions (works on the last two axes)."""
    s = a.shape[:-2]
    return a.reshape(*s, 4, 4, 4, 4).sum(axis=(-3, -1))


def hbar(p, q):
    m = p > 0
    return float(np.sum(p[m] * np.log(p[m] / q[m])))


def tv(p, q):
    return float(0.5 * np.abs(p - q).sum())


def load(name):
    d = np.load(name)
    N = int(d["N"])
    t = d["times"]
    P = d["counts"] / N
    Q = d["born"]
    H = np.array([hbar(P[k], Q[k]) for k in range(len(t))])
    PR, QR = regions(P), regions(Q)
    T = np.array([tv(PR[k], QR[k]) for k in range(len(t))])
    Hf = np.zeros((len(t), 2)); Tf = np.zeros((len(t), 2))
    for k in range(len(t)):
        q = Q[k].ravel(); q = q / q.sum()
        draws = rng.multinomial(N, q, size=NDRAW).reshape(NDRAW, 16, 16) / N
        hs = [hbar(x, Q[k]) for x in draws]
        ts = [tv(regions(x), QR[k]) for x in draws]
        Hf[k] = np.mean(hs), np.std(hs)
        Tf[k] = np.mean(ts), np.std(ts)
    return dict(t=t, H=H, Hf=Hf, TV=T, TVf=Tf, M=int(d["M"]), seed=int(d["seed"]),
                reflections=int(d["reflections"]), N=N, seconds=float(d["seconds"]),
                mean_steps=float(d["mean_steps"]))


def efold(t, y, floor, factor, tmax=4 * PI + 1e-9):
    m = (t <= tmax) & (y > factor * floor)
    if m.sum() < 4:
        return None, int(m.sum())
    b = np.polyfit(t[m], np.log(y[m]), 1)[0]
    return (None if b >= 0 else float(-1 / b)), int(m.sum())


def main():
    log = []
    say = lambda s: (print(s, flush=True), log.append(s))
    res = dict(checks={}, runs=[], tau={}, test1a={}, test2_w1={})

    # checks
    eq = load(OUT + "box_equiv_M64_s0.npz")
    lim = eq["Hf"][:, 0] + 5 * eq["Hf"][:, 1]
    ok_eq = bool(np.all(eq["H"] <= lim))
    say(f"Check, equivariance (M=64, Born start): max H-bar {eq['H'].max():.5f}, "
        f"max of H-bar minus limit {np.max(eq['H'] - lim):+.5f} -> {'OK' if ok_eq else 'FAILED'}")
    st = load(OUT + "box_step_M64_s0.npz")
    m0 = load(OUT + "box_main_M64_s0.npz")
    ts_, _ = efold(st["t"], st["H"], st["Hf"][:, 0], 10)
    tm_, _ = efold(m0["t"], m0["H"], m0["Hf"][:, 0], 10)
    ok_st = ts_ is not None and tm_ is not None and abs(ts_ - tm_) / tm_ < 0.05
    say(f"Check, step size (M=64, set 0): tau {tm_:.3f} at 0.01, {ts_:.3f} at 0.005, "
        f"difference {100 * abs(ts_ - tm_) / tm_:.2f}% -> {'OK' if ok_st else 'FAILED'}")
    res["checks"] = dict(equivariance=ok_eq, step=bool(ok_st), tau_step001=tm_, tau_step0005=ts_,
                         equiv_max_H=float(eq["H"].max()))

    # Test 1a
    runs = {}
    for name in sorted(glob.glob(OUT + "box_main_M*_s*.npz")):
        r = load(name)
        tau, npts = efold(r["t"], r["H"], r["Hf"][:, 0], 10)
        r["tau"], r["npts"] = tau, npts
        runs[(r["M"], r["seed"])] = r
        res["runs"].append(dict(M=r["M"], seed=r["seed"], tau=tau, fit_points=npts,
                                H0=float(r["H"][0]), H_4pi=float(r["H"][32]),
                                floor_H=float(r["Hf"][0, 0]), reflections=r["reflections"],
                                mean_steps=r["mean_steps"], seconds=r["seconds"]))
        say(f"M={r['M']:2d} set {r['seed']}: H-bar {r['H'][0]:.3f} -> {r['H'][32]:.4f} at 4pi "
            f"(floor {r['Hf'][32, 0]:.4f}); tau = {tau if tau is None else round(tau, 3)} "
            f"from {npts} points; reflections {r['reflections']}")
    Ms = sorted({k[0] for k in runs})
    for M in Ms:
        taus = [runs[(M, s)]["tau"] for s in range(6) if (M, s) in runs]
        good = [x for x in taus if x is not None]
        res["tau"][M] = dict(mean=float(np.mean(good)) if good else None,
                             sd=float(np.std(good)) if len(good) > 1 else None,
                             n=len(good), missing=len(taus) - len(good))
        say(f"tau(M={M}) = {res['tau'][M]['mean']} ± {res['tau'][M]['sd']} "
            f"({len(good)} runs with a fit, {len(taus) - len(good)} without)")
    fitM = [M for M in Ms if M >= 9 and res["tau"][M]["mean"] is not None]
    x = np.array(fitM, float)
    y = np.array([res["tau"][M]["mean"] for M in fitM])
    e = np.array([res["tau"][M]["sd"] for M in fitM])
    (A, p), cov = curve_fit(lambda M, A, p: A * M ** p, x, y, p0=(y[0] * x[0], -1.0),
                            sigma=e, absolute_sigma=True)
    pse = float(np.sqrt(cov[1, 1]))
    pass1a = bool(-1.25 <= p <= -0.85)
    say(f"Fit tau = A M^p over M = {fitM}: A = {A:.3f}, p = {p:.3f} ± {pse:.3f}")
    say(f"TEST 1a: {'PASS' if pass1a else 'FAIL'} (band -1.05 ± 0.20; TRV: -1.05 ± 0.03)"
        + ("" if (ok_eq and ok_st) else "  -- NOT VALID: a check failed"))
    res["test1a"] = dict(A=float(A), p=float(p), p_se=pse, fit_M=fitM, passed=pass1a,
                         valid=bool(ok_eq and ok_st))

    # Test 2, W1
    tau64 = res["tau"][64]["mean"]
    Ts, tv_end, band_end = [], [], []
    for s in range(6):
        r = runs[(64, s)]
        T, npts = efold(r["t"], r["TV"], r["TVf"][:, 0], 3)
        Ts.append(T)
        tv_end.append(float(r["TV"][-1]))
        band_end.append(float(r["TVf"][-1, 0] + 3 * r["TVf"][-1, 1]))
        say(f"Test 2 W1, set {s}: TV {r['TV'][0]:.3f} -> {r['TV'][32]:.4f} at 4pi -> {r['TV'][-1]:.4f} "
            f"at 12pi (band {band_end[-1]:.4f}); T_TV = {T if T is None else round(T, 3)} from {npts} points")
    goodT = [x for x in Ts if x is not None]
    meanT = float(np.mean(goodT))
    ratio = meanT / tau64
    p1 = bool(0.5 <= ratio <= 4.0)
    med = float(np.median(tv_end)); band = float(np.median(band_end))
    p2 = bool(med < band)
    say(f"Mean T_TV = {meanT:.3f}; tau(64) = {tau64:.3f}; ratio {ratio:.2f} (band 0.5 to 4) -> {p1}")
    say(f"Median TV at 12pi = {med:.4f}; median band = {band:.4f} -> {p2}")
    say(f"TEST 2 (W1): {'PASS' if (p1 and p2) else 'FAIL'}")
    res["test2_w1"] = dict(T_TV=Ts, mean_T_TV=meanT, tau64=tau64, ratio=ratio, pass_timescale=p1,
                           tv_12pi=tv_end, band_12pi=band_end, median_tv_12pi=med, pass_floor=p2,
                           passed=bool(p1 and p2))
    res["curves"] = {f"M{k[0]}_s{k[1]}": dict(t=v["t"].tolist(), H=v["H"].tolist(),
                                              Hfloor=v["Hf"][:, 0].tolist(), TV=v["TV"].tolist(),
                                              TVfloor=v["TVf"][:, 0].tolist(), TVsd=v["TVf"][:, 1].tolist())
                     for k, v in runs.items()}
    res["curves"]["equiv"] = dict(t=eq["t"].tolist(), H=eq["H"].tolist(), Hfloor=eq["Hf"][:, 0].tolist())
    with open(OUT + "test1a_test2w1.json", "w") as f:
        json.dump(res, f)
    with open(OUT + "test1a_test2w1_console.txt", "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
