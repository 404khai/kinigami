import type { FigureId } from "../generated/figures";
import { REGISTER } from "../generated/records";
import { GH_BLOB, PORTFOLIO } from "../lib/site";

/** A post is a list of blocks, so it renders as HTML and copies as Markdown from one source. */
export type Block =
  | { p: string }
  | { h2: string }
  | { code: string; lang?: string }
  | { figure: FigureId; caption: string }
  | { list: string[] }
  | { stats: { label: string; value: string; note?: string }[] };

export type Post = {
  slug: string;
  title: string;
  /** short display title for the cover */
  cover: string;
  category: "Determinism" | "Control" | "Validation" | "Mechanism";
  date: string; // ISO
  summary: string;
  figure: FigureId;
  /** the decision records the post is written from */
  decisions: string[];
  sources: { label: string; href: string }[];
  body: Block[];
};

export const AUTHOR = {
  name: "404khai",
  handle: "@404khai",
  avatar: "/404khai.png",
  href: PORTFOLIO,
};

const Q = (file: string) => `${GH_BLOB}/docs/decisions/${file}`;

// Every claim below comes from the decision records listed on the post. Records govern: if a
// post and a record disagree, the record is right and the post is fixed.
// Inline markup: `code`, **bold**, [text](href). Kept tiny on purpose.
export const POSTS: Post[] = [
  {
    slug: "cand-a-stop",
    title: "Eight couplers, one 40 mm cavity",
    cover: "cand-a",
    category: "Mechanism",
    date: "2026-11-20",
    summary:
      "Our nearest Kin candidate failed the paper gate eight times, always at the coupler. Why we stopped revising it, what we kept, and why stopping selects nothing.",
    figure: "cavity",
    decisions: ["Q62", "Q73", "Q84"],
    sources: [
      { label: "Q62: Gate 1 paper-feasibility criteria", href: Q("Q062-gate1-paper-criteria.md") },
      { label: "Q73: Gate 1 run 5 disposition (cand-a v5)", href: Q("Q073-gate1-run5-disposition.md") },
      { label: "Q84: stop cand-a coupler revisions", href: Q("Q084-stop-cand-a-coupler-revisions.md") },
      { label: "Study: cand-a v6 = K4 + K1 go/no-go", href: `${GH_BLOB}/docs/studies/coupler-k4-gonogo.md` },
      { label: "Study: cand-a v6 K4w (wedge-driven jaw) go/no-go", href: `${GH_BLOB}/docs/studies/coupler-k4w-gonogo.md` },
    ],
    body: [
      { p: "A Kin candidate has to pass **Gate 1** on paper before anything about it is simulated. Gate 1 has eight hard items: the 60 mm stowed envelope, packaging, a cited source for every part, mass and power budgets, a coupler layout that lets a three-unit chain rest on a tabletop, passive retention and pre-alignment, and two originality checks. There is no weighted score. One `fail` rejects the version." },
      { p: "cand-a is family A: a single rigid polyhedral body that moves by pivoting or rolling over its edges, with couplers on its faces. After the first run it was the nearest of the three candidates to passing. On 20 November we stopped revising its coupler." },
      { h2: "Five versions, one pattern" },
      { p: "Each version got a new declaration, a new independent retention review and a new gate run. The retention item, G6, is where each one stopped:" },
      { list: [
        "**v1:** unresolved. The dossier did not size its retention or alignment features.",
        "**v2:** unresolved. The toggle lock's geometry was undefined, and the declared spring direction did not make it bistable.",
        "**v3:** fail, on the channel arc. The roll-in kinematics had to be corrected.",
        "**v4:** unresolved. The corrected kinematics reproduced, but class-f tolerance on PA12 parts reached the lock and the stroke.",
        "**v5:** fail. The roll lock is lost for free play above 0.62 mm, so the declared torsion load has nothing to carry it.",
      ] },
      { p: "Every fix exposed the next margin. The run 5 disposition put it plainly: what was left were coupler tolerance-stack problems inside a 40 mm cavity." },
      { figure: "cavity", caption: "Schematic, not cand-a's geometry. The cell, controller, three motors and three mechanisms claim the cavity before the coupler gets any room." },
      { h2: "The eighth attempt" },
      { p: "Three more couplers followed as exploratory paper studies: a seat-frame v6, a two-pin v6, and K4 + K1, a lead-screw lock. The K4 go/no-go ran three checks." },
      { stats: [
        { label: "Self-locking margin, dry", value: "2.05×", note: "cited μ ≥ 0.15 against tan λ = 0.073" },
        { label: "Self-locking margin, oiled", value: "1.37×", note: "and sensitive to vibration" },
        { label: "Screw top needed", value: "21.23 mm", note: "the r ≤ 20 rule allows 19.97" },
      ] },
      { p: "Self-locking passed, but only dry. Packing passed only with five changes to v5 parts and the screw stroke capped at 4.97 mm. The jaw window failed: at the stroke the screw can supply, the jaw clearance to a raised peg is **0.000 mm against 0.30 mm** required. The screw would need 1.26 mm more length than the cavity has." },
      { h2: "Stopping is a result" },
      { p: "A ninth variant, K4w, drove the jaw through a wedge instead. It was checked after the stop and is also a no-go: self-locking fails, and the screw is 1.98 mm short." },
      { p: "Q84 records the stop. The cavity has to hold the cell, the controller, three motors and the roll-in, yaw and keeper mechanisms. Eight times, that left no room for a tolerance-robust, two-sided coupler at cited machining classes." },
      { list: [
        "v5 is preserved with its `fail` verdict. Nothing is deleted or edited.",
        "The body, the lift-lobe locomotion, the corrected roll-in kinematics, the four-bar lock and the analysis scripts stay as reusable results.",
        "No candidate survives Gate 1, so modeling the sensors, actuators and communication of a real Kin stays blocked.",
      ] },
      { h2: "The next step is the owner's" },
      { p: "Each remaining option changes an earlier owner decision or the candidate set, so none is taken under delegation:" },
      { list: [
        "Revise cand-b or cand-c. Each fails the tabletop-chain item and has unsized retention.",
        "Revisit scope: the 60 mm envelope (Q12), or whether chain bending must be built into the coupler at Gate 1.",
        "New candidates or families that budget the coupler first.",
      ] },
      { p: "None of this selects a design. A paper gate is not evidence that a mechanism works, and a stopped line of revisions is not proof that it can't." },
    ],
  },
  {
    slug: "swap-check",
    title: "The check we got wrong twice",
    cover: "Preregistration",
    category: "Validation",
    date: "2026-11-19",
    summary:
      "Criteria are hashed before the run they govern. That rule earns its keep on the day the criteria are wrong. The body-contact suite gave us that day twice.",
    figure: "register",
    decisions: ["Q39", "Q79", "Q80"],
    sources: [
      { label: "Q39: decision records and preregistration", href: Q("Q039-records-and-preregistration.md") },
      { label: "Q79: body-contact criteria v2", href: Q("Q079-body-contact-v2-bb6-swap-bb8-gyroscopic.md") },
      { label: "Q80: body-contact criteria v3, BB6 on the midplane", href: Q("Q080-body-contact-v3-bb6-midplane.md") },
      { label: "Criteria register", href: `${GH_BLOB}/criteria/REGISTER.md` },
    ],
    body: [
      { p: "In Kinigami, criteria are written, committed and hashed before the evaluation they govern, and a slice's solver code is not written until its validation criteria exist. The body-body contact criteria were registered before any box-box contact code. Then they turned out to be wrong, twice." },
      { h2: "How a criterion is registered" },
      { list: [
        "A criteria file is JSON, parsed strictly. Unknown fields, missing fields, duplicate keys and out-of-range values are all rejected.",
        "Its identity is the SHA-256 of its exact bytes, recorded with the commit and date in `criteria/REGISTER.md`.",
        "Every result records the criteria path and hash it was evaluated against.",
        "A revision is a new file and a new register row. A registered file is never edited in place.",
      ] },
      { p: "A local commit is not independent proof of when something was written. Where stronger evidence is needed, the hash can be published or externally timestamped before the run. None has been yet, and every row of the register says so." },
      { h2: "BB6, version 1" },
      { p: "The box-box suite has a symmetry case, **BB6**: evaluate the contact between boxes A and B, then again as B and A, and the answers should agree. Version 1 asked for the same point set when swapped, and for every point to lie on the incident face. Those two rules contradict each other, because swapping the pair can change which box is incident. Run 1 failed BB6 on that conflict. The run is preserved, and the slice was not qualified." },
      { figure: "register", caption: "Each version of the criteria is its own sealed file. Run 2 reads version 3; versions 1 and 2 stay in the rack." },
      { h2: "Version 2 was the lead's error" },
      { p: "Version 2 said a swapped point is the original point translated by one penetration depth. That holds when swapping exchanges the incident box, as in face-face contact. In edge-face contact the same reference face wins in both orders, and in edge-edge contact the midpoint is already symmetric." },
      { p: "A non-official run caught it: face-face passed, and edge-face and edge-edge failed by exactly one depth. No official run ever used version 2." },
      { h2: "Version 3 projects onto the midplane" },
      { p: "Version 3 asks that the swapped manifold have the negated normal, the same depth, the same point count, and **the same point set after projecting each point onto the contact midplane**. Projected onto the midplane, a point does not depend on which box is incident. Run 2 uses version 3, and every other value in the criteria is unchanged." },
      { stats: [
        { label: "Versions of the body-contact criteria", value: "3" },
        { label: "Official runs judged by version 2", value: "0" },
        { label: "Criteria files in the register", value: String(REGISTER.length), note: "each registered before its run" },
      ] },
      { h2: "Why not just fix the file" },
      { p: "Editing version 1 in place would make run 1 look as if it had been judged against rules it never saw. Instead each revision names what it supersedes, gives the reason and the date, and lists the evaluations it affects and the reruns it needs. The wrong versions stay in the repository, next to the runs that exposed them." },
    ],
  },
  {
    slug: "information-boundary",
    title: "What a Kin is allowed to know",
    cover: "The Boundary",
    category: "Control",
    date: "2026-10-30",
    summary:
      "Every Kin runs in one process, so it would be easy to let controllers peek at the simulator. A pass is only worth something if they can't. Where the wall goes, and the one exception.",
    figure: "boundary",
    decisions: ["Q32"],
    sources: [{ label: "Q32: controller information boundary", href: Q("Q032-controller-information-boundary.md") }],
    body: [
      { p: "The first benchmark asks five Kins on a tabletop to change shape as one connected chain. A pass only means something if the controllers could have done it with information a real Kin would have. A controller that reads the simulator's exact poses is not decentralized. It is the simulator steering itself." },
      { h2: "Two sides of a wall" },
      { p: "The physics engine and the evaluator see everything: exact poses, joint configurations, contact states, topology, forces, deflections, actuator states and the full history. An acceptance controller sees only:" },
      { list: [
        "its modeled onboard sensors",
        "its own internal state and the estimates it is allowed to form",
        "direct feedback from its own actuators and couplers",
        "messages received over modeled communication links",
        "what it has kept, within declared memory limits",
      ] },
      { figure: "boundary", caption: "Ground truth stays with the evaluator. The controller's only inputs are ports a real Kin would have." },
      { p: "The evaluator uses ground truth to score a run and never hands it over." },
      { h2: "Even the target arrives by message" },
      { p: "The target shape goes to one designated Kin through its normal communication interface. From there it spreads only over modeled links between connected Kins. No Kin gets an automatic snapshot of global geometry, pose or topology. The designated Kin's role is software only, with no extra mechanics, sensing or computation." },
      { p: "The target describes the desired collective shape, preferably as relative chain geometry. It does not prescribe body trajectories, actuator histories or the order in which attachments change. The evaluator compares the final shape and ignores whole-chain translation and rotation." },
      { h2: "One process is not a radio" },
      { p: "Because every Kin shares a process, instant communication would cost nothing, so it is forbidden. Each link model documents range, latency, bandwidth, ordering, queuing, loss and, where supported, energy. A Kin never hears from a neighbor it could not physically reach. Sensor noise, quantization and latency reach the controller through its interface, not only through the visualization." },
      { p: "No noise level, delay or bandwidth is picked to make a run work. Each comes from a documented component or a justified estimate. Otherwise it is labeled provisional and gets a sensitivity study." },
      { h2: "Oracle runs, labeled" },
      { p: "Some questions need ground truth. Is the target reachable at all? What is the best accuracy any controller could get? Did the mechanism fail, or the controller? **Oracle runs** answer those questions. Each one is labeled in its replay metadata and results, and none ever counts as a decentralized pass." },
      { stats: [
        { label: "Kins in the first benchmark", value: "5" },
        { label: "Oracle runs that can pass", value: "0", note: "diagnostic comparison only" },
      ] },
      { p: "A privileged trajectory is also never copied quietly into an acceptance controller as prescribed poses or actuator commands. That would carry the oracle across the wall by another route." },
    ],
  },
  {
    slug: "integer-time",
    title: "Time is an integer",
    cover: "Integer Time",
    category: "Determinism",
    date: "2026-10-30",
    summary:
      "Same build plus same configuration must give the same result. That starts with the clock: an integer tick count, a stable order for ties, and honest timestamps between physics steps.",
    figure: "clock",
    decisions: ["Q43"],
    sources: [{ label: "Q43: simulated time representation and scheduling", href: Q("Q043-simulated-time.md") }],
    body: [
      { p: "Kinigami runs have to replay exactly. Floating-point time works against that without saying so: an accumulator that adds a step millions of times drifts, and two events that should coincide end up in an order nobody chose." },
      { h2: "The clock is a counter" },
      { p: "Simulated time is an **integer tick count**, with a time unit declared per experiment. The fixed physics step is an integer multiple of that unit. Time arithmetic checks for overflow and never wraps silently. Every run records its time unit, its physics step and its scheduler configuration." },
      { p: "Sensor sampling, message delivery, computation and controller events each have their own scheduled times and periods. They are not rounded to the physics step, so a message latency shorter than one step is represented exactly." },
      { figure: "clock", caption: "Events land on their own ticks. A sensor reads the last completed step; a command waits for the next one." },
      { h2: "Ties are broken on purpose" },
      { p: "Events at the same tick are never ordered by insertion order, by which thread finished first or by memory layout. The queue uses a stable total order, with the phase order written down:" },
      { code: "(scheduled_tick, event_phase, source_id, sequence_number)", lang: "event order" },
      { h2: "Between physics steps" },
      { list: [
        "A message is delivered, and a computation completes, at its scheduled tick.",
        "A sensor samples the most recently completed physics state.",
        "A controller's output becomes available after its declared compute latency.",
        "An actuator command takes effect at the next physics boundary. It cannot change an integration that has already finished.",
      ] },
      { p: "Each sensor record carries both the requested sample time and the time of the state it actually read. Each actuator record carries both when the command was ready and when it was applied. The gap is recorded, not hidden." },
      { h2: "Changing the step changes something" },
      { p: "When a sensitivity study changes the physics step, the nominal sensor, compute and message times stay where they were. What changes is how old a sampled state is and how long a command waits for a boundary. The first proposal said those timings \"stay fixed\". The owner corrected it: they are measured in the study, and never described as unchanged." },
      { p: "The principle we kept: **simulated time belongs to the experiment, not to the physics solver.**" },
      { h2: "What we ruled out" },
      { list: [
        "**Quantizing everything to the physics step.** Sub-step latencies can't be represented, and every rate quietly depends on the step.",
        "**An adaptive or variable step.** Another source of nondeterminism, and harder sensitivity studies. It is excluded from slices 1 and 2. Adding it later needs its own evidence-backed decision, not a quiet solver optimization.",
      ] },
    ],
  },
];

export const postBySlug = (slug: string) => POSTS.find((p) => p.slug === slug);

/** Plain-text word count, for reading time. */
export function readingMinutes(post: Post) {
  const words = post.body
    .map((b) => ("p" in b ? b.p : "h2" in b ? b.h2 : "list" in b ? b.list.join(" ") : "code" in b ? b.code : ""))
    .join(" ")
    .split(/\s+/).length;
  return Math.max(1, Math.round(words / 220));
}

/** The post as Markdown, for "Copy as Markdown". */
export function toMarkdown(post: Post, url: string) {
  const out = [`# ${post.title}`, "", `_${post.summary}_`, "", `By ${AUTHOR.name} · ${post.date} · ${url}`, ""];
  for (const b of post.body) {
    if ("p" in b) out.push(b.p, "");
    else if ("h2" in b) out.push(`## ${b.h2}`, "");
    else if ("code" in b) out.push("```", b.code, "```", "");
    else if ("list" in b) out.push(...b.list.map((l) => `- ${l}`), "");
    else if ("figure" in b) out.push(`> Figure: ${b.caption}`, "");
    else if ("stats" in b) out.push(...b.stats.map((s) => `- **${s.value}** ${s.label}${s.note ? ` (${s.note})` : ""}`), "");
  }
  out.push("Sources:", ...post.sources.map((s) => `- [${s.label}](${s.href})`));
  return out.join("\n");
}
