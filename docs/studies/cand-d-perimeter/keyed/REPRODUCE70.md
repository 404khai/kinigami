# Reproduce Take 70
Flat, standalone archive. Python 3.10.12, NumPy 2.2.6, SciPy 1.15.3, Linux x86-64. No network, render engine, Git checkout or Gate runner needed. Float formatting, Qhull and BLAS implementations matter for byte equality. Files are relative to the study directory.

    sha256sum -c SHA256SUMS
    sh reproduce-take70.sh
    sha256sum -c SHA256SUMS

To regenerate starting without outputs, copy only the Python sources and shell driver into an empty directory, run the driver there and compare every generated .txt, .json and .scad against the archive hashes. Markdown documents are static. The archived Graft entry is a copy of the uncommitted Graft's report.

Start with shell-take70.md. shell-model70.json is named stock, world mm, encoded [name, convex vertices, Minkowski radius, disk-axis or null for a ball]; some records are intentionally outer envelopes, not material. shell-cell70.json / shell-elec70.json hold the separately routed reservations. shell-cam70.json / shell-bolt70.json / shell-material70.json define cuts, drive, and sleeve material. shell-working70.scad offers editable cut-stock views (worm hob only in the analytical Python model); shell-coupon70.scad is a separate **rejected** alternative coupon, not an installed part. No as-built CAD/BOM.

- Dimensions and stages: basics, face, install, solids.
- Packaging: chosen/cell/electrics, audit, inspect, sphere/yaw/witness, peer, reaction/track. The arc-max solver supersedes the looser isotropic yaw bounds. A negative finite-direction gap on outer solids is inconclusive unless a true common material witness is provided.
- Contact and drive: cam/contact/path, load/worm/material, assembly. The path study preserves the superseded spindle/pin tie clashes. The untouched front-shoulder axle witness uses the new 8.53 mm throw.
- Separate architectures/probes: space/cavity (deep cup rejection); tilt (66/69); probe (72 external only).
- Mass and stability: mass/weigh. Listed-material minimum, typical-motor subtotal, incomplete gross upper and actual as-built unknown are different categories.

Reproduction confirms the frozen numerical study only, not physical validation or qualification. No accepted requirements or criteria modified.
