import { db } from "@/lib/db";
import { acceptSuggestion, rejectSuggestion } from "@/lib/lore";
import { actorOf, dbError, fail, gameOr404 } from "@/lib/api";

// Body: {"action": "accept" | "reject"}
export async function PATCH(req: Request, ctx: RouteContext<"/api/games/[game]/suggestions/[id]">) {
  const { game: slug, id } = await ctx.params;
  const game = await gameOr404(slug);
  if (!game) return fail(404, `unknown game ${slug}`);
  const { action } = await req.json();
  try {
    if (action === "reject") return (await rejectSuggestion(db(), game.id, id)) ? Response.json({ ok: true }) : fail(404, "not found");
    const created = await acceptSuggestion(db(), game.id, id, actorOf(req));
    return created ? Response.json(created) : fail(404, "not found or already handled");
  } catch (e) {
    return dbError(e);
  }
}
