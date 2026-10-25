import { db } from "@/lib/db";
import { deleteRow, isEditableTable, updateRow } from "@/lib/lore";
import { actorOf, dbError, fail, gameOr404 } from "@/lib/api";

type Ctx = RouteContext<"/api/games/[game]/[table]/[id]">;

async function target(ctx: Ctx) {
  const { game: slug, table, id } = await ctx.params;
  if (!isEditableTable(table)) return { error: fail(404, `cannot edit ${table}`) };
  const game = await gameOr404(slug);
  if (!game) return { error: fail(404, `unknown game ${slug}`) };
  return { game, table, id };
}

export async function PATCH(req: Request, ctx: Ctx) {
  const t = await target(ctx);
  if ("error" in t) return t.error;
  try {
    const row = await updateRow(db(), t.game.id, t.table, t.id, await req.json(), actorOf(req));
    return row ? Response.json(row) : fail(404, "not found");
  } catch (e) {
    return dbError(e);
  }
}

export async function DELETE(req: Request, ctx: Ctx) {
  const t = await target(ctx);
  if ("error" in t) return t.error;
  try {
    return (await deleteRow(db(), t.game.id, t.table, t.id, actorOf(req)))
      ? new Response(null, { status: 204 })
      : fail(404, "not found");
  } catch (e) {
    return dbError(e);
  }
}
