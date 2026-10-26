import { readFile } from "node:fs/promises";
import path from "node:path";
import { GameApp } from "@/components/GameApp";
import { STATIC } from "@/lib/static";

// The Pages build pre-renders one page per exported game; the local app renders on demand.
export async function generateStaticParams() {
  if (!STATIC) return [];
  const data = JSON.parse(await readFile(path.join(process.cwd(), "public/data/home.json"), "utf8"));
  return (data.games as { slug: string }[]).map((g) => ({ game: g.slug }));
}

export default async function GamePage({ params }: PageProps<"/g/[game]">) {
  const { game } = await params;
  return <GameApp slug={game} />;
}
