/**
 * AddKnowledgeModal - Markdown editor for adding new definitions
 */

import React, { useState } from 'react';
import { MarkdownRenderer } from '../markdown/MarkdownRenderer';

interface AddKnowledgeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: NewConceptData) => void;
}

interface NewConceptData {
  name: string;
  domain: string;
  subfield: string;
  definitionMd: string;
  prerequisites: string[];
  books: string[];
  papers: string[];
}

const DOMAINS = ['MATH', 'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'CS'];

export const AddKnowledgeModal: React.FC<AddKnowledgeModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}) => {
  const [name, setName] = useState('');
  const [domain, setDomain] = useState('MATH');
  const [subfield, setSubfield] = useState('');
  const [definitionMd, setDefinitionMd] = useState('');
  const [showPreview, setShowPreview] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      name,
      domain,
      subfield,
      definitionMd,
      prerequisites: [],
      books: [],
      papers: [],
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Add Definition</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <label>
              Term Name:
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </label>
          </div>

          <div className="form-row">
            <label>
              Domain:
              <select value={domain} onChange={(e) => setDomain(e.target.value)}>
                {DOMAINS.map((d) => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </label>

            <label>
              Subfield:
              <input
                type="text"
                value={subfield}
                onChange={(e) => setSubfield(e.target.value)}
              />
            </label>
          </div>

          <div className="form-row">
            <label>
              Definition (Markdown + LaTeX):
              <div className="editor-toggle">
                <button
                  type="button"
                  className={!showPreview ? 'active' : ''}
                  onClick={() => setShowPreview(false)}
                >
                  Edit
                </button>
                <button
                  type="button"
                  className={showPreview ? 'active' : ''}
                  onClick={() => setShowPreview(true)}
                >
                  Preview
                </button>
              </div>
              {showPreview ? (
                <div className="preview-pane">
                  <MarkdownRenderer content={definitionMd} />
                </div>
              ) : (
                <textarea
                  value={definitionMd}
                  onChange={(e) => setDefinitionMd(e.target.value)}
                  rows={10}
                  placeholder="A **Hilbert space** is a complete inner product space..."
                />
              )}
            </label>
          </div>

          <div className="form-actions">
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit">Submit</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddKnowledgeModal;
