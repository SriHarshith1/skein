import { z } from "zod";
import type { Sql } from "./db";
import { addSuggestion, getGame } from "./lore";
import type { LLM } from "./agent/llm";
import { RELATION_KINDS } from "./seed";

// Reads scraped passages and proposes events/relationships the database lacks.
// Proposals land in `suggestions` for a human to accept or reject.

const Extracted = z.object({
  events: z.array(z.object({
    title: z.string(), summary: z.string(), date_label: z.string().nullish(),
    sort_key: z.coerce.number().nullish(), participants: z.array(z.string()).default([]),
  })).default([]),
  relationships: z.array(z.object({
    source: z.string(), target: z.string(), kind: z.enum(RELATION_KINDS).catch("other"), description: z.string(),
  })).default([]),
});

export async function extractSuggestions(sql: Sql, llm: LLM, slug: string, opts: { entities?: number; log?: (m: string) => void } = {}) {
  const game = await getGame(sql, slug);
  if (!game) throw new Error(`unknown game ${slug}`);
  const log = opts.log ?? (() => {});
  const targets = await sql`select e.id, e.name from entities e
    where e.game_id = ${game.id} and exists (select 1 from lore_chunks c where c.entity_id = e.id)
      and not exists (select 1 from suggestions s where s.game_id = e.game_id and s.origin = 'scraper'
                      and s.payload ->> 'about' = e.name)
    order by e.name limit ${opts.entities ?? 5}`;
  let proposed = 0;
  for (const t of targets) {
    const chunks = await sql`select c.heading, c.content, s.url from lore_chunks c join sources s on s.id = c.source_id
      where c.entity_id = ${t.id} order by c.created_at limit 8`;
    const known = await sql`select title from events e join event_participants p on p.event_id = e.id
      where p.entity_id = ${t.id}`;
    const rels = await sql`select r.kind, s.name as a, x.name as b from relationships r
      join entities s on s.id = r.source_id join entities x on x.id = r.target_id
      where r.source_id = ${t.id} or r.target_id = ${t.id}`;
    const names = await sql`select name from entities where game_id = ${game.id}`;
    try {
      const raw = await llm.json(
        `You extract lore facts for ${game.name} from wiki passages. Return JSON only: ` +
          `{"events":[{"title","summary","date_label","sort_key","participants":[names]}],` +
          `"relationships":[{"source","target","kind","description"}]}. kind is one of ${RELATION_KINDS.join(", ")}. ` +
          `Only facts stated in the passages. Skip anything already known. At most 4 events and 6 relationships. ` +
          `Use character names exactly as in the known list when they match. Summaries in your own words.`,
        `Character: ${t.name}\nCalendar: ${game.calendar}\nKnown names: ${names.map((n) => n.name).join(", ")}\n` +
          `Already known events: ${known.map((k) => k.title).join("; ") || "none"}\n` +
          `Already known relationships: ${rels.map((r) => `${r.a} ${r.kind} ${r.b}`).join("; ") || "none"}\n\n` +
          chunks.map((c) => `### ${c.heading}\n${c.content}`).join("\n\n"),
      );
      const out = Extracted.parse(raw);
      const url = chunks[0]?.url;
      for (const e of out.events) {
        await addSuggestion(sql, game.id, { kind: "event", payload: { ...e, about: t.name }, rationale: `Extracted from ${t.name}'s wiki page`, source_url: url, origin: "scraper" });
        proposed++;
      }
      for (const r of out.relationships) {
        await addSuggestion(sql, game.id, { kind: "relationship", payload: { ...r, about: t.name }, rationale: `Extracted from ${t.name}'s wiki page`, source_url: url, origin: "scraper" });
        proposed++;
      }
      log(`${t.name}: ${out.events.length} events, ${out.relationships.length} relationships proposed`);
    } catch (e) {
      log(`${t.name}: ${(e as Error).message}`);
    }
  }
  return { game: slug, entities: targets.length, proposed };
}
