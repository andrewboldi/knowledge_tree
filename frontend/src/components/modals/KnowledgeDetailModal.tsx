import { MarkdownRenderer } from '../markdown/MarkdownRenderer';
import './KnowledgeDetailModal.css';

export interface Concept {
  id: string;
  name: string;
  definition_md: string;
  domain: string;
  subfield: string;
  complexity_level: number;
  books: string[];
  papers: string[];
  articles?: string[];
  related_concepts: string[];
  prerequisites: string[];
  llm_summary?: string;
  is_axiom: boolean;
  is_verified?: boolean;
}

interface KnowledgeDetailModalProps {
  concept: Concept;
  onClose: () => void;
  onConceptClick?: (conceptId: string) => void;
  onAddBook?: () => void;
  onAddPaper?: () => void;
  onAddNote?: () => void;
}

export function KnowledgeDetailModal({
  concept,
  onClose,
  onConceptClick,
  onAddBook,
  onAddPaper,
  onAddNote,
}: KnowledgeDetailModalProps) {
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <div
      className="modal-backdrop"
      onClick={handleBackdropClick}
      onKeyDown={handleKeyDown}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="modal-content">
        <header className="modal-header">
          <h2 id="modal-title" className="modal-title">{concept.name}</h2>
          <button
            className="modal-close-btn"
            onClick={onClose}
            aria-label="Close modal"
          >
            &times;
          </button>
        </header>

        <div className="modal-meta">
          <span className="meta-badge domain-badge">{concept.domain}</span>
          <span className="meta-badge subfield-badge">{concept.subfield.replace(/_/g, ' ')}</span>
          <span className="meta-badge level-badge">Level {concept.complexity_level}</span>
          {concept.is_axiom && <span className="meta-badge axiom-badge">Axiom</span>}
        </div>

        <section className="modal-section definition-section">
          <MarkdownRenderer content={concept.definition_md} className="definition-content" />
        </section>

        {concept.books.length > 0 && (
          <section className="modal-section">
            <h3 className="section-title">Books</h3>
            <ul className="resource-list">
              {concept.books.map((book, index) => (
                <li key={index} className="resource-item">{book}</li>
              ))}
            </ul>
          </section>
        )}

        {concept.papers.length > 0 && (
          <section className="modal-section">
            <h3 className="section-title">Papers</h3>
            <ul className="resource-list">
              {concept.papers.map((paper, index) => (
                <li key={index} className="resource-item">{paper}</li>
              ))}
            </ul>
          </section>
        )}

        {concept.related_concepts.length > 0 && (
          <section className="modal-section">
            <h3 className="section-title">Related Concepts</h3>
            <div className="concept-tags">
              {concept.related_concepts.map((conceptId) => (
                <button
                  key={conceptId}
                  className="concept-tag"
                  onClick={() => onConceptClick?.(conceptId)}
                >
                  {conceptId}
                </button>
              ))}
            </div>
          </section>
        )}

        {concept.prerequisites.length > 0 && (
          <section className="modal-section">
            <h3 className="section-title">Prerequisites</h3>
            <div className="concept-tags">
              {concept.prerequisites.map((prereqId) => (
                <button
                  key={prereqId}
                  className="concept-tag prerequisite-tag"
                  onClick={() => onConceptClick?.(prereqId)}
                >
                  {prereqId}
                </button>
              ))}
            </div>
          </section>
        )}

        <section className="modal-section user-notes-section">
          <h3 className="section-title">Your Notes</h3>
          <div className="user-actions">
            <button className="action-btn" onClick={onAddBook}>+ Add Book</button>
            <button className="action-btn" onClick={onAddPaper}>+ Add Paper</button>
            <button className="action-btn" onClick={onAddNote}>+ Add Note</button>
          </div>
        </section>
      </div>
    </div>
  );
}
