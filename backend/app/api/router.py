"""API router."""
from fastapi import APIRouter
from app.api.endpoints import auth, users, rounds, trading, leaderboard, payments

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(rounds.router, prefix="/rounds", tags=["rounds"])
api_router.include_router(trading.router, prefix="/trading", tags=["trading"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])