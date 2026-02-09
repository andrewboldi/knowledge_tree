/**
 * KnowledgeDetailModal - Displays concept definition with Markdown + LaTeX rendering
 */

import React from 'react';
import { MarkdownRenderer } from '../markdown/MarkdownRenderer';

interface Concept {
  id: string;
  name: string;
  definitionMd: string;
  domain: string;
  subfield: string;
  complexityLevel: number;
  books: string[];
  papers: string[];
  relatedConcepts: string[];
  prerequisites: string[];
  isAxiom: boolean;
}

interface KnowledgeDetailModalProps {
  concept: Concept | null;
  isOpen: boolean;
  onClose: () => void;
}

export const KnowledgeDetailModal: React.FC<KnowledgeDetailModalProps> = ({
  concept,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !concept) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{concept.name}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <div className="modal-meta">
          <span className="domain">{concept.domain}</span>
          <span className="subfield">{concept.subfield}</span>
          <span className="level">Level: {concept.complexityLevel}</span>
        </div>

        <div className="modal-body">
          <MarkdownRenderer content={concept.definitionMd} />
        </div>

        {concept.books.length > 0 && (
          <div className="modal-section">
            <h3>Books</h3>
            <ul>
              {concept.books.map((book, i) => (
                <li key={i}>{book}</li>
              ))}
            </ul>
          </div>
        )}

        {concept.papers.length > 0 && (
          <div className="modal-section">
            <h3>Papers</h3>
            <ul>
              {concept.papers.map((paper, i) => (
                <li key={i}>{paper}</li>
              ))}
            </ul>
          </div>
        )}

        {concept.relatedConcepts.length > 0 && (
          <div className="modal-section">
            <h3>Related Concepts</h3>
            <div className="concept-chips">
              {concept.relatedConcepts.map((rel, i) => (
                <span key={i} className="chip">{rel}</span>
              ))}
            </div>
          </div>
        )}

        {concept.prerequisites.length > 0 && (
          <div className="modal-section">
            <h3>Prerequisites</h3>
            <div className="concept-chips">
              {concept.prerequisites.map((prereq, i) => (
                <span key={i} className="chip">{prereq}</span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default KnowledgeDetailModal;
