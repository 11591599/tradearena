"""Real-time crypto price endpoints."""
import os
from fastapi import APIRouter
from src.game.engine import engine

router = APIRouter()


@router.get("/{symbol}")
async def get_price(symbol: str = "BTC-USDT"):
    """Get current price for a symbol."""
    price = await engine.get_price(symbol)
    return {"symbol": symbol, "price": price}


@router.get("/")
async def get_all_prices():
    """Get prices for all trading pairs."""
    symbols = os.getenv("SYMBOLS", "BTC-USDT,ETH-USDT,SOL-USDT").split(",")
    prices = {}
    for sym in symbols:
        prices[sym] = await engine.get_price(sym)
    return prices