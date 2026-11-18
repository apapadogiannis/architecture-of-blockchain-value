"""Extension, not in the article: Equation (7) with capabilities of unequal value.
The article's Figure 5 uses the symmetric benchmark, where every capability is worth the same.
Here the total stand-alone value is kept the same (K units for K capabilities) and split unequally:
the largest capability holds a given share and the others share the rest equally. One eta = 0.75
applies to every pair and V0 is the average capability value. The direct term is then K whatever the
split, so the table isolates what unequal values do to the bonus from pairs. The way the total is
split is an illustrative choice. The script also confirms that an equal split returns Equation (14).
Writes ext_unequal_values.csv, the table behind panel 2 of the demo page.
Usage: python3 -I ext_unequal_values.py DATA_DIR OUT_DIR"""
import sys, os, csv
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from blockchain_value import unequal_value, benchmark_value

OUT = sys.argv[2]
ETA = 0.75
rows = 0
with open(f'{OUT}/ext_unequal_values.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['K', 'top_share', 'direct_value', 'pair_bonus', 'V', 'pair_bonus_if_equal'])
    for K in range(2, 21):
        equal = benchmark_value(K, ETA)
        assert abs(unequal_value(K, ETA, 0.0) - equal) < 1e-9
        for share in (0.0, 0.25, 0.5, 0.75, 0.9, 0.95):
            v = unequal_value(K, ETA, share)
            assert v <= equal + 1e-9
            w.writerow([K, f'{share:.2f}', f'{K:.4f}', f'{v - K:.10f}', f'{v:.10f}', f'{equal - K:.10f}']); rows += 1
print(f'{rows} rows written to ext_unequal_values.csv')
