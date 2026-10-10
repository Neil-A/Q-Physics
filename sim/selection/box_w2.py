"""W2 in the TRV box (11 Oct). A measurement, not a test.

Written after the W2 second test failed its floor condition in the free
double slit (RESULTS-04). Question: is the slow W2 tail a property of the rule
W2, or of the free spreading of the double slit? In a free double slit the
packets keep spreading, so the pull toward Born weakens with time. The TRV box
is bounded. If W2 relaxes fully in the box, the tail comes from the spreading.
This measurement cannot change any verdict.

Set-up: the box and the wave function of box2d.py, M = 64, phase set 0 (W1 gave
tau = 1.037 for this set). Rule W2: dX = (v + u) dt + dW, with v = Im(grad psi/psi),
u = Re(grad psi/psi), D = 1/2. Euler-Maruyama, dt = 1e-4. A seed that a step
puts outside the box is reflected back, and the code counts the events.
N = 5e4. Output every pi/8 to 4 pi: 16 x 16 cell counts and Born weights.
Runs: ground-state start (as W1), and a Born start as the control for
integrator drift. Streams: start points as box2d.py (ground [2026,10,10,64,0,1];
Born [2026,10,10,64,0,2]); kicks rng.states(N, [2026,10,11,64,0,7]) and
[2026,10,11,64,0,8].
The analysis uses analyse_box.load and the same rules for H-bar, TV and floors.

Usage:  python box_w2.py ground|born
"""
import math
import sys
import time

import numba as nb
import numpy as np

import box2d as b
import rng as rs

N = 50_000
DT = 1e-4
OUT = "results/"


@nb.njit(fastmath=True)
def drift(x, y, t, amp):
    pr, pim, xr, xi, yr, yi = b.psi_and_grad(x, y, t, amp)
    d = pr * pr + pim * pim + 1e-300
    vx = (pr * xi - pim * xr) / d
    vy = (pr * yi - pim * yr) / d
    ux = (pr * xr + pim * xi) / d
    uy = (pr * yr + pim * yi) / d
    return vx + ux, vy + uy


@nb.njit(fastmath=True, parallel=True)
def advance(X, Y, st, t0, nsteps, dt, amp, refl):
    sq = math.sqrt(dt)
    for i in nb.prange(X.shape[0]):
        x = X[i]; y = Y[i]; z = st[i]; t = t0; rc = 0
        for k in range(nsteps):
            bx, by = drift(x, y, t, amp)
            z, n1, n2 = rs.normal_pair(z)
            x += bx * dt + sq * n1
            y += by * dt + sq * n2
            t += dt
            if x < 0.0:
                x = -x; rc += 1
            elif x > math.pi:
                x = 2 * math.pi - x; rc += 1
            if y < 0.0:
                y = -y; rc += 1
            elif y > math.pi:
                y = 2 * math.pi - y; rc += 1
        X[i] = x; Y[i] = y; st[i] = z; refl[i] += rc


def main():
    kind = sys.argv[1]
    M, s = 64, 0
    amp = b.amplitudes(M, s)
    if kind == "ground":
        X, Y = b.sample_ground(N, np.random.default_rng([2026, 10, 10, M, s, 1]))
        st = rs.states(N, [2026, 10, 11, M, s, 7])
    elif kind == "born":
        X, Y = b.sample_born(N, amp, np.random.default_rng([2026, 10, 10, M, s, 2]))
        st = rs.states(N, [2026, 10, 11, M, s, 8])
    else:
        raise SystemExit(__doc__)
    times = np.arange(33) * b.DT_OUT
    C = np.zeros((33, b.NCELL, b.NCELL), np.int64)
    Q = np.zeros((33, b.NCELL, b.NCELL))
    refl = np.zeros(N, np.int64)
    C[0] = b.counts(X, Y); Q[0] = b.born_cells(0.0, amp)
    t0 = time.time()
    for k in range(32):
        n = int(round((times[k + 1] - times[k]) / DT))
        advance(X, Y, st, times[k], n, DT, amp, refl)
        C[k + 1] = b.counts(X, Y); Q[k + 1] = b.born_cells(times[k + 1], amp)
        print(f"{kind} t={times[k + 1]:.3f}: {time.time() - t0:.0f}s", flush=True)
    name = f"{OUT}boxw2_{kind}_M64_s0.npz"
    np.savez_compressed(name, times=times, counts=C, born=Q, M=M, seed=s, N=N, delta=0.0,
                        mean_steps=float(n * 32), reflections=int(refl.sum()), seconds=time.time() - t0)
    print(f"done {kind}: reflections {int(refl.sum())} -> {name}", flush=True)


if __name__ == "__main__":
    main()
