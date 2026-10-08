"""3+1D check of the 2*pi rule for a small ball, via Srednicki's partial waves.

NOTE: the __main__ run here (a mass-term bump) was DISCARDED. In 3+1D a mass
bump changes the field's short-distance structure and the energy response grows
with the cutoff. The canonical 3D check is ball3d_squeeze.py + ball3d_fit.py,
which import radial_V from this file.

Massless free scalar on a radial lattice (spacing 1, r_j = j, j = 1..N).
Per angular momentum l, the radial chain is
  H_l = 1/2 sum_j [ pi_j^2 + (j+1/2)^2 (phi_j/j - phi_{j+1}/(j+1))^2 + (l(l+1)/j^2 + m_j^2) phi_j^2 ]
and the full field is the sum over l with degeneracy (2l+1).

Ball = sites j <= n, boundary R = n + 1/2. Hislop-Longo weight
  beta(r) = 2*pi * (R^2 - r^2) / (2R).
Perturbation: a spherically symmetric bump in the local mass term,
  m_j^2 -> lam * g(r_j), applied to every l channel.

Compared:
  dS                  change in the ball's entanglement entropy (summed over l)
  dK_canonical        sum beta * d<T00> with the canonical energy density
  dK_improved         same with the conformally improved energy density
                      T00 - xi * Laplacian(phi^2), xi = 1/6
"""
import json
import sys
import numpy as np
from chain import ground_corr, entropy

XI = 1.0 / 6.0


def radial_V(N, l, msq):
    j = np.arange(1, N + 1, dtype=float)
    V = np.zeros((N, N))
    # gradient term (j+1/2)^2 (phi_j/j - phi_{j+1}/(j+1))^2, j = 1..N (phi_{N+1}=0)
    for k in range(N):
        jj = j[k]; c = (jj + 0.5) ** 2
        V[k, k] += c / jj ** 2
        if k + 1 < N:
            jn = j[k + 1]
            V[k + 1, k + 1] += c / jn ** 2
            V[k, k + 1] -= c / (jj * jn)
            V[k + 1, k] -= c / (jj * jn)
    V += np.diag(l * (l + 1) / j ** 2 + msq)
    return V


def channel(N, n, l, msq0, bump, lam):
    """Return (dS_l, dKcan_l, dphi2_l per site) for one l channel (symmetric difference)."""
    j = np.arange(1, N + 1, dtype=float)
    R = n + 0.5
    beta = lambda r: np.pi * (R * R - r * r) / R
    res = {}
    for sgn in (1, -1):
        V = radial_V(N, l, msq0 + sgn * lam * bump)
        X, P = ground_corr(V)
        S = entropy(X[:n, :n], P[:n, :n])
        d = np.diag(X)
        site_e = 0.5 * np.diag(P) + 0.5 * (l * (l + 1) / j ** 2 + msq0) * d
        # link energy between j and j+1 (positions j+1/2)
        off = np.diag(X, 1)
        jj = j[:-1]; jn = j[1:]
        link_e = 0.5 * (jj + 0.5) ** 2 * (d[:-1] / jj ** 2 + d[1:] / jn ** 2 - 2 * off / (jj * jn))
        Kcan = np.sum(beta(j[:n]) * site_e[:n]) + np.sum(beta(j[:n - 1] + 0.5) * link_e[:n - 1])
        res[sgn] = (S, Kcan, d)
    dS = (res[1][0] - res[-1][0]) / 2
    dK = (res[1][1] - res[-1][1]) / 2
    dX = (res[1][2] - res[-1][2]) / 2
    return dS, dK, dX


def run(n=20, Nfac=8, x0f=0.4, wf=0.15, lam=1e-3, lmax=400, msq0=0.0):
    N = Nfac * n
    j = np.arange(1, N + 1, dtype=float)
    R = n + 0.5
    beta = lambda r: np.pi * (R * R - r * r) / R
    x0, w = x0f * R, max(wf * R, 1.0)
    bump = np.exp(-((j - x0) ** 2) / (2 * w * w))
    dS = dK = 0.0
    dphi2 = np.zeros(N)            # d<phi(x)^2> at radius r_j (sum over l)
    partial = []
    for l in range(lmax + 1):
        s, k, dX = channel(N, n, l, msq0, bump, lam)
        deg = 2 * l + 1
        dS += deg * s; dK += deg * k
        dphi2 += deg * dX / (4 * np.pi * j ** 2)
        if l in (10, 25, 50, 100, 200, 300, 400, 600, 800):
            partial.append({"lmax": l, "dS": dS, "dK_can": dK})
    # improvement: -xi * integral over ball of beta * Laplacian(d<phi^2>), discrete radial Laplacian
    f = dphi2
    lap = np.zeros(N)
    for k in range(N):
        jj = j[k]
        fp = f[k + 1] if k + 1 < N else 0.0
        fm = f[k - 1] if k > 0 else f[k]       # regular at the origin
        lap[k] = ((jj + 0.5) ** 2 * (fp - f[k]) - (jj - 0.5) ** 2 * (f[k] - fm)) / jj ** 2
    vol = 4 * np.pi * j ** 2                   # shell volume (spacing 1)
    dImp = -XI * np.sum((beta(j[:n]) * lap[:n] * vol[:n]))
    dK_imp = dK + dImp
    return {"n": n, "R": R, "N": N, "lmax": lmax, "bump_center": x0, "bump_width": w,
            "dS": dS, "dK_canonical": dK, "dK_improved": dK_imp,
            "ratio_canonical": dS / dK, "ratio_improved": dS / dK_imp, "partial_sums": partial}


if __name__ == "__main__":
    out = []
    for n in (int(a) for a in sys.argv[1:]) if len(sys.argv) > 1 else (10, 20, 30):
        r = run(n=n, lmax=int(12 * n + 100))
        out.append(r)
        print(json.dumps({k: v for k, v in r.items() if k != "partial_sums"}), flush=True)
        for p in r["partial_sums"]:
            print("   lmax=%d dS=%.6e dKcan=%.6e" % (p["lmax"], p["dS"], p["dK_can"]), flush=True)
    json.dump(out, open("results/ball3d_massbump_DISCARDED.json", "w"), indent=1)
