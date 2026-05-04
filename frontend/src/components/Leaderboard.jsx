import React, { useState, useEffect } from 'react'
import api from '../api'

export default function Leaderboard() {
  const [players, setPlayers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const res = await api.get('/leaderboard/global')
        setPlayers(res.data)
      } catch (e) {
        console.error('Leaderboard fetch error:', e)
      } finally {
        setLoading(false)
      }
    }
    fetchLeaderboard()
    const interval = setInterval(fetchLeaderboard, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="loading"><div className="spinner" /></div>
  }

  return (
    <div className="card">
      <h3 style={{ marginBottom: 12, fontSize: 18 }}>🏆 Leaderboard</h3>
      {players.length === 0 ? (
        <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: 20 }}>
          No players yet. Be the first!
        </p>
      ) : (
        players.map((p, i) => (
          <div key={i} className="leaderboard-item">
            <span className={`rank ${p.rank <= 3 ? `rank-${p.rank}` : ''}`}>
              {p.rank <= 3 ? ['🥇', '🥈', '🥉'][p.rank - 1] : `#${p.rank}`}
            </span>
            <div style={{ flex: 1, marginLeft: 12 }}>
              <div style={{ fontWeight: 600, fontSize: 14 }}>
                {p.username}
                {p.is_premium && <span className="badge badge-premium" style={{ marginLeft: 6 }}>PRO</span>}
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
                {p.wins} wins
              </div>
            </div>
            <div style={{
              fontWeight: 700,
              color: p.pnl >= 0 ? 'var(--green)' : 'var(--red)',
              fontFamily: 'monospace',
            }}>
              {p.pnl >= 0 ? '+' : ''}{p.pnl.toLocaleString()}
            </div>
          </div>
        ))
      )}
    </div>
  )
}