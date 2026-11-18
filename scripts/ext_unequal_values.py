"""Extension, not in the article: Equation (7) with capabilities of unequal value.
The article's Figure 5 uses the symmetric benchmark, where every capability is worth the same.
Here the k-th capability is worth k^(-s) of the largest, for s = 0 (equal, the benchmark), 0.5 and 1,
with the same complementarities as Figure 5 (eta = 0.5 multi, 0.75 meta) and the normalization
V0 = value of the largest capability. Both the shape and the normalization are illustrative choices.
The script also confirms that s = 0 returns Equation (14).
Writes ext_unequal_values.csv, the table behind the "how unequal" control of the demo page.
Usage: python3 -I ext_unequal_values.py DATA_DIR OUT_DIR"""
import sys, os, csv
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from blockchain_value import unequal_value, effective_capabilities, benchmark_value

OUT = sys.argv[2]
with open(f'{OUT}/ext_unequal_values.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['s', 'K', 'effective_capabilities', 'V_multi_eta_0.5', 'V_meta_eta_0.75'])
    for s in (0.0, 0.5, 1.0):
        for K in range(1, 51):
            multi, meta = unequal_value(K, 0.5, s), unequal_value(K, 0.75, s)
            if s == 0.0:
                assert abs(multi - benchmark_value(K, 0.5)) < 1e-9 and abs(meta - benchmark_value(K, 0.75)) < 1e-9
            w.writerow([f'{s:.1f}', K, f'{effective_capabilities(K, s):.6f}', f'{multi:.6f}', f'{meta:.6f}'])
print('150 rows written to ext_unequal_values.csv')
