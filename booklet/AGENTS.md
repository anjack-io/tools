# booklet

Small utility repo for turning an 8-page PDF into a single-sheet, duplex-printable mini-book (zine fold).

## Dev environment

- Nix flake + direnv. `.envrc` uses `use flake`, so the dev shell auto-loads on `cd`.
- Run commands directly (`./transform.sh`, `pdfjam ...`) — do **not** wrap in `nix develop --command`.
- The flake provides a minimal TeX Live combine (`scheme-basic` + `pdfjam` + `pdfpages`) plus `qpdf` and `poppler_utils`. Keep it minimal; do not add `texliveFull` or other heavy deps without discussion.

## Workflow

1. `./transform.sh [input.pdf] [output.pdf]` — defaults to `checklist.pdf` → `chl-booklet.pdf`.
   Imposes an 8-page input onto 2 A4 sheets (2×2 n-up, bottom row rotated 180°) so the result folds into an 8-page booklet.
2. `./print-page-1.sh` — prints odd sheets (side A) on the configured CUPS printer.
3. Flip sheets in the paper tray as instructed, then `./print-page-2.sh` for side B.
4. Cut once across the middle, stack, fold.

Printer name is set in `printer-name.sh` (HP LaserJet M276n); `printer-details.sh` shows `lpstat` info.

## Conventions

- Keep the dependency footprint small — this repo is deliberately a few shell scripts + a flake.
- Don't introduce new tools (Python, Node, etc.) without discussion.
- The output filename `chl-booklet.pdf` is referenced by both `print-page-*.sh` scripts; keep it in sync if renamed.
