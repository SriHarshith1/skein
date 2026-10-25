"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { loadBundle, type Bundle } from "./client";
import { AskView } from "./AskView";
import { RelationsView } from "./RelationsView";
import { ReviewView } from "./ReviewView";
import { TimelineView } from "./TimelineView";

const TABS = [
  { id: "timeline", label: "Timeline" },
  { id: "relations", label: "Relations" },
  { id: "ask", label: "Ask" },
  { id: "review", label: "Review" },
] as const;
type Tab = (typeof TABS)[number]["id"];

function stored(key: string) {
  try {
    return typeof window === "undefined" ? null : localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function GameApp({ slug }: { slug: string }) {
  const [bundle, setBundle] = useState<Bundle | null>(null);
  const [error, setError] = useState<string | null>(null);
  // The page shows a loading line until data arrives, so reading saved choices here
  // cannot cause a hydration mismatch.
  const [tab, setTab] = useState<Tab>(() => {
    const saved = stored("lore-tab");
    return TABS.some((t) => t.id === saved) ? (saved as Tab) : "timeline";
  });
  const [version, setVersion] = useState(0);
  const [actor, setActor] = useState(() => stored("lore-actor") || "editor");

  const reload = useCallback(() => {
    loadBundle(slug)
      .then((b) => {
        setBundle(b);
        setVersion((v) => v + 1);
      })
      .catch((e) => setError(e.message));
  }, [slug]);

  useEffect(() => {
    reload();
  }, [reload]);

  const choose = (t: Tab) => {
    setTab(t);
    try { localStorage.setItem("lore-tab", t); } catch {}
  };

  if (error) return <p className="p-8 text-danger">Could not load this game: {error}</p>;
  if (!bundle) return <p className="p-8 text-dim">Unwinding the skein…</p>;

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-30 border-b border-line bg-ink/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-x-6 gap-y-2 px-4 py-3">
          <Link href="/" className="font-display text-2xl font-extrabold uppercase text-dim hover:text-chalk">Skein</Link>
          <h1 className="font-display text-3xl font-extrabold uppercase">{bundle.game.name}</h1>
          <nav className="flex gap-1" aria-label="Views">
            {TABS.map((t) => (
              <button key={t.id} onClick={() => choose(t.id)} aria-current={tab === t.id}
                className={`px-3 py-2 font-mono text-[11px] uppercase tracking-wider ${tab === t.id ? "text-chalk shadow-[inset_0_-3px_0_var(--madder)]" : "text-dim hover:text-chalk"}`}>
                {t.label}
                {t.id === "review" && bundle.stats.pendingSuggestions > 0 && (
                  <span className="ml-1.5 rounded-full bg-madder px-1.5 font-mono text-[10px] text-ink">{bundle.stats.pendingSuggestions}</span>
                )}
              </button>
            ))}
          </nav>
          <label className="ml-auto flex items-center gap-2 text-xs text-dim">
            Editing as
            <input className="field w-28 py-1 text-xs" value={actor} onChange={(e) => {
              setActor(e.target.value);
              try { localStorage.setItem("lore-actor", e.target.value); } catch {}
            }} />
          </label>
        </div>
      </header>
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-6">
        {tab === "timeline" && <TimelineView bundle={bundle} reload={reload} />}
        {tab === "relations" && <RelationsView bundle={bundle} reload={reload} />}
        {/* Ask stays mounted so the conversation survives tab switches. */}
        <div hidden={tab !== "ask"}><AskView bundle={bundle} onChanged={reload} /></div>
        {tab === "review" && <ReviewView bundle={bundle} version={version} onChanged={reload} />}
      </main>
      <footer className="border-t border-line px-4 py-3 text-center text-xs text-dim">
        {bundle.events.length} events · {bundle.entities.length} entities · {bundle.relationships.length} relationships ·{" "}
        {bundle.stats.chunks} wiki passages · {bundle.sources.length} sources
        {bundle.game.wiki_license && <> · wiki text {bundle.game.wiki_license}</>}
      </footer>
    </div>
  );
}
