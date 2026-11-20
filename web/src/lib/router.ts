import { useEffect, useState } from 'react';

/** A tiny pathname router: no dependency, History API only. */
const listeners = new Set<() => void>();
const notify = () => listeners.forEach((l) => l());

if (typeof window !== 'undefined') window.addEventListener('popstate', notify);

export function usePath() {
  const [path, setPath] = useState(() => location.pathname);
  useEffect(() => {
    const on = () => setPath(location.pathname);
    listeners.add(on);
    return () => void listeners.delete(on);
  }, []);
  return path;
}

/** Navigate to an in-app URL ("/docs/json", "/#roster"), then scroll to its hash or the top. */
export function navigate(to: string) {
  const url = new URL(to, location.href);
  const samePage = url.pathname === location.pathname;
  if (samePage && url.hash) {
    history.pushState(null, '', url.pathname + url.hash);
  } else if (!samePage) {
    history.pushState(null, '', url.pathname + url.search + url.hash);
    notify();
  }
  requestAnimationFrame(() => {
    const el = url.hash && document.getElementById(decodeURIComponent(url.hash.slice(1)));
    if (el) el.scrollIntoView({ behavior: samePage ? 'smooth' : 'auto' });
    else if (!samePage) window.scrollTo(0, 0);
  });
}

/** Intercept clicks on internal links anywhere in the document. */
export function useLinkInterception() {
  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = (e.target as Element).closest?.('a');
      if (!a || a.target || a.hasAttribute('download')) return;
      const href = a.getAttribute('href');
      if (!href || !href.startsWith('/') || href.startsWith('//')) return;
      e.preventDefault();
      navigate(href);
    };
    document.addEventListener('click', onClick);
    return () => document.removeEventListener('click', onClick);
  }, []);
}
