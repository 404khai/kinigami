#!/bin/sh
set -eu
cd "$(dirname "$0")"
here=$(pwd)
temp=$(mktemp -d)
trap 'rm -rf "$temp"' EXIT INT TERM
cp ./*.py "$temp/"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 LC_ALL=C PYTHONDONTWRITEBYTECODE=1
cd "$temp"
for name in geo retention cones hertz pull band ceiling toe pressure exit lock; do
 python3 "${name}83.py" > "${name}83.json"
 cmp "${name}83.json" "$here/${name}83.json"
done
python3 verify83.py
cd "$here"
sha256sum -c SHA256SUMS
