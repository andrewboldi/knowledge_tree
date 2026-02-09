export interface Concept {
  id: string;
  name: string;
  definition_md: string;
  domain: 'MATH' | 'PHYSICS' | 'CHEMISTRY' | 'BIOLOGY' | 'CS';
  subfield: string;
  complexity_level: number;
  is_axiom: boolean;
  is_verified: boolean;
  books?: string[];
  papers?: string[];
  articles?: string[];
  related_concepts?: string[];
  llm_summary?: string;
}

export interface TreeNode {
  id: string;
  name: string;
  domain: Concept['domain'];
  complexity_level: number;
  is_axiom: boolean;
  children?: TreeNode[];
  _concept?: Concept;
}

export interface GraphNode extends d3.SimulationNodeDatum {
  id: string;
  name: string;
  domain: Concept['domain'];
  complexity_level: number;
  is_axiom: boolean;
  _concept?: Concept;
}

export interface GraphLink extends d3.SimulationLinkDatum<GraphNode> {
  source: string | GraphNode;
  target: string | GraphNode;
  is_cross_domain?: boolean;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export const DOMAIN_COLORS: Record<Concept['domain'], string> = {
  MATH: '#3B82F6',
  PHYSICS: '#10B981',
  CHEMISTRY: '#F59E0B',
  BIOLOGY: '#EC4899',
  CS: '#8B5CF6',
};

export const DOMAIN_LABELS: Record<Concept['domain'], string> = {
  MATH: 'Mathematics',
  PHYSICS: 'Physics',
  CHEMISTRY: 'Chemistry',
  BIOLOGY: 'Biology',
  CS: 'Computer Science',
};
