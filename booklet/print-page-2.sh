#!/usr/bin/env bash

echo "Put the sheet flipped, so that you do not print over the printed material, but make what was top top again!"
read

. printer-name.sh

lp -d ${PRINTER_NAME} -o page-set=even chl-booklet.pdf
