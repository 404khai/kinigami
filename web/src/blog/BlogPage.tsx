import { useEffect, useState, type ReactNode } from "react";
import { Footer, Nav } from "../components/SiteChrome";
import { figures, type FigureId } from "../generated/figures";
import { DECISIONS } from "../generated/records";
import { GH_BLOB } from "../lib/site";
import { AUTHOR, POSTS, postBySlug, readingMinutes, toMarkdown, type Block, type Post } from "./posts";
import { ScrollIndicator } from "./ScrollIndicator";
import "../generated/anatomy.css";
import "./blog.css";

const fmt = (iso: string) =>
  new Date(`${iso}T12:00:00Z`).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });

const byDate = () => [...POSTS].sort((a, b) => b.date.localeCompare(a.date));

/** `code`, **bold** and [text](href) inside a paragraph. */
function inline(text: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re = /`([^`]+)`|\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)]+)\)/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(text.slice(last, m.index));
    if (m[1]) out.push(<code key={m.index}>{m[1]}</code>);
    else if (m[2]) out.push(<b key={m.index}>{m[2]}</b>);
    else out.push(<a key={m.index} href={m[4]}>{m[3]}</a>);
    last = re.lastIndex;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

function Figure({ id }: { id: FigureId }) {
  return <div className="iso blog-figure" data-theme="light" dangerouslySetInnerHTML={{ __html: figures[id] }} />;
}

/** A drawing sheet: the figure on grid paper, a ruler along the top, the title in the corner. */
function Cover({ post, large }: { post: Post; large?: boolean }) {
  return (
    <div className={`blog-cover${large ? " large" : ""}`}>
      <div className="blog-cover-rule" aria-hidden="true" />
      <span className="blog-cover-sheet mono" aria-hidden="true">{post.decisions.join(" · ")}</span>
      <Figure id={post.figure} />
      <div className="blog-cover-title">
        <span>— {post.category}</span>
        <b>{post.cover}</b>
      </div>
    </div>
  );
}

function Meta({ post }: { post: Post }) {
  return (
    <div className="blog-meta">
      <span>{AUTHOR.name}</span>
      <i />
      <time dateTime={post.date}>{fmt(post.date)}</time>
      <i />
      <span>{readingMinutes(post)} min read</span>
    </div>
  );
}

export function PostCard({ post }: { post: Post }) {
  return (
    <a className="blog-card" href={`/blog/${post.slug}`}>
      <Cover post={post} />
      <span className="blog-cat mono">{post.category}</span>
      <h3 className="display">{post.title}</h3>
      <p>{post.summary}</p>
      <Meta post={post} />
    </a>
  );
}

export const latestPosts = (n: number) => byDate().slice(0, n);

function BlogIndex() {
  const [featured, ...rest] = byDate();
  useEffect(() => {
    document.title = "Blog · Kinigami";
  }, []);
  return (
    <main className="blog">
      <header className="blog-head">
        <span className="mono eyebrow">Engineering notes · {POSTS.length} posts</span>
        <h1 className="display">Kinigami Blog</h1>
        <p>
          The decisions behind Kinigami, one record at a time: why time is an integer, what a controller may know, how criteria are sealed before a run, and
          what happens when a design fails its gate. The decision log governs; every post links to the records it is written from.
        </p>
      </header>

      <a className="blog-featured" href={`/blog/${featured.slug}`}>
        <Cover post={featured} large />
        <div className="blog-featured-copy">
          <span className="blog-cat mono">{featured.category}</span>
          <h2 className="display">{featured.title}</h2>
          <p>{featured.summary}</p>
          <Meta post={featured} />
        </div>
      </a>

      <div className="blog-grid">
        {rest.map((p) => (
          <PostCard key={p.slug} post={p} />
        ))}
      </div>
    </main>
  );
}

function BlockView({ block, index }: { block: Block; index: number }) {
  if ("p" in block) return <p>{inline(block.p)}</p>;
  if ("h2" in block)
    return (
      <h2 className="display" id={block.h2.toLowerCase().replace(/\W+/g, "-")} data-section-index={index}>
        {block.h2}
      </h2>
    );
  if ("code" in block)
    return (
      <pre className="blog-code" data-lang={block.lang}>
        <code>{block.code}</code>
      </pre>
    );
  if ("figure" in block)
    return (
      <figure className="blog-fig">
        <Figure id={block.figure} />
        <figcaption>{block.caption}</figcaption>
      </figure>
    );
  if ("list" in block)
    return (
      <ul>
        {block.list.map((l) => (
          <li key={l}>{inline(l)}</li>
        ))}
      </ul>
    );
  return (
    <div className="blog-stats">
      {block.stats.map((s) => (
        <div key={s.label}>
          <b className="display">{s.value}</b>
          <span>{s.label}</span>
          {s.note && <small>{s.note}</small>}
        </div>
      ))}
    </div>
  );
}

async function copyText(text: string) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
}

function Ask({ post }: { post: Post }) {
  const [copied, setCopied] = useState(false);
  useEffect(() => {
    if (!copied) return;
    const t = setTimeout(() => setCopied(false), 1600);
    return () => clearTimeout(t);
  }, [copied]);
  const url = location.href;
  const q = encodeURIComponent(`Read ${url} and help me understand it.`);
  return (
    <div className="blog-ask mono">
      <span>Ask about this post</span>
      <a href={`https://claude.ai/new?q=${q}`} target="_blank" rel="noreferrer">
        <img src="/claude.svg" alt="" />Claude
      </a>
      <button type="button" onClick={async () => setCopied(await copyText(toMarkdown(post, url)))}>
        {copied ? "Copied" : "Copy as Markdown"}
      </button>
    </div>
  );
}

/** The decision records a post rests on, read from the log itself. */
function Governing({ post }: { post: Post }) {
  const rows = post.decisions.map((id) => DECISIONS.find((d) => d.id === id)).filter((d) => d !== undefined);
  return (
    <aside className="blog-governs">
      <span className="mono">Governing records</span>
      {rows.map((d) => (
        <a key={d.id} href={`${GH_BLOB}/docs/decisions/${d.file}`}>
          <b className="mono">{d.id}</b>
          <span>{d.title}</span>
          <small className="mono">{d.status} · {d.recorded}</small>
        </a>
      ))}
      <p>If this post and a record disagree, the record is right.</p>
    </aside>
  );
}

function PostView({ post }: { post: Post }) {
  useEffect(() => {
    document.title = `${post.title} · Kinigami blog`;
  }, [post]);
  // Section 0 is the top of the article; each h2 is the next section.
  let n = 0;
  const sections = [{ id: "intro", title: "Intro" }, ...post.body.flatMap((b) => ("h2" in b ? [{ id: b.h2, title: b.h2 }] : []))];
  const others = byDate().filter((p) => p.slug !== post.slug);
  return (
    <main className="blog blog-post">
      <article>
        <a className="blog-back mono" href="/blog">← All posts</a>
        <div className="blog-post-head" data-section-index={0}>
          <div className="blog-kicker mono">
            <span className="blog-cat">{post.category}</span>
            <span>· {fmt(post.date)} · {readingMinutes(post)} min read</span>
          </div>
          <h1 className="display">{post.title}</h1>
          <p className="blog-lede">{post.summary}</p>
          <a className="blog-author" href={AUTHOR.href}>
            <img src={AUTHOR.avatar} alt="" width="40" height="40" />
            <span>
              <b>{AUTHOR.name}</b>
              <small className="mono">{AUTHOR.handle}</small>
            </span>
          </a>
          <Ask post={post} />
        </div>
        <Cover post={post} large />
        <div className="blog-body">
          {post.body.map((b, i) => (
            <BlockView key={i} block={b} index={"h2" in b ? ++n : -1} />
          ))}
        </div>
        <Governing post={post} />
        <aside className="blog-sources">
          <b className="mono">Sources</b>
          {post.sources.map((s) => (
            <a key={s.href} href={s.href}>{s.label} ↗</a>
          ))}
        </aside>
        <div className="blog-more">
          <span className="blog-cat mono">Keep reading</span>
          {others.map((p) => (
            <a key={p.slug} href={`/blog/${p.slug}`}>
              <b className="display">{p.title}</b>
              <span className="mono">{fmt(p.date)}</span>
            </a>
          ))}
        </div>
      </article>
      <aside className="blog-rail" aria-label="On this page">
        <ScrollIndicator sections={sections} />
      </aside>
    </main>
  );
}

function NotFound({ slug }: { slug: string }) {
  return (
    <main className="blog blog-missing">
      <span className="mono eyebrow">404 · no such post</span>
      <h1 className="display">Nothing filed under “{slug}”.</h1>
      <a className="mono" href="/blog">← All posts</a>
    </main>
  );
}

export function Blog({ slug }: { slug?: string }) {
  const post = slug ? postBySlug(slug) : undefined;
  return (
    <div className="rails">
      <Nav current="blog" />
      {post ? <PostView post={post} /> : slug ? <NotFound slug={slug} /> : <BlogIndex />}
      <Footer />
    </div>
  );
}
