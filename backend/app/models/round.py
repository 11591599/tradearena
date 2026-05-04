"""Trading round model."""
from sqlalchemy import String, Float, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.models.base import Base, TimestampMixin


class Round(TimestampMixin, Base):
    __tablename__ = "rounds"

    status: Mapped[str] = mapped_column(String, default="waiting")  # waiting, active, finished
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    prize_pool_ton: Mapped[float] = mapped_column(Float, default=0.0)
    participants_count: Mapped[int] = mapped_column(Integer, default=0)
