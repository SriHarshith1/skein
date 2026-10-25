import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import type { Sql } from "./db";

export const MIGRATIONS_DIR = path.resolve(process.cwd(), "../supabase/migrations");

// Applies supabase/migrations/*.sql in name order, once each. The RLS file
// needs Supabase's anon/authenticated roles, so it is skipped where they are absent.
export async function migrate(sql: Sql, dir = MIGRATIONS_DIR): Promise<string[]> {
  await sql`create table if not exists lorelines_migrations (
    name text primary key, applied_at timestamptz not null default now())`;
  const done = new Set((await sql`select name from lorelines_migrations`).map((r) => r.name));
  const [{ supabase }] = await sql`select exists(select 1 from pg_roles where rolname = 'anon') as supabase`;
  const files = (await readdir(dir)).filter((f) => f.endsWith(".sql")).sort();
  const applied: string[] = [];
  for (const file of files) {
    if (done.has(file)) continue;
    if (file.includes("_rls") && !supabase) continue;
    const text = await readFile(path.join(dir, file), "utf8");
    await sql.unsafe(text);
    await sql`insert into lorelines_migrations (name) values (${file})`;
    applied.push(file);
  }
  return applied;
}
