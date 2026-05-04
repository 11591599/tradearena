"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_WEBAPP_URL: str = "http://localhost:3000"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://tradearena:secret@db:5432/tradearena"
    REDIS_URL: str = "redis://redis:6379/0"

    # Coinbase
    COINBASE_API_KEY: str = ""
    COINBASE_API_SECRET: str = ""
    COINBASE_PASSPHRASE: str = ""

    # TON
    TON_WALLET_ADDRESS: str = ""
    TON_API_KEY: str = ""
    TONCENTER_API_URL: str = "https://toncenter.com/api/v2"

    # JWT
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # Game
    STARTING_BALANCE: float = 10000.0
    ROUND_DURATION_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
