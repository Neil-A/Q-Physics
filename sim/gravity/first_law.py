"""Does empty rubber's linking respond to energy with the 2*pi (Unruh) factor?

For a region A of the lattice vacuum, perturb the field locally, and compare
  dS                 (change in entanglement entropy of A)
with
  dK_BW = sum_x beta(x) * d<h(x)>   (distance-weighted change in energy)
where beta is the Bisognano-Wichmann / Hislop-Longo weight:
  half-line (Rindler horizon):  beta(x) = 2*pi*(x - x_cut)
  interval  (small 'ball'):     beta(x) = 2*pi*(x-xa)*(xb-x)/(xb-xa)
In the continuum, dS = dK_BW exactly at first order (the 'first law of
entanglement' with a local modular Hamiltonian). This is ingredient 3+4 of
Jacobson's argument. Ratio dS/dK_BW -> 1 is the test.
"""
import json
import sys
import numpy as np
from chain import potential, ground_corr, entropy, modular_matrices

OUT = {}


def region_response(N, m, sites, beta_site, beta_link, pert, lam=1e-3, check_true_K=False):
    A = np.asarray(sites)
    res = {}
    vals = {}
    for sgn in (+1, -1):
        kind, g = pert
        V = potential(N, m, bump=sgn * lam * g if kind == "site" else None,
                      link_bump=sgn * lam * g if kind == "link" else None)
        X, P = ground_corr(V)
        XA, PA = X[np.ix_(A, A)], P[np.ix_(A, A)]
        S = entropy(XA, PA)
        d = np.diag(X)
        onsite = 0.5 * np.diag(P) + 0.5 * m * m * d
        link = 0.5 * (d[1:] + d[:-1] - 2 * np.diag(X, 1))
        Kbw = float(np.sum(beta_site * onsite[A]) + np.sum(beta_link * link[A[:-1]]))
        vals[sgn] = (S, Kbw, XA, PA)
    dS = (vals[1][0] - vals[-1][0]) / 2
    dK = (vals[1][1] - vals[-1][1]) / 2
    res.update(dS=dS, dK_BW=dK, ratio=dS / dK)
    if check_true_K:
        V0 = potential(N, m)
        X0, P0 = ground_corr(V0)
        XA0, PA0 = X0[np.ix_(A, A)], P0[np.ix_(A, A)]
        M, Nm = modular_matrices(XA0, PA0)
        dX = (vals[1][2] - vals[-1][2]) / 2
        dP = (vals[1][3] - vals[-1][3]) / 2
        dKtrue = 0.5 * (np.sum(M * dX) + np.sum(Nm * dP))
        res.update(dK_true=float(dKtrue), first_law_identity_ratio=float(dS / dKtrue))
    return res


def interval_case(L, Nfac=10, m=0.0, x0_frac=0.15, w_frac=0.1, kind="site", check=False, lam=1e-3):
    N = Nfac * L
    a = N // 2 - L // 2
    sites = np.arange(a, a + L)
    xa, xb = a - 0.5, a + L - 0.5
    beta = lambda x: 2 * np.pi * (x - xa) * (xb - x) / (xb - xa)
    bs = beta(sites.astype(float))
    bl = beta(sites[:-1] + 0.5)
    x0 = (xa + xb) / 2 + x0_frac * L
    w = max(w_frac * L, 1.0)
    j = np.arange(N) if kind == "site" else np.arange(N - 1) + 0.5
    g = np.exp(-((j - x0) ** 2) / (2 * w * w))
    r = region_response(N, m, sites, bs, bl, (kind, g), lam=lam, check_true_K=check)
    r.update(L=L, N=N, m=m, bump_center_from_mid=x0_frac * L, bump_width=w, kind=kind)
    return r


def rindler_case(m, d, wfac=0.25, N=2000, kind="site", check=False, lam=1e-3):
    c = N // 2
    sites = np.arange(c, N)
    xc = c - 0.5
    beta = lambda x: 2 * np.pi * (x - xc)
    bs = beta(sites.astype(float))
    bl = beta(sites[:-1] + 0.5)
    x0 = xc + d
    w = max(wfac * d, 1.0)
    j = np.arange(N) if kind == "site" else np.arange(N - 1) + 0.5
    g = np.exp(-((j - x0) ** 2) / (2 * w * w))
    r = region_response(N, m, sites, bs, bl, (kind, g), lam=lam, check_true_K=check)
    r.update(m=m, distance_from_horizon=d, bump_width=w, kind=kind, N=N)
    return r


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("sanity", "all"):
        OUT["sanity_first_law_identity"] = [
            # small nudges: lam well below the stiffness (link) and below m^2 (site)
            interval_case(24, Nfac=8, kind="link", check=True, lam=1e-4),
            rindler_case(0.1, 20, N=600, check=True, lam=1e-4),
        ]
    if which in ("interval", "all"):
        OUT["interval_massless_link_bump"] = [interval_case(L, kind="link") for L in (8, 16, 32, 64, 128, 256)]
        OUT["interval_bump_position_L128"] = [interval_case(128, kind="link", x0_frac=f) for f in (0.0, 0.15, 0.3, 0.4)]
    if which == "rindler":
        # SUPERSEDED by rindler_scan.py: these site bumps are too strong for the
        # lightest mass (lam > m^2), so they are not small disturbances. Kept only
        # so the first, discarded run can be reproduced.
        OUT["rindler"] = [rindler_case(m, d) for m in (0.02, 0.05, 0.1) for d in (8, 16, 32, 64)]
        OUT["rindler_link_bump"] = [rindler_case(0.05, d, kind="link") for d in (8, 16, 32, 64)]
    print(json.dumps(OUT, indent=1))
    json.dump(OUT, open(f"results/first_law_{which}.json", "w"), indent=1)
