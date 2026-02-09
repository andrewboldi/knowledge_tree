import type { MVGResponse, ConceptNode } from './types';

interface MinimumViableGraphProps {
  mvg: MVGResponse | null;
  onNodeClick?: (node: ConceptNode) => void;
}

export function MinimumViableGraph({ mvg, onNodeClick }: MinimumViableGraphProps) {
  if (!mvg) {
    return (
      <div className="mvg-container mvg-empty">
        <div className="mvg-placeholder">
          <h3>Learning Path</h3>
          <p>Ask about a concept in the chat to see the prerequisite path here.</p>
        </div>
      </div>
    );
  }

  const { target, prerequisites, path } = mvg;

  const getNodeForId = (id: string): ConceptNode | undefined => {
    if (target.id === id) return target;
    return prerequisites.find((p) => p.id === id);
  };

  const getDomainColor = (domain: string): string => {
    const colors: Record<string, string> = {
      MATH: '#4285f4',
      PHYSICS: '#34a853',
      CHEMISTRY: '#fbbc04',
      BIOLOGY: '#ea4335',
      CS: '#9333ea',
    };
    return colors[domain] || '#6b7280';
  };

  return (
    <div className="mvg-container">
      <div className="mvg-header">
        <h3>Learning Path to: {target.name}</h3>
        <span className="mvg-stats">
          {path.length} concept{path.length !== 1 ? 's' : ''} to learn
        </span>
      </div>

      <div className="mvg-path">
        {path.map((conceptId, index) => {
          const node = getNodeForId(conceptId);
          if (!node) return null;

          const isTarget = node.id === target.id;
          const domainColor = getDomainColor(node.domain);

          return (
            <div key={node.id} className="mvg-node-wrapper">
              {index > 0 && (
                <div className="mvg-connector">
                  <svg width="24" height="40" viewBox="0 0 24 40">
                    <path
                      d="M12 0 L12 40"
                      stroke="#444"
                      strokeWidth="2"
                      fill="none"
                    />
                    <path
                      d="M6 32 L12 40 L18 32"
                      stroke="#444"
                      strokeWidth="2"
                      fill="none"
                    />
                  </svg>
                </div>
              )}

              <button
                className={`mvg-node ${isTarget ? 'mvg-node-target' : ''} ${node.is_axiom ? 'mvg-node-axiom' : ''}`}
                style={{ borderColor: domainColor }}
                onClick={() => onNodeClick?.(node)}
                type="button"
              >
                <div className="mvg-node-header">
                  <span className="mvg-node-step">{index + 1}</span>
                  <span
                    className="mvg-node-domain"
                    style={{ backgroundColor: domainColor }}
                  >
                    {node.domain}
                  </span>
                </div>

                <div className="mvg-node-name">{node.name}</div>

                <div className="mvg-node-meta">
                  <span className="mvg-node-subfield">{node.subfield}</span>
                  {node.is_axiom && <span className="mvg-node-axiom-badge">Axiom</span>}
                </div>

                <div className="mvg-node-level">
                  Level {node.complexity_level}
                </div>
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
