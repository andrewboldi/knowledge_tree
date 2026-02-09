/**
 * ChatPane - LLM chat interface for knowledge exploration
 */

import React, { useState } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export const ChatPane: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    // TODO: Implement LLM API call
    const assistantMessage: Message = {
      role: 'assistant',
      content: 'LLM integration not yet implemented.',
    };
    setMessages((prev) => [...prev, assistantMessage]);
    setLoading(false);
  };

  return (
    <div className="chat-pane">
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {loading && <div className="message loading">Thinking...</div>}
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask about concepts..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatPane;
