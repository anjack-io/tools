#!/usr/bin/env bash

. printer-name.sh

lp -d ${PRINTER_NAME} -P 1 chl-booklet.pdf
