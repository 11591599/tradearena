"""Market data service — real-time crypto prices."""
import aiohttp
from loguru import logger


async def get_price(symbol: str = "BTC-USDT") -> float | None:
    """Get current price from Coinbase."""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.exchange.coinbase.com/products/{symbol}/ticker"
            async with session.get(url) as resp:
                data = await resp.json()
                return float(data.get("price", 0))
    except Exception as e:
        logger.error(f"Price fetch error: {e}")
        return None


async def get_prices(symbols: list[str] = None) -> dict:
    """Get multiple prices."""
    if symbols is None:
        symbols = ["BTC-USDT", "ETH-USDT", "SOL-USDT"]
    result = {}
    for symbol in symbols:
        price = await get_price(symbol)
        if price:
            result[symbol] = price
    return result


async def get_candles(symbol: str = "BTC-USDT", granularity: int = 3600) -> list:
    """Get candlestick data."""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.exchange.coinbase.com/products/{symbol}/candles?granularity={granularity}"
            async with session.get(url) as resp:
                return await resp.json()
    except Exception as e:
        logger.error(f"Candles fetch error: {e}")
        return []
