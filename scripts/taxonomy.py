"""The three paradigms described along the five pillars, as one machine-readable file.
Reads the transcriptions of Tables 2 to 6 in DATA_DIR and writes paradigms.json: for each paradigm
(single-, multi-, meta-capability) its entry under purpose, consensus, incentives, tokenomics and
network effects, with the table each entry comes from.
Usage: python3 -I taxonomy.py DATA_DIR OUT_DIR"""
import sys, csv, json

DATA, OUT = sys.argv[1], sys.argv[2]
TABLES = [('purpose', 'table2_purpose.csv', 'Table 2'),
          ('consensus', 'table3_consensus.csv', 'Table 3'),
          ('incentives', 'table4_incentives.csv', 'Table 4'),
          ('tokenomics', 'table5_coins_tokens.csv', 'Table 5'),
          ('network_effects', 'table6_network_effects.csv', 'Table 6')]
ORDER = ['Single-capability', 'Multi-capability', 'Meta-capability']

paradigms = {p: {} for p in ORDER}
for pillar, name, table in TABLES:
    with open(f'{DATA}/{name}', newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            entry = {k.lower().replace(' ', '_'): v for k, v in row.items() if k != 'Paradigm'}
            entry['source'] = table
            paradigms[row['Paradigm']][pillar] = entry
assert all(len(v) == len(TABLES) for v in paradigms.values())

with open(f'{OUT}/paradigms.json', 'w', encoding='utf-8') as f:
    json.dump({'pillars': [t[0] for t in TABLES], 'paradigms': paradigms}, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('paradigms.json written: 3 paradigms x 5 pillars')
