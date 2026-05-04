"""TradeArena — Telegram Mini App for crypto trading battles."""
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from src.database import init_db
from src.api import router as api_router
from src.bot import setup_bot
from src.game.engine import TradingEngine


engine = TradingEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("🚀 TradeArena starting...")
    await init_db()
    await engine.start()
    bot_app = await setup_bot()
    yield
    await engine.stop()
    if bot_app:
        await bot_app.shutdown()
    logger.info("👋 TradeArena stopped.")


app = FastAPI(
    title="TradeArena",
    description="Telegram Mini App for crypto trading battles",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# Serve frontend
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)