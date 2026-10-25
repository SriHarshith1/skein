"use client";

import { useEffect, type ReactNode } from "react";

export function Button({
  children, onClick, kind = "ghost", type = "button", disabled, title,
}: {
  children: ReactNode; onClick?: () => void; kind?: "primary" | "ghost" | "danger";
  type?: "button" | "submit"; disabled?: boolean; title?: string;
}) {
  const styles = {
    primary: "bg-madder text-ink hover:brightness-110 font-semibold",
    ghost: "border border-line text-chalk hover:bg-raise",
    danger: "border border-danger/50 text-danger hover:bg-danger/10",
  }[kind];
  return (
    <button type={type} onClick={onClick} disabled={disabled} title={title}
      className={`rounded-[3px] px-3 py-1.5 text-sm transition disabled:opacity-40 ${styles}`}>
      {children}
    </button>
  );
}

export function Field({ label, children, hint }: { label: string; children: ReactNode; hint?: string }) {
  return (
    <label className="block space-y-1">
      <span className="tag">{label}</span>
      {children}
      {hint && <span className="block text-xs text-dim">{hint}</span>}
    </label>
  );
}

export function Drawer({ open, onClose, title, children }: { open: boolean; onClose: () => void; title: string; children: ReactNode }) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-40 flex justify-end" role="dialog" aria-modal="true" aria-label={title}>
      <button aria-label="Close" className="absolute inset-0 bg-black/50" onClick={onClose} />
      <aside className="relative h-full w-full max-w-md overflow-y-auto border-l border-line bg-panel p-5 shadow-2xl">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="font-display text-lg font-bold">{title}</h2>
          <button onClick={onClose} className="text-dim hover:text-chalk" aria-label="Close panel">✕</button>
        </div>
        {children}
      </aside>
    </div>
  );
}

export function Chip({ children, color }: { children: ReactNode; color?: string }) {
  return (
    <span className="inline-flex items-center gap-1 rounded-full border border-line px-2 py-0.5 text-xs text-chalk/90"
      style={color ? { borderColor: color + "88", color } : undefined}>
      {children}
    </span>
  );
}

export function Empty({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="rounded-[3px] border border-dashed border-line p-8 text-center">
      <p className="font-display text-lg font-semibold">{title}</p>
      {children && <div className="mt-2 text-sm text-dim">{children}</div>}
    </div>
  );
}
