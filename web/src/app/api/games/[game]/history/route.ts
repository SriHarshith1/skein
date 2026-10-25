import { db } from "@/lib/db";
import { history, recentRevisions } from "@/lib/lore";
import { fail, gameOr404 } from "@/lib/api";

export async function GET(req: Request, ctx: RouteContext<"/api/games/[game]/history">) {
  const { game: slug } = await ctx.params;
  const game = await gameOr404(slug);
  if (!game) return fail(404, `unknown game ${slug}`);
  const row = new URL(req.url).searchParams.get("row");
  return Response.json(row ? await history(db(), row) : await recentRevisions(db(), game.id));
}
