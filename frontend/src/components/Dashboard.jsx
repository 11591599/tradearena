import React, { useState, useEffect } from 'react'
import api from '../api'

export default function Dashboard({ gameStatus }) {
  const [prices, setPrices] = useState({})

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const res = await api.get('/prices/')
        setPrices(res.data)
      } catch (e) {
        console.error('Price fetch error:', e)
      }
    }
    fetchPrices()
    const interval = setInterval(fetchPrices, 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="card">
      <h3 style={{ marginBottom: 12, fontSize: 16 }}>📊 Live Prices</h3>
      {Object.entries(prices).map(([symbol, price]) => (
        <div key={symbol} style={{
          display: 'flex',
          justifyContent: 'space-between',
          padding: '8px 0',
          borderBottom: '1px solid var(--border)'
        }}>
          <span style={{ fontWeight: 600 }}>{symbol.replace('-USDT', '/USDT')}</span>
          <span style={{ fontFamily: 'monospace', fontSize: 16 }}>
            ${typeof price === 'number' ? price.toLocaleString(undefined, { maximumFractionDigits: 2 }) : price}
          </span>
        </div>
      ))}
    </div>
  )
}