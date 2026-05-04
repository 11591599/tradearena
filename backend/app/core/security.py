"""JWT & Telegram auth."""
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_telegram_webapp(init_data: str) -> dict:
    """Verify Telegram WebApp init_data."""
    from urllib.parse import parse_qs
    parsed = parse_qs(init_data)
    hash_val = parsed.get("hash", [""])[0]
    if not hash_val:
        return {}
    parsed.pop("hash", None)
    check_string = "\n".join(f"{k}={v[0]}" for k, v in sorted(parsed.items()))
    secret_key = hmac.new(
        "WebAppData".encode(), settings.TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256
    ).digest()
    computed = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    if computed != hash_val:
        return {}
    return {k: v[0] for k, v in parsed.items()}
