"""Figures for RESULTS-04 (SIM-SPEC-03, selection), from the analysis .json files."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

R = "results/"
PI = np.pi


def fig_box():
    d = json.load(open(R + "test1a_test2w1.json"))
    c = d["curves"]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    Ms = sorted(int(k) for k in d["tau"])
    cmap = plt.get_cmap("viridis")
    for i, M in enumerate(Ms):
        Hs = np.array([c[f"M{M}_s{s}"]["H"][:33] for s in range(6)])
        t = np.array(c[f"M{M}_s0"]["t"][:33])
        ax[0].semilogy(t / PI, Hs.mean(0), color=cmap(i / (len(Ms) - 1)), label=f"M = {M}")
    fl = np.array(c["M64_s0"]["Hfloor"][:33])
    ax[0].semilogy(t / PI, 10 * fl, "k:", label="10 × noise floor")
    ax[0].semilogy(np.array(c["equiv"]["t"]) / PI, c["equiv"]["H"], "k--", lw=1, label="Born start (check)")
    ax[0].set_xlabel("t / π"); ax[0].set_ylabel("H̄ (mean of 6 phase sets)")
    ax[0].set_title("Test 1a: W1 relaxation in the TRV box"); ax[0].legend(fontsize=7)
    fitM = d["test1a"]["fit_M"]
    x = np.array(Ms, float)
    y = np.array([d["tau"][str(M)]["mean"] for M in Ms])
    e = np.array([d["tau"][str(M)]["sd"] for M in Ms])
    ax[1].errorbar(x, y, e, fmt="o", capsize=3, label="this run (mean ± sd, 6 sets)")
    xx = np.linspace(8, 70, 50)
    A, p = d["test1a"]["A"], d["test1a"]["p"]
    ax[1].loglog(xx, A * xx ** p, "-", label=f"fit: p = {p:.2f} ± {d['test1a']['p_se']:.2f}")
    ax[1].loglog(xx, A * xx ** p * (xx / fitM[0]) ** (-1.05 - p), "--", color="grey", label="slope −1.05 (TRV)")
    ax[1].set_xticks(Ms); ax[1].set_xticklabels([str(M) for M in Ms]); ax[1].minorticks_off()
    ax[1].set_xlabel("M (modes)"); ax[1].set_ylabel("τ"); ax[1].set_title("Test 1a: τ against M (M = 4 not fitted)")
    ax[1].legend(fontsize=7)
    for s in range(6):
        k = c[f"M64_s{s}"]
        ax[2].semilogy(np.array(k["t"]) / PI, k["TV"], lw=1, label=f"set {s}")
    k = c["M64_s0"]
    ax[2].semilogy(np.array(k["t"]) / PI, np.array(k["TVfloor"]) + 3 * np.array(k["TVsd"]), "k:",
                   label="floor + 3 sd")
    ax[2].set_xlabel("t_rec / π"); ax[2].set_ylabel("TV of the record from Born")
    ax[2].set_title("Test 2 (W1): M = 64, 4 × 4 regions"); ax[2].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(R + "fig_w1_box.png", dpi=130)


def fig_nelson():
    d = json.load(open(R + "test1b_test2w2.json"))
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    sig = sorted(d["curves"], key=float)
    cmap = plt.get_cmap("plasma")
    for i, s in enumerate(sig):
        k = d["curves"][s]
        ax[0].semilogy(k["t"], k["L1"], color=cmap(i / len(sig)), label=f"σ = {s}")
    ax[0].axhline(3 * d["floors"]["L1"][0], color="k", ls=":", label="3 × noise floor")
    ax[0].set_xlim(0, 0.6); ax[0].set_xlabel("t"); ax[0].set_ylabel("L1 from Born")
    ax[0].set_title("Test 1b: W2 relaxation in the double slit"); ax[0].legend(fontsize=7)
    x = np.array([float(s) for s in sig])
    ax[1].plot(x, [d["sigma"][s]["tau_q"] for s in sig], "o-", label="τ_q (relaxation)")
    ax[1].plot(x, [d["sigma"][s]["tau_int_literal"] for s in sig], "s-", label="τ_int, literal")
    ax[1].plot(x, [d["sigma"][s]["tau_int_visible"] for s in sig], "^--", label="τ_int, visible peak")
    ax[1].set_xlabel("σ / a"); ax[1].set_ylabel("time"); ax[1].set_title("Test 1b: relaxation against fringes")
    ax[1].legend(fontsize=7)
    t2 = d["test2_w2"]
    ax[2].semilogy(t2["t"], t2["TV"], label="TV of the record, 20 bins")
    ax[2].axhline(t2["band"], color="k", ls=":", label="floor + 3 sd")
    ax[2].axvline(t2["tau_q"], color="grey", ls="--", label="τ_q")
    ax[2].set_xlabel("t_rec"); ax[2].set_ylabel("TV from Born")
    ax[2].set_title("Test 2 (W2): σ = 0.4"); ax[2].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(R + "fig_w2_nelson.png", dpi=130)


def fig_signal():
    d = json.load(open(R + "test3.json"))
    t = [0.5, 1, 2, 3]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for k, m in zip(d["tv"], "osD^"):
        ax.semilogy(t, d["tv"][k], m + "-", label=k)
    ax.axhline(d["band"], color="k", ls=":", label="null band")
    ax.set_xlabel("t"); ax.set_ylabel("TV of B's statistics between A's two choices")
    ax.set_title("Test 3: signals"); ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(R + "fig_signal.png", dpi=130)


if __name__ == "__main__":
    for f in (fig_box, fig_nelson, fig_signal):
        try:
            f()
        except FileNotFoundError as e:
            print("skip", f.__name__, e)


def fig_rerun():
    d = json.load(open(R + "rerun_w2.json"))
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    sig = sorted(d["curves"], key=float)
    cmap = plt.get_cmap("plasma")
    fl = d["floors"]["L1"][0]
    for i, s in enumerate(sig):
        k = d["curves"][s]; v = d["sigma"][s]; col = cmap(i / len(sig))
        t = np.array(k["t"]); L = np.array(k["L1"])
        ax[0].loglog(t[1:], L[1:], color=col, label=f"σ = {s}")
        ax[0].plot(v["t_half"], L[0] / 2, "o", color=col, ms=4)
        ax[0].plot(v["tau_int_literal"], v["L1_at_literal"], "s", color=col, ms=5, mfc="none")
    ax[0].axhline(3 * fl, color="k", ls=":", label="3 × noise floor")
    ax[0].set_xlabel("t"); ax[0].set_ylabel("L1 from Born")
    ax[0].set_title("W2 second test: dots = half time, squares = first fringe"); ax[0].legend(fontsize=7)
    x = np.array([float(s) for s in sig])
    ax[1].semilogy(x, [d["sigma"][s]["t_half"] for s in sig], "o-", label="t½ (half of the relaxation)")
    ax[1].semilogy(x, [d["sigma"][s]["tau_int_literal"] for s in sig], "s-", label="τ_int, literal (first fringe)")
    ax[1].semilogy(x, [d["sigma"][s]["t_3"] for s in sig], "^-", label="t₃ (L1 at 3 × floor)")
    ax[1].set_xlabel("σ / a"); ax[1].set_ylabel("time")
    ax[1].set_title("Bulk before the first fringe; completion after it"); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(R + "fig_w2_rerun.png", dpi=130)


if __name__ == "__main__":
    fig_rerun()
