import type postgres from "postgres";
import type { Sql } from "./db";

export type Game = {
  id: string; slug: string; name: string; calendar: string | null; description: string | null;
  wiki_base: string | null; wiki_api: string | null; wiki_license: string | null;
};
export type Timeline = {
  id: string; slug: string; name: string; kind: "canon" | "alternate" | "au";
  parent_id: string | null; branch_event_id: string | null; branch_note: string | null;
  description: string | null; color: string | null;
};
export type Entity = {
  id: string; slug: string; name: string; kind: string; timeline_id: string | null;
  variant_of: string | null; aliases: string[]; summary: string | null; image_url: string | null;
};
export type LoreEvent = {
  id: string; slug: string; timeline_id: string; title: string; summary: string | null;
  date_label: string | null; sort_key: number; era: string | null; importance: number;
  participants: { entity_id: string; role: string | null }[];
};
export type Relationship = {
  id: string; source_id: string; target_id: string; kind: string; timeline_id: string | null;
  description: string | null; since_event_id: string | null; until_event_id: string | null;
};
export type Source = { id: string; key: string; url: string; title: string | null; publisher: string };

export type Bundle = {
  game: Game;
  timelines: Timeline[];
  entities: Entity[];
  events: LoreEvent[];
  relationships: Relationship[];
  sources: Source[];
  citations: Record<string, string[]>; // subject id -> source ids
  stats: { chunks: number; pendingSuggestions: number };
};

export async function listGames(sql: Sql) {
  return sql`
    select g.slug, g.name, g.description, g.calendar,
      (select count(*)::int from events e where e.game_id = g.id) as events,
      (select count(*)::int from entities e where e.game_id = g.id) as entities,
      (select count(*)::int from relationships r where r.game_id = g.id) as relationships,
      coalesce((select json_agg(json_build_object('name', t.name, 'kind', t.kind, 'color', t.color,
          'events', (select count(*)::int from events e where e.timeline_id = t.id))
          order by (t.kind = 'canon') desc, t.name)
        from timelines t where t.game_id = g.id), '[]') as timelines
    from games g order by g.name`;
}

export async function getGame(sql: Sql, slug: string): Promise<Game | null> {
  const [g] = await sql<Game[]>`select id, slug, name, calendar, description, wiki_base, wiki_api,
    wiki_license from games where slug = ${slug}`;
  return g ?? null;
}

export async function getBundle(sql: Sql, slug: string): Promise<Bundle | null> {
  const game = await getGame(sql, slug);
  if (!game) return null;
  const gid = game.id;
  const [timelines, entities, events, relationships, sources, citations, [stats]] = await Promise.all([
    sql<Timeline[]>`select id, slug, name, kind, parent_id, branch_event_id, branch_note, description, color
      from timelines where game_id = ${gid} order by (kind = 'canon') desc, name`,
    sql<Entity[]>`select id, slug, name, kind, timeline_id, variant_of, aliases, summary, image_url
      from entities where game_id = ${gid} order by name`,
    sql<LoreEvent[]>`select e.id, e.slug, e.timeline_id, e.title, e.summary, e.date_label, e.sort_key,
        e.era, e.importance,
        coalesce((select json_agg(json_build_object('entity_id', p.entity_id, 'role', p.role))
                  from event_participants p where p.event_id = e.id), '[]') as participants
      from events e where e.game_id = ${gid} order by e.sort_key, e.title`,
    sql<Relationship[]>`select id, source_id, target_id, kind, timeline_id, description,
        since_event_id, until_event_id
      from relationships where game_id = ${gid}`,
    sql<Source[]>`select id, key, url, title, publisher from sources where game_id = ${gid} order by key`,
    sql`select c.subject_id, c.source_id from citations c join sources s on s.id = c.source_id
      where s.game_id = ${gid}`,
    sql`select (select count(*)::int from lore_chunks where game_id = ${gid}) as chunks,
      (select count(*)::int from suggestions where game_id = ${gid} and status = 'pending') as pending`,
  ]);
  const cites: Record<string, string[]> = {};
  for (const c of citations) (cites[c.subject_id] ??= []).push(c.source_id);
  return {
    game,
    timelines: [...timelines],
    entities: [...entities],
    events: events.map((e) => ({ ...e, sort_key: Number(e.sort_key) })),
    relationships: [...relationships],
    sources: [...sources],
    citations: cites,
    stats: { chunks: stats.chunks, pendingSuggestions: stats.pending },
  };
}

// ---------- read helpers for the agent ----------

// Resolves "Doom 2099", "doom-2099" or an alias to entities, best match first.
export async function findEntities(sql: Sql, gameId: string, query: string, limit = 5) {
  const q = query.trim();
  return sql<(Entity & { score: number })[]>`
    select id, slug, name, kind, timeline_id, variant_of, aliases, summary, image_url,
      case when lower(name) = lower(${q}) or slug = lower(${q}) then 3
           when exists (select 1 from unnest(aliases) a where lower(a) = lower(${q})) then 2.5
           when name ilike ${"%" + q + "%"} then 2
           else ts_rank(to_tsvector('english', name || ' ' || coalesce(summary, '')),
                        websearch_to_tsquery('english', ${q})) end as score
    from entities
    where game_id = ${gameId} and (
      name ilike ${"%" + q + "%"} or slug = lower(${q})
      or exists (select 1 from unnest(aliases) a where a ilike ${"%" + q + "%"})
      or to_tsvector('english', name || ' ' || coalesce(summary, '')) @@ websearch_to_tsquery('english', ${q}))
    order by score desc limit ${limit}`;
}

export async function resolveEntity(sql: Sql, gameId: string, ref: string) {
  const [byId] = /^[0-9a-f-]{36}$/.test(ref)
    ? await sql<Entity[]>`select id, slug, name, kind, timeline_id, variant_of, aliases, summary, image_url
        from entities where id = ${ref} and game_id = ${gameId}`
    : [];
  if (byId) return byId;
  const [best] = await findEntities(sql, gameId, ref, 1);
  return best ?? null;
}

export async function resolveTimeline(sql: Sql, gameId: string, ref: string | null | undefined) {
  if (!ref) return null;
  const [t] = await sql<Timeline[]>`select id, slug, name, kind, parent_id, branch_event_id, branch_note,
      description, color from timelines
    where game_id = ${gameId} and (slug = lower(${ref}) or name ilike ${ref} or id::text = ${ref})`;
  return t ?? null;
}

export async function entityEvents(sql: Sql, entityId: string) {
  return sql`select e.id, e.title, e.date_label, e.sort_key, e.importance, e.summary, p.role,
      t.slug as timeline
    from event_participants p join events e on e.id = p.event_id join timelines t on t.id = e.timeline_id
    where p.entity_id = ${entityId} order by e.sort_key`;
}

export async function searchEvents(
  sql: Sql,
  gameId: string,
  opts: { query?: string; timelineId?: string | null; entityId?: string | null; from?: number; to?: number; limit?: number },
) {
  const q = opts.query?.trim() || null;
  return sql`
    select e.id, e.title, e.date_label, e.sort_key, e.importance, e.summary, t.slug as timeline,
      coalesce((select array_agg(en.name) from event_participants p join entities en on en.id = p.entity_id
                where p.event_id = e.id), '{}') as participants
    from events e join timelines t on t.id = e.timeline_id
    where e.game_id = ${gameId}
      and (${opts.timelineId ?? null}::uuid is null or e.timeline_id = ${opts.timelineId ?? null}::uuid)
      and (${opts.entityId ?? null}::uuid is null or exists (
            select 1 from event_participants p where p.event_id = e.id and p.entity_id = ${opts.entityId ?? null}::uuid))
      and (${opts.from ?? null}::float8 is null or e.sort_key >= ${opts.from ?? null}::float8)
      and (${opts.to ?? null}::float8 is null or e.sort_key <= ${opts.to ?? null}::float8)
      and (${q}::text is null
           or to_tsvector('english', e.title || ' ' || coalesce(e.summary, '')) @@ websearch_to_tsquery('english', ${q})
           or e.title ilike ${"%" + (q ?? "") + "%"})
    order by e.sort_key limit ${opts.limit ?? 25}`;
}

// Relationships around an entity, optionally inside one timeline (null-timeline rows hold everywhere).
export async function relationsOf(sql: Sql, entityId: string, timelineId: string | null, depth = 1) {
  const seen = new Set<string>([entityId]);
  let frontier = [entityId];
  const edges = new Map<string, Record<string, unknown>>();
  for (let d = 0; d < depth && frontier.length; d++) {
    const rows = await sql`
      select r.id, r.kind, r.description, r.timeline_id, r.source_id, r.target_id,
        s.name as source, t.name as target, tl.slug as timeline
      from relationships r join entities s on s.id = r.source_id join entities t on t.id = r.target_id
        left join timelines tl on tl.id = r.timeline_id
      where (r.source_id = any(${frontier}::uuid[]) or r.target_id = any(${frontier}::uuid[]))
        and (${timelineId}::uuid is null or r.timeline_id is null or r.timeline_id = ${timelineId}::uuid
             or r.kind = 'variant')`;
    const next: string[] = [];
    for (const r of rows) {
      edges.set(r.id, r);
      for (const id of [r.source_id, r.target_id]) {
        if (!seen.has(id)) {
          seen.add(id);
          next.push(id);
        }
      }
    }
    frontier = next;
  }
  return [...edges.values()];
}

// Shortest chain of relationships between two entities (breadth-first, max 4 hops).
export async function relationPath(sql: Sql, gameId: string, fromId: string, toId: string, timelineId: string | null) {
  const rows = await sql`select id, source_id, target_id, kind, description from relationships
    where game_id = ${gameId}
      and (${timelineId}::uuid is null or timeline_id is null or timeline_id = ${timelineId}::uuid)`;
  const adj = new Map<string, { to: string; rel: (typeof rows)[number] }[]>();
  for (const r of rows) {
    (adj.get(r.source_id) ?? adj.set(r.source_id, []).get(r.source_id)!).push({ to: r.target_id, rel: r });
    (adj.get(r.target_id) ?? adj.set(r.target_id, []).get(r.target_id)!).push({ to: r.source_id, rel: r });
  }
  const prev = new Map<string, { from: string; rel: (typeof rows)[number] }>();
  const queue = [fromId];
  const depth = new Map([[fromId, 0]]);
  while (queue.length) {
    const cur = queue.shift()!;
    if (cur === toId) break;
    if (depth.get(cur)! >= 4) continue;
    for (const { to, rel } of adj.get(cur) ?? []) {
      if (depth.has(to)) continue;
      depth.set(to, depth.get(cur)! + 1);
      prev.set(to, { from: cur, rel });
      queue.push(to);
    }
  }
  if (!prev.has(toId) && fromId !== toId) return null;
  const chain: (typeof rows)[number][] = [];
  for (let at = toId; at !== fromId; at = prev.get(at)!.from) chain.unshift(prev.get(at)!.rel);
  return chain;
}

export async function variantsOf(sql: Sql, entityId: string) {
  // Walk to the root character, then list it and every variant of it.
  const [root] = await sql`with recursive up as (
      select id, variant_of from entities where id = ${entityId}
      union all select e.id, e.variant_of from entities e join up on e.id = up.variant_of)
    select id from up where variant_of is null limit 1`;
  const rootId = root?.id ?? entityId;
  return sql`with recursive down as (
      select id from entities where id = ${rootId}
      union all select e.id from entities e join down on e.variant_of = down.id)
    select e.id, e.name, e.slug, e.summary, e.variant_of, t.slug as timeline, t.name as timeline_name
    from entities e join down using (id) left join timelines t on t.id = e.timeline_id`;
}

// Full-text search over scraped wiki passages, with their source.
export async function searchChunks(sql: Sql, gameId: string, query: string, limit = 6) {
  return sql`
    select c.id, c.heading, left(c.content, 1200) as content, s.id as source_id, s.url, s.title,
      ts_rank(to_tsvector('english', coalesce(c.heading, '') || ' ' || c.content),
              websearch_to_tsquery('english', ${query})) as rank
    from lore_chunks c left join sources s on s.id = c.source_id
    where c.game_id = ${gameId}
      and to_tsvector('english', coalesce(c.heading, '') || ' ' || c.content) @@ websearch_to_tsquery('english', ${query})
    order by rank desc limit ${limit}`;
}

export async function sourcesFor(sql: Sql, subjectIds: string[]) {
  if (!subjectIds.length) return [];
  return sql<(Source & { subject_id: string })[]>`select distinct s.id, s.key, s.url, s.title, s.publisher,
      c.subject_id from citations c join sources s on s.id = c.source_id
    where c.subject_id = any(${subjectIds}::uuid[])`;
}

// ---------- writes (editable lore) ----------

const EDITABLE: Record<string, readonly string[]> = {
  timelines: ["slug", "name", "kind", "parent_id", "branch_event_id", "branch_note", "description", "color"],
  entities: ["slug", "name", "kind", "timeline_id", "variant_of", "aliases", "summary", "image_url"],
  events: ["slug", "timeline_id", "title", "summary", "date_label", "sort_key", "era", "importance"],
  relationships: ["source_id", "target_id", "kind", "timeline_id", "description", "since_event_id", "until_event_id"],
  sources: ["key", "url", "title", "publisher"],
};

export function isEditableTable(t: string): t is keyof typeof EDITABLE {
  return t in EDITABLE;
}

function pick(table: string, input: Record<string, unknown>) {
  const out: Record<string, unknown> = {};
  for (const col of EDITABLE[table]) {
    if (input[col] !== undefined) out[col] = input[col] === "" ? null : input[col];
  }
  return out;
}

export function slugify(s: string) {
  return s.toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "item";
}

type Participants = { entity_id: string; role?: string | null }[];

async function setParticipants(tx: postgres.TransactionSql, eventId: string, participants: Participants) {
  await tx`delete from event_participants where event_id = ${eventId}`;
  for (const p of participants) {
    await tx`insert into event_participants (event_id, entity_id, role) values (${eventId}, ${p.entity_id},
      ${p.role ?? null}) on conflict do nothing`;
  }
}

async function setCitations(tx: postgres.TransactionSql, type: string, id: string, sourceIds: string[]) {
  await tx`delete from citations where subject_type = ${type} and subject_id = ${id}`;
  for (const sid of new Set(sourceIds)) {
    await tx`insert into citations (source_id, subject_type, subject_id) values (${sid}, ${type}, ${id})
      on conflict do nothing`;
  }
}

const SUBJECT: Record<string, string> = {
  entities: "entity", events: "event", relationships: "relationship", timelines: "timeline",
};

export async function createRow(
  sql: Sql, gameId: string, table: string, input: Record<string, unknown>, actor = "editor",
) {
  if (!isEditableTable(table)) throw new Error(`table ${table} is not editable`);
  const row = pick(table, input);
  if ((table === "entities" || table === "events" || table === "timelines") && !row.slug) {
    row.slug = slugify(String(row.name ?? row.title ?? "item")) + "-" + Math.random().toString(36).slice(2, 6);
  }
  if (table === "sources" && !row.key) row.key = slugify(String(row.title ?? row.url ?? "source"));
  row.game_id = gameId;
  return sql.begin(async (tx) => {
    await tx`select set_config('lorelines.actor', ${actor}, true)`;
    const [created] = await tx`insert into ${tx(table)} ${tx(row)} returning *`;
    if (table === "events" && Array.isArray(input.participants)) {
      await setParticipants(tx, created.id, input.participants as Participants);
    }
    if (SUBJECT[table] && Array.isArray(input.source_ids)) {
      await setCitations(tx, SUBJECT[table], created.id, input.source_ids as string[]);
    }
    return created;
  });
}

export async function updateRow(
  sql: Sql, gameId: string, table: string, id: string, input: Record<string, unknown>, actor = "editor",
) {
  if (!isEditableTable(table)) throw new Error(`table ${table} is not editable`);
  const row = pick(table, input);
  return sql.begin(async (tx) => {
    await tx`select set_config('lorelines.actor', ${actor}, true)`;
    let updated;
    if (Object.keys(row).length) {
      [updated] = await tx`update ${tx(table)} set ${tx(row)} where id = ${id} and game_id = ${gameId} returning *`;
    } else {
      [updated] = await tx`select * from ${tx(table)} where id = ${id} and game_id = ${gameId}`;
    }
    if (!updated) return null;
    if (table === "events" && Array.isArray(input.participants)) {
      await setParticipants(tx, id, input.participants as Participants);
    }
    if (SUBJECT[table] && Array.isArray(input.source_ids)) {
      await setCitations(tx, SUBJECT[table], id, input.source_ids as string[]);
    }
    return updated;
  });
}

export async function deleteRow(sql: Sql, gameId: string, table: string, id: string, actor = "editor") {
  if (!isEditableTable(table)) throw new Error(`table ${table} is not editable`);
  return sql.begin(async (tx) => {
    await tx`select set_config('lorelines.actor', ${actor}, true)`;
    const rows = await tx`delete from ${tx(table)} where id = ${id} and game_id = ${gameId} returning id`;
    if (SUBJECT[table]) await tx`delete from citations where subject_type = ${SUBJECT[table]} and subject_id = ${id}`;
    return rows.length > 0;
  });
}

export async function history(sql: Sql, rowId: string) {
  return sql`select id, table_name, op, before, after, actor, created_at from revisions
    where row_id = ${rowId} order by created_at desc, id desc limit 50`;
}

export async function recentRevisions(sql: Sql, gameId: string, limit = 40) {
  return sql`select id, table_name, row_id, op, actor, created_at,
      coalesce(after ->> 'title', after ->> 'name', before ->> 'title', before ->> 'name',
               after ->> 'kind', before ->> 'kind') as label
    from revisions
    where coalesce(after ->> 'game_id', before ->> 'game_id') = ${gameId}
      and coalesce(actor, '') <> 'seed'
    order by created_at desc, id desc limit ${limit}`;
}

// ---------- suggestions (agent / scraper proposals) ----------

export async function addSuggestion(
  sql: Sql,
  gameId: string,
  s: { kind: "event" | "entity" | "relationship"; payload: Record<string, unknown>; rationale?: string; source_url?: string; origin?: string },
) {
  const [row] = await sql`insert into suggestions (game_id, kind, payload, rationale, source_url, origin)
    values (${gameId}, ${s.kind}, ${sql.json(s.payload as never)}, ${s.rationale ?? null},
            ${s.source_url ?? null}, ${s.origin ?? "agent"})
    returning *`;
  return row;
}

export async function listSuggestions(sql: Sql, gameId: string, status = "pending") {
  return sql`select * from suggestions where game_id = ${gameId} and status = ${status}
    order by created_at desc limit 100`;
}

// Accepting turns the payload (names, not ids) into real rows.
export async function acceptSuggestion(sql: Sql, gameId: string, id: string, actor = "editor") {
  const [s] = await sql`select * from suggestions where id = ${id} and game_id = ${gameId} and status = 'pending'`;
  if (!s) return null;
  const p = s.payload as Record<string, unknown>;
  const ent = async (ref: unknown) => (ref ? (await resolveEntity(sql, gameId, String(ref)))?.id : undefined);
  const tl = async (ref: unknown) => (await resolveTimeline(sql, gameId, ref as string))?.id;
  let source_ids: string[] = [];
  if (s.source_url) {
    const [src] = await sql`insert into sources (game_id, key, url, title, publisher)
      values (${gameId}, ${slugify(s.source_url).slice(-50)}, ${s.source_url}, ${s.source_url}, 'wiki')
      on conflict (game_id, key) do update set url = excluded.url returning id`;
    source_ids = [src.id];
  }
  let created;
  if (s.kind === "entity") {
    created = await createRow(sql, gameId, "entities", {
      name: p.name, kind: p.kind ?? "character", summary: p.summary, aliases: p.aliases ?? [],
      timeline_id: await tl(p.timeline), source_ids,
    }, actor);
  } else if (s.kind === "event") {
    const timeline_id = (await tl(p.timeline)) ??
      (await sql`select id from timelines where game_id = ${gameId} order by (kind = 'canon') desc limit 1`)[0]?.id;
    const participants = [];
    for (const name of (p.participants as string[] | undefined) ?? []) {
      const eid = await ent(name);
      if (eid) participants.push({ entity_id: eid });
    }
    created = await createRow(sql, gameId, "events", {
      title: p.title, summary: p.summary, date_label: p.date_label, sort_key: Number(p.sort_key ?? 0),
      importance: Number(p.importance ?? 3), timeline_id, participants, source_ids,
    }, actor);
  } else {
    const source_id = await ent(p.source);
    const target_id = await ent(p.target);
    if (!source_id || !target_id) throw new Error("relationship needs two known entities");
    created = await createRow(sql, gameId, "relationships", {
      source_id, target_id, kind: p.kind ?? "other", description: p.description,
      timeline_id: await tl(p.timeline), source_ids,
    }, actor);
  }
  await sql`update suggestions set status = 'accepted' where id = ${id}`;
  return created;
}

export async function rejectSuggestion(sql: Sql, gameId: string, id: string) {
  const rows = await sql`update suggestions set status = 'rejected' where id = ${id} and game_id = ${gameId}
    returning id`;
  return rows.length > 0;
}
