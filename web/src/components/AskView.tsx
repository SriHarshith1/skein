"use client";

import { useMemo, useRef, useState } from "react";
import Markdown from "react-markdown";
import type { UIBlock } from "@/lib/agent/blocks";
import type { AgentName, AskEvent } from "@/lib/agent/orchestrator";
import type { Bundle } from "./client";
import { Blocks } from "./Blocks";
import { Button } from "./ui";

type AgentState = { agent: AgentName; title: string; task: string; tools: string[]; done: boolean; findings?: string };
type Exchange = {
  question: string; model?: string; agents: AgentState[]; answer?: string; blocks?: UIBlock[]; error?: string;
};

// Example questions built from this game's own data, so they work for any game.
function examples(bundle: Bundle) {
  const deg = new Map<string, number>();
  bundle.relationships.forEach((r) => [r.source_id, r.target_id].forEach((id) => deg.set(id, (deg.get(id) ?? 0) + 1)));
  const chars = bundle.entities.filter((e) => e.kind === "character").sort((a, b) => (deg.get(b.id) ?? 0) - (deg.get(a.id) ?? 0));
  const variant = bundle.entities.find((e) => e.variant_of);
  const alt = bundle.timelines.find((t) => t.kind !== "canon");
  const top = bundle.events.filter((e) => e.importance >= 5)[0];
  return [
    chars[0] && `Who are ${chars[0].name}'s closest allies and worst enemies?`,
    chars[1] && chars[2] && `How is ${chars[1].name} connected to ${chars[2].name}?`,
    variant && `How does ${variant.name} differ from the original?`,
    alt && `What happens in the ${alt.name} timeline, and how does it branch from canon?`,
    top && `What led up to "${top.title}" and what came after?`,
  ].filter(Boolean) as string[];
}

export function AskView({ bundle, onChanged }: { bundle: Bundle; onChanged: () => void }) {
  const slug = bundle.game.slug;
  const [log, setLog] = useState<Exchange[]>([]);
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);
  const bottom = useRef<HTMLDivElement>(null);
  const ideas = useMemo(() => examples(bundle), [bundle]);

  const update = (fn: (x: Exchange) => Exchange) =>
    setLog((l) => [...l.slice(0, -1), fn(l[l.length - 1])]);

  const send = async (question: string) => {
    if (!question.trim() || busy) return;
    const history = log.flatMap((x) => [
      { role: "user" as const, content: x.question },
      ...(x.answer ? [{ role: "assistant" as const, content: x.answer }] : []),
    ]);
    setLog((l) => [...l, { question, agents: [] }]);
    setQ("");
    setBusy(true);
    try {
      const res = await fetch(`/api/games/${slug}/ask`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ question, history }),
      });
      if (!res.ok || !res.body) throw new Error((await res.json().catch(() => ({}))).error ?? `request failed (${res.status})`);
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop() ?? "";
        for (const line of lines) {
          if (!line.trim()) continue;
          const ev = JSON.parse(line) as AskEvent;
          update((x) => apply(x, ev));
          if (ev.type === "answer") {
            if (ev.blocks.some((b) => b.type === "suggestion")) onChanged();
            setTimeout(() => bottom.current?.scrollIntoView({ behavior: "smooth", block: "end" }), 50);
          }
        }
      }
    } catch (e) {
      update((x) => ({ ...x, error: (e as Error).message }));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl">
      {log.length === 0 && (
        <div className="mb-8">
          <h2 className="font-display text-2xl font-bold">Ask the archive</h2>
          <p className="mt-1 text-sm text-dim">
            A planner splits your question between specialist subagents: the Chronicler (dates and order), the Cartographer
            (relationships), the Multiverse analyst (alternate timelines and variants), the Archivist (scraped wiki text) and the
            Scout (live wiki, proposes edits). The narrator then answers with timelines, graphs and cards.
          </p>
          <ul className="mt-4 flex flex-col gap-2">
            {ideas.map((idea) => (
              <li key={idea}>
                <button onClick={() => send(idea)} className="rounded-[3px] border border-line px-3 py-1.5 text-left text-sm hover:border-madder hover:bg-panel">
                  {idea}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="space-y-8">
        {log.map((x, i) => (
          <article key={i}>
            <p className="font-display text-lg font-semibold">{x.question}</p>
            {x.agents.length > 0 && (
              <ul className="mt-2 space-y-1">
                {x.agents.map((a) => (
                  <li key={a.agent}>
                    <details className="group text-sm">
                      <summary className="flex cursor-pointer list-none items-center gap-2 text-dim">
                        <span className={`inline-block h-2 w-2 rounded-full ${a.done ? "bg-emerald-400" : "animate-pulse bg-madder"}`} />
                        <b className="text-chalk">{a.title}</b>
                        <span className="truncate">{a.task}</span>
                        <span className="ml-auto shrink-0 font-mono text-[11px]">{a.tools.length} tool calls</span>
                      </summary>
                      <div className="ml-4 mt-1 border-l border-line pl-3 text-xs text-dim">
                        {a.tools.map((t, j) => <p key={j} className="font-mono">→ {t}</p>)}
                        {a.findings && <div className="prose-lore mt-1 whitespace-pre-wrap text-chalk/70">{a.findings}</div>}
                      </div>
                    </details>
                  </li>
                ))}
              </ul>
            )}
            {x.model && !x.answer && !x.error && <p className="mt-2 text-xs text-dim">Working with {x.model}…</p>}
            {x.answer && (
              <div className="prose-lore mt-3 text-[15px]">
                <Markdown>{x.answer}</Markdown>
              </div>
            )}
            {x.blocks && <Blocks blocks={x.blocks} slug={slug} onChanged={onChanged} />}
            {x.error && <p className="mt-2 text-sm text-danger">The agent stopped: {x.error}. Check that Ollama is running, then ask again.</p>}
          </article>
        ))}
      </div>
      <div ref={bottom} />
      <form onSubmit={(e) => { e.preventDefault(); send(q); }}
        className="sticky bottom-0 mt-8 flex gap-2 border-t border-line bg-ink/95 py-4 backdrop-blur">
        <input className="field" value={q} onChange={(e) => setQ(e.target.value)} disabled={busy}
          placeholder={busy ? "The subagents are working…" : "Ask about events, relationships or alternate timelines"} />
        <Button type="submit" kind="primary" disabled={busy || !q.trim()}>Ask</Button>
      </form>
    </div>
  );
}

function apply(x: Exchange, ev: AskEvent): Exchange {
  switch (ev.type) {
    case "plan":
      return { ...x, model: ev.model, agents: ev.subtasks.map((s) => ({ ...s, tools: [], done: false })) };
    case "tool":
      return { ...x, agents: x.agents.map((a) => (a.agent === ev.agent ? { ...a, tools: [...a.tools, `${ev.tool}(${JSON.stringify(ev.args)})${ev.ok ? "" : " ✕"}`] } : a)) };
    case "agent_done":
      return { ...x, agents: x.agents.map((a) => (a.agent === ev.agent ? { ...a, done: true, findings: ev.findings } : a)) };
    case "answer":
      return { ...x, answer: ev.markdown, blocks: ev.blocks };
    case "error":
      return { ...x, error: ev.message };
    default:
      return x;
  }
}
