# 🏆 TradeArena

TradeArena is a Telegram bot and Telegram Mini App for virtual trading rounds, missions, rewards and player battles. The bot uses **long polling**, so you do not need a public webhook port or a webhook secret. The Mini App itself must be hosted at a public HTTPS URL.

## Start it reliably

### 1. Create a Telegram bot token

In Telegram, open the official **@BotFather**, create or select your bot, and copy its token. Treat the token like a password: never paste it into GitHub, source files, screenshots, or chat. If it has ever been exposed, revoke it with BotFather and use the replacement.

### 2. Deploy the app at HTTPS

Deploy this repository to a host with Docker and a public HTTPS domain, for example `https://arena.example.com`. Telegram Mini Apps require HTTPS. Make sure the domain serves the app and that the deployment is reachable before testing the bot.

### 3. Configure the server

On the server, from the repository directory:

```bash
cp .env.example .env
```

Edit `.env` on the server (not in GitHub) and set:

```dotenv
TELEGRAM_BOT_TOKEN=the_token_from_BotFather
WEBAPP_URL=https://your-real-domain.example
```

Use the exact HTTPS origin where this app is deployed. Do not include `/webhook`; this project uses long polling. No TON or exchange API key is required to start the bot.

### 4. Build and start

```bash
docker compose up -d --build
docker compose logs -f app
```

On successful startup, the logs should include `Telegram bot @... connected and polling.` The health endpoint is `https://your-real-domain.example/health` and should return `{"status":"ok","service":"tradearena"}`.

Open your bot in Telegram and send `/start`. The **Open TradeArena** button should open the HTTPS Mini App. Send `/help` or `/leaderboard` to check the bot commands. To stop it, use `docker compose down`.

## Common startup errors

- **TELEGRAM_BOT_TOKEN is required**: set the token in the server-side `.env`; do not commit it.
- **WEBAPP_URL must be HTTPS**: configure the deployed public HTTPS address, not `localhost` and not the API key.
- **Unauthorized / invalid token**: create or rotate the token with BotFather, update the server `.env`, then run `docker compose up -d --force-recreate`.
- **Mini App button opens an error**: confirm the domain is online over HTTPS and the bot's Web App URL matches it exactly.
- **Port 8000 is occupied**: change the left side of the `ports` mapping in `docker-compose.yml`, keeping the container side `8000`.

## Configuration and secrets

`.env.example` is only a template. The real `.env` is ignored by Git. The required secret is `TELEGRAM_BOT_TOKEN`; set it in the hosting provider's secret/environment settings or in a server-local `.env`. Never add it to a commit. TON payment settings are optional and should remain disabled until payment verification is implemented and tested for the intended production network.

## Stack

- **Bot/API:** Python, python-telegram-bot, FastAPI, SQLAlchemy async
- **Mini App:** React, TypeScript, Vite, Telegram Web App SDK
- **Local container database:** SQLite persisted under `./data`
- **Runtime:** Docker Compose
