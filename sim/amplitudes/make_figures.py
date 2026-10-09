"""Figures for RESULTS-03 from the committed JSON (no re-computation)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("results/test1.json"))
X = np.array(r["X"])
phi_c = np.array(r["phi_c"])
Pc = 2 + 2 * np.cos(phi_c)

fig, axes = plt.subplots(1, 3, figsize=(13, 3.6), sharey=True)
for ax, rho in zip(axes, ["30000.0", "1000000.0", "10000000.0"]):
    ex = r["examples"][rho]
    Pd = 2 + 2 * np.cos(np.array(ex["phi_d"]))
    ax.plot(X, Pc, color="0.6", lw=2.5, label="continuum (exact proper times)")
    ax.plot(X, Pd, color="#2c47d4", lw=1.2, label="link counts (one sprinkling)")
    ax.set_title(f"density {float(rho):.0e}  (N = {ex['N']:,} elements)", fontsize=10)
    ax.set_xlabel("screen position")
axes[0].set_ylabel("intensity |e^{iφ₁}+e^{iφ₂}|²")
axes[0].legend(fontsize=8, loc="lower left")
fig.tight_layout()
fig.savefig("results/fig1_patterns.png", dpi=130)

rhos = np.array([d["rho"] for d in r["densities"]])
def stat(key):
    v = np.array([[x[key] for x in d["calibrated"]] for d in r["densities"]])
    return v.mean(1), v.std(1, ddof=1) / np.sqrt(v.shape[1])
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
m, e = stat("corr")
axes[0].errorbar(rhos, 1 - m, e, fmt="o-", color="#2c47d4"); axes[0].set_xscale("log"); axes[0].set_yscale("log")
axes[0].set_title("1 − pattern correlation", fontsize=10)
m, e = stat("spacing_ratio")
axes[1].errorbar(rhos, m, e, fmt="o-", color="#2c47d4"); axes[1].axhspan(0.98, 1.02, color="0.9")
axes[1].axhline(1, color="0.5", lw=0.8); axes[1].set_xscale("log"); axes[1].set_title("fringe spacing / continuum (band = ±2%)", fontsize=10)
m, e = stat("rms_unwrapped")
axes[2].errorbar(rhos, m, e, fmt="o-", color="#2c47d4", label="measured")
axes[2].plot(rhos, m[0] * (rhos / rhos[0]) ** (-1 / 3), "--", color="0.5", label="ρ^(−1/3)")
axes[2].set_xscale("log"); axes[2].set_yscale("log"); axes[2].legend(fontsize=8)
axes[2].set_title("RMS phase error (rad)", fontsize=10)
for ax in axes:
    ax.set_xlabel("sprinkling density ρ")
fig.tight_layout()
fig.savefig("results/fig2_convergence.png", dpi=130)
print("figures written")
