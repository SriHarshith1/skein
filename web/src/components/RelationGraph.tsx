"use client";

import { forceCollide, forceLink, forceManyBody, forceSimulation, forceX, forceY, type SimulationNodeDatum } from "d3-force";
import {
  Background, Controls, Handle, MarkerType, Position, ReactFlow, type Edge, type Node, type NodeProps,
} from "@xyflow/react";
import { useMemo } from "react";
import { RELATION_COLORS } from "./client";

export type GNode = { id: string; name: string; kind: string; timeline: string | null };
export type GEdge = { id: string; source: string; target: string; kind: string; description: string | null };

type SimNode = SimulationNodeDatum & { id: string };

// Deterministic force layout with the focus character pinned in the middle.
function layout(nodes: GNode[], edges: GEdge[], focusId: string | null) {
  const sim: SimNode[] = nodes.map((n, i) => {
    const a = (i / Math.max(1, nodes.length)) * Math.PI * 2;
    return n.id === focusId ? { id: n.id, x: 0, y: 0, fx: 0, fy: 0 } : { id: n.id, x: Math.cos(a) * 250, y: Math.sin(a) * 250 };
  });
  const links = edges.map((e) => ({ source: e.source, target: e.target }));
  const s = forceSimulation(sim)
    .force("link", forceLink<SimNode, { source: string; target: string }>(links).id((d) => d.id).distance(170).strength(0.5))
    .force("charge", forceManyBody().strength(-900))
    .force("collide", forceCollide(70))
    .force("x", forceX(0).strength(0.04))
    .force("y", forceY(0).strength(0.06))
    .stop();
  for (let i = 0; i < 300; i++) s.tick();
  return new Map(sim.map((n) => [n.id, { x: n.x ?? 0, y: n.y ?? 0 }]));
}

const KIND_GLYPH: Record<string, string> = { character: "●", faction: "◆", organization: "◆", place: "▲", artifact: "✦" };

function LoreNode({ data }: NodeProps<Node<{ label: string; kind: string; focus: boolean; timeline: string | null }>>) {
  return (
    <div
      className={`rounded-full border px-3 py-1.5 text-center text-sm shadow-lg ${
        data.focus ? "border-madder bg-madder text-ink font-semibold" : "border-line bg-raise text-chalk"
      }`}
    >
      <Handle type="target" position={Position.Top} className="!opacity-0" />
      <span className="mr-1 opacity-70">{KIND_GLYPH[data.kind] ?? "●"}</span>
      {data.label}
      {data.timeline && !data.focus && <span className="ml-1 font-mono text-[10px] text-dim">{data.timeline}</span>}
      <Handle type="source" position={Position.Bottom} className="!opacity-0" />
    </div>
  );
}

const nodeTypes = { lore: LoreNode };

export function RelationGraph({
  nodes, edges, focusId, height = 520, onNodeClick, onEdgeClick,
}: {
  nodes: GNode[]; edges: GEdge[]; focusId: string | null; height?: number;
  onNodeClick?: (id: string) => void; onEdgeClick?: (id: string) => void;
}) {
  const { flowNodes, flowEdges } = useMemo(() => {
    const pos = layout(nodes, edges, focusId);
    const flowNodes: Node[] = nodes.map((n) => ({
      id: n.id,
      type: "lore",
      position: { x: (pos.get(n.id)?.x ?? 0) - 60, y: (pos.get(n.id)?.y ?? 0) - 16 },
      data: { label: n.name, kind: n.kind, focus: n.id === focusId, timeline: n.timeline },
    }));
    const flowEdges: Edge[] = edges.map((e) => {
      const color = RELATION_COLORS[e.kind] ?? RELATION_COLORS.other;
      return {
        id: e.id,
        source: e.source,
        target: e.target,
        label: e.kind,
        type: "straight",
        animated: e.kind === "variant",
        style: { stroke: color, strokeWidth: 1.6, strokeDasharray: e.kind === "variant" ? "5 4" : undefined },
        labelStyle: { fill: color, fontSize: 11, fontFamily: "var(--font-plex-mono)" },
        labelBgStyle: { fill: "#10162b" },
        markerEnd: { type: MarkerType.ArrowClosed, color, width: 14, height: 14 },
        data: { description: e.description },
      };
    });
    return { flowNodes, flowEdges };
  }, [nodes, edges, focusId]);

  return (
    <div style={{ height }} className="overflow-hidden rounded-[3px] border border-line bg-ink">
      <ReactFlow
        nodes={flowNodes}
        edges={flowEdges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.2}
        nodesConnectable={false}
        onNodeClick={onNodeClick ? (_, n) => onNodeClick(n.id) : undefined}
        onEdgeClick={onEdgeClick ? (_, e) => onEdgeClick(e.id) : undefined}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#24304f" gap={28} />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}
