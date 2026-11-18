# The architecture of blockchain value: capabilities, pillars, and growth dynamics

[![Article](https://img.shields.io/badge/Frontiers-10.3389%2Ffbloc.2026.1747512-1f4e79)](https://doi.org/10.3389/fbloc.2026.1747512)
[![SSRN](https://img.shields.io/badge/SSRN-10.2139%2Fssrn.6196338-1f4e79)](https://doi.org/10.2139/ssrn.6196338)
[![replication](https://github.com/apapadogiannis/architecture-of-blockchain-value/actions/workflows/replicate.yml/badge.svg)](https://github.com/apapadogiannis/architecture-of-blockchain-value/actions/workflows/replicate.yml)

Replication package for the paper by Agisilaos Papadogiannis, published in *Frontiers in Blockchain* 9:1747512 (2026).
Paper: `paper/fbloc-9-1747512.pdf` (published version, open access); journal page: [doi:10.3389/fbloc.2026.1747512](https://doi.org/10.3389/fbloc.2026.1747512); preprint on SSRN: [doi:10.2139/ssrn.6196338](https://doi.org/10.2139/ssrn.6196338).
Interactive demo: [apapadogiannis.github.io/architecture-of-blockchain-value](https://apapadogiannis.github.io/architecture-of-blockchain-value/).

## What this is

The paper is a theory paper. It asks what a blockchain can deliver (its *capabilities*) and how
five architectural pillars (purpose, consensus, incentives, tokenomics, network effects) decide
which capabilities are feasible:

1. **Three paradigms.** Single-capability networks deliver one service, multi-capability networks a
   bounded set of programmable services, and meta-capability networks an open-ended market of
   services.
2. **Value grows with capabilities and with the pairs they form.** With *K* capabilities and a
   complementarity *η* between every pair, value is *V* = *φ u N*(*u*) [*K* + *η K*(*K* − 1)/2]
   (Equation 14): linear in *K* without complementarities, quadratic with them.
3. **Network effects set how value grows with users.** Sarnoff (*u*), Metcalfe (*u*²) and Reed
   (2^*u*) scaling give very different paths, and the paradigms differ in which one dominates.

The paper estimates nothing and uses no dataset. This package holds the model as code, the scripts
that produce Figures 5 and 8 and the numbers stated in Section 3, the paradigm tables in
machine-readable form, and a small interactive page.

## Interactive demo

`docs/index.html` is a single page with no dependencies. It lets the reader move *K*, *η* and the
number of users and watch Equation (14) and the three scaling laws respond. With the default
settings its first chart is Figure 5. Open the file in a browser, or use the link above.

One panel goes beyond the published figures. Figure 5 uses the symmetric benchmark, in which every
capability is worth the same. Panel 2 of the demo keeps the total stand-alone value fixed and splits
it unequally, using the paper's general formula, Equation (7). The stand-alone term does not change;
the bonus from pairs shrinks, because the bonus of a pair is proportional to the product of the two
values and a product is largest when they are equal. With 10 capabilities and *η* = 0.75 the network
is worth 43.75 with an equal split, 37.08 when one capability holds half of the value and 17.08 when
it holds 90%. The paper states the condition in words (Section 3.3: the dominance results rely on
symmetric benchmark assumptions). Splitting the value as one large capability and equal others is an
illustrative choice of this package, not a result of the paper.

## Using the model

```python
from blockchain_value import benchmark_value, unequal_value, network_value, Capability, scaling_law

benchmark_value(K=50, eta=0.75)        # Equation (14), normalized: 968.75
unequal_value(K=10, eta=0.75, top_share=0.5)   # Equation (7), same total split unequally (not in the paper): 37.08
scaling_law("reed", 10)                # 2**10 = 1024.0

# Equation (7) in general form: capabilities that differ in value, adoption and network effect
caps = [Capability("transfer", phi=100.0), Capability("contracts", phi=100.0)]
network_value(caps, u=1.0, eta=0.3, V0=100.0)   # 230.0, the example of footnote 2
```

`blockchain_value.py` uses the standard library only. Each function names the equation it implements.

## Layout

```
blockchain_value.py   the valuation model (Equations 5 to 19 and the scaling laws)
scripts/    one script per figure or calculation (see below)
outputs/    the tables behind the figures, the numbers stated in the text, the taxonomy (CSV, JSON)
figures/    Figures 5 and 8 (PNG and PDF)
data/       Tables 2 to 6 of the paper as CSV (see Data and licensing)
docs/       the interactive demo page
paper/      the published article (PDF)
```

## Reproducing

Requirements: Python 3.11+, `pip install -r requirements.txt` (numpy, matplotlib).
`requirements-lock.txt` lists the exact versions under which `outputs/` were generated.

```bash
./run_all.sh    # runs every script below in order, a few seconds
```

The scripts are deterministic; re-running them reproduces `outputs/` and `figures/`.
A GitHub Actions workflow re-runs the full pipeline on every push and monthly, and fails if
any stored result is not reproduced (see "How the check works"); the badge above shows the latest run.
Each takes `python3 -I <script>.py DATA_DIR OUT_DIR`.

| Script | What it produces | Where it appears |
|---|---|---|
| `text_numbers.py` | The worked example of footnote 2; Equation (14) checked against the general sum of Equation (7); the limiting ratio of the Corollary; `text_numbers.csv` | Section 3 |
| `taxonomy.py` | The three paradigms described along the five pillars; `paradigms.json` | Tables 2 to 6 |
| `fig5_capability_scaling.py` | Normalized value against the number of capabilities, *K* = 1 to 50, *η* = 0.5 and 0.75 (stylized values); `fig5_capability_scaling.csv` | Figure 5, Equations (15), (18), (19) |
| `ext_unequal_values.py` | Equation (7) with the same total value split unequally among 2 to 20 capabilities; `ext_unequal_values.csv` | Not in the paper: the table behind panel 2 of the demo (see above) |
| `fig8_scaling_laws.py` | Sarnoff, Metcalfe and Reed scaling for 1 to 20 users; `fig8_scaling_laws.csv` | Figure 8 |

Figures 1 to 4, 6 and 7 are diagrams without numerical content and are not redrawn here; they are in the paper.

## How the check works

```bash
python3 check_outputs.py    # reruns ./run_all.sh, then compares
```

1. The result tables in `outputs/` are stored in this repository exactly as they were when the
   figures were drawn from them.
2. `check_outputs.py` sets the stored copies aside, reruns `./run_all.sh` on the files in `data/`,
   and compares the fresh files with the stored ones, number by number.
3. A number counts as reproduced if it agrees with the stored one to nine significant digits
   (relative tolerance 1e-9). Text, labels and whole numbers must match exactly. Any other
   difference is listed and the check fails.

Why a tolerance and not a character-by-character match: the last digits of a floating-point
result depend on the processor and on the build of the numerical libraries, so two correct runs
on different machines can differ in the 12th to 16th significant digit. The check reports
how many numbers differed in this way and by how much. For the same reason, a value printed with
a fixed number of decimals may differ by one unit in its last printed place; such cases are listed.

The workflow behind the badge runs the pipeline on a new machine with the pinned package
versions, on every push and once a month, and applies the same comparison. It also runs
`node scripts/check_demo.mjs`, which takes the model code out of the demo page and compares its
numbers with the stored tables, so the page and the Python module cannot drift apart.

Two limits. The comparison is between regenerated and stored results, not with the paper's
PDF: to connect the two, use the script table above, which says where each output appears in
the paper. And figures are redrawn from the same values but are not compared, because image files can
differ slightly between versions of the plotting library.

## Data and licensing

- The paper uses no dataset. The files in `data/` are Tables 2 to 6 of the paper, transcribed by
  hand, one file per table: `table2_purpose.csv`, `table3_consensus.csv`, `table4_incentives.csv`,
  `table5_coins_tokens.csv`, `table6_network_effects.csv`.
- The values *η* = 0.5 and *η* = 0.75 are stylized parameters chosen in the paper for illustration.
  They are not estimates.
- Code: MIT License. Output tables and figures (`outputs/`, `figures/`) and the demo page: CC BY 4.0, cite the paper.
- Paper (`paper/`) and the tables transcribed from it (`data/`): CC BY, the license of *Frontiers in Blockchain*. © 2026 Papadogiannis.

## Citation

> Papadogiannis, A. (2026). "The architecture of blockchain value: capabilities, pillars, and growth dynamics." *Frontiers in Blockchain* 9:1747512.
> https://doi.org/10.3389/fbloc.2026.1747512
> SSRN: https://doi.org/10.2139/ssrn.6196338

## Disclaimer

Independent research; no funding, no institutional position. Not investment advice.
