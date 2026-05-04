"""TON payment endpoints."""
import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.models import User, Payment
from loguru import logger

router = APIRouter()
TONCENTER_URL = os.getenv("TONCENTER_API_URL", "https://api.toncenter.com/v1")
TON_WALLET = os.getenv("TON_WALLET_ADDRESS", "")


class PremiumRequest(BaseModel):
    tx_hash: str


class BoostRequest(BaseModel):
    boost_type: str  # x2_profit, extra_time
    tx_hash: str


PREMIUM_PRICE_TON = 0.5
BOOST_PRICES = {"x2_profit": 0.1, "extra_time": 0.15}


@router.post("/premium")
async def buy_premium(
    req: PremiumRequest,
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Activate premium via TON payment."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Verify transaction
    verified = await verify_ton_payment(req.tx_hash, PREMIUM_PRICE_TON)
    if not verified:
        raise HTTPException(400, "Payment verification failed")

    user.is_premium = True
    payment = Payment(
        user_id=user.id,
        amount_ton=PREMIUM_PRICE_TON,
        payment_type="premium",
        status="confirmed",
        tx_hash=req.tx_hash,
    )
    session.add(payment)
    await session.commit()

    logger.info(f"Premium activated for user {user.telegram_id}")
    return {"status": "ok", "is_premium": True}


@router.post("/boost")
async def buy_boost(
    req: BoostRequest,
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    price = BOOST_PRICES.get(req.boost_type)
    if not price:
        raise HTTPException(400, "Invalid boost type")

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    verified = await verify_ton_payment(req.tx_hash, price)
    if not verified:
        raise HTTPException(400, "Payment verification failed")

    payment = Payment(
        user_id=user.id,
        amount_ton=price,
        payment_type=f"boost_{req.boost_type}",
        status="confirmed",
        tx_hash=req.tx_hash,
    )
    session.add(payment)
    await session.commit()

    return {"status": "ok", "boost": req.boost_type}


async def verify_ton_payment(tx_hash: str, expected_amount: float) -> bool:
    """Verify TON transaction."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{TONCENTER_URL}/getTransaction",
                params={"hash": tx_hash},
            )
            data = resp.json()
            # Check destination and amount
            if not data.get("ok"):
                return False
            msg = data["result"][0]["out_msgs"][0]
            return (
                msg.get("destination") == TON_WALLET
                and float(msg.get("value", 0)) / 1e9 >= expected_amount * 0.95
            )
    except Exception as e:
        logger.error(f"Payment verification error: {e}")
        return False