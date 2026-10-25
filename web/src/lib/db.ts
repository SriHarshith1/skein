import postgres from "postgres";

// One driver for both backends: the local PGlite socket server (npm run db)
// and a hosted Supabase project (set DATABASE_URL to its connection string).
export const LOCAL_DATABASE_URL = "postgres://postgres:postgres@127.0.0.1:54322/postgres";

export type Sql = postgres.Sql;

export function connect(url = process.env.DATABASE_URL || LOCAL_DATABASE_URL): Sql {
  const local = url.includes("127.0.0.1") || url.includes("localhost");
  return postgres(url, {
    // Supabase's transaction pooler does not support prepared statements.
    prepare: false,
    ssl: local ? false : "require",
    max: local ? 1 : 10,
    idle_timeout: 20,
    onnotice: () => {},
  });
}

const globalForDb = globalThis as unknown as { loreSql?: Sql };

export function db(): Sql {
  globalForDb.loreSql ??= connect();
  return globalForDb.loreSql;
}
