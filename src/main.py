"""TradeArena — Telegram Mini App and game API."""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from src.api import router as api_router
from src.bot import setup_bot, stop_bot
from src.database import init_db
from src.game.engine import TradingEngine

engine = TradingEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting TradeArena...")
    await init_db()
    await engine.start()
    bot_app = None
    try:
        bot_app = await setup_bot()
        yield
    finally:
        await engine.stop()
        if bot_app:
            await stop_bot(bot_app)
        logger.info("TradeArena stopped.")


app = FastAPI(
    title="TradeArena",
    description="Telegram Mini App for virtual trading battles, missions and rewards",
    version="1.2.0",
    lifespan=lifespan,
)

# The Mini App is served from this same origin. Do not enable wildcard credentialed CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
app.include_router(api_router, prefix="/api")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "tradearena"}


app.mount("/", StaticFiles(directory="frontend/dist", html=True, check_dir=False), name="frontend")


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000)
