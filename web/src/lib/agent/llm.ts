import Anthropic from "@anthropic-ai/sdk";

// A tool the model can call. `run` gets parsed arguments and returns JSON-able data.
export type Tool = {
  name: string;
  description: string;
  parameters: { type: "object"; properties: Record<string, unknown>; required?: string[] };
  run: (args: Record<string, unknown>) => Promise<unknown>;
};

export type ToolTrace = { tool: string; args: Record<string, unknown>; ok: boolean; preview: string };

export type LoopResult = { text: string; trace: ToolTrace[] };

export interface LLM {
  readonly label: string;
  // Runs a tool-use loop until the model answers in text (or maxSteps runs out).
  loop(opts: {
    system: string;
    prompt: string;
    tools: Tool[];
    maxSteps?: number;
    onTool?: (t: ToolTrace) => void;
  }): Promise<LoopResult>;
  // One call that must return JSON. The caller validates the shape.
  json(system: string, prompt: string): Promise<unknown>;
}

const MAX_RESULT_CHARS = 6000;

async function callTool(tools: Tool[], name: string, args: Record<string, unknown>) {
  const tool = tools.find((t) => t.name === name);
  if (!tool) return { ok: false, content: JSON.stringify({ error: `unknown tool ${name}` }) };
  try {
    const out = await tool.run(args ?? {});
    let content = JSON.stringify(out);
    if (content.length > MAX_RESULT_CHARS) content = content.slice(0, MAX_RESULT_CHARS) + "…(truncated)";
    return { ok: true, content };
  } catch (e) {
    return { ok: false, content: JSON.stringify({ error: (e as Error).message }) };
  }
}

// Pulls the first JSON object out of a reply, tolerating ```json fences and chatter.
export function parseJsonLoose(text: string): unknown {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  const body = fenced ? fenced[1] : text;
  const start = body.indexOf("{");
  const end = body.lastIndexOf("}");
  if (start < 0 || end <= start) throw new Error("model did not return JSON");
  return JSON.parse(body.slice(start, end + 1));
}

// ---------- Ollama (default: free cloud models through a signed-in local Ollama) ----------

type OllamaMessage = {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  tool_calls?: { function: { name: string; arguments: Record<string, unknown> } }[];
  tool_name?: string;
};

export class OllamaLLM implements LLM {
  constructor(
    readonly model = process.env.LLM_MODEL || "gemma4:31b-cloud",
    readonly host = process.env.OLLAMA_HOST || "http://127.0.0.1:11434",
  ) {}

  get label() {
    return `ollama:${this.model}`;
  }

  private async chat(messages: OllamaMessage[], tools?: Tool[], format?: "json") {
    const res = await fetch(`${this.host}/api/chat`, {
      signal: AbortSignal.timeout(180_000),
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        model: this.model,
        stream: false,
        messages,
        format,
        options: { num_ctx: 32768 },
        tools: tools?.map((t) => ({
          type: "function",
          function: { name: t.name, description: t.description, parameters: t.parameters },
        })),
      }),
    }).catch((e: Error & { cause?: { code?: string; message?: string } }) => {
      // undici hides the real reason (refused, reset, timeout) in `cause`.
      const why = e.cause?.code ?? e.cause?.message ?? e.message;
      throw new Error(`cannot reach Ollama at ${this.host} (${why}). Is the Ollama app running?`);
    });
    if (!res.ok) throw new Error(`ollama ${res.status}: ${(await res.text()).slice(0, 300)}`);
    const data = (await res.json()) as { message: OllamaMessage };
    return data.message;
  }

  async loop({ system, prompt, tools, maxSteps = 6, onTool }: Parameters<LLM["loop"]>[0]) {
    const messages: OllamaMessage[] = [
      { role: "system", content: system },
      { role: "user", content: prompt },
    ];
    const trace: ToolTrace[] = [];
    for (let step = 0; step < maxSteps; step++) {
      // Last step: no tools, so the model must write its findings.
      const msg = await this.chat(messages, step === maxSteps - 1 ? undefined : tools);
      messages.push(msg);
      if (!msg.tool_calls?.length) return { text: msg.content, trace };
      for (const call of msg.tool_calls) {
        const args = call.function.arguments ?? {};
        const r = await callTool(tools, call.function.name, args);
        const t = { tool: call.function.name, args, ok: r.ok, preview: r.content.slice(0, 160) };
        trace.push(t);
        onTool?.(t);
        messages.push({ role: "tool", tool_name: call.function.name, content: r.content });
      }
    }
    const final = await this.chat([...messages, { role: "user", content: "Write your findings now." }]);
    return { text: final.content, trace };
  }

  async json(system: string, prompt: string) {
    const msg = await this.chat(
      [
        { role: "system", content: system },
        { role: "user", content: prompt },
      ],
      undefined,
      "json",
    );
    return parseJsonLoose(msg.content);
  }
}

// ---------- Claude (optional: set LLM_PROVIDER=anthropic and an Anthropic credential) ----------

export class ClaudeLLM implements LLM {
  private client = new Anthropic();
  constructor(readonly model = process.env.LLM_MODEL || "claude-opus-5-5") {}

  get label() {
    return `anthropic:${this.model}`;
  }

  private async create(params: {
    system: string;
    messages: Anthropic.Beta.BetaMessageParam[];
    tools?: Tool[];
  }) {
    const response = await this.client.beta.messages.create({
      model: this.model,
      max_tokens: 16000,
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      output_config: { effort: "low" },
      system: params.system,
      messages: params.messages,
      tools: params.tools?.map((t) => ({
        name: t.name,
        description: t.description,
        input_schema: t.parameters,
      })),
    } as Anthropic.Beta.MessageCreateParamsNonStreaming);
    if (response.stop_reason === "refusal") throw new Error("the model declined this request");
    return response;
  }

  async loop({ system, prompt, tools, maxSteps = 6, onTool }: Parameters<LLM["loop"]>[0]) {
    const messages: Anthropic.Beta.BetaMessageParam[] = [{ role: "user", content: prompt }];
    const trace: ToolTrace[] = [];
    for (let step = 0; step < maxSteps; step++) {
      const response = await this.create({ system, messages, tools: step === maxSteps - 1 ? undefined : tools });
      messages.push({ role: "assistant", content: response.content });
      const uses = response.content.filter((b): b is Anthropic.Beta.BetaToolUseBlock => b.type === "tool_use");
      if (response.stop_reason !== "tool_use" || !uses.length) {
        const text = response.content
          .filter((b): b is Anthropic.Beta.BetaTextBlock => b.type === "text")
          .map((b) => b.text)
          .join("\n");
        return { text, trace };
      }
      // All results go back in one user message so parallel calls keep working.
      const results: Anthropic.Beta.BetaToolResultBlockParam[] = await Promise.all(
        uses.map(async (u) => {
          const args = (u.input ?? {}) as Record<string, unknown>;
          const r = await callTool(tools, u.name, args);
          const t = { tool: u.name, args, ok: r.ok, preview: r.content.slice(0, 160) };
          trace.push(t);
          onTool?.(t);
          return { type: "tool_result" as const, tool_use_id: u.id, content: r.content, is_error: !r.ok };
        }),
      );
      messages.push({ role: "user", content: results });
    }
    return { text: "", trace };
  }

  async json(system: string, prompt: string) {
    const response = await this.create({ system, messages: [{ role: "user", content: prompt }] });
    const text = response.content
      .filter((b): b is Anthropic.Beta.BetaTextBlock => b.type === "text")
      .map((b) => b.text)
      .join("\n");
    return parseJsonLoose(text);
  }
}

export function defaultLLM(): LLM {
  return process.env.LLM_PROVIDER === "anthropic" ? new ClaudeLLM() : new OllamaLLM();
}
