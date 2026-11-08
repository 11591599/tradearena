import { useState } from 'react'
import { CheckCircle2, Coins, Sparkles, TimerReset } from 'lucide-react'

const missions = [
  { id: 1, title: 'Daily login', detail: 'Open the app today', reward: '+50 credits + 1 ticket', tone: 'easy' },
  { id: 2, title: 'Trade streak', detail: 'Make your first trade', reward: '+80 credits + 2 tickets', tone: 'medium' },
  { id: 3, title: 'Battle entry', detail: 'Join a ranked battle', reward: '+120 credits + 2 tickets', tone: 'medium' },
  { id: 4, title: 'Arena legend', detail: 'Win 3 battles', reward: '+220 credits + 3 tickets', tone: 'hard' },
]

export default function QuestBoard() {
  const [claimed, setClaimed] = useState<number[]>([])

  const handleClaim = (id: number) => {
    setClaimed((prev) => (prev.includes(id) ? prev : [...prev, id]))
  }

  return (
    <div className="animate-slide-up">
      <div className="header">
        <div className="header-logo">✨ Quests</div>
      </div>

      <div className="card">
        <div className="card-title">Daily & seasonal missions</div>
        {missions.map((mission) => (
          <div key={mission.id} className="quest-item">
            <div>
              <div className="quest-title">{mission.title}</div>
              <div className="quest-detail">{mission.detail}</div>
            </div>
            <div className="quest-meta">
              <span className={`status-pill ${mission.tone}`}>{mission.tone}</span>
              <div className="quest-reward">{mission.reward}</div>
              <button className="primary-btn small" onClick={() => handleClaim(mission.id)}>
                {claimed.includes(mission.id) ? <CheckCircle2 size={14} /> : <Coins size={14} />} 
                {claimed.includes(mission.id) ? 'Claimed' : 'Claim'}
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="card" style={{ display: 'grid', gap: 12 }}>
        <div className="stat-row">
          <div className="mini-stat">
            <Sparkles size={16} />
            <div>
              <div className="mini-label">Streak</div>
              <div className="mini-value">5 days</div>
            </div>
          </div>
          <div className="mini-stat">
            <TimerReset size={16} />
            <div>
              <div className="mini-label">Reset</div>
              <div className="mini-value">12h</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
