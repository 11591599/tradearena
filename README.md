# 🏆 TradeArena

Telegram Mini App for crypto trading battles.

Compete in real-time trading rounds with virtual funds. Who earned more — wins.

## Features
- 🔐 Telegram authentication
- 💰 Virtual $10,000 starting balance
- 📊 Real-time BTC, ETH, SOL prices
- ⏱ 1-hour trading rounds
- 🏆 Leaderboard & rankings
- 💎 TON payments for premium features
- 🎯 Boosts & power-ups
- 👥 Referral system

## Quick Start

```bash
cp .env.example .env
# Edit .env with your values
docker-compose up -d
```

## Tech Stack
- **Backend**: FastAPI + SQLite + WebSocket
- **Frontend**: React + Telegram Web App SDK
- **Payments**: TON Connect
- **Deploy**: Docker Compose