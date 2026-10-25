"use client";

import { useState } from "react";
import type { CardEntity, UIBlock } from "@/lib/agent/blocks";
import { api, RELATION_COLORS } from "./client";
import { RelationGraph } from "./RelationGraph";
import { ThreadTimeline, type ThreadLane } from "./ThreadTimeline";
import { Button, Chip } from "./ui";

// Renders the blocks the narrator chose for an answer. Each block is data-complete.
export function Blocks({ blocks, slug, onChanged }: { blocks: UIBlock[]; slug: string; onChanged?: () => void }) {
  return (
    <div className="mt-3 space-y-3">
      {blocks.map((b, i) => (
        <BlockView key={i} block={b} slug={slug} onChanged={onChanged} />
      ))}
    </div>
  );
}

function Frame({ label, title, children }: { label: string; title?: string; children: React.ReactNode }) {
  return (
    <section className="rounded-[3px] border border-line bg-panel/70 p-3">
      <p className="mb-2 font-mono text-[10px] uppercase tracking-[0.18em] text-dim">
        {label}
        {title && <span className="ml-2 normal-case tracking-normal text-chalk/80">{title}</span>}
      </p>
      {children}
    </section>
  );
}

function BlockView({ block, slug, onChanged }: { block: UIBlock; slug: string; onChanged?: () => void }) {
  switch (block.type) {
    case "timeline": {
      const lanes = new Map<string, ThreadLane>();
      for (const e of block.events) {
        lanes.set(e.timeline.name, {
          key: e.timeline.name, name: e.timeline.name, color: e.timeline.color ?? "#d9c9a3", kind: e.timeline.kind, parentKey: null,
        });
      }
      return (
        <Frame label="Timeline" title={block.title}>
          <ThreadTimeline compact lanes={[...lanes.values()]} events={block.events.map((e) => ({ ...e, lane: e.timeline.name }))} />
        </Frame>
      );
    }
    case "relation_graph":
      return (
        <Frame label="Relations" title={[block.title, block.timeline && `in ${block.timeline}`].filter(Boolean).join(" · ")}>
          <RelationGraph nodes={block.nodes} edges={block.edges} focusId={block.focusId} height={340} />
        </Frame>
      );
    case "character_card":
      return (
        <Frame label="Character">
          <Card entity={block.entity} />
        </Frame>
      );
    case "variant_compare":
      return (
        <Frame label="Across timelines">
          <div className="grid gap-3" style={{ gridTemplateColumns: `repeat(${Math.min(3, block.variants.length)}, minmax(0, 1fr))` }}>
            {block.variants.map((v) => (
              <div key={v.id} className="rounded-[3px] border border-line bg-ink/60 p-3">
                <Card entity={v} />
              </div>
            ))}
          </div>
        </Frame>
      );
    case "path":
      return (
        <Frame label="Connection">
          <ol className="flex flex-wrap items-center gap-1.5 text-sm">
            <li className="rounded-full bg-raise px-2.5 py-1 font-semibold">{block.steps[0]?.from}</li>
            {block.steps.map((s, i) => (
              <li key={i} className="flex items-center gap-1.5" title={s.description ?? undefined}>
                <span className="font-mono text-xs" style={{ color: RELATION_COLORS[s.kind] }}>—{s.kind}→</span>
                <span className="rounded-full bg-raise px-2.5 py-1 font-semibold">{s.to}</span>
              </li>
            ))}
          </ol>
        </Frame>
      );
    case "suggestion":
      return <SuggestionBlock s={block.suggestion} slug={slug} onChanged={onChanged} />;
    case "sources":
      return (
        <Frame label="Sources">
          <ul className="grid gap-1 text-sm sm:grid-cols-2">
            {block.sources.map((s) => (
              <li key={s.url} className="truncate">
                <a href={s.url} target="_blank" rel="noreferrer" className="text-sky-300 hover:underline">{s.title}</a>
                <span className="ml-1.5 font-mono text-[10px] text-dim">{s.publisher}</span>
              </li>
            ))}
          </ul>
        </Frame>
      );
  }
}

function Card({ entity }: { entity: CardEntity }) {
  return (
    <div>
      <div className="flex flex-wrap items-baseline gap-2">
        <h4 className="font-display text-base font-bold">{entity.name}</h4>
        <span className="font-mono text-[10px] uppercase text-dim">{entity.kind}</span>
        {entity.timeline && <Chip>{entity.timeline}</Chip>}
      </div>
      {entity.aliases.length > 0 && <p className="text-xs text-dim">also {entity.aliases.join(", ")}</p>}
      {entity.summary && <p className="mt-1 text-sm text-chalk/85">{entity.summary}</p>}
      {entity.relations.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          {entity.relations.map((r, i) => (
            <Chip key={i} color={RELATION_COLORS[r.kind]}>{r.kind} · {r.other}</Chip>
          ))}
        </div>
      )}
      {entity.events.length > 0 && (
        <ul className="mt-2 space-y-0.5 text-xs text-chalk/75">
          {entity.events.map((e, i) => (
            <li key={i}><span className="font-mono text-dim">{e.date_label}</span> {e.title}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

type Suggestion = Extract<UIBlock, { type: "suggestion" }>["suggestion"];

export function SuggestionBlock({ s, slug, onChanged }: { s: Suggestion; slug: string; onChanged?: () => void }) {
  const [status, setStatus] = useState(s.status);
  const [error, setError] = useState<string | null>(null);
  const act = async (action: "accept" | "reject") => {
    setError(null);
    try {
      await api(`/api/games/${slug}/suggestions/${s.id}`, { method: "PATCH", body: JSON.stringify({ action }) });
      setStatus(action === "accept" ? "accepted" : "rejected");
      onChanged?.();
    } catch (e) {
      setError((e as Error).message);
    }
  };
  const p = s.payload as Record<string, unknown>;
  const headline =
    s.kind === "relationship" ? `${p.source} —${p.kind}→ ${p.target}` : String(p.title ?? p.name ?? "Untitled");
  return (
    <Frame label={`Proposed ${s.kind}`}>
      <p className="font-semibold">{headline}</p>
      {(p.summary || p.description) ? <p className="mt-1 text-sm text-chalk/80">{String(p.summary ?? p.description)}</p> : null}
      {p.date_label ? <p className="mt-1 font-mono text-xs text-dim">{String(p.date_label)}</p> : null}
      {s.rationale && <p className="mt-1 text-xs text-dim">Why: {s.rationale}</p>}
      {s.source_url && (
        <a href={s.source_url} target="_blank" rel="noreferrer" className="mt-1 block truncate text-xs text-sky-300 hover:underline">{s.source_url}</a>
      )}
      <div className="mt-2 flex items-center gap-2">
        {status === "pending" ? (
          <>
            <Button kind="primary" onClick={() => act("accept")}>Add to timeline</Button>
            <Button onClick={() => act("reject")}>Reject</Button>
          </>
        ) : (
          <span className="text-sm text-dim">{status === "accepted" ? "Added to the timeline." : "Rejected."}</span>
        )}
        {error && <span className="text-sm text-danger">{error}</span>}
      </div>
    </Frame>
  );
}
