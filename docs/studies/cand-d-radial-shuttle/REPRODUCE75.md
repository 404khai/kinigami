# Reproduce Take 75

Label: exploratory. All units mm, N, N·mm, g unless stated. The JSON reference is an input, not an output. It contains the registered tail, yaw/feet and electronics reservations from the frozen Take 70 archive (SHA-256 5e45ce1fa0ff5a0773a030643bb44ac2475e67cece4d0ffcbfc2fb28cb47ff8c). No old jaw mechanism is loaded.

Use Python 3.10.12, NumPy 2.2.6 and SciPy 1.15.3 on x86-64 Linux. For exact replay, copy only the top-level Python sources, reference75.json and reproduce75.sh to a new directory; run the shell script there. Compare the ten stdout captures, installed75.json and both SCAD files with the reference outputs. SHA256SUMS covers the frozen deliverable apart from itself; run sha256sum -c SHA256SUMS in the extracted archive. No network or repo checkout is needed. SCAD is for inspection; no physical or CAD-kernel validation is implied.

- plug75: solid profile datum, continuous guide/carrier sweep, exact local displacement.
- carrier75: installed stock, four gearmotor reserves and independent terminal drive.
- lock75/load75: tooth-material/dog registration and transparent load hypotheses.
- verify75/covers75: 3D support gaps, LP witnesses, containment and peer yaw. Swept blanks and negative projection gaps alone are not interference witnesses.
- assembly75/cut75: assembly paths, actual single-displacement veto, optional external bore probes and editable sections.
- mass75: separate disjoint-component lower and listed component upper screens; not as-built mass.
- shellwall75: true ring-versus-cover material ball and same-pose extraction load.
- space75: convex primitives and finite-solid support/LP routines. reference75.json is the only input data file.
