#!/usr/bin/env bash
# Compiles the six diagrams (Figures 1 to 4, 6 and 7) from their TikZ sources and writes
# PDF, PNG and SVG files to figures/. Needs pdflatex (with TikZ) and pdftocairo (poppler).
# Not part of run_all.sh: the diagrams contain no numbers, so the replication check does not need them.
set -e
cd "$(dirname "$0")"
tmp=$(mktemp -d)
for f in fig*.tex; do
  n="${f%.tex}"
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$tmp" "$f" >/dev/null
  cp "$tmp/$n.pdf" "../$n.pdf"
  pdftocairo -png -r 200 -singlefile "$tmp/$n.pdf" "../$n"
  pdftocairo -svg "$tmp/$n.pdf" "../$n.svg"
  echo "== $n"
done
rm -rf "$tmp"
