#!/usr/bin/env bash

. printer-name.sh

lp -d ${PRINTER_NAME} -o page-set=odd chl-booklet.pdf
