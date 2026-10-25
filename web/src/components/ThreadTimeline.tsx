"use client";

// Lore as a skein: every timeline is a two-ply cord in the gutter, every event a knot.
// An alternate timeline peels off its parent cord at its first event; an AU (a separate
// continuity) starts with a loose loop instead. Knot size follows importance.

export type ThreadLane = { key: string; name: string; color: string; kind: string; parentKey: string | null };
export type ThreadEvent = {
  id: string; title: string; date_label: string | null; sort_key: number; summary: string | null;
  importance: number; era?: string | null; lane: string; participants: string[];
};

const LANE_W = 18;
const KNOT_Y = 21;

// Two plies: the dyed cord, then short dark stitches across it to read as twist.
function Cord({ x, y1, y2, color, faint }: { x: number; y1: number | string; y2: number | string; color: string; faint?: boolean }) {
  return (
    <g opacity={faint ? 0.45 : 1}>
      <line x1={x} x2={x} y1={y1} y2={y2} stroke={color} strokeWidth={3} strokeLinecap="round" />
      <line x1={x} x2={x} y1={y1} y2={y2} stroke="var(--ink)" strokeWidth={3} strokeDasharray="1.5 3.5" opacity={0.55} />
    </g>
  );
}

export function ThreadTimeline({
  events, lanes, onSelect, selectedId, compact = false,
}: {
  events: ThreadEvent[]; lanes: ThreadLane[]; onSelect?: (id: string) => void; selectedId?: string | null; compact?: boolean;
}) {
  const used = lanes.filter((l) => events.some((e) => e.lane === l.key));
  const index = new Map(used.map((l, i) => [l.key, i]));
  const sorted = [...events].sort((a, b) => a.sort_key - b.sort_key || a.title.localeCompare(b.title));
  const first = new Map<string, number>();
  const last = new Map<string, number>();
  sorted.forEach((e, i) => {
    if (!first.has(e.lane)) first.set(e.lane, i);
    last.set(e.lane, i);
  });
  const gutter = Math.max(1, used.length) * LANE_W + 10;
  const x = (key: string) => (index.get(key) ?? 0) * LANE_W + LANE_W / 2 + 3;

  if (!sorted.length) return null;

  return (
    <div>
      {used.length > 1 && (
        <ul className="mb-4 flex flex-wrap gap-x-4 gap-y-1.5">
          {used.map((l) => (
            <li key={l.key} className="inline-flex items-center gap-2 text-sm">
              <svg width="22" height="8" aria-hidden><line x1="0" x2="22" y1="4" y2="4" stroke={l.color} strokeWidth="3" /><line x1="0" x2="22" y1="4" y2="4" stroke="var(--ink)" strokeWidth="3" strokeDasharray="1.5 3.5" opacity="0.55" /></svg>
              {l.name}
              <span className="tag">{l.kind}</span>
            </li>
          ))}
        </ul>
      )}
      <ol className="relative">
        {sorted.map((e, i) => {
          const lane = used[index.get(e.lane) ?? 0];
          const prevEra = i > 0 ? sorted[i - 1].era : undefined;
          const showEra = !compact && e.era && e.era !== prevEra;
          const pk = lane?.parentKey;
          const parent = pk && index.has(pk) && first.get(pk)! < i && last.get(pk)! >= i ? pk : null;
          const isStart = first.get(e.lane) === i;
          const loose = isStart && !parent && lane?.kind !== "canon";
          const size = 5 + e.importance * 1.6;
          const threads = used.filter((l) => first.get(l.key)! <= i && last.get(l.key)! >= i);
          return (
            <li key={e.id}>
              {showEra && (
                <div className="flex">
                  <div className="relative shrink-0" style={{ width: gutter }}>
                    <svg className="absolute inset-0 h-full w-full" aria-hidden>
                      {threads.filter((l) => first.get(l.key)! < i).map((l) => (
                        <Cord key={l.key} x={x(l.key)} y1={0} y2="100%" color={l.color} faint />
                      ))}
                    </svg>
                  </div>
                  <p className="pb-2 pl-3 pt-6 font-display text-2xl font-extrabold uppercase text-chalk/90">{e.era}</p>
                </div>
              )}
              <div className="flex">
                <div className="relative shrink-0" style={{ width: gutter }}>
                  <svg className="absolute inset-0 h-full w-full overflow-visible" aria-hidden>
                    {threads.map((l) => (
                      <Cord key={l.key} x={x(l.key)} color={l.color} faint={l.key !== e.lane}
                        y1={first.get(l.key) === i ? KNOT_Y : 0} y2={last.get(l.key) === i ? KNOT_Y : "100%"} />
                    ))}
                    {isStart && parent && (
                      <path d={`M ${x(parent)} 0 C ${x(parent)} ${KNOT_Y}, ${x(e.lane)} 0, ${x(e.lane)} ${KNOT_Y}`}
                        fill="none" stroke={lane.color} strokeWidth={3} strokeLinecap="round" />
                    )}
                    {loose ? (
                      <ellipse cx={x(e.lane)} cy={KNOT_Y} rx={size / 2 + 2} ry={size / 2 + 4} fill="none" stroke={lane.color} strokeWidth={2.5} />
                    ) : (
                      <rect x={x(e.lane) - size / 2} y={KNOT_Y - size / 2} width={size} height={size} rx={2}
                        transform={`rotate(45 ${x(e.lane)} ${KNOT_Y})`} fill={lane?.color} stroke="var(--ink)" strokeWidth={2} />
                    )}
                  </svg>
                </div>
                <button
                  onClick={onSelect ? () => onSelect(e.id) : undefined}
                  disabled={!onSelect}
                  className={`mb-1 min-w-0 flex-1 rounded-[3px] border-l-2 px-3 py-2 text-left transition ${
                    selectedId === e.id ? "border-madder bg-raise" : "border-transparent hover:bg-panel"
                  } disabled:cursor-default`}
                >
                  <span className="block font-mono text-[11px]" style={{ color: lane?.color }}>{e.date_label || e.sort_key}</span>
                  <span className={`block text-[16px] font-semibold leading-snug ${e.importance >= 5 ? "text-white" : ""}`}>{e.title}</span>
                  {e.summary && (
                    <span className={`mt-0.5 block text-sm leading-relaxed text-chalk/70 ${compact ? "line-clamp-2" : "line-clamp-3"}`}>{e.summary}</span>
                  )}
                  {!compact && e.participants.length > 0 && (
                    <span className="mt-1 block truncate font-mono text-[10px] uppercase tracking-wider text-dim">{e.participants.join(" · ")}</span>
                  )}
                </button>
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
