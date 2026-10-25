import { GameApp } from "@/components/GameApp";

export default async function GamePage({ params }: PageProps<"/g/[game]">) {
  const { game } = await params;
  return <GameApp slug={game} />;
}
