import { useEffect, useState, type ReactNode } from "react";
import { DECISIONS, REGISTER } from "../generated/records";
import { GH, GH_BLOB, PORTFOLIO } from "../lib/site";
import { KLogo } from "./KLogo";

export type Page = "home" | "blog" | "docs";

const LINKS: [string, string, Page | null][] = [
  ["Principles", "/#principles", null],
  ["Refusals", "/#refusals", null],
  ["Decision log", "/#decisions", null],
  ["Docs", "/docs", "docs"],
  ["Blog", "/blog", "blog"],
  ["Records", `${GH}/tree/main/docs`, null],
];

function GitHubMark() {
  return (
    <svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true">
      <path
        fill="currentColor"
        d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"
      />
    </svg>
  );
}

const STARS_KEY = "kinigami:stars";

/** GitHub mark with the repo's star count, fetched once per session. */
function GitHubLink() {
  const [stars, setStars] = useState<number | null>(() => {
    try {
      const v = sessionStorage.getItem(STARS_KEY);
      return v ? Number(v) : null;
    } catch {
      return null;
    }
  });
  useEffect(() => {
    if (stars !== null) return;
    const ctl = new AbortController();
    fetch("https://api.github.com/repos/404khai/kinigami", { signal: ctl.signal })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (typeof d?.stargazers_count !== "number") return;
        setStars(d.stargazers_count);
        try {
          sessionStorage.setItem(STARS_KEY, String(d.stargazers_count));
        } catch {
          // storage blocked: the count just isn't cached
        }
      })
      .catch(() => {});
    return () => ctl.abort();
  }, [stars]);
  return (
    <a className="gh-link" href={GH} aria-label={stars === null ? "Kinigami on GitHub" : `Kinigami on GitHub, ${stars} stars`}>
      <GitHubMark />
      {stars !== null && <span className="gh-stars">★ {stars}</span>}
    </a>
  );
}

export function Nav({ current }: { current: Page }) {
  const [open, setOpen] = useState(false);
  return (
    <header className="nav">
      <a className="brand" href="/" aria-label="Kinigami home">
        <KLogo className="klogo brand-logo" title="" />
        <span>kinigami</span>
      </a>
      <nav className={`nav-links${open ? " open" : ""}`} id="nav-links" aria-label="Primary">
        {LINKS.map(([label, href, page]) => (
          <a key={label} href={href} aria-current={page === current ? "page" : undefined} onClick={() => setOpen(false)}>
            {label}
          </a>
        ))}
      </nav>
      <div className="nav-actions">
        <GitHubLink />
        <a className="btn btn-dark btn-sm" href="/blog">Read the blog →</a>
      </div>
      <button className="nav-toggle" aria-expanded={open} aria-controls="nav-links" aria-label="Menu" onClick={() => setOpen((o) => !o)}>
        <span />
        <span />
      </button>
    </header>
  );
}

export const CLONE = "git clone https://github.com/404khai/kinigami && cd kinigami && tools/zig build test";

/** A shell command in a dark box with a copy button. */
export function CopyCommand({ command }: { command: string }) {
  const [copied, setCopied] = useState(false);
  useEffect(() => {
    if (!copied) return;
    const t = setTimeout(() => setCopied(false), 1600);
    return () => clearTimeout(t);
  }, [copied]);
  return (
    <div className="copy-box">
      <code>
        <span className="prompt">$</span> {command}
      </code>
      <button
        type="button"
        aria-label="Copy command"
        onClick={async () => {
          try {
            await navigator.clipboard.writeText(command);
            setCopied(true);
          } catch {
            setCopied(false);
          }
        }}
      >
        {copied ? "copied" : "copy"}
      </button>
    </div>
  );
}

/** Colour blocks, halftone and coordinate tags around the edges; content on the dark field. */
export function Poster({ layout, children }: { layout: "footer" | "card"; children: ReactNode }) {
  const last = DECISIONS[DECISIONS.length - 1];
  return (
    <div className={`poster poster-${layout}`}>
      <div className="poster-blocks" aria-hidden="true">
        <i className="pb pb1" />
        <i className="pb pb2" />
        <i className="pb pb3" />
        <i className="pb pb4" />
        <i className="pb pb5" />
        <i className="pb pb6" />
        <span className="halftone h1" />
        <span className="halftone h2" />
        <span className="coord c1"><b>K01</b><em>LOG</em><em>{last?.id}</em></span>
        <span className="coord c2"><b>FIG</b><em>M / V</em><em>{REGISTER.length} SEALED</em></span>
      </div>
      <div className="poster-content">{children}</div>
    </div>
  );
}

const COLUMNS: { title: string; links: [string, string][] }[] = [
  { title: "Site", links: [["Overview", "/"], ["Docs", "/docs"], ["Brand", "/docs#brand"], ["Blog", "/blog"], ["Decision log", "/#decisions"], ["Principles", "/#principles"]] },
  {
    title: "Records",
    links: [
      ["Decisions", `${GH_BLOB}/docs/decisions/README.md`],
      ["Requirements", `${GH_BLOB}/docs/requirements/README.md`],
      ["Criteria register", `${GH_BLOB}/criteria/REGISTER.md`],
      ["Traceability", `${GH_BLOB}/docs/traceability.md`],
    ],
  },
  { title: "Community", links: [["GitHub", GH], ["Issues", `${GH}/issues`], ["404khai", PORTFOLIO]] },
];

export function Footer() {
  return (
    <footer className="footer">
      <Poster layout="footer">
        <div className="footer-links">
          <p className="footer-tag">
            Kinetic origami,
            <br />
            checked by physics.
          </p>
          {COLUMNS.map((c) => (
            <div key={c.title}>
              <span>{c.title}</span>
              {c.links.map(([label, href]) => (
                <a key={label} href={href}>{label}</a>
              ))}
            </div>
          ))}
        </div>
        <div className="wordmark">
          <KLogo className="klogo wordmark-logo" title="" />
          <span aria-hidden="true">kinigami</span>
        </div>
        <div className="footer-bar">
          <div className="footer-meta">
            <span>
              © 2026 built by <a className="footer-author" href={PORTFOLIO}>404khai</a>
            </span>
            <span>Zig · std only</span>
          </div>
          <div className="badges">
            <span className="badge-box"><i className="blocks" aria-hidden="true"><b /><b /><b /></i> {DECISIONS.length} decisions on record</span>
            <span className="badge-box">Deterministic · full 3D only</span>
          </div>
        </div>
      </Poster>
    </footer>
  );
}
