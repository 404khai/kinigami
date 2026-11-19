import { useEffect } from "react";
import { PostCard, latestPosts } from "../blog/BlogPage";
import { GearTrain } from "../components/GearTrain";
import { Footer, Nav } from "../components/SiteChrome";
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

const RULES: [string, string][] = [
  ["No silent changes", "A requirement, criterion or threshold changes only through a new decision record that names what it supersedes."],
  ["No invented numbers", "Values come from evidence or are labeled provisional. Otherwise they stay unresolved."],
  ["Full 3D only", "No planar mode, no snapping, no docking assist, no unmodeled pose or velocity correction."],
  ["Information boundary", "Controllers see modeled sensors, their own state and modeled messages. Ground truth belongs to the evaluator."],
  ["Preregistration", "Criteria are committed and hashed before the evaluation they govern."],
  ["Determinism", "Integer time, explicit event ordering, seeded RNG and canonical state hashes."],
];

const LABELS = ["exploratory", "oracle", "fixture", "uncertain", "validated_acceptance"];

function Corners() {
  return (
    <>
      <i className="corner tl" />
      <i className="corner tr" />
      <i className="corner bl" />
      <i className="corner br" />
    </>
  );
}

export function Home() {
  useEffect(() => {
    document.title = "Kinigami — kinetic origami, checked by physics";
  }, []);
  const recent = [...DECISIONS].reverse().slice(0, 8);
  const range = `${DECISIONS[0]?.id}–${DECISIONS[DECISIONS.length - 1]?.id}`;
  return (
    <>
      <Nav current="home" />
      <main>
        <section className="hero">
          <div>
            <span className="mono eyebrow">Kinetic origami · Swarm simulation · Zig</span>
            <h1 className="display headline">
              Small machines.
              <br />
              Honest <em>physics.</em>
            </h1>
            <p className="hero-copy">
              Kinigami is a deterministic, physically grounded simulation of small robotic units called <b>Kins</b> that move, connect, communicate, share
              energy and articulate together, and can be inspected down to mechanical detail. Nothing is claimed until a preregistered criterion says so.
            </p>
            <ul className="stats mono">
              <li><b>{DECISIONS.length}</b>Decisions {range}</li>
              <li><b>{String(REGISTER.length).padStart(2, "0")}</b>Criteria sealed</li>
              <li><b>{String(LABELS.length).padStart(2, "0")}</b>Result labels</li>
              <li><b>00</b>2D modes</li>
            </ul>
          </div>
          <div className="hero-art panel">
            <Corners />
            <GearTrain />
          </div>
        </section>

        <section className="section">
          <div className="section-head">
            <span className="mono idx">§ 01</span>
            <h2 className="display">In this order.</h2>
            <p>When two goals conflict, the higher one wins. Scale comes last, after correctness.</p>
          </div>
          <div className="priorities">
            <ol className="prio-list">
              {PRIORITIES.map((p, i) => (
                <li key={p}>
                  <span className="mono">{String(i + 1).padStart(2, "0")}</span>
                  {p}
                </li>
              ))}
            </ol>
            <div className="rules">
              {RULES.map(([t, d]) => (
                <div key={t} className="rule panel">
                  <Corners />
                  <b className="mono">{t}</b>
                  <p>{d}</p>
                </div>
              ))}
              <blockquote className="rule-quote display">An attractive animation is not evidence that a mechanism works.</blockquote>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="section-head">
            <span className="mono idx">§ 02</span>
            <h2 className="display">From the blog.</h2>
            <p>
              Engineering notes on the decisions, one record at a time. <a href="/blog">All posts →</a>
            </p>
          </div>
          <div className="blog-grid home-posts">
            {latestPosts(3).map((p) => (
              <PostCard key={p.slug} post={p} />
            ))}
          </div>
        </section>

        <section className="section" id="decisions">
          <div className="section-head">
            <span className="mono idx">§ 03</span>
            <h2 className="display">The decision log.</h2>
            <p>
              Append-only. A decision changes only through a new record that names what it supersedes. Read straight from{" "}
              <a href={`${GH_BLOB}/docs/decisions/README.md`}>docs/decisions</a> at build time.
            </p>
          </div>
          <div className="log panel">
            <Corners />
            <div className="log-head mono">
              <span>ID</span>
              <span>Title</span>
              <span>Status</span>
              <span>Recorded</span>
            </div>
            {recent.map((d) => (
              <a key={d.id} className="log-row" href={`${GH_BLOB}/docs/decisions/${d.file}`}>
                <b className="mono">{d.id}</b>
                <span>{d.title}</span>
                <span className="mono log-status">{d.status}</span>
                <span className="mono log-date">{d.recorded}</span>
              </a>
            ))}
            <a className="log-more mono" href={`${GH_BLOB}/docs/decisions/README.md`}>
              Full index · {DECISIONS.length} records since {DECISIONS[0]?.id}, Q1–Q30 by reference ↗
            </a>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
