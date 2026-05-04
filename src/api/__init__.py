from fastapi import APIRouter
from src.api.auth import router as auth_router
from src.api.game import router as game_router
from src.api.leaderboard import router as leaderboard_router
from src.api.payments import router as payments_router
from src.api.prices import router as prices_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(game_router, prefix="/game", tags=["game"])
router.include_router(leaderboard_router, prefix="/leaderboard", tags=["leaderboard"])
router.include_router(payments_router, prefix="/payments", tags=["payments"])
router.include_router(prices_router, prefix="/prices", tags=["prices"])