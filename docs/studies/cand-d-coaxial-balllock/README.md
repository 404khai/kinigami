# Take 80 — Coaxial axial-sleeve tri-roller coupler (exploratory screen)

Exploratory screening study only. No Gate 1 evidence, no candidate promotion, no change to Q12, Q85, Q100, or `gate1-v1`.

## Motivation

Takes 75 (Ø60.90 mm) and 79 (Ø62.11 mm) both exceeded the 60 mm envelope because radial-stroke locking mechanisms stack a large barrel (~Ø30 mm) plus radial stroke (~5 mm) plus external guide bands (~5–10 mm) outside the bore. Take 78 also showed that a narrow R4.10 central ram can be bypassed laterally.

This study screens a coaxial axial-sleeve tri-roller coupler inside an Ø21.8 mm barrel (8.3 mm smaller diameter than Takes 74–79, with zero external radial guide tower):

- **6 fixed V-seat flats** on the housing front (`x = 0`) engaging 3 tail registry balls (`R = 1.50 mm`, circle `r = 8.20 mm` at `-90°, 30°, 150°`, V half-angle `65°`).
- **3 hardened-steel cylindrical rollers** (`Ø3.0 × 3.0 mm`) at `0°, 120°, 240°` in a captive cage at `x = -4.20 mm`, bearing on tri-flat `45°` shoulders of the central tail pin (`R_neck = 3.20 mm`, `R_head = 4.60 mm`) and tri-flat `0°` internal lands of an axially sliding locking sleeve (`R_lock = 6.4307 mm`, `R_unlock = 7.95 mm`, `OD = 19.2 mm`, barrel `OD = 21.8 mm`).
- **360° coaxial annular ejector** pushing directly on the tail flange to prevent narrow-ram lateral bypass.

## Deterministic screen results (`sleeve.py`)

Run with `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B docs/studies/cand-d-coaxial-balllock/sleeve.py`:

- **70 g provisional 6-DOF retention (all 128 corners per box, no equal load sharing):**
  - Minimum all-seated axial draw: **9.642 N** (service), **11.554 N** (fault), **27.289 N** (table).
  - Under a **45.0 N** force-limited axial draw cap: worst single-roller normal **59.079 N** (table) / **47.827 N** (service); worst single-seat normal **75.515 N** (table) / **45.672 N** (service).
- **Line-contact Hertzian stress (`Ø3.0 × 3.0 mm` steel rollers on flat steel):**
  - **694.4 MPa** on the tail 45° flat (contact half-width `0.0181 mm`), **647.6 MPa** on the sleeve 0° flat.
- **Loaded axial-sleeve unlock and M3 × 0.5 mm leadscrew (`μ = 0.23`):**
  - Worst total radial load on sleeve: **55.35 N**; axial unlock force **12.731 N** nominal (**19.096 N** with `1.5×` eccentric drag factor).
  - M3 × 0.5 mm leadscrew torque (with `r_c = 2.0 mm` thrust collar): **16.291 N·mm** unlock, **29.86 N·mm** at 35 N ejection, **46.07 N·mm** at 54 N draw (needs a ~2:1 spur stage on `0615N003S + 256:1` or thrust bearing).
  - Screw lead angle **3.40°** vs friction angle **12.95°** at `μ = 0.23` (still `< 4.57°` even at `μ = 0.08`).
- **Nonlinear finite-flat form closure (9 unilateral contacts, `0.025 mm` seat / `0.040 mm` roller recess, `0.60°/1.00°` normal tilt):**
  - 27 feasible vertices, max translation **0.116 mm**, max rotation **0.808°** (`+0.392°` margin to `1.20°`), max seat/roller center displacement **0.158 / 0.1258 mm** (`+0.092 mm` margin to `0.250 mm`).
- **First-order envelope screen:**
  - `Ø21.8 mm` barrel OD leaves `+1.8 mm` Y and `+1.1 mm` Z radial margin inside a `48.0 × 25.4 × 24.0 mm` box (`Ø59.373 mm`).

## What this does NOT prove

- Does not prove roller-in-cage cocking/wedging resistance under loaded unlock or compression.
- Does not prove off-axis annular ejection clears the unlocked rollers and front lip without tilt-jam.
- Does not prove finite land geometry, chamfer-edge contact stress, driven take-up sequencing, installed drives, battery/controller/joint layout inside Ø60 mm, or as-built mass.
- Assigned to Take 81 (mechanics) and Take 82 (packaging) for independent scrutiny.
