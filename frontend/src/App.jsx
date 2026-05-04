import React, { useState, useEffect, useCallback } from 'react'
import WebApp from '@twa-dev/sdk'
import Dashboard from './components/Dashboard'
import TradePanel from './components/TradePanel'
import Leaderboard from './components/Leaderboard'
import Portfolio from './components/Portfolio'
import Premium from './components/Premium'
import api from './api'

const TABS = ['Trade', 'Portfolio', 'Leaderboard', 'Premium']

export default function App() {
  const [user, setUser] = useState(null)
  const [tab, setTab] = useState(0)
  const [loading, setLoading] = useState(true)
  const [gameStatus, setGameStatus] = useState(null)

  const init = useCallback(async () => {
    try {
      WebApp.ready()
      WebApp.expand()

      const initData = WebApp.initData
      if (!initData) {
        // Dev mode
        setUser({ id: 1, telegram_id: 6010708429, username: 'dev', balance: 10000, is_premium: false, referral_code: 'dev123' })
        setLoading(false)
        return
      }

      const res = await api.post('/auth/login', { init_data: initData })
      setUser(res.data)
    } catch (e) {
      console.error('Auth failed:', e)
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchStatus = useCallback(async () => {
    try {
      const res = await api.get('/game/status')
      setGameStatus(res.data)
    } catch (e) {
      console.error('Status fetch failed:', e)
    }
  }, [])

  useEffect(() => { init() }, [init])
  useEffect(() => {
    if (user) {
      fetchStatus()
      const interval = setInterval(fetchStatus, 10000)
      return () => clearInterval(interval)
    }
  }, [user, fetchStatus])

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
      </div>
    )
  }

  if (!user) {
    return (
      <div className="container" style={{ textAlign: 'center', paddingTop: '40vh' }}>
        <h2>Authentication Failed</h2>
        <p style={{ color: 'var(--text-secondary)', marginTop: 8 }}>Please open via Telegram bot</p>
      </div>
    )
  }

  return (
    <div className="container">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 800 }}>🏆 TradeArena</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: 13 }}>
            {gameStatus?.status === 'active' ? '🔴 Round Active' : '⏳ Next round soon'}
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: 18, fontWeight: 700 }}>${user.balance.toLocaleString()}</div>
          <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
            {user.is_premium && <span className="badge badge-premium">PRO</span>}
            {user.username || `Player ${user.telegram_id}`}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tab-bar">
        {TABS.map((t, i) => (
          <div
            key={t}
            className={`tab ${tab === i ? 'active' : ''}`}
            onClick={() => setTab(i)}
          >
            {t}
          </div>
        ))}
      </div>

      {/* Content */}
      {tab === 0 && <TradePanel user={user} setUser={setUser} gameStatus={gameStatus} />}
      {tab === 1 && <Portfolio user={user} />}
      {tab === 2 && <Leaderboard />}
      {tab === 3 && <Premium user={user} setUser={setUser} />}
    </div>
  )
}