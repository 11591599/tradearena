"""Round endpoints."""
from fastapi import APIRouter, Depends
from app.core.database import async_session
from app.models.round import Round
from app.models.user import User
from app.api.endpoints.users import get_current_user
from sqlalchemy import select

router = APIRouter()


@router.get("/active")
async def get_active_round():
    async with async_session() as session:
        result = await session.execute(select(Round).where(Round.status == "active"))
        round_ = result.scalar_one_or_none()
    if not round_:
        return {"round": None, "message": "No active round"}
    return {"round": {"id": round_.id, "status": round_.status, "start_time": str(round_.start_time), "end_time": str(round_.end_time), "prize_pool": round_.prize_pool_ton, "participants": round_.participants_count}}


@router.get("/history")
async def get_rounds_history(limit: int = 20):
    async with async_session() as session:
        result = await session.execute(select(Round).where(Round.status == "finished").order_by(Round.id.desc()).limit(limit))
        rounds = result.scalars().all()
    return {"rounds": [{"id": r.id, "start_time": str(r.start_time), "end_time": str(r.end_time), "prize_pool": r.prize_pool_ton, "participants": r.participants_count} for r in rounds]}
