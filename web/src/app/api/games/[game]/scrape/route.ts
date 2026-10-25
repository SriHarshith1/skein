import { db } from "@/lib/db";
import { scrapeEntity } from "@/lib/scrape";
import { dbError, fail, gameOr404 } from "@/lib/api";

// Body: {"entity_id": "...", "title"?: "Wiki page title"} — pulls one wiki page into the lore corpus.
export async function POST(req: Request, ctx: RouteContext<"/api/games/[game]/scrape">) {
  const { game: slug } = await ctx.params;
  const game = await gameOr404(slug);
  if (!game) return fail(404, `unknown game ${slug}`);
  const { entity_id, title } = await req.json();
  try {
    return Response.json(await scrapeEntity(db(), game, entity_id, title));
  } catch (e) {
    return dbError(e);
  }
}
