import Link from "next/link";
import { connection } from "next/server";
import { db } from "@/lib/db";
import { listGames } from "@/lib/lore";
import { REPO_URL, STATIC } from "@/lib/static";
import { readFile } from "node:fs/promises";
import path from "node:path";

type GameRow = {
  slug: string; name: string; description: string | null;
  events: number; entities: number; relationships: number;
  timelines: { name: string; kind: string; color: string | null; events: number }[];
};
type Knot = { timeline: string; importance: number };

// One game's continuities as horizontal cords. Knots sit at each event's place in the
// game's story order, so a branch starts where its first event falls.
function Weave({ game, knots }: { game: GameRow; knots: Knot[] }) {
  const W = 1000;
  const rowH = 22;
  const lanes = game.timelines.filter((t) => t.events > 0);
  const H = lanes.length * rowH + 8;
  const n = Math.max(1, knots.length - 1);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="block w-full" role="img"
      aria-label={`${game.name}: ${lanes.map((t) => `${t.name}, ${t.events} events`).join("; ")}`}>
      {lanes.map((t, li) => {
        const y = li * rowH + 14;
        const xs = knots.map((k, i) => ({ ...k, x: 8 + (i / n) * (W - 16) })).filter((k) => k.timeline === t.name);
        if (!xs.length) return null;
        const x1 = xs[0].x;
        const x2 = xs[xs.length - 1].x;
        const color = t.color ?? "var(--flax)";
        const len = Math.max(1, x2 - x1);
        return (
          <g key={t.name}>
            <line x1={x1} x2={x2} y1={y} y2={y} stroke={color} strokeWidth={3} strokeLinecap="round" className="cord-draw"
              style={{ ["--len" as string]: len, animationDelay: `${li * 120}ms` }} />
            <line x1={x1} x2={x2} y1={y} y2={y} stroke="var(--ink)" strokeWidth={3} strokeDasharray="1.5 3.5" opacity={0.55} />
            {xs.map((k, i) => {
              const s = 3 + k.importance;
              return <rect key={i} x={k.x - s / 2} y={y - s / 2} width={s} height={s} rx={1.5} fill={color}
                transform={`rotate(45 ${k.x} ${y})`} stroke="var(--ink)" strokeWidth={1.5} />;
            })}
          </g>
        );
      })}
    </svg>
  );
}

type HomeData = { games: GameRow[]; knots: Map<string, Knot[]>; dbError: string | null };

// The Pages build reads JSON exported by `npm run export:data`; the local app reads Postgres.
async function loadHome(): Promise<HomeData> {
  const knots = new Map<string, Knot[]>();
  if (STATIC) {
    const data = JSON.parse(await readFile(path.join(process.cwd(), "public/data/home.json"), "utf8"));
    for (const [slug, list] of Object.entries(data.knots)) knots.set(slug, list as Knot[]);
    return { games: data.games, knots, dbError: null };
  }
  await connection();
  try {
    const sql = db();
    const games = (await listGames(sql)) as unknown as GameRow[];
    const rows = await sql`select g.slug, t.name as timeline, e.importance from events e
      join games g on g.id = e.game_id join timelines t on t.id = e.timeline_id order by g.slug, e.sort_key, e.title`;
    for (const r of rows) (knots.get(r.slug) ?? knots.set(r.slug, []).get(r.slug)!).push({ timeline: r.timeline, importance: r.importance });
    return { games, knots, dbError: null };
  } catch (e) {
    return { games: [], knots, dbError: (e as Error).message };
  }
}

export default async function Home() {
  const { games, knots, dbError } = await loadHome();

  return (
    <main className="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6">
      <header className="mb-14 grid gap-6 border-b border-line pb-10 sm:grid-cols-[auto_1fr] sm:items-end">
        <h1 className="font-display text-[clamp(88px,18vw,200px)] font-extrabold uppercase leading-[0.8] text-chalk">Skein</h1>
        <p className="max-w-md text-lg leading-relaxed text-chalk/80 sm:justify-self-end sm:pb-3">
          Game lore as thread. Canon runs undyed; every alternate timeline is a dyed cord that splits from it.
          Edit any knot, trace who is tied to whom, and ask the archive.
          {STATIC && (
            <span className="mt-3 block text-sm text-dim">
              This is a read-only copy. Editing and the Q&amp;A agent run locally:{" "}
              <a className="text-madder underline underline-offset-2" href={REPO_URL}>get Skein on GitHub</a>.
            </span>
          )}
        </p>
      </header>

      {dbError && (
        <div className="rounded-[3px] border border-danger/50 p-5 text-sm">
          <p className="font-semibold text-danger">The database is not reachable.</p>
          <p className="mt-1 text-dim">Start it with <code className="font-mono">npm run db</code>, then run <code className="font-mono">npm run db:seed</code>. Detail: {dbError}</p>
        </div>
      )}
      {!dbError && games.length === 0 && (
        <p className="text-dim">No games yet. Run <code className="font-mono">npm run db:seed</code> to load the research files.</p>
      )}

      <ul className="space-y-14">
        {games.map((g) => (
          <li key={g.slug}>
            <Link href={`/g/${g.slug}`} className="group block">
              <div className="mb-3 flex flex-wrap items-end justify-between gap-x-6 gap-y-1">
                <h2 className="font-display text-5xl font-extrabold uppercase transition group-hover:text-white sm:text-6xl">
                  {g.name}
                  <span aria-hidden className="ml-3 inline-block translate-y-[-0.1em] text-3xl text-madder opacity-0 transition group-hover:opacity-100">→</span>
                </h2>
                <p className="tag pb-2">{g.events} events · {g.entities} entities · {g.relationships} bonds · {g.timelines.length} timelines</p>
              </div>
              <Weave game={g} knots={knots.get(g.slug) ?? []} />
              <div className="mt-3 grid gap-4 sm:grid-cols-[1fr_auto]">
                {g.description && <p className="max-w-2xl text-[15px] leading-relaxed text-chalk/70">{g.description}</p>}
                <ul className="flex flex-wrap gap-x-4 gap-y-1 sm:max-w-sm sm:justify-end">
                  {g.timelines.filter((t) => t.events > 0).map((t) => (
                    <li key={t.name} className="inline-flex items-center gap-1.5 text-xs text-chalk/75">
                      <span className="inline-block h-[3px] w-3 rounded-full" style={{ background: t.color ?? "var(--flax)" }} />
                      {t.name}
                    </li>
                  ))}
                </ul>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
