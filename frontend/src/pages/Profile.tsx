import { useAuth } from '../services/api'
import { Crown, TrendingUp, TrendingDown, Zap } from 'lucide-react'

export default function Profile() {
  const { user } = useAuth()

  const stats = [
    { label: 'Total P&L', value: `$${user?.total_pnl?.toFixed(2) || '0.00'}`, icon: user?.total_pnl >= 0 ? TrendingUp : TrendingDown, color: user?.total_pnl >= 0 ? 'var(--green)' : 'var(--red)' },
    { label: 'Wins', value: user?.wins || 0, icon: Crown, color: '#f9d423' },
    { label: 'Losses', value: user?.losses || 0, icon: TrendingDown, color: 'var(--red)' },
  ]

  return (
    <div className="animate-slide-up">
      <div className="header">
        <div className="header-logo">👤 Profile</div>
      </div>

      {/* Avatar */}
      <div style={{ textAlign: 'center', padding: '24px 0' }}>
        <div className="avatar" style={{ width: 72, height: 72, fontSize: 28, margin: '0 auto 12px' }}>
          {user?.username?.[0]?.toUpperCase() || '?'}
        </div>
        <div style={{ fontSize: 20, fontWeight: 700 }}>{user?.username || 'Trader'}</div>
        <div style={{ color: 'var(--text-secondary)', fontSize: 14, marginTop: 4 }}>
          Balance: ${user?.balance_usd?.toLocaleString() || '10,000'}
        </div>
        {user?.is_premium && <span className="badge premium" style={{ marginTop: 8 }}><Crown size={12} /> PREMIUM</span>}
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12 }}>
        {stats.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="card" style={{ textAlign: 'center', padding: 16 }}>
            <Icon size={20} style={{ color, marginBottom: 8 }} />
            <div style={{ fontSize: 18, fontWeight: 700 }}>{value}</div>
            <div style={{ fontSize: 11, color: 'var(--text-secondary)', marginTop: 4 }}>{label}</div>
          </div>
        ))}
      </div>

      {/* Premium */}
      {!user?.is_premium && (
        <div className="round-card" style={{ marginTop: 16, textAlign: 'center' }}>
          <Crown size={32} style={{ color: '#f9d423', marginBottom: 8 }} />
          <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 4 }}>Upgrade to Premium</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 16 }}>
            More rounds, advanced tools, x2 profits
          </div>
          <button className="btn-buy" style={{ width: '100%' }}>
            <Zap size={16} style={{ display: 'inline', verticalAlign: 'middle' }} /> Pay 2 TON
          </button>
        </div>
      )}
    </div>
  )
}