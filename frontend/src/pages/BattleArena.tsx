import { Swords, Crown, Ticket, Zap } from 'lucide-react'

const battleRooms = [
  { id: 1, name: 'Shadow Duel', prize: '250 credits', ticket: 1, cooldown: '10 min' },
  { id: 2, name: 'Vault Rush', prize: '500 credits', ticket: 2, cooldown: '30 min' },
  { id: 3, name: 'Legend Circuit', prize: '900 credits', ticket: 3, cooldown: '1 hour' },
]

export default function BattleArena() {
  return (
    <div className="animate-slide-up">
      <div className="header">
        <div className="header-logo">⚔️ Battles</div>
      </div>

      {battleRooms.map((battle) => (
        <div key={battle.id} className="battle-card">
          <div className="battle-header">
            <div>
              <div className="battle-name">{battle.name}</div>
              <div className="battle-meta">{battle.cooldown} cooldown</div>
            </div>
            <span className="status-pill open">open</span>
          </div>
          <div className="battle-stats">
            <span><Crown size={14} /> {battle.prize}</span>
            <span><Ticket size={14} /> {battle.ticket} ticket</span>
          </div>
          <button className="primary-btn full">Join battle</button>
        </div>
      ))}

      <div className="card">
        <div className="card-title">Battle momentum</div>
        <div className="stat-row">
          <div className="mini-stat">
            <Zap size={16} />
            <div>
              <div className="mini-label">Win rate</div>
              <div className="mini-value">62%</div>
            </div>
          </div>
          <div className="mini-stat">
            <Swords size={16} />
            <div>
              <div className="mini-label">Current rank</div>
              <div className="mini-value">#18</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
