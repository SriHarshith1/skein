import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { connect } from "../src/lib/db";
import { getBundle, listGames } from "../src/lib/lore";

// Writes public/data/home.json and one <slug>.json per game for the static Pages build.
const out = path.resolve(process.cwd(), "public/data");
await mkdir(out, { recursive: true });
const sql = connect();
const games = await listGames(sql);
const knots = await sql`select g.slug, t.name as timeline, e.importance from events e
  join games g on g.id = e.game_id join timelines t on t.id = e.timeline_id order by g.slug, e.sort_key, e.title`;
const bySlug: Record<string, { timeline: string; importance: number }[]> = {};
for (const k of knots) (bySlug[k.slug] ??= []).push({ timeline: k.timeline, importance: k.importance });
await writeFile(path.join(out, "home.json"), JSON.stringify({ games, knots: bySlug }));
for (const g of games) {
  const bundle = await getBundle(sql, g.slug);
  await writeFile(path.join(out, `${g.slug}.json`), JSON.stringify(bundle));
  console.log(`${g.slug}: ${bundle!.events.length} events, ${bundle!.entities.length} entities`);
}
await sql.end();
