import { db } from "@/lib/db";
import { listSuggestions } from "@/lib/lore";
import { fail, gameOr404 } from "@/lib/api";

export async function GET(req: Request, ctx: { params: Promise<{ game: string }> }) {
  const { game: slug } = await ctx.params;
  const game = await gameOr404(slug);
  if (!game) return fail(404, `unknown game ${slug}`);
  const status = new URL(req.url).searchParams.get("status") ?? "pending";
  return Response.json(await listSuggestions(db(), game.id, status));
}
