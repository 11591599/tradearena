import { useState, useEffect } from 'react'
import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
})

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export function useAuth() {
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const tg = (window as any).Telegram?.WebApp
    if (tg) {
      tg.ready()
      tg.expand()
      const initData = tg.initData
      if (initData) {
        API.post('/auth/login', { init_data: initData })
          .then(({ data }) => {
            localStorage.setItem('token', data.access_token)
            setUser(data.user)
          })
          .catch(console.error)
      }
    }
  }, [])

  return { user }
}

export function usePrices(symbols: string[] = ['BTC-USDT', 'ETH-USDT', 'SOL-USDT']) {
  const [prices, setPrices] = useState<Record<string, number>>({})

  useEffect(() => {
    const fetch = () => {
      API.get('/trading/prices', { params: { symbols: symbols.join(',') } })
        .then(({ data }) => setPrices(data.prices || {}))
        .catch(() => {})
    }
    fetch()
    const interval = setInterval(fetch, 10000)
    return () => clearInterval(interval)
  }, [symbols.join(',')])

  return { prices }
}

export default API