import { useState, useEffect } from 'react'
import { Swords, Clock, Users } from 'lucide-react'
import API from '../services/api'

interface Round {
  id: number
  status: string
  start_time: string
  end_time: string
  prize_pool: number
  participants: number
}

export default function Arena() {
  const [rounds, setRounds] = useState<Round[]>([])
  const [activeRound, setActiveRound] = useState<Round | null>(null)

  useEffect(() => {
    API.get('/rounds/active').then(({ data }) => {
      if (data.round) setActiveRound(data.round)
    })
    API.get('/rounds/history').then(({ data }) => {
      setRounds(data.rounds || [])
    })
  }, [])

  return (
    <div className="animate-slide-up">
      <div className="header">
        <div className="header-logo">⚔️ Arena</div>
      </div>

      {/* Active Round */}
      {activeRound ? (
        <div className="round-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className={`round-status ${activeRound.status}`}>{activeRound.status}</span>
            <span style={{ color: 'var(--text-secondary)', fontSize: 12 }}>
              <Clock size={12} /> {activeRound.end_time}
            </span>
          </div>
          <div className="round-prize">
            {activeRound.prize_pool} <span>TON</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--text-secondary)', fontSize: 13 }}>
            <Users size={14} /> {activeRound.participants} traders
          </div>
        </div>
      ) : (
        <div className="round-card">
          <div style={{ textAlign: 'center', padding: 20 }}>
            <Swords size={48} style={{ color: 'var(--accent)', marginBottom: 12 }} />
            <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>No Active Round</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Next round starting soon...</div>
          </div>
        </div>
      )}

      {/* History */}
      <div className="card">
        <div className="card-title">Past Rounds</div>
        {rounds.length === 0 ? (
          <div style={{ color: 'var(--text-muted)', fontSize: 14, textAlign: 'center', padding: 20 }}>
            No completed rounds yet
          </div>
        ) : (
          rounds.map((r) => (
            <div key={r.id} className="leaderboard-item">
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: 14 }}>Round #{r.id}</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: 12 }}>{r.participants} participants</div>
              </div>
              <div style={{ fontWeight: 700, color: 'var(--accent)' }}>{r.prize_pool} TON</div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}