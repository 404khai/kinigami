#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0
for n in chosen electrics install cam; do
 out=$n; [ "$n" != electrics ] || out=elec
 python3 -B "shell-${n}70.py" > "shell-${out}70.txt"
done
# Independent analytical screens; no geometry generation races here.
pids=""
for group in 'cavity material worm' 'weigh space reaction' 'contact assembly load' 'yaw sphere witness' 'audit peer probe track path' 'tilt' 'inspect'; do
 (
  for n in $group; do python3 -B "shell-${n}70.py" > "shell-${n}70.txt"; done
 ) &
 pids="$pids $!"
done
for p in $pids; do wait "$p" || exit 1; done
