"""Figure 5: normalized value V(u) against the number of capabilities K, for K = 1 to 50.
Equations (18) and (19), which are Equation (14) with phi = 1 and N(u) = 1 (the user base u is set
to 1 as well, so that the value is normalized): V = K + eta K (K - 1) / 2, with eta = 0.5 for the
multi-capability paradigm and eta = 0.75 for the meta-capability paradigm (stylized values). The
single-capability paradigm has K = 1 and stays at V = 1, Equation (15).
Writes the plotted series and the figure.
Usage: python3 -I fig5_capability_scaling.py DATA_DIR OUT_DIR"""
import sys, os, csv
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from blockchain_value import benchmark_value

OUT = sys.argv[2]
ETA_MULTI, ETA_META = 0.5, 0.75
K = list(range(1, 51))
single = [benchmark_value(1) for _ in K]
multi = [benchmark_value(k, ETA_MULTI) for k in K]
meta = [benchmark_value(k, ETA_META) for k in K]

with open(f'{OUT}/fig5_capability_scaling.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['K', 'V_single', 'V_multi_eta_0.5', 'V_meta_eta_0.75'])
    for k, s, mu, me in zip(K, single, multi, meta):
        w.writerow([k, f'{s:.4f}', f'{mu:.4f}', f'{me:.4f}'])

plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 12, 'mathtext.fontset': 'dejavuserif'})
fig, ax = plt.subplots(figsize=(7.4, 3.6))
ax.plot(K, meta, color='red', lw=1.4, marker='^', ms=3, label=r'Meta-capability ($\eta = 0.75$)')
ax.plot(K, multi, color='blue', lw=1.4, marker='o', ms=2.5, label=r'Multi-capability ($\eta = 0.5$)')
ax.plot(K, single, color='#006400', lw=1.6, ls='--', marker='s', ms=2, label='Single-capability')
ax.set_xlim(0, 50); ax.set_ylim(0, 1000)
ax.set_xticks(range(5, 51, 5)); ax.set_yticks(range(0, 1001, 200))
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
ax.set_xlabel('Number of capabilities $K$'); ax.set_ylabel('$V(u)$ (normalized)')
ax.grid(True, color='#cccccc', ls='--')
ax.legend(loc='upper left', fontsize=10, frameon=True, edgecolor='black', fancybox=False)
fig.savefig(f'{OUT}/fig5_capability_scaling.png', dpi=220, bbox_inches='tight', metadata={'Software': None})
fig.savefig(f'{OUT}/fig5_capability_scaling.pdf', bbox_inches='tight', metadata={'CreationDate': None, 'Creator': None, 'Producer': None})
print('Figure 5 written; series in fig5_capability_scaling.csv')
