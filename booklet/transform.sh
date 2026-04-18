#!/usr/bin/env bash
set -euo pipefail

IN=${1:-./checklist.pdf}
OUT=${2:-./chl-booklet.pdf}

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# Rotate the pages that must appear upside-down in the lower row of each side.
qpdf --rotate=+180:3,4,5,6 "$IN" "$TMP/rot.pdf"

# Side A (outer): P2 P7 / P3' P6'
pdfjam "$TMP/rot.pdf" '2,7,3,6' --nup 2x2 --no-landscape \
       --paper a4paper --outfile "$TMP/front.pdf"

# Side B (inner): P8 P1 / P5' P4'
pdfjam "$TMP/rot.pdf" '8,1,5,4' --nup 2x2 --no-landscape \
       --paper a4paper --outfile "$TMP/back.pdf"

pdfunite "$TMP/front.pdf" "$TMP/back.pdf" "$OUT"
