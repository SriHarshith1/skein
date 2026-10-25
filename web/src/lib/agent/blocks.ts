import { z } from "zod";
import type { Sql } from "../db";
import { findEntities, relationPath, relationsOf, sourcesFor, variantsOf, type Game } from "../lore";
import type { Evidence } from "./tools";

// What the composer model may ask for. Refs come from the evidence catalog.
export const RawBlock = z.discriminatedUnion("type", [
  z.object({ type: z.literal("timeline"), title: z.string().optional(), events: z.array(z.string()).min(1) }),
  z.object({
    type: z.literal("relation_graph"), title: z.string().optional(), focus: z.string(),
    timeline: z.string().nullish(), depth: z.coerce.number().optional(),
  }),
  z.object({ type: z.literal("character_card"), entity: z.string() }),
  z.object({ type: z.literal("variant_compare"), entity: z.string() }),
  z.object({ type: z.literal("path"), from: z.string(), to: z.string(), timeline: z.string().nullish() }),
  z.object({ type: z.literal("suggestion"), ref: z.string() }),
]);
export type RawBlock = z.infer<typeof RawBlock>;

export const ComposerOutput = z.object({
  answer: z.string(),
  blocks: z.array(z.unknown()).default([]),
});

export const BLOCK_GUIDE = `UI blocks you can attach (pick the 1-3 that best show the answer). Fill every ref field with a ref code from the catalog, e.g. "E3" or "V12", not a name:
- {"type":"timeline","title":"...","events":["V1","V2",...]}  chronological strip of events (2+ events)
- {"type":"relation_graph","title":"...","focus":"E1","timeline":"T2" or null,"depth":1|2}  relationship graph around a character
- {"type":"character_card","entity":"E1"}  profile card for one character
- {"type":"variant_compare","entity":"E1"}  the character's versions across timelines side by side
- {"type":"path","from":"E1","to":"E2","timeline":null}  chain of relationships linking two characters
- {"type":"suggestion","ref":"P1"}  an edit you proposed, so the user can accept it`;

type Named = { id: string; name: string };

export type UIBlock =
  | { type: "timeline"; title?: string; events: TimelineEvent[] }
  | { type: "relation_graph"; title?: string; focusId: string; timeline: string | null; nodes: GraphNode[]; edges: GraphEdge[] }
  | { type: "character_card"; entity: CardEntity }
  | { type: "variant_compare"; variants: CardEntity[] }
  | { type: "path"; steps: { from: string; kind: string; to: string; description: string | null }[] }
  | { type: "suggestion"; suggestion: { id: string; kind: string; payload: Record<string, unknown>; rationale: string | null; status: string; source_url: string | null } }
  | { type: "sources"; sources: { title: string; url: string; publisher: string }[] };

export type TimelineEvent = {
  id: string; title: string; date_label: string | null; sort_key: number; summary: string | null;
  importance: number; timeline: { name: string; kind: string; color: string | null }; participants: string[];
};
export type GraphNode = { id: string; name: string; kind: string; timeline: string | null };
export type GraphEdge = { id: string; source: string; target: string; kind: string; description: string | null; timeline: string | null };
export type CardEntity = {
  id: string; name: string; kind: string; summary: string | null; aliases: string[]; timeline: string | null;
  events: { title: string; date_label: string | null }[]; relations: { kind: string; other: string }[];
};

async function card(sql: Sql, entityId: string): Promise<CardEntity | null> {
  const [e] = await sql`select e.id, e.name, e.kind, e.summary, e.aliases, t.name as timeline
    from entities e left join timelines t on t.id = e.timeline_id where e.id = ${entityId}`;
  if (!e) return null;
  const events = await sql`select ev.title, ev.date_label from event_participants p
    join events ev on ev.id = p.event_id where p.entity_id = ${entityId} order by ev.importance desc, ev.sort_key limit 5`;
  const rels = await sql`select r.kind, case when r.source_id = ${entityId} then t.name else s.name end as other
    from relationships r join entities s on s.id = r.source_id join entities t on t.id = r.target_id
    where r.source_id = ${entityId} or r.target_id = ${entityId} limit 8`;
  return {
    id: e.id, name: e.name, kind: e.kind, summary: e.summary, aliases: e.aliases, timeline: e.timeline,
    events: events.map((x) => ({ title: x.title, date_label: x.date_label })),
    relations: rels.map((x) => ({ kind: x.kind, other: x.other })),
  };
}

// Turns raw composer blocks into data-complete UI blocks. Bad refs are dropped, never guessed.
export async function hydrateBlocks(sql: Sql, game: Game, evidence: Evidence, raw: unknown[]): Promise<UIBlock[]> {
  const out: UIBlock[] = [];
  const cited = new Set<string>();
  // An entity named outside the evidence still counts when the name matches exactly.
  const entity = async (ref: string) => {
    const id = evidence.resolve(ref, "E");
    if (id) return id;
    const [best] = await findEntities(sql, game.id, ref, 1);
    return best && best.score >= 2.5 ? best.id : null;
  };
  for (const item of raw.slice(0, 4)) {
    const parsed = RawBlock.safeParse(item);
    if (!parsed.success) {
      console.warn("[lorelines] dropped block", JSON.stringify(item).slice(0, 300));
      continue;
    }
    const b = parsed.data;
    try {
      if (b.type === "timeline") {
        const ids = b.events.map((r) => evidence.resolve(r, "V")).filter((x): x is string => !!x);
        if (!ids.length) continue;
        const rows = await sql`select e.id, e.title, e.date_label, e.sort_key, e.summary, e.importance,
            json_build_object('name', t.name, 'kind', t.kind, 'color', t.color) as timeline,
            coalesce((select array_agg(en.name) from event_participants p join entities en on en.id = p.entity_id
                      where p.event_id = e.id), '{}') as participants
          from events e join timelines t on t.id = e.timeline_id where e.id = any(${ids}::uuid[]) order by e.sort_key`;
        rows.forEach((r) => cited.add(r.id));
        out.push({ type: "timeline", title: b.title, events: rows.map((r) => ({ ...r, sort_key: Number(r.sort_key) })) as TimelineEvent[] });
      } else if (b.type === "relation_graph") {
        const focusId = await entity(b.focus);
        if (!focusId) continue;
        const tl = b.timeline ? evidence.resolve(b.timeline, "T") : null;
        const edges = await relationsOf(sql, focusId, tl, Math.min(2, Math.max(1, b.depth ?? 1)));
        const nodeIds = [...new Set(edges.flatMap((e) => [String(e.source_id), String(e.target_id)]).concat(focusId))];
        const nodes = await sql<GraphNode[]>`select e.id, e.name, e.kind, t.slug as timeline from entities e
          left join timelines t on t.id = e.timeline_id where e.id = any(${nodeIds}::uuid[])`;
        edges.forEach((e) => cited.add(String(e.id)));
        const [tname] = tl ? await sql`select name from timelines where id = ${tl}` : [];
        out.push({
          type: "relation_graph", title: b.title, focusId, timeline: tname?.name ?? null, nodes: [...nodes],
          edges: edges.map((e) => ({
            id: String(e.id), source: String(e.source_id), target: String(e.target_id), kind: String(e.kind),
            description: (e.description as string) ?? null, timeline: (e.timeline as string) ?? null,
          })),
        });
      } else if (b.type === "character_card") {
        const id = await entity(b.entity);
        const c = id ? await card(sql, id) : null;
        if (c) {
          cited.add(c.id);
          out.push({ type: "character_card", entity: c });
        }
      } else if (b.type === "variant_compare") {
        const id = await entity(b.entity);
        if (!id) continue;
        const vs = await variantsOf(sql, id);
        if (vs.length < 2) {
          const c = await card(sql, id);
          if (c) out.push({ type: "character_card", entity: c });
          continue;
        }
        const variants = (await Promise.all(vs.map((v) => card(sql, v.id)))).filter((x): x is CardEntity => !!x);
        variants.forEach((v) => cited.add(v.id));
        out.push({ type: "variant_compare", variants });
      } else if (b.type === "path") {
        const a = await entity(b.from);
        const z2 = await entity(b.to);
        if (!a || !z2) continue;
        const tl = b.timeline ? evidence.resolve(b.timeline, "T") : null;
        const chain = await relationPath(sql, game.id, a, z2, tl);
        if (!chain?.length) continue;
        const ids = [...new Set(chain.flatMap((r) => [r.source_id, r.target_id]))];
        const names = new Map((await sql<Named[]>`select id, name from entities where id = any(${ids}::uuid[])`).map((n) => [n.id, n.name]));
        // Walk the chain in order so each step starts where the last ended.
        let at = a;
        const steps = chain.map((r) => {
          const forward = r.source_id === at;
          const next = forward ? r.target_id : r.source_id;
          const step = { from: names.get(at) ?? "?", kind: r.kind, to: names.get(next) ?? "?", description: r.description };
          at = next;
          cited.add(r.id);
          return step;
        });
        out.push({ type: "path", steps });
      } else if (b.type === "suggestion") {
        const id = evidence.resolve(b.ref, "P");
        if (!id) continue;
        const [s] = await sql`select id, kind, payload, rationale, status, source_url from suggestions where id = ${id}`;
        if (s) out.push({ type: "suggestion", suggestion: s as never });
      }
    } catch {
      // A block that fails to build is left out; the text answer still stands.
    }
  }
  // Sources: whatever backs the blocks, plus sources the subagents read directly.
  const srcRows = await sourcesFor(sql, [...cited]);
  const seen = new Map<string, { title: string; url: string; publisher: string }>();
  for (const s of srcRows) seen.set(s.url, { title: s.title ?? s.url, url: s.url, publisher: s.publisher });
  for (const id of evidence.ids("S")) {
    const [s] = await sql`select url, title, publisher from sources where id = ${id}`;
    if (s && seen.size < 12) seen.set(s.url, { title: s.title ?? s.url, url: s.url, publisher: s.publisher });
  }
  for (const [url, title] of evidence.sourceUrls) seen.set(url, { title, url, publisher: "wiki (live)" });
  if (seen.size) out.push({ type: "sources", sources: [...seen.values()].slice(0, 12) });
  return out;
}

// Refs are for the machine; the prose the user reads should not show them.
export function stripRefs(text: string) {
  return text.replace(/\s?\[(?:[EVTSRP]\d+)(?:\s*,\s*[EVTSRP]\d+)*\]/g, "").replace(/[ \t]+\n/g, "\n").trim();
}
