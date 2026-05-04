"""Leaderboard endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from src.database import get_session
from src.models import User

router = APIRouter()


@router.get("/global")
async def global_leaderboard(session: AsyncSession = Depends(get_session)):
    """Top players by total PnL."""
    result = await session.execute(
        select(User)
        .order_by(desc(User.total_pnl))
        .limit(50)
    )
    users = result.scalars().all()
    return [
        {
            "rank": i + 1,
            "username": u.username or f"Player {u.telegram_id}",
            "pnl": round(u.total_pnl, 2),
            "wins": u.wins,
            "is_premium": u.is_premium,
        }
        for i, u in enumerate(users)
    ]


@router.get("/round/{round_id}")
async def round_leaderboard(round_id: int, session: AsyncSession = Depends(get_session)):
    """Leaderboard for a specific round."""
    from src.models import Trade
    from sqlalchemy import func

    result = await session.execute(
        select(
            Trade.user_id,
            func.sum(Trade.pnl).label("total_pnl"),
        )
        .where(Trade.round_id == round_id)
        .group_by(Trade.user_id)
        .order_by(desc("total_pnl"))
    )
    rows = result.all()

    leaderboard = []
    for i, (uid, pnl) in enumerate(rows):
        user = await session.get(User, uid)
        leaderboard.append({
            "rank": i + 1,
            "username": user.username or f"Player {user.telegram_id}",
            "pnl": round(pnl, 2),
        })
    return leaderboard