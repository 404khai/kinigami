#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0
D=$(mktemp -d)
trap 'rm -rf "$D"' EXIT
for f in lands roller bearing wedge travel catch takeup edge; do
    python3 -B "$f.py" > "$D/$f.json"
    cmp "$D/$f.json" "$f.json"
done
printf 'Eight outputs match.\n'
