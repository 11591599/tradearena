"""Database setup and session management."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from loguru import logger
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./tradearena.db")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    """Create all tables."""
    from src.models import User, Round, Trade, Payment  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")


async def get_session():
    """Dependency for getting DB sessions."""
    async with async_session() as session:
        yield session