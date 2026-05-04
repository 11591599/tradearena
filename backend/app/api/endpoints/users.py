"""User endpoints."""
from fastapi import APIRouter, Depends, Header
from jose import jwt, JWTError
from app.core.config import settings
from app.core.database import async_session
from app.models.user import User
from sqlalchemy import select

router = APIRouter()


async def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("user_id"))
    except (JWTError, ValueError):
        from fastapi import HTTPException
        raise HTTPException(401, "Invalid token")
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {"id": user.id, "telegram_id": user.telegram_id, "username": user.username, "balance_usd": user.balance_usd, "total_pnl": user.total_pnl, "wins": user.wins, "losses": user.losses, "is_premium": user.is_premium}


@router.get("/profile/{user_id}")
async def get_profile(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(404, "User not found")
    return {"id": user.id, "username": user.username, "total_pnl": user.total_pnl, "wins": user.wins, "losses": user.losses}
