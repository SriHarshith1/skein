-- Row level security for Supabase. The Lorelines server connects with the
-- database URL (owner role) and is not affected. These policies matter when a
-- browser talks to Supabase directly with the anon key: everyone can read,
-- only signed-in users can edit. The local PGlite dev database skips this file.

do $$
declare t text;
begin
  foreach t in array array['games', 'sources', 'timelines', 'entities', 'events',
                           'event_participants', 'relationships', 'citations',
                           'lore_chunks', 'suggestions', 'revisions'] loop
    execute format('alter table %I enable row level security', t);
    execute format('drop policy if exists "%s read" on %I', t, t);
    execute format('create policy "%s read" on %I for select to anon, authenticated using (true)', t, t);
    if t <> 'revisions' then
      execute format('drop policy if exists "%s write" on %I', t, t);
      execute format(
        'create policy "%s write" on %I for all to authenticated using (true) with check (true)', t, t);
    end if;
  end loop;
end $$;
