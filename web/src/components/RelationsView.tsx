"use client";

import { useMemo, useState } from "react";
import type { Bundle, Entity, Relationship } from "./client";
import { RELATION_COLORS } from "./client";
import { EntityEditor, RelationEditor } from "./Editors";
import { RelationGraph } from "./RelationGraph";
import { Button, Chip, Empty } from "./ui";
import { STATIC } from "@/lib/static";

// Ego graph around one character, filtered to one timeline (null-timeline bonds hold everywhere).
export function RelationsView({ bundle, reload, initialFocus }: { bundle: Bundle; reload: () => void; initialFocus?: string }) {
  const characters = bundle.entities;
  const degree = useMemo(() => {
    const d = new Map<string, number>();
    bundle.relationships.forEach((r) => {
      d.set(r.source_id, (d.get(r.source_id) ?? 0) + 1);
      d.set(r.target_id, (d.get(r.target_id) ?? 0) + 1);
    });
    return d;
  }, [bundle.relationships]);
  const busiest = [...characters].sort((a, b) => (degree.get(b.id) ?? 0) - (degree.get(a.id) ?? 0))[0];
  const [focus, setFocus] = useState(initialFocus ?? busiest?.id ?? "");
  const [timeline, setTimeline] = useState("");
  const [depth, setDepth] = useState(1);
  const [editRel, setEditRel] = useState<Relationship | "new" | null>(null);
  const [editEnt, setEditEnt] = useState<Entity | "new" | null>(null);

  const visible = (r: Relationship) => !timeline || !r.timeline_id || r.timeline_id === timeline || r.kind === "variant";
  const { nodes, edges } = useMemo(() => {
    const seen = new Set([focus]);
    let frontier = [focus];
    const picked = new Map<string, Relationship>();
    for (let d = 0; d < depth; d++) {
      const next: string[] = [];
      for (const r of bundle.relationships) {
        if (!visible(r) || !(frontier.includes(r.source_id) || frontier.includes(r.target_id))) continue;
        picked.set(r.id, r);
        for (const id of [r.source_id, r.target_id]) if (!seen.has(id)) { seen.add(id); next.push(id); }
      }
      frontier = next;
    }
    const tl = new Map(bundle.timelines.map((t) => [t.id, t.slug]));
    return {
      nodes: bundle.entities.filter((e) => seen.has(e.id)).map((e) => ({ id: e.id, name: e.name, kind: e.kind, timeline: e.timeline_id ? tl.get(e.timeline_id) ?? null : null })),
      edges: [...picked.values()].map((r) => ({ id: r.id, source: r.source_id, target: r.target_id, kind: r.kind, description: r.description })),
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bundle, focus, timeline, depth]);

  const me = bundle.entities.find((e) => e.id === focus);
  const names = new Map(bundle.entities.map((e) => [e.id, e.name]));
  const mine = edges.filter((e) => e.source === focus || e.target === focus);

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <div className="space-y-3">
        <div className="flex flex-wrap items-end gap-3">
          <label className="space-y-1">
            <span className="block tag">Character</span>
            <select className="field min-w-56" value={focus} onChange={(e) => setFocus(e.target.value)}>
              {[...characters].sort((a, b) => a.name.localeCompare(b.name)).map((c) => (
                <option key={c.id} value={c.id}>{c.name} ({degree.get(c.id) ?? 0})</option>
              ))}
            </select>
          </label>
          <label className="space-y-1">
            <span className="block tag">Timeline</span>
            <select className="field" value={timeline} onChange={(e) => setTimeline(e.target.value)}>
              <option value="">All timelines</option>
              {bundle.timelines.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
          </label>
          <label className="space-y-1">
            <span className="block tag">Reach</span>
            <select className="field" value={depth} onChange={(e) => setDepth(Number(e.target.value))}>
              <option value={1}>Direct bonds</option>
              <option value={2}>Two steps out</option>
            </select>
          </label>
          {!STATIC && <Button kind="primary" onClick={() => setEditRel("new")}>Add relationship</Button>}
          {!STATIC && <Button onClick={() => setEditEnt("new")}>Add character</Button>}
        </div>
        {edges.length ? (
          <RelationGraph nodes={nodes} edges={edges} focusId={focus} height={600}
            onNodeClick={(id) => setFocus(id)}
            onEdgeClick={STATIC ? undefined : (id) => setEditRel(bundle.relationships.find((r) => r.id === id) ?? null)} />
        ) : (
          <Empty title="No relationships here yet">Pick another timeline, or add the first relationship for this character.</Empty>
        )}
        <div className="flex flex-wrap gap-2 text-xs">
          {Object.entries(RELATION_COLORS).map(([k, c]) => <span key={k} style={{ color: c }} className="font-mono">— {k}</span>)}
        </div>
      </div>
      {me && (
        <aside className="space-y-3 rounded-[3px] border border-line bg-panel p-4 lg:self-start">
          <div className="flex items-start justify-between gap-2">
            <h3 className="font-display text-xl font-bold">{me.name}</h3>
            {!STATIC && <Button onClick={() => setEditEnt(me)}>Edit</Button>}
          </div>
          {me.variant_of && <p className="text-xs text-dim">Variant of {names.get(me.variant_of)}</p>}
          {me.aliases.length > 0 && <p className="text-xs text-dim">Also known as {me.aliases.join(", ")}</p>}
          <p className="text-sm text-chalk/85">{me.summary}</p>
          <ul className="space-y-1.5">
            {mine.map((e) => {
              const other = e.source === focus ? e.target : e.source;
              return (
                <li key={e.id}>
                  <button className="w-full rounded-[3px] p-1.5 text-left text-sm hover:bg-raise disabled:hover:bg-transparent"
                    disabled={STATIC} onClick={() => setEditRel(bundle.relationships.find((r) => r.id === e.id) ?? null)}>
                    <Chip color={RELATION_COLORS[e.kind]}>{e.kind}</Chip> <b>{names.get(other)}</b>
                    {e.description && <span className="block text-xs text-dim">{e.description}</span>}
                  </button>
                </li>
              );
            })}
          </ul>
          <p className="text-xs text-dim">{STATIC ? "Click a person in the graph to re-center." : "Click a person in the graph to re-center. Click a line to edit it."}</p>
        </aside>
      )}
      {editRel && (
        <RelationEditor key={editRel === "new" ? "new" : editRel.id} bundle={bundle} relation={editRel === "new" ? null : editRel}
          defaults={{ source_id: focus, timeline_id: timeline || null }} onClose={() => setEditRel(null)} onSaved={reload} />
      )}
      {editEnt && (
        <EntityEditor key={editEnt === "new" ? "new" : editEnt.id} bundle={bundle} entity={editEnt === "new" ? null : editEnt}
          onClose={() => setEditEnt(null)} onSaved={reload} />
      )}
    </div>
  );
}
