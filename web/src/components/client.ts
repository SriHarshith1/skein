"use client";

import type { Bundle } from "@/lib/lore";

export type { Bundle, Entity, LoreEvent, Relationship, Source, Timeline } from "@/lib/lore";

function actor() {
  try {
    return localStorage.getItem("lore-actor") || "editor";
  } catch {
    return "editor";
  }
}

export async function api<T = unknown>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(path, {
    ...init,
    headers: { "content-type": "application/json", "x-lore-actor": actor(), ...(init.headers ?? {}) },
  });
  if (res.status === 204) return undefined as T;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { error?: string }).error ?? `request failed (${res.status})`);
  return data as T;
}

export const loadBundle = (slug: string) => api<Bundle>(`/api/games/${slug}`);

export const RELATION_KINDS = [
  "family", "sibling", "parent", "romance", "ally", "friend", "rival", "enemy",
  "mentor", "member", "leader", "creator", "variant", "other",
] as const;

// Edge colors carry meaning: weld/cochineal = bonds, madder = conflict, indigo/woad = structure.
export const RELATION_COLORS: Record<string, string> = {
  family: "#e3b23c", sibling: "#e3b23c", parent: "#e3b23c", romance: "#c4467f",
  ally: "#93b36b", friend: "#b5cc8e", mentor: "#93b36b",
  rival: "#f0884a", enemy: "#d9573f",
  member: "#6f8fe0", leader: "#3fa39b", creator: "#9a74e0",
  variant: "#d9c9a3", other: "#a59588",
};
