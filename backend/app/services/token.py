from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


def create_access_token(telegram_id: int) -> str:
    """Create JWT access token."""
    expire_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    payload = {
        "sub": str(telegram_id),
        "exp": expire_at,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int:
    """Decode JWT access token and return Telegram ID."""
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    return int(payload["sub"])
