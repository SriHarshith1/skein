import { z } from "zod";
import type { Sql } from "./db";

// The research seed format (research/<game>.json). Slugs link rows inside one file.

const slug = z.string().regex(/^[a-z0-9][a-z0-9-]*$/, "lowercase-kebab slug");
const keys = z.array(z.string()).default([]);

export const RELATION_KINDS = [
  "family", "sibling", "parent", "romance", "ally", "friend", "rival", "enemy",
  "mentor", "member", "leader", "creator", "variant", "other",
] as const;
export const ENTITY_KINDS = ["character", "faction", "place", "artifact", "organization"] as const;
export const TIMELINE_KINDS = ["canon", "alternate", "au"] as const;

export const SeedSchema = z.object({
  game: z.object({
    slug,
    name: z.string(),
    calendar: z.string().nullish(),
    description: z.string().nullish(),
  }),
  wiki: z
    .object({
      base: z.string().nullish(),
      api: z.string().nullish(),
      license: z.string().nullish(),
      notes: z.string().nullish(),
    })
    .partial()
    .default({}),
  sources: z.array(
    z.object({
      key: z.string(),
      url: z.string(),
      title: z.string().nullish(),
      publisher: z.enum(["official", "wiki", "other", "user"]).catch("other"),
    }),
  ),
  timelines: z.array(
    z.object({
      slug,
      name: z.string(),
      kind: z.enum(TIMELINE_KINDS).catch("alternate"),
      parent: slug.nullish(),
      branch_note: z.string().nullish(),
      description: z.string().nullish(),
    }),
  ),
  entities: z.array(
    z.object({
      slug,
      name: z.string(),
      kind: z.enum(ENTITY_KINDS).catch("character"),
      timeline: slug.nullish(),
      variant_of: slug.nullish(),
      aliases: z.array(z.string()).default([]),
      summary: z.string().nullish(),
      sources: keys,
    }),
  ),
  events: z.array(
    z.object({
      slug,
      timeline: slug,
      title: z.string(),
      summary: z.string().nullish(),
      date_label: z.union([z.string(), z.number()]).transform(String).nullish(),
      sort_key: z.coerce.number(),
      era: z.string().nullish(),
      importance: z.coerce.number().int().min(1).max(5).catch(3),
      participants: z
        .array(z.object({ entity: slug, role: z.string().nullish() }))
        .default([]),
      sources: keys,
    }),
  ),
  relationships: z.array(
    z.object({
      source: slug,
      target: slug,
      kind: z.enum(RELATION_KINDS).catch("other"),
      timeline: slug.nullish(),
      description: z.string().nullish(),
      since_event: slug.nullish(),
      until_event: slug.nullish(),
      sources: keys,
    }),
  ),
});

export type Seed = z.infer<typeof SeedSchema>;

// Reports every slug or source key that points at nothing.
export function checkReferences(seed: Seed): string[] {
  const problems: string[] = [];
  const tl = new Set(seed.timelines.map((t) => t.slug));
  const en = new Set(seed.entities.map((e) => e.slug));
  const ev = new Set(seed.events.map((e) => e.slug));
  const src = new Set(seed.sources.map((s) => s.key));
  const need = (set: Set<string>, value: string | null | undefined, where: string) => {
    if (value && !set.has(value)) problems.push(`${where}: unknown "${value}"`);
  };
  for (const t of seed.timelines) need(tl, t.parent, `timeline ${t.slug}.parent`);
  for (const e of seed.entities) {
    need(tl, e.timeline, `entity ${e.slug}.timeline`);
    need(en, e.variant_of, `entity ${e.slug}.variant_of`);
    e.sources.forEach((s) => need(src, s, `entity ${e.slug}.sources`));
  }
  for (const e of seed.events) {
    need(tl, e.timeline, `event ${e.slug}.timeline`);
    e.participants.forEach((p) => need(en, p.entity, `event ${e.slug}.participants`));
    e.sources.forEach((s) => need(src, s, `event ${e.slug}.sources`));
  }
  seed.relationships.forEach((r, i) => {
    const where = `relationship #${i} ${r.source}->${r.target}`;
    need(en, r.source, where);
    need(en, r.target, where);
    need(tl, r.timeline, `${where}.timeline`);
    need(ev, r.since_event, `${where}.since_event`);
    need(ev, r.until_event, `${where}.until_event`);
    r.sources.forEach((s) => need(src, s, `${where}.sources`));
  });
  return problems;
}

export function parseSeed(json: unknown): { seed: Seed; problems: string[] } {
  const seed = SeedSchema.parse(json);
  return { seed, problems: checkReferences(seed) };
}

// Canon is the undyed thread (flax); every other continuity gets a natural dye.
export const CANON_COLOR = "#d9c9a3";
// indigo, madder, weld, woad, cochineal, lichen, murex, walnut, logwood, saffron
export const TIMELINE_COLORS = ["#6f8fe0", "#d9573f", "#e3b23c", "#3fa39b", "#c4467f", "#93b36b", "#9a74e0", "#b0805a", "#7275cc", "#f0884a"];

// Replaces one game's lore with the seed, in one transaction. Rows with broken
// references are skipped, not fatal: research data is never perfect.
export async function loadSeed(sql: Sql, seed: Seed) {
  return sql.begin(async (tx) => {
    await tx`select set_config('lorelines.actor', 'seed', true)`;
    const { game, wiki } = seed;
    const [g] = await tx`
      insert into games (slug, name, calendar, description, wiki_base, wiki_api, wiki_license)
      values (${game.slug}, ${game.name}, ${game.calendar ?? null}, ${game.description ?? null},
              ${wiki.base ?? null}, ${wiki.api ?? null}, ${wiki.license ?? null})
      on conflict (slug) do update set name = excluded.name, calendar = excluded.calendar,
        description = excluded.description, wiki_base = excluded.wiki_base,
        wiki_api = excluded.wiki_api, wiki_license = excluded.wiki_license
      returning id`;
    const gid: string = g.id;
    // Wipe lore but keep scraped chunks' sources stable by key.
    await tx`delete from relationships where game_id = ${gid}`;
    await tx`delete from events where game_id = ${gid}`;
    await tx`delete from entities where game_id = ${gid}`;
    await tx`delete from timelines where game_id = ${gid}`;
    await tx`delete from citations c using sources s where c.source_id = s.id and s.game_id = ${gid}`;

    const sourceId = new Map<string, string>();
    for (const s of seed.sources) {
      const [row] = await tx`
        insert into sources (game_id, key, url, title, publisher)
        values (${gid}, ${s.key}, ${s.url}, ${s.title ?? null}, ${s.publisher})
        on conflict (game_id, key) do update set url = excluded.url, title = excluded.title,
          publisher = excluded.publisher
        returning id`;
      sourceId.set(s.key, row.id);
    }
    const cite = async (type: string, id: string, srcKeys: string[]) => {
      for (const k of new Set(srcKeys)) {
        const sid = sourceId.get(k);
        if (sid) {
          await tx`insert into citations (source_id, subject_type, subject_id)
                   values (${sid}, ${type}, ${id}) on conflict do nothing`;
        }
      }
    };

    const timelineId = new Map<string, string>();
    let hue = 0;
    for (const t of seed.timelines) {
      const color = t.kind === "canon" ? CANON_COLOR : TIMELINE_COLORS[hue++ % TIMELINE_COLORS.length];
      const [row] = await tx`
        insert into timelines (game_id, slug, name, kind, branch_note, description, color)
        values (${gid}, ${t.slug}, ${t.name}, ${t.kind}, ${t.branch_note ?? null},
                ${t.description ?? null}, ${color})
        returning id`;
      timelineId.set(t.slug, row.id);
    }
    for (const t of seed.timelines) {
      const parent = t.parent ? timelineId.get(t.parent) : undefined;
      if (parent) await tx`update timelines set parent_id = ${parent} where id = ${timelineId.get(t.slug)!}`;
    }

    const entityId = new Map<string, string>();
    for (const e of seed.entities) {
      if (entityId.has(e.slug)) continue;
      const [row] = await tx`
        insert into entities (game_id, slug, name, kind, timeline_id, aliases, summary)
        values (${gid}, ${e.slug}, ${e.name}, ${e.kind},
                ${e.timeline ? (timelineId.get(e.timeline) ?? null) : null},
                ${e.aliases}, ${e.summary ?? null})
        returning id`;
      entityId.set(e.slug, row.id);
      await cite("entity", row.id, e.sources);
    }
    for (const e of seed.entities) {
      const v = e.variant_of ? entityId.get(e.variant_of) : undefined;
      if (v) await tx`update entities set variant_of = ${v} where id = ${entityId.get(e.slug)!}`;
    }

    const eventId = new Map<string, string>();
    let skipped = 0;
    for (const e of seed.events) {
      const tid = timelineId.get(e.timeline);
      if (!tid || eventId.has(e.slug)) {
        skipped++;
        continue;
      }
      const [row] = await tx`
        insert into events (game_id, timeline_id, slug, title, summary, date_label, sort_key, era, importance)
        values (${gid}, ${tid}, ${e.slug}, ${e.title}, ${e.summary ?? null}, ${e.date_label ?? null},
                ${e.sort_key}, ${e.era ?? null}, ${e.importance})
        returning id`;
      eventId.set(e.slug, row.id);
      for (const p of e.participants) {
        const en = entityId.get(p.entity);
        if (en) {
          await tx`insert into event_participants (event_id, entity_id, role)
                   values (${row.id}, ${en}, ${p.role ?? null}) on conflict do nothing`;
        }
      }
      await cite("event", row.id, e.sources);
    }

    let relations = 0;
    for (const r of seed.relationships) {
      const s = entityId.get(r.source);
      const t = entityId.get(r.target);
      if (!s || !t || s === t) {
        skipped++;
        continue;
      }
      const [row] = await tx`
        insert into relationships (game_id, source_id, target_id, kind, timeline_id, description,
                                   since_event_id, until_event_id)
        values (${gid}, ${s}, ${t}, ${r.kind},
                ${r.timeline ? (timelineId.get(r.timeline) ?? null) : null},
                ${r.description ?? null},
                ${r.since_event ? (eventId.get(r.since_event) ?? null) : null},
                ${r.until_event ? (eventId.get(r.until_event) ?? null) : null})
        returning id`;
      relations++;
      await cite("relationship", row.id, r.sources);
    }
    // Variant links double as graph edges so the multiverse view can cross timelines.
    for (const e of seed.entities) {
      const v = e.variant_of ? entityId.get(e.variant_of) : undefined;
      const me = entityId.get(e.slug);
      if (v && me && v !== me) {
        await tx`insert into relationships (game_id, source_id, target_id, kind, description)
                 select ${gid}, ${me}, ${v}, 'variant', ${`${e.name} is a variant of this character.`}
                 where not exists (select 1 from relationships where source_id = ${me}
                                   and target_id = ${v} and kind = 'variant')`;
      }
    }
    return {
      game: game.slug,
      timelines: timelineId.size,
      entities: entityId.size,
      events: eventId.size,
      relationships: relations,
      sources: sourceId.size,
      skipped,
    };
  });
}
