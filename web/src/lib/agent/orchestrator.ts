import { z } from "zod";
import type { Sql } from "../db";
import type { Game } from "../lore";
import { BLOCK_GUIDE, ComposerOutput, hydrateBlocks, stripRefs, type UIBlock } from "./blocks";
import type { LLM, ToolTrace } from "./llm";
import { buildTools, Evidence } from "./tools";

// ---------- the subagents ----------

export type AgentName = "chronicler" | "cartographer" | "multiverse" | "archivist" | "scout";

export const SUBAGENTS: Record<AgentName, { title: string; brief: string; tools: string[]; system: string }> = {
  chronicler: {
    title: "Chronicler",
    brief: "WHEN things happened: order of events, eras, what happened before/after, a character's life story.",
    tools: ["find_entity", "character_events", "search_events", "list_timelines"],
    system: "You are the Chronicler. You answer questions about chronology using the lore database. " +
      "Find the relevant entities, then pull their events in order. Note dates exactly as the lore writes them.",
  },
  cartographer: {
    title: "Cartographer",
    brief: "WHO relates to whom: family, rivals, allies, romance, factions, how two characters are connected.",
    tools: ["find_entity", "get_relations", "find_path", "list_timelines"],
    system: "You are the Cartographer. You map relationships between characters and factions. " +
      "Use get_relations (depth 2 for broad questions) and find_path to connect two characters.",
  },
  multiverse: {
    title: "Multiverse analyst",
    brief: "ALTERNATE timelines and AU skin lines: variants of a character, how timelines differ or branch.",
    tools: ["list_timelines", "find_entity", "get_variants", "search_events", "get_relations"],
    system: "You are the Multiverse analyst. You compare timelines and character variants. " +
      "List timelines, find each variant of the character, and contrast their events and relationships per timeline.",
  },
  archivist: {
    title: "Archivist",
    brief: "DETAILS and quotes from scraped wiki text: backstory specifics, motives, descriptions.",
    tools: ["find_entity", "search_lore"],
    system: "You are the Archivist. You search scraped wiki passages for details the structured timeline lacks. " +
      "Report what the passages say and which source they came from. Try 2-3 different search phrasings.",
  },
  scout: {
    title: "Scout",
    brief: "LIVE wiki research when the database has no answer, or when the user asks to add/fix lore (proposes edits for review).",
    tools: ["find_entity", "character_events", "wiki_search", "wiki_read", "propose_edit"],
    system: "You are the Scout. You read the live community wiki to fill gaps in the lore database. " +
      "Search, read the best page, and report facts with the page URL. Before you finish, compare what you read with " +
      "find_entity and character_events results. When the user asks to add, fix or propose lore, call propose_edit for " +
      "each clearly sourced fact the database lacks (at most 3), with a precise payload and the source_url. Never invent facts.",
  },
};

const COMMON_RULES = `Rules:
- Use only facts returned by your tools. If the tools return nothing useful, say so plainly.
- Each tool result carries a "ref" like E1, V3, T2, R5, S4, P1. Cite refs next to each fact, e.g. "Doom 2099 caused the Timestream Entanglement [V3]".
- Finish with a short findings report (bullet points). No preamble.`;

export type AskEvent =
  | { type: "plan"; subtasks: { agent: AgentName; title: string; task: string }[]; model: string }
  | { type: "agent_start"; agent: AgentName }
  | { type: "tool"; agent: AgentName; tool: string; args: Record<string, unknown>; ok: boolean }
  | { type: "agent_done"; agent: AgentName; findings: string; tools: number }
  | { type: "answer"; markdown: string; blocks: UIBlock[] }
  | { type: "error"; message: string };

export type Turn = { role: "user" | "assistant"; content: string };

const PlanSchema = z.object({
  subtasks: z
    .array(z.object({ agent: z.enum(["chronicler", "cartographer", "multiverse", "archivist", "scout"]), task: z.string() }))
    .min(1)
    .max(3),
});

function historyText(history: Turn[]) {
  return history
    .slice(-6)
    .map((t) => `${t.role === "user" ? "User" : "Skein"}: ${t.content.slice(0, 600)}`)
    .join("\n");
}

// Keyword fallback when the planner reply is unusable.
export function fallbackPlan(question: string): z.infer<typeof PlanSchema> {
  const q = question.toLowerCase();
  const subtasks: z.infer<typeof PlanSchema>["subtasks"] = [];
  if (/(timeline|universe|variant|alternate|2099|au\b|k\/da|kda|star guardian|arcane|version|branch)/.test(q)) {
    subtasks.push({ agent: "multiverse", task: question });
  }
  if (/(relat|rival|enemy|ally|friend|family|brother|sister|mother|father|love|romance|connect|team|between|vs\b)/.test(q)) {
    subtasks.push({ agent: "cartographer", task: question });
  }
  if (/(when|before|after|order|year|history|happen|timeline|story|first|origin)/.test(q) || subtasks.length === 0) {
    subtasks.push({ agent: "chronicler", task: question });
  }
  if (subtasks.length < 3) subtasks.push({ agent: "archivist", task: question });
  return { subtasks: subtasks.slice(0, 3) };
}

export async function ask(opts: {
  sql: Sql;
  llm: LLM;
  game: Game;
  question: string;
  history?: Turn[];
  emit: (e: AskEvent) => void;
}) {
  const { sql, llm, game, question, emit } = opts;
  const history = opts.history ?? [];
  const evidence = new Evidence();
  const tools = buildTools({ sql, game, evidence });
  const gameLine = `Game: ${game.name}. Calendar: ${game.calendar ?? "unknown"}.`;

  // 1. Plan: which subagents, with what task.
  const roster = (Object.entries(SUBAGENTS) as [AgentName, (typeof SUBAGENTS)[AgentName]][])
    .map(([k, v]) => `- ${k}: ${v.brief}`)
    .join("\n");
  let plan: z.infer<typeof PlanSchema>;
  try {
    const raw = await llm.json(
      `You are the Skein orchestrator. You split a lore question into 1-3 focused subtasks for specialist subagents.\n` +
        `Subagents:\n${roster}\n` +
        `Reply with JSON only: {"subtasks":[{"agent":"<name>","task":"<self-contained instruction naming the characters/timelines>"}]}. ` +
        `Use the fewest subagents that fully cover the question. Use scout only if the user asks for new/live info or to add lore.`,
      `${gameLine}\n${history.length ? `Conversation so far:\n${historyText(history)}\n` : ""}Question: ${question}`,
    );
    plan = PlanSchema.parse(raw);
  } catch {
    plan = fallbackPlan(question);
  }
  // One task per agent: merge duplicates.
  const merged = new Map<AgentName, string>();
  for (const s of plan.subtasks) merged.set(s.agent, merged.has(s.agent) ? `${merged.get(s.agent)}\n${s.task}` : s.task);
  emit({
    type: "plan",
    model: llm.label,
    subtasks: [...merged].map(([agent, task]) => ({ agent, title: SUBAGENTS[agent].title, task })),
  });

  // 2. Run subagents in parallel, each with only its own tools.
  const findings = await Promise.all(
    [...merged].map(async ([agent, task]) => {
      emit({ type: "agent_start", agent });
      const def = SUBAGENTS[agent];
      try {
        const r = await llm.loop({
          system: `${def.system}\n${gameLine}\n${COMMON_RULES}`,
          prompt: `${history.length ? `Context from the conversation:\n${historyText(history)}\n\n` : ""}Task: ${task}`,
          tools: def.tools.map((n) => tools[n]),
          maxSteps: agent === "scout" ? 8 : 5,
          onTool: (t: ToolTrace) => emit({ type: "tool", agent, tool: t.tool, args: t.args, ok: t.ok }),
        });
        emit({ type: "agent_done", agent, findings: r.text, tools: r.trace.length });
        return { agent, text: r.text };
      } catch (e) {
        const msg = `failed: ${(e as Error).message}`;
        emit({ type: "agent_done", agent, findings: msg, tools: 0 });
        return { agent, text: msg };
      }
    }),
  );

  // If no subagent got through (model down, wrong model name), say so once.
  const failed = findings.filter((f) => f.text.startsWith("failed:"));
  if (failed.length === findings.length) {
    emit({ type: "error", message: failed[0]?.text.replace(/^failed: /, "") ?? "no subagent ran" });
    return { answer: "", blocks: [] as UIBlock[] };
  }

  // 3. Compose: one answer plus generative UI blocks that point at evidence refs.
  const catalog = evidence.catalog() || "(empty: the subagents found nothing)";
  let answer = "";
  let rawBlocks: unknown[] = [];
  try {
    const raw = await llm.json(
      `You are the Skein narrator. You write the final answer to a lore question from subagent findings.\n` +
        `Write 1-3 short paragraphs of markdown. Use only facts in the findings; if they conflict or are missing, say so. ` +
        `Mention the timeline when a fact is timeline-specific. Write dates the way the lore writes them ("2099", "Season 3"), never internal sort numbers like 2025.0. ` +
        `Do not show refs in the answer text.\n${BLOCK_GUIDE}\n` +
        `Reply with JSON only: {"answer":"<markdown>","blocks":[...]}.`,
      `${gameLine}\nQuestion: ${question}\n\nEvidence catalog:\n${catalog}\n\nFindings:\n` +
        findings.map((f) => `## ${SUBAGENTS[f.agent].title}\n${f.text}`).join("\n\n"),
    );
    if (process.env.NODE_ENV !== "production") console.warn("[lorelines] composer blocks", JSON.stringify((raw as { blocks?: unknown }).blocks ?? null).slice(0, 600));
    const parsed = ComposerOutput.parse(raw);
    answer = parsed.answer;
    rawBlocks = parsed.blocks;
  } catch {
    answer = findings.map((f) => `**${SUBAGENTS[f.agent].title}:** ${f.text}`).join("\n\n");
  }
  const blocks = await hydrateBlocks(sql, game, evidence, rawBlocks);
  emit({ type: "answer", markdown: stripRefs(answer), blocks });
  return { answer: stripRefs(answer), blocks };
}
