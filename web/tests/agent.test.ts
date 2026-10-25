import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { getGame } from "../src/lib/lore";
import { parseJsonLoose, type LLM } from "../src/lib/agent/llm";
import { ask, fallbackPlan, type AskEvent } from "../src/lib/agent/orchestrator";
import { stripRefs } from "../src/lib/agent/blocks";
import { startDb } from "./helpers";

let ctx: Awaited<ReturnType<typeof startDb>>;
beforeAll(async () => {
  ctx = await startDb();
});
afterAll(async () => ctx?.stop());

// Scripted model: plans two subagents, each calls one tool, composer asks for blocks.
class FakeLLM implements LLM {
  label = "fake";
  jsonCalls: string[] = [];
  constructor(private compose: (catalog: string) => unknown) {}
  async json(_system: string, prompt: string) {
    this.jsonCalls.push(prompt);
    if (this.jsonCalls.length === 1) {
      return { subtasks: [
        { agent: "multiverse", task: "Compare Ara across timelines" },
        { agent: "cartographer", task: "Who does Ara relate to?" },
      ] };
    }
    const catalog = prompt.split("Evidence catalog:\n")[1].split("\n\nFindings:")[0];
    return this.compose(catalog);
  }
  async loop({ tools, onTool }: Parameters<LLM["loop"]>[0]) {
    const names = tools.map((t) => t.name);
    const tool = names.includes("get_variants") ? "get_variants" : "get_relations";
    const args = { entity: "Ara" };
    const out = await tools.find((t) => t.name === tool)!.run(args);
    onTool?.({ tool, args, ok: true, preview: "" });
    return { text: `found ${JSON.stringify(out).length} chars [E1]`, trace: [{ tool, args, ok: true, preview: "" }] };
  }
}

const refFor = (catalog: string, label: string) => catalog.split("\n").find((l) => l.includes(label))!.split(" ")[0];

describe("orchestrator", () => {
  it("plans, runs subagents with their own tools, and hydrates UI blocks", async () => {
    const game = (await getGame(ctx.sql, "testverse"))!;
    const llm = new FakeLLM((catalog) => ({
      answer: "Ara [E1] has a mirror self.",
      blocks: [
        { type: "variant_compare", entity: refFor(catalog, ": Ara") },
        { type: "relation_graph", focus: refFor(catalog, ": Ara"), timeline: null, depth: 1 },
        { type: "timeline", events: ["V99"] }, // unknown ref: dropped
        { type: "nonsense" },
      ],
    }));
    const events: AskEvent[] = [];
    const res = await ask({ sql: ctx.sql, llm, game, question: "How does Ara differ in the Mirror World?", emit: (e) => events.push(e) });
    expect(events[0]).toMatchObject({ type: "plan" });
    expect(events.filter((e) => e.type === "agent_done")).toHaveLength(2);
    expect(events.filter((e) => e.type === "tool").map((e) => (e as { tool: string }).tool).sort())
      .toEqual(["get_relations", "get_variants"]);
    expect(res.answer).toBe("Ara has a mirror self.");
    const types = res.blocks.map((b) => b.type);
    expect(types).toEqual(["variant_compare", "relation_graph", "sources"]);
    const vc = res.blocks[0] as Extract<(typeof res.blocks)[number], { type: "variant_compare" }>;
    expect(vc.variants.map((v) => v.name).sort()).toEqual(["Ara", "Mirror Ara"]);
    const g = res.blocks[1] as Extract<(typeof res.blocks)[number], { type: "relation_graph" }>;
    expect(g.edges.map((e) => e.kind).sort()).toEqual(["rival", "sibling", "variant"]);
    expect(g.nodes.length).toBe(4);
  });

  it("falls back to the subagent findings when the composer reply is unusable", async () => {
    const game = (await getGame(ctx.sql, "testverse"))!;
    const llm = new FakeLLM(() => ({ wrong: true }));
    const res = await ask({ sql: ctx.sql, llm, game, question: "Ara?", emit: () => {} });
    expect(res.answer).toContain("**Multiverse analyst:**");
  });
});

describe("helpers", () => {
  it("parses JSON wrapped in fences and chatter", () => {
    expect(parseJsonLoose('Sure!\n```json\n{"a": 1}\n```')).toEqual({ a: 1 });
    expect(parseJsonLoose('x {"b": {"c": 2}} y')).toEqual({ b: { c: 2 } });
  });
  it("strips refs from prose", () => {
    expect(stripRefs("Doom [E1] fell [V2, V3].")).toBe("Doom fell.");
  });
  it("routes by keyword when planning fails", () => {
    const agents = fallbackPlan("Who is K/DA Ahri's rival?").subtasks.map((s) => s.agent);
    expect(agents).toEqual(["multiverse", "cartographer", "archivist"]);
  });
});

describe("robustness", () => {
  it("resolves refs given as names or labels", async () => {
    const { Evidence } = await import("../src/lib/agent/tools");
    const ev = new Evidence();
    const r = ev.ref("E", "id-1", "K/DA Ahri");
    ev.ref("V", "id-2", "The Gate Opens (12 AF)");
    expect(ev.resolve(r, "E")).toBe("id-1");
    expect(ev.resolve("k/da ahri", "E")).toBe("id-1");
    expect(ev.resolve("The Gate Opens", "V")).toBe("id-2");
    expect(ev.resolve("K/DA Ahri", "V")).toBeNull();
  });

  it("emits one error when every subagent fails", async () => {
    const game = (await getGame(ctx.sql, "testverse"))!;
    const down: LLM = {
      label: "down",
      json: async () => { throw new Error("cannot reach Ollama"); },
      loop: async () => { throw new Error("cannot reach Ollama"); },
    };
    const events: AskEvent[] = [];
    const res = await ask({ sql: ctx.sql, llm: down, game, question: "Who is Ara?", emit: (e) => events.push(e) });
    expect(events.at(-1)).toEqual({ type: "error", message: "cannot reach Ollama" });
    expect(events.some((e) => e.type === "answer")).toBe(false);
    expect(res.answer).toBe("");
  });
});
