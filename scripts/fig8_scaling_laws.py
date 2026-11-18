"""Figure 8: network value under Sarnoff, Metcalfe and Reed scaling.
V(u) = u, V(u) = u^2 and V(u) = 2^u. Left panel: u from 1 to 20 on a logarithmic axis.
Right panel: u from 1 to 8 on a linear axis.
Writes the three laws at whole numbers of users and the figure.
Usage: python3 -I fig8_scaling_laws.py DATA_DIR OUT_DIR"""
import sys, os, csv
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from blockchain_value import scaling_law

OUT = sys.argv[2]
LAWS = [('sarnoff', 'Sarnoff: $V(u) = u$', 'blue', '-'),
        ('metcalfe', 'Metcalfe: $V(u) = u^2$', 'red', '--'),
        ('reed', 'Reed: $V(u) = 2^u$', 'green', ':')]

with open(f'{OUT}/fig8_scaling_laws.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['u', 'V_sarnoff', 'V_metcalfe', 'V_reed'])
    for u in range(1, 21):
        w.writerow([u] + [int(scaling_law(law, u)) for law, *_ in LAWS])

plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 12, 'mathtext.fontset': 'dejavuserif'})
fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8))
for ax, (lo, hi), title in zip(axes, [(1, 20), (1, 8)], ['Full range (log y-axis)', 'Early-stage region (linear y-axis)']):
    u = np.linspace(lo, hi, 400)
    for law, label, color, ls in LAWS:
        ax.plot(u, [scaling_law(law, x) for x in u], color=color, ls=ls, lw=1.3, label=label)
    ax.set_xlim(lo, hi); ax.set_title(title, fontsize=12)
    ax.set_xlabel('Number of users $u$'); ax.set_ylabel('Network value $V(u)$')
    ax.grid(True, color='#cccccc')
    ax.legend(loc='upper left', fontsize=10, frameon=True, edgecolor='black', fancybox=False)
axes[0].set_yscale('log'); axes[0].set_ylim(1, 1e6); axes[0].set_xticks([5, 10, 15, 20])
axes[1].set_ylim(0, 256); axes[1].set_yticks(range(50, 251, 50)); axes[1].set_xticks(range(1, 9))
fig.tight_layout()
fig.savefig(f'{OUT}/fig8_scaling_laws.png', dpi=220, bbox_inches='tight', metadata={'Software': None})
fig.savefig(f'{OUT}/fig8_scaling_laws.pdf', bbox_inches='tight', metadata={'CreationDate': None, 'Creator': None, 'Producer': None})
print('Figure 8 written; series in fig8_scaling_laws.csv')
