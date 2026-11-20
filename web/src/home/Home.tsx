import { useEffect } from "react";
import { PostCard, latestPosts } from "../blog/BlogPage";
import { DitherOrigami, type Creature } from "../components/DitherOrigami";
import { CLONE, CopyCommand, Footer, Nav, Poster } from "../components/SiteChrome";
import { DECISIONS, REGISTER } from "../generated/records";
import { GH_BLOB } from "../lib/site";

// From AGENTS.md, in its order. AGENTS.md governs if these drift.
const PRIORITIES = [
  "Mechanical plausibility",
  "Numerical and physical correctness",
  "Deterministic, reproducible experiments",
  "Explicitly validated operating envelopes",
  "Originality",
  "Inspectability",
  "Scalability, only after correctness is established",
];

const LABELS = ["exploratory", "oracle", "fixture", "uncertain", "validated_acceptance"];

const PORTS: [string, boolean][] = [
  ["modeled onboard sensors", true],
  ["its own state and estimates", true],
  ["its own actuators and couplers", true],
  ["messages over modeled links", true],
  ["ground truth: poses, topology, loads", false],
];

const PREREG = ["write the criteria file", "hash it: SHA-256 of the bytes", "register before the run", "run against that hash"];

const INK = { violet: "#5b3df5", orange: "#ff6a2a", yellow: "#f2b300", red: "#e63b2e", blue: "#3d6bff", pink: "#ff4f8b" };

const HERO: Creature[] = [
  { kind: "crane", x: 0.12, y: 0.6, size: 0.26, ink: INK.orange, tilt: -0.08 },
  { kind: "rocket", x: 0.89, y: 0.56, size: 0.3, ink: INK.yellow, tilt: 0.1 },
  { kind: "plane", x: 0.2, y: 0.17, size: 0.1, ink: INK.blue, tilt: -0.15 },
  { kind: "tulip", x: 0.73, y: 0.84, size: 0.13, ink: INK.red },
  { kind: "boat", x: 0.3, y: 0.92, size: 0.08, ink: INK.violet },
  { kind: "heart", x: 0.82, y: 0.15, size: 0.07, ink: INK.pink, tilt: 0.2 },
];
const HERO_FADE = { x: 0.5, y: 0.5, rx: 0.3, ry: 0.55 };

const CTA: Creature[] = [
  { kind: "crane", x: 0.12, y: 0.55, size: 0.36, ink: INK.violet, tilt: -0.1 },
  { kind: "rocket", x: 0.9, y: 0.5, size: 0.34, ink: INK.red, tilt: -0.08 },
];
const CTA_FADE = { x: 0.5, y: 0.5, rx: 0.3, ry: 0.55 };

const SHOT: Creature[] = [
  { kind: "boat", x: 0.08, y: 0.84, size: 0.1, ink: "#d4ff4f" },
  { kind: "plane", x: 0.93, y: 0.16, size: 0.1, ink: "#d4ff4f", tilt: 0.2 },
];

const short = (sha: string) => sha.slice(0, 12);

export function Home() {
  useEffect(() => {
    document.title = "Kinigami — kinetic origami, checked by physics";
  }, []);
  const last = DECISIONS[DECISIONS.length - 1];
  const recent = [...DECISIONS].reverse().slice(0, 10);
  return (
    <div className="rails">
      <Nav current="home" />
      <main>
        <section className="hero" id="top">
          <DitherOrigami className="hero-dither" creatures={HERO} fade={HERO_FADE} />
          <a className="pill" href={`${GH_BLOB}/docs/decisions/${last.file}`}>
            <i aria-hidden="true" />
            {last.id} · {last.recorded} · latest decision
          </a>
          <h1>
            Small machines.
            <br />
            Honest <em>physics.</em>
          </h1>
          <p className="lede">
            A deterministic, physically grounded swarm simulation in Zig. Small robotic units called Kins move, connect, share energy and articulate
            together, and nothing is claimed until a preregistered criterion says so.
          </p>
          <div className="actions">
            <CopyCommand command={CLONE} />
            <a className="btn btn-violet" href="/blog">Read the notes →</a>
          </div>
        </section>

        <div className="shot-wrap">
          <div className="shot">
            <DitherOrigami className="shot-dither" creatures={SHOT} cell={5} light={0.1} />
            <div className="term">
              <div className="term-dots"><i /><i /><i /></div>
              <div className="term-body">
                <p><span className="prompt">$</span> ls docs/decisions | tail -3</p>
                {DECISIONS.slice(-3).map((d) => (
                  <p key={d.id} className="row"><b>{d.id}</b><span>{d.recorded}</span><span className="clip">{d.title}</span></p>
                ))}
                <p><span className="prompt">$</span> cat criteria/REGISTER.md</p>
                {REGISTER.map((r) => (
                  <p key={r.file} className="row reg"><b>{r.file}</b><span className="ok">{short(r.sha256)}</span><span>{r.date}</span></p>
                ))}
                <p className="muted"># every result carries one of these hashes</p>
              </div>
            </div>
          </div>
        </div>

        <section className="features" id="refusals">
          <div className="section-head">
            <div>
              <span className="eyebrow">[01] What Kinigami refuses to fake</span>
              <h2>Every claim is folded from evidence, crease by crease.</h2>
            </div>
            <p>A pretty animation is not proof. These rules hold for every run, every controller and every result the simulator writes.</p>
          </div>

          <div className="bento">
            <article className="cell cell-wide">
              <div className="cell-head">
                <span className="label">Information boundary</span>
                <h3>A controller sees what a real Kin could sense. Nothing more.</h3>
              </div>
              <ul className="ports">
                {PORTS.map(([p, ok]) => (
                  <li key={p} className={ok ? "" : "denied"}>
                    <span>{ok ? "● allowed" : "✕ evaluator only"}</span>
                    <b>{p}</b>
                  </li>
                ))}
              </ul>
            </article>

            <article className="cell cell-violet">
              <div className="cell-head">
                <span className="label">Preregistration</span>
                <h3>Criteria are sealed before the run.</h3>
              </div>
              <ol className="steps">
                {PREREG.map((s, i) => (
                  <li key={s} className={i === PREREG.length - 1 ? "hl" : undefined}>
                    <span>{String(i + 1).padStart(2, "0")}</span>
                    {s}
                  </li>
                ))}
              </ol>
            </article>

            <article className="cell">
              <span className="label">Integer time</span>
              <div>
                <h4>The clock is a counter.</h4>
                <p>Integer ticks, a stable order for ties, seeded randomness and canonical state hashes. Same build, same config, same result.</p>
              </div>
            </article>
            <article className="cell">
              <span className="label">Full 3D only</span>
              <div>
                <h4>No snapping, ever.</h4>
                <p>No planar mode, no docking assist, no unmodeled pose or velocity correction. State labels never create physical links.</p>
              </div>
            </article>
            <article className="cell cell-lime">
              <span className="label">Result labels</span>
              <div>
                <h4>Exactly one, every time.</h4>
                <p className="labels">
                  {LABELS.map((l) => (
                    <code key={l}>{l}</code>
                  ))}
                </p>
              </div>
            </article>
          </div>
        </section>

        <section className="night" id="principles">
          <div className="night-head">
            <h2>In this order.</h2>
            <a className="btn btn-ghost-dark btn-sm" href={`${GH_BLOB}/AGENTS.md`}>Read AGENTS.md →</a>
          </div>
          <div className="night-body">
            <ol className="prio">
              {PRIORITIES.map((p, i) => (
                <li key={p}>
                  <span>{String(i + 1).padStart(2, "0")}</span>
                  {p}
                </li>
              ))}
            </ol>
            <Poster layout="card">
              <div className="statement">
                <p>An attractive animation is not evidence that a mechanism works.</p>
                <small>AGENTS.md · priorities, in order</small>
              </div>
            </Poster>
          </div>
        </section>

        <section className="log-section" id="decisions">
          <div className="section-head">
            <div>
              <span className="eyebrow">[02] The decision log</span>
              <h2>Recorded, not remembered.</h2>
            </div>
            <p>
              Append-only. A decision changes only through a new record that names what it supersedes. This table is read from{" "}
              <a href={`${GH_BLOB}/docs/decisions/README.md`}>docs/decisions</a> on every build.
            </p>
          </div>
          <div className="table-wrap">
            <table className="log">
              <thead>
                <tr><th>ID</th><th>Decision</th><th>Status</th><th>Recorded</th></tr>
              </thead>
              <tbody>
                {recent.map((d, i) => (
                  <tr key={d.id} className={i === 0 ? "hl" : undefined}>
                    <td><a href={`${GH_BLOB}/docs/decisions/${d.file}`}>{d.id}</a></td>
                    <td><a href={`${GH_BLOB}/docs/decisions/${d.file}`}>{d.title}</a></td>
                    <td>{d.status}</td>
                    <td>{d.recorded}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="table-foot">
            <p>
              <b>Where the log is thin:</b> Q1–Q30 survive only by reference; their original wording is not in the repository and is never reconstructed
              as verbatim.
            </p>
            <a href={`${GH_BLOB}/docs/decisions/README.md`}>Full index · {DECISIONS.length} records since {DECISIONS[0]?.id} →</a>
          </div>
        </section>

        <section className="posts-section">
          <div className="section-head">
            <div>
              <span className="eyebrow">[03] From the blog</span>
              <h2>Notes from the bench.</h2>
            </div>
            <p>
              Engineering decisions, one record at a time. <a href="/blog">All posts →</a>
            </p>
          </div>
          <div className="blog-grid home-posts">
            {latestPosts(3).map((p) => (
              <PostCard key={p.slug} post={p} />
            ))}
          </div>
        </section>

        <section className="cta">
          <DitherOrigami className="cta-dither" creatures={CTA} fade={CTA_FADE} light={0.15} />
          <h2>
            Fold once.
            <br />
            Check everything.
          </h2>
          <CopyCommand command={CLONE} />
        </section>
      </main>
      <Footer />
    </div>
  );
}
