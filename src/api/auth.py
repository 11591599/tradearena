"""Telegram Web App authentication endpoints."""
import hashlib
import hmac
import json
import os
import time
from urllib.parse import parse_qsl

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.database import get_session
from src.models import User

router = APIRouter()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
AUTH_MAX_AGE_SECONDS = int(os.getenv("TELEGRAM_AUTH_MAX_AGE_SECONDS", "86400"))


class AuthRequest(BaseModel):
    init_data: str = Field(min_length=1, max_length=8192)


def verify_telegram_auth(init_data: str) -> dict | None:
    """Verify Telegram initData signature and reject expired/replayed payloads."""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not configured; refusing Telegram authentication.")
        return None
    try:
        pairs = parse_qsl(init_data, keep_blank_values=True, strict_parsing=True)
        values = dict(pairs)
        if len(values) != len(pairs):
            return None
        received_hash = values.pop("hash", "")
        auth_date = int(values.get("auth_date", "0"))
        now = int(time.time())
        if not received_hash or auth_date > now + 30 or now - auth_date > AUTH_MAX_AGE_SECONDS:
            return None

        check_string = "\n".join(f"{key}={value}" for key, value in sorted(values.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        expected_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_hash, received_hash):
            return None

        user_data = json.loads(values.get("user", "{}"))
        if not isinstance(user_data, dict) or not isinstance(user_data.get("id"), int):
            return None
        values["user"] = user_data
        return values
    except (ValueError, TypeError, json.JSONDecodeError):
        return None
    except Exception:
        logger.exception("Unexpected Telegram authentication verification error")
        return None


@router.post("/login")
async def login(req: AuthRequest, session: AsyncSession = Depends(get_session)):
    """Authenticate a Telegram Mini App request and return the player's profile."""
    data = verify_telegram_auth(req.init_data)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired Telegram authentication data")

    user_data = data["user"]
    tg_id = user_data["id"]
    result = await session.execute(select(User).where(User.telegram_id == tg_id))
    user = result.scalar_one_or_none()

    if not user:
        import secrets
        user = User(
            telegram_id=tg_id,
            username=user_data.get("username"),
            first_name=user_data.get("first_name", ""),
            balance=10000.0,
            starting_balance=10000.0,
            referral_code=secrets.token_urlsafe(8),
        )
        session.add(user)
    else:
        user.username = user_data.get("username") or user.username
        user.first_name = user_data.get("first_name") or user.first_name

    await session.commit()
    await session.refresh(user)
    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "balance": user.balance,
        "total_pnl": user.total_pnl,
        "wins": user.wins,
        "losses": user.losses,
        "credits": user.credits,
        "tickets": user.tickets,
        "xp": user.xp,
        "level": user.level,
        "is_premium": user.is_premium,
        "referral_code": user.referral_code,
    }
