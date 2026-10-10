"""SIM-SPEC-03 Test 3: equilibrium forbids signals (Valentini's theorem).

Model: two particles, each in a 1D harmonic trap, omega = hbar = m = 1.
  psi0 = [phi0(x1) phi1(x2) + phi1(x1) phi0(x2)] / sqrt(2).
Choice at A (t = 0): nothing, or the local pulse exp(i k x1^2), k = 1.

Exact evolution after the pulse. With A0 = 1 - 2ik, D = cos t + i A0 sin t,
A(t) = (A0 cos t + i sin t)/D and c(t) = exp(it)/D:
  psi(x1, x2, t) is proportional to exp(-A x1^2/2 - x2^2/2) (x2 + c x1).
So  d/dx1 ln psi = -A x1 + c/(x2 + c x1),  d/dx2 ln psi = -x2 + 1/(x2 + c x1).
With no pulse, A = c = 1: psi is real (up to a constant phase), so v = 0.
(A kick exp(i p x1) would leave x2 + c x1 real, so it cannot move particle 2.)

W1: v = Im(grad ln psi). RK4, step h = min(0.01, 0.01/|v|).
W2: dX = (Im + Re)(grad ln psi) dt + dW, Euler-Maruyama, dt = 1e-4; the same
    random kicks for both choices (rng.py, the same start states).
Ensembles, N = 1e5 each, the same start points for both choices:
  equilibrium      |psi0|^2       start stream default_rng([2026,10,10,3,0])
  not equilibrium  |phi0 phi0|^2  start stream default_rng([2026,10,10,3,1])
W2 noise streams: rng.states(N, [2026,10,10,3,2]) (equilibrium) and [..,3].

Measure (fixed before any run): B's histogram of x2 in 40 bins on [-4, 4]
plus one bin below and one above, at t = 0.5, 1, 2, 3. TV between the two
choices. Null band: mean + 3 sd of TV between two independent samples of N
from B's Born marginal (200 pairs, stream default_rng([2026,10,10,3,9])).
PASS (W1): equilibrium TV <= band at all four times; not-equilibrium TV > band
at one time or more. PASS (W2, equilibrium only): TV <= band at all four
times. W2 not in equilibrium: report only.
Checks first: the closed forms agree with a direct numerical evolution
(split-step, max error < 1e-6), the gradient formula agrees with a finite
difference of ln psi (< 1e-6), and B's Born marginal is the same for both
choices (max difference < 1e-10).

Change after the first run (10 Oct): the first run printed all verdicts, then
stopped at the JSON write (a numpy bool). The fix casts to bool. The seeds are
fixed, so the second run must print the same numbers; its log is compared with
results/run_signal_first_crash.log.

Usage:  python signal2p.py
"""
import json
import math
import time

import numba as nb
import numpy as np

import rng as rs

KAPPA = 1.0
N = 100_000
TIMES = [0.5, 1.0, 2.0, 3.0]
BINS = np.concatenate([[-np.inf], np.linspace(-4, 4, 41), [np.inf]])
OUT = "results/"


@nb.njit(fastmath=True)
def grad_ln_psi(x1, x2, t, pulsed):
    if pulsed:
        A0 = complex(1.0, -2.0 * KAPPA)
        D = math.cos(t) + 1j * A0 * math.sin(t)
        Aa = (A0 * math.cos(t) + 1j * math.sin(t)) / D
        c = complex(math.cos(t), math.sin(t)) / D
    else:
        Aa = complex(1.0, 0.0)
        c = complex(1.0, 0.0)
    z = x2 + c * x1
    return -Aa * x1 + c / z, -x2 + 1.0 / z


@nb.njit(fastmath=True)
def v_w1(x1, x2, t, pulsed):
    g1, g2 = grad_ln_psi(x1, x2, t, pulsed)
    return g1.imag, g2.imag


@nb.njit(fastmath=True, parallel=True)
def run_w1(X1, X2, t0, t1, pulsed):
    for i in nb.prange(X1.shape[0]):
        x1 = X1[i]; x2 = X2[i]; t = t0
        while t < t1 - 1e-13:
            a1, a2 = v_w1(x1, x2, t, pulsed)
            h = min(0.01, 0.01 / (math.sqrt(a1 * a1 + a2 * a2) + 1e-30), t1 - t)
            b1, b2 = v_w1(x1 + 0.5 * h * a1, x2 + 0.5 * h * a2, t + 0.5 * h, pulsed)
            c1, c2 = v_w1(x1 + 0.5 * h * b1, x2 + 0.5 * h * b2, t + 0.5 * h, pulsed)
            d1, d2 = v_w1(x1 + h * c1, x2 + h * c2, t + h, pulsed)
            x1 += h * (a1 + 2 * b1 + 2 * c1 + d1) / 6
            x2 += h * (a2 + 2 * b2 + 2 * c2 + d2) / 6
            t += h
        X1[i] = x1; X2[i] = x2


@nb.njit(fastmath=True, parallel=True)
def run_w2(X1, X2, st, t0, nsteps, dt, pulsed):
    sq = math.sqrt(dt)
    for i in nb.prange(X1.shape[0]):
        x1 = X1[i]; x2 = X2[i]; z = st[i]; t = t0
        for k in range(nsteps):
            g1, g2 = grad_ln_psi(x1, x2, t, pulsed)
            z, n1, n2 = rs.normal_pair(z)
            x1 += (g1.imag + g1.real) * dt + sq * n1
            x2 += (g2.imag + g2.real) * dt + sq * n2
            t += dt
        X1[i] = x1; X2[i] = x2; st[i] = z


def sample_eq(n, gen):
    u = np.sqrt(gen.gamma(1.5, 1.0, n)) * gen.choice([-1.0, 1.0], n)
    w = gen.normal(0, math.sqrt(0.5), n)
    return (u + w) / math.sqrt(2), (u - w) / math.sqrt(2)


def sample_neq(n, gen):
    return gen.normal(0, math.sqrt(0.5), n), gen.normal(0, math.sqrt(0.5), n)


def hist(x2):
    return np.histogram(x2, BINS)[0] / x2.size


def tv(a, b):
    return float(0.5 * np.abs(a - b).sum())


# ---------------------------------------------------------------- checks
def closed_f(n, x, t):
    """Closed form of U(t) exp(i k x^2) phi_n(x), n = 0 or 1."""
    A0 = 1 - 2j * KAPPA
    D = np.cos(t) + 1j * A0 * np.sin(t)
    # follow the branch of sqrt(D) continuously from D(0) = 1
    ts = np.linspace(0, t, 2001)
    ph = np.unwrap(np.angle(np.cos(ts) + 1j * A0 * np.sin(ts)))[-1]
    sqrtD = np.sqrt(abs(D)) * np.exp(0.5j * ph)
    Aa = (A0 * np.cos(t) + 1j * np.sin(t)) / D
    g = np.exp(-Aa * x * x / 2)
    if n == 0:
        return np.pi ** -0.25 / sqrtD * g
    return math.sqrt(2) * np.pi ** -0.25 / sqrtD ** 3 * x * g


def splitstep(f, x, t, dt=2.5e-4):
    k = 2 * np.pi * np.fft.fftfreq(x.size, x[1] - x[0])
    half = np.exp(-0.25j * x * x * dt)          # exp(-i V dt/2), V = x^2/2
    kin = np.exp(-0.5j * k * k * dt)
    n = int(round(t / dt))
    for _ in range(n):
        f = half * np.fft.ifft(kin * np.fft.fft(half * f))
    return f


def checks(say):
    x = np.linspace(-20, 20, 4096, endpoint=False)
    phi = [np.pi ** -0.25 * np.exp(-x * x / 2), math.sqrt(2) * np.pi ** -0.25 * x * np.exp(-x * x / 2)]
    err = 0.0
    for nn in (0, 1):
        f = np.exp(1j * KAPPA * x * x) * phi[nn]
        tprev = 0.0
        for t in TIMES:
            f = splitstep(f, x, t - tprev)
            tprev = t
            err = max(err, float(np.max(np.abs(f - closed_f(nn, x, t)))))
    ok_cf = err < 1e-6
    say(f"Check, closed forms vs split-step evolution: max error {err:.2e} -> {'OK' if ok_cf else 'FAILED'}")
    # B's Born marginal for both choices. psi = [f0(x1) p1(x2) e0 + f1(x1) p0(x2) e1]/sqrt(2),
    # so the marginal of x2 needs only the 1D integrals of |f0|^2, |f1|^2 and f0 f1*.
    g = np.linspace(-25, 25, 5001)
    x2 = np.linspace(-4, 4, 81)
    born = (1 + 2 * x2 * x2) * np.exp(-x2 * x2) / (2 * math.sqrt(math.pi))
    p0 = np.pi ** -0.25 * np.exp(-x2 * x2 / 2)
    p1 = math.sqrt(2) * np.pi ** -0.25 * x2 * np.exp(-x2 * x2 / 2)
    mdiff = 0.0
    for t in TIMES:
        for pulsed in (False, True):
            if pulsed:
                f0, f1 = closed_f(0, g, t), closed_f(1, g, t)
            else:
                f0 = np.pi ** -0.25 * np.exp(-g * g / 2) * np.exp(-0.5j * t)
                f1 = math.sqrt(2) * np.pi ** -0.25 * g * np.exp(-g * g / 2) * np.exp(-1.5j * t)
            e0, e1 = np.exp(-1.5j * t), np.exp(-0.5j * t)
            n00 = np.trapezoid(np.abs(f0) ** 2, g)
            n11 = np.trapezoid(np.abs(f1) ** 2, g)
            n01 = np.trapezoid(f0 * np.conj(f1), g)
            marg = 0.5 * (p1 ** 2 * n00 + p0 ** 2 * n11 + 2 * np.real(p1 * p0 * e0 * np.conj(e1) * n01))
            mdiff = max(mdiff, float(np.max(np.abs(marg - born))))
    # the closed-form gradient agrees with a finite difference of ln psi (pulse, t = 1)
    def lnpsi(a, b, t):
        f0 = closed_f(0, np.array([a]), t)[0]; f1 = closed_f(1, np.array([a]), t)[0]
        q0 = np.pi ** -0.25 * math.exp(-b * b / 2); q1 = math.sqrt(2) * b * q0
        return np.log(f0 * q1 * np.exp(-1.5j * t) + f1 * q0 * np.exp(-0.5j * t))
    h, a, b = 1e-5, 0.7, -0.4
    d1 = (lnpsi(a + h, b, 1.0) - lnpsi(a - h, b, 1.0)) / (2 * h)
    d2 = (lnpsi(a, b + h, 1.0) - lnpsi(a, b - h, 1.0)) / (2 * h)
    c1, c2 = grad_ln_psi(a, b, 1.0, True)
    gerr = max(abs(d1 - c1), abs(d2 - c2))
    say(f"  gradient check (pulse, t = 1, x1 = {a}, x2 = {b}): max difference {gerr:.1e}")
    ok_m = mdiff < 1e-10 and gerr < 1e-6
    say(f"Check, B's Born marginal equal for both choices: max difference {mdiff:.1e} "
        f"-> {'OK' if ok_m else 'FAILED'}")
    return ok_cf, ok_m, err, mdiff


def main():
    log = []
    say = lambda s: (print(s, flush=True), log.append(s))
    ok_cf, ok_m, err, mdiff = checks(say)
    gen = np.random.default_rng([2026, 10, 10, 3, 9])
    null = []
    for _ in range(200):
        _, a = sample_eq(N, gen)
        _, b = sample_eq(N, gen)
        null.append(tv(hist(a), hist(b)))
    band = float(np.mean(null) + 3 * np.std(null))
    say(f"Null band: TV mean {np.mean(null):.4f}, sd {np.std(null):.4f}, band {band:.4f}")

    starts = {"equilibrium": sample_eq(N, np.random.default_rng([2026, 10, 10, 3, 0])),
              "not equilibrium": sample_neq(N, np.random.default_rng([2026, 10, 10, 3, 1]))}
    noise = {"equilibrium": [2026, 10, 10, 3, 2], "not equilibrium": [2026, 10, 10, 3, 3]}
    res = dict(band=band, null_mean=float(np.mean(null)), null_sd=float(np.std(null)),
               checks=dict(closed_form=bool(ok_cf), closed_form_err=float(err), marginal=bool(ok_m),
                           marginal_diff=float(mdiff)),
               tv={})
    for rule in ("W1", "W2"):
        for ens, (a1, a2) in starts.items():
            H = {}
            for pulsed in (False, True):
                X1, X2 = a1.copy(), a2.copy()
                st = rs.states(N, noise[ens])
                H[pulsed] = []
                t0, tprev = time.time(), 0.0
                for t in TIMES:
                    if rule == "W1":
                        run_w1(X1, X2, tprev, t, pulsed)
                    else:
                        run_w2(X1, X2, st, tprev, int(round((t - tprev) / 1e-4)), 1e-4, pulsed)
                    tprev = t
                    H[pulsed].append(hist(X2))
                assert np.all(np.isfinite(X1)) and np.all(np.isfinite(X2))
            tvs = [tv(H[False][k], H[True][k]) for k in range(len(TIMES))]
            res["tv"][f"{rule} {ens}"] = tvs
            say(f"{rule}, {ens}: TV between choices at t = {TIMES}: "
                + ", ".join(f"{x:.4f}" for x in tvs) + f"  (band {band:.4f})")
    w1eq = all(x <= band for x in res["tv"]["W1 equilibrium"])
    w1ne = any(x > band for x in res["tv"]["W1 not equilibrium"])
    w2eq = all(x <= band for x in res["tv"]["W2 equilibrium"])
    valid = ok_cf and ok_m
    say(f"TEST 3 (W1): {'PASS' if (w1eq and w1ne) else 'FAIL'} "
        f"(equilibrium inside band: {w1eq}; not equilibrium above band once or more: {w1ne})"
        + ("" if valid else "  -- NOT VALID: a check failed"))
    say(f"TEST 3 (W2, equilibrium part): {'PASS' if w2eq else 'FAIL'}; "
        f"W2 not in equilibrium: report only (above band once or more: "
        f"{any(x > band for x in res['tv']['W2 not equilibrium'])})")
    res.update(w1_pass=bool(w1eq and w1ne), w2_eq_pass=bool(w2eq), valid=bool(valid))
    with open(OUT + "test3.json", "w") as f:
        json.dump(res, f, indent=1)
    with open(OUT + "test3_console.txt", "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
