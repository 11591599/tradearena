"""TradeArena — Telegram Mini App backend."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.api.router import api_router
from app.ws.manager import ws_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & shutdown."""
    logger.info("🚀 TradeArena starting...")
    from app.core.database import engine
    from app.models.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database initialized")
    yield
    logger.info("👋 TradeArena shutting down...")
    await ws_manager.disconnect_all()


app = FastAPI(
    title="TradeArena",
    description="🏆 Telegram Mini App for crypto trading battles",
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

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "TradeArena"}
