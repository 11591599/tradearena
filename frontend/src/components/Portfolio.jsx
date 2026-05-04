import React, { useState, useEffect } from 'react'
import api from '../api'

export default function Portfolio({ user }) {
  const [portfolio, setPortfolio] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const res = await api.get('/game/portfolio')
        setPortfolio(res.data)
      } catch (e) {
        console.error('Portfolio fetch error:', e)
      } finally {
        setLoading(false)
      }
    }
    fetchPortfolio()
    const interval = setInterval(fetchPortfolio, 15000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="loading"><div className="spinner" /></div>
  }

  if (!portfolio) {
    return <div className="card"><p>Failed to load portfolio</p></div>
  }

  const pnlColor = portfolio.pnl >= 0 ? 'var(--green)' : 'var(--red)'
  const pnlSign = portfolio.pnl >= 0 ? '+' : ''

  return (
    <div>
      {/* Balance card */}
      <div className="card" style={{ textAlign: 'center' }}>
        <div style={{ color: 'var(--text-secondary)', fontSize: 13, marginBottom: 4 }}>Balance</div>
        <div style={{ fontSize: 32, fontWeight: 800, fontFamily: 'monospace' }}>
          ${portfolio.balance.toLocaleString(undefined, { maximumFractionDigits: 2 })}
        </div>
        <div style={{ fontSize: 18, fontWeight: 700, color: pnlColor, marginTop: 8 }}>
          {pnlSign}{portfolio.pnl.toLocaleString(undefined, { maximumFractionDigits: 2 })} USDT
          <span style={{ fontSize: 14, marginLeft: 8 }}>
            ({pnlSign}{portfolio.pnl_percent.toFixed(2)}%)
          </span>
        </div>
      </div>

      {/* Positions */}
      <div className="card">
        <h3 style={{ marginBottom: 12, fontSize: 16 }}>📊 Positions</h3>
        {portfolio.positions.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: 20 }}>
            No open positions. Start trading!
          </p>
        ) : (
          portfolio.positions.map((pos, i) => (
            <div key={i} style={{
              display: 'flex',
              justifyContent: 'space-between',
              padding: '8px 0',
              borderBottom: '1px solid var(--border)'
            }}>
              <div>
                <div style={{ fontWeight: 600 }}>{pos.symbol.replace('-USDT', '/USDT')}</div>
                <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
                  Qty: {pos.quantity}
                </div>
              </div>
              <div style={{ textAlign: 'right', fontFamily: 'monospace' }}>
                <div>${pos.value.toLocaleString()}</div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}