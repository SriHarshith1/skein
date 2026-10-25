import type { Sql } from "../db";
import {
  addSuggestion, entityEvents, findEntities, relationPath, relationsOf, resolveEntity, resolveTimeline,
  searchChunks, searchEvents, sourcesFor, variantsOf, type Game,
} from "../lore";
import { wikiPage, wikiSearch } from "../wiki";
import type { Tool } from "./llm";

// Everything the subagents looked at, keyed by short refs (E1, V2, T1, S3, R4, P1)
// so the composer can point UI blocks at real rows without copying UUIDs.
export class Evidence {
  private refs = new Map<string, { kind: string; id: string; label: string }>();
  private byId = new Map<string, string>();
  private counters: Record<string, number> = {};
  sourceUrls = new Map<string, string>(); // url -> title, for live wiki reads

  ref(kind: "E" | "V" | "T" | "S" | "R" | "P", id: string, label: string) {
    const key = `${kind}:${id}`;
    const existing = this.byId.get(key);
    if (existing) return existing;
    this.counters[kind] = (this.counters[kind] ?? 0) + 1;
    const r = `${kind}${this.counters[kind]}`;
    this.refs.set(r, { kind, id, label });
    this.byId.set(key, r);
    return r;
  }

  // Accepts a ref ("E1") or, because models often write names instead, a label ("K/DA Ahri").
  resolve(ref: string, kind?: string) {
    const key = ref.trim();
    const hit = this.refs.get(key.toUpperCase());
    if (hit) return !kind || hit.kind === kind ? hit.id : null;
    const want = key.toLowerCase();
    for (const v of this.refs.values()) {
      if (kind && v.kind !== kind) continue;
      const label = v.label.toLowerCase();
      // Labels carry suffixes like " (2099)" or " [alternate]"; match with and without them.
      if (label === want || label.replace(/ [(\[].*$/, "") === want) return v.id;
    }
    return null;
  }

  catalog() {
    const names: Record<string, string> = { E: "entity", V: "event", T: "timeline", S: "source", R: "relationship", P: "suggestion" };
    return [...this.refs.entries()].map(([r, v]) => `${r} (${names[v.kind]}): ${v.label}`).join("\n");
  }

  ids(kind: string) {
    return [...this.refs.values()].filter((v) => v.kind === kind).map((v) => v.id);
  }
}

export type ToolContext = { sql: Sql; game: Game; evidence: Evidence };

const str = (v: unknown) => (v == null ? "" : String(v));

export function buildTools(ctx: ToolContext) {
  const { sql, game, evidence } = ctx;
  const gid = game.id;

  const timelineFor = async (ref: unknown) => {
    const t = await resolveTimeline(sql, gid, ref ? str(ref) : null);
    if (t) evidence.ref("T", t.id, `${t.name} [${t.kind}]`);
    return t;
  };
  const entityFor = async (ref: unknown) => {
    const e = await resolveEntity(sql, gid, str(ref));
    if (e) evidence.ref("E", e.id, e.name);
    return e;
  };
  const withSources = async <T extends { id: string }>(rows: T[]) => {
    const srcs = await sourcesFor(sql, rows.map((r) => r.id));
    for (const s of srcs) evidence.ref("S", s.id, s.title ?? s.url);
    return srcs;
  };

  const tools: Record<string, Tool> = {
    list_timelines: {
      name: "list_timelines",
      description: "List every timeline/continuity of this game (canon, alternate branches, AU skin lines).",
      parameters: { type: "object", properties: {} },
      run: async () => {
        const rows = await sql`select id, slug, name, kind, branch_note, description,
            (select count(*)::int from events e where e.timeline_id = t.id) as events
          from timelines t where game_id = ${gid} order by (kind = 'canon') desc, name`;
        return rows.map((t) => ({ ref: evidence.ref("T", t.id, `${t.name} [${t.kind}]`), ...t, id: undefined }));
      },
    },
    find_entity: {
      name: "find_entity",
      description: "Find characters, factions, places or artifacts by name, alias or description. Returns summaries.",
      parameters: { type: "object", properties: { query: { type: "string" } }, required: ["query"] },
      run: async ({ query }) => {
        const rows = await findEntities(sql, gid, str(query), 5);
        const srcs = await withSources(rows);
        return rows.map((e) => ({
          ref: evidence.ref("E", e.id, e.name),
          name: e.name, kind: e.kind, aliases: e.aliases, summary: e.summary,
          variant_of: e.variant_of ? true : undefined,
          sources: srcs.filter((s) => s.subject_id === e.id).map((s) => s.url),
        }));
      },
    },
    character_events: {
      name: "character_events",
      description: "Chronological list of events a character/entity took part in, across all timelines.",
      parameters: { type: "object", properties: { entity: { type: "string", description: "name or ref" } }, required: ["entity"] },
      run: async ({ entity }) => {
        const e = await entityFor(entity);
        if (!e) return { error: `no entity matches "${entity}"` };
        const rows = await entityEvents(sql, e.id);
        await withSources(rows as never);
        return rows.map((v) => ({ ref: evidence.ref("V", v.id, `${v.title} (${v.date_label ?? v.sort_key})`), ...v, id: undefined }));
      },
    },
    search_events: {
      name: "search_events",
      description: "Search timeline events by text and/or timeline and/or in-universe date range (sort_key numbers).",
      parameters: {
        type: "object",
        properties: {
          query: { type: "string" },
          timeline: { type: "string", description: "timeline slug or name" },
          from: { type: "number" },
          to: { type: "number" },
        },
      },
      run: async ({ query, timeline, from, to }) => {
        const t = timeline ? await timelineFor(timeline) : null;
        const rows = await searchEvents(sql, gid, {
          query: query ? str(query) : undefined, timelineId: t?.id ?? null,
          from: from == null ? undefined : Number(from), to: to == null ? undefined : Number(to), limit: 20,
        });
        await withSources(rows as never);
        return rows.map((v) => ({ ref: evidence.ref("V", v.id, `${v.title} (${v.date_label ?? v.sort_key})`), ...v, id: undefined }));
      },
    },
    get_relations: {
      name: "get_relations",
      description: "Relationships around a character (family, rivals, allies, romance, variants). Optionally only those valid in one timeline.",
      parameters: {
        type: "object",
        properties: {
          entity: { type: "string" },
          timeline: { type: "string" },
          depth: { type: "number", description: "1 or 2 hops" },
        },
        required: ["entity"],
      },
      run: async ({ entity, timeline, depth }) => {
        const e = await entityFor(entity);
        if (!e) return { error: `no entity matches "${entity}"` };
        const t = timeline ? await timelineFor(timeline) : null;
        const rows = await relationsOf(sql, e.id, t?.id ?? null, Math.min(2, Math.max(1, Number(depth) || 1)));
        await withSources(rows as never);
        return rows.map((r) => ({
          ref: evidence.ref("R", String(r.id), `${r.source} —${r.kind}→ ${r.target}`),
          source: r.source, kind: r.kind, target: r.target, timeline: r.timeline ?? "all", description: r.description,
        }));
      },
    },
    find_path: {
      name: "find_path",
      description: "Shortest chain of relationships connecting two characters (how is A connected to B).",
      parameters: {
        type: "object",
        properties: { from: { type: "string" }, to: { type: "string" }, timeline: { type: "string" } },
        required: ["from", "to"],
      },
      run: async ({ from, to, timeline }) => {
        const a = await entityFor(from);
        const b = await entityFor(to);
        if (!a || !b) return { error: "both characters must exist" };
        const t = timeline ? await timelineFor(timeline) : null;
        const chain = await relationPath(sql, gid, a.id, b.id, t?.id ?? null);
        if (!chain) return { connected: false };
        return {
          connected: true,
          hops: chain.map((r) => ({ ref: evidence.ref("R", r.id, `${r.kind}`), kind: r.kind, description: r.description })),
        };
      },
    },
    get_variants: {
      name: "get_variants",
      description: "All versions of a character across timelines (e.g. present-day vs 2099 vs AU skin-line versions).",
      parameters: { type: "object", properties: { entity: { type: "string" } }, required: ["entity"] },
      run: async ({ entity }) => {
        const e = await entityFor(entity);
        if (!e) return { error: `no entity matches "${entity}"` };
        const rows = await variantsOf(sql, e.id);
        return rows.map((v) => ({
          ref: evidence.ref("E", v.id, v.name), name: v.name, timeline: v.timeline_name ?? "canon", summary: v.summary,
        }));
      },
    },
    search_lore: {
      name: "search_lore",
      description: "Full-text search over scraped wiki passages. Use for details not in the structured timeline.",
      parameters: { type: "object", properties: { query: { type: "string" } }, required: ["query"] },
      run: async ({ query }) => {
        const rows = await searchChunks(sql, gid, str(query), 5);
        return rows.map((c) => ({
          source: c.source_id ? evidence.ref("S", c.source_id, c.title ?? c.url) : null,
          heading: c.heading, passage: c.content, url: c.url,
        }));
      },
    },
    wiki_search: {
      name: "wiki_search",
      description: "Search the game's live community wiki for page titles. Use only when the database lacks the answer.",
      parameters: { type: "object", properties: { query: { type: "string" } }, required: ["query"] },
      run: async ({ query }) => {
        if (!game.wiki_api) return { error: "this game has no wiki configured" };
        return wikiSearch(game.wiki_api, str(query), 5);
      },
    },
    wiki_read: {
      name: "wiki_read",
      description: "Read a live wiki page (by exact title from wiki_search). Returns its sections as text.",
      parameters: { type: "object", properties: { title: { type: "string" } }, required: ["title"] },
      run: async ({ title }) => {
        if (!game.wiki_api) return { error: "this game has no wiki configured" };
        const page = await wikiPage(game.wiki_api, str(title));
        if (!page) return { error: "page not found" };
        evidence.sourceUrls.set(page.url, page.title);
        return { url: page.url, sections: page.sections.slice(0, 8).map((s) => ({ heading: s.heading, text: s.text.slice(0, 900) })) };
      },
    },
    propose_edit: {
      name: "propose_edit",
      description:
        "Propose a NEW event, entity or relationship for the timeline. It goes to a human review queue; nothing changes until accepted. " +
        "payload for event: {title, summary, date_label, sort_key, timeline, participants:[names]}; " +
        "entity: {name, kind, summary, timeline}; relationship: {source, target, kind, description, timeline}.",
      parameters: {
        type: "object",
        properties: {
          kind: { type: "string", enum: ["event", "entity", "relationship"] },
          payload: { type: "object" },
          rationale: { type: "string" },
          source_url: { type: "string" },
        },
        required: ["kind", "payload", "rationale"],
      },
      run: async ({ kind, payload, rationale, source_url }) => {
        const k = str(kind) as "event" | "entity" | "relationship";
        if (!["event", "entity", "relationship"].includes(k)) return { error: "bad kind" };
        const p = (typeof payload === "string" ? JSON.parse(payload) : payload) as Record<string, unknown>;
        const row = await addSuggestion(sql, gid, {
          kind: k, payload: p, rationale: str(rationale), source_url: source_url ? str(source_url) : undefined, origin: "agent",
        });
        const label = str(p.title ?? p.name ?? `${p.source} ${p.kind} ${p.target}`);
        return { ref: evidence.ref("P", row.id, `proposed ${k}: ${label}`), status: "pending review" };
      },
    },
  };
  return tools;
}
