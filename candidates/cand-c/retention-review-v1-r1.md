# Retention review: cand-c v1, r1

candidate_id: cand-c
candidate_version: 1
author: agent task-6 (cand-c dossier author)
reviewer: reviewer-c-independent
outcome: unresolved

Review date: 2026-11-05. The reviewer authored no cand-c file. This is a paper review of the declared statements. It is not a test of the mechanism. Rule applied: unsupported retention or alignment claims are `unresolved`, never `pass`.

## Retention (spring_preload, no power)

- **Declared mechanism:** two spring-preloaded jaws in the tail socket close behind the 6 mm steel ball once it passes the throat. Components: `tail-socket-cartridge`, `head-ball-stud`. `requires_power_to_hold` is false.
- **Physical principle (accepted in kind):** a ball seated behind a sprung jaw throat is a detent. Separation needs the ball to push the jaws apart against the spring preload, so the holding force exists with no energy supply. The principle is sound and common.
- **Governing geometry and forces: not supported.** The dossier (section 7) says retention force "depends on spring rate, preload and jaw geometry, none of which is designed". Jaw geometry, throat width, spring rate, preload and the retention force are all absent. The only declared dimensions are the ball (6 mm diameter) and a socket box (cylinder of radius 4.5 mm and half height 3 mm), and the box does not show a throat or jaws. No reasoning is given that the force exceeds any load (for example the 0.07 N rolling thrust or the weight of a neighbour). A detent with no force value cannot be judged to hold.
- **Orientations:** the joint has three rotational degrees of freedom and holds only against separation. Retention of orientation (shape) is explicitly not claimed by the dossier. The reviewer accepts that statement. No orientation is held by this mechanism.
- **Unpowered stability against pull-out:** unsupported for the reason above. Also, the ball is released by the head unit's servo; a bounded, independent release is declared and is structurally plausible (the ball is on the head, the servo retracts the ram 9 mm). But the ram stroke has no mechanism (dossier section 2), and the ram thrust or retraction force is not compared with the jaw force. The release statement is therefore plausible and not supported.
- **Retraction while engaged:** retracting the ball by 9 mm pulls it back through the throat only if the retraction force exceeds the preload; the servo force is not stated.

## Alignment (geometric_guide)

- **Declared:** a conical funnel in the tail socket guides the ball onto the axis by contact while units close by rolling. No magnet is assumed, so the magnet check does not apply.
- **Principle (accepted in kind):** a conical lead-in centres a ball by contact. The dossier itself says funnel half angle and depth are undefined and that capture across an offset window is for Gate 2 to measure.
- **Governing geometry: not supported.** The capture window is not stated, nor the lateral and angular error the funnel corrects. Candidate-level reasoning also says the units cannot steer (dossier section 8), so approach offset is uncontrolled, which makes the unsized funnel the only guide. Whether it suffices on paper cannot be shown.
- **Closing force:** the ball is already deployed 1.5 mm beyond the shell, so the ball meets the funnel first. The force needed to open the jaws at the throat depends on the unstated preload, and capture depends on approach speed (dossier section 6).

## Conclusion

The principle for both means is physically reasonable. But Gate 1 item G6 requires, for retention and for each alignment means, the governing geometry or forces with the declared dimensions. They are absent, and the dossier says so. Per G6, missing support is `unresolved`. Nothing declared contradicts the requirement (no power to hold, a bounded release, no magnet claim), so this is not a `fail`.

## Required changes before a re-review (r2)

1. Declare jaw geometry, throat width, spring rate and preload, with a retention force in newtons and a comparison to the loads it must resist.
2. Declare funnel half angle, depth and the offset window the funnel corrects, and show on paper that it covers the unsteered approach error.
3. Give the servo's retraction force and show it exceeds the jaw preload, and give a mechanism for the 9 mm ram stroke.
4. State whether orientation is meant to be held in any stated pose; if not, say so in the declaration so the review has a stated scope.
