import { db } from "@/lib/db";
import { listGames } from "@/lib/lore";

export async function GET() {
  return Response.json(await listGames(db()));
}
