# Temporary pressure transfer — exploratory, not a candidate

Can a local vacuum hold the six pose-defining contacts while the mechanical latch retracts? **Conditionally yes for the calculated interval; not indefinitely, and not after a sudden vent.** In particular, a pressure switch cannot recover the unsupported tension at the instant the aligned T-bar clears its shoulder. These are design screens under Q85/Q100, not observations of hardware and not reviews.

| Study | Calculated case | What prevents a handoff |
| --- | --- | --- |
| [Area sensitivity](annulus.py) | 60 g, R9.25 seats, R12.75/R5.90 seal, 85 kPa: 0.44 N minimum solved seat reaction | Assumes bounds on effective area, pressure field and seal wrench; no hardware guarantee. |
| [Take 20: one local evacuation stroke](vacuum-take20.md) | Distinct R9.50 face and R13.30/R5.80 seal; 324 mm³ dead volume, 2.49 cm³ swept. The 87 s drive cycle needs leakage below 0.068 reference cm³/min at 98 kPa ambient. | Return shaft intersects the retained joint motor. An indefinitely stalled, exposed bar can outlast the hold interval. |
| [Take 21: floating latch](vacuum-fork.md) | R9.25 face, 60 g. Twelve force-transfer steps avoid assuming two simultaneous full preloads. The single clocking key changes the one-foot reaction bound. | Sudden venting with the bar aligned leaves even 2.354 N axial tension unsupported. The 3.15 mm withdrawal is not yet a swept package. |

Run from here with Python 3 and NumPy: `python3 -B annulus.py`, `python3 -B vacuum-fork.py`, `python3 -B vacuum-take20.py`. The two Grafts used different geometry, allowable seal wrenches and timing. No margins may be combined across their rows. Do not use vacuum as passive structural retention or infer that the 60 mm envelope is infeasible.
