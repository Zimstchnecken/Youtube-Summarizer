import { Clock, AlignLeft, PlaySquare } from 'lucide-react'
import TimestampCard from './TimestampCard'

/**
 * SummaryDisplay — Renders the full video summary with metadata and timestamp cards
 */
function SummaryDisplay({ data }) {
  if (!data) return null

  const { title, duration, summary, video_id, url } = data

  return (
    <div className="animate-fade-in" style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '24px',
      width: '100%',
    }}>
      {/* Video info header */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        paddingBottom: '20px',
        borderBottom: '1px solid var(--color-border)',
      }}>
        <h2 style={{
          fontSize: '24px',
          fontWeight: 700,
          letterSpacing: '-0.025em',
          color: 'var(--color-text-primary)',
          margin: 0,
        }}>
          {title}
        </h2>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
          flexWrap: 'wrap',
        }}>
          <span style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '14px',
            color: 'var(--color-text-secondary)',
          }}>
            <Clock size={16} />
            {duration}
          </span>
          <span style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '14px',
            color: 'var(--color-text-secondary)',
          }}>
            <AlignLeft size={16} />
            {summary.length} key points
          </span>
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              fontSize: '14px',
              color: 'var(--color-secondary)',
            }}
          >
            <PlaySquare size={16} />
            Watch on YouTube
          </a>
        </div>
      </div>

      {/* Summary points */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
      }}>
        <h3 style={{
          fontSize: '16px',
          fontWeight: 600,
          color: 'var(--color-text-secondary)',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          margin: '0 0 8px 0',
        }}>
          Key Points
        </h3>
        {summary.map((point, index) => (
          <TimestampCard
            key={index}
            timestamp={point.timestamp}
            point={point.point}
            videoId={video_id}
            index={index}
          />
        ))}
      </div>
    </div>
  )
}

export default SummaryDisplay
