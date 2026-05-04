import { useState } from 'react'
import { useAuth, usePrices } from '../services/api'
import { TrendingUp, ArrowUpRight, ArrowDownRight } from 'lucide-react'

const COINS = [
  { symbol: 'BTC-USDT', name: 'Bitcoin', short: 'BTC' },
  { symbol: 'ETH-USDT', name: 'Ethereum', short: 'ETH' },
  { symbol: 'SOL-USDT', name: 'Solana', short: 'SOL' },
]

export default function Trade() {
  const { user } = useAuth()
  const { prices } = usePrices()
  const [selected, setSelected] = useState(COINS[0])
  const [amount, setAmount] = useState('100')
  const [side, setSide] = useState<'buy' | 'sell'>('buy')

  const price = prices[selected.symbol]
  const changePercent = 2.34 // TODO: real data

  return (
    <div className="animate-slide-up">
      <div className="header">
        <div className="header-logo">🏆 TradeArena</div>
        <div className="header-balance">
          💵 ${user?.balance_usd?.toLocaleString() || '10,000'}
        </div>
      </div>

      {/* Coin Selector */}
      <div className="tabs">
        {COINS.map((coin) => (
          <button
            key={coin.symbol}
            className={`tab ${selected.symbol === coin.symbol ? 'active' : ''}`}
            onClick={() => setSelected(coin)}
          >
            {coin.short}
          </button>
        ))}
      </div>

      {/* Price Card */}
      <div className="price-card">
        <div className="price-symbol">{selected.name}</div>
        <div className="price-value">
          ${price ? price.toLocaleString(undefined, { minimumFractionDigits: 2 }) : '—'}
        </div>
        <div className={`price-change ${changePercent >= 0 ? 'positive' : 'negative'}`}>
          {changePercent >= 0 ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
          {Math.abs(changePercent)}%
        </div>
      </div>

      {/* Amount Input */}
      <div className="input-group">
        <label className="input-label">Amount (USD)</label>
        <input
          className="input"
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="Enter amount"
        />
      </div>

      {/* Quick Amounts */}
      <div style={{ display: 'flex', gap: 8, margin: '8px 0 16px' }}>
        {['50', '100', '500', '1000'].map((v) => (
          <button
            key={v}
            className="tab"
            style={{ flex: 1, fontSize: 12 }}
            onClick={() => setAmount(v)}
          >
            ${v}
          </button>
        ))}
      </div>

      {/* Trade Buttons */}
      <div className="trade-buttons">
        <button className="btn-buy" onClick={() => setSide('buy')}>
          📈 BUY
        </button>
        <button className="btn-sell" onClick={() => setSide('sell')}>
          📉 SELL
        </button>
      </div>

      {/* Positions */}
      <div className="card">
        <div className="card-title">Open Positions</div>
        <div style={{ color: 'var(--text-muted)', fontSize: 14, textAlign: 'center', padding: 20 }}>
          No open positions yet
        </div>
      </div>
    </div>
  )
}