"""Auth endpoints — Telegram WebApp login."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import verify_telegram_webapp, create_access_token
from app.core.database import async_session
from app.models.user import User
from sqlalchemy import select

router = APIRouter()


class AuthRequest(BaseModel):
    init_data: str


@router.post("/login")
async def login(req: AuthRequest):
    """Login via Telegram WebApp init_data."""
    data = verify_telegram_webapp(req.init_data)
    if not data:
        raise HTTPException(401, "Invalid Telegram data")

    user_id = int(data.get("user", {}).get("id", 0))
    if not user_id:
        raise HTTPException(401, "User ID not found")

    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=user_id,
                username=data.get("user", {}).get("username"),
                first_name=data.get("user", {}).get("first_name"),
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

    token = create_access_token({"sub": str(user_id), "user_id": user.id})
    return {"access_token": token, "user": {"id": user.id, "telegram_id": user_id, "username": user.username, "balance_usd": user.balance_usd}}
