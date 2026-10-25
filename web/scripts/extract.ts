import { connect } from "../src/lib/db";
import { defaultLLM } from "../src/lib/agent/llm";
import { extractSuggestions } from "../src/lib/extract";

// Usage: npm run extract -- <game-slug> [--entities 5]
const [slug, flag, n] = process.argv.slice(2);
if (!slug) {
  console.error("usage: npm run extract -- <game-slug> [--entities N]");
  process.exit(1);
}
const sql = connect();
console.log(await extractSuggestions(sql, defaultLLM(), slug, { entities: flag === "--entities" ? Number(n) : 5, log: console.log }));
await sql.end();
