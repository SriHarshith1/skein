import { db } from "./db";
import { getGame } from "./lore";

export function actorOf(req: Request) {
  return (req.headers.get("x-lore-actor") || "editor").slice(0, 60);
}

export async function gameOr404(slug: string) {
  const game = await getGame(db(), slug);
  return game;
}

export function fail(status: number, message: string) {
  return Response.json({ error: message }, { status });
}

// Postgres errors (bad uuid, check constraint, fk) become 400s with a readable message.
export function dbError(e: unknown) {
  const err = e as { code?: string; message?: string };
  if (err.code && /^(22|23)/.test(err.code)) return fail(400, err.message ?? "invalid data");
  return fail(500, err.message ?? "server error");
}
