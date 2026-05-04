# 🏆 TradeArena

**Telegram Mini App for crypto trading battles.**

Compete with other traders in real-time. Trade crypto on virtual accounts, climb the leaderboard, win prizes in TON.

## 🚀 Features

- ⚡ Real-time crypto trading with live prices
- 🏆 Hourly/daily trading battles
- 📊 Leaderboard among friends & global
- 💎 Premium boosts & tools
- 🔗 TON payments integration
- 📱 Telegram Mini App — no download needed

## 🏗 Architecture

```
tradearena/
├── backend/          # FastAPI + WebSocket server
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── ws/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # React + Telegram Web App SDK
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── styles/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## ⚡ Quick Start

```bash
cp .env.example .env
# Edit .env with your keys
docker-compose up -d
```

## 🔧 Environment Variables

See `.env.example` for all configuration options.

## 📄 License

MIT