"""Causal-set core for SIM-SPEC-02 Test 1.

1+1 Minkowski space, c = 1. Light-cone coordinates u = t + x, v = t - x.
Event a precedes event b  <=>  u_a < u_b and v_a < v_b.

The source S sits at the origin. Every sprinkled element lies in the causal
future of S, so S precedes every element and is not stored explicitly.

Chain lengths count elements, both ends included (S and the end point).
The same convention is used for calibration and for the test, so it cancels.
"""
import numpy as np
from numba import njit
from scipy.optimize import minimize

NEG = -(10**9)

# ---------------------------------------------------------------- geometry
T1 = 0.5          # time of the slit plane
T2 = 1.0          # time of the screen
SLITS = (0.1, -0.1)   # slit centres (slit 1, slit 2)
SLIT_W = 0.02     # slit width in x
SLIT_H = 0.01     # slit half-thickness in t (the slit is a thin slab)
XMAX = 0.25       # screen half-width
N_SCREEN = 201


def region_area():
    """Area of J+(S) intersected with the past of the screen segment."""
    tt = np.linspace(0.0, T2, 200001)
    half = np.minimum(tt, XMAX + (T2 - tt))
    return float(np.trapezoid(2.0 * half, tt))


def sprinkle(rho, rng, chunk=4_000_000):
    """Poisson sprinkling of density rho in the region
    |x| <= t and |x| <= XMAX + (T2 - t), 0 <= t <= T2.
    Done by thinning a Poisson process on the box [0,T2] x [-T2,T2]."""
    n_box = rng.poisson(rho * 2.0 * T2 * T2)
    ts, xs = [], []
    left = n_box
    while left > 0:
        k = min(left, chunk)
        t = rng.random(k) * T2
        x = (rng.random(k) * 2.0 - 1.0) * T2
        keep = (np.abs(x) <= t) & (np.abs(x) <= XMAX + (T2 - t))
        ts.append(t[keep])
        xs.append(x[keep])
        left -= k
    return np.concatenate(ts), np.concatenate(xs)


def in_slit(t, x, j):
    s = SLITS[j]
    return (np.abs(t - T1) <= SLIT_H) & (np.abs(x - s) <= SLIT_W / 2.0)


# ---------------------------------------------------------------- Fenwick tree (prefix max)
@njit(cache=True)
def _fw_query(tree, i):
    r = NEG
    while i > 0:
        if tree[i] > r:
            r = tree[i]
        i -= i & (-i)
    return r


@njit(cache=True)
def _fw_update(tree, i, val):
    n = tree.shape[0] - 1
    while i <= n:
        if tree[i] < val:
            tree[i] = val
        i += i & (-i)


@njit(cache=True)
def _forward_from_S(order, vrank, is_query):
    """L[p] = longest chain S -> ... -> p (elements counted, ends included).
    Queries are evaluated but not inserted."""
    n = order.shape[0]
    tree = np.full(n + 1, NEG, dtype=np.int64)
    L = np.zeros(n, dtype=np.int64)
    for k in range(n):
        p = order[k]
        q = _fw_query(tree, vrank[p] - 1)
        best = q if q > 1 else 1          # S itself (length 1) always precedes p
        L[p] = best + 1
        if not is_query[p]:
            _fw_update(tree, vrank[p], L[p])
    return L


@njit(cache=True)
def _through_slit(order, vrank, is_query, LS, slit):
    """F[p] = longest chain S -> ... -> e -> ... -> p that contains at least one
    element e in the slit. NEG-ish if none exists. Queries are not inserted."""
    n = order.shape[0]
    tree = np.full(n + 1, NEG, dtype=np.int64)
    F = np.full(n, NEG, dtype=np.int64)
    for k in range(n):
        p = order[k]
        q = _fw_query(tree, vrank[p] - 1)
        val = q + 1 if q > NEG // 2 else NEG
        if (not is_query[p]) and slit[p]:
            if LS[p] > val:
                val = LS[p]
        F[p] = val
        if not is_query[p]:
            _fw_update(tree, vrank[p], val)
    return F


def _prepare(t, x, qt, qx):
    """Stack elements and queries; return order by u and 1-based v ranks."""
    tt = np.concatenate([t, qt])
    xx = np.concatenate([x, qx])
    u = tt + xx
    v = tt - xx
    order = np.argsort(u, kind="stable").astype(np.int64)
    vrank = np.empty(len(v), dtype=np.int64)
    vrank[np.argsort(v, kind="stable")] = np.arange(1, len(v) + 1)
    is_query = np.zeros(len(tt), dtype=np.bool_)
    is_query[len(t):] = True
    return tt, xx, order, vrank, is_query


def chain_to_points(t, x, qt, qx):
    """Longest chain from S to each query point (straight histories)."""
    tt, xx, order, vrank, is_query = _prepare(t, x, qt, qx)
    L = _forward_from_S(order, vrank, is_query)
    return L[len(t):]


def chain_through_slits(t, x, qt, qx):
    """Longest chain from S to each query point through slit 1 and slit 2."""
    tt, xx, order, vrank, is_query = _prepare(t, x, qt, qx)
    LS = _forward_from_S(order, vrank, is_query)
    out = []
    for j in range(2):
        slit = np.zeros(len(tt), dtype=np.bool_)
        slit[: len(t)] = in_slit(t, x, j)
        F = _through_slit(order, vrank, is_query, LS, slit)
        out.append(F[len(t):])
    return out[0], out[1]


# ---------------------------------------------------------------- continuum reference
def tau(dt, dx):
    return np.sqrt(np.maximum(dt * dt - dx * dx, 0.0))


def tau_through_slit(X, j, ngrid=81):
    """Max over points p in slit j of tau(S, p) + tau(p, (T2, X)).
    The function is concave on the slab, so grid + bounded local refine."""
    s = SLITS[j]
    tg = np.linspace(T1 - SLIT_H, T1 + SLIT_H, 21)
    xg = np.linspace(s - SLIT_W / 2, s + SLIT_W / 2, ngrid)
    TT, XX = np.meshgrid(tg, xg, indexing="ij")
    val = tau(TT, XX) + tau(T2 - TT, X - XX)
    k = np.unravel_index(np.argmax(val), val.shape)
    p0 = np.array([TT[k], XX[k]])
    f = lambda p: -(tau(p[0], p[1]) + tau(T2 - p[0], X - p[1]))
    res = minimize(f, p0, method="L-BFGS-B",
                   bounds=[(T1 - SLIT_H, T1 + SLIT_H), (s - SLIT_W / 2, s + SLIT_W / 2)])
    return max(-res.fun, val[k])


def screen():
    return np.linspace(-XMAX, XMAX, N_SCREEN)


def continuum_taus():
    X = screen()
    t1 = np.array([tau_through_slit(xx, 0) for xx in X])
    t2 = np.array([tau_through_slit(xx, 1) for xx in X])
    return X, t1, t2
