"""User model."""
from sqlalchemy import String, Float, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    balance_usd: Mapped[float] = mapped_column(Float, default=10000.0)
    total_pnl: Mapped[float] = mapped_column(Float, default=0.0)
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    referral_code: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    referred_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
