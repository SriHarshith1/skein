-- Postgres does not index foreign key columns by itself. Without these, joins
-- and ON DELETE cascades (deleting a timeline or entity) scan whole tables.

create index if not exists event_participants_entity_idx on event_participants (entity_id);
create index if not exists entities_timeline_idx on entities (timeline_id);
create index if not exists entities_variant_of_idx on entities (variant_of);
create index if not exists timelines_game_idx on timelines (game_id);
create index if not exists timelines_parent_idx on timelines (parent_id);
create index if not exists timelines_branch_event_idx on timelines (branch_event_id);
create index if not exists relationships_game_idx on relationships (game_id);
create index if not exists relationships_timeline_idx on relationships (timeline_id);
create index if not exists relationships_since_idx on relationships (since_event_id);
create index if not exists relationships_until_idx on relationships (until_event_id);
create index if not exists lore_chunks_source_idx on lore_chunks (source_id);
create index if not exists lore_chunks_entity_idx on lore_chunks (entity_id);
create index if not exists suggestions_game_status_idx on suggestions (game_id, status);

-- Pin the trigger function's search_path (Supabase linter: function_search_path_mutable).
alter function lorelines_log_revision() set search_path = public;
