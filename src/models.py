"""SQLAlchemy models for TradeArena."""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum
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
    is_premium = Column(Boolean, default=False)
    referred_by = Column(Integer, nullable=True)
    referral_code = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    trades = relationship("Trade", back_populates="user")
    payments = relationship("Payment", back_populates="user")


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