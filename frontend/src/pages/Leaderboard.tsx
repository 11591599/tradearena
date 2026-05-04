import { useState, useEffect } from 'react'
import { Trophy } from 'lucide-react'
import API from '../services/api'

interface Leader {
  rank: number
  id: number
  username: string
  pnl: number
  wins: number
}

export default function Leaderboard() {
  const [leaders, setLeaders] = useState<Leader[]>([])

  useEffect(() => {
    API.get('/leaderboard/global').then(({ data }) => {
      setLeaders(data.leaderboard || [])
    })
  }, [])

  const getRankClass = (rank: number) => {
    if (rank === 1) return 'gold'
    if (rank === 2) return 'silver'
    if (rank === 3) return 'bronze'
    return ''
  }

  return (
    <div className="animate-slide-up">
      <div className="header">
        <div className="header-logo">🏆 Leaderboard</div>
      </div>

      {leaders.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: 40 }}>
          <Trophy size={48} style={{ color: 'var(--accent)', marginBottom: 12 }} />
          <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>Be the First!</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Start trading to appear here</div>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          {leaders.map((l) => (
            <div key={l.id} className="leaderboard-item">
              <div className={`rank ${getRankClass(l.rank)}`}>#{l.rank}</div>
              <div className="avatar">{l.username?.[0]?.toUpperCase() || '?'}</div>
              <div className="user-info">
                <div className="user-name">{l.username || `Trader${l.id}`}</div>
                <div className="user-pnl">{l.wins} wins</div>
              </div>
              <div className={`user-pnl ${l.pnl >= 0 ? 'positive' : 'negative'}`}>
                {l.pnl >= 0 ? '+' : ''}{l.pnl.toFixed(2)}%
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}