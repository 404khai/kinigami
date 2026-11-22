# Take 67 / offset-quill

The archive is flat. Preserve the historical layouts and their logs; do not mix them into the final installation. Python 3.10, NumPy 2.2.6, SciPy 1.15.3; no network required.

    sha256sum -c SHA256SUMS
    sh reproduce-take67.sh
    sha256sum -c SHA256SUMS

Read quill-take67.md. Editable finite solids are [name, convex hull vertices in world mm, Minkowski radius, disk axis or null for a ball]. Distinguish outer envelopes from inner contact witnesses. quill-model67.json enumerates the actual listed assemblies; quill-cell67.json and quill-elec67.json carry the folded cell and complete electronic reservations. quill-cam67.json + quill-bolt67.json specify the actual cuts. quill-working67.scad is an optional high-resolution editable track/dog/link/worm view, not a fabrication or assembly model. The Python check does not require an OpenSCAD renderer.

quill-history67.py regenerates the two prior geometry failures. quill-first67.txt and quill-pretrim67.txt are historical captured logs, retained unchanged. quill-history67.txt is the reproducible targeted reevaluation. Upper-bound overlapping mass allowances and density assumptions are in quill-mass67.py; no whole as-built mass or official result.
