import React, { useState, useEffect } from 'react'
import api from '../api'
import Dashboard from './Dashboard'

const SYMBOLS = ['BTC-USDT', 'ETH-USDT', 'SOL-USDT']

export default function TradePanel({ user, setUser, gameStatus }) {
  const [symbol, setSymbol] = useState('BTC-USDT')
  const [side, setSide] = useState('buy')
  const [amount, setAmount] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const handleTrade = async () => {
    if (!amount || parseFloat(amount) <= 0) return
    setLoading(true)
    setMessage(null)
    try {
      const res = await api.post('/game/trade', {
        symbol,
        side,
        amount: parseFloat(amount),
      })
      if (res.data.error) {
        setMessage({ type: 'error', text: res.data.error })
      } else {
        setUser(prev => ({ ...prev, balance: res.data.balance }))
        setMessage({ type: 'success', text: `${side === 'buy' ? '🟢 Bought' : '🔴 Sold'} ${amount} USDT of ${symbol}` })
        setAmount('')
      }
    } catch (e) {
      setMessage({ type: 'error', text: 'Trade failed' })
    } finally {
      setLoading(false)
    }
  }

  const quickAmounts = [100, 500, 1000, 5000]

  return (
    <div>
      <Dashboard gameStatus={gameStatus} />

      {/* Symbol selector */}
      <div className="card">
        <h3 style={{ marginBottom: 12, fontSize: 16 }}>Select Pair</h3>
        <div style={{ display: 'flex', gap: 8 }}>
          {SYMBOLS.map(s => (
            <button
              key={s}
              className={`btn ${symbol === s ? 'btn-primary' : 'btn-outline'}`}
              style={{ flex: 1, padding: '8px 4px', fontSize: 13 }}
              onClick={() => setSymbol(s)}
            >
              {s.replace('-USDT', '')}
            </button>
          ))}
        </div>
      </div>

      {/* Buy/Sell toggle */}
      <div className="card">
        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <button
            className={`btn ${side === 'buy' ? 'btn-buy' : 'btn-outline'}`}
            style={{ flex: 1 }}
            onClick={() => setSide('buy')}
          >
            🟢 Buy
          </button>
          <button
            className={`btn ${side === 'sell' ? 'btn-sell' : 'btn-outline'}`}
            style={{ flex: 1 }}
            onClick={() => setSide('sell')}
          >
            🔴 Sell
          </button>
        </div>

        {/* Amount input */}
        <input
          type="number"
          placeholder="Amount in USDT"
          value={amount}
          onChange={e => setAmount(e.target.value)}
          style={{ marginBottom: 12 }}
        />

        {/* Quick amounts */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          {quickAmounts.map(a => (
            <button
              key={a}
              className="btn btn-outline"
              style={{ flex: 1, padding: '6px 4px', fontSize: 12 }}
              onClick={() => setAmount(String(a))}
            >
              ${a}
            </button>
          ))}
        </div>

        {/* Trade button */}
        <button
          className={`btn ${side === 'buy' ? 'btn-buy' : 'btn-sell'}`}
          onClick={handleTrade}
          disabled={loading || !amount}
        >
          {loading ? 'Processing...' : `${side === 'buy' ? '🟢' : '🔴'} ${side.toUpperCase()} ${symbol.replace('-USDT', '')}`}
        </button>

        {/* Message */}
        {message && (
          <div style={{
            marginTop: 12,
            padding: '8px 12px',
            borderRadius: 8,
            background: message.type === 'success' ? 'rgba(0,210,160,0.15)' : 'rgba(255,107,107,0.15)',
            color: message.type === 'success' ? 'var(--green)' : 'var(--red)',
            fontSize: 14,
          }}>
            {message.text}
          </div>
        )}
      </div>
    </div>
  )
}