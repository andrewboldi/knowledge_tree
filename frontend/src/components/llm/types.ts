export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ConceptNode {
  id: string;
  name: string;
  definition_md: string;
  domain: string;
  subfield: string;
  complexity_level: number;
  is_axiom: boolean;
}

export interface MVGResponse {
  target: ConceptNode;
  prerequisites: ConceptNode[];
  path: string[];
}
