# Evaluation protocol: Gate 1 paper criteria v1

Governs evaluation against `criteria/gates/gate1-v1.json` (Q61, Q62), **revision 1**. Committed before any candidate declaration exists. Results are labeled **`exploratory`**. A paper-gate pass never becomes `validated_acceptance` (Q38, Q40).

Every result records the criteria path and SHA-256, this protocol's revision, the candidate id and version, the declaration SHA-256, and the code revision of the evaluator, if any (DAT-011, Q39).

Values marked **provisional** are listed in the criteria file with that status.

## 1. Conventions

- Lengths are **integer micrometres** (µm), masses **integer milligrams** (mg), power **integer milliwatts** (mW). All integers are below 2^53. Quantities that must be reals (orientations, densities, volumes, voltages, currents) are decimal numbers. No NaN or infinity.
- Geometry is computed in double precision (IEEE 754 binary64) from the integer inputs. Evaluation order is fixed as written, so the same declaration and the same build give the same result.
- The body frame is right-handed, and the unit length of a quaternion is 1 within 1e-9 (otherwise the declaration is rejected). Quaternions are `[w, x, y, z]`, and rotation is by `q v q*`.
- A **pose** is `{ "position_um": [x, y, z], "orientation": [w, x, y, z] }`.
- **Primitives** are convex and given in the body frame:

| Kind | Fields | Support function h(d) for unit direction d (in the primitive frame) |
| --- | --- | --- |
| `sphere` | `radius_um` | r·d |
| `box` | `half_extent_um: [hx, hy, hz]` | (sgn(dx)·hx, sgn(dy)·hy, sgn(dz)·hz), with sgn(0) = +1 |
| `cylinder` | `radius_um`, `half_height_um`, axis = primitive-frame z | (r·dx/ρ, r·dy/ρ, sgn(dz)·hh) with ρ = √(dx²+dy²); if ρ = 0 the rim point is (r, 0, ·) |

  All extents must be > 0.
- **Outcomes** per item: `pass`, `fail`, `unresolved`. An evaluator error or non-completion of a computation yields `unresolved`, never `pass`.

## 2. Declaration schema (`candidates/<id>/declaration.json`, schema_version 1)

Parsed strictly (DAT-005): unknown fields, missing required fields, duplicate keys, type mismatches, and out-of-range values are rejected. A rejected declaration gets no outcome, and is reported as `rejected` with the reason. It is not a pass.

```text
{
  "schema_version": 1,
  "candidate_id": string,             // [a-z0-9-]+, equals the directory name
  "candidate_version": integer >= 1,
  "family": "A" | "B" | "C",
  "declared_on": "YYYY-MM-DD",
  "author": string,
  "summary": string,

  "stowed_geometry": {
    "primitives": [ { "id": string, "kind": "sphere"|"box"|"cylinder",
                      <kind fields>, "pose": Pose,
                      "role": "body" | "coupler" | "cavity" } ... ]
  },
  "chain_geometry": {                 // geometry with couplers deployed or engaged
    "primitives": [ ... same form, roles "body" | "coupler" ... ]
  },

  "components": [ {
      "id": string,
      "kind": "controller"|"energy_source"|"actuator"|"sensor"|"communication"|"coupler_mechanism"|"magnet"|"structure"|"other",
      "description": string,
      "mass_mg": integer >= 0,
      "mass_basis": "source" | "derived" | "estimate",
      "derivation": { "density_kg_m3": number > 0, "volume_m3": number > 0 },   // required iff mass_basis = derived
      "box": { "half_extent_um": [hx, hy, hz], "pose": Pose },
      "dimension_basis": "source" | "derived" | "estimate",
      "peak_power_mw": integer >= 0,
      "average_power_mw": integer >= 0,
      "power_basis": "source" | "derived" | "estimate",
      "source": { "kind": "datasheet"|"publication", "url": "http(s)://...", "accessed": "YYYY-MM-DD", "title": string },
      "nominal_voltage_v": number > 0,                       // energy_source only
      "rated_continuous_discharge_a": number > 0 | null,     // energy_source only, null if the source does not state it
      "energy_mj": integer > 0                               // energy_source only (millijoules of usable energy)
  } ... ],

  "mass_budget": { "total_mass_mg": integer },

  "assembly_access": { "statement": string },

  "coupler_sites": [ { "id": string, "position_um": [x, y, z], "normal": [x, y, z] (unit, 1e-9),
                       "mount": string } ... ],

  "chain": {
    "head_site": site id, "tail_site": site id (different),
    "rest_orientation": [w, x, y, z],     // unit 1's orientation on the tabletop (world z up, table z = 0)
    "mating_roll_deg": [ number ... ]     // allowed rolls about the mating normal; at least one
  },

  "retention": {
    "requires_power_to_hold": boolean,
    "mechanism_kind": "geometric_interlock"|"spring_preload"|"friction_wedge"|"permanent_magnet"|"other",
    "mechanism": string,
    "component_ids": [ component id ... ],
    "release": { "bounded_independent_release": boolean, "means": string }
  },
  "alignment": [ { "kind": "geometric_guide"|"magnetic"|"other", "description": string,
                   "justification": string, "component_ids": [ component id ... ] } ... ],

  "limitations": [ string ... ]
}
```

Required: every field above except `derivation` (see its condition), the energy-source-only fields on non-source components, and `limitations` (may be empty). Exactly one component has `kind = "energy_source"` (the others must not carry the energy-source-only fields). All `component_ids` and site ids must exist. Ids are unique within their list.

The declaration's SHA-256 is over its exact file bytes.

## 3. G1 — stowed enclosing sphere

Input: `stowed_geometry.primitives` with role `body` or `coupler` (cavity primitives describe the interior and are not part of the envelope). Pose each primitive into the body frame.

1. **Seed points.** For each primitive, in declaration order:
   - box: its 8 corners;
   - cylinder: 64 points on each rim at angles 2πk/64 (k = 0..63), plus the 2 axis end points;
   - sphere: its centre plus r·u for the 26 directions u normalized from every nonzero vector in {−1,0,1}³, ordered lexicographically.
2. **Order and dedupe.** Sort the seed points lexicographically by (x, y, z), drop exact duplicates.
3. **Welzl.** Compute the minimal enclosing sphere of the sorted points with the deterministic move-to-front-free recursive Welzl algorithm: `welzl(P, R)` removes the points of P in sorted order (the last point first), with R at most 4 boundary points; the circumsphere of R is solved by the standard linear system with a deterministic pivoting order. A degenerate (collinear or coplanar) support set falls back to its minimal-dimension circumsphere. Points are tested inside with a relative slack of 1e-12 of the radius.
4. **Certification.** Let `c` be the Welzl centre. The certified radius is `R_cert = max over primitives of the exact farthest-point distance from c to the primitive`, computed per kind: sphere = |c_p − c| + r; box = the max over its 8 corners; cylinder = √((|t| + half_height)² + (ρ_c + r)²), where t is the signed axial offset of c from the cylinder centre and ρ_c is the distance of c from the cylinder axis. The sphere (c, R_cert) provably contains every primitive.
5. **Diameter** D = 2·R_cert (µm).

Outcome: `pass` if D < 60000 − 0.001; `fail` if D > 60000 + 0.001; `unresolved` if |D − 60000| ≤ 0.001 (the numerical band, provisional), or no body or coupler primitive exists, or the computation does not complete (the Welzl recursion is capped at 10⁷ steps).

D is reported, together with the Welzl radius, so the amount the certification adds is visible. For polyhedral parts the two coincide. For round parts D is a **conservative upper bound** on the true minimal diameter.

## 4. G2 — packaging

Components' boxes are oriented boxes (OBBs) with `box.pose`. Cavity primitives are those with role `cavity` (at least one required).

**Intersection test (used here and in G5).** Two convex shapes A and B (spheres, boxes, cylinders, each posed) are said to **interfere** when their **eroded** shapes intersect. Erosion by δ = 1.0 µm (provisional) reduces a sphere's radius by δ, a box's half extents by δ per axis, and a cylinder's radius and half-height by δ (any dimension ≤ 0 after erosion makes the shape empty, which never interferes). The intersection of two convex shapes is decided by the **GJK boolean test** on the Minkowski difference, with initial direction (1, 0, 0), a cap of 64 iterations, and termination when the new support point does not pass the origin within 1e-9 µm. Reaching the cap makes the item `unresolved`. Touching or overlapping by less than the erosion is not interference.

Checks, in order:

1. **No pairwise interference.** For every unordered pair of components (by declaration order), test their boxes. Any interfering pair is a `fail`, listed by id.
2. **Inside the shell.** Each component box must lie entirely inside **one** cavity primitive (conservative for unions): all 8 box corners must have signed distance ≤ 0.001 µm to that primitive (convex shapes, so the corners suffice). A box that fits no single cavity primitive fails, listed by id.
3. **Assembly access.** `assembly_access.statement` has at least 1 non-whitespace character. An absent or empty statement is a `fail`. (This checks presence only. Whether the statement is credible is a reviewer judgement at the gate record, and is noted as a limitation.)

Outcome: `pass` if all three hold; `fail` if any fails; `unresolved` if boxes, poses, or cavity primitives are missing, or a test hits its cap. Minimum clearance between boxes is 0 µm (provisional).

## 5. G3 — evidence

For every component:

- `source.kind` ∈ {datasheet, publication}; `source.url` starts `http://` or `https://` and has at least one character after the scheme; `source.accessed` is a valid calendar date, not before 2000-01-01 and not after `declared_on`.
- `mass_basis`, `dimension_basis`, and `power_basis` are each `source` or `derived`.
- If `mass_basis = derived`: `|mass_mg − density·volume·10⁶| ≤ 1` mg (provisional), where density and volume come from `derivation`.

A **violation of the source rule** (missing source object, invalid kind, malformed URL or date, a date after `declared_on`) makes the component **uncited**. Any `estimate` basis, and any uncited component, makes G3 `unresolved`. A derived-mass inconsistency is a `fail`. There is no `pass` with an uncited component or an estimate. If every component is cited and every basis is source or derived and consistent, G3 is `pass`. With no components, `unresolved`.

The evaluator does not fetch URLs. That the URL resolves and states the cited value is checked by sampling at the gate record, and is a limitation.

## 6. G4 — budgets

Let S be the energy source component.

1. **Mass.** `mass_budget.total_mass_mg` must equal `Σ mass_mg` over all components exactly. Unequal is a `fail`. (Shell, structure, couplers, and fasteners must be components, or their mass is not in the budget.)
2. **Peak power.** `P_peak_mW = Σ peak_power_mw` over all components other than S. The rated limit `P_lim_mW = nominal_voltage_v · rated_continuous_discharge_a · 1000`, computed in double precision and compared as `P_peak_mW ≤ P_lim_mW`. A greater peak is a `fail`. If `rated_continuous_discharge_a` is null, the item is `unresolved`. No credit for non-simultaneous peaks is given at Gate 1 (worst case).
3. **Endurance (reported only).** `P_avg_mW = Σ average_power_mw` over components other than S, `endurance_s = energy_mj · 1000 / P_avg_mW` stated with the `P_avg_mW` it assumes (infinite endurance is reported as `not_applicable` when `P_avg_mW = 0`). No threshold is compared (the criteria mark it `unresolved`, Q31 task duration undecided). The report states that the endurance figure does not enter the outcome.

Outcome: `fail` if mass or peak power fails, `unresolved` if a budget input is missing or the discharge rating is null, else `pass`. The endurance report never changes the outcome.

## 7. G5 — tabletop chain

A declaration with fewer than 2 coupler sites is a `fail`. Otherwise the prerequisites are (missing ones give `unresolved`): `chain.head_site` and `chain.tail_site` exist and differ, `rest_orientation` and at least one `mating_roll_deg` are present.

**Chain construction.** Use `chain_geometry` (roles `body` and `coupler`). For a roll angle ψ in `mating_roll_deg`:

- Unit 1 has orientation `rest_orientation` and is translated vertically so the lowest point of its **body-role** seed points (the §3 seeds) lies at z = 0.
- Unit k+1 is placed by **mating** its `tail_site` onto unit k's `head_site`: the site positions coincide, the site normals become antiparallel, and the unit is rolled by ψ about the shared normal (right-handed about unit k's head normal). The unit's pose is then fully determined.
- Three units are built. Roll angles are tried in the declared order. The first ψ for which all checks below pass is recorded; if none pass, the item is a `fail`.

**Checks for one ψ:**

1. **Table contact for every unit.** The lowest body-role seed point of each unit must be within ±1.0 µm of z = 0 (provisional), and none may lie below −1.0 µm.
2. **Static support for every unit.** Let C be the unit's set of body-role seed points with z ≤ 1.0 µm. Their horizontal projection's convex hull must have non-zero area (≥ 3 non-collinear points), and the unit's centre-of-mass horizontal projection must lie inside it (closed). The centre of mass is the `mass_mg`-weighted mean of the component box centres in the unit frame.
3. **No inter-unit interference.** For every pair of units, and every pair of their **body-role** primitives, the §4 intersection test must report no interference. Coupler-role primitives are exempt (they engage by design).
4. **Coupler sites meet.** The mated site positions agree within 1.0 µm and the normals within 1e-9 (a check of the construction).

A capped intersection test (§4) gives `unresolved`. Outcome: `pass` when some ψ passes; `fail` when the prerequisites hold and no ψ passes; `unresolved` for missing prerequisites or a capped test.

**Limitation.** The check is static geometry at the declared nominal state: mass that shifts in use (for example an internal reaction mass) is evaluated only at its declared nominal position, and coupler-region interference is not examined. Gate 2 tests the dynamics.

## 8. G6 — retention and pre-alignment

Automated checks (all must hold):

1. `retention.requires_power_to_hold` is `false`.
2. `retention.release.bounded_independent_release` is `true` and `release.means` is nonempty.
3. `retention.mechanism` and every `alignment[].justification` are nonempty, and `retention.component_ids` names at least one existing component.
4. **Magnetism.** If `retention.mechanism_kind = "permanent_magnet"` or any alignment `kind = "magnetic"`, then at least one referenced component (in that item's `component_ids`) has `kind = "magnet"`. A magnet component in the list does not by itself justify magnetism.
5. Every alignment entry names at least one component id (a purely geometric guide names the structure or coupler component that carries the guide).
6. **Justification record.** `candidates/<candidate_id>/retention-review-v<candidate_version>-r<n>.md` exists, is written by a reviewer who is not the author, and states `outcome: pass`. The record states, for retention and for each alignment means, the physical principle, the governing geometry or forces with the declared dimensions, and the reasoning that the means works unpowered. Without the record, G6 is `unresolved`. With `outcome: fail`, it is a `fail`.

A check 1–5 violation is a `fail` (statements present but contradicting the requirement). Missing retention or alignment statements are `unresolved`. The record only says the means was judged physically justified on paper. It is not a test of the mechanism (Gate 2/3).

## 9. G7 and G8 — originality (Q61)

Read from the Q61 gate1 review file for this candidate version (latest revision `r<n>` that is complete, with its declaration hash matching the current declaration).

- **G7.** `pass` if the review is complete (Q61 §3 items 3–5 and §6), independent (reviewer ≠ author), and its outcome is `pass`. `fail` if its outcome is `fail`. `unresolved` if the record is missing, incomplete, or its recorded declaration hash differs from the current declaration (a changed declaration needs a re-review).
- **G8.** `fail` if any matrix cell against an F1 or F2 reference is `high`, or if either exclusion (cube with internal flywheel; needle- or particle-like silhouette) is recorded as present. `unresolved` if the record is missing, incomplete, or an exclusion check is not recorded. Otherwise `pass`.

Family membership (A/B/C, Q62 §3) is stated in the review and checked by the reviewer against the declaration. A candidate that does not meet its family's constraint is reported with that finding in the gate record. This is not a separate item.

## 10. Outcome aggregation

Per candidate version, in item order G1..G8:

1. If any item is `fail` → candidate outcome **`fail`**.
2. Else if any item is `unresolved` → **`unresolved`** (not a pass; the unresolved items are listed).
3. Else (all `pass`) → **`pass`**.

The report lists every item's outcome, the computed values (D, Welzl radius, packaging pair results, total mass, `P_peak_mW`, `P_lim_mW`, endurance with its assumed average power, the chain roll angle used and its checks), the declaration and criteria hashes, and the label `exploratory`. Rejected and unresolved candidates are preserved with their reasons (Q38, SEL-007). A revision is a new candidate version, evaluated against the same criteria.

## Limitations of this protocol

- It is a paper gate. It does not show that any mechanism works, that parts can be assembled, or that cited values are correct.
- The G2 shell check requires each box to lie in a single cavity primitive. A shell built as a union of primitives may fail this conservative test and then must be declared with a primitive that contains each part.
- The chain test is static, uses three units, and uses nominal mass positions.
- Several tolerances are provisional (see the criteria file). They are numerical margins, not physical claims.
- Independence of reviewers (Q61 §4) and the sampling of cited sources are procedural. The evaluator cannot verify them beyond recorded fields.
