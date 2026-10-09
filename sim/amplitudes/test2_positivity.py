"""SIM-SPEC-02 Test 2 — Is positivity doing the work?

A comparison rule f depends only on the difference of clock readings (A2):
D(h, h') = f(n_h - n_h'), with f(-n) = f(n) here (real, symmetric kernels).
An event A is a set of histories; several histories may share a reading, so
an event is a vector of counts c_a >= 0 over readings a, and
    P(A) = sum_{a,b} c_a c_b f(a - b).

Three settings are searched for an event with P < 0:
  ALONE      — the system by itself: counts c_a in {0,..,3}.
  COPY       — composed with an independent second copy of the same kernel:
               events are arbitrary sets of joint histories (a, b);
               D = f(a - a') f(b - b').
  QUBIT      — composed with one independent quantum two-state system with
               amplitudes (1, -1) (a valid, positive decoherence functional
               D2 = psi_b psi_b'). An event picks counts at (a, 0) and (a, 1);
               P = c^T F c with c_a = count(a,0) - count(a,1) in {-3,..,3}.

Whether f is positive semidefinite (as a function on the integers) is decided
independently by Herglotz: its Fourier series must be >= 0 everywhere.

Kernel families:
  K1  short range: f(0) = 1, f(+-1) = a, a in -1.0 .. 1.0 step 0.1
      (positive semidefinite exactly when |a| <= 1/2).
  K2  random cosine series f(n) = sum_k w_k cos(n theta_k), 3 terms,
      normalised to f(0) = 1: 15 with all w_k > 0, 15 with one w_k < 0.
  K3  random short range: f(0) = 1, f(+-n) uniform in [-0.6, 0.6], n = 1..3;
      30 kernels.

Search window: readings 0..W-1, with W grown (16, 32, 64, 128, 256) until the
windowed matrix has a negative eigenvalue; ALONE and COPY use W <= 16 and
W <= 8 per factor. Searches: exhaustive 0/1 events where small, roundings of
negative eigenvectors, and single-move local search from random starts.

Pass (SIM-SPEC-02 §5 Test 2, fixed before the run): every kernel that is not
positive semidefinite gives P < 0 in at least one setting; no positive
semidefinite kernel ever does. Kernels caught only under composition are
recorded: those are the cases where assumption A3 does the deciding.
"""
import json
import itertools
import numpy as np

rng = np.random.default_rng(20261009)
TOL = 1e-10


def short_range(vals):
    return lambda n, vals=vals: vals.get(abs(int(n)), 0.0)


def toeplitz(f, W):
    idx = np.arange(W)
    return np.vectorize(f)(idx[:, None] - idx[None, :]).astype(float)


def herglotz_min(f, R):
    th = np.linspace(0, np.pi, 20001)
    s = f(0) + 2 * sum(f(n) * np.cos(n * th) for n in range(1, R + 1))
    return float(s.min())


def local_search(Fm, lo, hi, starts, iters=4000):
    """Minimise c^T F c / max(1, |c|^2) over integer c in [lo, hi]^W."""
    W = Fm.shape[0]
    best = np.inf
    for c in starts:
        c = c.astype(float).copy()
        val = c @ Fm @ c
        improved = True
        steps = 0
        while improved and steps < iters:
            improved = False
            steps += 1
            g = Fm @ c
            for i in rng.permutation(W):
                for d in (-1, 1):
                    if not (lo <= c[i] + d <= hi):
                        continue
                    newval = val + 2 * d * g[i] + d * d * Fm[i, i]
                    if newval < val - 1e-12:
                        c[i] += d
                        val = newval
                        g = g + d * Fm[:, i]
                        improved = True
        best = min(best, val)
        if best < -TOL:
            return best
    return best


def rounded_eig_starts(Fm, lo, hi, n_rand=60):
    w, V = np.linalg.eigh(Fm)
    starts = []
    for j in range(min(3, len(w))):
        v = V[:, j] / np.abs(V[:, j]).max()
        for scale in (1, 2, 3):
            starts.append(np.clip(np.round(v * scale), lo, hi))
            starts.append(np.clip(np.round(-v * scale), lo, hi))
    W = Fm.shape[0]
    for _ in range(n_rand):
        starts.append(rng.integers(lo, hi + 1, size=W))
    return starts


def search_alone(Fm):
    W = Fm.shape[0]
    best = np.inf
    if W <= 16:
        B = np.array(list(itertools.product((0, 1), repeat=W)), dtype=float)
        best = float(np.min(np.einsum("ij,jk,ik->i", B, Fm, B)))
        if best < -TOL:
            return best
    return min(best, local_search(Fm, 0, 3, rounded_eig_starts(Fm, 0, 3)))


def search_copy(Fm):
    W = min(Fm.shape[0], 8)
    F = Fm[:W, :W]
    K = np.kron(F, F)
    w, V = np.linalg.eigh(F)
    starts = []
    for i in range(W):
        for j in range(W):
            out = np.outer(V[:, i], V[:, j]).ravel()
            for sgn in (1, -1):
                starts.append((sgn * out > 0).astype(float))
    for _ in range(200):
        starts.append(rng.integers(0, 2, size=W * W))
    return local_search(K, 0, 1, starts)


def search_qubit(Fm):
    return local_search(Fm, -3, 3, rounded_eig_starts(Fm, -3, 3))


def evaluate(name, f, R=None, psd_exact=None):
    """R: support radius for the Herglotz check (short-range kernels).
    psd_exact: known answer for kernels whose Fourier measure is a sum of
    point masses (K2), where a truncated Fourier sum would mislead."""
    if psd_exact is None:
        hmin = herglotz_min(f, R)
        psd = hmin >= -1e-12
    else:
        hmin = float("nan")
        psd = psd_exact
    W = 16
    Fm = toeplitz(f, W)
    while not psd and np.linalg.eigvalsh(Fm).min() >= -TOL and W < 256:
        W *= 2
        Fm = toeplitz(f, W)
    a = search_alone(toeplitz(f, min(W, 16)))
    c = search_copy(toeplitz(f, 8))
    q = search_qubit(Fm)
    neg = {k: v < -TOL for k, v in (("alone", a), ("copy", c), ("qubit", q))}
    return dict(name=name, psd=bool(psd), herglotz_min=hmin, window=W,
                min_eig_window=float(np.linalg.eigvalsh(Fm).min()),
                alone=float(a), copy=float(c), qubit=float(q),
                caught=bool(any(neg.values())),
                only_under_composition=bool((neg["copy"] or neg["qubit"]) and not neg["alone"]))


def main():
    rows = []
    for a in np.round(np.arange(-1.0, 1.0001, 0.1), 2):
        rows.append(evaluate(f"K1 a={a:+.1f}", short_range({0: 1.0, 1: float(a)}), R=1))
    for k in range(30):
        th = rng.uniform(0.2, np.pi, 3)
        w = rng.uniform(0.2, 1.0, 3)
        if k >= 15:
            w[rng.integers(3)] *= -1
        if w.sum() <= 0.05:
            w[np.argmax(w)] += 1.0
        w = w / w.sum()
        fv = lambda n, th=th, w=w: float(np.sum(w * np.cos(n * th)))
        # Fourier measure = point masses w_k at +-theta_k: PSD exactly when all w_k >= 0
        rows.append(evaluate(f"K2 #{k:02d}", fv, psd_exact=bool(np.all(w >= 0))))
    for k in range(30):
        vals = {0: 1.0}
        vals.update({n: float(rng.uniform(-0.6, 0.6)) for n in (1, 2, 3)})
        rows.append(evaluate(f"K3 #{k:02d}", short_range(vals), R=3))

    log = []
    say = lambda s: (print(s), log.append(s))
    say(f"{'kernel':<12} {'PSD':<5} {'Herglotz min':>12} {'W':>4} {'alone':>10} {'copy':>10} {'qubit':>10}  verdict")
    bad = []
    for r in rows:
        verdict = ("never negative" if not r["caught"] else
                   ("NEGATIVE only under composition" if r["only_under_composition"] else "NEGATIVE alone"))
        ok = (r["psd"] and not r["caught"]) or ((not r["psd"]) and r["caught"])
        if not ok:
            bad.append(r["name"])
        say(f"{r['name']:<12} {str(r['psd']):<5} {r['herglotz_min']:>12.4f} {r['window']:>4} "
            f"{r['alone']:>10.3f} {r['copy']:>10.3f} {r['qubit']:>10.3f}  {verdict}{'' if ok else '   <-- MISMATCH'}")
    n_psd = sum(r["psd"] for r in rows)
    n_non = len(rows) - n_psd
    n_caught = sum(r["caught"] for r in rows if not r["psd"])
    n_only = sum(r["only_under_composition"] for r in rows if not r["psd"])
    n_psd_neg = sum(r["caught"] for r in rows if r["psd"])
    say("")
    say(f"Kernels: {len(rows)} ({n_psd} positive semidefinite, {n_non} not)")
    say(f"Not PSD and caught: {n_caught}/{n_non}; of those, caught only under composition: {n_only}")
    say(f"PSD and ever negative: {n_psd_neg}/{n_psd}")
    say(f"TEST 2: {'PASS' if not bad else 'FAIL'}" + (f"  mismatches: {bad}" if bad else ""))
    with open("results/test2.json", "w") as f:
        json.dump(dict(rows=rows, passed=not bad, mismatches=bad), f, indent=1)
    with open("results/test2_console.txt", "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
