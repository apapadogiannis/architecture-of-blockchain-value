#!/usr/bin/env bash
# Reproduces Figures 5 and 8, the numbers stated in Section 3, the taxonomy file and the table behind the demo's extension. Runs in a few seconds.
set -e
cd "$(dirname "$0")/scripts"
mkdir -p ../outputs ../figures
for f in text_numbers taxonomy fig5_capability_scaling fig8_scaling_laws ext_unequal_values; do
  echo "== $f"; python3 -I "$f.py" ../data ../outputs
done
mv -f ../outputs/*.pdf ../outputs/*.png ../figures/
