import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { LoginButton, UserProfile } from './components/auth';
import { ChatPane, MinimumViableGraph } from './components/llm';
import type { MVGResponse } from './components/llm';
import { TreeVisualization, type Concept } from './components/tree';
import { sampleGraphData } from './components/tree/sampleData';
import './App.css';

function Header() {
  return (
    <header className="app-header">
      <h1>Knowledge Tree</h1>
      <nav className="header-nav">
        <UserProfile />
        <LoginButton />
      </nav>
    </header>
  );
}

function HomePage() {
  const [mvgData, setMVGData] = useState<MVGResponse | null>(null);
  const [selectedConcept, setSelectedConcept] = useState<Concept | null>(null);

  return (
    <main className="main-content">
      <h2>Welcome to Knowledge Tree</h2>
      <p>Interactive knowledge visualization with formal definitions.</p>

      <div className="llm-section">
        <ChatPane onMVGGenerated={setMVGData} />
        <MinimumViableGraph mvg={mvgData} />
      </div>

      <h2>Knowledge Tree Visualization</h2>
      <p style={{ marginBottom: '1rem', color: '#9ca3af' }}>
        Click on nodes to view definitions. Axioms are at the top, complex topics branch down.
      </p>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <TreeVisualization
          data={sampleGraphData}
          width={900}
          height={600}
          onNodeClick={setSelectedConcept}
        />
        {selectedConcept && (
          <div
            style={{
              width: '350px',
              background: '#1e293b',
              borderRadius: '8px',
              padding: '1rem',
            }}
          >
            <h3 style={{ margin: '0 0 0.5rem 0' }}>{selectedConcept.name}</h3>
            <div style={{ fontSize: '0.875rem', color: '#9ca3af', marginBottom: '1rem' }}>
              {selectedConcept.domain} | {selectedConcept.subfield} | Level{' '}
              {selectedConcept.complexity_level}
              {selectedConcept.is_axiom && ' | Axiom'}
            </div>
            <pre
              style={{
                background: '#0f172a',
                padding: '1rem',
                borderRadius: '4px',
                fontSize: '0.75rem',
                overflow: 'auto',
                whiteSpace: 'pre-wrap',
              }}
            >
              {selectedConcept.definition_md}
            </pre>
            {selectedConcept.books && selectedConcept.books.length > 0 && (
              <div style={{ marginTop: '1rem' }}>
                <strong style={{ fontSize: '0.875rem' }}>Books:</strong>
                <ul style={{ margin: '0.5rem 0', paddingLeft: '1.5rem', fontSize: '0.75rem' }}>
                  {selectedConcept.books.map((book, i) => (
                    <li key={i}>{book}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="app">
          <Header />
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
