"""Game-play API: missions, battles, wallet & progression."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models import User, Mission, UserMission, Battle, BattleEntry, DEFAULT_MISSIONS, DEFAULT_BATTLES

router = APIRouter()


class MissionClaimRequest(BaseModel):
    mission_id: int


async def ensure_seed_data(session: AsyncSession) -> None:
    """Ensure default missions and battles exist."""
    missions = (await session.execute(select(Mission))).scalars().all()
    if not missions:
        for item in DEFAULT_MISSIONS:
            session.add(Mission(**item))

    battles = (await session.execute(select(Battle))).scalars().all()
    if not battles:
        for item in DEFAULT_BATTLES:
            session.add(Battle(**item))

    await session.commit()


@router.get("/dashboard")
async def user_dashboard(user_id: int, session: AsyncSession = Depends(get_session)):
    """Return a compact profile summary for the Telegram Mini App."""
    await ensure_seed_data(session)
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "balance": round(user.balance, 2),
            "credits": round(user.credits, 2),
            "tickets": user.tickets,
            "xp": user.xp,
            "level": user.level,
            "battle_wins": user.battle_wins,
            "mission_streak": user.mission_streak,
            "is_premium": user.is_premium,
        },
        "summary": {
            "daily_mission_ready": True,
            "active_battles": 3,
            "next_reward_window": "24h",
        },
    }


@router.get("/missions")
async def list_missions(user_id: int, session: AsyncSession = Depends(get_session)):
    """List missions with user progress and reward info."""
    await ensure_seed_data(session)
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    missions = (await session.execute(select(Mission))).scalars().all()
    result = []
    for mission in missions:
        progress = await session.execute(
            select(UserMission).where(UserMission.user_id == user.id, UserMission.mission_id == mission.id)
        )
        progress_entry = progress.scalar_one_or_none()
        if progress_entry is None:
            progress_entry = UserMission(
                user_id=user.id,
                mission_id=mission.id,
                target=mission.target,
                progress=0,
                status="available",
            )
            session.add(progress_entry)
            await session.commit()

        result.append({
            "id": mission.id,
            "title": mission.title,
            "description": mission.description,
            "mission_type": mission.mission_type,
            "difficulty": mission.difficulty,
            "reward_credits": mission.reward_credits,
            "reward_tickets": mission.reward_tickets,
            "reward_xp": mission.reward_xp,
            "target": mission.target,
            "progress": progress_entry.progress,
            "status": progress_entry.status,
            "is_daily": mission.is_daily,
        })

    return {"missions": result}


@router.post("/missions/claim")
async def claim_mission(req: MissionClaimRequest, user_id: int, session: AsyncSession = Depends(get_session)):
    """Claim completed mission rewards."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    mission = await session.get(Mission, req.mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    progress = await session.execute(
        select(UserMission).where(UserMission.user_id == user.id, UserMission.mission_id == mission.id)
    )
    progress_entry = progress.scalar_one_or_none()
    if progress_entry is None:
        progress_entry = UserMission(
            user_id=user.id,
            mission_id=mission.id,
            target=mission.target,
            progress=0,
            status="available",
        )
        session.add(progress_entry)
        await session.commit()

    if progress_entry.status == "claimed":
        raise HTTPException(status_code=400, detail="Mission already claimed")

    if progress_entry.progress < mission.target:
        raise HTTPException(status_code=400, detail="Mission is not completed yet")

    user.credits += mission.reward_credits
    user.tickets += mission.reward_tickets
    user.xp += mission.reward_xp
    user.level = max(1, user.level + (mission.reward_xp // 50))
    user.mission_streak += 1
    progress_entry.status = "claimed"
    progress_entry.claimed_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    await session.commit()

    return {
        "status": "claimed",
        "credits_awarded": mission.reward_credits,
        "tickets_awarded": mission.reward_tickets,
        "xp_awarded": mission.reward_xp,
        "new_level": user.level,
    }


@router.get("/battles")
async def list_battles(user_id: int, session: AsyncSession = Depends(get_session)):
    """Return current open battle rooms."""
    await ensure_seed_data(session)
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    battles = (await session.execute(select(Battle))).scalars().all()
    result = []
    for battle in battles:
        result.append({
            "id": battle.id,
            "title": battle.title,
            "description": battle.description,
            "status": battle.status,
            "entry_ticket_cost": battle.entry_ticket_cost,
            "prize_credits": battle.prize_credits,
            "participants": len(battle.entries),
        })
    return {"battles": result}


@router.post("/battles/{battle_id}/join")
async def join_battle(battle_id: int, user_id: int, session: AsyncSession = Depends(get_session)):
    """Join a battle room and pay tournament entry ticket cost."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    battle = await session.get(Battle, battle_id)
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")

    if user.tickets < battle.entry_ticket_cost:
        raise HTTPException(status_code=400, detail="Not enough tickets to join")

    existing = await session.execute(
        select(BattleEntry).where(BattleEntry.user_id == user.id, BattleEntry.battle_id == battle.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="You already joined this battle")

    user.tickets -= battle.entry_ticket_cost
    battle_entry = BattleEntry(battle_id=battle.id, user_id=user.id, score=0, status="joined")
    session.add(battle_entry)
    await session.commit()

    return {
        "status": "joined",
        "battle_id": battle.id,
        "remaining_tickets": user.tickets,
        "entry_cost": battle.entry_ticket_cost,
    }


@router.post("/battles/{battle_id}/resolve")
async def resolve_battle(battle_id: int, user_id: int, score: int, session: AsyncSession = Depends(get_session)):
    """Resolve a user score in a battle and reward credits.|"""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    battle = await session.get(Battle, battle_id)
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")

    entry = await session.execute(
        select(BattleEntry).where(BattleEntry.user_id == user.id, BattleEntry.battle_id == battle.id)
    )
    entry = entry.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="User did not join this battle")

    entry.score = score
    battle.status = "closed"
    if score > 0:
        user.credits += battle.prize_credits
        user.battle_wins += 1
        user.xp += 60
        entry.status = "won"
    else:
        entry.status = "completed"

    await session.commit()
    return {"status": "resolved", "battle_id": battle.id, "score": score, "credits_awarded": battle.prize_credits if score > 0 else 0}


@router.get("/wallet")
async def wallet(user_id: int, session: AsyncSession = Depends(get_session)):
    """Return virtual wallet summary for the app."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "balance": round(user.balance, 2),
        "credits": round(user.credits, 2),
        "tickets": user.tickets,
        "currency": {
            "primary": "USDT",
            "game": "credits",
            "bonus_tickets": user.tickets,
        },
    }
