/**
 * TimestampCard — Individual summary point with clickable timestamp
 */
function TimestampCard({ timestamp, point, videoId, index }) {
  /**
   * Convert timestamp string (MM:SS or HH:MM:SS) to seconds for YouTube link
   */
  const timestampToSeconds = (ts) => {
    const parts = ts.split(':').map(Number)
    if (parts.length === 3) {
      return parts[0] * 3600 + parts[1] * 60 + parts[2]
    }
    return parts[0] * 60 + (parts[1] || 0)
  }

  const seconds = timestampToSeconds(timestamp)
  const youtubeLink = `https://www.youtube.com/watch?v=${videoId}&t=${seconds}s`

  return (
    <div
      className="animate-fade-in-up"
      style={{
        display: 'flex',
        gap: '16px',
        padding: '16px',
        backgroundColor: 'var(--color-surface)',
        borderLeft: '3px solid var(--color-primary)',
        borderRadius: 'var(--radius-sm)',
        transition: 'all 0.2s ease',
        animationDelay: `${index * 100}ms`,
        animationFillMode: 'both',
        cursor: 'pointer',
      }}
      onClick={() => window.open(youtubeLink, '_blank')}
      onMouseEnter={(e) => {
        e.currentTarget.style.backgroundColor = 'var(--color-surface-hover)'
        e.currentTarget.style.transform = 'translateX(4px)'
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.backgroundColor = 'var(--color-surface)'
        e.currentTarget.style.transform = 'translateX(0)'
      }}
      role="link"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter') window.open(youtubeLink, '_blank')
      }}
    >
      <a
        href={youtubeLink}
        target="_blank"
        rel="noopener noreferrer"
        onClick={(e) => e.stopPropagation()}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          minWidth: '64px',
          height: '28px',
          padding: '0 8px',
          backgroundColor: 'rgba(255, 77, 77, 0.1)',
          color: 'var(--color-primary)',
          borderRadius: 'var(--radius-sm)',
          fontFamily: 'monospace',
          fontSize: '13px',
          fontWeight: 600,
          textDecoration: 'none',
          flexShrink: 0,
        }}
      >
        {timestamp}
      </a>
      <p style={{
        margin: 0,
        fontSize: '15px',
        lineHeight: '1.5',
        color: 'var(--color-text-primary)',
      }}>
        {point}
      </p>
    </div>
  )
}

export default TimestampCard
