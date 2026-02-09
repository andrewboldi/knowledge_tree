import { useState, useCallback } from 'react';
import { MarkdownRenderer } from '../markdown/MarkdownRenderer';
import { useAuth } from '../../hooks/useAuth';
import './AddKnowledgeModal.css';

const DOMAINS = ['MATH', 'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'CS'] as const;
type Domain = typeof DOMAINS[number];

interface Prerequisite {
  id: string;
  name: string;
}

interface AddKnowledgeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit?: (data: ConceptFormData) => Promise<void>;
}

export interface ConceptFormData {
  name: string;
  domain: Domain;
  subfield: string;
  definition_md: string;
  prerequisites: Prerequisite[];
  books: string[];
  papers: string[];
}

const EXAMPLE_DEFINITION = `A **Hilbert space** is a complete inner product space.

That is, a vector space $H$ over $\\mathbb{R}$ or $\\mathbb{C}$ equipped with an inner product $\\langle \\cdot, \\cdot \\rangle: H \\times H \\to F$ such that the induced norm

$$\\|x\\| = \\sqrt{\\langle x, x \\rangle}$$

makes $H$ a complete metric space.`;

export function AddKnowledgeModal({ isOpen, onClose, onSubmit }: AddKnowledgeModalProps) {
  const { user } = useAuth();

  const [name, setName] = useState('');
  const [domain, setDomain] = useState<Domain>('MATH');
  const [subfield, setSubfield] = useState('');
  const [definitionMd, setDefinitionMd] = useState('');
  const [prerequisites, setPrerequisites] = useState<Prerequisite[]>([]);
  const [books, setBooks] = useState<string[]>([]);
  const [papers, setPapers] = useState<string[]>([]);

  const [prerequisiteSearch, setPrerequisiteSearch] = useState('');
  const [newBook, setNewBook] = useState('');
  const [newPaper, setNewPaper] = useState('');

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const resetForm = useCallback(() => {
    setName('');
    setDomain('MATH');
    setSubfield('');
    setDefinitionMd('');
    setPrerequisites([]);
    setBooks([]);
    setPapers([]);
    setPrerequisiteSearch('');
    setNewBook('');
    setNewPaper('');
    setError(null);
  }, []);

  const handleClose = useCallback(() => {
    resetForm();
    onClose();
  }, [resetForm, onClose]);

  const handleAddPrerequisite = useCallback(() => {
    if (!prerequisiteSearch.trim()) return;

    // For now, create a simple prerequisite with generated ID
    // In a full implementation, this would search the API
    const newPrereq: Prerequisite = {
      id: `prereq-${Date.now()}`,
      name: prerequisiteSearch.trim(),
    };

    setPrerequisites(prev => [...prev, newPrereq]);
    setPrerequisiteSearch('');
  }, [prerequisiteSearch]);

  const handleRemovePrerequisite = useCallback((id: string) => {
    setPrerequisites(prev => prev.filter(p => p.id !== id));
  }, []);

  const handleAddBook = useCallback(() => {
    if (!newBook.trim()) return;
    setBooks(prev => [...prev, newBook.trim()]);
    setNewBook('');
  }, [newBook]);

  const handleRemoveBook = useCallback((index: number) => {
    setBooks(prev => prev.filter((_, i) => i !== index));
  }, []);

  const handleAddPaper = useCallback(() => {
    if (!newPaper.trim()) return;
    setPapers(prev => [...prev, newPaper.trim()]);
    setNewPaper('');
  }, [newPaper]);

  const handleRemovePaper = useCallback((index: number) => {
    setPapers(prev => prev.filter((_, i) => i !== index));
  }, []);

  const handleSubmit = useCallback(async () => {
    if (!name.trim()) {
      setError('Term name is required');
      return;
    }
    if (!definitionMd.trim()) {
      setError('Definition is required');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    const formData: ConceptFormData = {
      name: name.trim(),
      domain,
      subfield: subfield.trim(),
      definition_md: definitionMd.trim(),
      prerequisites,
      books,
      papers,
    };

    try {
      if (onSubmit) {
        await onSubmit(formData);
      } else {
        // Default API submission
        const response = await fetch('/api/contributions/concept', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        if (!response.ok) {
          throw new Error('Failed to submit concept');
        }
      }

      handleClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  }, [name, domain, subfield, definitionMd, prerequisites, books, papers, onSubmit, handleClose]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent, action: () => void) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      action();
    }
  }, []);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-container" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Add Definition</h2>
          <button className="modal-close" onClick={handleClose} aria-label="Close">
            &times;
          </button>
        </div>

        <div className="modal-body">
          {!user && (
            <div className="auth-warning">
              Sign in to submit definitions
            </div>
          )}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="form-row">
            <div className="form-group form-group-large">
              <label htmlFor="term-name">Term Name</label>
              <input
                id="term-name"
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="e.g., Hilbert Space"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="domain">Domain</label>
              <select
                id="domain"
                value={domain}
                onChange={e => setDomain(e.target.value as Domain)}
              >
                {DOMAINS.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>

            <div className="form-group form-group-large">
              <label htmlFor="subfield">Subfield</label>
              <input
                id="subfield"
                type="text"
                value={subfield}
                onChange={e => setSubfield(e.target.value)}
                placeholder="e.g., functional_analysis"
              />
            </div>
          </div>

          <div className="editor-section">
            <label>Definition (Markdown + LaTeX)</label>
            <div className="editor-container">
              <div className="editor-pane">
                <textarea
                  value={definitionMd}
                  onChange={e => setDefinitionMd(e.target.value)}
                  placeholder={EXAMPLE_DEFINITION}
                  rows={10}
                />
              </div>
              <div className="preview-pane">
                <div className="preview-label">Preview</div>
                <div className="preview-content">
                  {definitionMd ? (
                    <MarkdownRenderer content={definitionMd} />
                  ) : (
                    <span className="preview-placeholder">
                      Preview will appear here...
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="form-section">
            <label>Prerequisites (link to existing)</label>
            <div className="input-with-button">
              <input
                type="text"
                value={prerequisiteSearch}
                onChange={e => setPrerequisiteSearch(e.target.value)}
                onKeyDown={e => handleKeyDown(e, handleAddPrerequisite)}
                placeholder="Search for concepts..."
              />
              <button type="button" onClick={handleAddPrerequisite}>
                + Add
              </button>
            </div>
            {prerequisites.length > 0 && (
              <div className="tag-list">
                {prerequisites.map(prereq => (
                  <span key={prereq.id} className="tag">
                    {prereq.name}
                    <button
                      type="button"
                      className="tag-remove"
                      onClick={() => handleRemovePrerequisite(prereq.id)}
                      aria-label={`Remove ${prereq.name}`}
                    >
                      &times;
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          <div className="form-row">
            <div className="form-section form-section-half">
              <label>Books</label>
              <div className="input-with-button">
                <input
                  type="text"
                  value={newBook}
                  onChange={e => setNewBook(e.target.value)}
                  onKeyDown={e => handleKeyDown(e, handleAddBook)}
                  placeholder="e.g., Linear Algebra - Axler, Ch. 1"
                />
                <button type="button" onClick={handleAddBook}>
                  + Add
                </button>
              </div>
              {books.length > 0 && (
                <ul className="resource-list">
                  {books.map((book, index) => (
                    <li key={index}>
                      {book}
                      <button
                        type="button"
                        className="resource-remove"
                        onClick={() => handleRemoveBook(index)}
                        aria-label={`Remove ${book}`}
                      >
                        &times;
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="form-section form-section-half">
              <label>Papers</label>
              <div className="input-with-button">
                <input
                  type="text"
                  value={newPaper}
                  onChange={e => setNewPaper(e.target.value)}
                  onKeyDown={e => handleKeyDown(e, handleAddPaper)}
                  placeholder="e.g., arXiv:1234.5678"
                />
                <button type="button" onClick={handleAddPaper}>
                  + Add
                </button>
              </div>
              {papers.length > 0 && (
                <ul className="resource-list">
                  {papers.map((paper, index) => (
                    <li key={index}>
                      {paper}
                      <button
                        type="button"
                        className="resource-remove"
                        onClick={() => handleRemovePaper(index)}
                        aria-label={`Remove ${paper}`}
                      >
                        &times;
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button
            type="button"
            className="btn-secondary"
            onClick={handleClose}
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            type="button"
            className="btn-primary"
            onClick={handleSubmit}
            disabled={isSubmitting || !user}
          >
            {isSubmitting ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      </div>
    </div>
  );
}
