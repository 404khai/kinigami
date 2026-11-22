#!/bin/sh
set -eu
cd "$(dirname "$0")"
export LC_ALL=C OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
for n in key79 hold79 latch79 package79 rating79 detail79 containment79 path79 tilt79 service79 ledger79 view79; do
  python3 -B "$n.py" > "$n.txt"
done
