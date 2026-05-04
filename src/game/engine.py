"""Trading engine — rounds, prices, trades."""
import asyncio
from datetime import datetime, timezone, timedelta
from loguru import logger
import httpx
import os
from src.models import Round, Trade, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class TradingEngine:
    """Core game engine managing rounds and prices."""

    SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT"]
    ROUND_DURATION = int(os.getenv("ROUND_DURATION_MINUTES", "60"))
    STARTING_BALANCE = float(os.getenv("STARTING_BALANCE", "10000"))

    def __init__(self):
        self.prices = {sym: 0.0 for sym in self.SYMBOLS}
        self.active_round = None
        self._task = None
        self._price_task = None

    async def start(self):
        """Start the engine."""
        self._price_task = asyncio.create_task(self._update_prices_loop())
        self._task = asyncio.create_task(self._round_loop())
        logger.info("Trading engine started")

    async def stop(self):
        """Stop the engine."""
        if self._task:
            self._task.cancel()
        if self._price_task:
            self._price_task.cancel()
        logger.info("Trading engine stopped")

    async def _update_prices_loop(self):
        """Fetch prices every 10 seconds."""
        while True:
            try:
                async with httpx.AsyncClient() as client:
                    for sym in self.SYMBOLS:
                        try:
                            resp = await client.get(
                                f"https://api.exchange.coinbase.com/products/{sym}/ticker"
                            )
                            if resp.status_code == 200:
                                data = resp.json()
                                self.prices[sym] = float(data.get("price", 0))
                        except Exception as e:
                            logger.warning(f"Price fetch error for {sym}: {e}")
            except Exception as e:
                logger.error(f"Price update error: {e}")
            await asyncio.sleep(10)

    async def _round_loop(self):
        """Manage round lifecycle."""
        while True:
            try:
                await self._start_new_round()
                await asyncio.sleep(self.ROUND_DURATION * 60)
                await self._end_round()
                await asyncio.sleep(30)  # 30s break between rounds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Round error: {e}")
                await asyncio.sleep(60)

    async def _start_new_round(self):
        """Start a new trading round."""
        from src.database import async_session
        async with async_session() as session:
            new_round = Round(
                status="active",
                started_at=datetime.now(timezone.utc),
                start_price=self.prices.get("BTC-USDT", 0),
            )
            session.add(new_round)
            await session.commit()
            self.active_round = new_round.id
            logger.info(f"Round {new_round.id} started")

    async def _end_round(self):
        """End current round and calculate results."""
        from src.database import async_session
        async with async_session() as session:
            result = await session.execute(
                select(Round).where(Round.id == self.active_round)
            )
            round_obj = result.scalar_one_or_none()
            if round_obj:
                round_obj.status = "finished"
                round_obj.ended_at = datetime.now(timezone.utc)
                round_obj.end_price = self.prices.get("BTC-USDT", 0)
                await session.commit()
                self.active_round = None
                logger.info(f"Round {round_obj.id} finished")

    async def get_active_round(self) -> dict | None:
        """Get info about the active round."""
        if not self.active_round:
            return None
        return {
            "round_id": self.active_round,
            "status": "active",
            "prices": self.prices,
            "time_remaining": self.ROUND_DURATION * 60,
        }

    async def next_round_countdown(self) -> int:
        """Seconds until next round."""
        if self.active_round:
            return 0
        return 30

    async def get_price(self, symbol: str) -> float:
        """Get current price."""
        return self.prices.get(symbol, 0.0)

    async def join_round(self, user: User) -> dict:
        """Join the current round."""
        return {
            "round_id": self.active_round,
            "balance": user.balance,
            "prices": self.prices,
        }

    async def place_trade(
        self, user: User, symbol: str, side: str, amount: float, session: AsyncSession
    ) -> dict:
        """Execute a trade."""
        price = self.prices.get(symbol, 0)
        if price == 0:
            return {"error": "Price not available"}

        if side == "buy":
            user.balance -= amount
        else:
            user.balance += amount

        trade = Trade(
            user_id=user.id,
            round_id=self.active_round,
            symbol=symbol,
            side=side,
            amount=amount,
            price=price,
        )
        session.add(trade)
        await session.commit()

        return {
            "trade_id": trade.id,
            "symbol": symbol,
            "side": side,
            "amount": amount,
            "price": price,
            "balance": user.balance,
        }

    async def get_portfolio(self, user_id: int, session: AsyncSession) -> list:
        """Get user's positions."""
        result = await session.execute(
            select(Trade).where(
                Trade.user_id == user_id,
                Trade.round_id == self.active_round,
            )
        )
        trades = result.scalars().all()
        positions = {}
        for t in trades:
            sym = t.symbol
            if sym not in positions:
                positions[sym] = {"qty": 0, "avg_price": 0, "total": 0}
            if t.side == "buy":
                positions[sym]["qty"] += t.amount / t.price
                positions[sym]["total"] += t.amount
            else:
                positions[sym]["qty"] -= t.amount / t.price
                positions[sym]["total"] -= t.amount
        return [
            {"symbol": s, "quantity": round(p["qty"], 6), "value": round(p["total"], 2)}
            for s, p in positions.items()
        ]