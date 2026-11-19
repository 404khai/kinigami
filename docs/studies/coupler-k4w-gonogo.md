# cand-a v6 K4w (wedge-driven jaw): go/no-go

Label: **exploratory**. Date: 2026-11-20. Selects nothing. Script `candidates/cand-a/scripts/k4w_gonogo.py` (reuses the validated `jawwin.py` and `k4_gonogo.py`). Follows `coupler-k4-gonogo.md` and Q84.

**Verdict: NO-GO.** Check 1 PASS only on paper, check 2 FAIL, check 3 FAIL (1.98 mm short), check 4 closing PASS and release blocked.

Variant: M2 x 0.4 screw on the M3 axis (x -4.5, z 12.272) along y, y -11.6..-6.7; nut 1.6 long, so nut travel **3.30 mm**; an inclined slot in a wedge plate on the nut moves a follower pin on the yaw axis (rod through the hollow shaft, as in v5), which moves jaw and tongue.

## 1. Jaw window: PASS on paper (depends on check 3)
Required open stroke for 0.30 mm clearance with the peg 0.35 toward the part (validated sweep): jaw 5.727, tongue 4.969. With the K4 study's open-chain tolerance of +-0.25 mm (my arithmetic, not cited) S_max is 6.227. Seating a peg 0.90 mm low needs 1.0 mm of closed travel (escape table, loose corner). Follower travel **7.227 mm**. The stroke is a design choice here, so the clearance is 0.300 by construction and the closed jaw reaches any stack corner. The wedge angle is atan(7.227 / 3.30) = **65.5 deg**. The wedge does not shorten the follower travel; it only trades y length for force.

## 2. Self-locking: FAIL as asked
- The wedge cannot hold the jaw: it would need mu > tan 65.5 deg = 2.19; the highest cited value is 0.8 (steel on steel, dry, static; [Engineering ToolBox](https://www.engineeringtoolbox.com/friction-coefficients-d_778.html), accessed 2026-11-20; dry kinetic 0.42, greased static 0.16 from the same page).
- At 65.5 deg closing jams when mu_wedge >= cot(alpha) = **0.457**. Dry static 0.5 to 0.8 jams; dry kinetic 0.42 gives a negative net force (-0.389 per axial N with guide friction equal). Only a greased wedge and guide (0.16, 2.9x below the jam limit) closes. No cited lower or upper bound for a greased stainless pair over life.
- The screw alone holds: dry lower bound 0.15 is 2.05x tan(lambda) 0.0732; oiled 0.10 is 1.37x ([Wikipedia, Leadscrew](https://en.wikipedia.org/wiki/Leadscrew), accessed 2026-11-20), vibration-sensitive (same source). A jaw load F back-drives the screw with 1.50 F axial (greased wedge); that is a load on the lock, not a threshold, but it needs vibration-free conditions.

## 3. Packing: FAIL
- Follower slot needs plate height 7.227 + 0.8 pin + 2 x 0.6 wall = **9.23 mm** (my sizing); plate envelope over the nut travel y -12.50..-3.90 (violates |y| <= 12 by 0.50 mm).
- Largest free vertical window on the yaw axis (x +-1; remaining v5 boxes, four-bar and rod removed; r <= 20; arc keep-out): **5.60 mm** (z 14.35..19.95), or 7.25 mm (z 12.7..19.95) if the plate stays 0.6 mm clear of the frame base. Best shortfall **1.98 mm**. The r <= 20 limit still binds: the follower travel equals the jaw travel.
- Screw, nut and arm on the M3 axis do not overlap the v5 boxes; the failure is the plate window. A low follower (z < 12.7) has no window (shaft, collar, sector, puck, tongue, jaw).
- K1 pin: pocket 5 mm (y -14..-9): **no free position** at r 8, 10 or 12; pocket 2 mm: free at 0 or 180 deg, stress 0.35 MPa (derived from the study's 0.14 MPa at 5 mm), not the declared 0.14.

## 4. Forces: closing PASS, release blocked
Greased wedge and guide (0.16): net vertical force 0.1164 per axial N. Rated 3 mN m gives 8.67 N axial (study factor 0.346 mN m/N), jaw force **1.01 N against 0.4208 N required: 2.4x**. Dry: jammed. Release at the mu = 1 bound (rod force 3.366 N, dossier v5): axial 28.9 N, **10.0 mN m = 3.33x rated, 1.11x stall**: blocked, as v5 (1.07x). Release rule T <= 0.505 N at rated (v5: 0.5225 N). The wedge angle removes the K4 release gain.

## What would be needed
About 2 mm more vertical room on the yaw axis (lower the sector and collar, or accept r > 20), a shorter follower travel, a 5 mm K1 pocket position, and a lubricated wedge pair with a cited friction range. None is available inside the declared v5 boxes.
