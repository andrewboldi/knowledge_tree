import { DOMAIN_COLORS, type GraphNode } from './types';

interface TreeNodeProps {
  node: GraphNode;
  onNodeClick: (node: GraphNode) => void;
  isSelected?: boolean;
}

export function TreeNode({ node, onNodeClick, isSelected }: TreeNodeProps) {
  const radius = node.is_axiom ? 12 : 8 + Math.min(node.complexity_level, 5) * 1.5;
  const color = DOMAIN_COLORS[node.domain];

  return (
    <g
      className="tree-node"
      transform={`translate(${node.x ?? 0},${node.y ?? 0})`}
      onClick={() => onNodeClick(node)}
      style={{ cursor: 'pointer' }}
    >
      <circle
        r={radius}
        fill={color}
        stroke={isSelected ? '#fff' : color}
        strokeWidth={isSelected ? 3 : 1.5}
        opacity={0.9}
      />
      {node.is_axiom && (
        <circle r={radius + 3} fill="none" stroke={color} strokeWidth={1} opacity={0.5} />
      )}
      <text
        dy={radius + 14}
        textAnchor="middle"
        fontSize={11}
        fill="#e5e7eb"
        style={{ pointerEvents: 'none', userSelect: 'none' }}
      >
        {node.name.length > 15 ? node.name.slice(0, 12) + '...' : node.name}
      </text>
    </g>
  );
}

export function TreeNodeTooltip({ node }: { node: GraphNode | null }) {
  if (!node) return null;

  return (
    <div
      className="tree-node-tooltip"
      style={{
        position: 'absolute',
        background: 'rgba(17, 24, 39, 0.95)',
        border: `1px solid ${DOMAIN_COLORS[node.domain]}`,
        borderRadius: '8px',
        padding: '12px',
        maxWidth: '250px',
        pointerEvents: 'none',
        zIndex: 100,
      }}
    >
      <div style={{ fontWeight: 600, marginBottom: '4px' }}>{node.name}</div>
      <div style={{ fontSize: '12px', color: '#9ca3af' }}>
        {node.domain} | Level {node.complexity_level}
        {node.is_axiom && ' | Axiom'}
      </div>
      {node._concept?.llm_summary && (
        <div style={{ fontSize: '12px', marginTop: '8px', color: '#d1d5db' }}>
          {node._concept.llm_summary}
        </div>
      )}
    </div>
  );
}
