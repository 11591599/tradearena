import React, { useState } from 'react'
import WebApp from '@twa-dev/sdk'
import api from '../api'

const FEATURES = [
  { icon: '📊', title: 'Extended Charts', desc: '1m, 5m, 15m timeframes' },
  { icon: '⚡', title: 'Priority Matching', desc: 'Faster trade execution' },
  { icon: '🎯', title: '5x Boosts Daily', desc: 'Double your profits' },
  { icon: '🏆', title: 'Premium Badge', desc: 'Stand out on leaderboard' },
  { icon: '📈', title: 'More Pairs', desc: 'Trade 20+ pairs' },
  { icon: '🛡', title: 'Risk Manager', desc: 'Auto stop-loss & take-profit' },
]

const BOOSTS = [
  { type: 'x2_profit', name: 'x2 Profit', price: '0.1 TON', desc: 'Double profits for 5 minutes' },
  { type: 'extra_time', name: '+15 min', price: '0.15 TON', desc: 'Extra time for your round' },
]

export default function Premium({ user, setUser }) {
  const [loading, setLoading] = useState(false)

  const buyPremium = async () => {
    setLoading(true)
    try {
      // Open TON payment via Telegram
      WebApp.openInvoice({
        slug: 'tradearena_premium',
      }, async (status) => {
        if (status === 'paid') {
          await api.post('/payments/premium', { tx_hash: 'stars_payment' })
          setUser(prev => ({ ...prev, is_premium: true }))
        }
        setLoading(false)
      })
    } catch (e) {
      console.error('Premium purchase error:', e)
      setLoading(false)
    }
  }

  return (
    <div>
      {/* Premium card */}
      {!user.is_premium ? (
        <div className="card" style={{ textAlign: 'center', background: 'linear-gradient(135deg, #1a1a2e 0%, #2d1b69 100%)' }}>
          <div style={{ fontSize: 40, marginBottom: 8 }}>💎</div>
          <h2 style={{ marginBottom: 4 }}>TradeArena Premium</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 16 }}>
            Unlock the full potential
          </p>
          <div style={{ fontSize: 28, fontWeight: 800, marginBottom: 16 }}>
            0.5 TON
            <span style={{ fontSize: 14, color: 'var(--text-secondary)', marginLeft: 8 }}>/ lifetime</span>
          </div>
          <button
            className="btn btn-primary"
            onClick={buyPremium}
            disabled={loading}
          >
            {loading ? 'Processing...' : '💎 Get Premium'}
          </button>
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', background: 'linear-gradient(135deg, #1a1a2e 0%, #2d1b69 100%)' }}>
          <div style={{ fontSize: 40, marginBottom: 8 }}>💎</div>
          <h2 style={{ marginBottom: 4 }}>Premium Active</h2>
          <p style={{ color: 'var(--green)' }}>✓ All features unlocked</p>
        </div>
      )}

      {/* Features list */}
      <div className="card">
        <h3 style={{ marginBottom: 12, fontSize: 16 }}>Features</h3>
        {FEATURES.map((f, i) => (
          <div key={i} style={{
            display: 'flex',
            alignItems: 'center',
            padding: '8px 0',
            borderBottom: '1px solid var(--border)'
          }}>
            <span style={{ fontSize: 24, marginRight: 12 }}>{f.icon}</span>
            <div>
              <div style={{ fontWeight: 600, fontSize: 14 }}>{f.title}</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{f.desc}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Boosts */}
      <div className="card">
        <h3 style={{ marginBottom: 12, fontSize: 16 }}>⚡ Boosts</h3>
        {BOOSTS.map((b, i) => (
          <div key={i} style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '12px 0',
            borderBottom: '1px solid var(--border)'
          }}>
            <div>
              <div style={{ fontWeight: 600 }}>{b.name}</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{b.desc}</div>
            </div>
            <button className="btn btn-outline" style={{ width: 'auto', padding: '8px 16px', fontSize: 13 }}>
              {b.price}
            </button>
          </div>
        ))}
      </div>

      {/* Referral */}
      <div className="card" style={{ textAlign: 'center' }}>
        <h3 style={{ marginBottom: 8, fontSize: 16 }}>🎁 Invite Friends</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: 13, marginBottom: 12 }}>
          Both get +20% to starting balance!
        </p>
        <div style={{
          background: 'var(--bg-secondary)',
          padding: '8px 12px',
          borderRadius: 8,
          fontFamily: 'monospace',
          fontSize: 14,
          wordBreak: 'break-all',
        }}>
          {user.referral_code || '—'}
        </div>
      </div>
    </div>
  )
}