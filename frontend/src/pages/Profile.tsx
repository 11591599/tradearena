import { useState } from 'react'

const defaultStats = {
  balance: 10000,
  credits: 150,
  tickets: 5,
  level: 12,
  xp: 870,
}

export default function Profile() {
  const [user] = useState(defaultStats)

  return (
    <div className="animate-slide-up">
      <div className="header">
        <div className="header-logo">👤 Profile</div>
      </div>

      <div className="card profile-hero">
        <div className="avatar big">A</div>
        <div>
          <div className="profile-name">Arena Agent</div>
          <div className="profile-subtitle">Level {user.level} • {user.xp} XP</div>
        </div>
      </div>

      <div className="stat-grid">
        <div className="stat-card">
          <div className="mini-label">Balance</div>
          <div className="mini-value">${user.balance.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <div className="mini-label">Credits</div>
          <div className="mini-value">{user.credits}</div>
        </div>
        <div className="stat-card">
          <div className="mini-label">Tickets</div>
          <div className="mini-value">{user.tickets}</div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Progress</div>
        <div className="xp-bar">
          <span style={{ width: '72%' }} />
        </div>
        <div className="progress-label">72% to next level</div>
      </div>
    </div>
  )
}
