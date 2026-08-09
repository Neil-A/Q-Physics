"""Figures for SIM-SPEC-01."""

import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('results', exist_ok=True)
J = lambda p: json.load(open(f'results/{p}.json'))

t1, t2, t3, t3b, t3c = J('test1'), J('test2'), J('test3'), J('test3b'), J('test3c')

# ---------------------------------------------------------------- fig 1
sweep = np.load('results/test1_sweep.npy')
inv = np.load('results/test1_inversion.npy')
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(sweep[:, 0], sweep[:, 1], label='$l_1$-norm')
ax[0].plot(sweep[:, 0], sweep[:, 2], label='rel. entropy')
ax[0].plot(sweep[:, 0], sweep[:, 3], label='geometric')
ax[0].set_xlabel('dephasing $p$'); ax[0].set_ylabel('coherence')
ax[0].set_title('Test 1a: endpoints and monotonicity'); ax[0].legend(); ax[0].grid(alpha=.3)
ax[1].plot(inv[:, 0], inv[:, 1], label='coherence ($l_1$)')
ax[1].plot(inv[:, 0], inv[:, 3], label='entanglement entropy')
ax[1].set_xlabel(r'record strength $\theta$')
ax[1].set_title('Test 1b: the inversion (Spearman $=-1$)')
ax[1].legend(); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig('results/fig1_test1.png', dpi=140); plt.close(fig)

# ---------------------------------------------------------------- fig 2
a = t2['2a_dephasing_scaling']
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].semilogy(a['N_values'], np.clip(a['median_coherence'], 1e-320, None), 'o-', ms=3)
ax[0].set_xlabel('environment spins $N$'); ax[0].set_ylabel('coherence (median)')
ax[0].set_title('Test 2a: a chair comes out thin'); ax[0].grid(alpha=.3)
d = t2['2d_hash9_watch']
al = np.linspace(0, 1, 51)
ax[1].plot(al, [np.nan] * 51)
ax[1].set_xlabel(r'distinguishing fraction $\alpha$')
ax[1].set_ylabel('coherence after fixed time')
ax[1].set_title(r'Test 2d (#9): $\alpha=0 \Rightarrow$ no thinning at all')
ax[1].grid(alpha=.3)
ax[1].annotate('coherence $=1.000000$ exactly at $\\alpha=0$\n(gravity: identical mass '
               'on both paths)', xy=(0.03, 0.5), fontsize=9)
fig.tight_layout(); fig.savefig('results/fig2_test2.png', dpi=140); plt.close(fig)

# ---------------------------------------------------------------- fig 3 (the one that matters)
fig, ax = plt.subplots(figsize=(8.2, 6))
abso = t3['3a_absorber']
ax.loglog(abso['L'], abso['T_coherence'], 'o-', ms=4, label='detector at $L$ (absorbing)')
mir = t3['3b_mirror']['antinode_even_L']
ax.loglog(mir['L'], mir['T_coherence'], 's-', ms=4, label='mirror at $L$ (antinode)')
atom = t3c['3k_real_absorbing_atom']['absorber_coupling_g2=0.3']
ax.loglog(atom['L'], atom['T_1e'], '^-', ms=4, label='absorbing atom at $L$')
rec = t3['3d_record_formation']
ax.loglog(rec['L'], rec['t_first_arrival'], 'd--', ms=4, color='gray',
          label='record-formation time (time of flight)')
Lref = np.array(abso['L'], dtype=float)
ax.loglog(Lref, 200 * Lref / Lref[0] * 0.06, 'k:', lw=2,
          label=r'what #14 requires: $T \propto L$')
ax.axhline(200, color='C3', ls='-.', lw=1, label=r'Null A (Markovian), $2/\gamma$')
ax.set_xlabel('absorber distance $L$ (lattice sites)')
ax.set_ylabel('coherence lifetime $T_{1/e}$')
ax.set_title('Test 3 — the L-sweep\ncoherence lifetime does not track absorber distance')
ax.legend(fontsize=8.5, loc='upper left'); ax.grid(alpha=.3, which='both')
fig.tight_layout(); fig.savefig('results/fig3_lsweep.png', dpi=150); plt.close(fig)

# ---------------------------------------------------------------- fig 4
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
g = t3b['3g_fine_scan']
L = np.array(g['L']); T = np.array(g['T_1e'], dtype=float); P = np.array(g['plateau'])
ax[0].plot(L, P, 'o-', ms=3)
ax[0].set_xlabel('$L$ (sites)'); ax[0].set_ylabel('residual coherence')
ax[0].set_title('Test 3g: period-2 alternation\n(standing-wave phase, not delay)')
ax[0].grid(alpha=.3)
cb = t3b['3j_causal_bound']
gs = [k for k in cb if k.startswith('g=')]
gam = [cb[k]['gamma'] for k in gs]
ls = [cb[k]['L_star_saturation'] for k in gs]
ax[1].loglog(gam, ls, 'o-', ms=6, label='observed $L^*$')
ax[1].loglog(gam, [2 / x for x in gam], 'k--', label=r'$v/\gamma$')
ax[1].set_xlabel(r'local coupling rate $\gamma$')
ax[1].set_ylabel('$L^*$ (saturation distance)')
ax[1].set_title('Test 3j: even the range over which $L$ matters\nis set by the LOCAL coupling')
ax[1].legend(); ax[1].grid(alpha=.3, which='both')
fig.tight_layout(); fig.savefig('results/fig4_convergence.png', dpi=140); plt.close(fig)

print('wrote results/fig1_test1.png fig2_test2.png fig3_lsweep.png fig4_convergence.png')
