import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { LoginButton, UserProfile } from './components/auth';
import { ChatPane, MinimumViableGraph } from './components/llm';
import type { MVGResponse } from './components/llm';
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

  return (
    <main className="main-content">
      <h2>Welcome to Knowledge Tree</h2>
      <p>Interactive knowledge visualization with formal definitions.</p>

      <div className="llm-section">
        <ChatPane onMVGGenerated={setMVGData} />
        <MinimumViableGraph mvg={mvgData} />
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
