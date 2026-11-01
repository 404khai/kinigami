# Q51 — Recording snapshot payload and interval

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-01 |
| Supersedes | — (fills the payload layout and snapshot interval Q44 left open) |
| Provenance | condensed from owner decision ("go with A") |

## Context

Recording format v1 fixed only the container: the effective configuration chunk plus an end marker. The inspector (Q45, Q50) needs recorded state to display. Q44 left the payload layout and snapshot interval open.

## Decision

**Option A: a snapshot after every physics step, holding full body state and solver-native contacts.**

- **Interval.** One snapshot per physics step on the evaluation timeline (t ≥ 0), including the initial state at t = 0. The interval is an explicit field in the recording (`snapshot_interval_steps = 1`), so a sparser interval would need a new decision, not a silent change.
- **Contents.**
  - **Scene header, once:** time unit, physics step, snapshot interval, and per body: ID, kind (fixture or Kin candidate), shape (cuboid half-extents), and mass.
  - **Each snapshot:** tick, and per body: position, orientation, linear velocity, and angular velocity. Every contact from the step that produced the state: bodies, point, normal, normal force, and tangential force, all solver outputs (PHY-005).
- **Encoding.** Recording **format version 2**, with explicit little-endian fields and exact `f64` bit patterns (DAT-002). Readers for v1 remain (DAT-010).

## Rationale

- Every recorded frame corresponds one-to-one with the samples the evaluator scored, so the inspector shows exactly what was judged.
- Single-step events stay visible. The run 1 friction slip happened within one step.
- Size is small at fixture scale (about 0.5 MB for a 2 s run at 0.5 ms).

## Alternatives considered

- **B. Every N steps:** short events between snapshots are lost, and playback no longer matches the scored samples.
- **C. Keyframes plus an event log:** more compact but more complex. It can be revisited for large swarms (R17).

## Consequences

- Recording writes must not change simulation results. This is verified by comparing final-state hashes with recording on and off (INS-007).
- Pre-roll settling (protocol revision 2) is not recorded. Recordings start at t = 0.
