import { useState, useRef, useEffect } from 'react';
import type { FormEvent } from 'react';
import type { ChatMessage, MVGResponse } from './types';

interface ChatPaneProps {
  onMVGGenerated?: (mvg: MVGResponse) => void;
}

export function ChatPane({ onMVGGenerated }: ChatPaneProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/mvg/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage.content }),
      });

      if (!response.ok) {
        throw new Error(`Failed to generate MVG: ${response.statusText}`);
      }

      const data: MVGResponse = await response.json();

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: formatMVGResponse(data),
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      onMVGGenerated?.(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);

      const errorResponse: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setLoading(false);
    }
  };

  const formatMVGResponse = (mvg: MVGResponse): string => {
    const { target, prerequisites, path } = mvg;
    let response = `To understand **${target.name}**, you'll need to learn these concepts in order:\n\n`;

    path.forEach((conceptId, index) => {
      const concept = prerequisites.find((p) => p.id === conceptId) ||
                      (target.id === conceptId ? target : null);
      if (concept) {
        response += `${index + 1}. **${concept.name}** (${concept.domain} - ${concept.subfield})\n`;
      }
    });

    return response;
  };

  return (
    <div className="chat-pane">
      <div className="chat-header">
        <h3>Learning Path Assistant</h3>
        <p>Ask about any concept to get a prerequisite learning path</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-placeholder">
            <p>Ask me about a topic you want to learn!</p>
            <p className="chat-examples">
              Examples: "What do I need to learn before eigenvalues?",
              "Path to understanding Gibbs free energy"
            </p>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message chat-message-${msg.role}`}>
            <div className="chat-message-content">{msg.content}</div>
            <div className="chat-message-time">
              {msg.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-message chat-message-assistant">
            <div className="chat-loading">Generating learning path...</div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="chat-error">
          {error}
        </div>
      )}

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="What concept do you want to learn?"
          disabled={loading}
          className="chat-input"
        />
        <button type="submit" disabled={loading || !input.trim()} className="chat-submit">
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>
    </div>
  );
}
