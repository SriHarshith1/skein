import { PGlite } from "@electric-sql/pglite";
import { PGLiteSocketServer } from "@electric-sql/pglite-socket";
import { readFileSync } from "node:fs";
import path from "node:path";
import { connect, type Sql } from "../src/lib/db";
import { migrate } from "../src/lib/migrate";
import { loadSeed, parseSeed } from "../src/lib/seed";

export const fixture = () =>
  JSON.parse(readFileSync(path.join(__dirname, "fixtures/testverse.json"), "utf8"));

// A fresh in-memory Postgres per test file, reached the same way as Supabase.
export async function startDb() {
  const pg = await PGlite.create();
  const port = 40000 + Math.floor(Math.random() * 20000);
  const server = new PGLiteSocketServer({ db: pg, port, host: "127.0.0.1", maxConnections: 4 } as never);
  await server.start();
  const sql = connect(`postgres://postgres:postgres@127.0.0.1:${port}/postgres`);
  await migrate(sql, path.resolve(__dirname, "../../supabase/migrations"));
  const { seed } = parseSeed(fixture());
  await loadSeed(sql, seed);
  const [{ id: gameId }] = await sql`select id from games where slug = 'testverse'`;
  return {
    sql,
    gameId: gameId as string,
    stop: async () => {
      await sql.end();
      await server.stop();
      await pg.close();
    },
  };
}

export async function idOf(sql: Sql, slug: string) {
  const [r] = await sql`select id from entities where slug = ${slug}
    union all select id from events where slug = ${slug}
    union all select id from timelines where slug = ${slug}`;
  return r.id as string;
}
