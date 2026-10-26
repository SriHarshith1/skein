import { db } from "@/lib/db";
import { getBundle } from "@/lib/lore";
import { fail } from "@/lib/api";

export async function GET(_req: Request, ctx: { params: Promise<{ game: string }> }) {
  const { game } = await ctx.params;
  const bundle = await getBundle(db(), game);
  return bundle ? Response.json(bundle) : fail(404, `unknown game ${game}`);
}
