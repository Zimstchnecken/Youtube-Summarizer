import { Bot } from 'lucide-react'

/**
 * LoadingSpinner — Shimmer skeleton cards mimicking summary layout
 */
function LoadingSpinner() {
  const skeletonCards = Array.from({ length: 5 }, (_, i) => i)

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      width: '100%',
    }}>
      {/* Title skeleton */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '8px' }}>
        <div className="animate-shimmer" style={{
          width: '60%',
          height: '28px',
          borderRadius: 'var(--radius-sm)',
        }} />
        <div className="animate-shimmer" style={{
          width: '120px',
          height: '20px',
          borderRadius: 'var(--radius-sm)',
        }} />
      </div>

      {/* Card skeletons */}
      {skeletonCards.map((i) => (
        <div
          key={i}
          style={{
            display: 'flex',
            gap: '16px',
            padding: '16px',
            borderLeft: '3px solid var(--color-border)',
            borderRadius: 'var(--radius-sm)',
            animationDelay: `${i * 100}ms`,
          }}
        >
          <div className="animate-shimmer" style={{
            width: '64px',
            height: '28px',
            borderRadius: 'var(--radius-sm)',
            flexShrink: 0,
          }} />
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div className="animate-shimmer" style={{
              width: `${80 - i * 10}%`,
              height: '16px',
              borderRadius: 'var(--radius-sm)',
            }} />
            <div className="animate-shimmer" style={{
              width: `${60 - i * 5}%`,
              height: '16px',
              borderRadius: 'var(--radius-sm)',
            }} />
          </div>
        </div>
      ))}

      {/* Status message */}
      <p style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '6px',
        color: 'var(--color-text-secondary)',
        fontSize: '14px',
        marginTop: '8px',
      }}>
        <Bot size={16} /> AI is analyzing the video transcript...
      </p>
    </div>
  )
}

export default LoadingSpinner
