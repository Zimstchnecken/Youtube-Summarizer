import { useNavigate } from 'react-router-dom'
import { Search, ArrowLeft } from 'lucide-react'
import SummaryDisplay from '../components/SummaryDisplay'

/**
 * Summary page — Displays the structured AI summary
 */
function Summary({ data }) {
  const navigate = useNavigate()

  // Redirect to home if no data
  if (!data) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: 'calc(100vh - 200px)',
        padding: '40px 24px',
        textAlign: 'center',
      }}>
        <div style={{ 
          padding: '24px', 
          backgroundColor: 'var(--color-surface)', 
          borderRadius: '50%',
          color: 'var(--color-text-secondary)',
          marginBottom: '24px'
        }}>
          <Search size={48} />
        </div>
        <h2 style={{
          fontSize: '24px',
          fontWeight: 700,
          color: 'var(--color-text-primary)',
          margin: '0 0 8px 0',
        }}>
          No summary available
        </h2>
        <p style={{
          color: 'var(--color-text-secondary)',
          fontSize: '16px',
          margin: '0 0 24px 0',
        }}>
          Paste a YouTube URL on the home page to generate a summary.
        </p>
        <button
          className="btn btn-primary"
          onClick={() => navigate('/')}
        >
          <ArrowLeft size={18} />
          Go to Home
        </button>
      </div>
    )
  }

  return (
    <div className="container" style={{ padding: '40px 24px' }}>
      {/* Back button */}
      <button
        className="btn btn-secondary"
        onClick={() => navigate('/')}
        style={{
          marginBottom: '32px',
          fontSize: '14px',
          height: '36px',
          padding: '8px 16px',
        }}
      >
        <ArrowLeft size={16} />
        Summarize another video
      </button>

      {/* Summary content */}
      <SummaryDisplay data={data} />
    </div>
  )
}

export default Summary
