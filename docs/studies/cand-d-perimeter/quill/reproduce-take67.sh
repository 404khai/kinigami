#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0 LC_ALL=C
for n in install history audit contact cell electrics cam scad worm load mass inspect assembly tilt space; do
 out=$n; [ "$n" != electrics ] || out=elec
 python3 -B "quill-${n}67.py" > "quill-${out}67.txt"
done
