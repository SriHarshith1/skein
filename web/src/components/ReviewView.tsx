"use client";

import { useEffect, useState } from "react";
import type { UIBlock } from "@/lib/agent/blocks";
import { api, type Bundle } from "./client";
import { SuggestionBlock } from "./Blocks";
import { Empty } from "./ui";

type Suggestion = Extract<UIBlock, { type: "suggestion" }>["suggestion"] & { origin: string; created_at: string };
type Rev = { id: number; table_name: string; op: string; actor: string | null; created_at: string; label: string | null };

export function ReviewView({ bundle, version, onChanged }: { bundle: Bundle; version: number; onChanged: () => void }) {
  const slug = bundle.game.slug;
  const [items, setItems] = useState<Suggestion[] | null>(null);
  const [revs, setRevs] = useState<Rev[]>([]);
  useEffect(() => {
    api<Suggestion[]>(`/api/games/${slug}/suggestions`).then(setItems).catch(() => setItems([]));
    api<Rev[]>(`/api/games/${slug}/history`).then(setRevs).catch(() => setRevs([]));
  }, [slug, version]);

  return (
    <div className="grid gap-8 lg:grid-cols-[1fr_340px]">
      <section>
        <h2 className="font-display text-xl font-bold">Proposed edits</h2>
        <p className="mb-4 text-sm text-dim">
          The Scout subagent and <code className="font-mono">npm run extract</code> propose facts from the wiki. Nothing joins the timeline until you add it.
        </p>
        {items === null ? null : items.length === 0 ? (
          <Empty title="Nothing to review">Ask the Scout to research something, or run the extractor after scraping.</Empty>
        ) : (
          <div className="space-y-3">
            {items.map((s) => (
              <div key={s.id}>
                <p className="mb-1 font-mono text-[10px] uppercase text-dim">from {s.origin} · {new Date(s.created_at).toLocaleDateString()}</p>
                <SuggestionBlock s={s} slug={slug} onChanged={onChanged} />
              </div>
            ))}
          </div>
        )}
      </section>
      <section>
        <h2 className="font-display text-xl font-bold">Recent edits</h2>
        <p className="mb-4 text-sm text-dim">Every change is kept with who made it.</p>
        {revs.length === 0 ? (
          <p className="text-sm text-dim">No edits since the seed data was loaded.</p>
        ) : (
          <ul className="space-y-2 text-sm">
            {revs.map((r) => (
              <li key={r.id} className="border-b border-line/60 pb-2">
                <b>{r.actor ?? "unknown"}</b> {r.op === "INSERT" ? "added" : r.op === "DELETE" ? "deleted" : "edited"}{" "}
                {r.table_name.replace(/s$/, "").replace("entitie", "entity")} <span className="text-chalk/80">{r.label}</span>
                <span className="block font-mono text-[11px] text-dim">{new Date(r.created_at).toLocaleString()}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
