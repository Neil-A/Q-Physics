"""SIM-SPEC-03 Test 1a (W1 relaxes as published) and the W1 runs for Test 2.

The model is the 2D box of Towler, Russell & Valentini 2012 (TRV):
  box side pi, hbar = m = 1,
  psi = (2/(pi sqrt(M))) sum_{n,m=1..sqrt(M)} sin(nx) sin(my) exp(i(theta_nm - E_nm t)),
  E_nm = (n^2 + m^2)/2, period 4 pi.
Start spread: the ground state rho = (4/pi^2) sin^2 x sin^2 y.

Each seed moves with the guidance equation v = Im(grad psi / psi) (rule W1).
Integrator: RK4, step h = min(0.05, DELTA/|v|), so no step moves a seed more
than DELTA = 0.01. If a step puts a seed outside the box, the code reflects it
back (psi is odd across each wall, so the flow is symmetric there) and counts
the event.

Output every pi/8: counts in 16 x 16 cells (the coarse grain, TRV epsilon = 64)
and the exact Born weight of each cell (Gauss-Legendre quadrature, 8 x 8 nodes
per cell). The analysis script computes H-bar, TV and the fits.

Runs (fixed before any run, 10 Oct 2026; SIM-SPEC-03 section 5):
  main   M in {4, 9, 16, 25, 36, 49, 64}, phase sets 0..5, N = 1e5, to 4 pi;
         M = 64 runs continue to 12 pi for Test 2.
  step   M = 64, phase set 0, step limit 0.005, to 4 pi (step check).
  equiv  M = 64, phase set 0, seeds from the exact Born spread, to 4 pi
         (equivariance check).
Random streams: phases use default_rng([2026,10,10,M,s,0]); start points use
default_rng([2026,10,10,M,s,1]). The step check uses the same start points as
the main run. The equivariance check uses default_rng([2026,10,10,M,s,2]).

Change before the main runs (10 Oct). The first equivariance run used
DELTA = 0.02 and failed: H-bar of the Born start rose from 0.0012 to 0.0035 by
4 pi (limit about 0.0018). A diagnostic to t = pi gave H-bar 0.0024 at 0.02,
0.0013 at 0.01 and 0.0012 at 0.005 (floor 0.0013). So DELTA is now 0.01 and
the step check uses 0.005. The failed run is kept as
results/box_equiv_M64_s0_step002_FAILED.npz.

Usage:  python box2d.py main|step|equiv [M ...]
"""
import math
import sys
import time

import numba as nb
import numpy as np

PI = np.pi
NCELL = 16
GL = 8                       # Gauss-Legendre nodes per cell per axis
N = 100_000
DELTA = 0.01
HMAX = 0.05
DT_OUT = PI / 8
MS = [4, 9, 16, 25, 36, 49, 64]
SEEDS = range(6)
OUT = "results/"


def amplitudes(M, s):
    K = int(round(math.sqrt(M)))
    assert K * K == M
    theta = np.random.default_rng([2026, 10, 10, M, s, 0]).uniform(0, 2 * PI, (K, K))
    return (2 / (PI * math.sqrt(M))) * np.exp(1j * theta)


@nb.njit(fastmath=True)
def psi_and_grad(x, y, t, amp):
    """Return psi, d psi/dx, d psi/dy as (re, im) pairs."""
    K = amp.shape[0]
    sx = np.empty(K); cx = np.empty(K); sy = np.empty(K); cy = np.empty(K)
    s1x, c1x = math.sin(x), math.cos(x)
    s1y, c1y = math.sin(y), math.cos(y)
    sx[0] = s1x; cx[0] = c1x; sy[0] = s1y; cy[0] = c1y
    for n in range(1, K):
        sx[n] = sx[n - 1] * c1x + cx[n - 1] * s1x
        cx[n] = cx[n - 1] * c1x - sx[n - 1] * s1x
        sy[n] = sy[n - 1] * c1y + cy[n - 1] * s1y
        cy[n] = cy[n - 1] * c1y - sy[n - 1] * s1y
    ur = np.empty(K); ui = np.empty(K)
    for n in range(K):
        ph = -0.5 * (n + 1) * (n + 1) * t      # exp(-i n^2 t / 2)
        ur[n] = math.cos(ph); ui[n] = math.sin(ph)
    pr = 0.; pim = 0.; xr = 0.; xi = 0.; yr = 0.; yi = 0.
    for n in range(K):
        Rr = 0.; Ri = 0.; Qr = 0.; Qi = 0.
        for m in range(K):
            er = ur[n] * ur[m] - ui[n] * ui[m]
            ei = ur[n] * ui[m] + ui[n] * ur[m]
            ar = amp[n, m].real; ai = amp[n, m].imag
            cr = ar * er - ai * ei; ci = ar * ei + ai * er
            Rr += cr * sy[m]; Ri += ci * sy[m]
            Qr += cr * (m + 1) * cy[m]; Qi += ci * (m + 1) * cy[m]
        pr += sx[n] * Rr; pim += sx[n] * Ri
        xr += (n + 1) * cx[n] * Rr; xi += (n + 1) * cx[n] * Ri
        yr += sx[n] * Qr; yi += sx[n] * Qi
    return pr, pim, xr, xi, yr, yi


@nb.njit(fastmath=True)
def vel(x, y, t, amp):
    pr, pim, xr, xi, yr, yi = psi_and_grad(x, y, t, amp)
    d = pr * pr + pim * pim + 1e-300
    # v = Im(grad psi / psi) = (Re psi Im grad - Im psi Re grad) / |psi|^2
    return (pr * xi - pim * xr) / d, (pr * yi - pim * yr) / d


@nb.njit(fastmath=True, parallel=True)
def advance(X, Y, t0, t1, amp, delta, hmax, steps, refl):
    for i in nb.prange(X.shape[0]):
        x = X[i]; y = Y[i]; t = t0; cnt = 0; rc = 0
        while t < t1 - 1e-13:
            k1x, k1y = vel(x, y, t, amp)
            sp = math.sqrt(k1x * k1x + k1y * k1y)
            h = min(hmax, delta / (sp + 1e-30), t1 - t)
            k2x, k2y = vel(x + 0.5 * h * k1x, y + 0.5 * h * k1y, t + 0.5 * h, amp)
            k3x, k3y = vel(x + 0.5 * h * k2x, y + 0.5 * h * k2y, t + 0.5 * h, amp)
            k4x, k4y = vel(x + h * k3x, y + h * k3y, t + h, amp)
            x += h * (k1x + 2 * k2x + 2 * k3x + k4x) / 6
            y += h * (k1y + 2 * k2y + 2 * k3y + k4y) / 6
            t += h
            cnt += 1
            if x < 0.0:
                x = -x; rc += 1
            elif x > math.pi:
                x = 2 * math.pi - x; rc += 1
            if y < 0.0:
                y = -y; rc += 1
            elif y > math.pi:
                y = 2 * math.pi - y; rc += 1
        X[i] = x; Y[i] = y
        steps[i] += cnt
        refl[i] += rc


@nb.njit(parallel=True)
def density_on(xs, ys, t, amp):
    out = np.empty((xs.shape[0], ys.shape[0]))
    for i in nb.prange(xs.shape[0]):
        for j in range(ys.shape[0]):
            pr, pim, _, _, _, _ = psi_and_grad(xs[i], ys[j], t, amp)
            out[i, j] = pr * pr + pim * pim
    return out


_gx, _gw = np.polynomial.legendre.leggauss(GL)
_h = PI / NCELL
QX = (np.arange(NCELL)[:, None] * _h + (_gx[None, :] + 1) * _h / 2).ravel()
QW = np.tile(_gw * _h / 2, NCELL)


def born_cells(t, amp):
    """Exact Born weight of each of the 16 x 16 cells at time t."""
    rho = density_on(QX, QX, t, amp) * QW[:, None] * QW[None, :]
    return rho.reshape(NCELL, GL, NCELL, GL).sum(axis=(1, 3))


def counts(X, Y):
    ix = np.clip((X / _h).astype(np.int64), 0, NCELL - 1)
    iy = np.clip((Y / _h).astype(np.int64), 0, NCELL - 1)
    return np.bincount(ix * NCELL + iy, minlength=NCELL * NCELL).reshape(NCELL, NCELL)


def sample_ground(n, rng):
    """Sample (4/pi^2) sin^2 x sin^2 y exactly (rejection, one axis at a time)."""
    def axis():
        out = np.empty(0)
        while out.size < n:
            x = rng.uniform(0, PI, 2 * n)
            out = np.concatenate([out, x[rng.uniform(0, 1, 2 * n) < np.sin(x) ** 2]])
        return out[:n]
    return axis(), axis()


def sample_born(n, amp, rng):
    """Sample |psi(t=0)|^2 exactly by rejection; the bound is checked."""
    g = np.linspace(0, PI, 801)
    bound = 1.25 * density_on(g, g, 0.0, amp).max()
    xs, ys = np.empty(0), np.empty(0)
    while xs.size < n:
        x = rng.uniform(0, PI, 4 * n); y = rng.uniform(0, PI, 4 * n)
        d = density_pts(x, y, 0.0, amp)
        assert d.max() < bound, "rejection bound too low"
        keep = rng.uniform(0, bound, x.size) < d
        xs = np.concatenate([xs, x[keep]]); ys = np.concatenate([ys, y[keep]])
    return xs[:n], ys[:n]


@nb.njit(parallel=True)
def density_pts(xs, ys, t, amp):
    out = np.empty(xs.shape[0])
    for i in nb.prange(xs.shape[0]):
        pr, pim, _, _, _, _ = psi_and_grad(xs[i], ys[i], t, amp)
        out[i] = pr * pr + pim * pim
    return out


def run(M, s, kind, t_end):
    amp = amplitudes(M, s)
    if kind == "equiv":
        X, Y = sample_born(N, amp, np.random.default_rng([2026, 10, 10, M, s, 2]))
    else:
        X, Y = sample_ground(N, np.random.default_rng([2026, 10, 10, M, s, 1]))
    delta = 0.005 if kind == "step" else DELTA
    nout = int(round(t_end / DT_OUT))
    times = np.arange(nout + 1) * DT_OUT
    C = np.zeros((nout + 1, NCELL, NCELL), np.int64)
    Q = np.zeros((nout + 1, NCELL, NCELL))
    steps = np.zeros(N, np.int64); refl = np.zeros(N, np.int64)
    C[0] = counts(X, Y); Q[0] = born_cells(0.0, amp)
    assert abs(Q[0].sum() - 1) < 1e-9, Q[0].sum()
    t0 = time.time()
    for k in range(nout):
        advance(X, Y, times[k], times[k + 1], amp, delta, HMAX, steps, refl)
        C[k + 1] = counts(X, Y)
        Q[k + 1] = born_cells(times[k + 1], amp)
        assert abs(Q[k + 1].sum() - 1) < 1e-9
    el = time.time() - t0
    name = f"{OUT}box_{kind}_M{M:02d}_s{s}.npz"
    np.savez_compressed(name, times=times, counts=C, born=Q, M=M, seed=s, N=N, delta=delta,
                        mean_steps=steps.mean(), reflections=int(refl.sum()), seconds=el)
    print(f"{kind} M={M} s={s}: {el:.0f}s, mean steps {steps.mean():.0f}, "
          f"reflections {int(refl.sum())} ({refl.sum() / N:.4f} per seed) -> {name}", flush=True)


def main():
    kind = sys.argv[1]
    ms = [int(a) for a in sys.argv[2:]] or MS
    if kind == "main":
        for M in ms:
            for s in SEEDS:
                run(M, s, "main", 12 * PI if M == 64 else 4 * PI)
    elif kind in ("step", "equiv"):
        run(64, 0, kind, 4 * PI)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
