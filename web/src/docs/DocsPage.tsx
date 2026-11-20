import { useEffect, useRef, useState, type ReactNode } from "react";
import { ScrollIndicator } from "../blog/ScrollIndicator";
import { DitherOrigami, type Creature } from "../components/DitherOrigami";
import { KLogo } from "../components/KLogo";
import { PaperOrigami } from "../components/PaperOrigami";
import { Footer, Nav } from "../components/SiteChrome";
import { GH_BLOB } from "../lib/site";
import type { ShapeKind } from "../lib/origami";
import "./docs.css";

type Section = { id: string; title: string; body: ReactNode };
type DocPage = { id: string; title: string; summary: string; sections: Section[] };

const SWATCHES: [string, string, string][] = [
  ["Ground", "#ECEBE4", "Page background: warm paper grey"],
  ["Panel", "#F5F4EE", "Cards, code chips, quiet fills"],
  ["Ink", "#111015", "Text, dark sections, terminals"],
  ["Violet", "#5B3DF5", "The accent and the mark: links, actions, one word per headline"],
  ["Deep violet", "#24157A", "The paper's back in the fold, dark violet fields"],
  ["Chartreuse", "#D4FF4F", "Highlights on dark, the decision pill, the newest row"],
  ["Origami orange", "#FF6A2A", "Creatures and offset shadows. Sparingly"],
  ["Origami red", "#E63B2E", "Creatures; denials in UI (evaluator only)"],
  ["Origami yellow", "#F2B300", "Creatures, poster blocks"],
];

const PAPER: { kind: ShapeKind; color: string; name: string; tilt?: number }[] = [
  { kind: "crane", color: "#ff6a2a", name: "Crane" },
  { kind: "rocket", color: "#f2b300", name: "Rocket", tilt: 0.08 },
  { kind: "boat", color: "#5b3df5", name: "Boat" },
  { kind: "plane", color: "#3d6bff", name: "Plane", tilt: -0.1 },
  { kind: "tulip", color: "#e63b2e", name: "Tulip" },
  { kind: "heart", color: "#ff4f8b", name: "Heart" },
];

const D_GROUND: Creature[] = [
  { kind: "crane", x: 0.3, y: 0.55, size: 0.36, ink: "#ff6a2a", tilt: -0.08 },
  { kind: "rocket", x: 0.75, y: 0.52, size: 0.38, ink: "#f2b300" },
];
const D_VIOLET: Creature[] = [{ kind: "plane", x: 0.5, y: 0.5, size: 0.4, ink: "#d4ff4f", tilt: -0.12 }];
const D_INK: Creature[] = [
  { kind: "tulip", x: 0.35, y: 0.5, size: 0.38, ink: "#e63b2e" },
  { kind: "heart", x: 0.72, y: 0.45, size: 0.22, ink: "#ff4f8b", tilt: 0.15 },
];

/** Scrub or play the fold from K to crane. */
function FoldDemo() {
  const [p, setP] = useState(0);
  const raf = useRef(0);
  const play = () => {
    cancelAnimationFrame(raf.current);
    const from = p;
    const to = p < 0.5 ? 1 : 0;
    const start = performance.now();
    const step = (now: number) => {
      const k = Math.min(1, (now - start) / 1400);
      setP(from + (to - from) * k);
      if (k < 1) raf.current = requestAnimationFrame(step);
    };
    raf.current = requestAnimationFrame(step);
  };
  useEffect(() => () => cancelAnimationFrame(raf.current), []);
  return (
    <div className="fold-demo">
      <div className="fold-stage">
        <KLogo className="klogo fold-mark" title={p < 0.5 ? "Kinigami K" : "Kinigami crane"} fold={p} />
      </div>
      <div className="fold-controls">
        <span className="mono">K</span>
        <input type="range" min={0} max={1000} value={Math.round(p * 1000)} onChange={(e) => setP(Number(e.target.value) / 1000)} aria-label="Fold progress, K to crane" />
        <span className="mono">Crane</span>
        <button type="button" className="btn btn-violet btn-sm" onClick={play}>
          {p < 0.5 ? "Fold into a crane" : "Unfold to the K"}
        </button>
      </div>
      <ol className="fold-steps mono">
        <li><b>01</b> Upper arm lifts into the wing</li>
        <li><b>02</b> Lower arm turns up into neck and head</li>
        <li><b>03</b> Stem settles into body and tail</li>
      </ol>
    </div>
  );
}

const BRAND: DocPage = {
  id: "brand",
  title: "Brand guidelines",
  summary: "The folding K, the palette, the type, and two ways of drawing origami: paper-cut and dither. Everything here is a rule you can check, like the rest of the project.",
  sections: [
    {
      id: "name",
      title: "Name",
      body: (
        <>
          <p>
            <b>Kinigami</b> is kinetic origami: small units that move, connect and articulate together. The wordmark is always lowercase,{" "}
            <code>kinigami</code>; in prose it is Kinigami. One unit is a <b>Kin</b>, several are <b>Kins</b>.
          </p>
          <ul className="brand-rules">
            <li><b>Never</b> call a Kin a "microbot", or describe it in a way that borrows another robot's identity. The project's design must be its own (AGENTS.md).</li>
            <li><b>Never</b> say a mechanism "works" in brand copy unless a result labelled <code>validated_acceptance</code> says so.</li>
          </ul>
        </>
      ),
    },
    {
      id: "mark",
      title: "The mark",
      body: (
        <>
          <p>
            The K is a sheet of paper with three pieces: a notched stem and two arms. On load the arms unfold out from behind the stem, showing
            the darker back of the sheet mid-fold. On hover the same three pieces refold into a <b>crane</b>: the upper arm lifts into the wing,
            the lower arm turns up into the neck, and the stem settles into the body and tail. Nothing is added or cut; every piece keeps its
            corners.
          </p>
          <p>
            Why a crane: it is the first model most people fold, so it reads at a glance, and turning three creases into a recognisable animal
            is the project in one gesture. Simple parts, a declared sequence, a shape you can check.
          </p>
          <FoldDemo />
          <div className="brand-marks">
            <div className="on-ground"><KLogo title="" fold={0} /></div>
            <div className="on-lime"><KLogo title="" fold={0} /></div>
            <div className="on-violet"><KLogo title="" fold={0} tone="paper" /></div>
            <div className="on-ink"><KLogo title="" fold={1} /></div>
          </div>
          <div className="clear-space">
            <div className="cs-box">
              <KLogo title="" fold={0} />
              <i className="cs-pad" aria-hidden="true" />
            </div>
            <ul className="brand-rules">
              <li><b>Clear space</b> is the stem's width (28% of the mark) on every side.</li>
              <li><b>Minimum size</b> is 16 px. Below 24 px, use the K only, never the crane.</li>
              <li><b>Grounds:</b> violet K on ground, panel, chartreuse or ink; paper-white K on violet.</li>
              <li><b>Motion:</b> the fold takes 0.9–1.4 s, eased in and out, staggered wing → neck → body. It plays on hover and holds still under reduced motion.</li>
              <li><b>Don't</b> rotate, outline, gradient-fill or add pieces to the mark, or fold it into anything but the crane.</li>
            </ul>
          </div>
        </>
      ),
    },
    {
      id: "colour",
      title: "Colour",
      body: (
        <>
          <p>
            Warm paper ground, ink for text, and one violet. Chartreuse is the highlighter. The origami colours belong to the creatures and to
            poster blocks, not to interface text. If a screen has more than one strong colour moment, remove one.
          </p>
          <div className="brand-swatches">
            {SWATCHES.map(([name, hex, use]) => (
              <div key={hex} className="brand-swatch">
                <i style={{ background: hex }} />
                <b>{name}</b>
                <code>{hex}</code>
                <span>{use}</span>
              </div>
            ))}
          </div>
        </>
      ),
    },
    {
      id: "type",
      title: "Type",
      body: (
        <div className="brand-type">
          <div>
            <span className="eyebrow">Display · Bricolage Grotesque 650–800</span>
            <p className="bt-display">Small machines. Honest <em>physics.</em></p>
          </div>
          <div>
            <span className="eyebrow">Text and labels · JetBrains Mono 400</span>
            <p className="bt-mono">A deterministic, physically grounded swarm simulation in Zig. Nothing is claimed until a preregistered criterion says so.</p>
          </div>
          <div>
            <span className="eyebrow">Eyebrows · JetBrains Mono, 0.12em, uppercase, violet</span>
            <p className="bt-eyebrow">[01] What Kinigami refuses to fake</p>
          </div>
          <ul className="brand-rules">
            <li><b>Headlines</b> are short and declarative, with letter-spacing −0.04 to −0.05em. One word may take the violet.</li>
            <li><b>Numbers, IDs and hashes</b> (Q84, 05c3d2ec…) are always set in mono.</li>
          </ul>
        </div>
      ),
    },
    {
      id: "origami",
      title: "Origami illustration",
      body: (
        <>
          <p>
            The illustration style is <b>paper-cut</b>. Every creature is built from flat facets, the way a folded model is. Each facet takes
            one tone of a single hue, lighter where it faces the light. Creases are thin paper-white lines. A hard shadow sits down and to the
            right, and a fine grain sits on top.
          </p>
          <div className="paper-gallery">
            {PAPER.map((c) => (
              <figure key={c.kind}>
                <PaperOrigami kind={c.kind} color={c.color} tilt={c.tilt} title={`Origami ${c.name.toLowerCase()}`} />
                <figcaption className="mono">{c.name} · <code>{c.color}</code></figcaption>
              </figure>
            ))}
          </div>
          <div className="paper-diagram">
            <PaperOrigami kind="crane" color="#5b3df5" diagram />
            <div>
              <span className="eyebrow">Instruction marks</span>
              <p>
                For explainers, add the marks of a folding diagram: a dashed valley-fold line along the next hinge and a curved arrow showing
                which way the paper goes. The marks are ink at 70%; never more than one fold per figure.
              </p>
            </div>
          </div>
          <ul className="brand-rules">
            <li><b>Shapes:</b> crane, rocket, boat, plane, tulip and heart. New shapes are faceted the same way: 2–8 facets, one hue.</li>
            <li><b>Never</b> draw a Kin. No candidate geometry is selected (Q38), so an illustrated Kin would be an invented design. Creatures are paper, not robots.</li>
            <li><b>Shadow</b> offset is 3% of the figure, down and right, in ink at 12%.</li>
          </ul>
        </>
      ),
    },
    {
      id: "dither",
      title: "Dither",
      body: (
        <>
          <p>
            The same creatures, printed as an ordered (Bayer 8×8) dither of square dots, each in its own ink. They unfold facet by facet when
            they enter the screen, bob gently, and pause off screen. Use dither as a field behind a section; use paper-cut when a figure
            has to explain something.
          </p>
          <div className="brand-dithers">
            <figure>
              <div className="bd-tile bd-ground"><DitherOrigami creatures={D_GROUND} light={0.2} /></div>
              <figcaption className="mono">On ground · 4 px pitch · hero</figcaption>
            </figure>
            <figure>
              <div className="bd-tile bd-violet"><DitherOrigami creatures={D_VIOLET} cell={5} light={0.1} /></div>
              <figcaption className="mono">On violet · chartreuse ink · 5 px</figcaption>
            </figure>
            <figure>
              <div className="bd-tile bd-ink"><DitherOrigami creatures={D_INK} cell={3} light={0.15} /></div>
              <figcaption className="mono">On ink · fine pitch · 3 px</figcaption>
            </figure>
          </div>
          <ul className="brand-rules">
            <li><b>Pitch:</b> 3 px for small tiles, 4 px for sections, 5 px for dark fields.</li>
            <li><b>Quiet area:</b> clear an ellipse behind any text; never print dots under body copy.</li>
            <li><b>Motion</b> stops off screen and under reduced motion.</li>
          </ul>
        </>
      ),
    },
    {
      id: "voice",
      title: "Voice",
      body: (
        <>
          <p>Plain, exact, and honest about what is not done yet. The records set the tone: say what was run, what it showed, and what it does not show.</p>
          <div className="voice-grid">
            <div className="voice-do">
              <span className="mono">Say</span>
              <p>"Run 2 passes 10 of 10 checks, in the fixture envelope only."</p>
              <p>"No candidate survives Gate 1."</p>
              <p>"This value is provisional."</p>
            </div>
            <div className="voice-dont">
              <span className="mono">Don't say</span>
              <p>"Our robots self-assemble."</p>
              <p>"Physically accurate." (accurate where, to what tolerance?)</p>
              <p>Any number that is not in a record.</p>
            </div>
          </div>
          <p>
            The result labels are part of the voice: <code>exploratory</code>, <code>oracle</code>, <code>fixture</code>, <code>uncertain</code>{" "}
            and <code>validated_acceptance</code>. Planned, implemented, tested, validated, qualified and accepted are not interchangeable. See{" "}
            <a href={`${GH_BLOB}/AGENTS.md`}>AGENTS.md</a>.
          </p>
        </>
      ),
    },
  ],
};

const PAGES: DocPage[] = [BRAND];

function Overview({ go }: { go: (id: string) => void }) {
  return (
    <>
      <header className="doc-banner" data-section-index={0}>
        <div className="doc-banner-copy">
          <span className="eyebrow">Kinigami / Docs</span>
          <h1>Kinigami docs</h1>
          <p>
            How Kinigami looks and speaks. Engineering documentation lives with the code: the decision log, requirements, criteria and
            traceability are linked below and read straight from the repository.
          </p>
        </div>
        <div className="doc-banner-art" aria-hidden="true">
          <PaperOrigami kind="crane" color="#ff6a2a" className="dba-crane" tilt={-0.08} />
          <PaperOrigami kind="plane" color="#3d6bff" className="dba-plane" tilt={-0.2} />
          <PaperOrigami kind="boat" color="#5b3df5" className="dba-boat" />
        </div>
      </header>
      <section className="doc-section" data-section-index={1}>
        <span className="eyebrow">Start here</span>
        <div className="doc-grid">
          <button type="button" className="doc-tile" onClick={() => go("brand")}>
            <div className="doc-tile-stage stage-lime">
              <KLogo className="klogo tile-mark" title="" fold={1} />
            </div>
            <div className="doc-tile-copy">
              <b>Brand guidelines</b>
              <span>The folding mark, colour, type, paper-cut and dither origami, voice.</span>
            </div>
          </button>
          {[
            ["Decision log", "Append-only records. Decisions govern.", `${GH_BLOB}/docs/decisions/README.md`, "rocket", "#f2b300"],
            ["Requirements", "Current requirements with stable IDs and status.", `${GH_BLOB}/docs/requirements/README.md`, "tulip", "#e63b2e"],
            ["Criteria register", "Every criteria file, hashed before its run.", `${GH_BLOB}/criteria/REGISTER.md`, "heart", "#ff4f8b"],
            ["Traceability", "What is implemented, tested, validated and qualified.", `${GH_BLOB}/docs/traceability.md`, "boat", "#5b3df5"],
            ["Blog", "Engineering notes, one record at a time.", "/blog", "plane", "#3d6bff"],
          ].map(([title, body, href, kind, color]) => (
            <a key={title} className="doc-tile" href={href}>
              <div className="doc-tile-stage">
                <PaperOrigami kind={kind as ShapeKind} color={color} />
              </div>
              <div className="doc-tile-copy">
                <b>{title}{href.startsWith("http") ? " ↗" : ""}</b>
                <span>{body}</span>
              </div>
            </a>
          ))}
        </div>
      </section>
    </>
  );
}

function PageView({ page }: { page: DocPage }) {
  return (
    <>
      <header className="doc-page-head" data-section-index={0}>
        <div className="doc-page-art" aria-hidden="true">
          <KLogo className="klogo" title="" />
        </div>
        <span className="eyebrow">Kinigami / Docs</span>
        <h1>{page.title}</h1>
        <p>{page.summary}</p>
      </header>
      {page.sections.map((s, i) => (
        <section key={s.id} className="doc-section doc-prose" data-section-index={i + 1} id={s.id}>
          <h2>{s.title}</h2>
          {s.body}
        </section>
      ))}
    </>
  );
}

const ROUTES = ["overview", ...PAGES.map((p) => p.id)];
const fromHash = () => {
  const id = location.hash.slice(1).split("/")[0];
  return ROUTES.includes(id) ? id : "overview";
};

export function Docs() {
  const [route, setRoute] = useState(fromHash);
  useEffect(() => {
    const on = () => setRoute(fromHash());
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  const page = PAGES.find((p) => p.id === route);
  useEffect(() => {
    document.title = page ? `${page.title} · Kinigami docs` : "Kinigami docs";
    window.scrollTo(0, 0);
  }, [page]);
  const go = (id: string) => {
    location.hash = id;
  };
  const sections = page ? [{ id: "top", title: page.title }, ...page.sections.map((s) => ({ id: s.id, title: s.title }))] : [{ id: "top", title: "Overview" }, { id: "start", title: "Start here" }];
  const jump = (id: string) => document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  return (
    <div className="rails">
      <Nav current="docs" />
      <div className="docs">
        <aside className="docs-side">
          <span className="mono">Docs</span>
          <a href="#overview" aria-current={route === "overview" ? "page" : undefined}>Overview</a>
          {PAGES.map((p) => (
            <div key={p.id} className="docs-side-group">
              <a href={`#${p.id}`} aria-current={route === p.id ? "page" : undefined}>{p.title}</a>
              {route === p.id && (
                <div className="docs-side-sections">
                  {p.sections.map((s) => (
                    <button key={s.id} type="button" onClick={() => jump(s.id)}>{s.title}</button>
                  ))}
                </div>
              )}
            </div>
          ))}
          <span className="mono">Records</span>
          <a href={`${GH_BLOB}/docs/decisions/README.md`}>Decision log ↗</a>
          <a href={`${GH_BLOB}/docs/requirements/README.md`}>Requirements ↗</a>
          <a href={`${GH_BLOB}/criteria/REGISTER.md`}>Criteria register ↗</a>
          <a href="/blog">Blog</a>
        </aside>
        <main className="docs-main" key={route}>
          {page ? <PageView page={page} /> : <Overview go={go} />}
        </main>
        <aside className="docs-rail" aria-label="On this page">
          <ScrollIndicator sections={sections} />
        </aside>
      </div>
      <Footer />
    </div>
  );
}
