/**
 * MinimumViableGraph - Display learning path to a target concept
 */

import React, { useState } from 'react';

interface MVGNode {
  id: string;
  name: string;
  domain: string;
  isKnown: boolean;
}

interface MinimumViableGraphProps {
  onNodeClick: (nodeId: string) => void;
}

export const MinimumViableGraph: React.FC<MinimumViableGraphProps> = ({
  onNodeClick,
}) => {
  const [targetConcept, setTargetConcept] = useState('');
  const [path, setPath] = useState<MVGNode[]>([]);
  const [loading, setLoading] = useState(false);

  const generateMVG = async () => {
    if (!targetConcept.trim() || loading) return;

    setLoading(true);
    // TODO: Call MVG API endpoint
    setPath([]);
    setLoading(false);
  };

  return (
    <div className="mvg-container">
      <div className="mvg-input">
        <input
          type="text"
          value={targetConcept}
          onChange={(e) => setTargetConcept(e.target.value)}
          placeholder="Enter target concept (e.g., Hilbert Space)"
        />
        <button onClick={generateMVG} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Learning Path'}
        </button>
      </div>

      {path.length > 0 && (
        <div className="mvg-path">
          <h3>Learning Path</h3>
          <div className="path-nodes">
            {path.map((node, i) => (
              <React.Fragment key={node.id}>
                <div
                  className={`path-node ${node.isKnown ? 'known' : ''}`}
                  onClick={() => onNodeClick(node.id)}
                >
                  <span className="node-name">{node.name}</span>
                  <span className="node-domain">{node.domain}</span>
                </div>
                {i < path.length - 1 && <span className="path-arrow">→</span>}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MinimumViableGraph;
