# Reproduce Take 82 (exploratory)
The archive is self-contained. Base: 3cb5a25 on feat/cand-d-coupler-first. No simulator, solver Gate, CAD server, internet call or other session is used in the replay, aside from optional first-time dependency installation.

1. Extract the zip in an empty directory; enter coaxial-module82.
2. Use Linux x86-64, CPython 3.10 with the three exact packages in requirements82.txt; for example install them into a fresh venv with pip. util-linux taskset is used to keep manifold and hull output ordering reproducible.
3. Run `sha256sum -c SHA256SUMS`, then `bash reproduce82.sh`, then check the manifest again. To test regeneration from sources rather than the bundled output, remove only installed82.json, local82.json, sphere82.json, phase-pairs.json, service82.json, mass82.json, rating82.json, neighbor82.json, witness82.json and cutaway82.scad first.
4. See coaxial-take82.md for frame, methods, fit, rejection and limits. Open cutaway82.scad in OpenSCAD to inspect the parked orientation of the whole assembly at the DRAW axial datum, with optional covers, guest and sectional views. This mesh is a view, not the source of the reported collisions.

Inputs: catalog-reserves79.json is the earlier trial's joint, power, controls and feet datum exchange file. Only the joint and electronics are imported into the final layout. upstream80.json is the byte-for-byte Take 80 reference. search82.py is an optional deterministic yaw surrogate search (seed 82); it is not used as clearance evidence or a replay prerequisite. All added dimensions, materials, arrangements, friction, assumed efficiencies and service routes are Take 82 trial assumptions unless a source is identified. The report journal excerpt records this Graft's Take 82 entry.
