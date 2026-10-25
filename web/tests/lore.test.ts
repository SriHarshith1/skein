import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { parseSeed } from "../src/lib/seed";
import {
  acceptSuggestion, addSuggestion, createRow, deleteRow, findEntities, getBundle, history,
  relationPath, relationsOf, resolveTimeline, searchEvents, updateRow, variantsOf,
} from "../src/lib/lore";
import { fixture, idOf, startDb } from "./helpers";

let ctx: Awaited<ReturnType<typeof startDb>>;
beforeAll(async () => {
  ctx = await startDb();
});
afterAll(async () => ctx?.stop());

describe("seed", () => {
  it("reports broken references", () => {
    const { problems } = parseSeed(fixture());
    expect(problems).toContain('relationship #3 ara->ghost: unknown "ghost"');
    expect(problems.some((p) => p.includes('"nope"'))).toBe(true);
  });

  it("loads rows and skips the broken relationship", async () => {
    const b = (await getBundle(ctx.sql, "testverse"))!;
    expect(b.timelines.map((t) => t.slug).sort()).toEqual(["mirror", "prime"]);
    expect(b.entities).toHaveLength(5);
    expect(b.events.map((e) => e.slug)).toEqual(["the-fall", "gate-opens", "mirror-crowning"]);
    // 3 valid seed relations + 1 generated variant edge
    expect(b.relationships).toHaveLength(4);
    const mirror = b.timelines.find((t) => t.slug === "mirror")!;
    expect(mirror.parent_id).toBe(b.timelines.find((t) => t.slug === "prime")!.id);
    const ara = b.entities.find((e) => e.slug === "ara")!;
    expect(b.citations[ara.id]).toHaveLength(1);
  });
});

describe("queries", () => {
  it("finds entities by alias and by fuzzy name", async () => {
    expect((await findEntities(ctx.sql, ctx.gameId, "the lantern"))[0].slug).toBe("ara");
    expect((await findEntities(ctx.sql, ctx.gameId, "mirror"))[0].slug).toBe("mirror-ara");
  });

  it("filters relations by timeline but keeps all-timeline rows and variant links", async () => {
    const ara = await idOf(ctx.sql, "ara");
    const prime = (await resolveTimeline(ctx.sql, ctx.gameId, "prime"))!;
    const mirror = (await resolveTimeline(ctx.sql, ctx.gameId, "mirror"))!;
    const inPrime = await relationsOf(ctx.sql, ara, prime.id);
    expect(inPrime.map((r) => r.kind).sort()).toEqual(["rival", "sibling", "variant"]);
    const inMirror = await relationsOf(ctx.sql, ara, mirror.id, 2);
    expect(inMirror.map((r) => r.kind).sort()).toEqual(["romance", "sibling", "variant"]);
  });

  it("finds a relationship path across a variant link", async () => {
    const bren = await idOf(ctx.sql, "bren");
    const cass = await idOf(ctx.sql, "cass");
    const mirror = (await resolveTimeline(ctx.sql, ctx.gameId, "mirror"))!;
    const chain = await relationPath(ctx.sql, ctx.gameId, bren, cass, mirror.id);
    expect(chain!.map((r) => r.kind)).toEqual(["sibling", "variant", "romance"]);
  });

  it("lists every variant of a character from any variant", async () => {
    const rows = await variantsOf(ctx.sql, await idOf(ctx.sql, "mirror-ara"));
    expect(rows.map((r) => r.slug).sort()).toEqual(["ara", "mirror-ara"]);
  });

  it("searches events by text, entity and range", async () => {
    expect((await searchEvents(ctx.sql, ctx.gameId, { query: "gate" }))[0].title).toBe("The Gate Opens");
    const cass = await idOf(ctx.sql, "cass");
    expect(await searchEvents(ctx.sql, ctx.gameId, { entityId: cass })).toHaveLength(1);
    expect(await searchEvents(ctx.sql, ctx.gameId, { from: 10, to: 12.5 })).toHaveLength(1);
  });
});

describe("editing", () => {
  it("creates, updates and deletes an event with history", async () => {
    const prime = await idOf(ctx.sql, "prime");
    const ara = await idOf(ctx.sql, "ara");
    const ev = await createRow(ctx.sql, ctx.gameId, "events", {
      title: "Ara loses her lantern", timeline_id: prime, sort_key: 20, importance: 2,
      participants: [{ entity_id: ara, role: "victim" }], game_id: "not-allowed",
    }, "tester");
    expect(ev.slug).toMatch(/^ara-loses-her-lantern-/);
    expect(ev.game_id).toBe(ctx.gameId);
    await updateRow(ctx.sql, ctx.gameId, "events", ev.id, { date_label: "20 AF" }, "tester");
    const h = await history(ctx.sql, ev.id);
    expect(h.map((r) => r.op)).toEqual(["UPDATE", "INSERT"]);
    expect(h[0].actor).toBe("tester");
    expect(h[0].after.date_label).toBe("20 AF");
    expect(await deleteRow(ctx.sql, ctx.gameId, "events", ev.id, "tester")).toBe(true);
    expect((await history(ctx.sql, ev.id))[0].op).toBe("DELETE");
  });

  it("refuses tables that are not editable", async () => {
    await expect(createRow(ctx.sql, ctx.gameId, "revisions", {})).rejects.toThrow(/not editable/);
  });

  it("turns an accepted relationship suggestion into a row", async () => {
    const s = await addSuggestion(ctx.sql, ctx.gameId, {
      kind: "relationship",
      payload: { source: "Bren", target: "Cass", kind: "friend", description: "Drinking buddies." },
      source_url: "https://testverse.example/wiki/Bren",
    });
    const rel = await acceptSuggestion(ctx.sql, ctx.gameId, s.id);
    expect(rel!.kind).toBe("friend");
    const [st] = await ctx.sql`select status from suggestions where id = ${s.id}`;
    expect(st.status).toBe("accepted");
    expect(await acceptSuggestion(ctx.sql, ctx.gameId, s.id)).toBeNull();
  });
});
