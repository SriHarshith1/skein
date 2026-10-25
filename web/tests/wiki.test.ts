import { describe, expect, it } from "vitest";
import { chunkText, htmlToSections } from "../src/lib/wiki";

describe("wiki html cleaning", () => {
  it("drops infoboxes, references and navboxes, and splits at headings", () => {
    const html = `<div class="mw-parser-output"><aside class="portable-infobox">Name: Ara</aside>
      <p>Ara is a <b>gatekeeper</b>.<sup class="reference">[1]</sup></p>
      <div class="toc"><div>Contents</div></div>
      <h2><span class="mw-headline">Background</span></h2><p>Born in &amp; raised by the Rift.</p>
      <h2>Trivia</h2><p>Skip me.</p>
      <h3>Early life</h3><p>She had a brother.</p>
      <div class="navbox"><div>nav</div></div></div>`;
    const s = htmlToSections(html);
    expect(s.map((x) => x.heading)).toEqual(["Overview", "Background", "Early life"]);
    expect(s[0].text).toBe("Ara is a gatekeeper.");
    expect(s[1].text).toBe("Born in & raised by the Rift.");
    expect(JSON.stringify(s)).not.toMatch(/nav|Contents|Skip/);
  });

  it("chunks on paragraph boundaries", () => {
    const text = Array.from({ length: 6 }, (_, i) => `Paragraph ${i} `.repeat(20)).join("\n\n");
    const chunks = chunkText(text, 700);
    expect(chunks.length).toBeGreaterThan(2);
    expect(chunks.every((c) => c.length <= 700)).toBe(true);
  });
});
