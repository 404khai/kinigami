# Q57 — Coupler-engagement qualification criteria (preregistration before coupler code)

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-02 |
| Supersedes | — (fills PHY-012/PHY-013-style acceptance values for the coupler-engagement capability; carries the Q54 carry-overs) |
| Provenance | **agent decision under explicit owner delegation** ("I trust its judgement"). The owner may revise it through a superseding record |

## Context

Q56 declares the fixture stand-in. Q36 and Q40 require engagement to be continuous, assistance-free, and measured by sweeps. Q54 deferred three items here: link load limits and failure, link release and topology change (PHY-003), and stiff-link dynamics at a finer timestep. This record preregisters the acceptance values **before any guide-contact, latch, or engagement code exists** (Q39, Q52 precedent).

All values are solver-qualification parameters on neutral fixtures, not coupler or Kin-candidate claims (Q40).

## Decision

1. **Criteria file** `criteria/qualification/coupler-engagement-v1.json` (SHA-256 in `criteria/REGISTER.md`) and **protocol** `docs/validation/coupler-engagement-v1-protocol.md` revision 1 are the governing documents. Every measurement definition is fixed there.
2. **Cases C1–C10:**

   | Case | Qualifies | Reference |
   | --- | --- | --- |
   | C1 | Seated preload statics: guide contact and latch link share load consistently | Closed form, 1e-3 |
   | C2 | Seat separation threshold at 0.9× and 1.1× the pull that unseats the ball | Closed form, 1e-3, no seat force once open |
   | C3 | Link load limits and separation per axis (tension, shear, bending, torsion) at e = 1 and 0.5 | Limits from solver loads only; 1e-2 accuracy; no separation at 0.9× |
   | C4 | Engagement from zero: timing, continuity of e, resulting preload; blocked outside the capture zone | Closed form, 2 steps |
   | C5 | Release under axial load: separates at 0.9× the block tension, blocked at 1.1× | Independent RK4 one-DOF model, 2 steps |
   | C6 | Unloaded release: clean removal at zero stiffness, no force jump | Closed form, 2 steps |
   | C7 | Stiff-link dynamics (Q54 carry-over) at Δt = 50, 100, 200 µs | Q52 measures; period 1e-2, ζ 25 %, ζ_num ≤ 0.01 |
   | C8 | Capture sweep: approach speed × lateral offset × misalignment × direction × friction | Measured, reported, not gated |
   | C9 | Audit discrimination: deliberately wrong controls must fail the audits | Both controls fail at every Δt |
   | C10 | Determinism | Bit-identical replay |

3. **Timestep grid:** 50, 100, 200 µs. The stiff link (1e4 N/m, reduced mass 0.01 kg) has ω = 1000 rad/s, so ω·Δt = 0.05, 0.1, 0.2 and all axial combinations are resolved. This is the "finer-Δt criteria version" Q54 §4 called for. Torsion at 200 µs (ω·Δt = 0.245) is `outside_envelope`.
4. **No-unmodeled-forces audits (CPL-004)** run on every C1–C8 run: momentum, per-step impulse accounting against reported solver forces, bit-exact pose integration, and a one-sided energy-creation bound. C9 shows the audits are not vacuous: a velocity snap or a pose snap on link activation must be caught.
5. **The capture window is reported, not gated** (CPL-006). Its uncertainty is the grid resolution (1 mm lateral) and the Δt disagreement flag. Declaring a capture window as a pass criterion would pre-decide the measurement Q36 §2 forbids.
6. **Outcome rule** is Q48/Q52: all evaluated combinations pass → pass, all fail → fail, mixed → uncertain. `outside_envelope` and `outside_model` are listed and not counted.
7. **Label:** `fixture`. A pass qualifies the declared envelope for this stand-in only.

## Rationale

- Statics tolerances reuse Q52's 1e-3. Event-time tolerances reuse Q48's two steps.
- The limit-separation tolerance (1e-2) is wider than statics because the load is ramped and sampled once per step. It stays far below the 10 % factor that brackets each threshold.
- The energy bound's 2 % allows the bounded shadow-energy oscillation of the q = 1/4 link step ((ω·Δt)²/4 = 1 % at the resolution limit). It is one-sided so dissipation is allowed and creation is not.
- C5's reference is an independent RK4 integration at 1 µs, not the production step map, so a timing error in the production update cannot cancel.

## Safeguards (Q49)

- Criteria and protocol are committed before any solver code for this slice. Changing either after observing results requires a new decision record before the rerun counts as official.
- The same agent wrote criteria and (via delegation) the implementation. Mitigations: closed-form and independent-integrator references, audit-discrimination controls (C9), and a regression gate that the existing 63 and 60 final-state hashes stay bit-identical.

## Consequences

- Link release, failure, and topology change (PHY-003) and link load limits are verified here, for the fixture only.
- CPL-011 stays `unresolved` for Kin couplers. Only the fixture scope is decided (Q56).
- A failure or `uncertain` result is reported as such.
