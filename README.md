# Skein

Editable lore timelines for any game, with alternate timelines, relationship graphs per character,
and a Q&A agent made of specialist subagents that answers with generated UI (timelines, graphs,
character cards) and sources.

Loaded today: **Marvel Rivals** (10 timelines: Present, 2099, Collapsed, Mosaic…), **League of
Legends** (Runeterra canon + Arcane, K/DA and Star Guardian), **Apex Legends** (Outlands +
Shadowfall, IMC-Victory and Alter's dying worlds).

## How it fits together

```
research/*.json ──seed──▶ Postgres (Supabase or local PGlite) ◀── Next.js app (web/)
wiki api.php ──scrape──▶ lore_chunks                │                ├─ Timeline view (git-graph threads)
lore_chunks ──extract (LLM)──▶ suggestions ─review──┘                ├─ Relations view (ego graph per timeline)
                                                                     ├─ Ask view (agent + generative UI)
                                                                     └─ Review view (proposed edits, history)
```

- **Game-agnostic schema** (`supabase/migrations`): games, timelines (`canon` / `alternate` / `au`,
  with a parent), entities (with `variant_of` for Doom 2099 or K/DA Ahri), events (free-form
  `date_label` + numeric `sort_key`), relationships (scoped to one timeline or all), sources +
  citations, scraped `lore_chunks`, `suggestions`, and `revisions` (every edit, with who made it).
- **Agent** (`web/src/lib/agent`): a planner picks 1–3 subagents, they run in parallel with their
  own tools, and a narrator writes the answer and picks UI blocks.

| Subagent | Answers | Tools |
|---|---|---|
| Chronicler | when, in what order | `character_events`, `search_events` |
| Cartographer | who relates to whom | `get_relations`, `find_path` |
| Multiverse analyst | alternate timelines, variants | `list_timelines`, `get_variants` |
| Archivist | details from wiki text | `search_lore` (Postgres full-text) |
| Scout | live wiki, new facts | `wiki_search`, `wiki_read`, `propose_edit` |

  Tool results carry short refs (E1, V3); UI blocks cite refs, and the server fills them with real
  rows, so the model cannot invent a character into a graph. Proposed edits wait in Review.

## Run it locally (no Docker needed)

```bash
cd web
npm install
npm run db            # terminal 1: Postgres (PGlite) on 127.0.0.1:54322, data in web/.data
npm run db:seed       # loads research/*.json (runs migrations first)
npm run dev           # terminal 2: http://localhost:3000
```

The agent uses Ollama by default (free): run the Ollama app or `ollama serve`, signed in for cloud
models. Default model `gemma4:31b-cloud`; change with `LLM_MODEL`. To use Claude instead:
`LLM_PROVIDER=anthropic` plus an Anthropic credential (model `claude-opus-5-5` by default).

## Use Supabase

1. Create a project, copy the **connection string** (Settings → Database, the transaction pooler
   URI works; prepared statements are off).
2. Put it in `web/.env.local` as `DATABASE_URL=postgres://...`.
3. `npm run db:seed` applies every migration (including RLS: public read, signed-in write) and loads
   the data. Or apply `supabase/migrations` with `supabase db push`.

## Fill and grow the data

```bash
npm run scrape -- marvel-rivals            # wiki pages for each entity -> lore_chunks
npm run scrape -- league-of-legends --limit 20 --page "Timeline"
npm run extract -- apex-legends --entities 5   # LLM proposes events/relations -> Review tab
```

Everything is editable in the app: click an event, a character or a graph edge. Each edit keeps
history. "Fetch wiki page" on a character pulls its page into the Archivist's corpus.

**Add a game:** write `research/<slug>.json` in the same shape as the others (see
`web/src/lib/seed.ts` for the schema, `research/generators/` for how the three were built), set
`wiki.api` to the game's `api.php`, then seed and scrape. No code changes.

## Tests

```bash
npm test          # 19 tests on a real in-memory Postgres; agent tested with a scripted model
npm run typecheck
```

## Sources and licensing

Lore summaries are written in our own words and cite their sources. Scraped wiki text keeps its
license: League and Rivals wikis on Fandom are CC BY-SA 3.0; the Apex wiki.gg wiki is
CC BY-NC-SA 4.0. Official bios come from Riot's Universe site and EA's character pages.

## Known limits

- Local PGlite serves one connection per process well; heavy parallel use belongs on Supabase.
- `sort_key` scales differ per game (League uses AN years, Arcane/K/DA use release years, Rivals
  places all Chronoverses on one present-day axis), so AU threads start as separate rings.
- Some Rivals timeline assignments come from wiki deductions; check before treating as canon.
