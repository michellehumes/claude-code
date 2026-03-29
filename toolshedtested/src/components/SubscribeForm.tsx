'use client'

import { useState } from 'react'

export default function SubscribeForm() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setStatus('loading')

    try {
      const res = await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })

      const data = await res.json()

      if (res.ok) {
        setStatus('success')
        setMessage("You're in. Deals and reviews headed your way.")
        setEmail('')
      } else {
        setStatus('error')
        setMessage(data.error || 'Something went wrong. Try again.')
      }
    } catch {
      setStatus('error')
      setMessage('Connection error. Try again.')
    }
  }

  if (status === 'success') {
    return (
      <div style={{
        padding: '16px 24px',
        background: 'var(--bg-secondary, #141414)',
        borderRadius: '8px',
        fontFamily: 'IBM Plex Mono, monospace',
        fontSize: '14px',
        color: 'var(--accent, #ff6b00)',
      }}>
        {message}
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        required
        style={{
          flex: '1 1 240px',
          padding: '12px 16px',
          fontSize: '14px',
          fontFamily: 'Barlow, sans-serif',
          border: '1px solid var(--border, #333)',
          borderRadius: '6px',
          background: 'var(--bg-secondary, #141414)',
          color: 'var(--text-primary, #fff)',
        }}
      />
      <button
        type="submit"
        disabled={status === 'loading'}
        style={{
          padding: '12px 24px',
          fontSize: '14px',
          fontWeight: 600,
          fontFamily: 'Barlow, sans-serif',
          background: 'var(--accent, #ff6b00)',
          color: '#fff',
          border: 'none',
          borderRadius: '6px',
          cursor: status === 'loading' ? 'wait' : 'pointer',
          opacity: status === 'loading' ? 0.7 : 1,
        }}
      >
        {status === 'loading' ? 'Subscribing...' : 'Subscribe'}
      </button>
      {status === 'error' && (
        <p style={{ width: '100%', color: '#ef4444', fontSize: '13px', margin: '4px 0 0' }}>
          {message}
        </p>
      )}
    </form>
  )
}
