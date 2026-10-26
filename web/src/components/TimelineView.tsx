"use client";

import { useMemo, useState } from "react";
import type { Bundle, LoreEvent } from "./client";
import { EventEditor } from "./Editors";
import { ThreadTimeline, type ThreadLane } from "./ThreadTimeline";
import { Button, Empty } from "./ui";
import { STATIC } from "@/lib/static";

export function TimelineView({ bundle, reload }: { bundle: Bundle; reload: () => void }) {
  const [hidden, setHidden] = useState<Set<string>>(new Set());
  const [who, setWho] = useState("");
  const [q, setQ] = useState("");
  const [minImp, setMinImp] = useState(1);
  const [editing, setEditing] = useState<LoreEvent | "new" | null>(null);

  const lanes: ThreadLane[] = useMemo(
    () => bundle.timelines.map((t) => ({
      key: t.id, name: t.name, color: t.color ?? "#d9c9a3", kind: t.kind, parentKey: t.parent_id,
    })),
    [bundle.timelines],
  );
  const names = useMemo(() => new Map(bundle.entities.map((e) => [e.id, e.name])), [bundle.entities]);
  const needle = q.trim().toLowerCase();
  const events = bundle.events
    .filter((e) => !hidden.has(e.timeline_id) && e.importance >= minImp)
    .filter((e) => !who || e.participants.some((p) => p.entity_id === who))
    .filter((e) => !needle || `${e.title} ${e.summary ?? ""}`.toLowerCase().includes(needle))
    .map((e) => ({ ...e, lane: e.timeline_id, participants: e.participants.map((p) => names.get(p.entity_id) ?? "?") }));
  const counts = new Map<string, number>();
  bundle.events.forEach((e) => counts.set(e.timeline_id, (counts.get(e.timeline_id) ?? 0) + 1));

  return (
    <div className="grid gap-6 lg:grid-cols-[240px_1fr]">
      <aside className="space-y-5 lg:sticky lg:top-20 lg:self-start">
        <div>
          <h3 className="mb-2 tag">Timelines</h3>
          <ul className="space-y-1">
            {bundle.timelines.map((t) => (
              <li key={t.id}>
                <label className="flex cursor-pointer items-start gap-2 text-sm">
                  <input type="checkbox" className="mt-1 accent-madder" checked={!hidden.has(t.id)}
                    onChange={() => setHidden((h) => { const n = new Set(h); if (n.has(t.id)) n.delete(t.id); else n.add(t.id); return n; })} />
                  <span className="mt-1.5 inline-block h-2.5 w-2.5 shrink-0 rounded-full" style={{ background: t.color ?? "#d9c9a3" }} />
                  <span>
                    {t.name} <span className="font-mono text-[10px] text-dim">{counts.get(t.id) ?? 0}</span>
                    <span className="block font-mono text-[10px] uppercase text-dim">{t.kind}</span>
                  </span>
                </label>
              </li>
            ))}
          </ul>
        </div>
        <label className="block space-y-1">
          <span className="tag">Character</span>
          <select className="field" value={who} onChange={(e) => setWho(e.target.value)}>
            <option value="">Everyone</option>
            {bundle.entities.filter((e) => bundle.events.some((ev) => ev.participants.some((p) => p.entity_id === e.id)))
              .map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
          </select>
        </label>
        <label className="block space-y-1">
          <span className="tag">Search events</span>
          <input className="field" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Timestream, Rune Wars…" />
        </label>
        <label className="block space-y-1">
          <span className="tag">Only importance {minImp}+</span>
          <input type="range" min={1} max={5} value={minImp} onChange={(e) => setMinImp(Number(e.target.value))} className="w-full accent-madder" />
        </label>
        {!STATIC && <Button kind="primary" onClick={() => setEditing("new")}>Add event</Button>}
      </aside>
      <div>
        <p className="mb-4 text-sm text-dim">
          {events.length} of {bundle.events.length} events. Bigger knots matter more. A cord that curves off another is a branch; a loose loop starts a separate continuity.
        </p>
        {events.length ? (
          <ThreadTimeline events={events} lanes={lanes} onSelect={STATIC ? undefined : (id) => setEditing(bundle.events.find((e) => e.id === id) ?? null)}
            selectedId={editing && editing !== "new" ? editing.id : null} />
        ) : (
          <Empty title="No events match these filters">Clear the search or turn timelines back on.</Empty>
        )}
      </div>
      {editing && (
        <EventEditor key={editing === "new" ? "new" : editing.id} bundle={bundle} event={editing === "new" ? null : editing}
          onClose={() => setEditing(null)} onSaved={reload} />
      )}
    </div>
  );
}
