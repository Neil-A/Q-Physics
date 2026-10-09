"""SIM-SPEC-02 Test 1 — Are link counts good enough clocks?

For each density rho, on fresh Poisson sprinklings of 1+1 Minkowski space:
  1. Calibrate the clock: on 10 independent sprinklings, fit the mean longest
     chain n along STRAIGHT histories S -> (t, 0) as n = a*tau + b*tau^(1/3) + c
     (the continuum form 2*sqrt(N) - 1.77 N^(1/6) with N = rho*tau^2/2).
  2. Test: on 20 further sprinklings, take the longest chain from S to each
     screen point through slit 1 and through slit 2 (BENT histories), convert
     each to a clock reading tau_hat with the calibration, and form the pattern
     |exp(i M tau_hat_1) + exp(i M tau_hat_2)|^2.
  3. Compare with the continuum pattern built from the exact proper times of
     the same histories (max of tau over each slit).

The clock is calibrated on straight histories and used on bent ones, so the
calibration cannot absorb the geometry of the test.

Fixed before the run (9 Oct 2026):
  M = 90 (about three fringes across the screen).
  Pass conditions are SIM-SPEC-02 §5 Test 1, read as follows:
   - correlation "rises toward 1": mean correlation increases with density,
     and 1 - mean correlation falls with density;
   - spacing: |mean(1/slope) - 1| < 0.02 at the highest density, where slope
     is the least-squares slope of discrete phase against continuum phase;
   - phase error: the RMS of the UNWRAPPED phase difference falls with
     exponent -1/3 +/- 0.08, fitted over all densities. (Unwrapped, because
     a wrapped phase error saturates at about 1.8 rad and would bend the fit.)
  The raw clock tau_hat = n / sqrt(2 rho), with no calibration, is reported
  alongside as a secondary result.

Change after the first launch (9 Oct, before any metric was computed): the
first launch stopped at rho = 1e4 because a slit held no elements in one
sprinkling (expected ~4 elements per slit at that density). A slit with no
elements is not a slit, so 1e4 was dropped and the run starts at 3e4
(~12 elements per slit). Nothing else changed.
"""
import json
import time
import numpy as np
import cs

M = 90.0
DENSITIES = [3e4, 1e5, 3e5, 1e6, 3e6, 1e7]   # 1e4 dropped after the first launch crashed: see docstring
N_CAL = 10
N_TEST = 20
CAL_T = np.linspace(0.7, 1.0, 31)
OUT = "results/"


def rng_for(di, k, kind):
    return np.random.default_rng([2026, 10, 9, di, k, kind])


def calibrate(rho, di):
    taus, ns = [], []
    qt, qx = CAL_T.copy(), np.zeros_like(CAL_T)
    for k in range(N_CAL):
        t, x = cs.sprinkle(rho, rng_for(di, k, 0))
        n = cs.chain_to_points(t, x, qt, qx)
        taus.append(CAL_T)
        ns.append(n)
    tau_all = np.concatenate(taus)
    n_all = np.concatenate(ns).astype(float)
    A = np.vstack([tau_all, tau_all ** (1 / 3), np.ones_like(tau_all)]).T
    coef, *_ = np.linalg.lstsq(A, n_all, rcond=None)
    resid = n_all - A @ coef
    grid = np.linspace(0.5, 1.1, 60001)
    ngrid = coef[0] * grid + coef[1] * grid ** (1 / 3) + coef[2]
    assert np.all(np.diff(ngrid) > 0), "calibration not monotone"
    inv = lambda n: np.interp(n, ngrid, grid)
    return coef, float(resid.std()), inv


def metrics(phi_d, phi_c):
    Pd = 2 + 2 * np.cos(phi_d)
    Pc = 2 + 2 * np.cos(phi_c)
    corr = float(np.corrcoef(Pd, Pc)[0, 1])
    slope = float(np.polyfit(phi_c, phi_d, 1)[0])
    diff = phi_d - phi_c
    wrapped = (diff + np.pi) % (2 * np.pi) - np.pi
    return dict(corr=corr, slope=slope, spacing_ratio=1.0 / slope,
                rms_unwrapped=float(np.sqrt(np.mean(diff ** 2))),
                rms_wrapped=float(np.sqrt(np.mean(wrapped ** 2))))


def main():
    X, tc1, tc2 = cs.continuum_taus()
    phi_c = M * (tc1 - tc2)
    qx = X.copy()
    qt = np.full_like(qx, cs.T2)
    log = []
    say = lambda s: (print(s, flush=True), log.append(s))
    say(f"Test 1: M = {M}, fringes across screen = {(phi_c.max() - phi_c.min()) / (2 * np.pi):.3f}")
    say(f"Region area = {cs.region_area():.5f}; slits at {cs.SLITS}, width {cs.SLIT_W}, half-thickness {cs.SLIT_H}")
    results = dict(M=M, X=X.tolist(), phi_c=phi_c.tolist(), densities=[])
    examples = {}
    for di, rho in enumerate(DENSITIES):
        t0 = time.time()
        coef, cal_sd, inv = calibrate(rho, di)
        rows_cal, rows_raw = [], []
        for k in range(N_TEST):
            t, x = cs.sprinkle(rho, rng_for(di, k, 1))
            n1, n2 = cs.chain_through_slits(t, x, qt, qx)
            assert n1.min() > 0 and n2.min() > 0, "a screen point has no chain through a slit"
            phi_d = M * (inv(n1) - inv(n2))
            phi_raw = M * (n1 - n2) / np.sqrt(2 * rho)
            rows_cal.append(metrics(phi_d, phi_c))
            rows_raw.append(metrics(phi_raw, phi_c))
            if k == 0:
                examples[rho] = dict(phi_d=phi_d.tolist(), N=int(len(t)))
        agg = lambda rows, key: (float(np.mean([r[key] for r in rows])), float(np.std([r[key] for r in rows])))
        entry = dict(rho=rho, cal_coef=coef.tolist(), cal_theory_a=float(np.sqrt(2 * rho)),
                     cal_resid_sd=cal_sd, calibrated=rows_cal, raw=rows_raw,
                     mean_N=float(rho * cs.region_area()))
        results["densities"].append(entry)
        c, s, ru, rw = (agg(rows_cal, k) for k in ("corr", "spacing_ratio", "rms_unwrapped", "rms_wrapped"))
        cr, sr = agg(rows_raw, "corr"), agg(rows_raw, "spacing_ratio")
        say(f"rho={rho:.0e} N~{entry['mean_N']:.2e} | cal a={coef[0]:.2f} (theory {np.sqrt(2*rho):.2f}) b={coef[1]:.2f} c={coef[2]:.2f} | "
            f"corr {c[0]:.4f}±{c[1]:.4f}  spacing {s[0]:.4f}±{s[1]:.4f}  rms_unwr {ru[0]:.3f}±{ru[1]:.3f}  rms_wr {rw[0]:.3f} | "
            f"raw: corr {cr[0]:.4f} spacing {sr[0]:.4f} | {time.time() - t0:.0f}s")
    results["examples"] = {str(k): v for k, v in examples.items()}

    # verdicts
    rhos = np.array(DENSITIES)
    mc = np.array([np.mean([r["corr"] for r in d["calibrated"]]) for d in results["densities"]])
    ms = np.array([np.mean([r["spacing_ratio"] for r in d["calibrated"]]) for d in results["densities"]])
    mr = np.array([np.mean([r["rms_unwrapped"] for r in d["calibrated"]]) for d in results["densities"]])
    p, cov = np.polyfit(np.log(rhos), np.log(mr), 1, cov=True)
    expo, expo_se = float(p[0]), float(np.sqrt(cov[0, 0]))
    pc = np.polyfit(np.log(rhos), np.log(1 - mc), 1)
    v_corr = bool(np.all(np.diff(mc) > 0))
    v_space = bool(abs(ms[-1] - 1) < 0.02)
    v_expo = bool(abs(expo + 1 / 3) <= 0.08)
    say("")
    say(f"Correlation rises at every density step: {v_corr}  (1 - corr falls as rho^{pc[0]:.3f})")
    say(f"Spacing ratio at highest density: {ms[-1]:.4f}  -> within 2%: {v_space}")
    say(f"RMS phase error exponent: {expo:.3f} ± {expo_se:.3f}  (required -0.333 ± 0.08) -> {v_expo}")
    say(f"TEST 1: {'PASS' if (v_corr and v_space and v_expo) else 'FAIL'}")
    results["verdict"] = dict(corr_rises=v_corr, one_minus_corr_exponent=float(pc[0]),
                              spacing_highest=float(ms[-1]), spacing_ok=v_space,
                              rms_exponent=expo, rms_exponent_se=expo_se, rms_exponent_ok=v_expo,
                              passed=bool(v_corr and v_space and v_expo))
    with open(OUT + "test1.json", "w") as f:
        json.dump(results, f)
    with open(OUT + "test1_console.txt", "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
