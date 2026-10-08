import json, numpy as np
from chain import potential, ground_corr, entropy
from first_law import region_response

def run(m, d, kind, N=1600, wfac=0.25):
    c = N // 2; sites = np.arange(c, N); xc = c - 0.5
    beta = lambda x: 2*np.pi*(x - xc)
    bs = beta(sites.astype(float)); bl = beta(sites[:-1] + 0.5)
    w = max(wfac*d, 1.0); x0 = xc + d
    j = np.arange(N) if kind == "site" else np.arange(N-1) + 0.5
    g = np.exp(-((j-x0)**2)/(2*w*w))
    lam = 0.01*m*m if kind == "site" else 1e-3
    r = region_response(N, m, sites, bs, bl, (kind, g), lam=lam)
    r.update(m=m, d=d, d_over_xi=d*m, w=w, kind=kind)
    return r

out = []
for m in (0.05, 0.1, 0.2):
    for dxi in (0.2, 0.4, 0.8, 1.2, 1.6, 2.4):
        d = max(int(round(dxi/m)), 3)
        for kind in ("site", "link"):
            r = run(m, d, kind); out.append(r)
            print("m=%.2f d=%3d d/xi=%.2f %s ratio=%.4f dS=%.3e" % (m, d, d*m, kind, r["ratio"], r["dS"]), flush=True)
json.dump(out, open("results/rindler_scan.json", "w"), indent=1)
