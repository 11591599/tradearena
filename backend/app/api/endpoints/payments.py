"""TON payment endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.api.endpoints.users import get_current_user
from app.models.user import User

router = APIRouter()


class PremiumRequest(BaseModel):
    ton_amount: float
    tx_hash: str


@router.post("/premium")
async def activate_premium(req: PremiumRequest, user: User = Depends(get_current_user)):
    """Activate premium after TON payment."""
    # TODO: Verify transaction on TON blockchain
    # For now, just activate premium
    from app.core.database import async_session
    async with async_session() as session:
        await session.execute(
            User.__table__.update().where(User.id == user.id).values(is_premium=True)
        )
        await session.commit()
    return {"status": "activated", "user_id": user.id, "premium": True}


@router.get("/wallet")
async def get_payment_wallet():
    """Get wallet address for payments."""
    return {"wallet_address": settings.TON_WALLET_ADDRESS}
