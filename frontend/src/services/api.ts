import { useState, useEffect } from 'react'
import axios from 'axios'

type ArenaUser = {
  id: number
  telegram_id: number
  username?: string
  first_name?: string
  balance: number
  balance_usd: number
  total_pnl: number
  wins: number
  losses: number
  credits: number
  tickets: number
  xp: number
  level: number
  is_premium: boolean
  referral_code?: string
}

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

export function useAuth() {
  const [user, setUser] = useState<ArenaUser | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    const telegram = window.Telegram?.WebApp
    if (!telegram?.initData) {
      setError('Open TradeArena using the bot in Telegram to sign in securely.')
      setLoading(false)
      return
    }

    telegram.ready()
    telegram.expand()
    API.post('/auth/login', { init_data: telegram.initData })
      .then(({ data }) => {
        if (cancelled) return
        const authenticatedUser: ArenaUser = {
          ...data,
          balance_usd: data.balance,
        }
        localStorage.setItem('user_id', String(data.id))
        setUser(authenticatedUser)
      })
      .catch(() => {
        if (!cancelled) setError('Telegram sign-in failed. Close the app and reopen it from the bot.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => { cancelled = true }
  }, [])

  return { user, loading, error }
}

export function usePrices(symbols: string[] = ['BTC-USDT', 'ETH-USDT', 'SOL-USDT']) {
  const [prices, setPrices] = useState<Record<string, number>>({})

  useEffect(() => {
    let cancelled = false
    const fetchPrices = () => {
      API.get('/prices', { params: { symbols: symbols.join(',') } })
        .then(({ data }) => { if (!cancelled) setPrices(data.prices || {}) })
        .catch(() => {})
    }
    fetchPrices()
    const interval = window.setInterval(fetchPrices, 10000)
    return () => {
      cancelled = true
      window.clearInterval(interval)
    }
  }, [symbols.join(',')])

  return { prices }
}

export default API
