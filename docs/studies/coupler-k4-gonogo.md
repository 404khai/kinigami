# cand-a v6 = K4 + K1: go/no-go

Label: **exploratory**. Date: 2026-11-20. Selects nothing (Q38 gates, CPL-011 `unresolved`). Script: `candidates/cand-a/scripts/k4_gonogo.py` (with `jawwin.py`). Nothing here is reviewed.

**Verdict: NO-GO for K4 as laid out.** Check 1 PASS (dry only), check 2 PASS (only with the screw top capped at r 20, which cuts the stroke to 4.97 mm), check 3 **FAIL**.

## 1. Self-locking: PASS (dry, conditional)

Screw (study K4): M2 x 0.4, pitch diameter 2.0 - 0.6495 x 0.4 = 1.740 mm, lead 0.4 mm, lead angle 4.185 deg, **tan = 0.0732** (0.0634 if the 30 deg flank is credited; the stricter value is used).

Cited friction, steel screw with bronze nut ([Wikipedia, Leadscrew](https://en.wikipedia.org/wiki/Leadscrew), accessed 2026-11-20): dry **0.15 to 0.23**, machine oil **0.10 to 0.16**. Statement cited from the same page: self-locking when mu > tan(lead angle), "not absolute"; under vibration or shock the effective mu may fall to dynamic levels. Also [Roton](https://roton.com/screw-university/screw-actions/screw-backdriving-efficiency) (accessed 2026-11-20): mu 0.15 for a screw on a bronze nut, negative backdrive efficiency means self-locking. Steel on steel, greased, static 0.16 ([Engineering ToolBox](https://www.engineeringtoolbox.com/friction-coefficients-d_778.html), accessed 2026-11-20).

| Condition | cited lower bound | margin on 0.0732 |
| --- | --- | --- |
| dry | 0.15 | **2.05x** |
| oiled | 0.10 | 1.37x (below the 1.5x I used; no margin is preregistered) |

Limits: the sources are steel/bronze, not 304/304 (stainless on stainless, 0.5 in air in a search snippet, was not confirmed on the fetched page and galls); the nut material is not declared in v5. The lock needs no minimum load (it is a friction-angle condition), but it needs **vibration-free conditions**: rolling impacts are a shock load, and the declared back-driving loads (tension 1.683 N through the notch wedge, up to 1.683 N axial as an upper bound) are small only if the lock holds. Not shown: that the rolling cell is vibration-free. Needs: a dry-friction test of the chosen pair (UNRESOLVED), and a nut material choice.

## 2. Packing: PASS (conditional, with five changes to v5 parts)

Layout (boxes in the script): the screw runs on the yaw axis (x 0, y -8.2) and **translates**, keyed by the stem; the **nut is the hub of a 17-tooth module 0.2 worm wheel** (x +-1.9, y -10.1..-6.3, z 12.8..14.3) just above the yaw sector; a thrust bridge on the frame base (x -0.5..2.0, y -11.4..-6.2, z 14.32..15.1); worm (module 0.2, pitch r 0.8, lead angle 7.1 deg) on a shaft at x -2.5 supported at its -y end by a frame bearing; a 10 T / 17 T spur stage (y -10.6..-10.1) from M3 at x -5.2, z 13.55, body y -7.0..11.7 (r corner 18.47 <= 19.5). Screw exposed boxes: z 3.0..8.7 (moving group) and z 15.1..19.97 (r 20.00).

Result of the AABB test against all remaining v5 boxes (four-bar parts removed; ring segments skipped, covered by the radial rule): **no overlaps** except the declared mesh, shaft and frame pairs. Arc keep-out (3.2) of every part with y < -7: smallest 4.02 (pinion); the script reproduces the dossier's 3.31 (frame base) and 4.98 (rocker post). Negative control (M3 pushed into the wheel) is flagged.

Changes to remaining v5 parts that this layout needs: yaw shaft OD 2.0 to 3.0 (bore 2.1); sector hub r 1.0 to 1.5; puck column y_min -7.0 to -6.7; **driver-2 relocated and turned** (x -8.0..9.8, y -4.0..6.2, z 6.5..8.3; no v5 position fits); frame base gains a bridge and a bearing. Unverified: the overhung motor shaft (no radial rating, v5 item), the worm shaft has one support, gear width 0.5 mm, thrust support below the wheel, hub wall 0.45 mm.

**K1 pin** (1.5 mm, 10 mm from the peg axis): with a 5 mm pocket (y -14..-9) there is **no free position** at r 8, 10 or 12 (saddle, collar, frame base, cell, tongue). With a 2 mm pocket (end plate only, y -14..-12) free at 0 deg (+z) or 180 deg (-z) for both roll-in directions; the contact then rises from 0.14 MPa (study) to 0.36 MPa (1.07 N over 1.5 x 2 mm, derived).

## 3. Jaw window and seating: FAIL

Computed clearance of the open jaw/tongue to the swept peg (script `jawwin.py`, validated to the dossier and review: 0.448 / 0.089 / 0.052 / 0.000). Required (peg 0.35 toward the part, clearance >= 0.30):

| Part | minimum open stroke S |
| --- | --- |
| jaw | **5.727 mm** |
| tongue | 4.969 mm |

With an open-position chain of +-0.25 (stop 0.1 + three 0.05 class-f terms; my arithmetic, not cited) the nominal stroke is 5.977 and the largest 6.227. Closing onto a peg up to 0.90 low (escape table, loose corner) takes the jaw 1.0 mm below the nominal closed height. The translating screw must stay engaged 1.2 mm (3 pitches) in the nut at z 12.8, so the screw top must reach 12.8 + 1.2 + 1.0 + 6.227 = **21.23 mm against 19.97 allowed by r <= 20: short by 1.26 mm**. Best case (zero tolerance, no travel below nominal) the open jaw just fits (19.73). At the stroke the screw can supply (S_max 4.97, S_min 4.47) the jaw clearance with the peg raised is **0.000** against 0.30. So the open clearance holds at no class-f corner that the packing allows, and the closed jaw cannot reach a low peg. The tongue alone (4.969) passes only if the jaw is ignored, which it cannot be.

## What would be needed

- 1.3 mm more screw length: a nut above z 12.8 is not possible (sector top 12.7); lower the sector and collar by 1.3 mm (saddle, yaw worm and M2 axis move), or let the screw top leave r 20 (a cavity-rule decision for the owner), or shorten the closed travel by registering the peg height.
- Or a rotating screw with a travelling nut: the nut (OD >= 3.2) needs a shaft bore of 3.4 and OD 4.4, which hits M2 (body y >= -6.7, x >= 2.25) and the puck column.
- Or a narrower jaw (the jaw, not the tongue, sets S_min 5.727).
- K1 pocket must be 2 mm, not 5.
- A friction test for the screw pair.
