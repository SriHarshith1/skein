import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { connect } from "../src/lib/db";
import { migrate } from "../src/lib/migrate";
import { loadSeed, parseSeed } from "../src/lib/seed";

// Usage: npm run db:seed [-- game-slug ...]   (default: every research/*.json)
const dir = path.resolve(process.cwd(), "../research");
const only = process.argv.slice(2);
const files = (await readdir(dir)).filter(
  (f) => f.endsWith(".json") && (only.length === 0 || only.includes(f.replace(/\.json$/, ""))),
);

const sql = connect();
await migrate(sql);
for (const file of files) {
  const { seed, problems } = parseSeed(JSON.parse(await readFile(path.join(dir, file), "utf8")));
  if (problems.length) {
    console.warn(`${file}: ${problems.length} broken references (rows skipped)`);
    for (const p of problems.slice(0, 10)) console.warn(`  - ${p}`);
  }
  console.log(await loadSeed(sql, seed));
}
await sql.end();
