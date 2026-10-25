import type { Sql } from "./db";
import { getGame } from "./lore";
import { chunkText, wikiPage, wikiSearch, type WikiPage } from "./wiki";

const MAX_CHUNKS_PER_PAGE = 40;

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export type ScrapeOptions = {
  limit?: number;          // max entity pages this run
  pages?: string[];        // extra wiki pages (e.g. "Timeline") not tied to an entity
  refresh?: boolean;       // re-fetch entities that already have chunks
  delayMs?: number;        // politeness delay between requests
  log?: (msg: string) => void;
};

export function titleFromUrl(url: string) {
  return decodeURIComponent(url.split("/wiki/")[1] ?? "").replace(/_/g, " ").replace(/[#?].*$/, "");
}

async function storePage(sql: Sql, gameId: string, page: WikiPage, entityId: string | null) {
  const key = `wiki:${page.title}`.slice(0, 120);
  const [src] = await sql`insert into sources (game_id, key, url, title, publisher)
    values (${gameId}, ${key}, ${page.url}, ${page.title}, 'wiki')
    on conflict (game_id, key) do update set url = excluded.url, retrieved_at = now()
    returning id`;
  await sql`delete from lore_chunks where source_id = ${src.id}`;
  let n = 0;
  for (const section of page.sections) {
    for (const content of chunkText(section.text)) {
      if (n >= MAX_CHUNKS_PER_PAGE) break;
      await sql`insert into lore_chunks (game_id, source_id, entity_id, heading, content)
        values (${gameId}, ${src.id}, ${entityId}, ${section.heading}, ${content})`;
      n++;
    }
  }
  if (entityId) {
    await sql`insert into citations (source_id, subject_type, subject_id) values (${src.id}, 'entity', ${entityId})
      on conflict do nothing`;
  }
  return n;
}

// Fetches each entity's wiki page into lore_chunks (the archivist's search corpus).
export async function scrapeGame(sql: Sql, slug: string, opts: ScrapeOptions = {}) {
  const log = opts.log ?? (() => {});
  const game = await getGame(sql, slug);
  if (!game) throw new Error(`unknown game ${slug}`);
  if (!game.wiki_api) throw new Error(`${slug} has no wiki_api; set it in research/${slug}.json`);
  const delay = opts.delayMs ?? 1200;
  // Research files cite wiki pages per entity; a cited page named after the entity beats guessing.
  const host = new URL(game.wiki_api).host;
  const entities = await sql`select e.id, e.name, e.kind, coalesce(e.attributes ->> 'wiki_title', (
        select s.url from citations c join sources s on s.id = c.source_id
        where c.subject_type = 'entity' and c.subject_id = e.id and s.url like ${"%" + host + "%/wiki/%"}
          and s.url ilike '%' || replace(e.name, ' ', '_') || '%'
        order by length(s.url) limit 1)) as wiki_title
    from entities e where e.game_id = ${game.id} and e.variant_of is null
      and (${!!opts.refresh} or not exists (select 1 from lore_chunks c where c.entity_id = e.id))
    order by (e.kind = 'character') desc, e.name
    limit ${opts.limit ?? 1000}`;
  let pages = 0;
  let chunks = 0;
  const missing: string[] = [];
  const stored = new Set<string>();
  for (const e of entities) {
    try {
      const cited = e.wiki_title?.includes("/wiki/") ? titleFromUrl(e.wiki_title) : e.wiki_title;
      // Common lore-page conventions across wikis, most specific first.
      const candidates = [cited, `${e.name}/Lore`, `${e.name} (character)`, e.name].filter(
        (t, i, all): t is string => !!t && all.indexOf(t) === i,
      );
      let page: WikiPage | null = null;
      for (const title of candidates) {
        if (stored.has(title)) break;
        page = await wikiPage(game.wiki_api, title).catch(() => null);
        if (page?.sections.length) break;
        page = null;
        await sleep(delay / 3);
      }
      if (!page && !candidates.some((t) => stored.has(t))) {
        const [hit] = await wikiSearch(game.wiki_api, e.name, 1);
        if (hit && !stored.has(hit.title)) page = await wikiPage(game.wiki_api, hit.title);
      }
      if (!page) {
        missing.push(e.name);
      } else {
        stored.add(page.title);
        const n = await storePage(sql, game.id, page, e.id);
        pages++;
        chunks += n;
        log(`${e.name} <- ${page.title} (${n} chunks)`);
      }
    } catch (err) {
      missing.push(e.name);
      log(`${e.name}: ${(err as Error).message}`);
    }
    await sleep(delay);
  }
  for (const title of opts.pages ?? []) {
    const page = await wikiPage(game.wiki_api, title).catch(() => null);
    if (page) {
      const n = await storePage(sql, game.id, page, null);
      pages++;
      chunks += n;
      log(`page ${title} (${n} chunks)`);
    } else missing.push(title);
    await sleep(delay);
  }
  return { game: slug, pages, chunks, missing };
}

// One page for one entity (the "fetch from wiki" button in the editor).
export async function scrapeEntity(sql: Sql, game: { id: string; wiki_api: string | null }, entityId: string, title?: string) {
  if (!game.wiki_api) throw new Error("this game has no wiki configured");
  const [e] = await sql`select id, name from entities where id = ${entityId} and game_id = ${game.id}`;
  if (!e) throw new Error("unknown entity");
  let page = await wikiPage(game.wiki_api, title || e.name);
  if (!page || !page.sections.length) {
    const [hit] = await wikiSearch(game.wiki_api, title || e.name, 1);
    page = hit ? await wikiPage(game.wiki_api, hit.title) : null;
  }
  if (!page) return { found: false };
  await sql`update entities set attributes = attributes || ${sql.json({ wiki_title: page.title })} where id = ${e.id}`;
  return { found: true, title: page.title, url: page.url, chunks: await storePage(sql, game.id, page, e.id) };
}
