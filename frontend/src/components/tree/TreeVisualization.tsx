import { useEffect, useRef, useState, useCallback } from 'react';
import * as d3 from 'd3';
import { TreeNode, TreeNodeTooltip } from './TreeNode';
import { DomainLinks, CrossDomainLinks } from './CrossDomainLinks';
import {
  type Concept,
  type GraphData,
  type GraphNode,
  type GraphLink,
  DOMAIN_COLORS,
  DOMAIN_LABELS,
} from './types';

interface TreeVisualizationProps {
  data: GraphData;
  width?: number;
  height?: number;
  onNodeClick?: (concept: Concept) => void;
  showCrossDomainLinks?: boolean;
}

export function TreeVisualization({
  data,
  width = 900,
  height = 600,
  onNodeClick,
  showCrossDomainLinks = true,
}: TreeVisualizationProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const simulationRef = useRef<d3.Simulation<GraphNode, GraphLink> | null>(null);
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [links, setLinks] = useState<GraphLink[]>([]);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const [transform, setTransform] = useState(d3.zoomIdentity);

  useEffect(() => {
    if (!data.nodes.length) return;

    const nodesCopy = data.nodes.map((n) => ({ ...n }));
    const linksCopy = data.links.map((l) => ({ ...l }));

    const simulation = d3
      .forceSimulation<GraphNode>(nodesCopy)
      .force(
        'link',
        d3
          .forceLink<GraphNode, GraphLink>(linksCopy)
          .id((d) => d.id)
          .distance(80)
      )
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force(
        'y',
        d3.forceY<GraphNode>((d) => {
          const levelOffset = d.complexity_level * 60;
          return 80 + levelOffset;
        }).strength(0.3)
      )
      .force(
        'x',
        d3.forceX<GraphNode>((d) => {
          const domainOrder = ['MATH', 'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'CS'];
          const idx = domainOrder.indexOf(d.domain);
          const domainSpacing = width / (domainOrder.length + 1);
          return domainSpacing * (idx + 1);
        }).strength(0.1)
      )
      .force('collision', d3.forceCollide<GraphNode>().radius(25));

    simulation.on('tick', () => {
      setNodes([...nodesCopy]);
      setLinks([...linksCopy]);
    });

    simulationRef.current = simulation;

    return () => {
      simulation.stop();
    };
  }, [data, width, height]);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const zoom = d3
      .zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.3, 3])
      .on('zoom', (event) => {
        setTransform(event.transform);
      });

    svg.call(zoom);

    return () => {
      svg.on('.zoom', null);
    };
  }, []);

  const handleNodeClick = useCallback(
    (node: GraphNode) => {
      setSelectedNode(node);
      if (node._concept && onNodeClick) {
        onNodeClick(node._concept);
      }
    },
    [onNodeClick]
  );

  const handleNodeHover = useCallback(
    (node: GraphNode | null, event?: React.MouseEvent) => {
      setHoveredNode(node);
      if (event && node) {
        setTooltipPos({ x: event.clientX + 10, y: event.clientY + 10 });
      }
    },
    []
  );

  return (
    <div className="tree-visualization" style={{ position: 'relative' }}>
      <TreeLegend />
      <svg
        ref={svgRef}
        width={width}
        height={height}
        style={{
          background: 'linear-gradient(180deg, #0f172a 0%, #1e293b 100%)',
          borderRadius: '8px',
        }}
      >
        <g transform={`translate(${transform.x},${transform.y}) scale(${transform.k})`}>
          <DomainLinks links={links} showCrossDomain={!showCrossDomainLinks} />
          {showCrossDomainLinks && <CrossDomainLinks links={links} />}
          {nodes.map((node) => (
            <g
              key={node.id}
              onMouseEnter={(e) => handleNodeHover(node, e)}
              onMouseLeave={() => handleNodeHover(null)}
            >
              <TreeNode
                node={node}
                onNodeClick={handleNodeClick}
                isSelected={selectedNode?.id === node.id}
              />
            </g>
          ))}
        </g>
      </svg>
      {hoveredNode && (
        <div style={{ position: 'fixed', left: tooltipPos.x, top: tooltipPos.y }}>
          <TreeNodeTooltip node={hoveredNode} />
        </div>
      )}
    </div>
  );
}

function TreeLegend() {
  const domains = Object.entries(DOMAIN_LABELS) as [keyof typeof DOMAIN_COLORS, string][];

  return (
    <div
      className="tree-legend"
      style={{
        position: 'absolute',
        top: '12px',
        right: '12px',
        background: 'rgba(15, 23, 42, 0.9)',
        borderRadius: '8px',
        padding: '12px',
        zIndex: 10,
      }}
    >
      <div style={{ fontSize: '12px', fontWeight: 600, marginBottom: '8px', color: '#e5e7eb' }}>
        Domains
      </div>
      {domains.map(([domain, label]) => (
        <div
          key={domain}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            marginBottom: '4px',
            fontSize: '11px',
            color: '#d1d5db',
          }}
        >
          <span
            style={{
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              background: DOMAIN_COLORS[domain],
            }}
          />
          {label}
        </div>
      ))}
      <div
        style={{
          marginTop: '8px',
          paddingTop: '8px',
          borderTop: '1px solid #374151',
          fontSize: '11px',
          color: '#9ca3af',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '4px' }}>
          <span
            style={{
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              border: '2px solid #6b7280',
            }}
          />
          Axiom
        </div>
        <div>Scroll to zoom, drag to pan</div>
      </div>
    </div>
  );
}

export { type Concept, type GraphData, type GraphNode, type GraphLink };
