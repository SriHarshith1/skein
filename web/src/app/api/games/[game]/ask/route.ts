import { db } from "@/lib/db";
import { defaultLLM } from "@/lib/agent/llm";
import { ask, type AskEvent, type Turn } from "@/lib/agent/orchestrator";
import { fail, gameOr404 } from "@/lib/api";

export const maxDuration = 300;

// Streams the agent's progress as newline-delimited JSON, ending with the answer.
export async function POST(req: Request, ctx: RouteContext<"/api/games/[game]/ask">) {
  const { game: slug } = await ctx.params;
  const game = await gameOr404(slug);
  if (!game) return fail(404, `unknown game ${slug}`);
  const { question, history } = (await req.json()) as { question?: string; history?: Turn[] };
  if (!question?.trim()) return fail(400, "question is required");
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      const emit = (e: AskEvent) => controller.enqueue(encoder.encode(JSON.stringify(e) + "\n"));
      try {
        await ask({ sql: db(), llm: defaultLLM(), game, question: question.trim(), history: history ?? [], emit });
      } catch (e) {
        emit({ type: "error", message: (e as Error).message });
      } finally {
        controller.close();
      }
    },
  });
  return new Response(stream, { headers: { "content-type": "application/x-ndjson", "cache-control": "no-store" } });
}
