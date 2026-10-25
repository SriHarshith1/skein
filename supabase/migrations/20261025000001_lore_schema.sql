-- Lorelines: game-agnostic lore schema.
-- Every row belongs to a game. Nothing here is specific to one franchise:
-- a "timeline" is any continuity (canon, alternate branch, AU skin line),
-- an "entity" is any character / faction / place / artifact.

create table if not exists games (
  id            uuid primary key default gen_random_uuid(),
  slug          text not null unique,
  name          text not null,
  calendar      text,          -- how the lore writes dates, e.g. "AN/BN years"
  description   text,
  wiki_base     text,
  wiki_api      text,          -- MediaWiki api.php used by the scraper
  wiki_license  text,
  created_at    timestamptz not null default now()
);

create table if not exists sources (
  id            uuid primary key default gen_random_uuid(),
  game_id       uuid not null references games(id) on delete cascade,
  key           text not null,
  url           text not null,
  title         text,
  publisher     text not null default 'other'
                check (publisher in ('official', 'wiki', 'other', 'user')),
  retrieved_at  timestamptz not null default now(),
  unique (game_id, key)
);

create table if not exists timelines (
  id            uuid primary key default gen_random_uuid(),
  game_id       uuid not null references games(id) on delete cascade,
  slug          text not null,
  name          text not null,
  kind          text not null default 'canon'
                check (kind in ('canon', 'alternate', 'au')),
  parent_id     uuid references timelines(id) on delete set null,
  branch_event_id uuid,        -- fk added below, events do not exist yet
  branch_note   text,
  description   text,
  color         text,
  unique (game_id, slug)
);

create table if not exists entities (
  id            uuid primary key default gen_random_uuid(),
  game_id       uuid not null references games(id) on delete cascade,
  slug          text not null,
  name          text not null,
  kind          text not null default 'character'
                check (kind in ('character', 'faction', 'place', 'artifact', 'organization')),
  timeline_id   uuid references timelines(id) on delete set null, -- null = canon
  variant_of    uuid references entities(id) on delete set null,
  aliases       text[] not null default '{}',
  summary       text,
  image_url     text,
  attributes    jsonb not null default '{}',
  updated_at    timestamptz not null default now(),
  unique (game_id, slug)
);

create table if not exists events (
  id            uuid primary key default gen_random_uuid(),
  game_id       uuid not null references games(id) on delete cascade,
  timeline_id   uuid not null references timelines(id) on delete cascade,
  slug          text not null,
  title         text not null,
  summary       text,
  date_label    text,          -- as the lore writes it: "c. 1000 BN", "2099", "Season 3"
  sort_key      double precision not null, -- orders events inside a game
  era           text,
  importance    smallint not null default 3 check (importance between 1 and 5),
  tags          text[] not null default '{}',
  updated_at    timestamptz not null default now(),
  unique (game_id, slug)
);

alter table timelines drop constraint if exists timelines_branch_event_fk;
alter table timelines add constraint timelines_branch_event_fk
  foreign key (branch_event_id) references events(id) on delete set null;

create table if not exists event_participants (
  event_id      uuid not null references events(id) on delete cascade,
  entity_id     uuid not null references entities(id) on delete cascade,
  role          text,
  primary key (event_id, entity_id)
);

create table if not exists relationships (
  id            uuid primary key default gen_random_uuid(),
  game_id       uuid not null references games(id) on delete cascade,
  source_id     uuid not null references entities(id) on delete cascade,
  target_id     uuid not null references entities(id) on delete cascade,
  kind          text not null
                check (kind in ('family', 'sibling', 'parent', 'romance', 'ally', 'friend',
                                'rival', 'enemy', 'mentor', 'member', 'leader', 'creator',
                                'variant', 'other')),
  timeline_id   uuid references timelines(id) on delete cascade, -- null = all timelines
  description   text,
  since_event_id uuid references events(id) on delete set null,
  until_event_id uuid references events(id) on delete set null,
  updated_at    timestamptz not null default now(),
  check (source_id <> target_id)
);

create table if not exists citations (
  id            uuid primary key default gen_random_uuid(),
  source_id     uuid not null references sources(id) on delete cascade,
  subject_type  text not null check (subject_type in ('entity', 'event', 'relationship', 'timeline')),
  subject_id    uuid not null,
  note          text,
  unique (source_id, subject_type, subject_id)
);

-- Raw wiki text, split into passages. The Q&A archivist searches these.
create table if not exists lore_chunks (
  id            uuid primary key default gen_random_uuid(),
  game_id       uuid not null references games(id) on delete cascade,
  source_id     uuid references sources(id) on delete cascade,
  entity_id     uuid references entities(id) on delete set null,
  heading       text,
  content       text not null,
  created_at    timestamptz not null default now()
);

-- Edits proposed by the scraper or the agent wait here for a human.
create table if not exists suggestions (
  id            uuid primary key default gen_random_uuid(),
  game_id       uuid not null references games(id) on delete cascade,
  kind          text not null check (kind in ('event', 'entity', 'relationship')),
  payload       jsonb not null,
  rationale     text,
  source_url    text,
  origin        text not null default 'agent' check (origin in ('agent', 'scraper', 'user')),
  status        text not null default 'pending' check (status in ('pending', 'accepted', 'rejected')),
  created_at    timestamptz not null default now()
);

-- Edit history for every editable table.
create table if not exists revisions (
  id            bigserial primary key,
  table_name    text not null,
  row_id        uuid not null,
  op            text not null,
  before        jsonb,
  after         jsonb,
  actor         text,
  created_at    timestamptz not null default now()
);

create index if not exists events_game_sort_idx on events (game_id, sort_key);
create index if not exists events_timeline_idx on events (timeline_id);
create index if not exists entities_game_idx on entities (game_id);
create index if not exists relationships_source_idx on relationships (source_id);
create index if not exists relationships_target_idx on relationships (target_id);
create index if not exists citations_subject_idx on citations (subject_type, subject_id);
create index if not exists lore_chunks_game_idx on lore_chunks (game_id);
create index if not exists lore_chunks_fts_idx on lore_chunks
  using gin (to_tsvector('english', coalesce(heading, '') || ' ' || content));
create index if not exists revisions_row_idx on revisions (row_id, created_at desc);

create or replace function lorelines_log_revision() returns trigger
language plpgsql as $$
begin
  if tg_op in ('INSERT', 'UPDATE') and tg_table_name <> 'timelines' then
    new.updated_at := now();
  end if;
  insert into revisions (table_name, row_id, op, before, after, actor)
  values (
    tg_table_name,
    coalesce(new.id, old.id),
    tg_op,
    case when tg_op = 'INSERT' then null else to_jsonb(old) end,
    case when tg_op = 'DELETE' then null else to_jsonb(new) end,
    nullif(current_setting('lorelines.actor', true), '')
  );
  if tg_op = 'DELETE' then return old; end if;
  return new;
end $$;

do $$
declare t text;
begin
  foreach t in array array['timelines', 'entities', 'events', 'relationships'] loop
    execute format('drop trigger if exists %I_revision on %I', t, t);
    execute format(
      'create trigger %I_revision before insert or update or delete on %I
       for each row execute function lorelines_log_revision()', t, t);
  end loop;
end $$;
