"""Test 1 follow-up — written AFTER Test 1's verdict (PASS), to look at its
weakest number. It cannot change the verdict.

Test 1's fringe-spacing ratio passed the 2% bar by a hair at rho = 1e7
(0.9811, with a standard error of about 0.005, so about 4 standard errors
below 1). Is that a finite-density bias that keeps shrinking, or a fixed
offset? Two things are measured with exactly Test 1's method:
  1. one more density, rho = 3e7;
  2. where across the screen the phase error sits (mean over sprinklings of
     discrete minus continuum phase at each screen point), at 3e6 and 3e7.
"""
import json
import time
import numpy as np
import cs
import test1_link_clock as t1

DENS = [3e6, 3e7]


def main():
    X, tc1, tc2 = cs.continuum_taus()
    phi_c = t1.M * (tc1 - tc2)
    qx, qt = X.copy(), np.full_like(X, cs.T2)
    out, log = {}, []
    say = lambda s: (print(s, flush=True), log.append(s))
    for rho in DENS:
        di = 100 + int(round(np.log10(rho) * 10))      # seeds disjoint from Test 1
        t0 = time.time()
        coef, cal_sd, inv = t1.calibrate(rho, di)
        rows, diffs, e1, e2 = [], [], [], []
        for k in range(t1.N_TEST):
            t, x = cs.sprinkle(rho, t1.rng_for(di, k, 1))
            n1, n2 = cs.chain_through_slits(t, x, qt, qx)
            del t, x
            phi_d = t1.M * (inv(n1) - inv(n2))
            rows.append(t1.metrics(phi_d, phi_c))
            diffs.append(phi_d - phi_c)
            e1.append(inv(n1) - tc1)
            e2.append(inv(n2) - tc2)
        sp = np.array([r["spacing_ratio"] for r in rows])
        co = np.array([r["corr"] for r in rows])
        ru = np.array([r["rms_unwrapped"] for r in rows])
        out[str(rho)] = dict(spacing=sp.tolist(), corr=co.tolist(), rms_unwrapped=ru.tolist(),
                             mean_phase_error_by_X=np.mean(diffs, axis=0).tolist(),
                             mean_clock_error_slit1=np.mean(e1, axis=0).tolist(),
                             mean_clock_error_slit2=np.mean(e2, axis=0).tolist())
        say(f"rho={rho:.0e}: spacing {sp.mean():.4f} ± {sp.std(ddof=1)/np.sqrt(len(sp)):.4f} (s.e.)  "
            f"corr {co.mean():.4f}  rms_unwr {ru.mean():.3f}  | {time.time()-t0:.0f}s")
        md = np.mean(diffs, axis=0)
        say(f"   mean phase error by screen position: centre {md[100]:+.3f}, "
            f"left edge {md[0]:+.3f}, right edge {md[-1]:+.3f}, max |.| {np.abs(md).max():.3f} rad")
    out["X"] = X.tolist()
    with open("results/test1b.json", "w") as f:
        json.dump(out, f)
    with open("results/test1b_console.txt", "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
