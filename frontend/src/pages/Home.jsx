import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Video, Zap, Target, CheckCircle } from 'lucide-react'
import VideoInputForm from '../components/VideoInputForm'
import LoadingSpinner from '../components/LoadingSpinner'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Home page — Hero section with URL input form
 */
function Home({ onSummaryComplete }) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (url) => {
    setIsLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_BASE_URL}/api/summarize`, {
        url: url,
      })

      onSummaryComplete(response.data)
      navigate('/summary')
    } catch (err) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else if (err.code === 'ERR_NETWORK') {
        setError('Cannot connect to the server. Make sure the backend is running.')
      } else {
        setError('Something went wrong. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: 'calc(100vh - 200px)',
      padding: '40px 24px',
    }}>
      {/* Hero */}
      <div className="animate-fade-in" style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '16px',
        marginBottom: '40px',
        textAlign: 'center',
      }}>
        <div style={{ 
          padding: '16px', 
          backgroundColor: 'rgba(255, 77, 77, 0.1)', 
          borderRadius: '50%',
          color: 'var(--color-primary)'
        }}>
          <Video size={48} />
        </div>
        <h1 style={{
          fontSize: '40px',
          fontWeight: 700,
          letterSpacing: '-0.025em',
          color: 'var(--color-text-primary)',
          margin: 0,
          lineHeight: 1.2,
        }}>
          YouTube Video<br />
          <span style={{ color: 'var(--color-primary)' }}>Summarizer</span>
        </h1>
        <p style={{
          fontSize: '18px',
          color: 'var(--color-text-secondary)',
          maxWidth: '480px',
          margin: 0,
        }}>
          Paste a YouTube URL and get an AI-powered summary with key points and timestamps — powered by Open Router.
        </p>
      </div>

      {/* Input form */}
      <div style={{
        width: '100%',
        maxWidth: '600px',
      }}>
        <VideoInputForm onSubmit={handleSubmit} isLoading={isLoading} />
      </div>

      {/* Error message */}
      {error && (
        <div className="animate-fade-in" style={{
          marginTop: '16px',
          padding: '12px 20px',
          backgroundColor: 'rgba(248, 113, 113, 0.1)',
          border: '1px solid rgba(248, 113, 113, 0.3)',
          borderRadius: 'var(--radius-md)',
          color: 'var(--color-error)',
          fontSize: '14px',
          maxWidth: '600px',
          width: '100%',
          textAlign: 'center',
        }}>
          {error}
        </div>
      )}

      {/* Loading state */}
      {isLoading && (
        <div style={{
          marginTop: '40px',
          width: '100%',
          maxWidth: '600px',
        }}>
          <LoadingSpinner />
        </div>
      )}

      {/* Feature hints */}
      {!isLoading && !error && (
        <div className="animate-fade-in" style={{
          display: 'flex',
          gap: '24px',
          marginTop: '48px',
          flexWrap: 'wrap',
          justifyContent: 'center',
        }}>
          {[
            { icon: <Zap size={18} />, text: 'AI-Powered Summaries' },
            { icon: <Target size={18} />, text: 'Key Points + Timestamps' },
            { icon: <CheckCircle size={18} />, text: 'Free to Use' },
          ].map((feature, i) => (
            <div key={i} style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '14px',
              color: 'var(--color-text-secondary)',
            }}>
              <span style={{ display: 'flex', color: 'var(--color-primary)' }}>
                {feature.icon}
              </span>
              <span>{feature.text}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Home
