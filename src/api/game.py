"""Game endpoints — rounds, trades, portfolio."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_session
from src.models import User, Round, Trade
from src.game.engine import engine
from loguru import logger

router = APIRouter()


class TradeRequest(BaseModel):
    symbol: str = "BTC-USDT"
    side: str  # buy, sell
    amount: float  # in USDT


class JoinRequest(BaseModel):
    referral_code: str | None = None


@router.get("/status")
async def game_status():
    """Current game status and active round."""
    round_info = await engine.get_active_round()
    return {
        "status": "active" if round_info else "waiting",
        "round": round_info,
        "next_round_in": await engine.next_round_countdown(),
    }


@router.post("/join")
async def join_round(
    req: JoinRequest,
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Join the current/next round."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Handle referral bonus
    if req.referral_code and not user.referred_by:
        referrer = await session.execute(
            select(User).where(User.referral_code == req.referral_code)
        )
        ref = referrer.scalar_one_or_none()
        if ref:
            user.referred_by = ref.telegram_id
            bonus = user.starting_balance * 0.2
            user.balance += bonus
            ref.balance += bonus
            logger.info(f"Referral: {ref.telegram_id} referred {user.telegram_id}, +{bonus}")

    round_info = await engine.join_round(user)
    await session.commit()
    return round_info


@router.post("/trade")
async def place_trade(
    req: TradeRequest,
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Place a trade in the current round."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if req.amount <= 0:
        raise HTTPException(400, "Amount must be positive")
    if req.amount > user.balance:
        raise HTTPException(400, "Insufficient balance")
    if req.side not in ("buy", "sell"):
        raise HTTPException(400, "Side must be buy or sell")

    result = await engine.place_trade(
        user=user,
        symbol=req.symbol,
        side=req.side,
        amount=req.amount,
        session=session,
    )
    return result


@router.get("/portfolio")
async def get_portfolio(user_id: int, session: AsyncSession = Depends(get_session)):
    """Get user's current portfolio."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    portfolio = await engine.get_portfolio(user.id, session)
    return {
        "balance": user.balance,
        "starting_balance": user.starting_balance,
        "pnl": user.balance - user.starting_balance,
        "pnl_percent": ((user.balance - user.starting_balance) / user.starting_balance) * 100,
        "positions": portfolio,
    }