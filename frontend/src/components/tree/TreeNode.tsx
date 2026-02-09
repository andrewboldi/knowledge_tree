/**
 * TreeNode - Individual node in the knowledge tree
 */

import React from 'react';

interface TreeNodeProps {
  id: string;
  name: string;
  domain: string;
  isAxiom: boolean;
  onClick: (id: string) => void;
}

export const TreeNode: React.FC<TreeNodeProps> = ({
  id,
  name,
  domain,
  isAxiom,
  onClick,
}) => {
  return (
    <div
      className={`tree-node ${isAxiom ? 'axiom' : ''}`}
      onClick={() => onClick(id)}
    >
      <span className="node-name">{name}</span>
      <span className="node-domain">{domain}</span>
    </div>
  );
};

export default TreeNode;
