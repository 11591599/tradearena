"""Trade model."""
from sqlalchemy import String, Float, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin


class Trade(TimestampMixin, Base):
    __tablename__ = "trades"

    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    round_id: Mapped[int] = mapped_column(Integer, index=True)
    symbol: Mapped[str] = mapped_column(String, default="BTC-USDT")
    side: Mapped[str] = mapped_column(String)  # buy, sell
    amount: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    pnl: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String, default="open")  # open, closed
