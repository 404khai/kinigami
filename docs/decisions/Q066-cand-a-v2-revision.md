# Q66 — cand-a version 2: revision decisions

| Field | Value |
| --- | --- |
| Status | accepted |
| Recorded | 2026-11-06 |
| Supersedes | — (revises a candidate, not a requirement; changes no criterion, threshold, protocol text or criteria JSON; Gate 1 is evaluated under the unchanged `criteria/gates/gate1-v1.json`, Q62, protocol rev. 2 per Q63) |
| Provenance | **agent decision under explicit owner delegation** (the owner asked for cand-a v2 and delegated its decisions). Engineering lead: Claude Opus 5.5. Implementation: Claude Sonnet 5.5. The owner may revise it through a superseding record |

## Context

Gate 1 run 1 left cand-a v1 `unresolved` (Q64 §3). Four things blocked it. G3 had estimate-basis parts. G6 had retention and alignment that were not sized. The kick mechanism was only a reservation. And the rigid coupler conflicted with the chain bending that Q31 requires. Q64 decided that no revision would be authored without real engineering numbers. This record states the choices made for v2 and why. It is a candidate proposal under Q38, **not a design selection**. Selection happens only at the Q38 gates.

## Decision

1. **Body.** Same family (A) and form: a regular hexagonal prism that rolls over its long edges about the prism axis. The circumradius drops from 26.0 to 25.5 mm (H 28 mm) to widen the G1 margin from 0.94 mm to about 1.8 mm, which leaves room for SLS tolerance. G1 passes at both sizes, so this is a manufacturing-margin choice, not gate tuning.
2. **Kick mechanism.** v1's reserved strut is replaced by one **lift lobe on a ring in a girdle slot** at mid-length. One PMD 206-109 gearmotor drives it through a spur pair, a layshaft and an internal gear. The lobe reach is L = 28.5 mm, which is more than R. This lets the lobe lift the body quasi-statically past its tipping point about the leading bottom edge. Every 60° of ring rotation is one 60° step, and reversing the ring reverses the roll. Rationale: one actuator gives both directions on every face, needs no stored-energy snap, and fits the Q12 sphere because the lobe sits at the girdle (y = 0), where the sphere is widest. **Steering and axial motion are not provided**, and this is recorded as a limitation, not hidden.
3. **Coupler.** The ball-lock with SMA-pulled sleeve and the cone lead-in are dropped. The new coupler has these parts:
   - **Lateral roll-in arc channel.** The channel is cut in the tail end so that a neighbour's head peg enters along the exact path the unit's own roll step traces. The closing force is the unit's own lift drive plus gravity, which answers the v1 retention review's "no closing force".
   - **Fixed hex peg** on the head (304 stainless).
   - **Dead-centre (bistable) toggle keeper** that locks the peg's groove geometrically when unpowered.
   - **Short Flexinol pulse** that flips the keeper open. It stays open unpowered and is re-closed by the arriving peg.
   - **Yaw turntable** that carries the seat, driven through a worm by a second 206-109. This gives an actuated in-plane bend of ±12° per joint, with ±15° hard stops.

   Rationale: a Family A unit has no internal joint, so Q31 bending must come from an articulating coupler. A passive coupler driven by the units' own rolling would need about ±45° per joint at 25.5 mm per step. That would mean an end-face gap of about 20 mm, which does not fit. So the joint is actuated.
4. **Release actuator.** Releasing by yaw overtravel was considered and rejected. After overtravel the open seat cannot carry the neighbour's yaw back to zero, so the peg could not leave along the channel. A third gearmotor did not fit in the cavity. A 22 mm Flexinol wire on the yaw axis does fit. **Originality risk, recorded on purpose:** an SMA-released latch on a grooved pin is the CONRO connector principle (Q64-C21, rated high against cand-b in run 1). The v2 keeper differs: it is a bistable geometric toggle with no spring holding it closed, it is released by a pulse, and it has a lateral arc entry, a single hex peg, and a yaw turntable. Whether that is enough is for the independent reviewer to decide. This record does not decide it.
5. **Parts with cited values (G3).**
   - The controller is the Adafruit QT Py ESP32-C3. Its peak power is bounded by its regulator's stated 600 mA peak output.
   - The IMU is the Pololu LSM6DSO carrier.
   - The drivers are two Pololu DRV8835 carriers. Their thickness comes from the Pololu dimension drawing.
   - Both motors are the PMD 206-109. They are PWM-limited to at most 3.0 V effective, because the datasheet's maximum operating voltage is 3.6 V.
   - Materials are EOS PA 2200, ATI 304, Dynalloy NiTi and Aurubis Cu-ETP. Hardware is the Lee Spring LC 014A 01 S spring, M1.6 A2 screws and Alpha Wire 2841/7.

   Where a part's thickness or mass was not stated by its maker (the Seeed XIAO nRF52840 Sense, the Pololu DRV8838 thickness), that part was replaced, not estimated. Derived masses of mixed or cut parts are stated as upper bounds.
6. **Design loads for passive retention (CPL-009, Q31 item 6).** These are derived from the unit weight and a table friction bound of μ ≤ 1. That bound is a **provisional design assumption** (Q47 fixes the friction law, not a coefficient). They are design inputs only. They are not Gate 1 thresholds and not acceptance loads.
7. **Records.** v2 uses the Q65 layout: `declaration.json` (v2), `declaration-v1.json` (the v1 bytes), `dossier-v2.md`, and r1 reviews for v2 written by an agent that did not author v2.

## Alternatives considered

- **Keep the v1 strut and enlarge the reservation:** a 14 mm stroke per face does not fit. Rejected.
- **Internal reaction wheel:** this would trigger family exclusion 1 (the M-Blocks lineage). Rejected.
- **Passive bending by differential rolling:** this needs about ±45° joint range and about a 20 mm end gap. Infeasible at this scale. Rejected.
- **A gearmotor as release actuator:** no packing solution was found with three motors. Rejected for v2.
- **Keep the XIAO nRF52840 Sense:** its mass and thickness are not stated by the maker, so G3 could only be unresolved. Replaced.

## Consequences

- v2 is evaluated under the unchanged Gate 1 criteria. Whatever the outcome, v1 and its reviews stay preserved (SEL-007).
- These remain open at Gate 1 and are listed in the dossier:
  - steering
  - whether the worm self-locks (it needs μ ≥ 0.125)
  - the share of landing energy that reaches the keeper trip
  - SLS tolerances, which are not cited
  - wall strength
  - heat
  - the five-unit chain

  None of these is a Gate 1 item, and none becomes evidence by passing Gate 1.
