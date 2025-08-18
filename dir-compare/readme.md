# dir-compare.py

In-depth directory comparison.

## Reasoning

At one point of time it was easier for me to write this script than to search if
there is such a tool available already.

## Usage

```bash
python dir-compare.py -s <dir1> -t <dir2> [-c sm] [-e true/false]
```

The `-s` and `-t` options are required, being the "source" and "target"
directories to compare. As we don't do any merge/move operations, the order of
these directories does not matter.

The `-c` option allows you to specify the comparison mode:

- `s`: compare file sizes
- `m`: compare file modification times It is a "flag" option, meaning that you
  can combine them, e.g. `-c sm` will compare both file sizes and modification
  times.

The `-e` option allows you to specify whether to show equal files or not in the
final report. The default value is false, meaning that only files that differ
will be shown.
