"""Trading endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.database import async_session
from app.models.trade import Trade
from app.models.user import User
from app.api.endpoints.users import get_current_user
from app.services.market import get_price
from sqlalchemy import select

router = APIRouter()


class TradeRequest(BaseModel):
    symbol: str = "BTC-USDT"
    side: str  # buy or sell
    amount_usd: float


@router.post("/open")
async def open_trade(req: TradeRequest, user: User = Depends(get_current_user)):
    if req.side not in ("buy", "sell"):
        raise HTTPException(400, "Side must be buy or sell")
    if req.amount_usd <= 0:
        raise HTTPException(400, "Amount must be positive")
    if req.amount_usd > user.balance_usd:
        raise HTTPException(400, "Insufficient balance")

    price = await get_price(req.symbol)
    if not price:
        raise HTTPException(503, "Price unavailable")

    amount = req.amount_usd / price if req.side == "buy" else req.amount_usd

    trade = Trade(
        user_id=user.id,
        round_id=1,  # TODO: current active round
        symbol=req.symbol,
        side=req.side,
        amount=amount,
        price=price,
    )
    async with async_session() as session:
        session.add(trade)
        new_balance = user.balance_usd - req.amount_usd if req.side == "buy" else user.balance_usd + req.amount_usd
        await session.execute(select(User).where(User.id == user.id).values(balance_usd=new_balance))
        await session.commit()
        await session.refresh(trade)

    return {"trade": {"id": trade.id, "symbol": trade.symbol, "side": trade.side, "amount": trade.amount, "price": trade.price, "status": trade.status}}


@router.get("/positions")
async def get_positions(user: User = Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(select(Trade).where(Trade.user_id == user.id, Trade.status == "open"))
        trades = result.scalars().all()
    return {"positions": [{"id": t.id, "symbol": t.symbol, "side": t.side, "amount": t.amount, "price": t.price, "pnl": t.pnl} for t in trades]}
