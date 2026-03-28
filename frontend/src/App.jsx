import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Video } from 'lucide-react'
import Home from './pages/Home'
import Summary from './pages/Summary'
import ThemeToggle from './components/ThemeToggle'

function App() {
  const [summaryData, setSummaryData] = useState(null)
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'dark'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }

  return (
    <BrowserRouter>
      {/* Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '16px 24px',
        borderBottom: '1px solid var(--color-border)',
        backgroundColor: 'var(--color-surface)',
      }}>
        <a href="/" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          color: 'var(--color-text-primary)',
          fontWeight: 700,
          fontSize: '18px',
          textDecoration: 'none',
        }}>
          <Video size={24} color="var(--color-primary)" />
          <span>YT Summarizer</span>
        </a>
        <ThemeToggle theme={theme} onToggle={toggleTheme} />
      </header>

      {/* Main content */}
      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={
            <Home onSummaryComplete={setSummaryData} />
          } />
          <Route path="/summary" element={
            <Summary data={summaryData} />
          } />
        </Routes>
      </main>

      {/* Footer */}
      <footer style={{
        textAlign: 'center',
        padding: '24px',
        borderTop: '1px solid var(--color-border)',
        color: 'var(--color-text-secondary)',
        fontSize: '14px',
      }}>
        <p>
          Powered by <a href="https://openrouter.ai/" target="_blank" rel="noopener noreferrer"
            style={{ color: 'var(--color-secondary)' }}>OpenRouter</a>
          {' · '}
          Built by Miro
        </p>
      </footer>
    </BrowserRouter>
  )
}

export default App
