import { DECISIONS, REGISTER } from "../generated/records";
import { GH, GH_BLOB, PORTFOLIO } from "../lib/site";
import { Logo } from "./Logo";

export type Page = "home" | "blog";

function GitHubIcon() {
  return (
    <svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">
      <path
        fill="currentColor"
        d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"
      />
    </svg>
  );
}

export function Nav({ current }: { current: Page }) {
  const links: [string, string, Page | null][] = [
    ["Overview", "/", "home"],
    ["Blog", "/blog", "blog"],
    ["Decisions", `${GH}/tree/main/docs/decisions`, null],
    ["Requirements", `${GH}/tree/main/docs/requirements`, null],
  ];
  return (
    <header className="topbar">
      <a className="brand" href="/">
        <Logo />
        <span className="display wordmark">kinigami</span>
        <span className="mono crumb">/ {current === "home" ? "kinetic origami" : "blog"}</span>
      </a>
      <nav className="mono">
        {links.map(([label, href, page]) => (
          <a key={label} href={href} aria-current={page === current ? "page" : undefined}>
            {label}
          </a>
        ))}
      </nav>
      <div className="topbar-right">
        <span className="status mono">
          <i />
          Core · Zig std only
        </span>
        <a className="gh-link" href={GH} aria-label="Kinigami on GitHub">
          <GitHubIcon />
        </a>
      </div>
    </header>
  );
}

const last = DECISIONS[DECISIONS.length - 1]?.id;

const COLUMNS: { title: string; links: [string, string][] }[] = [
  { title: "Site", links: [["Overview", "/"], ["Blog", "/blog"], ["Decision log", "/#decisions"]] },
  {
    title: "Records",
    links: [
      ["Decisions", `${GH_BLOB}/docs/decisions/README.md`],
      ["Requirements", `${GH_BLOB}/docs/requirements/README.md`],
      ["Criteria register", `${GH_BLOB}/criteria/REGISTER.md`],
      ["Traceability", `${GH_BLOB}/docs/traceability.md`],
      ["Roadmap", `${GH_BLOB}/docs/roadmap.md`],
    ],
  },
  { title: "Community", links: [["GitHub", GH], ["Issues", `${GH}/issues`], ["404khai", PORTFOLIO]] },
];

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-links">
        <p className="footer-tag display">
          An attractive animation
          <br />
          is not evidence.
        </p>
        {COLUMNS.map((c) => (
          <div key={c.title}>
            <span className="mono">{c.title}</span>
            {c.links.map(([label, href]) => (
              <a key={label} href={href}>
                {label}
              </a>
            ))}
          </div>
        ))}
      </div>

      <div className="titleblock">
        <div className="tb-big display">kinigami</div>
        <dl className="tb-grid mono">
          <div><dt>Project</dt><dd>Kinetic origami</dd></div>
          <div><dt>Core</dt><dd>Zig · std only</dd></div>
          <div><dt>Time</dt><dd>Integer ticks</dd></div>
          <div><dt>Default label</dt><dd>exploratory</dd></div>
          <div><dt>Decisions</dt><dd>Q1–{last}</dd></div>
          <div><dt>Criteria</dt><dd>{REGISTER.length} registered</dd></div>
          <div><dt>Builder</dt><dd><a href={PORTFOLIO}>404khai ↗</a></dd></div>
          <div><dt>Source</dt><dd><a href={GH}>404khai/kinigami ↗</a></dd></div>
        </dl>
      </div>

      <div className="footer-bar mono">
        <span>
          © 2026 built by <a className="footer-author" href={PORTFOLIO}>404khai</a>
        </span>
        <span className="badges">
          <span className="badge-plain">Deterministic</span>
          <span className="badge-plain">Full 3D only</span>
          <span className="badge-plain">Criteria before results</span>
        </span>
      </div>
    </footer>
  );
}
