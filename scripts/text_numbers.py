"""Numbers and identities stated in the text of Section 3.
1. Footnote 2: two capabilities worth 100 each, eta = 0.3 and V0 = 100 give an interaction
   contribution of 30.
2. Equation (14) against Equation (7): the closed form equals the general sum over capabilities and
   pairs under the symmetric benchmark (full adoption, common phi and N, V0 = phi u N).
3. Limiting dominance (Proposition) and Benchmark 1, Equations (11) to (13).
4. Corollary: V_meta / V_multi tends to (eta_meta / eta_multi) lambda^2 as K grows.
Writes text_numbers.csv.
Usage: python3 -I text_numbers.py DATA_DIR OUT_DIR"""
import sys, os, csv
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from blockchain_value import Capability, network_value, benchmark_value, complementarity_share

OUT = sys.argv[2]
rows = []

# 1. Footnote 2
caps = [Capability('f', phi=100.0), Capability('g', phi=100.0)]
total = network_value(caps, u=1.0, eta=0.3, V0=100.0)
rows.append(('footnote2_interaction_contribution', 'Footnote 2', f'{total - 200.0:.4f}'))
rows.append(('footnote2_total_value', 'Footnote 2', f'{total:.4f}'))

# 2. Equation (14) equals Equation (7) under the symmetric benchmark
PHI, U, NU = 2.0, 3.0, 5.0     # arbitrary positive values, to show the identity is not special to 1
for label, eta in (('multi', 0.5), ('meta', 0.75)):
    for K in (2, 10, 50):
        caps = [Capability(f'c{i}', phi=PHI, N=lambda u_f: NU) for i in range(K)]
        general = network_value(caps, u=U, eta=eta, V0=PHI * U * NU)
        closed = benchmark_value(K, eta, phi=PHI, u=U, N=NU)
        rows.append((f'eq7_general_{label}_K{K}', 'Equation (7)', f'{general:.4f}'))
        rows.append((f'eq14_closed_form_{label}_K{K}', 'Equation (14)', f'{closed:.4f}'))
        assert abs(general - closed) <= 1e-9 * closed

# 3. Figure 5 end points, Benchmark 1 and dominance
v_single, v_multi, v_meta = benchmark_value(1), benchmark_value(50, 0.5), benchmark_value(50, 0.75)
rows.append(('fig5_V_single', 'Figure 5, Equation (15)', f'{v_single:.4f}'))
rows.append(('fig5_V_multi_K50', 'Figure 5, Equation (18)', f'{v_multi:.4f}'))
rows.append(('fig5_V_meta_K50', 'Figure 5, Equation (19)', f'{v_meta:.4f}'))
rows.append(('fig5_share_from_complementarity_multi_K50', 'Equation (14)', f'{complementarity_share(50, 0.5):.6f}'))
rows.append(('fig5_share_from_complementarity_meta_K50', 'Equation (14)', f'{complementarity_share(50, 0.75):.6f}'))
rows.append(('benchmark1_V_K50_eta0', 'Equations (12), (13)', f'{benchmark_value(50, 0.0):.4f}'))
assert v_meta > v_multi > v_single

# 4. Corollary: limiting ratio
for K in (50, 1000, 100000):
    ratio = benchmark_value(K, 0.75) / benchmark_value(K, 0.5)
    rows.append((f'corollary_ratio_meta_to_multi_K{K}_lambda1', 'Corollary', f'{ratio:.6f}'))
ratio2 = benchmark_value(200000, 0.75) / benchmark_value(100000, 0.5)
rows.append(('corollary_ratio_meta_to_multi_K100000_lambda2', 'Corollary', f'{ratio2:.6f}'))
rows.append(('corollary_limit_lambda1', 'Corollary', f'{0.75 / 0.5:.6f}'))
rows.append(('corollary_limit_lambda2', 'Corollary', f'{0.75 / 0.5 * 4:.6f}'))

with open(f'{OUT}/text_numbers.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['quantity', 'where', 'value'])
    w.writerows(rows)
print(f'{len(rows)} numbers written to text_numbers.csv')
