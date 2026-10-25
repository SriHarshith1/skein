import { connect } from "../src/lib/db";
import { scrapeGame } from "../src/lib/scrape";

// Usage: npm run scrape -- <game-slug> [--limit 20] [--refresh] [--page "Timeline"]...
const args = process.argv.slice(2);
const slug = args.find((a) => !a.startsWith("--") && !["--limit", "--page"].includes(args[args.indexOf(a) - 1]));
if (!slug) {
  console.error('usage: npm run scrape -- <game-slug> [--limit N] [--refresh] [--page "Title"]');
  process.exit(1);
}
const flag = (name: string) => args.flatMap((a, i) => (a === name ? [args[i + 1]] : []));
const sql = connect();
const result = await scrapeGame(sql, slug, {
  limit: flag("--limit")[0] ? Number(flag("--limit")[0]) : undefined,
  pages: flag("--page"),
  refresh: args.includes("--refresh"),
  log: (m) => console.log(m),
});
console.log(result);
await sql.end();
