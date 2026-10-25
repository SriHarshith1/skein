// Minimal MediaWiki client. Works with any wiki that exposes api.php
// (Fandom, wiki.gg, Wikipedia), so the scraper stays game-agnostic.

export const USER_AGENT = "Skein/0.1 (personal lore timeline project; contact via GitHub SriHarshith1)";

export type Section = { heading: string; text: string };

const ENTITIES: Record<string, string> = {
  "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#39;": "'", "&nbsp;": " ", "&#160;": " ",
};

export function decodeEntities(s: string) {
  return s
    .replace(/&(amp|lt|gt|quot|nbsp|#39|#160);/g, (m) => ENTITIES[m] ?? m)
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)));
}

// Drops elements whose whole subtree is noise (infoboxes, navboxes, references, galleries).
function dropBlocks(html: string) {
  let out = html
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/<(script|style|noscript|figure|table|aside|sup)\b[\s\S]*?<\/\1>/gi, " ");
  // Divs nest, so strip the noisy ones by walking tags.
  const noisy = /<div\b[^>]*class="[^"]*(navbox|toc|reflist|references|gallery|mw-references-wrap|thumb|quote-box|reference|tabs|tabview|tabber|page-header|hatnote|dablink|notice)[^"]*"[^>]*>/i;
  for (let guard = 0; guard < 200; guard++) {
    const m = noisy.exec(out);
    if (!m) break;
    let depth = 0;
    const re = /<\/?div\b[^>]*>/gi;
    re.lastIndex = m.index;
    let end = out.length;
    for (let t = re.exec(out); t; t = re.exec(out)) {
      depth += t[0].startsWith("</") ? -1 : 1;
      if (depth === 0) {
        end = t.index + t[0].length;
        break;
      }
    }
    out = out.slice(0, m.index) + " " + out.slice(end);
  }
  return out;
}

function toText(html: string) {
  return decodeEntities(
    html
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/<\/(p|li|dd|dt|blockquote)>/gi, "\n")
      .replace(/<[^>]+>/g, "")
      .replace(/\[\d+\]|\[edit\]|\[citation needed\]/gi, ""),
  )
    .replace(/[ \t]+/g, " ")
    .replace(/\n\s*\n+/g, "\n\n")
    .trim();
}

const SKIP_HEADINGS = /^(references|trivia|gallery|see also|external links|navigation|notes|media|skins|patch history|abilities|change log|recommended items|cosmetics|emotes|quotes|voice lines|balance changes|team-ups|banners|finishers|sprays|skydive emotes|stickers|music packs|stats|update history|bugs|videos|audio|loading screens|holo-sprays|weapon charms|badges|trackers|intro quips|kill quips|legendary skins|epic skins|rare skins|reactive skins|prestige skins|achievements|sources)$/i;

// Splits rendered article HTML at h2/h3 headings into clean text sections.
export function htmlToSections(html: string): Section[] {
  const clean = dropBlocks(html);
  const parts = clean.split(/<h[23]\b[^>]*>([\s\S]*?)<\/h[23]>/i);
  const sections: Section[] = [];
  for (let i = 0; i < parts.length; i += 2) {
    const heading = i === 0 ? "Overview" : toText(parts[i - 1]).replace(/\s*\[.*?\]\s*$/, "");
    const text = toText(parts[i]);
    if (!text || SKIP_HEADINGS.test(heading)) continue;
    sections.push({ heading, text });
  }
  return sections;
}

// Cuts text into ~maxChars chunks on paragraph boundaries.
export function chunkText(text: string, maxChars = 1100): string[] {
  const paras = text.split(/\n\n+/);
  const chunks: string[] = [];
  let cur = "";
  for (const p of paras) {
    if (cur && cur.length + p.length + 2 > maxChars) {
      chunks.push(cur);
      cur = "";
    }
    if (p.length > maxChars) {
      for (let i = 0; i < p.length; i += maxChars) chunks.push(p.slice(i, i + maxChars));
    } else {
      cur = cur ? `${cur}\n\n${p}` : p;
    }
  }
  if (cur) chunks.push(cur);
  return chunks.filter((c) => c.trim().length > 40);
}

async function api(apiUrl: string, params: Record<string, string>) {
  const url = new URL(apiUrl);
  for (const [k, v] of Object.entries({ format: "json", formatversion: "2", ...params })) {
    url.searchParams.set(k, v);
  }
  const res = await fetch(url, { headers: { "user-agent": USER_AGENT, accept: "application/json" } });
  if (!res.ok) throw new Error(`wiki ${res.status} for ${url.searchParams.get("page") ?? url.search}`);
  return res.json();
}

export async function wikiSearch(apiUrl: string, query: string, limit = 5) {
  const data = await api(apiUrl, { action: "query", list: "search", srsearch: query, srlimit: String(limit) });
  return ((data?.query?.search ?? []) as { title: string; snippet: string }[]).map((r) => ({
    title: r.title,
    snippet: toText(r.snippet),
  }));
}

export type WikiPage = { title: string; url: string; sections: Section[] };

export async function wikiPage(apiUrl: string, title: string): Promise<WikiPage | null> {
  const data = await api(apiUrl, { action: "parse", page: title, prop: "text", redirects: "1" });
  if (data?.error) return null;
  const parsed = data.parse as { title: string; text: string };
  const base = apiUrl.replace(/\/(w\/)?api\.php.*$/, "");
  return {
    title: parsed.title,
    url: `${base}/wiki/${encodeURIComponent(parsed.title.replace(/ /g, "_"))}`,
    sections: htmlToSections(parsed.text),
  };
}
