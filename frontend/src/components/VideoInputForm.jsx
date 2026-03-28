import { useState } from 'react'
import { Zap, AlertCircle } from 'lucide-react'

/**
 * VideoInputForm — YouTube URL input with validation and submit
 */
function VideoInputForm({ onSubmit, isLoading }) {
  const [url, setUrl] = useState('')
  const [error, setError] = useState('')

  const youtubeRegex = /^https?:\/\/(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)[\w-]{11}/

  const validateUrl = (value) => {
    if (!value.trim()) {
      return 'Please enter a YouTube URL'
    }
    if (!youtubeRegex.test(value.trim())) {
      return 'Please enter a valid YouTube URL'
    }
    return ''
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const validationError = validateUrl(url)
    if (validationError) {
      setError(validationError)
      return
    }
    setError('')
    onSubmit(url.trim())
  }

  const handleChange = (e) => {
    setUrl(e.target.value)
    if (error) setError('')
  }

  return (
    <form onSubmit={handleSubmit} id="video-input-form" style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '12px',
      width: '100%',
    }}>
      <div style={{
        display: 'flex',
        gap: '12px',
        width: '100%',
      }}>
        <input
          id="youtube-url-input"
          type="url"
          className="input"
          placeholder="Paste YouTube URL here..."
          value={url}
          onChange={handleChange}
          disabled={isLoading}
          autoFocus
          style={{
            flex: 1,
            height: '52px',
            fontSize: '16px',
          }}
        />
        <button
          id="summarize-button"
          type="submit"
          className="btn btn-primary"
          disabled={isLoading || !url.trim()}
          style={{
            height: '52px',
            padding: '12px 32px',
            fontSize: '16px',
            whiteSpace: 'nowrap',
          }}
        >
          {isLoading ? (
            <>
              <span style={{
                display: 'inline-block',
                width: '16px',
                height: '16px',
                border: '2px solid rgba(255,255,255,0.3)',
                borderTopColor: '#fff',
                borderRadius: '50%',
                animation: 'spin 0.6s linear infinite',
              }} />
              Summarizing...
            </>
          ) : (
            <>
              <Zap size={18} />
              Summarize
            </>
          )}
        </button>
      </div>

      {error && (
        <p className="text-error animate-fade-in" style={{ display: 'flex', alignItems: 'center', gap: '6px', margin: 0 }}>
          <AlertCircle size={16} />
          {error}
        </p>
      )}
    </form>
  )
}

export default VideoInputForm
