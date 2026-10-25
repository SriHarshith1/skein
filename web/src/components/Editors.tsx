"use client";

import { useEffect, useState } from "react";
import { api, RELATION_KINDS, type Bundle, type Entity, type LoreEvent, type Relationship } from "./client";
import { Button, Drawer, Field } from "./ui";

type Rev = { id: number; op: string; actor: string | null; created_at: string; before: Record<string, unknown> | null; after: Record<string, unknown> | null };

const SKIP = new Set(["updated_at", "id", "game_id"]);

function diffKeys(r: Rev) {
  if (!r.before || !r.after) return [];
  return Object.keys(r.after).filter((k) => !SKIP.has(k) && JSON.stringify(r.before![k]) !== JSON.stringify(r.after![k]));
}

export function History({ slug, rowId, version }: { slug: string; rowId: string; version: number }) {
  const [rows, setRows] = useState<Rev[] | null>(null);
  useEffect(() => {
    api<Rev[]>(`/api/games/${slug}/history?row=${rowId}`).then(setRows).catch(() => setRows([]));
  }, [slug, rowId, version]);
  if (!rows?.length) return null;
  return (
    <div className="mt-6 border-t border-line pt-4">
      <h3 className="mb-2 tag">Edit history</h3>
      <ul className="space-y-1.5 text-xs">
        {rows.map((r) => (
          <li key={r.id} className="flex gap-2">
            <span className="font-mono text-dim">{new Date(r.created_at).toLocaleString()}</span>
            <span>
              <b>{r.actor ?? "unknown"}</b> {r.op === "INSERT" ? "created" : r.op === "DELETE" ? "deleted" : "changed"}
              {r.op === "UPDATE" && diffKeys(r).length > 0 && <span className="text-dim"> {diffKeys(r).join(", ")}</span>}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function SourcePicker({ bundle, value, onChange }: { bundle: Bundle; value: string[]; onChange: (ids: string[]) => void }) {
  const [url, setUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const chosen = bundle.sources.filter((s) => value.includes(s.id));
  const add = async () => {
    if (!url.trim()) return;
    setBusy(true);
    try {
      const existing = bundle.sources.find((s) => s.url === url.trim());
      const src = existing ?? (await api<{ id: string }>(`/api/games/${bundle.game.slug}/sources`, {
        method: "POST",
        body: JSON.stringify({ url: url.trim(), title: url.trim().replace(/^https?:\/\//, "").slice(0, 80), publisher: "user" }),
      }));
      onChange([...new Set([...value, src.id])]);
      setUrl("");
    } finally {
      setBusy(false);
    }
  };
  return (
    <Field label="Sources" hint="Every fact should point at where it came from.">
      <ul className="space-y-1">
        {chosen.map((s) => (
          <li key={s.id} className="flex items-center gap-2 text-sm">
            <a href={s.url} target="_blank" rel="noreferrer" className="truncate text-sky-300 hover:underline">{s.title ?? s.url}</a>
            <button type="button" className="text-dim hover:text-danger" aria-label="Remove source"
              onClick={() => onChange(value.filter((v) => v !== s.id))}>✕</button>
          </li>
        ))}
      </ul>
      <div className="flex gap-2">
        <input className="field" placeholder="https://… source URL" value={url} onChange={(e) => setUrl(e.target.value)} />
        <Button onClick={add} disabled={busy}>Add</Button>
      </div>
    </Field>
  );
}

function useSave(slug: string, table: string, id: string | null, onSaved: () => void) {
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [version, setVersion] = useState(0);
  const save = async (body: Record<string, unknown>) => {
    setBusy(true);
    setError(null);
    try {
      await api(`/api/games/${slug}/${table}${id ? `/${id}` : ""}`, { method: id ? "PATCH" : "POST", body: JSON.stringify(body) });
      setVersion((v) => v + 1);
      onSaved();
      return true;
    } catch (e) {
      setError((e as Error).message);
      return false;
    } finally {
      setBusy(false);
    }
  };
  const remove = async () => {
    if (!id || !confirm("Delete this for everyone? The edit history keeps a copy.")) return false;
    setBusy(true);
    try {
      await api(`/api/games/${slug}/${table}/${id}`, { method: "DELETE" });
      onSaved();
      return true;
    } catch (e) {
      setError((e as Error).message);
      return false;
    } finally {
      setBusy(false);
    }
  };
  return { save, remove, error, busy, version };
}

// ---------- event ----------

export function EventEditor({
  bundle, event, defaultTimeline, onClose, onSaved,
}: { bundle: Bundle; event: LoreEvent | null; defaultTimeline?: string; onClose: () => void; onSaved: () => void }) {
  const slug = bundle.game.slug;
  const [form, setForm] = useState(() => ({
    title: event?.title ?? "",
    date_label: event?.date_label ?? "",
    sort_key: event ? String(event.sort_key) : "",
    era: event?.era ?? "",
    importance: event?.importance ?? 3,
    timeline_id: event?.timeline_id ?? defaultTimeline ?? bundle.timelines[0]?.id ?? "",
    summary: event?.summary ?? "",
    participants: event?.participants.map((p) => p.entity_id) ?? [],
    source_ids: event ? bundle.citations[event.id] ?? [] : [],
  }));
  const [pick, setPick] = useState("");
  const { save, remove, error, busy, version } = useSave(slug, "events", event?.id ?? null, onSaved);
  const set = (k: string, v: unknown) => setForm((f) => ({ ...f, [k]: v }));
  const byId = new Map(bundle.entities.map((e) => [e.id, e]));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = await save({
      ...form,
      sort_key: Number(form.sort_key),
      participants: form.participants.map((id) => ({
        entity_id: id, role: event?.participants.find((p) => p.entity_id === id)?.role ?? null,
      })),
    });
    if (ok && !event) onClose();
  };

  return (
    <Drawer open onClose={onClose} title={event ? "Edit event" : "New event"}>
      <form onSubmit={submit} className="space-y-4">
        <Field label="Title"><input required className="field" value={form.title} onChange={(e) => set("title", e.target.value)} /></Field>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Date as written" hint="e.g. c. 1000 BN, 2099, Season 3">
            <input className="field" value={form.date_label} onChange={(e) => set("date_label", e.target.value)} />
          </Field>
          <Field label="Order key" hint="A number that sorts it in time">
            <input required type="number" step="any" className="field font-mono" value={form.sort_key} onChange={(e) => set("sort_key", e.target.value)} />
          </Field>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Timeline">
            <select className="field" value={form.timeline_id} onChange={(e) => set("timeline_id", e.target.value)}>
              {bundle.timelines.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
          </Field>
          <Field label="Era"><input className="field" value={form.era} onChange={(e) => set("era", e.target.value)} /></Field>
        </div>
        <Field label={`Importance: ${form.importance} of 5`}>
          <input type="range" min={1} max={5} value={form.importance} onChange={(e) => set("importance", Number(e.target.value))} className="w-full accent-madder" />
        </Field>
        <Field label="Summary"><textarea rows={5} className="field" value={form.summary} onChange={(e) => set("summary", e.target.value)} /></Field>
        <Field label="Who was involved">
          <div className="flex flex-wrap gap-1.5">
            {form.participants.map((id) => (
              <button type="button" key={id} onClick={() => set("participants", form.participants.filter((p) => p !== id))}
                className="rounded-full border border-line px-2 py-0.5 text-xs hover:border-danger" title="Remove">
                {byId.get(id)?.name ?? "?"} ✕
              </button>
            ))}
          </div>
          <select className="field" value={pick} onChange={(e) => {
            if (e.target.value) set("participants", [...new Set([...form.participants, e.target.value])]);
            setPick("");
          }}>
            <option value="">Add a character…</option>
            {bundle.entities.map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
          </select>
        </Field>
        <SourcePicker bundle={bundle} value={form.source_ids} onChange={(ids) => set("source_ids", ids)} />
        {error && <p className="text-sm text-danger">{error}</p>}
        <div className="flex justify-between">
          <Button type="submit" kind="primary" disabled={busy}>{event ? "Save event" : "Add event"}</Button>
          {event && <Button kind="danger" onClick={async () => (await remove()) && onClose()}>Delete</Button>}
        </div>
      </form>
      {event && <History slug={slug} rowId={event.id} version={version} />}
    </Drawer>
  );
}

// ---------- entity ----------

export function EntityEditor({
  bundle, entity, onClose, onSaved,
}: { bundle: Bundle; entity: Entity | null; onClose: () => void; onSaved: () => void }) {
  const slug = bundle.game.slug;
  const [form, setForm] = useState(() => ({
    name: entity?.name ?? "",
    kind: entity?.kind ?? "character",
    timeline_id: entity?.timeline_id ?? "",
    variant_of: entity?.variant_of ?? "",
    aliases: entity?.aliases.join(", ") ?? "",
    summary: entity?.summary ?? "",
    source_ids: entity ? bundle.citations[entity.id] ?? [] : [],
  }));
  const [wiki, setWiki] = useState<string | null>(null);
  const { save, remove, error, busy, version } = useSave(slug, "entities", entity?.id ?? null, onSaved);
  const set = (k: string, v: unknown) => setForm((f) => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = await save({
      ...form,
      aliases: form.aliases.split(",").map((a) => a.trim()).filter(Boolean),
    });
    if (ok && !entity) onClose();
  };

  const fetchWiki = async () => {
    if (!entity) return;
    setWiki("Reading the wiki…");
    try {
      const r = await api<{ found: boolean; title?: string; chunks?: number }>(`/api/games/${slug}/scrape`, {
        method: "POST", body: JSON.stringify({ entity_id: entity.id }),
      });
      setWiki(r.found ? `Saved ${r.chunks} passages from "${r.title}". The Archivist can now search them.` : "No wiki page matches this name.");
      onSaved();
    } catch (e) {
      setWiki((e as Error).message);
    }
  };

  return (
    <Drawer open onClose={onClose} title={entity ? `Edit ${entity.name}` : "New character or entity"}>
      <form onSubmit={submit} className="space-y-4">
        <Field label="Name"><input required className="field" value={form.name} onChange={(e) => set("name", e.target.value)} /></Field>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Kind">
            <select className="field" value={form.kind} onChange={(e) => set("kind", e.target.value)}>
              {["character", "faction", "organization", "place", "artifact"].map((k) => <option key={k}>{k}</option>)}
            </select>
          </Field>
          <Field label="Belongs to timeline">
            <select className="field" value={form.timeline_id} onChange={(e) => set("timeline_id", e.target.value)}>
              <option value="">Canon (all)</option>
              {bundle.timelines.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
          </Field>
        </div>
        <Field label="Variant of" hint="Another version of an existing character, e.g. Doom 2099 of Victor von Doom">
          <select className="field" value={form.variant_of} onChange={(e) => set("variant_of", e.target.value)}>
            <option value="">Not a variant</option>
            {bundle.entities.filter((e) => e.id !== entity?.id).map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
          </select>
        </Field>
        <Field label="Aliases" hint="Comma separated"><input className="field" value={form.aliases} onChange={(e) => set("aliases", e.target.value)} /></Field>
        <Field label="Summary"><textarea rows={5} className="field" value={form.summary} onChange={(e) => set("summary", e.target.value)} /></Field>
        <SourcePicker bundle={bundle} value={form.source_ids} onChange={(ids) => set("source_ids", ids)} />
        {error && <p className="text-sm text-danger">{error}</p>}
        <div className="flex flex-wrap justify-between gap-2">
          <Button type="submit" kind="primary" disabled={busy}>{entity ? "Save" : "Add"}</Button>
          {entity && bundle.game.wiki_api && <Button onClick={fetchWiki}>Fetch wiki page</Button>}
          {entity && <Button kind="danger" onClick={async () => (await remove()) && onClose()}>Delete</Button>}
        </div>
        {wiki && <p className="text-sm text-dim">{wiki}</p>}
      </form>
      {entity && <History slug={slug} rowId={entity.id} version={version} />}
    </Drawer>
  );
}

// ---------- relationship ----------

export function RelationEditor({
  bundle, relation, defaults, onClose, onSaved,
}: {
  bundle: Bundle; relation: Relationship | null; defaults?: { source_id?: string; timeline_id?: string | null };
  onClose: () => void; onSaved: () => void;
}) {
  const slug = bundle.game.slug;
  const [form, setForm] = useState(() => ({
    source_id: relation?.source_id ?? defaults?.source_id ?? "",
    target_id: relation?.target_id ?? "",
    kind: relation?.kind ?? "ally",
    timeline_id: relation?.timeline_id ?? defaults?.timeline_id ?? "",
    description: relation?.description ?? "",
    since_event_id: relation?.since_event_id ?? "",
    until_event_id: relation?.until_event_id ?? "",
    source_ids: relation ? bundle.citations[relation.id] ?? [] : [],
  }));
  const { save, remove, error, busy, version } = useSave(slug, "relationships", relation?.id ?? null, onSaved);
  const set = (k: string, v: unknown) => setForm((f) => ({ ...f, [k]: v }));
  const events = bundle.events;
  const people = bundle.entities;

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = await save(form);
    if (ok && !relation) onClose();
  };

  return (
    <Drawer open onClose={onClose} title={relation ? "Edit relationship" : "New relationship"}>
      <form onSubmit={submit} className="space-y-4">
        <div className="grid grid-cols-[1fr_auto_1fr] items-end gap-2">
          <Field label="From">
            <select required className="field" value={form.source_id} onChange={(e) => set("source_id", e.target.value)}>
              <option value="" disabled>Pick…</option>
              {people.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </Field>
          <select className="field mb-0 w-auto" aria-label="Relationship kind" value={form.kind} onChange={(e) => set("kind", e.target.value)}>
            {RELATION_KINDS.map((k) => <option key={k}>{k}</option>)}
          </select>
          <Field label="To">
            <select required className="field" value={form.target_id} onChange={(e) => set("target_id", e.target.value)}>
              <option value="" disabled>Pick…</option>
              {people.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </Field>
        </div>
        <Field label="Holds in" hint="Pick one timeline when the bond only exists there (e.g. only in an AU).">
          <select className="field" value={form.timeline_id} onChange={(e) => set("timeline_id", e.target.value)}>
            <option value="">Every timeline</option>
            {bundle.timelines.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
          </select>
        </Field>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Since event">
            <select className="field" value={form.since_event_id} onChange={(e) => set("since_event_id", e.target.value)}>
              <option value="">—</option>
              {events.map((ev) => <option key={ev.id} value={ev.id}>{ev.title}</option>)}
            </select>
          </Field>
          <Field label="Until event">
            <select className="field" value={form.until_event_id} onChange={(e) => set("until_event_id", e.target.value)}>
              <option value="">—</option>
              {events.map((ev) => <option key={ev.id} value={ev.id}>{ev.title}</option>)}
            </select>
          </Field>
        </div>
        <Field label="Description"><textarea rows={3} className="field" value={form.description} onChange={(e) => set("description", e.target.value)} /></Field>
        <SourcePicker bundle={bundle} value={form.source_ids} onChange={(ids) => set("source_ids", ids)} />
        {error && <p className="text-sm text-danger">{error}</p>}
        <div className="flex justify-between">
          <Button type="submit" kind="primary" disabled={busy}>{relation ? "Save" : "Add relationship"}</Button>
          {relation && <Button kind="danger" onClick={async () => (await remove()) && onClose()}>Delete</Button>}
        </div>
      </form>
      {relation && <History slug={slug} rowId={relation.id} version={version} />}
    </Drawer>
  );
}
