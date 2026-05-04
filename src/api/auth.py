"""Telegram authentication endpoints."""
import hmac
import hashlib
import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.models import User
from sqlalchemy import select
from loguru import logger

router = APIRouter()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


class AuthRequest(BaseModel):
    init_data: str


def verify_telegram_auth(init_data: str) -> dict | None:
    """Verify Telegram WebApp init_data."""
    try:
        vals = {k: v for k, v in [x.split("=", 1) for x in init_data.split("&")]}
        hash_val = vals.pop("hash", "")
        check_string = "\n".join(f"{k}={v}" for k, v in sorted(vals.items()))
        secret_key = hmac.new(
            b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256
        ).digest()
        computed = hmac.new(
            secret_key, check_string.encode(), hashlib.sha256
        ).hexdigest()
        if computed == hash_val:
            import json
            vals["user"] = json.loads(vals.get("user", "{}"))
            return vals
    except Exception as e:
        logger.error(f"Auth verification error: {e}")
    return None


@router.post("/login")
async def login(req: AuthRequest, session: AsyncSession = Depends(get_session)):
    """Authenticate user via Telegram WebApp."""
    data = verify_telegram_auth(req.init_data)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid auth data")

    user_data = data.get("user", {})
    tg_id = user_data.get("id")
    username = user_data.get("username")
    first_name = user_data.get("first_name", "")

    result = await session.execute(select(User).where(User.telegram_id == tg_id))
    user = result.scalar_one_or_none()

    if not user:
        import secrets
        user = User(
            telegram_id=tg_id,
            username=username,
            first_name=first_name,
            balance=10000.0,
            starting_balance=10000.0,
            referral_code=secrets.token_urlsafe(8),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        logger.info(f"New user: {tg_id} ({username})")
    else:
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        await session.commit()

    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "balance": user.balance,
        "is_premium": user.is_premium,
        "referral_code": user.referral_code,
    }