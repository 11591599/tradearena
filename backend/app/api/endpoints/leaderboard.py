"""Leaderboard endpoints."""
from fastapi import APIRouter
from app.core.database import async_session
from app.models.user import User
from sqlalchemy import select, desc

router = APIRouter()


@router.get("/global")
async def global_leaderboard(limit: int = 50):
    async with async_session() as session:
        result = await session.execute(select(User).order_by(desc(User.total_pnl)).limit(limit))
        users = result.scalars().all()
    return {"leaderboard": [{"rank": i + 1, "id": u.id, "username": u.username or f"Trader{u.id}", "pnl": u.total_pnl, "wins": u.wins} for i, u in enumerate(users)]}


@router.get("/round/{round_id}")
async def round_leaderboard(round_id: int, limit: int = 50):
    from app.models.trade import Trade
    from sqlalchemy import func
    async with async_session() as session:
        result = await session.execute(
            select(Trade.user_id, func.sum(Trade.pnl).label("total_pnl"))
            .where(Trade.round_id == round_id)
            .group_by(Trade.user_id)
            .order_by(desc("total_pnl"))
            .limit(limit)
        )
        rows = result.all()
    return {"leaderboard": [{"rank": i + 1, "user_id": r[0], "pnl": float(r[1] or 0)} for i, r in enumerate(rows)]}
