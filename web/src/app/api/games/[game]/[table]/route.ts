import { db } from "@/lib/db";
import { createRow, isEditableTable } from "@/lib/lore";
import { actorOf, dbError, fail, gameOr404 } from "@/lib/api";

export async function POST(req: Request, ctx: { params: Promise<{ game: string; table: string }> }) {
  const { game: slug, table } = await ctx.params;
  if (!isEditableTable(table)) return fail(404, `cannot edit ${table}`);
  const game = await gameOr404(slug);
  if (!game) return fail(404, `unknown game ${slug}`);
  try {
    return Response.json(await createRow(db(), game.id, table, await req.json(), actorOf(req)), { status: 201 });
  } catch (e) {
    return dbError(e);
  }
}
