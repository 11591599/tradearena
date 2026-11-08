"""SQLAlchemy models for TradeArena."""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    balance = Column(Float, default=10000.0)
    starting_balance = Column(Float, default=10000.0)
    total_pnl = Column(Float, default=0.0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    credits = Column(Float, default=150.0)
    tickets = Column(Integer, default=5)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    battle_wins = Column(Integer, default=0)
    mission_streak = Column(Integer, default=0)
    is_premium = Column(Boolean, default=False)
    referred_by = Column(Integer, nullable=True)
    referral_code = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    trades = relationship("Trade", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    missions = relationship("UserMission", back_populates="user")
    battle_entries = relationship("BattleEntry", back_populates="user")


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    mission_type = Column(String, default="daily")
    target = Column(Integer, default=1)
    reward_credits = Column(Float, default=50.0)
    reward_tickets = Column(Integer, default=1)
    reward_xp = Column(Integer, default=25)
    difficulty = Column(String, default="easy")
    is_daily = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_progress = relationship("UserMission", back_populates="mission")


class UserMission(Base):
    __tablename__ = "user_missions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    progress = Column(Integer, default=0)
    target = Column(Integer, default=1)
    status = Column(String, default="available")
    claimed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="missions")
    mission = relationship("Mission", back_populates="user_progress")


class Battle(Base):
    __tablename__ = "battles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    status = Column(String, default="open")
    entry_ticket_cost = Column(Integer, default=1)
    prize_credits = Column(Float, default=200.0)
    starts_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ends_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    entries = relationship("BattleEntry", back_populates="battle")


class BattleEntry(Base):
    __tablename__ = "battle_entries"

    id = Column(Integer, primary_key=True)
    battle_id = Column(Integer, ForeignKey("battles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, default=0)
    final_rank = Column(Integer, nullable=True)
    status = Column(String, default="joined")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    battle = relationship("Battle", back_populates="entries")
    user = relationship("User", back_populates="battle_entries")


class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True)
    status = Column(String, default="waiting")  # waiting, active, finished
    symbol = Column(String, default="BTC-USDT")
    start_price = Column(Float, nullable=True)
    end_price = Column(Float, nullable=True)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=60)
    prize_pool = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    trades = relationship("Trade", back_populates="round")


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    round_id = Column(Integer, ForeignKey("rounds.id"))
    symbol = Column(String, default="BTC-USDT")
    side = Column(String)  # buy, sell
    amount = Column(Float)
    price = Column(Float)
    pnl = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="trades")
    round = relationship("Round", back_populates="trades")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount_ton = Column(Float)
    amount_stars = Column(Integer, nullable=True)
    payment_type = Column(String)  # premium, boost
    status = Column(String, default="pending")  # pending, confirmed, failed
    tx_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="payments")


DEFAULT_MISSIONS = [
    {
        "title": "Daily login",
        "description": "Open the app once today.",
        "mission_type": "daily",
        "target": 1,
        "reward_credits": 50.0,
        "reward_tickets": 1,
        "reward_xp": 15,
        "difficulty": "easy",
        "is_daily": True,
    },
    {
        "title": "Trade streak",
        "description": "Place your first trade in the arena.",
        "mission_type": "trade",
        "target": 1,
        "reward_credits": 80.0,
        "reward_tickets": 2,
        "reward_xp": 30,
        "difficulty": "medium",
        "is_daily": False,
    },
    {
        "title": "Battle entry",
        "description": "Join a ranked battle room.",
        "mission_type": "battle",
        "target": 1,
        "reward_credits": 120.0,
        "reward_tickets": 2,
        "reward_xp": 40,
        "difficulty": "medium",
        "is_daily": False,
    },
    {
        "title": "Arena legend",
        "description": "Win 3 battles in total.",
        "mission_type": "wins",
        "target": 3,
        "reward_credits": 220.0,
        "reward_tickets": 3,
        "reward_xp": 90,
        "difficulty": "hard",
        "is_daily": False,
    },
]


DEFAULT_BATTLES = [
    {
        "title": "Shadow duel",
        "description": "Fast head-to-head match for sharp traders.",
        "status": "open",
        "entry_ticket_cost": 1,
        "prize_credits": 250.0,
    },
    {
        "title": "Vault rush",
        "description": "A riskier battle for players with momentum.",
        "status": "open",
        "entry_ticket_cost": 2,
        "prize_credits": 500.0,
    },
    {
        "title": "Legend circuit",
        "description": "Elite pass for top performers and veterans.",
        "status": "open",
        "entry_ticket_cost": 3,
        "prize_credits": 900.0,
    },
]


__all__ = [
    "User",
    "Mission",
    "UserMission",
    "Battle",
    "BattleEntry",
    "Round",
    "Trade",
    "Payment",
    "DEFAULT_MISSIONS",
    "DEFAULT_BATTLES",
    "Base",
]
